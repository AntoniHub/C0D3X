from enum import StrEnum

from pydantic import BaseModel, ConfigDict


class Category(StrEnum):
    PRODUCT_DEFECT = "product_defect"
    TEST_DEFECT = "test_defect"
    ENVIRONMENT = "environment"
    FLAKY = "flaky"


class Confidence(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Failure(BaseModel):
    model_config = ConfigDict(frozen=True)

    test_id: str
    message: str
    details: str


class Triage(BaseModel):
    category: Category
    confidence: Confidence
    summary: str
    suspected_cause: str
    next_step: str
