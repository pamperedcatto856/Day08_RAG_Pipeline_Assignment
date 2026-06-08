import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY", "")

STANDARDIZED_DIR = Path(__file__).parent.parent / "data" / "standardized"

DOCUMENT_IDS = []


def upload_documents():
    """
    Upload toàn bộ file markdown lên PageIndex.

    Returns:
        List[str]: danh sách document IDs
    """
    from pageindex import PageIndexClient

    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    doc_ids = []

    for md_file in STANDARDIZED_DIR.rglob("*.md"):
        try:
            result = client.submit_document(
            file_path=str(md_file)
        )
            print(result)
            doc_id = (
                result.get("doc_id")
                or result.get("id")
                or result.get("document_id")
            )

            if doc_id:
                doc_ids.append(doc_id)

            print(f"✓ Uploaded: {md_file.name}")

        except Exception as e:
            print(f"✗ Failed: {md_file.name}")
            print(f"  Error: {e}")

    return doc_ids

def pageindex_search(
    query: str,
    doc_ids: list[str] | None = None,
    top_k: int = 5,
) -> list[dict]:

    from pageindex import PageIndexClient

    client = PageIndexClient(api_key=PAGEINDEX_API_KEY)

    if not doc_ids:
        return []

    all_results = []

    for doc_id in doc_ids:
        try:
            response = client.submit_query(
                doc_id=doc_id,
                query=query,
            )

            all_results.append(
                {
                    "content": str(response),
                    "score": 1.0,
                    "metadata": {
                        "doc_id": doc_id
                    },
                    "source": "pageindex",
                }
            )

        except Exception as e:
            print(f"Query failed for {doc_id}: {e}")

    return all_results[:top_k]

if __name__ == "__main__":
    if not PAGEINDEX_API_KEY:
        print("⚠ Hãy set PAGEINDEX_API_KEY trong .env")

    else:
        print("Uploading documents...")

        doc_ids = upload_documents()

        print(f"\nUploaded {len(doc_ids)} documents")

        print("\nTesting search...\n")

        results = pageindex_search(
            "hình phạt sử dụng ma tuý",
            doc_ids,
            top_k=3,
        )

        for r in results:
            print(r["content"][:200])
            print("-" * 80)