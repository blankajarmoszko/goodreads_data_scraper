import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def extract_book_ids(url):
    try:
        # Fetch the HTML content from the provided URL and parse it with BeautifulSoup
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        # Find all <a> tags with class 'pollAnswer__bookLink' within the 'gcaRightContainer' class
        book_links = soup.select('.gcaRightContainer a.pollAnswer__bookLink')

        # Extract and return the part of the link after the last / and before any ?
        return [urlparse(link['href']).path.split('/')[-1].split('?')[0] for link in book_links]
    except Exception as e:
        print(f"Error: {e}")
        return []
# Example usage:

webpage_list = ["https://www.goodreads.com/choiceawards/best-fiction-books-2019",
                "https://www.goodreads.com/choiceawards/best-mystery-thriller-books-2019",
                "https://www.goodreads.com/choiceawards/best-historical-fiction-books-2019",
                "https://www.goodreads.com/choiceawards/best-fantasy-books-2019",
                "https://www.goodreads.com/choiceawards/best-romance-books-2019",
                "https://www.goodreads.com/choiceawards/best-science-fiction-books-2019",
                "https://www.goodreads.com/choiceawards/best-horror-books-2019",
                "https://www.goodreads.com/choiceawards/best-humor-books-2019",
                "https://www.goodreads.com/choiceawards/best-nonfiction-books-2019",
                "https://www.goodreads.com/choiceawards/best-memoir-autobiography-books-2019",
                "https://www.goodreads.com/choiceawards/best-history-biography-books-2019",
                "https://www.goodreads.com/choiceawards/best-science-technology-books-2019",
                "https://www.goodreads.com/choiceawards/best-food-cookbooks-2019",
                "https://www.goodreads.com/choiceawards/best-graphic-novels-comics-2019",
                "https://www.goodreads.com/choiceawards/best-poetry-books-2019",
                "https://www.goodreads.com/choiceawards/best-debut-novel-2019",
                "https://www.goodreads.com/choiceawards/best-young-adult-fiction-books-2019",
                "https://www.goodreads.com/choiceawards/best-young-adult-fantasy-books-2019",
                "https://www.goodreads.com/choiceawards/best-childrens-books-2019",
                "https://www.goodreads.com/choiceawards/best-picture-books-2019"
                ]

def save_to_textfile(unique_urls, filename):
    with open(filename, 'a') as file:
        for url in unique_urls:
            file.write(url + '\n')


# Set to store unique URLs
unique_urls = set()
output_filename = "booklist_2019.txt"
for url in webpage_list:
    webpage_url = url
    book_urls = extract_book_ids(webpage_url)

    if book_urls:
        for book_id in book_urls:
            if book_id not in unique_urls:
                unique_urls.add(book_id)
                print(book_id)

# Save unique URLs to text file
save_to_textfile(unique_urls, output_filename)
