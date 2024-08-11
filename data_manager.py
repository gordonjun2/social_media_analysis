import time
from datetime import datetime
import pandas as pd
from urllib.request import urlopen
import json
from bs4 import BeautifulSoup
from urllib.error import HTTPError
import requests
from PIL import Image
import re
import random
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
import os
import openai
import spacy
from collections import Counter
import warnings
import pickle
import sys
import re
import unicodedata

pd.set_option('display.max_rows', None)
warnings.filterwarnings("ignore")


def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


def get_boards_info():
    url = "https://a.4cdn.org/boards.json"
    data = get_jsonparsed_data(url)

    return data


def save_df(dataframe, dir_path, start_datetime, end_datetime):
    """
    Save 4chan's posts dataframe.
    """

    cached_file_path = '{}/{}_{}.pkl'.format(dir_path, start_datetime,
                                             end_datetime)

    os.makedirs(dir_path, exist_ok=True)
    with open(cached_file_path, 'wb') as file:
        pickle.dump(dataframe, file)


def load_df(file_path):
    """
    Load 4chan's posts dataframe.
    """

    with open(file_path, 'rb') as file:
        dataframe = pickle.load(file)

    return dataframe


def load_df_range(source, board, start_date, end_date):
    """
    Load dataframe that is within the specified date range.
    """

    if source not in ['4chan', 'hugging_face']:
        print("Invalid source. Please enter '4chan' or 'hugging_face'.")

        return None
    elif source == '4chan':
        dir_path = './saved_data/4chan/{}'.format(board)
        merged_df = pd.DataFrame(columns=[
            'Date Time', 'Name', 'ID', 'Thread Subject', 'Comment',
            'Thread Post Number', 'Post Number', 'Thread Replies',
            'Is Thread OP'
        ])
    else:
        dir_path = './saved_data/hugging_face'
        merged_df = pd.DataFrame(columns=['Date Time', 'Comment'])

    date_format = '%Y-%m-%d'
    datetime_format = '%Y-%m-%d %H:%M:%S'

    parsed_input_start_datetime = datetime.strptime(start_date, date_format)
    parsed_input_end_datetime = datetime.strptime(
        end_date, date_format).replace(hour=23, minute=59, second=59)

    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        if files:
            for file in files:
                if not file.endswith('.pkl'):
                    continue

                file_start_datetime, file_end_datetime = file.replace(
                    '.pkl', '').split('_')
                parsed_file_start_datetime = datetime.strptime(
                    file_start_datetime, datetime_format)
                parsed_file_end_datetime = datetime.strptime(
                    file_end_datetime, datetime_format)

                if check_datetime_overlap(parsed_input_start_datetime,
                                          parsed_input_end_datetime,
                                          parsed_file_start_datetime,
                                          parsed_file_end_datetime):
                    file_path = dir_path + '/' + file
                    try:
                        df = load_df(file_path)
                    except:
                        print('\nUnable to load the file at {}. Skipping...'.
                              format(file_path))
                        continue

                    if df is None:
                        print("\nNo data found in {}. Skipping...".format(
                            file_path))
                        continue
                else:
                    continue

                merged_df = pd.concat([merged_df, df],
                                      axis=0,
                                      ignore_index=True)

            if source == '4chan':
                merged_df = merged_df.drop_duplicates(
                    subset='Post Number'
                )  # Drop rows with duplicated 'Post Number'

            merged_df = merged_df[
                (merged_df['Date Time'] >= parsed_input_start_datetime)
                & (merged_df['Date Time'] <= parsed_input_end_datetime)]
            merged_df = merged_df.sort_values(
                by='Date Time', ascending=True).reset_index(drop=True)

            return merged_df

        else:
            print(
                "\nNo files found in the selected directory {}. Please run 'data_manager.py' or 'download_hugging_face_data.py' to generate the data."
                .format(dir_path))

            return None
    else:
        print(
            "\nNo files found in the selected directory {}. Please run 'data_manager.py' or 'download_hugging_face_data.py' to generate the data."
            .format(dir_path))

        return None


def clean_text(text):

    # 1. Parse using BeautifulSoup to remove HTML tags
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.get_text()

    # 2. Remove Chinese, Japanese, and Korean characters
    text = re.sub(
        r'[\u4e00-\u9fff\u3400-\u4dbf\u3040-\u30ff\u31f0-\u31ff\uac00-\ud7af]+',
        '', text)

    # 3. Remove crypto wallet addresses (assuming alphanumeric and special characters)
    text = re.sub(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', '',
                  text)  # Example for Bitcoin-like addresses
    text = re.sub(r'\b0x[a-fA-F0-9]{40}\b', '',
                  text)  # Example for Ethereum-like addresses
    text = re.sub(r'\b[A-HJ-NP-Za-km-z1-9]{32,44}\b', '',
                  text)  # Example for Solana-like addresses

    # 4. Remove URLs
    text = re.sub(r'http\S+|www\S+', '', text)

    # 5. Remove cashtags ($), hashtags (#), usernames (@), and retweets (RT)
    text = re.sub(r'\$\w+', '', text)  # Remove cashtags
    text = re.sub(r'#\w+', '', text)  # Remove hashtags
    text = re.sub(r'@\w+', '', text)  # Remove usernames
    text = re.sub(r'\bRT\b', '', text)  # Remove retweet indicator

    # 6. Remove 4chan reply indicator (e.g., '>>123456789')
    text = re.sub(r'&gt;&gt;\d+', "", text)
    text = re.sub(r'>>\d+', "", text)

    # 7. Fix known special character encoding errors (e.g., ampersand, apostrophe)
    text = re.sub('&#039;', "'", text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&lt;', '<', text)
    text = text.replace('&amp;', '&').replace('&quot;',
                                              '"').replace('&apos;', "'")

    # 8. Replace multiple dots with triple dots
    text = re.sub(r'\.{2,}', '...', text)

    # 9. Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)

    # 10. Convert to lowercase (BERT models are case-sensitive)
    text = text.lower()

    # 11. Normalize text (fix any remaining encoding issues)
    text = unicodedata.normalize('NFKD', text)

    # 12. Remove posts containing less than four words
    if len(text.split()) < 3:
        return ''

    # 13. Final trimming of any leading/trailing spaces
    return text.strip()


def check_datetime_overlap(input_start_datetime, input_end_datetime,
                           file_start_datetime, file_end_datetime):

    if input_start_datetime <= file_end_datetime and input_end_datetime >= file_start_datetime:
        return True

    return False


def delete_files(file_list):
    for file_path in file_list:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print("Deleted: {}".format(file_path))
            else:
                print("File to delete not found: {}".format(file_path))
        except Exception as e:
            print("Error deleting {}: {}".format(file_path, e))

    print("\n")


if __name__ == "__main__":

    boards_info = get_boards_info()

    board_names = []
    board_titles = []
    combined = []
    pages = []

    for board in boards_info['boards']:
        name = board['board']
        title = board['title']
        page = board['pages']
        board_names.append(name)
        board_titles.append(title)
        pages.append(page)

    board_df = pd.DataFrame({
        'Name': board_names,
        'Title': board_titles,
        'Max Pages': pages
    })

    print("\n4chan Boards:\n")
    print(board_df)
    print("\n")
    user_input = input("Enter the board name to scrape: ")
    board = user_input.strip().lower()
    print("You entered: ", board)
    print("\n")

    if board not in board_names:
        print(
            "Invalid board name entered. Please enter a valid board name from the list above.\n"
        )
        sys.exit(1)

    dir_path = './saved_data/4chan/{}'.format(board)
    dataframe = pd.DataFrame(columns=[
        'Date Time', 'Name', 'ID', 'Thread Subject', 'Comment',
        'Thread Post Number', 'Post Number', 'Thread Replies', 'Is Thread OP'
    ])

    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        if files:
            expected_columns = set(dataframe.columns)
            files_to_delete = []

            for file in files:
                if not file.endswith('.pkl'):
                    continue

                file_path = dir_path + '/' + file
                try:
                    df = load_df(file_path)
                except:
                    continue

                if df is None:
                    continue

                if set(df.columns) == expected_columns:
                    dataframe = pd.concat([dataframe, df],
                                          axis=0,
                                          ignore_index=True)

                files_to_delete.append(file_path)

    max_pages = board_df.loc[board_df['Name'] == board, 'Max Pages'].values[0]

    for i in range(1, max_pages + 1):
        board_page_url = "https://a.4cdn.org/" + board + "/" + str(i) + '.json'
        print("Retrieving data from {}...".format(board_page_url))
        board_page_data = get_jsonparsed_data(board_page_url)

        time.sleep(
            1.5)  # API Rules: Do not make more than one request per second.

        for thread in board_page_data['threads']:
            poster_id = thread['posts'][0].get('id', '')

            if poster_id == 'Mod':
                continue

            thread_post_no = thread['posts'][0].get('no', -1)
            replies = thread['posts'][0].get('replies', 0)
            subject = thread['posts'][0].get('sub', 'No Subject')

            thread_url = "https://a.4cdn.org/" + board + "/thread/" + str(
                thread_post_no) + '.json'
            print("Retrieving data from {}...".format(thread_url))
            thread_data = get_jsonparsed_data(thread_url)

            for post in thread_data['posts']:
                post_no = post.get('no', -1)
                comment = post.get('com', '')
                name = post.get('name', '')
                poster_id = post.get('id', '')
                timestamp = post.get('time', 0)
                date_time = datetime.fromtimestamp(timestamp)

                if post_no == thread_post_no:
                    is_thread_op = 'Yes'
                else:
                    is_thread_op = 'No'

                new_row = pd.DataFrame([{
                    'Date Time': date_time,
                    'Name': name,
                    'ID': poster_id,
                    'Thread Subject': subject,
                    'Comment': comment,
                    'Thread Post Number': thread_post_no,
                    'Post Number': post_no,
                    'Thread Replies': replies,
                    'Is Thread OP': is_thread_op
                }])
                dataframe = pd.concat([dataframe, new_row],
                                      axis=0,
                                      ignore_index=True)

            time.sleep(
                1.5
            )  # API Rules: Do not make more than one request per second.

        print("\n")

    # Clean text and sort by date time
    dataframe['Comment'] = dataframe['Comment'].apply(clean_text)
    dataframe = dataframe[dataframe['Comment'] != '']
    dataframe = dataframe.drop_duplicates(
        subset='Post Number')  # Drop rows with duplicated 'Post Number'
    dataframe = dataframe.sort_values(by='Date Time',
                                      ascending=True).reset_index(drop=True)
    start_datetime = dataframe.iloc[0]['Date Time']
    end_datetime = dataframe.iloc[-1]['Date Time']

    print("First 10 retrieved data from {} to {}: ".format(
        start_datetime, end_datetime))
    print(dataframe.head(10))

    print("\n")

    save_df(dataframe, dir_path, start_datetime, end_datetime)
    delete_files(files_to_delete)

    print(
        "Data downloaded successfully. Please use crypto-sentiment-on-chart.ipynb or 4chan-summariser.ipynb next.\n"
    )
