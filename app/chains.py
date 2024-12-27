import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GROQ_API_KEY")

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-specdec",
                            )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### Scrape
            {page_data}
            ### Instruction:
           The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse!")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, resume):
        prompt_email = PromptTemplate.from_template(
            """
            ### Job Description
            {job_description}
            ### Resume:
            {resume_data}

            ### Instruction:
              Imagine that the above resume is yours with your name.
              Your job is to write a cold email to the hiring manager tailoring to the job description mentioned above describing your capability and how they should hire you according to the resume. Dont make it sound like AI, dont make it too long, keep it relevant, impressive and simple. Get the subject right according to the job title. Add relevant stuff relating your resume to the job description and skills.
              Do not provide a preamble.
            
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "resume_data" : str(resume)})
        return res.content
