from service import TruckScraperService

class FakeHTTPClient:

    def get(self, url):

        # page catégorie
        if "brand" in url and "?page=" not in url:
            return "<html></html>"

        # page listing
        if "?page=1" in url:
            return """
            <div id="plp-results">
                <div id="wrap-plp-list">
                    <a href="/detail-1">
                        <h2>Truck A</h2>
                    </a>
                </div>
            </div>
            """

        # page détail
        if "detail-1" in url:
            return """
            <div class="typography-heading-2">10000€</div>
            """

        return None


class FakeParser:

    def extract_total_pages(self, html):
        return 1

    def parse_listing_page(self, html):
        return [{
            "title": "Truck A",
            "link": "http://test.com/detail-1"
        }]

    def parse_details(self, html):
        return {"price": "10000€", "mileage": ""}


class FakeRepository:

    def __init__(self):
        self.saved_rows = []

    def save(self, filename, rows):
        self.saved_rows.extend(rows)

    def deduplicate(self, filename):
        pass


def test_scrape_brand():

    http = FakeHTTPClient()
    parser = FakeParser()
    repo = FakeRepository()

    service = TruckScraperService(http, parser, repo)

    service.scrape_brand(
        brand_url="http://test.com/brand",
        output_file="dummy.tab",
        workers=1
    )

    assert len(repo.saved_rows) == 1
    assert repo.saved_rows[0]["title"] == "Truck A"
    assert repo.saved_rows[0]["price"] == "10000€"