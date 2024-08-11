import csv
from typing import List


def write(url: str) -> None:
    with open("history.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([url])


def read() -> List[str]:
    try:
        with open("history.csv", "r") as f:
            reader = csv.reader(f)
            return list(reader)[0]
    except FileNotFoundError:
        return []


def write_empty(url: str) -> None:
    with open("errors.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([url])
