import os
import re
import chromadb
from datetime import datetime


storage_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma_storage"))
client = chromadb.PersistentClient(path=storage_path)
collection = client.get_or_create_collection("book_chapters")


def split_into_sentences(text):
    sentence_endings = r'(?<=[.!?])\s+'
    return [s.strip() for s in re.split(sentence_endings, text) if s.strip()]

def save_to_chromadb(text, chapter_title="Unknown Chapter"):
    sentences = split_into_sentences(text)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    ids = [f"{chapter_title}_s{i}_{timestamp}" for i in range(len(sentences))]
    metadatas = [{"chapter": chapter_title, "sentence_num": i} for i in range(len(sentences))]

    collection.add(documents=sentences, ids=ids, metadatas=metadatas)
    print(f"Saved {len(sentences)} sentences to ChromaDB.")

def search_chromadb(query, n_results=3):
    results = collection.query(query_texts=[query], n_results=20)  
    documents = results.get("documents", [[]])[0]

    
    filtered = [doc for doc in documents if query.lower() in doc.lower()]

    if not filtered:
        print(f"No sentence contains the word: '{query}'")
    else:
        print(f" Search Results for '{query}':")
        for i, doc in enumerate(filtered[:n_results]):
            print(f"\n Result {i+1}: {doc}\n")

    return filtered[:n_results]  
