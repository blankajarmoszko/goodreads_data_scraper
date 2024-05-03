import pandas as pd

def process_book_data(book_data_1, book_data_2, book_data_3):
    book_data = pd.concat([book_data_1, book_data_2, book_data_3], axis=0, ignore_index=True)
    normalized_details = pd.json_normalize(book_data['book_details'])
    # Concatenate the normalized DataFrame with the original DataFrame
    result = pd.concat([book_data, normalized_details], axis=1)
    # Drop the original dictionary column
    result = result.drop(['book_details'], axis=1)
    result.to_csv('book_data.csv', index=False)


def process_review_data(rd1, rd2, rd3, rd4, rd5, rd6):

    review_data = pd.concat([rd1, rd2, rd3, rd4, rd5, rd6], axis=0, ignore_index=True)
    normalized_reviewer = pd.json_normalize(review_data['reviewer_info'])
    normalized_review = pd.json_normalize(review_data['review_info'])

    # Concatenate the normalized DataFrame with the original DataFrame
    result = pd.concat([review_data, normalized_reviewer,normalized_review], axis=1)

    # Drop the original dictionary column
    result = result.drop(['reviewer_info', 'review_info'], axis=1)
    result.to_csv('review_data_new.csv', index=False)


process_book_data(pd.read_json("book_data_1.json"), pd.read_json("book_data_2.json"),pd.read_json('book_data_missing.json'))
#process_review_data(pd.read_json("review_data_1.json"),
                    # pd.read_json("review_data_2.json"),
                    # pd.read_json("review_data_2022.json"),
                    # pd.read_json("review_data_2021.json"),
                    # pd.read_json("review_data_2020.json"),
                    # pd.read_json("review_data_2019.json")
                    #                     )
