from langchain_groq import ChatGroq

llm = ChatGroq(
    temperature=0,
    groq_api_key='',
    model_name="llama-3.3-70b-specdec",
)

response = llm.invoke("Hi, what model are you?")
print(response.content)

