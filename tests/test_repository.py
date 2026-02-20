from repository import FileRepository

def test_save_and_deduplicate(tmp_path):

    repo = FileRepository()
    file_path = tmp_path / "test.tab"

    rows = [
        {"title": "A", "link": "1", "price": "10", "mileage": "100"},
        {"title": "A", "link": "1", "price": "10", "mileage": "100"},
    ]

    repo.save(file_path, rows)
    repo.deduplicate(file_path)

    with open(file_path, encoding="utf-8") as f:
        lines = f.readlines()

    # header + 1 unique row
    assert len(lines) == 2