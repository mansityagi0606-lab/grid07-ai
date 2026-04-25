import numpy as np
from personas import PERSONAS
from utils import embed

# Precompute persona embeddings
persona_embeddings = {
    bot_id: embed(text)
    for bot_id, text in PERSONAS.items()
}

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def route_post_to_bots(post_content: str, threshold: float = 0.3):
    post_emb = embed(post_content)

    matched = []

    for bot_id, p_emb in persona_embeddings.items():
        sim = cosine_similarity(post_emb, p_emb)
        print(f"{bot_id} similarity:", sim)  # DEBUG
        if sim > threshold:
            matched.append((bot_id, round(sim, 3)))

    return matched