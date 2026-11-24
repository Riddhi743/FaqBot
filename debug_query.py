import sys
from rag_core import retrieve_context

q = " ".join(sys.argv[1:]) or "How do I clean the basket?"
for c in retrieve_context(q, 5):
    print(f"distance={c['distance']}  page={c['page']}")
    print("   ", c["text"][:200].replace("\n", " "))
    print()