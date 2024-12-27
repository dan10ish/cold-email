import streamlit as st
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
import asyncio
import tempfile
from chains import Chain
from utils import clean_text

def create_streamlit_app(llm, clean_text):
    st.title("Cold Email Generator")
    url_input = st.text_input("Enter the job posting URL:", value="https://www.google.com/about/careers/")
    resume_file = st.file_uploader('Choose your resume', type="pdf")
    submit_button = st.button("Submit")

    extracted_resume_text = ""

    if resume_file:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(resume_file.read())
                temp_file_path = temp_file.name

            loader = PyPDFLoader(temp_file_path)
            pages = []

            async def extract_pdf_text():
                async for page in loader.alazy_load():
                    pages.append(page.page_content)

            asyncio.run(extract_pdf_text())

            extracted_resume_text = "\n".join(pages)

        except Exception as e:
            st.error(f"Error reading resume: {e}")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)
            email = llm.write_mail(jobs, extracted_resume_text)
            st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Cold Email", page_icon="📧")
    create_streamlit_app(chain, clean_text)
