import requests
from bs4 import BeautifulSoup
import json
import re

class ReviewScraper:
    """
    ReviewScraper class takes in a base url. The overall methods in this class return reviews for each of the given books.
    """
    def __init__(self, base_url):
        self.base_url = base_url

    def extract_reviewer_info(self, review_card):
        """
        This function takes in a html of a review card and extracts relevant information about the reviewer.
        It takes into account both regular reviewers and authors who have a different layout of their review cards.
        :param review_card: html of a singular review card
        :return:
        - 'reviewer_name': name of the reviewer as appears on the website
        - 'num_reviews': total number of reviews ever published by the reviewer or None if reviewer is an Author
        - 'num_followers': total number of followers the reviewer has
        - 'num_books': number of distinct works published by the reviewer, only applies when the reviewer is an Author
        else it returns None.
        """
        try:
            # Extract reviewer meta div
            reviewer_meta_div = review_card.find('div', class_='ReviewerProfile__meta')
            reviewer_name_div = review_card.find('div', {'data-testid': 'name', 'class': 'ReviewerProfile__name'})
            reviewer_name = reviewer_name_div.a.text if reviewer_name_div else None

            if reviewer_meta_div:
                author_span = reviewer_meta_div.find('span', class_='ReviewerProfile__author')
                profile_author = author_span.get_text(strip=True) if author_span else None
                # if reviewer is an author
                if profile_author:
                    span_with_books = reviewer_meta_div.find('span', string=re.compile(r'\d+ books'))
                    span_with_followers = reviewer_meta_div.find('span', string=re.compile(r'\d+k followers'))

                    num_books = span_with_books.text.strip().split()[0] if span_with_books else None
                    num_followers = span_with_followers.text.strip().split()[0] if span_with_followers else None
                    return {
                        'reviewer_name': reviewer_name,
                        'num_books': num_books,
                        'num_followers': num_followers,
                        'num_reviews': None  # No reviews found in this case
                    }
                # reviewer is not an author
                else:
                    reviews_span = reviewer_meta_div.find('span', string=lambda text: 'reviews' in text)
                    num_reviews = reviews_span.get_text(strip=True) if reviews_span else "Number of Reviews Not Found"
                    followers_span = reviewer_meta_div.find('span', string=lambda text: 'followers' in text)
                    num_followers = followers_span.get_text(strip=True).split()[0] if followers_span else None
                    return {
                        'reviewer_name': reviewer_name,
                        'num_reviews': num_reviews,
                        'num_followers': num_followers,
                        'num_books': None
                    }
            else:
                return None

        except Exception as e:
            print(f"Error extracting reviewer information: {e}")
            return None
    def extract_review_info_from_card(self, review_card):
        """
        Function takes in html representing a singular review card and extracts review information for the card.
        :param review_card: html of a singualr review
        :return: 'star_rating': first_number,
                'review_text': review_text,
                'num_likes': num_likes,
                'num_comments': num_comments
        """
        try:
            # get star rating information from reviewer's profile
            rating_span = review_card.find('span', {'aria-label': True})
            additional_rating_info = rating_span['aria-label'] if rating_span else ''
            first_number = re.search(r'\b(\d+)\b', additional_rating_info).group(1) if re.search(r'\b(\d+)\b', additional_rating_info) else None

            # get review text
            review_text_section = review_card.find('section', class_='ReviewText__content')
            review_text = review_text_section.find('span', class_='Formatted').text.strip()

            # get statistics about the review: number of likes and comments
            stats_container_div = review_card.find('div', class_='SocialFooter__statsContainer')
            likes_button = stats_container_div.find('button', string=lambda text: 'likes' in text)
            comments_button = stats_container_div.find('button', string=lambda text: 'comments' in text)

            # convert num of like and comments to floats from strings
            num_likes = likes_button.text.split()[0] if likes_button else 0
            num_comments = comments_button.text.split()[0] if comments_button else 0

            # return results for each review
            return {
                'star_rating': first_number,
                'review_text': review_text,
                'num_likes': num_likes,
                'num_comments': num_comments
            }
        except Exception as e:
            print(f"Error extracting review information from card: {e}")
            return None

    def scrape_reviews(self, url_list, output_file):
        """Iterate through all URLs and scrape reviews for each book."""
        books = []  # Create a list to store book dictionaries

        for url in url_list:
            soup = BeautifulSoup(requests.get(url).content, "html.parser")
            review_cards = soup.find_all('article', class_='ReviewCard')

            for card in review_cards:
                book = {
                    "title": soup.find("h1", {"class": "Text Text__title1", "data-testid": "bookTitle"}).text,
                    "reviewer_info": self.extract_reviewer_info(card),
                    "review_info": self.extract_review_info_from_card(card)
                }
                books.append(book)  # Append the book dictionary to the list

        # Save the list of books to a JSON file
        with open(output_file, 'w') as json_file:
            json.dump(books, json_file, indent=2)

    def generate_full_url(self, book_id):
        """Generate the full URL for a given book ID."""
        return f'{self.base_url}{book_id}'

    def read_book_ids(self, file_path):
        """Read book IDs from a text file and return a list of full URLs."""
        url_list = []
        with open(file_path, 'r') as file:
            for line in file:
                book_id = line.strip()
                full_url = self.generate_full_url(book_id)
                url_list.append(full_url)
        return url_list

if __name__ == "__main__":
    base_url = 'https://www.goodreads.com/book/show/'
    file_path = 'example_booklist.txt'
    scraper = ReviewScraper(base_url)
    url_list = scraper.read_book_ids(file_path)
    scraper.scrape_reviews(url_list, 'data/example_review_data.json')

