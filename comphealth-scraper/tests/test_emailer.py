import os
import pytest
from unittest.mock import MagicMock, patch


def make_enriched_job(**kwargs) -> dict:
    defaults = {
        "id": "job-1",
        "title": "Cardiologist in TX",
        "location": "Austin, TX",
        "specialty": "",
        "job_type": "Locum Tenens",
        "url": "https://www.comphealth.com/jobs/job-1",
        "identification": {
            "facility_name": "St. David's Medical Center",
            "facility_type": "Community Hospital",
            "confidence": "high",
            "reasoning": "Only major cardiac center",
            "alternative_facility": "Ascension Seton",
        },
    }
    return {**defaults, **kwargs}


class TestBuildTable:
    def test_returns_no_postings_message_for_empty_list(self):
        import emailer
        html = emailer.build_table([])
        assert "No new job postings" in html

    def test_includes_job_title(self):
        import emailer
        html = emailer.build_table([make_enriched_job()])
        assert "Cardiologist in TX" in html

    def test_includes_facility_name(self):
        import emailer
        html = emailer.build_table([make_enriched_job()])
        assert "St. David's Medical Center" in html

    def test_includes_alternative_facility(self):
        import emailer
        html = emailer.build_table([make_enriched_job()])
        assert "Ascension Seton" in html

    def test_omits_also_possible_when_alternative_is_none(self):
        import emailer
        job = make_enriched_job()
        job["identification"]["alternative_facility"] = None
        html = emailer.build_table([job])
        assert "Also possible" not in html

    def test_high_confidence_uses_green_background(self):
        import emailer
        html = emailer.build_table([make_enriched_job()])
        assert "#d4edda" in html

    def test_unable_to_identify_uses_gray_background(self):
        import emailer
        job = make_enriched_job()
        job["identification"] = {
            "facility_name": "Unable to identify",
            "confidence": "none",
            "reasoning": "",
            "alternative_facility": None,
        }
        html = emailer.build_table([job])
        assert "#e2e3e5" in html

    def test_includes_link_to_job(self):
        import emailer
        html = emailer.build_table([make_enriched_job()])
        assert "https://www.comphealth.com/jobs/job-1" in html


class TestBuildSuccessEmail:
    def test_subject_includes_count(self):
        import emailer
        subject, _ = emailer.build_success_email([make_enriched_job()])
        assert "1 new posting" in subject

    def test_subject_no_postings_when_empty(self):
        import emailer
        subject, _ = emailer.build_success_email([])
        assert "No new postings" in subject


class TestBuildFailureEmail:
    def test_subject_includes_failed(self):
        import emailer
        subject, _ = emailer.build_failure_email("Site unreachable")
        assert "Failed" in subject

    def test_body_includes_reason(self):
        import emailer
        _, body = emailer.build_failure_email("Site unreachable")
        assert "Site unreachable" in body


class TestSendEmailGmail:
    def test_sends_via_gmail_smtp(self):
        import emailer
        env = {
            "EMAIL_TRANSPORT": "gmail",
            "GMAIL_USER": "sender@gmail.com",
            "GMAIL_APP_PASSWORD": "app-pass",
            "RECIPIENT_EMAIL": "tyler@connecthealthstaff.com",
        }
        with patch.dict(os.environ, env):
            with patch("smtplib.SMTP") as mock_smtp_class:
                mock_server = MagicMock()
                mock_smtp_class.return_value.__enter__ = MagicMock(return_value=mock_server)
                mock_smtp_class.return_value.__exit__ = MagicMock(return_value=False)
                emailer.send_email("Subject", "<p>body</p>", is_html=True)
                mock_server.sendmail.assert_called_once()


class TestSendEmailSendGrid:
    def test_sends_via_sendgrid(self):
        import emailer
        env = {
            "EMAIL_TRANSPORT": "sendgrid",
            "SENDGRID_API_KEY": "SG.fake",
            "GMAIL_USER": "sender@gmail.com",
            "RECIPIENT_EMAIL": "tyler@connecthealthstaff.com",
        }
        with patch.dict(os.environ, env):
            with patch("sendgrid.SendGridAPIClient") as mock_sg_class:
                mock_sg = MagicMock()
                mock_sg_class.return_value = mock_sg
                emailer.send_email("Subject", "<p>body</p>", is_html=True)
                mock_sg.send.assert_called_once()
