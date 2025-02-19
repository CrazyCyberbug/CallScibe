import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from dotenv import load_dotenv



# setting the environment variables
load_dotenv("../.env")

# getting the secret API key
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')



# embedding model

model_name = "BAAI/bge-small-en"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embedding_model  = HuggingFaceBgeEmbeddings(
                        model_name=model_name,
                        model_kwargs=model_kwargs,
                        encode_kwargs=encode_kwargs
                    )

GOOGLE_API_KEY  = "AIzaSyDudMaPYy1qlnwLLfYtt5ydRtRPGrb3oHo"

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

if __name__ == "__main__":
    
    print("Invoking the model")
    print("Generataing a test response:\n:")
    print("Q: What is AI?\n\n Model Response:\n`", (llm.invoke("What is AI?")))
    