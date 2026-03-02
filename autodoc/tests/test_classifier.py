from autodoc.core.classifier import SklearnDocumentClassifier


def test_classifier_predicts_invoice() -> None:
    classifier = SklearnDocumentClassifier()
    text = "Invoice number INV-999 total amount 1200 vendor ACME"
    assert classifier.predict(text) == "invoice"
