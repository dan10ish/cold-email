import streamlit as st
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
import asyncio
import tempfile
from chains import Chain
from utils import clean_text

st.set_page_config(
    layout="wide",
    page_title="MailBot - AI Email Generator",
    page_icon="📧",
    initial_sidebar_state="collapsed"
)

def set_custom_style():
    st.markdown("""
        <style>
        .caption {
            font-size: 1.1rem;
        }
        .opac {
            opacity: 0.7;
        }
        .caption a {
            text-decoration: none;
            opacity: 1 !important;
        }
        .caption a:hover {
            text-decoration: underline;
            opacity: 1;
        }
        .info {
            font-size: 0.85rem;
            padding: 1rem 2rem;
            border-radius: 0.5rem;
            background: rgba(255, 222, 33, 0.07);
            color: #ffda03;
            border: 1px solid rgba(255, 218, 3, 0.75);
            margin: 2rem 0;
        }
        .result-container {
            border-radius: 8px;
            padding: 0 1.5rem 1.5rem;
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

theme_color = "#1c1c1c"

st.markdown(
    f"""
    <script>
    const meta = document.createElement('meta');
    meta.name = "theme-color";
    meta.content = "{theme_color}";
    document.getElementsByTagName('head')[0].appendChild(meta);
    </script>
    """,
    unsafe_allow_html=True,
)

def create_streamlit_app(llm, clean_text):
    set_custom_style()

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    st.title("MailBot")

    st.markdown("""
        <div class="caption">
            <span class="opac">Cold Email Generator by</span> <a href="https://danish.bio" target="_blank">Danish</a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class="info">
            Generate personalized cold emails for job applications by providing a job posting URL and your resume. The AI will analyze both and create a tailored email.
        </div>
    """, unsafe_allow_html=True)

    url_input = st.text_input(
        "Job Posting URL",
        value="https://www.google.com/about/careers/",
        help="Enter the job posting URL"
    )

    resume_file = st.file_uploader(
        'Upload Your Resume (PDF)',
        type="pdf",
        help="Upload your resume in PDF"
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

if __name__ == "__main__":
    chain = Chain()
    create_streamlit_app(chain, clean_text)
