import requests
from bs4 import BeautifulSoup
import sqlite3
import time
from datetime import datetime

# Initialize the database
def init_db():
    conn = sqlite3.connect('tech_news.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT,
            points INTEGER,
            posted_time TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Scrape Hacker News
def scrape_hn():
    url = "https://news.ycombinator.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stories = []
        rows = soup.select('tr.athing')
        
        for row in rows[:30]:  # Get top 30 stories
            title_elem = row.select_one('.titleline a')
            title = title_elem.text
            url = title_elem['href']
            
            # Get points and time from next row
            next_row = row.find_next_sibling('tr')
            points = next_row.select_one('.score')
            points = int(points.text.split()[0]) if points else 0
            
            time_posted = next_row.select_one('.age')['title']
            
            stories.append({
                'title': title,
                'url': url,
                'points': points,
                'posted_time': time_posted
            })
        
        return stories
    
    except Exception as e:
        print(f"Error scraping: {e}")
        return []

# Save stories to database
def save_to_db(stories):
    conn = sqlite3.connect('tech_news.db')
    cursor = conn.cursor()
    
    for story in stories:
        # Check if story already exists
        cursor.execute('''
            SELECT 1 FROM news WHERE title = ? AND posted_time = ?
        ''', (story['title'], story['posted_time']))
        
        if not cursor.fetchone():  # Only insert new stories
            cursor.execute('''
                INSERT INTO news (title, url, points, posted_time)
                VALUES (?, ?, ?, ?)
            ''', (story['title'], story['url'], story['points'], story['posted_time']))
    
    conn.commit()
    print(f"Saved {len(stories)} new stories at {datetime.now()}")
    conn.close()

# Main function
def main():
    init_db()
    
    while True:
        print("Starting scrape...")
        stories = scrape_hn()
        if stories:
            save_to_db(stories)
        
        # Wait 10 minutes before next scrape
        time.sleep(600)

if __name__ == "__main__":
    main()
