import csv
from typing import List


def write(url: str) -> None:
    with open("history.csv", "a", newline='') as f:
        f.write(url + ",")


def read_file(path: str) -> List[str]:
    try:
        with open(path, "r") as f:
            reader = csv.reader(f)
            return list(reader)[0][:-1]
    except FileNotFoundError:
        return []


def read() -> List[str]:
    return read_file("history.csv") + read_file("errors.csv")


def write_empty(url: str) -> None:
    with open("errors.csv", "a", newline='') as f:
        f.write(url + ",")
