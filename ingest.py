import os
import time
import pandas as pd
from Bio import Entrez
from dotenv import load_dotenv

load_dotenv()
Entrez.api_key = os.getenv('NCBI_API_KEY')
Entrez.email = os.getenv('EMAIL')

def search_pubmed(query, max_results=1600):
    print('search term: {query}')
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results, usehistory="y")
    record = Entrez.read(handle)
    handle.close()
    return record

def fetch_details(id_list):
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
    results = Entrez.read(handle)
    handle.close()
    return results

def run_pipeline():
    query = '("cell-free DNA"[MeSH Terms]) AND ("circulating-tumor DNA"[MeSH Terms]) AND ("neoplasms"[MeSH Terms]) AND ("2015"[Date - Publication] : "2026"[Date - Publication])'
    search_results = search_pubmed(query)
    id_list = search_results["IdList"]
    print(f'Downloading a total of {len(id_list)} results')

    all_papers = []
    chunk_size = 100

    for i in range(0, len(id_list), chunk_size):
        chunk = id_list[i:i+chunk_size]
        print(f"Fetching chunk {i} to {i+chunk_size}...")
        
        try:
            details = fetch_details(chunk)
            for article in details['PubmedArticle']:
                # Extracting specific metadata for our RAG
                title = article['MedlineCitation']['Article']['ArticleTitle']
                try:
                    abstract = article['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
                except (KeyError, IndexError):
                    abstract = "No abstract available"
                
                pmid = article['MedlineCitation']['PMID']
                year = article['MedlineCitation']['Article']['Journal']['JournalIssue']['PubDate'].get('Year', 'N/A')
                
                all_papers.append({
                    "pmid": pmid,
                    "title": title,
                    "abstract": abstract,
                    "year": year,
                    "source": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
                })
        except Exception as e:
            print(f"Error fetching chunk: {e}")

        time.sleep(1)

    df = pd.Dataframe(all_papers)
    df.to_csv("data/cfdna_abstracts.csv", index=False)

if __name__ == "__main__":
    run_pipeline()