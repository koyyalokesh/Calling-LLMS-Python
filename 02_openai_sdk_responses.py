from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()

client = OpenAI() 

response = client.responses.create(    
    model="gpt-4o-mini",
    input="2021 ipl champions tropy won by which team"
)

print(response.output_text)