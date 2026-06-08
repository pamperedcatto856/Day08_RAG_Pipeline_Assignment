from pathlib import Path

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"


def load_corpus():
    corpus = []

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        content = md_file.read_text(encoding="utf-8")

        corpus.append({
            "content": content,
            "metadata": {
                "source": md_file.name,
                "type": "legal" if "legal" in str(md_file) else "news"
            }
        })

    return corpus


def build_bm25_index(corpus: list[dict]):
    """
    Xây dựng BM25 index từ corpus.

    Args:
        corpus: List of {'content': str, 'metadata': dict}
    """
    # TODO: Implement BM25 index
    #
    # from rank_bm25 import BM25Okapi
    #
    # # Tokenize - cho tiếng Việt nên dùng underthesea hoặc đơn giản split()
    # tokenized_corpus = [doc["content"].lower().split() for doc in corpus]
    # bm25 = BM25Okapi(tokenized_corpus)
    # return bm25
    raise NotImplementedError("Implement build_bm25_index")


def lexical_search(query: str, top_k: int = 10):

    corpus = load_corpus()

    bm25 = build_bm25_index(corpus)

    tokenized_query = query.lower().split()

    scores = bm25.get_scores(tokenized_query)

    import numpy as np

    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for idx in top_indices:
        if scores[idx] > 0:
            results.append({
                "content": corpus[idx]["content"],
                "score": float(scores[idx]),
                "metadata": corpus[idx]["metadata"]
            })

    return results

if __name__ == "__main__":
    # Test
    results = lexical_search("Điều 248 tàng trữ trái phép chất ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
    corpus = load_corpus()
    print(f"Loaded {len(corpus)} documents")