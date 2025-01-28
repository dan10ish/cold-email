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
              Using the above resume and job description, write a compelling cold email to the hiring manager. Follow these specific guidelines:

1. Use the name and experience exactly as shown in the resume - do not fabricate or add details
2. Structure:
   - Subject line: Application for [Job Title]
   - Opening: Concise introduction referencing the specific role
   - Core paragraphs: Match 2-3 strongest achievements from the resume to the job requirements
   - Closing: Brief call to action
   - Salutations and contact details (taken from resume data)

3. Writing style:
   - Natural and conversational tone
   - No AI-like language or generic phrases
   - Active voice with specific examples
   - Maximum 250 words

4. Content requirements:
   - Only reference skills and experiences explicitly stated in the resume
   - Draw clear connections between past achievements and job requirements
   - Include measurable impacts where available (%, numbers, scale)
   - Focus on most relevant experience for this role

5. Formatting:
   - Professional email format
   - Short, focused paragraphs
   - No bullet points
   - Clear spacing

Do not add any explanatory text before or after the email. Do not provide a preamble.
            
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "resume_data" : str(resume)})
        return res.content
