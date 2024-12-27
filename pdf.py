import asyncio
from langchain_community.document_loaders import PyPDFLoader

async def load_pdf():
    file_path = "./resume.pdf"
    loader = PyPDFLoader(file_path)
    pages = []
    async for page in loader.alazy_load():
        pages.append(page)
    if pages:
        print(f"{pages[0].metadata}\n")
        print(pages[0].page_content)

asyncio.run(load_pdf())
