from langchain.tools import tool

@tool
def mock_searxng_search(query: str) -> str:
    """
    Simulates a search engine. Returns recent news headlines based on query keywords.
    """

    q = query.lower()

    if "crypto" in q:
        return "Bitcoin hits new ATH after ETF approvals."

    if "ai" in q:
        return "New AI model surpasses junior developers in coding benchmarks."

    if "market" in q:
        return "Federal Reserve signals interest rate cuts amid slowdown."

    return "Global uncertainty continues across tech and economy."