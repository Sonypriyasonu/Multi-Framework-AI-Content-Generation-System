import os
import streamlit as st
from dotenv import load_dotenv
import autogen
from autogen import ConversableAgent

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")

config_list = [
    {
        "model": "gemini-2.0-flash",
        "api_key": GOOGLE_API_KEY,
        "api_type": "google"
    }
]

llm_config = {"config_list": config_list, "temperature": 0.3}

# Define Agents
researcher = ConversableAgent(
    name="Researcher",
    system_message="You are a research specialist. Find comprehensive information, facts, and insights about topics.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

writer = ConversableAgent(
    name="Writer",
    system_message="You are a professional content writer. Create well-structured, engaging articles based on research.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

proofreader = ConversableAgent(
    name="Proofreader",
    system_message="You are an editor. Polish grammar, clarity, and flow without changing meaning.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

summarizer = ConversableAgent(
    name="Summarizer",
    system_message="You are a summarizer. Create concise summaries of articles.",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

def extract_text(response):
    """Extract text content from AutoGen response"""
    if isinstance(response, str):
        return response
    elif isinstance(response, dict) and "content" in response:
        return response["content"]
    else:
        return str(response)

def generate_content(topic):
    # Step 1: Research
    research_response = researcher.generate_reply(
        messages=[{"role": "user", "content": f"Research the topic: {topic}. Provide comprehensive information."}]
    )
    research_text = extract_text(research_response)
    
    # Step 2: Writing (using research output)
    article_response = writer.generate_reply(
        messages=[{"role": "user", "content": f"Write a detailed article based on this research:\n\n{research_text}"}]
    )
    article_text = extract_text(article_response)
    
    # Step 3: Proofreading (using article output)
    refined_response = proofreader.generate_reply(
        messages=[{"role": "user", "content": f"Proofread and refine this article:\n\n{article_text}"}]
    )
    refined_text = extract_text(refined_response)
    
    # Step 4: Summary (using refined article output)
    summary_response = summarizer.generate_reply(
        messages=[{"role": "user", "content": f"Create a brief summary of this article:\n\n{refined_text}"}]
    )
    summary_text = extract_text(summary_response)
    
    return {
        "research": research_text,
        "article": article_text,
        "refined": refined_text,
        "summary": summary_text
    }

st.title("🤖 AutoGen Content Generation App")
st.write("Multi-agent conversation using Microsoft AutoGen")

topic = st.text_input("Enter a topic")

if st.button("Generate Content"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("AutoGen agents collaborating... ⏳"):
            result = generate_content(topic)
            
        st.subheader("📘 Research")
        st.write(result["research"])
        
        st.subheader("📝 Article")
        st.write(result["article"])
        
        st.subheader("✨ Refined Article")
        st.write(result["refined"])
        
        st.subheader("📄 Summary")
        st.write(result["summary"])
