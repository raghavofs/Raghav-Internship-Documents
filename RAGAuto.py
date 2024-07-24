import requests
from bs4 import BeautifulSoup
import faiss
import numpy as np
from openai import OpenAI

# Initialize OpenAI client
api_key = "500293d613d84863bfcff567380fe4d1"
base_url = "https://api.aimlapi.com"
client = OpenAI(api_key=api_key, base_url=base_url)

# Function to scrape documents from Hacker News
def scrape_documents():
    url = "https://news.ycombinator.com/"  # Hacker News
    response = requests.get(url)
    if response.status_code!= 200:
        print(f"Failed to retrieve webpage, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("tr", class_="athing")
    if not articles:
        print("No articles found on the webpage.")
        return []

    documents = []
    for article in articles[:10]:  # Limit to the first 10 articles for simplicity
        title_element = article.find("a", class_="storylink")
        content_element = article.find("span", class_="commtext c00")
        
        if title_element and content_element:
            title = title_element.text.strip()
            content = content_element.text.strip()
            documents.append(f"{title}: {content}")
        else:
            print(f"Skipping an article due to missing title or content: {article}")

    if not documents:
        print("No valid documents were scraped from the webpage.")
    return documents

# Function to create or update the index using FAISS
def create_faiss_index(documents):
    index = faiss.IndexFlatL2(768)  # Using a 768-dimensional space for embeddings
    # You need to generate embeddings for your documents using a model like BERT
    # For simplicity, we'll use random vectors as placeholders
    embeddings = np.random.rand(len(documents), 768).astype('float32')
    index.add(embeddings)
    return index, embeddings

# Function to retrieve top k documents based on query
def retrieve_documents(query, index, embeddings, documents, top_k=2):
    # Generate an embedding for the query using the same method as for documents
    # For simplicity, we'll use a random vector as a placeholder
    query_embedding = np.random.rand(1, 768).astype('float32')
    D, I = index.search(query_embedding, top_k)
    return [documents[i] for i in I[0]]

def ask_question():
    print("Welcome to the AI Assistant!")
    print("Ask me anything, and I'll do my best to answer.")
    conversation_history = []

    # Initial document retrieval and indexing
    documents = scrape_documents()
    if not documents:
        print("Failed to retrieve documents. Please check the URL or your internet connection.")
        return
    faiss_index, embeddings = create_faiss_index(documents)

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        conversation_history.append({"role": "user", "content": user_input})

        # Retrieve relevant documents based on user query
        retrieved_docs = retrieve_documents(user_input, faiss_index, embeddings, documents, top_k=2)
        context = " ".join(retrieved_docs)

        # Generate response using OpenAI API with retrieved context
        response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.2",
            messages=[
                {"role": "system", "content": "You are an AI assistant who knows everything."},
                {"role": "system", "content": f"Context: {context}"}
            ] + conversation_history,
        )
        message = response.choices[0].message.content
        print(f"Assistant: {message}")
        conversation_history.append({"role": "assistant", "content": message})

if __name__ == "__main__":
    ask_question()