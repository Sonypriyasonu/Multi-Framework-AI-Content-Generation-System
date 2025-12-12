# Multi-Framework-AI-Content-Generation-System
Multi-Framework AI Content Generation System" is a unified demo showcasing identical 4-stage content pipelines (research → writing → proofreading → summarization) built across five AI frameworks: AutoGen, CrewAI, Google AI SDK, LangGraph, and OpenAI Agents.

# Project Description

This project demonstrates a **unified content-generation workflow** implemented across five different AI agent frameworks. Each module performs the same **4-stage pipeline**:

1. **Research**
2. **Article Writing**
3. **Proofreading / Refinement**
4. **Summarization**

The goal is to showcase how various agent frameworks and SDKs can be used to achieve **identical workflows** with different architectures and orchestration styles.

---

## 🚀 Frameworks Implemented

This repository includes **four fully working content-generation apps**, each built with **Streamlit** and powered by different AI technologies.

### 🔹 1. AutoGen (Microsoft AutoGen)
*A multi-agent content generator using `ConversableAgent` and **Gemini 2.0 Flash** via Google API.*

**Features:**
- Four collaborating AutoGen agents:
  `Researcher → Writer → Proofreader → Summarizer`
- Automatic message passing between agents
- Sequential orchestration of content pipeline
- Clean extraction of AutoGen response content

**Purpose:**
Shows how AutoGen handles agent collaboration, message routing, and multi-step generation.

---

### 🔹 2. CrewAI
*A crew-based workflow using `Crew`, `Agent`, and `Task` objects.*

**Features:**
- Four CrewAI agents with defined roles, goals, and backstories
- Tasks assigned to each agent for research, writing, editing, and summarization
- One-click kickoff of the entire agent workflow
- Access to individual task outputs (research, article, refinement, summary)

**Purpose:**
Demonstrates CrewAI’s task-oriented agent execution and workflow management.

---

### 🔹 3. Google AI SDK (Direct Gemini API)
*A minimalistic, SDK-only implementation using `google.generativeai`.*

**Features:**
- No framework — pure Gemini API calls
- Four simple agent classes: `Research`, `Writer`, `Editor`, `Summarizer`
- Direct prompt-based pipeline execution
- Clean and simple architecture

**Purpose:**
Shows how to build a custom agent workflow manually using only the Gemini SDK.

---

### 🔹 4. LangGraph
*A graph-based agent pipeline built using **LangGraph + LangChain Google GenAI**.*

**Features:**
- Node-based state management using `StateGraph`
- Four agent nodes: `Research → Writing → Proofreading → Summary`
- Deterministic workflow with edges defining execution order
- Typed state object storing outputs at every stage
- Perfect for production-grade, controlled multi-agent flows

**Purpose:**
Shows how to build structured and deterministic agent workflows using a graph-based state machine.

---

### 🔹 5. OpenAI Agents (GPT-4o Mini)
*A lightweight agent pipeline using the **OpenAI Chat Completions API**.*

**Features:**
- Four OpenAI-powered agents with system prompts
- GPT-4o Mini for fast, cost-efficient generation
- Mirrors the same pipeline: `research → article → refinement → summary`
- Clean class abstraction for reusable agent logic

**Purpose:**
Shows how to build modular agent architectures using only OpenAI’s API.

---

## 🧠 Why This Repository Is Useful

This project is ideal for:
✅ Learning how different AI agent frameworks implement multi-step workflows
✅ Comparing **AutoGen vs CrewAI vs LangGraph vs custom SDK agents**
✅ Building your own production-ready content pipeline
✅ Understanding prompt engineering across multiple frameworks
✅ Educational demos & benchmarking agent frameworks
