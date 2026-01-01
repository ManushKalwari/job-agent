# rank/lexical.py

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class LexicalScorer:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            analyzer="char_wb",
            ngram_range=(3, 5),
            min_df=1
        )
        self.job_matrix = None
        self.job_ids = None

    def fit(self, job_texts: list[str], job_ids: list[str]):
        self.job_matrix = self.vectorizer.fit_transform(job_texts)
        self.job_ids = job_ids

    def score_query(self, query: str) -> dict[str, float]:
        q = self.vectorizer.transform([query])
        scores = (self.job_matrix @ q.T).toarray().ravel()
        return {jid: float(s) for jid, s in zip(self.job_ids, scores)}
