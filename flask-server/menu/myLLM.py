import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables from .env file
load_dotenv(r"D:\python_mini_projects\TASKS\menubased\Cloud-menu-project\flask-server\menu\Secret.env")


if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = os.getenv("LLM_KEY")

# Initialize your ChatGoogleGenerativeAI instance with the API key
llm = ChatGoogleGenerativeAI(model="gemini-pro")

# Example usage
result = llm.invoke("Write a ballad about LangChain")
print(result.content)