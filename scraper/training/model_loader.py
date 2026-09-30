from pathlib import Path

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)


class KBLIModelLoader:

    def __init__(self):
        self.model_path = (
            Path(__file__).resolve()
            .parents[2]
            / "models"
            / "KBLI"
            / "model_kbli"
        )

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained(
            str(self.model_path),
            local_files_only=True,
        )

    def load_model(self):
        return AutoModelForSequenceClassification.from_pretrained(
            str(self.model_path),
            local_files_only=True,
        )

    def load(self):
        tokenizer = self.load_tokenizer()
        model = self.load_model()

        return {
            "tokenizer": tokenizer,
            "model": model,
            "model_path": str(self.model_path),
        }


class DirectionModelLoader:

    def __init__(self):
        self.model_path = (
            Path(__file__).resolve()
            .parents[2]
            / "models"
            / "direction"
            / "finbert-indonesia"
        )

    def load_tokenizer(self):
        return AutoTokenizer.from_pretrained(
            str(self.model_path),
            local_files_only=True,
        )

    def load_model(self):
        return AutoModelForSequenceClassification.from_pretrained(
            str(self.model_path),
            local_files_only=True,
        )

    def load(self):
        tokenizer = self.load_tokenizer()
        model = self.load_model()

        return {
            "tokenizer": tokenizer,
            "model": model,
            "model_path": str(self.model_path),
        }