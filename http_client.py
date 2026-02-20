import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HTTPClient:
    def __init__(self):
        self.session = self._create_session()

    def _create_session(self):
        session = requests.Session()

        retry = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        session.headers.update({
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "fr-FR,fr;q=0.9"
        })

        return session

    def get(self, url: str) -> str | None:
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception:
            return None