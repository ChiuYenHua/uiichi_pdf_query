from pinecone import Pinecone
from openai import OpenAI
import streamlit as st

# Openai setup
client = OpenAI(api_key=st.secrets.OpenAI.api_key)

# Pincone setup
pc = Pinecone(api_key=st.secrets.pinecone.api_key)
index = pc.Index("experiment")

# Get embedding
def get_embedding(sentence):
    response = client.embeddings.create(
    model="text-embedding-3-small",
    input = sentence
    )
    embedding = response.data[0].embedding
    
    return embedding

# Extract data (preprocessing)
def extract_data(list_of_dict):
    temp_list = []
    for match in list_of_dict:
        temp_dict = {}
        temp_dict['score'] = match['score']
        temp_dict['content'] = match['metadata']['content']
        temp_dict['page'] = match['metadata']['page']
        temp_list.append(temp_dict)
    return temp_list

# Get similarity from pinecone
def get_similarity_from_pinecone(query_sentence):
    embedded_query = get_embedding(query_sentence)

    # Pinecone query (ncku)
    ncku = index.query(
        namespace="ncku_design_for_elders",
        vector=embedded_query,
        top_k=10,
        include_metadata=True
    )['matches']

    # Pinecone query (japan)
    japan = index.query(
        namespace="japan_design_for_elders",
        vector=embedded_query,
        top_k=10,
        include_metadata=True
    )['matches']

    # Pinecone query (china)
    china = index.query(
        namespace="china_design_for_elders",
        vector=embedded_query,
        top_k=10,
        include_metadata=True
    )['matches']

    # Pinecone query (tapei)
    taipei = index.query(
        namespace="taipei_design_for_elders",
        vector=embedded_query,
        top_k=10,
        include_metadata=True
    )['matches']

    return {
        'ncku':extract_data(ncku),
        'japan':extract_data(japan),
        'china':extract_data(china),
        'taipei':extract_data(taipei),
    }


