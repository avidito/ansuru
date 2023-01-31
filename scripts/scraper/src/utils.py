import csv

COLUMNS = [
    "latest_dt",
    "latest_chp",
    "latest_url"
]

def export_to_csv(filename: str, data: list):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()

        for row in data:
            writer.writerow(row)