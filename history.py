import csv
from typing import List


def write(url: str) -> None:
    with open("history.csv", "a", newline='') as f:
        f.write(url + ",")


def read() -> List[str]:
    try:
        with open("history.csv", "r") as f:
            reader = csv.reader(f)
            return list(reader)[0][:-1]
    except FileNotFoundError:
        return []


def write_empty(url: str) -> None:
    with open("errors.csv", "a", newline='') as f:
        f.write(url + ",")
