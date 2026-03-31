import json
import pytest
from unittest.mock import MagicMock


def make_job(**kwargs) -> dict:
    defaults = {
        "id": "job-1",
        "title": "Cardiologist Needed in Texas",
        "city": "Austin",
        "state": "TX",
        "specialty": "",
        "job_type": "Locum Tenens",
        "compensation": "$200-250/hr",
        "description_bullets": ["12-week assignment", "50 patients/day"],
        "url": "https://www.comphealth.com/jobs/job-1",
    }
    return {**defaults, **kwargs}


def make_claude_response(data: dict) -> MagicMock:
    response = MagicMock()
    response.content = [MagicMock()]
    response.content[0].text = json.dumps(data)
    return response


class TestIdentifyFacility:
    def test_returns_structured_result_on_success(self):
        import identifier
        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_claude_response({
            "facility_name": "St. David's Medical Center",
            "facility_type": "Community Hospital",
            "confidence": "high",
            "reasoning": "Only major cardiac center in Austin",
            "alternative_facility": "Ascension Seton",
        })
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "St. David's Medical Center"
        assert result["confidence"] == "high"
        assert "reasoning" in result

    def test_retries_once_on_invalid_json(self):
        import identifier
        mock_client = MagicMock()
        valid_response = make_claude_response({
            "facility_name": "Regional Hospital",
            "facility_type": "Hospital",
            "confidence": "medium",
            "reasoning": "Best match",
            "alternative_facility": None,
        })
        mock_client.messages.create.side_effect = [
            MagicMock(content=[MagicMock(text="not valid json")]),
            valid_response,
        ]
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "Regional Hospital"
        assert mock_client.messages.create.call_count == 2

    def test_returns_unable_to_identify_after_two_failures(self):
        import identifier
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(
            content=[MagicMock(text="not json")]
        )
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "Unable to identify"
        assert result["confidence"] == "none"

    def test_returns_unable_to_identify_on_missing_required_keys(self):
        import identifier
        mock_client = MagicMock()
        # Response missing 'reasoning' key
        mock_client.messages.create.return_value = make_claude_response({
            "facility_name": "Some Hospital",
            "confidence": "high",
        })
        result = identifier.identify_facility(mock_client, make_job())
        assert result["facility_name"] == "Unable to identify"

    def test_alternative_facility_defaults_to_none_when_absent(self):
        import identifier
        mock_client = MagicMock()
        mock_client.messages.create.return_value = make_claude_response({
            "facility_name": "City Hospital",
            "facility_type": "Hospital",
            "confidence": "low",
            "reasoning": "Only hospital in area",
        })
        result = identifier.identify_facility(mock_client, make_job())
        assert result.get("alternative_facility") is None
