import csv
import os


class FileRepository:

    FIELDNAMES = ["title", "link", "price", "mileage"]

    def save(self, filename: str, rows: list[dict]):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=self.FIELDNAMES,
                delimiter="\t"
            )
            writer.writeheader()
            writer.writerows(rows)

    def deduplicate(self, filename: str):
        seen = set()
        unique_rows = []

        with open(filename, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
            for row in reader:
                if row["link"] not in seen:
                    seen.add(row["link"])
                    unique_rows.append(row)

        self.save(filename, unique_rows)