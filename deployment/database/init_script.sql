DROP TABLE IF EXISTS scraper_cdc;
CREATE TABLE IF NOT EXISTS scraper_cdc (
  manga_id VARCHAR,
  manga_label VARCHAR,
  website VARCHAR,
  latest_dt DATE,
  latest_tm TIMESTAMP,
  latest_chp VARCHAR,
  latest_url VARCHAR,
  load_tm TIMESTAMP
);

DROP TABLE IF EXISTS manga;
CREATE TABLE IF NOT EXISTS manga (
  manga_id VARCHAR,
  manga_label VARCHAR,
  website VARCHAR,
  latest_dt DATE,
  latest_tm TIMESTAMP,
  latest_chp VARCHAR,
  latest_url VARCHAR,
  load_tm TIMESTAMP
);