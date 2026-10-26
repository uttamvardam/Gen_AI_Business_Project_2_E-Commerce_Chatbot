import os

import chromadb
from chromadb.utils import embedding_functions
from groq import Groq
import pandas
from dotenv import load_dotenv

load_dotenv()


ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='sentence-transformers/all-MiniLM-L6-v2'
        )

def get_groq_api_key():
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("GROQ_API_KEY")
        except Exception:
            pass
    return key

def get_groq_model():
    model = os.environ.get("GROQ_MODEL")
    if not model:
        try:
            import streamlit as st
            model = st.secrets.get("GROQ_MODEL")
        except Exception:
            pass
    return model or "openai/gpt-oss-20b"

def get_groq_client():
    api_key = get_groq_api_key()
    return Groq(api_key=api_key) if api_key else None

chroma_client = chromadb.Client()
collection_name_faq = 'faqs'


def ingest_faq_data(path):
    if collection_name_faq not in [c.name for c in chroma_client.list_collections()]:
        print("Ingesting FAQ data into Chromadb...")
        collection = chroma_client.create_collection(
            name=collection_name_faq,
            embedding_function=ef
        )
        df = pandas.read_csv(path)
        docs = df['question'].to_list()
        metadata = [{'answer': ans} for ans in df['answer'].to_list()]
        ids = [f"id_{i}" for i in range(len(docs))]
        collection.add(
            documents=docs,
            metadatas=metadata,
            ids=ids
        )
        print(f"FAQ Data successfully ingested into Chroma collection: {collection_name_faq}")
    else:
        print(f"Collection: {collection_name_faq} already exist")


def get_relevant_qa(query):
    collection = chroma_client.get_collection(
        name=collection_name_faq,
        embedding_function=ef
    )
    result = collection.query(
        query_texts=[query],
        n_results=2
    )
    return result


def generate_answer(query, context):
    prompt = f'''Given the following context and question, generate answer based on this context only.
    If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.
    
    CONTEXT: {context}
    
    QUESTION: {query}
    '''
    client = get_groq_client()
    if not client:
        return "⚠️ GROQ_API_KEY is not configured. Please add your GROQ_API_KEY to your Streamlit Cloud Secrets or .env file."
    
    completion = client.chat.completions.create(
        model=get_groq_model(),
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return completion.choices[0].message.content


def faq_chain(query):
    result = get_relevant_qa(query)
    context = "".join([r.get('answer') for r in result['metadatas'][0]])
    print("Context:", context)
    answer = generate_answer(query, context)
    return answer


if __name__ == '__main__':
    ingest_faq_data(faqs_path)
    query = "what's your policy on defective products?"
    query = "Do you take cash as a payment option?"
    # result = get_relevant_qa(query)
    answer = faq_chain(query)
    print("Answer:",answer)