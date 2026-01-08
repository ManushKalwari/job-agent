# Autonomous Job Agent

An end-to-end system that automates job discovery, ranking, and cover letter generation using real job boards, machine learning–based relevance scoring, and large language models.

---

## Overview

The Autonomous Job Agent streamlines the job application workflow by sourcing open roles, ranking them based on user-defined preferences, and generating tailored company-specific cover letters from an uploaded resume.

The system is designed as a modular, production-style application with a clear separation between frontend, backend services, ranking logic, and generation pipelines.

---

## System Architecture

The system is split into a frontend client and a backend service.

- **Frontend**: Interactive web UI for job discovery and selection  
- **Backend**: API layer, ranking pipeline, resume parsing, and document generation  

Communication between the frontend and backend occurs over HTTP using JSON and multipart form data.

---

## Ranking Methodology

Jobs are ranked using a **Product of Experts (PoE)** formulation that combines two independent relevance signals:

1. **Semantic relevance**  
   - Sentence-level embeddings of job descriptions and user queries  
   - Cosine similarity for meaning-based matching  

2. **Lexical relevance**  
   - Character n-gram TF-IDF scoring  
   - Captures exact and near-exact term overlap  

The final ranking score is computed as Product of Experts (PoE) score.

## Cover Letter Generation

- Users upload a resume as a PDF
- Resume text is extracted once per request
- For each selected job:
  - The enriched job description and resume text are passed to an LLM
  - The model is constrained to use only resume-provided experience
  - A concise, role-aligned cover letter is generated
- Output is rendered as a formatted PDF using ReportLab

---

## Technology Stack

### Frontend
- React
- TypeScript
- Vite

### Backend
- FastAPI
- Pydantic
- Uvicorn

### Machine Learning / NLP
- Sentence Transformers (semantic similarity)
- TF-IDF (lexical scoring)
- Product-of-Experts ranking
- OpenAI API (text generation)

### Data & Utilities
- SQLite
- BeautifulSoup
- PyPDF
- ReportLab

### Deployment
- Docker
- AWS EC2

---

## Design Goals

- Minimize manual effort in repetitive job applications and writing custom cover letters  
- Improve relevance between candidate experience and job requirements  

---

## Future Improvements

- Company list configuration via UI (currently uses Greenhouse API)
- Job tracking and application history  
