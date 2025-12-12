import os
import streamlit as st
from dotenv import load_dotenv

from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI


# =================================
#     Load Environment Variables
# =================================
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY not found in .env file!")

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GOOGLE_API_KEY
)


# =================================
#     LangGraph State Definition
# =================================
class WorkflowState(TypedDict):
    topic: str
    research: Optional[str]
    article: Optional[str]
    refined: Optional[str]
    summary: Optional[str]


# =================================
#     AGENTS
# =================================

def research_agent(state: WorkflowState):
    """Find information, facts, and insights about the topic."""
    topic = state["topic"]

    messages = [
        SystemMessage(
            content="You are a research assistant. Collect reliable facts, background, "
                    "benefits, challenges, and key points about the topic."
        ),
        HumanMessage(content=f"Research the topic: {topic}")
    ]

    result = llm.invoke(messages)
    state["research"] = result.content
    return state


def writing_agent(state: WorkflowState):
    """Writes a detailed article based on the research."""
    research = state["research"]

    messages = [
        SystemMessage(
            content="You are a professional content writer. Write a clear, structured, "
                    "well-formatted article based on the research."
        ),
        HumanMessage(content=f"Write an article using this research:\n{research}")
    ]

    result = llm.invoke(messages)
    state["article"] = result.content
    return state


def proofreading_agent(state: WorkflowState):
    """Polishes grammar, clarity, and flow."""
    article = state["article"]

    messages = [
        SystemMessage(
            content="You are a proofreader. Improve grammar, clarity, coherence, and structure "
                    "WITHOUT changing meaning."
        ),
        HumanMessage(content=article)
    ]

    result = llm.invoke(messages)
    state["refined"] = result.content
    return state


def summary_agent(state: WorkflowState):
    """Creates a short summary of the refined article."""
    refined = state["refined"]

    messages = [
        SystemMessage(
            content="Create a short crisp summary of this article."
        ),
        HumanMessage(content=refined)
    ]

    result = llm.invoke(messages)
    state["summary"] = result.content
    return state


# =================================
#        Build LangGraph
# =================================
graph = StateGraph(WorkflowState)

graph.add_node("ResearchAgent", research_agent)
graph.add_node("WritingAgent", writing_agent)
graph.add_node("ProofreadingAgent", proofreading_agent)
graph.add_node("SummaryAgent", summary_agent)

graph.add_edge("__start__", "ResearchAgent")
graph.add_edge("ResearchAgent", "WritingAgent")
graph.add_edge("WritingAgent", "ProofreadingAgent")
graph.add_edge("ProofreadingAgent", "SummaryAgent")
graph.add_edge("SummaryAgent", "__end__")

workflow = graph.compile()


# =================================
#        Streamlit UI
# =================================
st.title("🧠 LangGraph Content Generation App")
st.write("""
Enter a topic → the system will perform:
1. Research  
2. Article Writing  
3. Proofreading  
4. Summary  
""")

topic = st.text_input("Enter a topic")

if st.button("Generate Content"):
    if not topic.strip():
        st.error("Please enter a topic.")
    else:
        with st.spinner("Generating... Please wait ⏳"):
            result = workflow.invoke({
                "topic": topic,
                "research": None,
                "article": None,
                "refined": None,
                "summary": None
            })

        st.subheader("📘 Research Results")
        st.write(result["research"])

        st.subheader("📝 Article Draft")
        st.write(result["article"])

        st.subheader("✨ Refined Article (Proofread)")
        st.write(result["refined"])

        st.subheader("📄 Short Summary")
        st.write(result["summary"])
