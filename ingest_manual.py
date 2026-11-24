import chromadb
from pypdf import PdfReader

PDF_PATH = "data/manual/manual.pdf"
DB_PATH = "chroma_manual"
COLLECTION = "product_manual"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150


def main():
    reader = PdfReader(PDF_PATH)
    docs, metas, ids = [], [], []

    for page_no, page in enumerate(reader.pages, start=1):
        text = " ".join((page.extract_text() or "").split())
        start, i = 0, 0
        while start < len(text):
            piece = text[start:start + CHUNK_SIZE]
            if len(piece.strip()) > 40:
                docs.append(piece)
                metas.append({"source": "manual.pdf", "page": page_no})
                ids.append(f"p{page_no}-c{i}")
                i += 1
            start += CHUNK_SIZE - CHUNK_OVERLAP

    if not docs:
        print("No text found. The PDF may be a scanned image.")
        return

    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    col = client.create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})

    for i in range(0, len(docs), 100):
        col.add(documents=docs[i:i+100], metadatas=metas[i:i+100], ids=ids[i:i+100])

    print(f"Indexed {len(docs)} chunks from {len(reader.pages)} pages.")


if __name__ == "__main__":
    main()