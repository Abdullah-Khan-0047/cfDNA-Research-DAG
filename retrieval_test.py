from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# 1. Setup the same embedding model we used to create the DB
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Load the existing database from the folder
vector_db = Chroma(
    persist_directory="./db_cfdna", 
    embedding_function=embeddings
)

# 3. Define a specific medical query
query = "What is the accuracy of cfDNA in detecting early stage lung cancer?"

# 4. Perform a "Similarity Search"
# k=3 means "Give me the top 3 most relevant chunks"
print(f"\n--- Searching for: {query} ---\n")
results = vector_db.similarity_search(query, k=3)

# 5. Display the results and their metadata
for i, doc in enumerate(results):
    print(f"Result {i+1}:")
    print(f"Source: {doc.metadata['source']}")
    print(f"Title: {doc.metadata['title']}")
    print(f"Snippet: {doc.page_content[:200]}...") # Print first 200 chars
    print("-" * 30)