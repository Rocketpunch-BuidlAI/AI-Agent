import os

import dotenv

dotenv.load_dotenv(dotenv_path=".env.local")


class ApiKeys:
    openai: str
    pinecone: str


configs = ApiKeys()
configs.openai = os.getenv("OPENAI_API_KEY", "")
configs.pinecone = os.getenv("PINECONE_API_KEY", "")
