from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from scraper.training.model_registry import ModelRegistry


class SummarizationService:

    def __init__(self, model_path=None):
        # ====================================================
        # PATH PROJECT
        # ====================================================

        self.registry = ModelRegistry()

        if model_path is None:

            active_model = self.registry.get_active_model(
                "summarization"
            )

            self.model_path = self.registry.resolve_model_path(
                active_model

            )

        else:

            self.model_path = Path(model_path)
        # ====================================================
        # DEVICE
        # ====================================================

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # ====================================================
        # LOAD TOKENIZER
        # ====================================================

        print("Loading summarization tokenizer...")

        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        # ====================================================
        # LOAD MODEL
        # ====================================================

        print("Loading summarization model...")

        self.model = AutoModelForSeq2SeqLM.from_pretrained(
            self.model_path,
            local_files_only=True
        )

        self.model.to(self.device)
        self.model.eval()

        print("Summarization model loaded.")
        print(f"Device: {self.device}")

    # ========================================================
    # SUMMARIZE
    # ========================================================

    def summarize(self, text: str) -> str:

        if not text:
            return ""

        text = text.strip()

        if not text:
            return ""

        # ----------------------------------------------------
        # TOKENIZATION
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # GENERATE
        # ----------------------------------------------------

        with torch.no_grad():

            outputs = self.model.generate(
                **inputs,

                min_length=30,
                max_length=120,

                num_beams=5,
                do_sample=False,

                no_repeat_ngram_size=2,

                repetition_penalty=1.0
            )

        # ----------------------------------------------------
        # DECODE
        # ----------------------------------------------------

        summary = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        return summary.strip()