from pathlib import Path
from sklearn.model_selection import train_test_split
from datetime import datetime

from transformers import (
    TrainingArguments,
    Trainer as HFTrainer,
)

from scraper.training.config import (
    KBLITrainingConfig,
    DirectionTrainingConfig,
    get_kbli_model_path,
    get_kbli_candidate_root,
    get_direction_model_path,
    get_direction_candidate_root,
)
from scraper.training.model_loader import KBLIModelLoader
from scraper.training.huggingface_dataset import KBLIDataset
from scraper.training.evaluator import Evaluator
from scraper.training.model_loader import DirectionModelLoader




class Trainer:

    def __init__(self):
        self.evaluator = Evaluator()

    VALID_MODEL_TYPES = {
        "summarization",
        "kbli",
        "direction",
    }

    KBLI_LABEL2ID = {
        "A": 0,
        "B": 1,
        "C": 2,
        "D": 3,
        "E": 4,
        "F": 5,
        "G": 6,
        "H": 7,
        "I": 8,
        "J": 9,
        "K": 10,
        "L": 11,
        "M": 12,
        "N": 13,
        "O": 14,
        "P": 15,
        "Q": 16,
        "R": 17,
        "S": 18,
        "T": 19,
        "U": 20,
    }
    DIRECTION_LABEL2ID = {
        "meningkat": 0,
        "menurun": 1,
        "netral": 2,
    }

    def prepare_kbli_dataset(self, dataset_result):
        if not dataset_result:
            raise ValueError(
                "Dataset result tidak boleh kosong."
            )

        dataset = dataset_result.get("data")

        if not dataset:
            raise ValueError(
                "Dataset KBLI kosong."
            )

        texts = []
        labels = []
        article_ids = []

        for item in dataset:

            text = item.get("text")
            label = item.get("label")
            article_id = item.get("article_id")

            if not text:
                continue

            if label not in self.KBLI_LABEL2ID:
                continue

            texts.append(text)
            labels.append(
                self.KBLI_LABEL2ID[label]
            )
            article_ids.append(article_id)

        if not texts:
            raise ValueError(
                "Tidak ada data KBLI yang valid."
            )

        if len(texts) < 2:
            raise ValueError(
                "Minimal diperlukan 2 data untuk train/validation split."
            )

        train_texts, val_texts, train_labels, val_labels, train_ids, val_ids = (
            train_test_split(
                texts,
                labels,
                article_ids,
                test_size=0.2,
                random_state=42,
                stratify=labels if len(set(labels)) > 1 else None,
            )
        )

        return {
            "train": {
                "texts": train_texts,
                "labels": train_labels,
                "article_ids": train_ids,
            },
            "validation": {
                "texts": val_texts,
                "labels": val_labels,
                "article_ids": val_ids,
            },
            "stats": {
                "total": len(texts),
                "train": len(train_texts),
                "validation": len(val_texts),
            },
        }

    def prepare_direction_dataset(self, dataset_result):

        readiness = self.check_direction_training_readiness(
            dataset_result
        )

        if not readiness["ready"]:
            raise ValueError(
                f"Training Direction belum siap: "
                f"{readiness['reason']}"
            )

        dataset = dataset_result["data"]

        texts = [
            item["text"]
            for item in dataset
        ]

        labels = [
            item["label"]
            for item in dataset
        ]

        train_texts, validation_texts, train_labels, validation_labels = (
            train_test_split(
                texts,
                labels,
                test_size=0.2,
                random_state=42,
                stratify=labels,
            )
        )

        train_data = [
            {
                "text": text,
                "label": label,
            }
            for text, label in zip(
                train_texts,
                train_labels,
            )
        ]

        validation_data = [
            {
                "text": text,
                "label": label,
            }
            for text, label in zip(
                validation_texts,
                validation_labels,
            )
        ]

        return {
            "train": train_data,
            "validation": validation_data,
            "stats": {
                "total": len(dataset),
                "train": len(train_data),
                "validation": len(validation_data),
                "classes": sorted(set(labels)),
            },
    }

    def check_direction_training_readiness(self, dataset_result):

        dataset = dataset_result["data"]

        valid_directions = {
            "meningkat",
            "menurun",
            "netral",
        }

        class_counts = {
            direction: 0
            for direction in valid_directions
        }

        for item in dataset:

            label = item["label"]

            if label in valid_directions:
                class_counts[label] += 1

        missing_classes = [
            direction
            for direction, count in class_counts.items()
            if count == 0
        ]

        insufficient_classes = [
            direction
            for direction, count in class_counts.items()
            if 0 < count < 2
        ]

        if missing_classes:
            reason = (
                "Masih ada kelas Direction tanpa data."
            )

            return {
                "ready": False,
                "reason": reason,
                "total": len(dataset),
                "num_classes": sum(
                    count > 0
                    for count in class_counts.values()
                ),
                "classes": class_counts,
                "missing_classes": missing_classes,
                "insufficient_classes": insufficient_classes,
            }

        if insufficient_classes:

            reason = (
                "Masih ada kelas Direction "
                "dengan kurang dari 2 data."
            )

            return {
                "ready": False,
                "reason": reason,
                "total": len(dataset),
                "num_classes": sum(
                    count > 0
                    for count in class_counts.values()
                ),
                "classes": class_counts,
                "missing_classes": missing_classes,
                "insufficient_classes": insufficient_classes,
            }

        return {
            "ready": True,
            "reason": "Dataset Direction siap untuk training.",
            "total": len(dataset),
            "num_classes": 3,
            "classes": class_counts,
            "missing_classes": [],
            "insufficient_classes": [],
        }

    def check_kbli_training_readiness(self, dataset_result):
        if not dataset_result:
            raise ValueError(
                "Dataset result tidak boleh kosong."
            )

        dataset = dataset_result.get("data")

        if dataset is None:
            raise ValueError(
                "Data dataset tidak ditemukan."
            )

        if not dataset:
            return {
                "ready": False,
                "reason": "Dataset KBLI kosong.",
                "total": 0,
                "num_classes": 0,
                "classes": {},
                "missing_classes": sorted(
                    self.KBLI_LABEL2ID.keys()
                ),
                "insufficient_classes": [],
            }

        class_counts = {
            label: 0
            for label in self.KBLI_LABEL2ID
        }

        for item in dataset:
            label = item.get("label")

            if label in class_counts:
                class_counts[label] += 1

        missing_classes = [
            label
            for label, count in class_counts.items()
            if count == 0
        ]

        insufficient_classes = [
            label
            for label, count in class_counts.items()
            if 0 < count < 2
        ]

        num_classes = sum(
            1
            for count in class_counts.values()
            if count > 0
        )

        ready = (
            len(missing_classes) == 0
            and len(insufficient_classes) == 0
        )

        if ready:
            reason = (
                "Dataset KBLI memenuhi syarat minimum "
                "untuk train/validation split."
            )
        else:
            reason_parts = []

            if missing_classes:
                reason_parts.append(
                    "Masih ada kelas KBLI tanpa data."
                )

            if insufficient_classes:
                reason_parts.append(
                    "Masih ada kelas KBLI dengan kurang "
                    "dari 2 data."
                )

            reason = " ".join(reason_parts)

        return {
            "ready": ready,
            "reason": reason,
            "total": len(dataset),
            "num_classes": num_classes,
            "classes": class_counts,
            "missing_classes": missing_classes,
            "insufficient_classes": insufficient_classes,
        }

    def train_kbli(self, dataset_result):
        config = KBLITrainingConfig()

        readiness = self.check_kbli_training_readiness(
            dataset_result
        )

        if not readiness["ready"]:
            raise ValueError(
                f"Training KBLI belum siap: "
                f"{readiness['reason']}"
            )

        prepared = self.prepare_kbli_dataset(
            dataset_result
        )

        loader = KBLIModelLoader()
        model_data = loader.load()

        tokenizer = model_data["tokenizer"]
        model = model_data["model"]

        train_dataset = KBLIDataset(
            texts=prepared["train"]["texts"],
            labels=prepared["train"]["labels"],
            tokenizer=tokenizer,
            max_length=config.max_length,
        )

        validation_dataset = KBLIDataset(
            texts=prepared["validation"]["texts"],
            labels=prepared["validation"]["labels"],
            tokenizer=tokenizer,
            max_length=config.max_length,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_dir = (
            get_kbli_candidate_root()
            / f"candidate_{timestamp}"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        training_args = TrainingArguments(
            output_dir=str(output_dir),

            num_train_epochs=config.num_train_epochs,

            per_device_train_batch_size=(
                config.per_device_train_batch_size
            ),

            per_device_eval_batch_size=(
                config.per_device_eval_batch_size
            ),

            learning_rate=config.learning_rate,

            weight_decay=config.weight_decay,

            logging_steps=config.logging_steps,

            save_strategy=config.save_strategy,

            eval_strategy=config.eval_strategy,

            report_to="none",

            use_cpu=config.use_cpu,
        )

        hf_trainer = HFTrainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=validation_dataset,
            processing_class=tokenizer,
            compute_metrics=self.compute_kbli_metrics,
        )

        hf_trainer.train()

        evaluation_result = hf_trainer.evaluate()

        metrics = {
            "accuracy": evaluation_result.get(
                "eval_accuracy"
            ),
            "macro_precision": evaluation_result.get(
                "eval_macro_precision"
            ),
            "macro_recall": evaluation_result.get(
                "eval_macro_recall"
            ),
            "macro_f1": evaluation_result.get(
                "eval_macro_f1"
            ),
            "weighted_f1": evaluation_result.get(
                "eval_weighted_f1"
            ),
        }
        hf_trainer.save_model(
            str(output_dir)
        )

        tokenizer.save_pretrained(
            str(output_dir)
        )

        return {
            "status": "SUCCESS",
            "model_type": "kbli",
            "model_path": str(output_dir),
            "dataset_size": prepared["stats"]["total"],
            "train_size": prepared["stats"]["train"],
            "validation_size": prepared["stats"]["validation"],
            "metrics": metrics,
        }

    def train_direction(self, dataset_result):

        from scraper.training.config import (
            DirectionTrainingConfig,
            get_direction_candidate_root,
        )

        config = DirectionTrainingConfig()

        readiness = self.check_direction_training_readiness(
            dataset_result
        )

        if not readiness["ready"]:
            raise ValueError(
                f"Training Direction belum siap: "
                f"{readiness['reason']}"
            )

        prepared = self.prepare_direction_dataset(
            dataset_result
        )

        loader = DirectionModelLoader()

        model_data = loader.load()

        tokenizer = model_data["tokenizer"]
        model = model_data["model"]

        train_texts = [
            item["text"]
            for item in prepared["train"]
        ]

        train_labels = [
            self.DIRECTION_LABEL2ID[item["label"]]
            for item in prepared["train"]
        ]

        validation_texts = [
            item["text"]
            for item in prepared["validation"]
        ]

        validation_labels = [
            self.DIRECTION_LABEL2ID[item["label"]]
            for item in prepared["validation"]
        ]

        train_dataset = KBLIDataset(
            texts=train_texts,
            labels=train_labels,
            tokenizer=tokenizer,
            max_length=config.max_length,
        )

        validation_dataset = KBLIDataset(
            texts=validation_texts,
            labels=validation_labels,
            tokenizer=tokenizer,
            max_length=config.max_length,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        output_dir = (
            Path(get_direction_candidate_root())
            / f"candidate_{timestamp}"
        )

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        training_args = TrainingArguments(
            output_dir=str(output_dir),
            num_train_epochs=config.num_train_epochs,
            per_device_train_batch_size=(
                config.per_device_train_batch_size
            ),
            per_device_eval_batch_size=(
                config.per_device_eval_batch_size
            ),
            learning_rate=config.learning_rate,
            weight_decay=config.weight_decay,
            logging_steps=config.logging_steps,
            save_strategy=config.save_strategy,
            eval_strategy=config.eval_strategy,
            report_to="none",
            use_cpu=config.use_cpu,
        )

        hf_trainer = HFTrainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=validation_dataset,
            compute_metrics=self.compute_direction_metrics,
        )

        hf_trainer.train()

        evaluation_result = hf_trainer.evaluate()

        metrics = {
            "accuracy": evaluation_result.get(
                "eval_accuracy",
                0.0,
            ),
            "macro_precision": evaluation_result.get(
                "eval_macro_precision",
                0.0,
            ),
            "macro_recall": evaluation_result.get(
                "eval_macro_recall",
                0.0,
            ),
            "macro_f1": evaluation_result.get(
                "eval_macro_f1",
                0.0,
            ),
            "weighted_f1": evaluation_result.get(
                "eval_weighted_f1",
                0.0,
            ),
        }

        hf_trainer.save_model(
            str(output_dir)
        )

        tokenizer.save_pretrained(
            str(output_dir)
        )

        return {
            "status": "SUCCESS",
            "model_type": "direction",
            "model_path": str(output_dir),
            "dataset_size": len(dataset_result["data"]),
            "train_size": len(train_dataset),
            "validation_size": len(validation_dataset),
            "metrics": metrics,
        }

    def train(self, model_type, dataset_result):
        if model_type not in self.VALID_MODEL_TYPES:
            raise ValueError(
                f"Model type tidak valid: {model_type}"
            )

        if not dataset_result:
            raise ValueError(
                "Dataset result tidak boleh kosong."
            )

        dataset = dataset_result.get("data")
        stats = dataset_result.get("stats")

        if dataset is None:
            raise ValueError(
                "Dataset tidak ditemukan."
            )

        if stats is None:
            raise ValueError(
                "Statistik dataset tidak ditemukan."
            )

        if not dataset:
            raise ValueError(
                "Dataset training kosong."
            )

        return {
            "model_type": model_type,
            "dataset_size": len(dataset),
            "dataset_stats": stats,
            "status": "CANDIDATE",
            "model_path": self._get_candidate_path(model_type),
        }

    def compute_kbli_metrics(self, eval_prediction):
        """
        Mengubah output Hugging Face Trainer menjadi
        label KBLI A-U lalu menghitung metrik evaluasi.
        """

        import numpy as np

        logits = eval_prediction.predictions
        true_label_ids = eval_prediction.label_ids

        # Jika predictions berbentuk tuple
        if isinstance(logits, tuple):
            logits = logits[0]

        predicted_label_ids = np.argmax(
            logits,
            axis=-1,
        )

        id2label = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E",
            5: "F",
            6: "G",
            7: "H",
            8: "I",
            9: "J",
            10: "K",
            11: "L",
            12: "M",
            13: "N",
            14: "O",
            15: "P",
            16: "Q",
            17: "R",
            18: "S",
            19: "T",
            20: "U",
        }

        true_labels = [
            id2label[int(label_id)]
            for label_id in true_label_ids
        ]

        predicted_labels = [
            id2label[int(label_id)]
            for label_id in predicted_label_ids
        ]

        result = self.evaluator.evaluate_kbli(
            true_labels=true_labels,
            predicted_labels=predicted_labels,
        )

        return {
            "accuracy": result["accuracy"],
            "macro_precision": result["macro_precision"],
            "macro_recall": result["macro_recall"],
            "macro_f1": result["macro_f1"],
            "weighted_f1": result["weighted_f1"],
        }

    def compute_direction_metrics(self, eval_prediction):

        predictions = eval_prediction.predictions
        labels = eval_prediction.label_ids

        predicted_ids = predictions.argmax(
            axis=-1
        )

        id2label = {
            0: "meningkat",
            1: "menurun",
            2: "netral",
        }

        true_labels = [
            id2label[int(label)]
            for label in labels
        ]

        predicted_labels = [
            id2label[int(label)]
            for label in predicted_ids
        ]

        result = self.evaluator.evaluate_direction(
            true_labels=true_labels,
            predicted_labels=predicted_labels,
        )

        return {
            "accuracy": result["accuracy"],
            "macro_precision": result["macro_precision"],
            "macro_recall": result["macro_recall"],
            "macro_f1": result["macro_f1"],
            "weighted_f1": result["weighted_f1"],
        }

    def _get_candidate_path(self, model_type):
        base_path = Path("models") / "candidates"

        return str(
            base_path / f"{model_type}_candidate"
        )