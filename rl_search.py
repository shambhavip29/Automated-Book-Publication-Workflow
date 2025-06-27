import random
from vector_score.chroma_utils import search_chromadb


def epsilon_greedy_search(query, epsilon=0.2):
    results = search_chromadb(query, n_results=10)  # already filtered results

    if not results:
        print(" No relevant results found.")
        return []

    # Apply epsilon-greedy to reorder results (optional)
    if random.random() < epsilon:
        first = random.choice(results)
        print(" [Exploration] Random choice made:")
    else:
        first = results[0]
        print("[Exploitation] Top match returned:")

    print(f"\n {first}")
    return [first] + [r for r in results if r != first][:2]
