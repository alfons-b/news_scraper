from pathlib import Path

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification
)
from scraper.training.model_registry import ModelRegistry



class DirectionService:

    def __init__(self, model_path=None):
        self.registry = ModelRegistry()

        if model_path is None:
            active_model = self.registry.get_active_model(
                "direction"
            )

            self.model_path = self.registry.resolve_model_path(
                active_model
            )
        else:
            self.model_path = Path(model_path)        
        
        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print("Loading direction tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        print("Loading direction model...")

        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        self.model.to(self.device)
        self.model.eval()

        print("Direction model loaded.")
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

        probabilities = torch.softmax(
            outputs.logits,
            dim=-1
        )

        predicted_id = torch.argmax(
            probabilities,
            dim=-1
        ).item()

        original_label = self.model.config.id2label[
            predicted_id
        ]

        confidence = probabilities[
            0,
            predicted_id
        ].item()

        label_mapping = {
            "positive": "meningkat",
            "negative": "menurun",
            "neutral": "netral",
        }

        direction_label = label_mapping.get(
            original_label
        )

        return {
            "label": direction_label,
            "original_label": original_label,
            "confidence": confidence,
            "class_id": predicted_id,
        }