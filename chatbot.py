"""FAQ retrieval using TF-IDF and cosine similarity."""
import json
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from preprocessing import preprocess_text


GREETINGS = {
    "hi", "hello", "hey", "good morning", "good afternoon",
    "good evening", "howdy"
}


def load_faqs(path):
    """Load and validate FAQ records from a JSON file."""
    faq_path = Path(path)
    if not faq_path.exists():
        raise FileNotFoundError(
            f"FAQ file not found: {faq_path}. Run the app from the project folder."
        )

    with faq_path.open("r", encoding="utf-8") as file:
        faqs = json.load(file)

    if not isinstance(faqs, list) or not faqs:
        raise ValueError("The FAQ dataset must be a non-empty JSON list.")

    for index, faq in enumerate(faqs):
        if not all(key in faq for key in ("question", "answer")):
            raise ValueError(f"FAQ item {index + 1} needs question and answer fields.")
        if not faq["question"].strip() or not faq["answer"].strip():
            raise ValueError(f"FAQ item {index + 1} has an empty question or answer.")

    return faqs


class FAQChatbot:
    """Find the most similar stored FAQ question and return its answer."""

    def __init__(self, faqs, threshold=0.22):
        if not faqs:
            raise ValueError("At least one FAQ is required.")

        self.faqs = faqs
        self.threshold = threshold
        self.questions = [faq["question"] for faq in faqs]
        self.processed_questions = [
    " ".join(preprocess_text(question)) or question.lower()
    for question in self.questions
]

        # TF-IDF converts text into weighted numerical vectors.
        self.vectorizer = TfidfVectorizer(
            tokenizer=str.split,
            preprocessor=None,
            token_pattern=None,
            lowercase=False,
        )
        self.faq_vectors = self.vectorizer.fit_transform(self.processed_questions)

    def get_answer(self, user_question):
        """Return a greeting, a matched FAQ answer, or a safe fallback."""
        question = (user_question or "").strip()

        if not question:
            return {
                "answer": "Please type a question so I can try to help.",
                "matched_question": None,
                "score": 0.0,
            }

        normalized = " ".join(preprocess_text(question))
        if normalized in GREETINGS:
            return {
                "answer": "Hello! 👋 Ask me a question about college admissions or student services.",
                "matched_question": None,
                "score": 0.0,
            }

        processed = preprocess_text(question)
        if not processed:
            return {
                "answer": "I couldn't identify useful words in that message. Please rephrase your question.",
                "matched_question": None,
                "score": 0.0,
            }

        query_vector = self.vectorizer.transform([" ".join(processed)])
        scores = cosine_similarity(query_vector, self.faq_vectors).flatten()
        best_index = int(scores.argmax())
        best_score = float(scores[best_index])

        if best_score < self.threshold:
            return {
                "answer": (
                    "Sorry, I couldn't find a reliable match in my FAQ dataset. "
                    "Try asking about admissions, eligibility, documents, fees, exams, "
                    "scholarships, or student services."
                ),
                "matched_question": None,
                "score": best_score,
            }

        return {
            "answer": self.faqs[best_index]["answer"],
            "matched_question": self.questions[best_index],
            "score": best_score,
        }
