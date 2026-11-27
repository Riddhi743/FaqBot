\# Smart FAQ Bot for Product Manuals



\*\*Team TechBusters\*\* | Bennett University | Prompt Engineering (SCSE4041) | Mini-Project, Problem C17 (FAQ bot from a product manual)



A chatbot that answers product questions \*\*only from a product manual\*\*, in simple language, with the \*\*page number\*\* of the source. If the manual does not contain the answer, it says so instead of guessing.



\*\*Live demo:\*\* \[Streamlit app URL]



\## The problem

Product manuals are long and hard to search. Users who are setting up or troubleshooting a device need a quick, clear answer they can trust. A general chatbot may invent steps that are not in the manual, so this project grounds every answer in the manual text and cites the page.



\## How it works



```

Manual PDF -> extract text per page -> chunk (800 chars, 150 overlap) -> ChromaDB

User question -> \[Prompt 1] rewrite into manual-style search query

&#x20;             -> retrieve top chunks (original + rewritten query)

&#x20;             -> refusal gate (if best match is too far -> "I could not find this in the provided manual.")

&#x20;             -> \[Prompt 2] answer ONLY from the excerpts, cite pages

&#x20;             -> answer + "Sources used" panel

```



\*\*Prompts in the final solution: 2\*\*

1\. \*\*Query-rewrite prompt:\*\* turns the user's question into a short search query with alternative manual wording.

2\. \*\*Grounded-answer prompt:\*\* answers only from retrieved excerpts, cites pages, asks one clarifying question for vague inputs, refuses when the answer is missing, ignores instructions in the user message that try to change the rules.



\## Tech stack

\- \*\*UI:\*\* Streamlit

\- \*\*Vector store / retrieval:\*\* ChromaDB (default embeddings)

\- \*\*LLM:\*\* Groq API, `openai/gpt-oss-120b` (temperature 0)

\- \*\*PDF parsing:\*\* pypdf



\## Project files

| File | Purpose |

|---|---|

| `faq\_app.py` | Streamlit chat UI with a "Sources used" panel |

| `rag\_core.py` | Prompts, retrieval, query rewrite, refusal gate, answer generation |

| `ingest\_manual.py` | Reads the PDF, chunks it with page numbers, indexes it in ChromaDB |

| `debug\_query.py` | Prints retrieved chunks, distances and pages for a question (used for error analysis) |

| `check\_db.py` | Prints how many chunks are in the database |

| `data/manual/manual.pdf` | Test manual |



\## Run it locally

```

pip install -r requirements.txt

```

Create a `.env` file in the project root:

```

GROQ\_API\_KEY=your\_key\_here

```

Then:

```

python ingest\_manual.py

streamlit run faq\_app.py

```



\## Test manual

Cosori Premium 5.8-Quart Air Fryer, model CP358-AF, public user manual (13 pages), used for testing only. No personal or sensitive data is used.



\*\*Page numbers:\*\* the bot cites the \*\*PDF page index\*\* (1-13). The manual is printed in two-page spreads, so these differ from the printed page numbers.



\## Prompt iteration summary

| Version | Change | Why |

|---|---|---|

| v1 | Baseline prompt, top 4 chunks, distance threshold 0.6 | Milestone 1 baseline |

| v2 | Top 6 chunks, threshold 0.8 | Fix wrongly refused questions (e.g. commercial use) |

| v3 | New system prompt: clarifying question for vague inputs, injection guard | "It's not working" got a flat refusal |

| v4 | `max\_tokens` 500 to 1000 | Long answers (safety list) were cut off |

| v5 | Added query-rewrite step (2-step chain) | Attempt to fix the false refusal on "reset" |



Full log, test table and results are in the Milestone 2 PDF.



\## Known limitations

\- \*\*"How do I reset my air fryer?" is wrongly refused.\*\* The manual's reset instructions are about presets (PDF page 8). Retrieval ranked generic "air fryer" chunks higher, so the relevant chunk never reached the model. The query-rewrite step (v5) did not fix this.

\- The model sometimes adds small details that are not in the manual (for example extra button names or closing sentences), so answers should be checked against the cited page.

\- Works only on text-based PDFs (not scanned images) and one manual at a time.

\- Answers are for guidance. For safety-critical issues, contact the

