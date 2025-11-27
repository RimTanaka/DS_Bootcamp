#!/usr/bin/env python3
"""
Модуль для тестирования financial.py
"""

import pytest
from financial import fetch_financial_data


@pytest.fixture
def mock_requests_get(mocker):
    """
    Fixture для подмены функции requests.get для тестов.
    """
    mock = mocker.patch("requests.get")
    mock_response = mock.return_value
    mock_response.status_code = 200
    mock_response.text = "<html><body>Test HTML content</body></html>"
    return mock


def test_fetch_financial_data_success(mock_requests_get):
    """
    Тест успешного получения финансовых данных для указанного тикера и поля.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = """
    <html><div class="tableBody yf-9ft13">
        <div class="row lv-0 yf-t22klz"><div>Total Revenue</div><div>1,000</div></div>
        <div class="row lv-0 yf-t22klz"><div>Net Income</div><div>500</div></div>
    </div></html>"""

    ticker = "AAPL"
    field = "Total Revenue"

    result = fetch_financial_data(ticker, field)

    assert result == ["1,000"], f"Expected ['1,000'], but got {result}"


def test_return_type(mock_requests_get):
    """
    Тест на проверку типа возвращаемого значения.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = """
    <html><div class="tableBody yf-9ft13">
        <div class="row lv-0 yf-t22klz"><div>Total Revenue</div><div>1,000</div></div>
        <div class="row lv-0 yf-t22klz"><div>Net Income</div><div>500</div></div>
    </div></html>"""

    ticker = "AAPL"
    field = "Total Revenue"

    result = fetch_financial_data(ticker, field)

    assert isinstance(result, list), f"Expected result to be a list, but got {type(result)}"


def test_invalid_ticker(mock_requests_get):
    """
    Тест на обработку некорректного тикера (404).
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 404
    mock_response.text = ""

    ticker = "INVALID_TICKER"
    field = "Total Revenue"

    with pytest.raises(ValueError):
        fetch_financial_data(ticker, field)


def test_invalid_field(mock_requests_get):
    """
    Тест на обработку некорректного поля.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = """
    <html><div class="tableBody yf-9ft13">
        <div class="row lv-0 yf-t22klz"><div>Total Revenue</div><div>1,000</div></div>
        <div class="row lv-0 yf-t22klz"><div>Net Income</div><div>500</div></div>
    </div></html>"""

    ticker = "AAPL"
    field = "NonExistingField"

    with pytest.raises(ValueError):
        fetch_financial_data(ticker, field)


def test_fetch_multiple_fields(mock_requests_get):
    """
    Тест на получение нескольких полей из данных.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = """
    <html><div class="tableBody yf-9ft13">
        <div class="row lv-0 yf-t22klz"><div>Total Revenue</div><div>1,000</div></div>
        <div class="row lv-0 yf-t22klz"><div>Net Income</div><div>500</div></div>
    </div></html>"""

    ticker = "AAPL"
    fields = ["Total Revenue", "Net Income"]

    results = {}
    for field in fields:
        results[field] = fetch_financial_data(ticker, field)

    assert results["Total Revenue"] == ["1,000"]
    assert results["Net Income"] == ["500"]


def test_empty_html(mock_requests_get):
    """
    Тест на обработку пустого HTML-контента.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = ""

    ticker = "AAPL"
    field = "Total Revenue"

    with pytest.raises(ValueError):
        fetch_financial_data(ticker, field)


def test_field_not_found(mock_requests_get):
    """
    Тест на отсутствие поля в HTML.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = """
    <html><div class="tableBody yf-9ft13">
        <div class="row lv-0 yf-t22klz"><div>Total Revenue</div><div>1,000</div></div>
    </div></html>"""

    ticker = "AAPL"
    field = "Net Income"

    with pytest.raises(ValueError):
        fetch_financial_data(ticker, field)


def test_malformed_html(mock_requests_get):
    """
    Тест на обработку некорректного HTML.
    """
    mock_response = mock_requests_get.return_value
    mock_response.status_code = 200
    mock_response.text = "<html><body>Unfinished HTML"

    ticker = "AAPL"
    field = "Total Revenue"

    with pytest.raises(ValueError):
        fetch_financial_data(ticker, field)
