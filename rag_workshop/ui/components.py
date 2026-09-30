import streamlit as st


def render_status_badge(label: str, ok: bool, warning: bool = False):
    css_class = "status-pill"
    if warning:
        css_class += " warning"
    if not ok:
        css_class += " error"
    st.markdown(f'<span class="{css_class}">{label}</span>', unsafe_allow_html=True)


def render_retrieval_details(retrieval):
    if not retrieval:
        st.info("No relevant chunks passed the similarity threshold.")
        return

    for item in retrieval:
        with st.expander(f"Chunk {item['chunk_id']} • score {item['score']:.3f}"):
            st.write(f"Source: {item['source_file']}")
            st.write(f"Page: {item['page_number']}")
            st.write(item["text"])
