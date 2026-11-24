import os
import chromadb

print("Running from:", os.getcwd())
print("manual.pdf exists:", os.path.exists("data/manual/manual.pdf"))
print("chroma_manual exists:", os.path.exists("chroma_manual"))

client = chromadb.PersistentClient(path="chroma_manual")
print("Collections:", [c.name for c in client.list_collections()])
col = client.get_collection("product_manual")
print("Chunk count:", col.count())