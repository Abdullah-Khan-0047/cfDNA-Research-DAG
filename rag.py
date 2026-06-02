import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory="./db_cfdna", embedding_function=embeddings)
retriever = vector_db.as_retriever(search_kwargs={"k": 5})

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

template = """
You are a bioinformatics scientist focused on oncology research.
Use these PubMed snippets to answer the question. 
Since this field changes constantly, prioritize the info provided over your general training.

Rules:
- Cite the Title or PMID for every claim.
- If the context doesn't have the answer, just say you don't know based on these papers.

Context:
{context}

Question: {question}

Answer:

"""

prompt = ChatPromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(f"Source: {d.metadata['title']}\nContent: {d.page_content}" for d in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)


if __name__ == "__main__":
    print("cfDNA Research Assistant is Active. (Type 'exit' to quit)\n")
    while True:
        user_query = input("Research Question: ")
        if user_query.lower() == 'exit':
            break
            
        print("\nWorking of answer\n")
        response = rag_chain.invoke(user_query)
        print(f"{response}\n")
        print("-" * 50)
        