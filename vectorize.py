import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Loading ingested data
df = pd.read_csv('data/cfdna_abstracts.csv')
df['full_text'] = "Title: " + df['title'] + " | Abstract: " + df['abstract'] #structuring

documents = []
for _, row in df.iterrows():
    doc = Document(
        page_content=row['full_text'],
        metadata={
            "pmid": str(row['pmid']),
            "title": row['title'],
            "year": row['year'],
            "source": row['source']
        }
    )
    documents.append(doc)

    # Chunking
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700, 
    chunk_overlap=100
)
chunks = text_splitter.split_documents(documents)
print(f"Total {len(chunks)} chunks from {len(documents)} papers.")

print('Embedding')
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

print('making the vector database')
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./db_cfdna")

print('Finished')


