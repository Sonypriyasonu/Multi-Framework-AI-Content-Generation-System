import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

class Agent:
    def __init__(self, role, system_prompt):
        self.role = role
        self.system_prompt = system_prompt
    
    def execute(self, user_input):
        prompt = f"{self.system_prompt}\n\nTask: {user_input}"
        response = model.generate_content(prompt)
        return response.text

def content_pipeline(topic):
    # Initialize agents
    researcher = Agent(
        "Research Agent",
        "You are a research specialist. Collect comprehensive facts, benefits, challenges, and insights about topics."
    )
    
    writer = Agent(
        "Writing Agent",
        "You are a professional content writer. Create well-structured, engaging articles based on research data."
    )
    
    proofreader = Agent(
        "Proofreading Agent", 
        "You are an editor. Polish grammar, clarity, coherence, and structure without changing the core meaning."
    )
    
    summarizer = Agent(
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

st.title("🔥 Google AI SDK Content Generation")
st.write("Direct Google Generative AI SDK implementation")

topic = st.text_input("Enter a topic")

if st.button("Generate Content"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Google AI agents processing... ⏳"):
            result = content_pipeline(topic)
            
        st.subheader("📘 Research Results")
        st.write(result["research"])
        
        st.subheader("📝 Article Draft")
        st.write(result["article"])
        
        st.subheader("✨ Refined Article")
        st.write(result["refined"])
        
        st.subheader("📄 Summary")
        st.write(result["summary"])
