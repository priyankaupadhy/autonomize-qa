"""
test_ui_validation.py — Module 3: UI Validation Tests
TC-UI-01 | TC-UI-02 | TC-UI-03

What we are testing:
when a user makes a mistake on the screen —
  uploads wrong file type, file too big, or session expires.
"""

import logging

logger = logging.getLogger(__name__)

# ── Helper Functions ──────────────────────────
def validate_file_upload(file_name: str, page_count: int) -> tuple:
    """
    Simulates the upload validation logic.
    Returns (is_valid, error_message)
    """
    allowed_extensions = [".pdf"]
    extension = "." + file_name.split(".")[-1].lower()

    if extension not in allowed_extensions:
        return False, f"Invalid file type '{extension}'. Only PDF files are accepted."

    if page_count > 50:
        return False, f"File has {page_count} pages. Maximum allowed is 50 pages."

    return True, None


def validate_session(session_token: str) -> tuple:
    """
    Simulates session token validation.
    Returns (is_valid, error_message)
    """
    expired_tokens = ["expired-token-123", "expired-token-456"]

    if session_token in expired_tokens:
        return False, "Session expired. Please log in again and re-enter your data."

    return True, None

# TC-UI-01 — Wrong File Format(Negative, UX)
class TestTcUI01WrongFileFormat:
    """
      .docx uploaded instead of a PDF.
      System must reject it with a clear message.
    """

    def test_docx_upload_rejected(self):
        """A .docx file must be rejected — only PDF is accepted."""
        logger.info("TC-UI-01,Testing rejection of .docx file.")
        is_valid, error = validate_file_upload("patient_chart.docx", 10)
        assert is_valid is False, \
            "FAIL — .docx file was accepted. Only PDF should be allowed."

    def test_error_message_mentions_pdf(self):
        """Error must tell the user PDF is the accepted format."""
        logger.info("TC-UI-01,Verifying error message clarity for file type.")
        is_valid, error = validate_file_upload("patient_chart.docx", 10)
        assert "PDF" in error, \
            f"FAIL — Error does not mention PDF. Got: '{error}'"

    def test_pdf_upload_accepted(self):
        """A valid PDF must be accepted without errors."""
        logger.info("TC-UI-01,Verifying valid PDF upload.")
        is_valid, error = validate_file_upload("patient_chart.pdf", 10)
        assert is_valid is True, \
            f"FAIL — Valid PDF was rejected. Error: {error}"

# TC-UI-02 — File Exceeds Page Limit
class TestTcUI02FileTooLarge:
    """
      75-page PDF is uploaded (limit is 50).
      Error must tell them both the limit AND their count.
    """

    def test_75_pages_rejected(self):
        """A 75-page PDF exceeds the 50-page limit — must be rejected."""
        logger.info("TC-UI-02,Testing 75-page limit rejection.")
        is_valid, error = validate_file_upload("chart.pdf", 75)
        assert is_valid is False, \
            "FAIL — 75-page PDF was accepted. Limit is 50 pages."

    def test_error_shows_page_count_and_limit(self):
        """Error must show actual count (75) AND the limit (50)."""
        logger.info("TC-UI-02,Verifying that error shows both actual count and limit.")
        is_valid, error = validate_file_upload("chart.pdf", 75)
        assert "75" in error, \
            f"FAIL — Error does not show actual page count. Got: '{error}'"
        assert "50" in error, \
            f"FAIL — Error does not show the page limit. Got: '{error}'"

    def test_exactly_50_pages_accepted(self):
        """Exactly 50 pages = at the limit = must be accepted."""
        logger.info("TC-UI-02, Boundary Test - Exactly 50 pages.")
        is_valid, error = validate_file_upload("chart.pdf", 50)
        assert is_valid is True, \
            "FAIL — 50-page PDF rejected. Limit is 50 pages inclusive."

# TC-UI-03 — Session Timeout
class TestTcUI03SessionTimeout:
    """
      Half the form is filled and session expires.
      Must show a clear message
    """

    def test_expired_session_rejected(self):
        """An expired session token must be rejected."""
        logger.info("TC-UI-03,Verifying expired session rejection.")
        is_valid, error = validate_session("expired-token-123")
        assert is_valid is False, \
            "FAIL — Expired session was accepted."

    def test_error_message_is_actionable(self):
        """Error must tell nurse what to do — not just 'session expired'."""
        logger.info("TC-UI-03,Verifying 'Actionable' error message for Nurses.")
        is_valid, error = validate_session("expired-token-123")
        assert "log in" in error.lower() or "re-enter" in error.lower(), \
            f"FAIL — Error is not actionable. Got: '{error}'"

    def test_valid_session_accepted(self):
        """A valid session token must pass without errors."""
        logger.info("TC-UI-03,Verifying valid session access.")
        is_valid, error = validate_session("valid-token-abc")
        assert is_valid is True, \
            f"FAIL — Valid session was rejected. Error: {error}"
