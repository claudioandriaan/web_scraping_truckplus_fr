from bs4 import BeautifulSoup


class TruckParser:

    BASE_URL = "https://www.used-renault-trucks.fr"

    def extract_brands(self, html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        brands = []

        for a in soup.select(".vehicle-categories-filter a"):
            href = a.get("href")
            if href:
                if not href.startswith("http"):
                    href = self.BASE_URL + href
                brands.append(href)

        return list(set(brands))

    def extract_total_pages(self, html: str) -> int:
        soup = BeautifulSoup(html, "html.parser")
        last_page = soup.select_one("li.last a")

        if last_page:
            try:
                return int(last_page.text.strip())
            except:
                return 1

        return 1

    def parse_listing_page(self, html: str) -> list[dict]:
        soup = BeautifulSoup(html, "html.parser")
        results = []

        for item in soup.select("#plp-results #wrap-plp-list a"):
            title_tag = item.select_one("h2")
            link = item.get("href")

            if not title_tag or not link:
                continue

            if not link.startswith("http"):
                link = self.BASE_URL + link

            results.append({
                "title": title_tag.text.strip(),
                "link": link
            })

        return results

    def parse_details(self, html: str) -> dict:
        soup = BeautifulSoup(html, "html.parser")

        price_tag = soup.select_one("div.typography-heading-2")
        mileage_tag = soup.select_one("h1.typography-heading-2 div.typography-heading-4")

        return {
            "price": price_tag.text.strip() if price_tag else "",
            "mileage": mileage_tag.text.split("-")[0].strip() if mileage_tag else ""
        }