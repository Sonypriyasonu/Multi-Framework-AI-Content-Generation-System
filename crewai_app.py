import os
import streamlit as st
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")

llm = LLM(
    model="gemini/gemini-2.0-flash",
    api_key=GOOGLE_API_KEY
)

# Define Agents
researcher = Agent(
    role="Research Specialist",
    goal="Find comprehensive information about the given topic",
    backstory="Expert researcher with access to vast knowledge",
    llm=llm,
    verbose=False
)

writer = Agent(
    role="Content Writer",
    goal="Create well-structured articles based on research",
    backstory="Professional writer skilled in creating engaging content",
    llm=llm,
    verbose=False
)

proofreader = Agent(
    role="Editor",
    goal="Polish and refine written content",
    backstory="Meticulous editor focused on clarity and grammar",
    llm=llm,
    verbose=False
)

summarizer = Agent(
    role="Summarizer",
    goal="Create concise summaries of articles",
    backstory="Expert at distilling key information into brief summaries",
    llm=llm,
    verbose=False
)

def create_tasks(topic):
    research_task = Task(
        description=f"Research the topic: {topic}. Gather facts, benefits, challenges, and key insights.",
        agent=researcher,
        expected_output="Comprehensive research findings"
    )
    
    writing_task = Task(
        description="Write a detailed, well-structured article based on the research findings.",
        agent=writer,
        expected_output="Complete article draft"
    )
    
    proofreading_task = Task(
        description="Proofread and refine the article for grammar, clarity, and flow.",
        agent=proofreader,
        expected_output="Polished final article"
    )
    
    summary_task = Task(
        description="Create a concise summary of the refined article.",
        agent=summarizer,
        expected_output="Brief article summary"
    )
    
    return [research_task, writing_task, proofreading_task, summary_task]

st.title("🚀 CrewAI Content Generation App")
st.write("Multi-agent content creation using CrewAI")

topic = st.text_input("Enter a topic")

if st.button("Generate Content"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("CrewAI agents working... ⏳"):
            tasks = create_tasks(topic)
            crew = Crew(agents=[researcher, writer, proofreader, summarizer], tasks=tasks)
            result = crew.kickoff()
            
        # Extract clean content from CrewAI result
        if hasattr(result, 'raw'):
            content = result.raw
        elif hasattr(result, 'tasks_output') and result.tasks_output:
            # Get the last task output (summary)
            content = result.tasks_output[-1].raw if hasattr(result.tasks_output[-1], 'raw') else str(result.tasks_output[-1])
        else:
            content = str(result)
            
        st.subheader("📋 Final Result")
        st.write(content)
        
        # Show individual task outputs if available
        if hasattr(result, 'tasks_output') and len(result.tasks_output) >= 4:
            st.subheader("📘 Research")
            st.write(result.tasks_output[0].raw if hasattr(result.tasks_output[0], 'raw') else str(result.tasks_output[0]))
            
            st.subheader("📝 Article")
            st.write(result.tasks_output[1].raw if hasattr(result.tasks_output[1], 'raw') else str(result.tasks_output[1]))
            
            st.subheader("✨ Refined Article")
            st.write(result.tasks_output[2].raw if hasattr(result.tasks_output[2], 'raw') else str(result.tasks_output[2]))
            
            st.subheader("📄 Summary")
            st.write(result.tasks_output[3].raw if hasattr(result.tasks_output[3], 'raw') else str(result.tasks_output[3]))
