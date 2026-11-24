import streamlit as st

st.set_page_config(page_title="Smart FAQ Bot", page_icon="📘")

from rag_core import answer_with_rag, get_collection


@st.cache_resource(show_spinner="Building the manual index (first run only)...")
def ensure_index():
    """Build the ChromaDB index from the manual if it doesn't exist yet (needed on the cloud)."""
    try:
        if get_collection().count() > 0:
            return True
    except Exception:
        pass
    import ingest_manual
    import rag_core
    ingest_manual.main()
    rag_core._collection = None  # force reload of the fresh collection
    return True


ensure_index()

st.title("📘 Smart FAQ Bot for Product Manuals")
st.caption("Answers come only from the loaded product manual, with page references.")
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("sources"):
            with st.expander("Sources used"):
                for s in m["sources"]:
                    st.caption(f"**Page {s['page']}** (distance {s['distance']}): {s['text'][:300]}...")

question = st.chat_input("Ask a question about the product...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching the manual..."):
            try:
                result = answer_with_rag(question)
            except Exception as e:
                result = {"answer": f"Something went wrong: {e}", "sources": []}
        st.markdown(result["answer"])
        if result["sources"]:
            with st.expander("Sources used"):
                for s in result["sources"]:
                    st.caption(f"**Page {s['page']}** (distance {s['distance']}): {s['text'][:300]}...")

    st.session_state.messages.append(
        {"role": "assistant", "content": result["answer"], "sources": result["sources"]}
    )