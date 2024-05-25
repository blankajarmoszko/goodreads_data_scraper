
# Goodreads Data Scraper

## Table of Contents

- [About](#about)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)
- [Contributing](#contributing)
- [Contact](#contact)

## About

This project is a Goodreads data scraper designed to scrape book information and up to 30 reviews per given title. It was developed as a helper tool for my machine learning thesis to gather Goodreads book and review data. The project uses BeautifulSoup (bs4) to extract the necessary information.

## Features

- Scrape detailed book information from Goodreads.
- Scrape up to 30 reviews for each book title.
- Process JSON data into CSV format for analysis.
- Includes helper tools for efficient link gathering.

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/blankajarmoszko/goodreads_data_scraper
   ```
2. Navigate to the project directory:
   ```sh
   cd goodreads-data-scraper
   ```
3. Install the required dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Usage

1. Prepare a text file with a list of book titles (one title per line). See `example_booklist.txt` for formatting.
2. To scrape book information:
   ```sh
   python main.py <path_to_booklist_txt> <path_to_book_data_json>
   ```
   This command will generate a JSON file with the book data.

3. To scrape reviews:
   ```sh
   python review_data.py <path_to_booklist_txt> <path_to_review_data_json>
   ```
   This command will generate a JSON file with the top 30 reviews for each book.

4. To process the JSON data into CSV format:
   ```sh
   python data_processing.py <path_to_book_json_file> <path_to_text_file>
   ```
   Replace <path_to_book_json_file> with the path to your JSON file containing book data and <path_to_text_file> with the path to your text file containing book IDs.

   Example usage:
   python data_processing.py data/example_book_data.json example_booklist.txt


## Files

- `data_processing.py`: Processes JSON data into CSV format.
- `example_booklist.txt`: Example file showing how the input file should be formatted.
- `get_links.py`: Helper tool for retrieving multiple book links faster from Goodreads Choice Award websites.
- `main.py`: Scrapes book information for given book titles and returns a JSON file.
- `review_data.py`: Scrapes the top 30 reviews for each book title and returns a JSON file.


The `data` folder is used to store JSON and CSV files generated during data processing. You can save your book data JSON files, review data JSON files, and processed CSV files in this folder for easy organization and access.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Make sure your code follows the project's coding style and passes all tests.


## Contact

Project maintained by [Blanka Jarmoszko](https://github.com/blankajarmoszko).  
Feel free to reach out via email at jarmoszkoblanka@gmail.com.

---

 
