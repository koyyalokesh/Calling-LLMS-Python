from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


load_dotenv()

image_url = 'https://images.unsplash.com/photo-1592194996308-7b43878e84a6?ixid=M3w4MjcwNjd8MHwxfHNlYXJjaHwxfHxjYXRzfGVufDB8fHx8MTc4ODIyNTU4Nnww&ixlib=rb-4.1.0&fit=max&q=80'

llm = ChatOpenAI(model="gpt-4o-mini")

url_message = HumanMessage(content=[
    {
        "type":"text",
        "text":"Describe this picture in two sentences"
        
    },
    {
        "type":"image",
        "url":image_url
        
    }
])

response = llm.invoke([url_message])
print(response.content)