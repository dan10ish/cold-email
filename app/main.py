import streamlit as st
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
import asyncio
import tempfile
from chains import Chain
from utils import clean_text

def set_custom_style():
    st.markdown("""
        <style>

        html, body, [class*="css"] {
          font-family: monospace !important;
        }

        .stTitle {
            color: #1E1E1E;
            font-weight: 700;
            font-size: 2.5rem !important;
            padding-bottom: 0rem;
            font-family: monospace !important;
        }

        .stTextInput{
          padding: 0.5rem;
        }

        .stTextInput > div > div > input {
            font-family: monospace;
            padding: 0.5rem;
            border-radius: 8px;
            font-size: 0.85rem !important;
        }

        .stFileUploader > div > button {
            font-family: monospace;
            padding: 1rem;
            border-radius: 8px;
        }

        .stButton > button {
            font-family: monospace;
            color: white;
            padding: 0.75rem 2rem;
            border-radius: 8px;
            border: none;
            transition: all 0.3s ease;
        }

        .stButton > button:hover {
            background-color: #1E1E1E;
            color: #ADD8E6;
        }

        footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            color: #bbbbbb;
            padding: 1rem;
            text-align: center;
            z-index: 1000;
            font-size: 1rem;
        }

        footer a {
            color: white;
            text-decoration: none;
            border-bottom: 1px solid transparent;
            transition: all 0.3s ease;
        }

        footer a:hover {
            color: #E9ECEF;
            text-decoration: none;
        }

        .result-container {
            border-radius: 8px;
            padding: 1.5rem;
            margin-top: 2rem;
        }

        .loader {
            border: 4px solid #f3f3f3;
            border-radius: 50%;
            border-top: 4px solid #1E1E1E;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 2rem auto;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        </style>
    """, unsafe_allow_html=True)

def create_footer():
    st.markdown("""
        <footer>
            Made by <a href="https://danish.bio" target="_blank">Danish</a> |
            <a href="https://github.com/dan10ish/coldmailbot" target="_blank">Source Code</a>
        </footer>
    """, unsafe_allow_html=True)

def create_streamlit_app(llm, clean_text):
    set_custom_style()

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.title("Cold Email Generator")

    st.markdown("""
        Generate personalized cold emails for job applications by providing a job posting URL
        and your resume. The AI will analyze both and create a tailored email.
    """)

    url_input = st.text_input(
        "Job Posting URL",
        value="https://www.google.com/about/careers/",
        placeholder="Enter the job posting URL here..."
    )

    resume_file = st.file_uploader(
        'Upload Your Resume (PDF)',
        type="pdf",
        help="Upload your resume in PDF format"
    )

    extracted_resume_text = ""
    if resume_file:
        with st.spinner("Processing resume..."):
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
                st.success("Resume processed successfully!")
            except Exception as e:
                st.error(f"Error reading resume: {e}")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        submit_button = st.button("Generate Email", use_container_width=True)

    if submit_button:
        if not resume_file:
            st.warning("Please upload your resume first.")
        else:
            try:
                with st.spinner("Analyzing job posting and generating email..."):
                    loader = WebBaseLoader([url_input])
                    data = clean_text(loader.load().pop().page_content)
                    jobs = llm.extract_jobs(data)
                    email = llm.write_mail(jobs, extracted_resume_text)

                    st.markdown('<div class="result-container">', unsafe_allow_html=True)
                    st.markdown("### Generated Email")
                    st.code(email, language='markdown')
                    st.markdown('</div>', unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
    create_footer()

if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="ColdMailBot - AI Email Generator",
        page_icon="📧",
        initial_sidebar_state="collapsed"
    )
    chain = Chain()
    create_streamlit_app(chain, clean_text)
