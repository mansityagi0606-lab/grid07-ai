import os
from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from tools import mock_searxng_search
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="openai/gpt-oss-120b",
    temperature=0.7
)

class GraphState(dict):
    pass


def decide_search(state):
    prompt = f"""
You are this persona:
{state['persona']}

Pick a trending topic and generate a short search query.
Return ONLY the query.
"""
    res = llm.invoke(prompt)
    return {"query": res.content.strip()}


def search(state):
    result = mock_searxng_search.invoke(state["query"])
    return {"context": result}


def draft_post(state):
    prompt = f"""
You are:
{state['persona']}

Context:
{state['context']}

Write a strong opinionated tweet under 280 chars.

STRICT JSON OUTPUT ONLY:
{{
"bot_id": "{state['bot_id']}",
"topic": "...",
"post_content": "..."
}}
"""
    res = llm.invoke(prompt)
    return {"final": res.content}


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("decide", decide_search)
    graph.add_node("search", search)
    graph.add_node("draft", draft_post)

    graph.set_entry_point("decide")

    graph.add_edge("decide", "search")
    graph.add_edge("search", "draft")

    return graph.compile()