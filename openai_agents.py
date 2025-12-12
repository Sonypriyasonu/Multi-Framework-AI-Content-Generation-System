import os
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY not found in .env file!")

client = OpenAI(api_key=OPENAI_API_KEY)

class OpenAIAgent:
    def __init__(self, role, system_prompt):
        self.role = role
        self.system_prompt = system_prompt
    
    def execute(self, user_input):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content

def openai_content_pipeline(topic):
    # Initialize OpenAI agents
    researcher = OpenAIAgent(
        "Research Agent",
        "You are a research specialist. Collect comprehensive facts, benefits, challenges, and insights about topics."
    )
    
    writer = OpenAIAgent(
        "Writing Agent",
        "You are a professional content writer. Create well-structured, engaging articles based on research data."
    )
    
    proofreader = OpenAIAgent(
        "Proofreading Agent", 
        "You are an editor. Polish grammar, clarity, coherence, and structure without changing the core meaning."
    )
    
    summarizer = OpenAIAgent(
        "Summary Agent",
        "You are a summarizer. Create concise, crisp summaries that capture the essence of articles."
    )
    
    # Execute pipeline
    research = researcher.execute(f"Research the topic: {topic}")
    article = writer.execute(f"Write an article using this research:\n{research}")
    refined = proofreader.execute(f"Proofread this article:\n{article}")
    summary = summarizer.execute(f"Summarize this article:\n{refined}")
    
    return {
        "research": research,
        "article": article,
        "refined": refined,
        "summary": summary
    }

st.title("🤖 OpenAI Agents Content Generation")
st.write("Multi-agent content creation using OpenAI API")

topic = st.text_input("Enter a topic")

if st.button("Generate Content"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("OpenAI agents processing... ⏳"):
            result = openai_content_pipeline(topic)
            
        st.subheader("📘 Research Results")
        st.write(result["research"])
        
        st.subheader("📝 Article Draft")
        st.write(result["article"])
        
        st.subheader("✨ Refined Article")
        st.write(result["refined"])
        
        st.subheader("📄 Summary")
        st.write(result["summary"])
