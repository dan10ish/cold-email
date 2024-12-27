from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PrompTemplate

loader = WebBaseLoader("https://www.google.com/about/careers/applications/jobs/results/89754459076207302-software-engineer-corp-eng")

page_data = loader.load().pop().page_content
print(page_data)

prompt_extract = PrompTemplate.from_template(
    """
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}
        ### INSTRUCTION:
        The scraped text is from the career's page of a website.
        Your job is to extract the job postings and return them in JSON format containing the 
        following keys: `role`, `experience`, `skills` and `description`.
        Only return the valid JSON.
        ### VALID JSON (NO PREAMBLE):    
        """
)

