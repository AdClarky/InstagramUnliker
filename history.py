import csv
from typing import List


class History:
    def write(self, url: str) -> None:
        with open("history.csv", "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow([url])

    def read(self) -> List[str]:
        with open("history.csv", "r") as f:
            reader = csv.reader(f)
            return list(reader)[0]
