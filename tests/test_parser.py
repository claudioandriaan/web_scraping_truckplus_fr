import pytest
from parser import TruckParser

@pytest.fixture
def parser():
    return TruckParser()


def test_extract_total_pages(parser):
    html = """
    <ul>
        <li class="last"><a>4</a></li>
    </ul>
    """

    assert parser.extract_total_pages(html) == 4


def test_parse_listing_page(parser):
    html = """
    <div id="plp-results">
        <div id="wrap-plp-list">
            <a href="/truck-1">
                <h2>Truck A</h2>
            </a>
        </div>
    </div>
    """

    results = parser.parse_listing_page(html)

    assert len(results) == 1
    assert results[0]["title"] == "Truck A"
    assert "truck-1" in results[0]["link"]