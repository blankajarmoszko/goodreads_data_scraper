import pandas as pd

class BookDataProcessor:
    def __init__(self, *book_data_frames):
        """
        Initializes the BookDataProcessor with one or more DataFrames.

        Args:
        *book_data_frames (DataFrame): One or more DataFrames containing book data.
        """
        self.book_data_frames = book_data_frames

    def process_data(self, output_file='book_data.csv'):
        """
        Processes the book data, normalizes nested JSON columns, and saves the result to a CSV file.

        Args:
        output_file (str): The name of the output CSV file. Default is 'book_data.csv'.

        Returns:
        None
        """
        # Concatenate book data from multiple DataFrames
        book_data = pd.concat(self.book_data_frames, axis=0, ignore_index=True)

        # Normalize the 'book_details' column which contains nested JSON
        normalized_details = pd.json_normalize(book_data['book_details'])

        # Concatenate the normalized DataFrame with the original DataFrame
        result = pd.concat([book_data, normalized_details], axis=1)

        # Drop the original nested JSON column
        result = result.drop(['book_details'], axis=1)

        # Save the processed data to a CSV file
        result.to_csv(output_file, index=False)


class ReviewDataProcessor:
    def __init__(self, *review_data_frames):
        """
        Initializes the ReviewDataProcessor with one or more DataFrames.

        Args:
        *review_data_frames (DataFrame): One or more DataFrames containing review data.
        """
        self.review_data_frames = review_data_frames

    def process_data(self, output_file='review_data_new.csv'):
        """
        Processes the review data, normalizes nested JSON columns, and saves the result to a CSV file.

        Args:
        output_file (str): The name of the output CSV file. Default is 'review_data_new.csv'.

        Returns:
        None
        """
        # Concatenate review data from multiple DataFrames
        review_data = pd.concat(self.review_data_frames, axis=0, ignore_index=True)

        # Normalize the 'reviewer_info' and 'review_info' columns which contain nested JSON
        normalized_reviewer = pd.json_normalize(review_data['reviewer_info'])
        normalized_review = pd.json_normalize(review_data['review_info'])

        # Concatenate the normalized DataFrames with the original DataFrame
        result = pd.concat([review_data, normalized_reviewer, normalized_review], axis=1)

        # Drop the original nested JSON columns
        result = result.drop(['reviewer_info', 'review_info'], axis=1)

        # Save the processed data to a CSV file
        result.to_csv(output_file, index=False)


if __name__ == "__main__":
    # Example usage for book data processing
    book_processor = BookDataProcessor(
        pd.read_json("data/example_book_data.json")
    )
    book_processor.process_data('data/book_data.csv')

    # Example usage for review data processing
    review_processor = ReviewDataProcessor(
        pd.read_json("data/eexample_review_data.json"),
    )
    review_processor.process_data('data/review_data.csv')


