from concurrent.futures import ThreadPoolExecutor, as_completed


class TruckScraperService:

    def __init__(self, http_client, parser, repository):
        self.http = http_client
        self.parser = parser
        self.repo = repository

    def scrape_brand(self, brand_url: str, output_file: str, workers: int = 5):
        first_html = self.http.get(brand_url)
        if not first_html:
            return

        total_pages = self.parser.extract_total_pages(first_html)
        all_results = []

        def process_page(page):
            url = f"{brand_url}?page={page}"
            html = self.http.get(url)
            if not html:
                return []

            listings = self.parser.parse_listing_page(html)

            enriched = []
            for item in listings:
                detail_html = self.http.get(item["link"])
                if detail_html:
                    details = self.parser.parse_details(detail_html)
                    enriched.append({**item, **details})

            return enriched

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [
                executor.submit(process_page, page)
                for page in range(1, total_pages + 1)
            ]

            for future in as_completed(futures):
                all_results.extend(future.result())

        self.repo.save(output_file, all_results)
        self.repo.deduplicate(output_file)