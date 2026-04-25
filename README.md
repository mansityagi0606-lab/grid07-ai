# Grid07-ai assignment
1. Routing posts to relevant bots using embeddings
2. Generating content using a LangGraph workflow
3. Handling argument replies using context (RAG) with some protection against prompt injection

## Phase 1: Persona-Based Routing
Three bot personas (Tech, Skeptic, Finance) are created and stored their embeddings using a sentence-transformer model.
When a new post comes in it is converted into an embedding its cosine similarity is calculated against each persona and bots above a certain threshold are selected

## Phase 2: LangGraph Content Generation
1. **Decide Search**
   The bot based on its persona decides what topic to post about and generates a search query

2. **Search**
   A mock search tool returns predefined news headlines based on keywords

3. **Draft Post**
   The LLM uses persona + search results to generate a short opinionated post

The output is structured as JSON:

* bot_id
* topic
* post_content

## Phase 3: RAG-Based Defense

For replies in a thread, the bot gets parent post, previous comments and latest human reply. All of this is passed into the prompt so the model has full context.

### Prompt Injection Handling

To prevent prompt injection the system prompt clearly tells the model to ignore any instruction that tries to change its role. It must always stay in the given persona
and Inputs like “ignore previous instructions” are treated as malicious
In testing, the bot continues the argument normally and does not follow such instructions.





