import streamlit as st

from dom_scrapping_tutorial.main import dom_scrapping


# Streamlit app
def main():
    st.title("URL Summarizer")

    # Input for the URL
    url = st.text_input("Enter a URL:")

    if url:
        st.write("Fetching content and summarizing...")

        # Add progress bar
        with st.spinner("Fetching content and summarizing..."):
            # Fetch content from URL
            try:
                summary = dom_scrapping(url=url)
                st.write(summary)
            except Exception as e:
                st.error(e)


if __name__ == "__main__":
    main()
