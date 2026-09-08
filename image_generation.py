from pathlib import Path
import base64
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser

load_dotenv()

client = OpenAI()

Here = Path(__file__).parent


def save(result, filename):
    print("IMAGE RESPONSE :", result)
    """The image comes back as base64 text, so decode it and write the file."""
    PATH = Here/filename
    PATH.write_bytes(base64.b64decode(result.data[0].b64_json))
    print("Saved:", PATH.name)
# 1. a LangChain chain writes the image prompt

writer = (
    ChatPromptTemplate.from_messages([
    ("system", "You write short, visual image prompts. One sentence, no preamble."),
    ("human", "An illustration for a blog post about {topic}"),
    ]) | ChatOpenAI(model="gpt-4o-mini") | StrOutputParser()
   )

image_prompt = writer.invoke({"topic":"learning langchain"})
print("Our chain wrote:", image_prompt)

# 2. the OpenAI SDK turns that prompt into a picture

result = client.images.generate(
      model="gpt-image-1-mini",
      prompt=image_prompt,
      size="1024x1024",
      quality="low",
)

save(result, "Demo.png")



