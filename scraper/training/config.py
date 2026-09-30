from dataclasses import dataclass
from pathlib import Path


@dataclass
class KBLITrainingConfig:

    # Base model
    model_path: str = "models/KBLI/model_kbli"

    # Candidate model
    candidate_root: str = "models/candidates/kbli"

    # Dataset
    max_length: int = 256
    validation_size: float = 0.2
    random_state: int = 42

    # Training
    num_train_epochs: int = 2
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    learning_rate: float = 2e-5
    weight_decay: float = 0.01

    # Logging / checkpoint
    logging_steps: int = 10
    save_strategy: str = "epoch"
    eval_strategy: str = "epoch"

    # CPU
    use_cpu: bool = True

@dataclass
class DirectionTrainingConfig:

    # Base model
    model_path: str = "models/direction/finbert-indonesia"

    # Candidate model
    candidate_root: str = "models/candidates/direction"

    # Dataset
    max_length: int = 256
    validation_size: float = 0.2
    random_state: int = 42

    # Training
    num_train_epochs: int = 2
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    learning_rate: float = 2e-5
    weight_decay: float = 0.01

    # Logging / checkpoint
    logging_steps: int = 10
    save_strategy: str = "epoch"
    eval_strategy: str = "epoch"

    # CPU
    use_cpu: bool = True

@dataclass
class SummarizationTrainingConfig:
    model_name: str = "models/summarizer/model_indonesian_summarizer"

    max_input_length: int = 512
    max_target_length: int = 128

    train_batch_size: int = 2
    eval_batch_size: int = 2

    learning_rate: float = 5e-5
    num_train_epochs: int = 3
    weight_decay: float = 0.01

    warmup_ratio: float = 0.1

    num_beams: int = 4
    generation_max_length: int = 128

    seed: int = 42

def get_project_root():
    return Path(__file__).resolve().parents[2]


def get_kbli_model_path():
    return (
        get_project_root()
        / "models"
        / "KBLI"
        / "model_kbli"
    )


def get_kbli_candidate_root():
    return (
        get_project_root()
        / "models"
        / "candidates"
        / "kbli"
    )

def get_direction_model_path():
    return (
        get_project_root()
        / "models"
        / "direction"
        / "finbert-indonesia"
    )


def get_direction_candidate_root():
    return (
        get_project_root()
        / "models"
        / "candidates"
        / "direction"
    )