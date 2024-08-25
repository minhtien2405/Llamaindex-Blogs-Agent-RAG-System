import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

def crawl_website(url):
    """Crawl a single blog post URL and extract its content."""
    # Set up headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', class_='BlogPost_htmlPost__Z5oDL')
        
        if not content:
            raise Exception("Blog post content not found.")
        
        all_tags = content.find_all()
        tags_to_extract = ['h1', 'h2', 'h3', 'p', 'li', 'code', 'blockquote', 'em']
        text = ""

        # Extract the content from the tags
        for tag in all_tags:
            if tag.name in tags_to_extract:
                if tag.name == 'h1':
                    text += f"\n\nSection: {tag.text.strip()}:\n"
                elif tag.name == 'h2':
                    text += f"\n\nSubsection: {tag.text.strip()}:\n"
                elif tag.name == 'h3':
                    text += f"\n\nSubSubsection: {tag.text.strip()}:\n"
                elif tag.name == 'li':
                    text += f"- {tag.text.strip()}\n"
                elif tag.name == 'code':
                    text += f"\n{tag.text.strip()}\n"
                else:
                    text += tag.text.strip() + "\n"
        
        return text

    except requests.RequestException as e:
        raise Exception(f"An error occurred while fetching the URL {url}: {e}")

# Set the output directory for saving files
output_dir = 'data'
os.makedirs(output_dir, exist_ok=True)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

try:
    r = requests.get('https://www.llamaindex.ai/blog', headers=headers, timeout=10)
    r.raise_for_status()  # Raise an exception for bad status codes

    # Print status code
    print(f"Status Code: {r.status_code}")

    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')

    # Print the title of the page
    print(f"Page Title: {soup.title.string if soup.title else 'No title found'}")

except requests.RequestException as e:
    print(f"An error occurred: {e}")
    exit(1)

# Find all blog cards
blog_cards = soup.find_all('div', class_='CardBlog_card__mm0Zw')
base_url = "https://www.llamaindex.ai"

# Prepare to save data
with open(os.path.join(output_dir, 'llama_blog.txt'), 'w', encoding="utf-8") as f:
    for card in blog_cards:
        title_element = card.find('p', class_='CardBlog_title__qC51U').find('a')
        title = title_element.text.strip()
        url = base_url + title_element['href']
        date = card.find('p', class_='Text_text__zPO0D Text_text-size-16__PkjFu').text.strip()
        f.write(f"Title: {title}\n")
        f.write(f"Date: {date}\n")
        f.write(f"URL: {url}\n")
        f.write("---\n")

print("Data saved to llama_blog.txt")

# Create a DataFrame to store blog information
df = pd.DataFrame(columns=['source', 'title', 'url', 'date', 'content'])

for card in blog_cards:
    title_element = card.find('p', class_='CardBlog_title__qC51U').find('a')
    title = title_element.text.strip()
    source = title_element['href']
    url = base_url + title_element['href']
    date = card.find('p', class_='Text_text__zPO0D Text_text-size-16__PkjFu').text.strip()

    # Append data to DataFrame
    df.loc[len(df)] = [source, title, url, date, '']

# Save the initial DataFrame to CSV
df.to_csv(os.path.join(output_dir, 'llama_blog.csv'), index=False)
print("Data saved to llama_blog.csv")

# Extract the content of all blog posts
for index in tqdm(df.index, desc="Crawling blog posts"):
    url = df['url'][index]
    df.at[index, 'content'] = crawl_website(url)

# Save the updated DataFrame to CSV
df.to_csv(os.path.join(output_dir, 'llama_blog.csv'), index=False)
print(f"Successfully saved {len(df)} blog posts to llama_blog.csv")
