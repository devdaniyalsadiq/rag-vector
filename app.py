import streamlit as st
from dotenv import load_dotenv
import pickle
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.callbacks import get_openai_callback
import os

load_dotenv()
st.set_page_config(page_title='💬 Tradedive Chat App - GPT')

def main():
    st.header("Talk to your PDF 💬")
    openai_key = os.environ.get("OPENAI_API_KEY")
    store_name = 'finalCopy'

    # Check if the pickle file exists
    if os.path.exists(f"./{store_name}.pkl"):
        with open(f"{store_name}.pkl", "rb") as f:
            VectorStore = pickle.load(f)
    else:
        # Process PDF and create pickle file
        pdf_path = r'./finalCopy.pdf'
        if os.path.exists(pdf_path):
            pdf_reader = PdfReader(pdf_path)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""

            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, length_function=len)
            chunks = text_splitter.split_text(text=text)

            embeddings = OpenAIEmbeddings()
            VectorStore = FAISS.from_texts(chunks, embedding=embeddings)
            with open(f"{store_name}.pkl", "wb") as f:
                pickle.dump(VectorStore, f)
        else:
            st.error("PDF file not found.")
            return

    # Interface for querying the PDF content
    st.header("Tradedive Custom Chat GPT:")
    query = st.text_input("Questions", value="Tell me about the content of the PDF")

    if st.button("Ask") and query:
        if not openai_key:
            st.error('Warning: Please set your OPEN AI API KEY in the environment.')
            return

        docs = VectorStore.similarity_search(query=query, k=3)

        llm = OpenAI()
        chain = load_qa_chain(llm=llm, chain_type="stuff")
        with get_openai_callback() as cb:
            response = chain.run(input_documents=docs, question=query)
        
        st.header("Answer:")
        st.markdown(f"<pre>{response}</pre>", unsafe_allow_html=True)

        st.write('--')
        st.header("OpenAI API Usage:")
        st.text(str(cb))

if __name__ == '__main__':
    main()
