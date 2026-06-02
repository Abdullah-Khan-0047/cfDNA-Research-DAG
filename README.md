# Cell-Free DNA Research Assistant (RAG)

As someone who has worked as an Academic Research Assistant, I understand the need to stay up to date on literature, especially on topics that have updated research being published every month. I recently interviewed for a Bioinformatics related position and one thing I gathered form talking to the interviewers was the need to stay up to date on literature in the ever evolving field of cfDNA within oncology. There are hundreds of papers being published every month and by the time a standard LLM is trained, its knowledge on specific subtopics is already outdated.

Recognizing this need, I built this RAG (Retrieval Augmented Generation) pipeline. Its main purpose to act an LLM research assistant that can be updated and isnt affected by a knowledge date cutoff. It pulls the most recent data directly form PubMed and give up to date and thorough answers based on current available evidence.

## Why this application is ideal for Research

The oncology landscape changes way too fast for regular models like Gemini, ChatGPT, and others to keep track of. This pipeline assists with:

### Staying Current
Index the latest published papers, from the past few years up to the current time (The time range can be edited).
### Avoid Hallucinations
In critical research topics, a guess could be much more damaging that no answer. I implemented a strict grounding prompt which makes sure that if the answer is not in the indexed papers, the model admits that it does not know. 
### References and Traceability
Every response is tied to a PMID (PubMed ID) or Title, so you can jump straight to the source to verify the data.
