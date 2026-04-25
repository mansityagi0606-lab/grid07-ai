import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from tools import mock_searxng_search

load_dotenv()


class GraphState(TypedDict, total=False):
    bot_id: str
    persona: str
    query: str
    context: str
    final: str


# Initialize Groq
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b",
    temperature=0.7
)


# ---------------- NODE 1 ----------------
def decide_search(state: GraphState):
    persona = state["persona"]

    prompt = f"""
You are this persona:
{persona}

Pick a trending topic and generate a short search query.
Return ONLY the query.
"""

    res = llm.invoke(prompt)
    query = res.content.strip()

    print("\n[Node: Decide] Query:", query)

    return {"query": query}   


# ---------------- NODE 2 ----------------
def search(state: GraphState):
    print("\n[Node: Search] State:", state)

    query = state["query"]

    result = mock_searxng_search.invoke(query)

    print("[Node: Search] Result:", result)

    return {"context": result}


# ---------------- NODE 3 ----------------
def draft_post(state: GraphState):
    prompt = f"""
You are:
{state['persona']}

Context:
{state['context']}

Write a strong opinionated tweet under 280 characters.

STRICT JSON OUTPUT ONLY:
{{
  "bot_id": "{state['bot_id']}",
  "topic": "...",
  "post_content": "..."
}}
"""

    res = llm.invoke(prompt)

    print("\n[Node: Draft] Output:", res.content)

    return {"final": res.content}


# ---------------- GRAPH ----------------
def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("decide", decide_search)
    graph.add_node("search", search)
    graph.add_node("draft", draft_post)

    graph.set_entry_point("decide")

    graph.add_edge("decide", "search")
    graph.add_edge("search", "draft")

    return graph.compile()