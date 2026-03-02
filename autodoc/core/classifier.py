"""Document classifier abstraction and implementations."""
from abc import ABC, abstractmethod

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline


class BaseDocumentClassifier(ABC):
    """Classifier interface for dependency injection in processing pipeline."""

    @abstractmethod
    def predict(self, text: str) -> str:
        raise NotImplementedError


class SklearnDocumentClassifier(BaseDocumentClassifier):
    """Simple lightweight text classifier trained on synthetic examples."""

    def __init__(self) -> None:
        self.pipeline: Pipeline = self._build_and_train()

    def _build_and_train(self) -> Pipeline:
        samples = [
            "Invoice number INV-104 total amount due USD 2500 vendor ACME Corp",
            "Tax invoice issued on 2024-01-02 subtotal and total amount 189.20",
            "Receipt from Coffee House total paid 14.25 card payment",
            "Merchant receipt date 2023-11-11 amount 77.90",
            "This contract is entered between Alpha LLC and Beta Inc effective date",
            "Service agreement contract date 2024-03-10 parties agree to terms",
        ]
        labels = ["invoice", "invoice", "receipt", "receipt", "contract", "contract"]
        model = Pipeline(
            [
                ("vectorizer", TfidfVectorizer(ngram_range=(1, 2))),
                ("classifier", LogisticRegression(max_iter=500)),
            ]
        )
        model.fit(samples, labels)
        return model

    def predict(self, text: str) -> str:
        return str(self.pipeline.predict([text or ""])[0])
