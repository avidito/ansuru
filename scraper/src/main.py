import os
import sys
import logging
from datetime import datetime

# Local
import scraper
import utils


def start_scraping(manga_id: str):
    logging.info(f"Start scraping for `{manga_id}`")
    job_id = int(datetime.now().strftime("%Y%m%d"))
    params = scraper.get_params(manga_id)
    all_result = []
    for scr in params.get("scraper"):
        scraper_func = scraper.get_scraper(scr)

        logging.info(f"Extract manga `{manga_id}` in `{scr.get('name')}`")
        result = scraper_func(url=scr.get("url"))
        result = {
            "manga_id": manga_id,
            "manga_label": params.get("name"),
            "website": scr.get("name"),
            **result
        }
        all_result.append(result)

    filename = f"tmp/{manga_id}_{datetime.now():%Y%m%d}.csv"
    utils.export_to_csv(filename=filename, data=all_result)
    logging.info(f"Result exported to {filename}")

    return job_id


def start_loading(job_id: int):
    logging.info("Start loading data to database")
    result_list = os.listdir(f"tmp")
    for result_file in result_list:
        filepath = os.path.join("tmp", result_file)

        logging.info(f"Loading `{filepath}`")
        utils.csv_to_postgres(filepath, job_id)


if __name__ == "__main__":
    logging.basicConfig(
        level   = logging.INFO,
        format  = "[%(asctime)s] %(levelname)s - %(message)s",
        datefmt = "%Y/%m/%d %H:%M:%S"
    )

    (_, *manga_list) = sys.argv
    for manga in manga_list:
        job_id = start_scraping(manga)
        start_loading(job_id)