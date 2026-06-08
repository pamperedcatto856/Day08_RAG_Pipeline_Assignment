
def semantic_search(query: str, top_k: int = 10) -> list[dict]:
    """
    Tìm kiếm ngữ nghĩa sử dụng vector similarity.

    Args:
        query: Câu truy vấn
        top_k: Số lượng kết quả tối đa

    Returns:
        List of {
            'content': str,      # Nội dung chunk
            'score': float,      # Cosine similarity score
            'metadata': dict     # source, doc_type, chunk_index
        }
        Sorted by score descending.
    """
    import weaviate
    from weaviate.classes.query import MetadataQuery
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer("BAAI/bge-m3")
    query_embedding = model.encode(query).tolist()
    
    client = weaviate.connect_to_local()
    try:
        collection = client.collections.get("DrugLawDocs")

        results = collection.query.near_vector(
            near_vector=query_embedding,
            limit=top_k,
            return_metadata=MetadataQuery(distance=True)
        )

        return [
            {
                "content": obj.properties["content"],
                "score": 1 - obj.metadata.distance,
                "metadata": {
                    "source": obj.properties["source"],
                    "doc_type": obj.properties.get("doc_type"),
                    "chunk_index": obj.properties.get("chunk_index")
                }
            }
            for obj in results.objects
        ]

    finally:
        client.close()
        


if __name__ == "__main__":
    # Test
    results = semantic_search("hình phạt cho tội tàng trữ ma tuý", top_k=5)
    for r in results:
        print(f"[{r['score']:.3f}] {r['content'][:100]}...")
