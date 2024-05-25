import requests
from bs4 import BeautifulSoup
import json
import argparse

class BookScraper:
    def __init__(self, base_url='https://www.goodreads.com/book/show/'):
        self.base_url = base_url
        self.url_list = []

    def generate_full_url(self, book_id):
        """Generate the full URL for a given book ID."""
        return f'{self.base_url}{book_id}'

    def read_book_ids(self, file_path):
        """Read book IDs from a text file and return a list of full URLs."""
        with open(file_path, 'r') as file:
            for line in file:
                book_id = line.strip()
                full_url = self.generate_full_url(book_id)
                self.url_list.append(full_url)

    def scrape_book(self, url):
        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        author_names = self.extract_author_names(soup)
        average_rating = float(soup.find('div', class_='RatingStatistics__rating').text.strip())
        ratings_count = float(self.extract_count(soup, 'ratingsCount').replace(",", ""))
        reviews_count = float(self.extract_count(soup, 'reviewsCount').replace(",", "").replace("reviews", ""))

        book = {
            "title": soup.find("h1", {"class": "Text Text__title1", "data-testid": "bookTitle"}).text,
            "author": author_names,
            "description": soup.find("span", {"class": "Formatted"}).text,
            "series_details": self.get_series(soup),
            "book_details": self.extract_book_details(soup),
            "genres": self.get_genres(soup),
            "avg_rating": average_rating,
            "num_ratings": ratings_count,
            "num_reviews": reviews_count
        }

        return book

    def extract_author_names(self, soup):
        author_elements = soup.find_all('span', class_='ContributorLink__name')
        author_list = [author.text for author in author_elements]
        return list(set(author_list))

    def extract_count(self, soup, data_testid):
        count_span = soup.find('span', {'data-testid': data_testid})
        return count_span.text.strip().replace('ratings', '').replace('\xa0', '')

    def extract_book_details(self, soup):
        book_details = soup.find('div', class_='BookDetails')
        if book_details:
            featured_details = book_details.find('div', class_='FeaturedDetails')
            pages_format = featured_details.find('p', {'data-testid': 'pagesFormat'}).text.strip()
            publication_info = featured_details.find('p', {'data-testid': 'publicationInfo'}).text.strip()
            return {'pages_format': pages_format, 'publication_info': publication_info}
        return None

    def get_series(self, soup):
        h3_element = soup.find('h3', class_='Text Text__title3 Text__italic Text__regular Text__subdued')
        return h3_element['aria-label'] if h3_element else None

    def get_genres(self, soup):
        return [a.text for a in soup.select('a[href*="/genres/"]')]

    def get_all_books(self, output_file):
        books = []
        for url in self.url_list:
            book = self.scrape_book(url)
            books.append(book)

        with open(output_file, 'w') as json_file:
            json.dump(books, json_file, indent=2)


if __name__ == "__main__":
    # file_path = 'example_booklist.txt'
    # output_file = 'data/example_book_data.json'
    # book_scraper = BookScraper()
    # book_scraper.read_book_ids(file_path)
    # book_scraper.get_all_books(output_file)
    parser = argparse.ArgumentParser(description='Scrape Goodreads book data.')
    parser.add_argument('input_file', type=str, help='Path to the input text file with book IDs')
    parser.add_argument('output_file', type=str, help='Path to the output JSON file to save book data')
    args = parser.parse_args()
    book_scraper = BookScraper()
    book_scraper.read_book_ids(args.input_file)
    book_scraper.get_all_books(args.output_file)
