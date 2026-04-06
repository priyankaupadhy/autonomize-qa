"""
test_model_integration.py — Model Integration Tests
TC-ML-01 | TC-ML-02 | TC-ML-03
"""
import logging

logger = logging.getLogger(__name__)


def classify_risk(patient: dict) -> dict:
    """Simulates AI risk model. Real system: replace with API call."""
    score = 0.0
    if patient.get("systolic_bp", 0) > 160:  score += 0.35
    if patient.get("cholesterol", 0) > 260:   score += 0.25
    if patient.get("age", 0) > 65:            score += 0.15
    score = min(score, 1.0)

    label = "HIGH_RISK" if score >= 0.75 else \
            "MEDIUM_RISK" if score >= 0.40 else "LOW_RISK"

    return {
        "risk_score":    round(score, 2),
        "risk_label":    label,
        "alert_fired":   label == "HIGH_RISK",
        "model_version": "v1.2",
    }


# TC-ML-01 — High Risk Patient
class TestTcMl01HighRiskClassification:

    def test_high_risk_score(self, high_risk_patient):
        """High BP + high cholesterol + age 72 must score >= 0.75."""
        logger.info("TC-ML-01,Verifying score for high-risk profile.")
        result = classify_risk(high_risk_patient)
        assert result["risk_score"] >= 0.75, \
            f"FAIL — Score {result['risk_score']} too low. Patient must be HIGH_RISK."

    def test_label_is_high_risk(self, high_risk_patient):
        """Label must be HIGH_RISK — alert system depends on this."""
        logger.info("TC-ML-01,Validating risk label is 'HIGH_RISK'.")
        result = classify_risk(high_risk_patient)
        assert result["risk_label"] == "HIGH_RISK", \
            f"FAIL — Expected HIGH_RISK, got {result['risk_label']}."

    def test_alert_fired(self, high_risk_patient):
        """Alert MUST fire for HIGH_RISK patient."""
        logger.info("TC-ML-01,Ensuring alert system triggers for safety.")
        result = classify_risk(high_risk_patient)
        assert result["alert_fired"] is True, \
            "FAIL — Alert not fired. Care team not notified."


# TC-ML-02 — Low Risk Patient
class TestTcMl02LowRiskClassification:

    def test_low_risk_score(self):
        """Healthy patient must score below 0.40."""
        logger.info("TC-ML-02,Verifying healthy patient score.")
        healthy = {"age": 35, "systolic_bp": 118, "cholesterol": 180}
        result = classify_risk(healthy)
        assert result["risk_score"] < 0.40, \
            f"FAIL — Score {result['risk_score']} too high for healthy patient."

    def test_no_alert_for_low_risk(self):
        """No alert should fire for a healthy patient."""
        logger.info("TC-ML-02,Checking for false alarms.")
        healthy = {"age": 35, "systolic_bp": 118, "cholesterol": 180}
        result = classify_risk(healthy)
        assert result["alert_fired"] is False, \
            "FAIL — False alarm fired for a LOW_RISK patient."


# TC-ML-03 — Boundary Inputs
class TestTcMl03BoundaryInputs:

    def test_score_always_between_0_and_1(self, high_risk_patient):
        """Risk score must always be 0.0 to 1.0 — never outside this range."""
        logger.info("TC-ML-03,Range check (0.0 - 1.0).")
        result = classify_risk(high_risk_patient)
        assert 0.0 <= result["risk_score"] <= 1.0, \
            f"FAIL — Score {result['risk_score']} is outside valid range."

    def test_age_zero_does_not_crash(self):
        """Age=0 (newborn) must not crash the model."""
        logger.info("TC-ML-03,Edge Case - Newborn (Age 0).")
        newborn = {"age": 0, "systolic_bp": 75, "cholesterol": 120}
        result = classify_risk(newborn)
        assert "risk_label" in result, \
            "FAIL — No result returned for newborn patient."