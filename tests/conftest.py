"""
conftest.py — Shared Test Data & API Client
--------------------------------------------
Two things defined here:
  1. api_session  — shows how a real API client would be set up
  2. Patient data — plain dictionaries used as test inputs
"""

import pytest
import requests

BASE_URL = "xyz"

@pytest.fixture(scope="session")
def api_session():
    """
    Creates one shared HTTP session for the entire test run.
    scope='session' = created once, reused across all tests.
    In real testing: every API call would use this session.
    """
    session = requests.Session()
    session.headers.update({
        "Content-Type":  "application/json",
        "X-API-Key":     "test-api-key-12345",
        "X-Environment": "test",
    })
    yield session
    session.close()


# ─────────────────────────────────────────────
# PATIENT DATA FIXTURES
# Plain dictionaries — no complexity needed
# ─────────────────────────────────────────────

@pytest.fixture
def valid_patient():
    """Complete valid patient — used in TC-AG-01."""
    return {
        "patient_id":      "PT-10001",
        "name":            "John Doe",
        "dob":             "1955-06-15",
        "age":             68,
        "weight_kg":       82.5,
        "diagnosis_codes": ["E11.9", "I10"],
    }


@pytest.fixture
def patient_missing_dob():
    """Patient with DOB removed — used in TC-AG-02."""
    return {
        "patient_id":      "PT-10002",
        "name":            "Jane Doe",
        "age":             45,
        "weight_kg":       70.0,
        "diagnosis_codes": ["J45.9"],
    }


@pytest.fixture
def high_risk_patient():
    """Elderly patient with high BP and cholesterol — used in TC-ML-01."""
    return {
        "patient_id":  "PT-20002",
        "age":         72,
        "systolic_bp": 178,
        "cholesterol": 295,
    }
