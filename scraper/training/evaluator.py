from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
)

from scraper.kbli.service import KBLIService
from scraper.direction.service import DirectionService
from rouge_score import rouge_scorer
from scraper.summarization.service import SummarizationService



class Evaluator:

    VALID_KBLI_LABELS = list(
        "ABCDEFGHIJKLMNOPQRSTU"
    )
    VALID_DIRECTION_LABELS = [
        "meningkat",
        "menurun",
        "netral",
    ]

    def evaluate_kbli(
        self,
        true_labels,
        predicted_labels,
    ):
        if true_labels is None:
            raise ValueError(
                "True labels tidak boleh None."
            )

        if predicted_labels is None:
            raise ValueError(
                "Predicted labels tidak boleh None."
            )

        if len(true_labels) == 0:
            raise ValueError(
                "True labels kosong."
            )

        if len(true_labels) != len(predicted_labels):
            raise ValueError(
                "Jumlah true labels dan predicted labels "
                "harus sama."
            )

        invalid_true = [
            label
            for label in true_labels
            if label not in self.VALID_KBLI_LABELS
        ]

        invalid_predicted = [
            label
            for label in predicted_labels
            if label not in self.VALID_KBLI_LABELS
        ]

        if invalid_true:
            raise ValueError(
                f"True labels tidak valid: {invalid_true}"
            )

        if invalid_predicted:
            raise ValueError(
                f"Predicted labels tidak valid: "
                f"{invalid_predicted}"
            )

        labels = self.VALID_KBLI_LABELS

        accuracy = accuracy_score(
            true_labels,
            predicted_labels,
        )

        precision = precision_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="macro",
            zero_division=0,
        )

        recall = recall_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="macro",
            zero_division=0,
        )

        f1 = f1_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="macro",
            zero_division=0,
        )

        weighted_f1 = f1_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="weighted",
            zero_division=0,
        )

        matrix = confusion_matrix(
            true_labels,
            predicted_labels,
            labels=labels,
        )

        return {
            "accuracy": float(accuracy),
            "macro_precision": float(precision),
            "macro_recall": float(recall),
            "macro_f1": float(f1),
            "weighted_f1": float(weighted_f1),
            "labels": labels,
            "confusion_matrix": matrix.tolist(),
            "total_samples": len(true_labels),
        }

    def evaluate_direction(
        self,
        true_labels,
        predicted_labels,
    ):
        if true_labels is None:
            raise ValueError(
                "True labels tidak boleh None."
            )

        if predicted_labels is None:
            raise ValueError(
                "Predicted labels tidak boleh None."
            )

        if len(true_labels) == 0:
            raise ValueError(
                "True labels kosong."
            )

        if len(true_labels) != len(predicted_labels):
            raise ValueError(
                "Jumlah true labels dan predicted labels "
                "harus sama."
            )

        invalid_true = [
            label
            for label in true_labels
            if label not in self.VALID_DIRECTION_LABELS
        ]

        invalid_predicted = [
            label
            for label in predicted_labels
            if label not in self.VALID_DIRECTION_LABELS
        ]

        if invalid_true:
            raise ValueError(
                f"True labels tidak valid: {invalid_true}"
            )

        if invalid_predicted:
            raise ValueError(
                f"Predicted labels tidak valid: "
                f"{invalid_predicted}"
            )

        labels = self.VALID_DIRECTION_LABELS

        accuracy = accuracy_score(
            true_labels,
            predicted_labels,
        )

        precision = precision_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="macro",
            zero_division=0,
        )

        recall = recall_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="macro",
            zero_division=0,
        )

        f1 = f1_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="macro",
            zero_division=0,
        )

        weighted_f1 = f1_score(
            true_labels,
            predicted_labels,
            labels=labels,
            average="weighted",
            zero_division=0,
        )

        matrix = confusion_matrix(
            true_labels,
            predicted_labels,
            labels=labels,
        )

        return {
            "accuracy": float(accuracy),
            "macro_precision": float(precision),
            "macro_recall": float(recall),
            "macro_f1": float(f1),
            "weighted_f1": float(weighted_f1),
            "labels": labels,
            "confusion_matrix": matrix.tolist(),
            "total_samples": len(true_labels),
        }

    def evaluate_summarization(
        self,
        references,
        predictions,
    ):
        if references is None:
            raise ValueError(
                "References tidak boleh None."
            )

        if predictions is None:
            raise ValueError(
                "Predictions tidak boleh None."
            )

        if len(references) == 0:
            raise ValueError(
                "References kosong."
            )

        if len(references) != len(predictions):
            raise ValueError(
                "Jumlah references dan predictions "
                "harus sama."
            )

        for index, reference in enumerate(references):
            if not isinstance(reference, str):
                raise ValueError(
                    f"Reference pada index {index} "
                    "harus berupa string."
                )

            if not reference.strip():
                raise ValueError(
                    f"Reference pada index {index} "
                    "tidak boleh kosong."
                )

        for index, prediction in enumerate(predictions):
            if not isinstance(prediction, str):
                raise ValueError(
                    f"Prediction pada index {index} "
                    "harus berupa string."
                )

            if not prediction.strip():
                raise ValueError(
                    f"Prediction pada index {index} "
                    "tidak boleh kosong."
                )

        scorer = rouge_scorer.RougeScorer(
            [
                "rouge1",
                "rouge2",
                "rougeL",
            ],
            use_stemmer=False,
        )

        rouge1_scores = []
        rouge2_scores = []
        rougeL_scores = []

        for reference, prediction in zip(
            references,
            predictions,
        ):
            scores = scorer.score(
                reference,
                prediction,
            )

            rouge1_scores.append(
                scores["rouge1"].fmeasure
            )

            rouge2_scores.append(
                scores["rouge2"].fmeasure
            )

            rougeL_scores.append(
                scores["rougeL"].fmeasure
            )

        return {
            "rouge1": float(
                sum(rouge1_scores)
                / len(rouge1_scores)
            ),
            "rouge2": float(
                sum(rouge2_scores)
                / len(rouge2_scores)
            ),
            "rougeL": float(
                sum(rougeL_scores)
                / len(rougeL_scores)
            ),
            "total_samples": len(references),
        }

    def evaluate_kbli_model(
        self,
        evaluation_samples,
        model_path=None,
    ):
        if evaluation_samples is None:
            raise ValueError(
                "Evaluation samples tidak boleh None."
            )

        samples = list(evaluation_samples)

        if not samples:
            raise ValueError(
                "Evaluation samples kosong."
            )

        service = KBLIService(
            model_path=model_path
        )

        true_labels = []
        predicted_labels = []

        for sample in samples:
            article = sample.article

            true_label = article.kbli_annotation
            text = article.annotated_summary

            if not true_label:
                raise ValueError(
                    f"Article {article.id} tidak memiliki "
                    "KBLI annotation."
                )

            if not text:
                raise ValueError(
                    f"Article {article.id} tidak memiliki "
                    "annotated summary."
                )

            prediction = service.predict(text)

            if prediction is None:
                raise ValueError(
                    f"Model tidak menghasilkan prediction "
                    f"untuk Article {article.id}."
                )

            true_labels.append(true_label)
            predicted_labels.append(
                prediction["label"]
            )

        return self.evaluate_kbli(
            true_labels=true_labels,
            predicted_labels=predicted_labels,
        )

    def evaluate_direction_model(
        self,
        evaluation_samples,
        model_path=None,
    ):
        if evaluation_samples is None:
            raise ValueError(
                "Evaluation samples tidak boleh None."
            )

        samples = list(evaluation_samples)

        if not samples:
            raise ValueError(
                "Evaluation samples kosong."
            )

        service = DirectionService(
            model_path=model_path
        )

        true_labels = []
        predicted_labels = []

        for sample in samples:
            article = sample.article

            true_label = article.direction_annotation
            text = article.annotated_summary

            if not true_label:
                raise ValueError(
                    f"Article {article.id} tidak memiliki "
                    "Direction annotation."
                )

            if not text:
                raise ValueError(
                    f"Article {article.id} tidak memiliki "
                    "annotated summary."
                )

            prediction = service.predict(text)

            if prediction is None:
                raise ValueError(
                    f"Model tidak menghasilkan prediction "
                    f"untuk Article {article.id}."
                )

            true_labels.append(true_label)
            predicted_labels.append(
                prediction["label"]
            )

        return self.evaluate_direction(
            true_labels=true_labels,
            predicted_labels=predicted_labels,
        )

    def evaluate_summarization_model(
        self,
        evaluation_samples,
        model_path=None,
    ):
        if evaluation_samples is None:
            raise ValueError(
                "Evaluation samples tidak boleh None."
            )

        samples = list(evaluation_samples)

        if not samples:
            raise ValueError(
                "Evaluation samples kosong."
            )

        service = SummarizationService(
            model_path=model_path
        )

        references = []
        predictions = []

        for sample in samples:
            article = sample.article

            reference = article.annotated_summary
            text = article.content

            if not reference:
                raise ValueError(
                    f"Article {article.id} tidak memiliki "
                    "annotated summary."
                )

            if not text:
                raise ValueError(
                    f"Article {article.id} tidak memiliki "
                    "content."
                )

            prediction = service.summarize(text)

            if not prediction:
                raise ValueError(
                    f"Model tidak menghasilkan summary "
                    f"untuk Article {article.id}."
                )

            references.append(reference)
            predictions.append(prediction)

        return self.evaluate_summarization(
            references=references,
            predictions=predictions,
        )