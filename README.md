# Cell-Free DNA Research Assistant (RAG)

As someone who has worked as an Academic Research Assistant, I understand the need to stay up to date on literature, especially on topics that have updated research being published every month. I recently interviewed for a Bioinformatics related position and one thing I gathered form talking to the interviewers was the need to stay up to date on literature in the ever evolving field of cfDNA within oncology. There are hundreds of papers being published every month and by the time a standard LLM is trained, its knowledge on specific subtopics is already outdated.

Recognizing this need, I built this RAG (Retrieval Augmented Generation) pipeline. Its main purpose to act an LLM research assistant that can be updated and isnt affected by a knowledge date cutoff. It pulls the most recent data directly form PubMed and give up to date and thorough answers based on current available evidence.

## Why this application is ideal for Research

The oncology landscape changes way too fast for regular models like Gemini, ChatGPT, and others to keep track of. This pipeline assists with:

### 2. Staying Current
Index the latest published papers, from the past few years up to the current time (The time range can be edited).
### 3. Avoid Hallucinations
In critical research topics, a guess could be much more damaging that no answer. I implemented a strict grounding prompt which makes sure that if the answer is not in the indexed papers, the model admits that it does not know. 
### 4. References and Traceability
Every response is tied to a PMID (PubMed ID) or Title, so you can jump straight to the source to verify the data.

## Tech Breakdown
### Data Source
Scraped PubMed via the Entrez API. I used MeSH (Medical Subject Headings) terms like "cell-free DNA"[MeSH] to make sure I wasn't getting junk data or unrelated "CF" (Cystic Fibrosis) results.
### Vector Store
ChromaDB. I used a local HNSW index because it's fast and handles a few thousand chunks without breaking a sweat.
### Embeddings
all-MiniLM-L6-v2 from HuggingFace. It’s lightweight but surprisingly good at picking up medical semantics.
### LLM Brain
Gemini 1.5 Flash. I chose this for the reasoning speed and the fact that it's great at following the "don't make things up" instructions in the prompt.

## Pipeline Details
### Ingest.py
Hits the PubMed API, filters for cancer-related cfDNA research from the past few years up to the current date.
### Vectorize.py
Chunks the abstracts (using a 700-char window with 100-char overlap) and stores the vectors in a local database.
### Rag.py
It takes a question, finds the top 5 most relevant snippets, and forces Gemini to answer based only on that context.
