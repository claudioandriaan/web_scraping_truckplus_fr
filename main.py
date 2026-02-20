from http_client import HTTPClient
from  parser import TruckParser
from  repository import FileRepository
from service import TruckScraperService


def main():

    http_client = HTTPClient()
    parser = TruckParser()
    repository = FileRepository()

    service = TruckScraperService(
        http_client=http_client,
        parser=parser,
        repository=repository
    )

    start_url = "https://www.used-renault-trucks.fr"

    html = http_client.get(start_url)
    brands = parser.extract_brands(html)

    for brand in brands:
        filename = brand.rstrip("/").split("/")[-1] + ".tab"
        service.scrape_brand(brand, filename)


if __name__ == "__main__":
    main()