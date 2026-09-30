from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)
from scraper.training.model_registry import ModelRegistry


class KBLIService:

    def __init__(self, model_path=None):
        self.registry = ModelRegistry()

        if model_path is None:
            active_model = self.registry.get_active_model(
                "kbli"
            )

            self.model_path = self.registry.resolve_model_path(
                active_model
            )
        else:
            self.model_path = Path(model_path)

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print("Loading KBLI tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        print("Loading KBLI model...")

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        self.model.to(self.device)
        self.model.eval()

        print("KBLI model loaded.")
        print(f"Device: {self.device}")
        print(f"Number of classes: {self.model.config.num_labels}")

    def predict(self, text: str):

        if not text:
            return None

        text = text.strip()

        if not text:
            return None

        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512
        )

        inputs = {
            key: value.to(self.device)
            for key, value in inputs.items()
        }

        with torch.no_grad():
            outputs = self.model(**inputs)

        logits = outputs.logits

        predicted_id = torch.argmax(
            logits,
            dim=-1
        ).item()

        predicted_label = self.model.config.id2label[
            predicted_id
        ]

        probabilities = torch.softmax(
            logits,
            dim=-1
        )

        confidence = probabilities[
            0,
            predicted_id
        ].item()

        return {
            "label": predicted_label,
            "confidence": confidence,
            "class_id": predicted_id,
        }