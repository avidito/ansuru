import csv
import pytz
from datetime import datetime

import database

COLUMNS = [
    "manga_id",
    "manga_label",
    "website",
    "latest_tm",
    "latest_chp",
    "latest_url"
]


def export_to_csv(filename: str, data: list):
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()

        for row in data:
            writer.writerow(row)

def csv_to_postgres(filename: str, job_id: int):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        _ = next(reader)
        fmt_row = [
            tr_row(row)
            for row in reader
        ]
    
    load_to_postgres(fmt_row, job_id)

def tr_row(row: str):
    return [
        row[0],
        row[1],
        row[2],
        datetime.strptime(row[3][:11], "%b %d,%Y").date(),
        datetime.strptime(row[3], "%b %d,%Y - %H:%M %p"),
        row[4],
        row[5]
    ]

def load_to_postgres(data: list, job_id: int):
    current_dtm = datetime.now(pytz.timezone("Asia/Jakarta")) 
    prepared_data = [
        {
            "manga_id"   : row[0],
            "manga_label": row[1],
            "website"    : row[2],
            "latest_dt"  : row[3],
            "latest_tm"  : row[4],
            "latest_chp" : row[5],
            "latest_url" : row[6],
            "load_tm"    : current_dtm,
            "job_id"     : job_id,
        }
        for row in data
    ]
    conn, cursor = database.get_cursor()
    cursor.executemany(
        """
        DELETE FROM scraper_cdc
        WHERE manga_id = %(manga_id)s
          AND job_id = %(job_id)s;

        INSERT INTO scraper_cdc
        VALUES (
            %(manga_id)s,
            %(manga_label)s,
            %(website)s,
            %(latest_dt)s,
            %(latest_tm)s,
            %(latest_chp)s,
            %(latest_url)s,
            %(load_tm)s,
            %(job_id)s
        );
        """,
        prepared_data
    )
    conn.commit()
    cursor.close()