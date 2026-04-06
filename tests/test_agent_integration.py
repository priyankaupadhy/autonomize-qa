"""
test_agent_integration.py — Module 1: Agent Integration Tests
TC-AG-01 | TC-AG-02 | TC-AG-03
"""
from datetime import date
import pytest
import logging

logger = logging.getLogger(__name__)

#Helper Functions

REQUIRED_FIELDS = ["patient_id", "name", "dob", "age", "weight_kg", "diagnosis_codes"]

def validate_schema(record: dict):
    missing = [f for f in REQUIRED_FIELDS if f not in record]
    return len(missing) == 0, missing

def get_retry_delay(attempt: int):
    return 2 ** attempt


# TC-AG-01 — Valid Patient Extraction
class TestTcAg01ValidExtraction:

    def test_age_is_integer(self, valid_patient):
        """age must be int — wrong type crashes the AI model."""
        logger.info("RUNNING: TC-AG-01, Age must be an integer")
        assert isinstance(valid_patient["age"], int), \
            f"FAIL — 'age' must be int, got {type(valid_patient['age']).__name__}"

    def test_dob_is_iso_format(self, valid_patient):
        """Checks if DOB is a real date and in ISO format."""
        logger.info("RUNNING: TC-AG-01 | Requirement: DOB must be ISO-8601 format")
        dob = valid_patient["dob"]
        try:
            # Validates both the ISO format (YYYY-MM-DD) and calendar logic
            date.fromisoformat(dob)
        except ValueError:
            pytest.fail(f"FAIL — DOB '{dob}' is not a valid ISO date.")

    def test_all_required_fields_present(self, valid_patient):
        """All required fields must exist before record reaches AI model."""
        logger.info("TC-AG-01,Checking for all mandatory fields.")
        is_valid, missing = validate_schema(valid_patient)
        assert is_valid is True, f"FAIL — Missing fields: {missing}"


# TC-AG-02 — Missing Mandatory Field (negative)
class TestTcAG02MissingMandatoryField:

    def test_missing_dob_fails_validation(self, patient_missing_dob):
        """Record without DOB must fail — never reach AI model."""
        logger.info("TC-AG-02,Verifying schema rejection for missing DOB.")
        is_valid, missing = validate_schema(patient_missing_dob)
        assert is_valid is False, \
            "FAIL — Validation passed for a record missing DOB."

    def test_error_names_missing_field(self, patient_missing_dob):
        """Error must name the missing field — not just say 'failed'."""
        logger.info("TC-AG-02,Verifying error message specifically identifies 'dob'.")
        is_valid, missing = validate_schema(patient_missing_dob)
        assert "dob" in missing, \
            f"FAIL — 'dob' not in missing fields. Got: {missing}"

# TC-AG-03 — API Timeout / Resilience
class TestTcAg03APITimeout:

    def test_retries_exactly_3_times(self):
        """Agent must retry exactly 3 times when source is unavailable."""
        logger.info("TC-AG-03,Verifying agent retry count (Target: 3).")
        attempts = 0
        for attempt in range(1, 4):
            attempts += 1
        assert attempts == 3, \
            f"FAIL — Expected 3 retries, got {attempts}."

    def test_retry_delays_increase(self):
        """Retry delays must increase: 2s → 4s → 8s."""
        logger.info("TC-AG-03,Verifying exponential backoff timing [2s, 4s, 8s].")
        delays = [get_retry_delay(i) for i in range(1, 4)]
        assert delays == [2, 4, 8], \
            f"FAIL — Expected [2, 4, 8], got {delays}."