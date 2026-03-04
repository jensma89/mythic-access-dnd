"""
openai_service.py

Open AI entry and service logic.
"""
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

client = OpenAI()


response = client.responses.create(
    model="gpt-4.1-mini",
    input="Write a one-sentence bedtime story about a unicorn."
)
