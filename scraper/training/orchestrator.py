from scraper.training.evaluation_set_manager import EvaluationSetManager
from scraper.training.job_manager import TrainingJobManager
from scraper.training.dataset_builder import DatasetBuilder
from scraper.training.trainer import Trainer
from scraper.training.model_registry import ModelRegistry
from scraper.training.evaluator import Evaluator


class TrainingOrchestrator:

    def __init__(self):
        self.job_manager = TrainingJobManager()
        self.dataset_builder = DatasetBuilder()
        self.trainer = Trainer()
        self.registry = ModelRegistry()
        self.evaluation_set_manager = EvaluationSetManager()

    def run_kbli_training(self):

        # 1. Buat training job
        job = self.job_manager.create_job("kbli")

        try:

            # 2. Ubah status PENDING → RUNNING
            self.job_manager.start_job(job)

            # 3. Bangun dataset
            dataset_result = (
                self.dataset_builder.build_kbli_dataset()
            )

            # 4. Cek kesiapan dataset
            readiness = (
                self.trainer.check_kbli_training_readiness(
                    dataset_result
                )
            )

            if not readiness["ready"]:
                raise ValueError(
                    f"Training KBLI belum siap: "
                    f"{readiness['reason']}"
                )

            # 5. Training candidate model
            training_result = (
                self.trainer.train_kbli(
                    dataset_result
                )
            )

            # 6. Daftarkan hasil training sebagai candidate
            candidate = self.registry.register_candidate(
                model_type="kbli",
                model_path=training_result["model_path"],
                metrics=training_result["metrics"],
            )

            # 7. Evaluasi candidate
            evaluation = (
                self.evaluate_kbli_candidate(
                    candidate
                )
            )

            # 8. Job berhasil
            self.job_manager.success_job(
                job,
                dataset_size=training_result[
                    "dataset_size"
                ],
                metrics=training_result[
                    "metrics"
                ],
                model_path=training_result[
                    "model_path"
                ],
            )

            return {
                "status": "SUCCESS",
                "job_id": job.id,
                "training": training_result,
                "candidate": {
                    "id": candidate.id,
                    "version": candidate.version,
                    "status": candidate.status,
                },
                "evaluation": evaluation,
                "readiness": readiness,
            }

        except Exception as error:

            self.job_manager.failed_job(
                job,
                error,
            )

            raise

    def run_direction_training(self):

        # 1. Buat training job
        job = self.job_manager.create_job("direction")

        try:

            # 2. PENDING → RUNNING
            self.job_manager.start_job(job)

            # 3. Bangun dataset Direction
            dataset_result = (
                self.dataset_builder.build_direction_dataset()
            )

            # 4. Cek kesiapan dataset
            readiness = (
                self.trainer.check_direction_training_readiness(
                    dataset_result
                )
            )

            if not readiness["ready"]:
                raise ValueError(
                    f"Training Direction belum siap: "
                    f"{readiness['reason']}"
                )

            # 5. Training candidate model
            training_result = (
                self.trainer.train_direction(
                    dataset_result
                )
            )

            # 6. Daftarkan candidate
            candidate = self.registry.register_candidate(
                model_type="direction",
                model_path=training_result["model_path"],
                metrics=training_result["metrics"],
            )

            # 7. Evaluasi candidate
            evaluation = (
                self.evaluate_direction_candidate(
                    candidate
                )
            )

            # 8. Job berhasil
            self.job_manager.success_job(
                job,
                dataset_size=training_result[
                    "dataset_size"
                ],
                metrics=training_result[
                    "metrics"
                ],
                model_path=training_result[
                    "model_path"
                ],
            )

            return {
                "status": "SUCCESS",
                "job_id": job.id,
                "training": training_result,
                "candidate": {
                    "id": candidate.id,
                    "version": candidate.version,
                    "status": candidate.status,
                },
                "evaluation": evaluation,
                "readiness": readiness,
            }

        except Exception as error:

            self.job_manager.failed_job(
                job,
                error,
            )

            raise

    def evaluate_kbli_candidate(self, candidate):

        active_model = (
            self.registry.get_active_model("kbli")
        )

        evaluation_samples = (
            self.evaluation_set_manager
            .get_evaluation_samples("kbli")
        )

        if not evaluation_samples.exists():
            raise ValueError(
                "Evaluation set KBLI belum tersedia."
            )

        evaluator = Evaluator()

        active_model_path = (
            self.registry.resolve_model_path(
                active_model
            )
        )

        candidate_model_path = (
            self.registry.resolve_model_path(
                candidate
            )
        )

        active_metrics = evaluator.evaluate_kbli_model(
            evaluation_samples=evaluation_samples,
            model_path=active_model_path,
        )

        candidate_metrics = evaluator.evaluate_kbli_model(
            evaluation_samples=evaluation_samples,
            model_path=candidate_model_path,
        )

        should_promote = self.registry.should_promote(
            candidate_metrics=candidate_metrics,
            active_metrics=active_metrics,
        )

        if should_promote:

            promoted = self.registry.promote_candidate(
                candidate
            )

            return {
                "status": "PROMOTED",
                "candidate_id": promoted.id,
                "version": promoted.version,
                "active_metrics": active_metrics,
                "candidate_metrics": candidate_metrics,
            }

        candidate.status = "REJECTED"

        candidate.save(
            update_fields=["status"]
        )

        return {
            "status": "REJECTED",
            "candidate_id": candidate.id,
            "version": candidate.version,
            "active_metrics": active_metrics,
            "candidate_metrics": candidate_metrics,
        }

    def evaluate_direction_candidate(self, candidate):

        active_model = (
            self.registry.get_active_model("direction")
        )

        evaluation_samples = (
            self.evaluation_set_manager
            .get_evaluation_samples("direction")
        )

        if not evaluation_samples.exists():
            raise ValueError(
                "Evaluation set Direction belum tersedia."
            )

        evaluator = Evaluator()

        active_model_path = (
            self.registry.resolve_model_path(
                active_model
            )
        )

        candidate_model_path = (
            self.registry.resolve_model_path(
                candidate
            )
        )

        active_metrics = evaluator.evaluate_direction_model(
            evaluation_samples=evaluation_samples,
            model_path=active_model_path,
        )

        candidate_metrics = evaluator.evaluate_direction_model(
            evaluation_samples=evaluation_samples,
            model_path=candidate_model_path,
        )

        should_promote = self.registry.should_promote(
            candidate_metrics=candidate_metrics,
            active_metrics=active_metrics,
        )

        if should_promote:

            promoted = self.registry.promote_candidate(
                candidate
            )

            return {
                "status": "PROMOTED",
                "candidate_id": promoted.id,
                "version": promoted.version,
                "active_metrics": active_metrics,
                "candidate_metrics": candidate_metrics,
            }

        candidate.status = "REJECTED"

        candidate.save(
            update_fields=["status"]
        )

        return {
            "status": "REJECTED",
            "candidate_id": candidate.id,
            "version": candidate.version,
            "active_metrics": active_metrics,
            "candidate_metrics": candidate_metrics,
        }