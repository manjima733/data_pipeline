#  Hacker News Scraper & SQLite Pipeline

A Python-based data pipeline that scrapes the top stories from [Hacker News](https://news.ycombinator.com/), extracts metadata like title, URL, points, and posting time, and stores the results in a local SQLite database (`tech_news.db`). The pipeline runs every 10 minutes and avoids duplicate entries.

---

## Features

- Scrapes top 30 stories from Hacker News
- Extracts title, link, score (points), and timestamp
- Stores data in a local SQLite database
-  Avoids duplicate entries
-  Automatically runs every 10 minutes



