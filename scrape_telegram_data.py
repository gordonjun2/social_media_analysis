from pyrogram import Client
import pandas as pd
import os
from datetime import datetime
import warnings
from data_manager import save_df, load_df, delete_files, clean_text
from config import TELEGRAM_API_KEY, TELEGRAM_HASH, CHAT_ID_LIST

warnings.filterwarnings("ignore")


def update_save_dataframe(dataframe, new_batch_dataframe, dir_path,
                          chat_title):

    dataframe = pd.concat([dataframe, new_batch_dataframe],
                          axis=0,
                          ignore_index=True)

    dataframe['Comment'] = dataframe['Comment'].apply(clean_text)
    dataframe = dataframe[dataframe['Comment'] != '']
    dataframe = dataframe.drop_duplicates(subset='Comment UUID')
    dataframe = dataframe.sort_values(by='Date Time',
                                      ascending=True).reset_index(drop=True)
    start_datetime = dataframe.iloc[0]['Date Time']
    end_datetime = dataframe.iloc[-1]['Date Time']

    files_to_delete = []
    if os.path.exists(dir_path):
        files = os.listdir(dir_path)
        if files:
            for file in files:
                if not file.endswith('.pkl'):
                    continue

                file_path = dir_path + '/' + file
                files_to_delete.append(file_path)

    delete_files(files_to_delete)
    save_df(dataframe, dir_path, start_datetime, end_datetime)
    print("Saved {}'s chat data from {} - {}".format(chat_title,
                                                     start_datetime,
                                                     end_datetime))
    print("\n")
    files_to_delete = []

    last_10_comment_uuids_dict = {
        uuid: True
        for uuid in dataframe['Comment UUID'].tail(10)
    }

    return dataframe, last_10_comment_uuids_dict


CONFIG = {
    "telegram_api_id": TELEGRAM_API_KEY,
    "telegram_hash": TELEGRAM_HASH,
}

app = Client("text_scraper",
             CONFIG["telegram_api_id"],
             CONFIG["telegram_hash"],
             takeout=True,
             sleep_threshold=10)


async def main(chat_id_list):
    async with app:
        for chat_id in chat_id_list:
            try:
                chat_info = await app.get_chat(chat_id)
            except Exception as e:
                print(
                    "\nUnable to scraping chat data from {} ({}) due to {}...\n"
                    .format(chat_title, chat_id, e))
                continue
            chat_title = chat_info.title

            print("\nScraping chat data from: {} ({})...\n".format(
                chat_title, chat_id))

            dir_path = './saved_data/telegram/{}'.format(
                str(chat_id) + '-' + chat_title)
            files_to_delete = []
            datetime_format = '%Y-%m-%d %H:%M:%S'
            dataframe = pd.DataFrame(columns=[
                'Date Time', 'Comment UUID', 'Chat ID', 'Chat Title',
                'User ID', 'Username', 'Comment'
            ])

            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                if files:
                    expected_columns = set(dataframe.columns)

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

            last_10_comment_uuids_dict = {
                uuid: True
                for uuid in dataframe['Comment UUID'].tail(10)
            }
            new_batch_dataframe = pd.DataFrame(columns=[
                'Date Time', 'Comment UUID', 'Chat ID', 'Chat Title',
                'User ID', 'Username', 'Comment'
            ])
            message_count = 1

            async for message in app.get_chat_history(chat_id):
                if message.date != None and message.text != None:
                    comment_uuid = str(chat_id) + '-' + str(message.id)
                    if comment_uuid in last_10_comment_uuids_dict:
                        update_save_dataframe(dataframe, new_batch_dataframe,
                                              dir_path, chat_title)
                        break

                    if message.from_user != None:
                        if message.from_user.username != None:
                            user_id = message.from_user.id
                            username = message.from_user.username

                        elif message.from_user.first_name != None:
                            user_id = message.from_user.id
                            username = message.from_user.first_name

                        else:
                            user_id = message.from_user.id
                            username = ''

                    elif message.sender_chat != None:
                        user_id = message.sender_chat.id
                        username = message.sender_chat.username

                    else:
                        user_id = ''
                        username = ''

                    comment = message.text

                    if isinstance(message.date, str):
                        parsed_datetime = datetime.strptime(
                            message.date, datetime_format)
                    else:
                        parsed_datetime = message.date

                    new_row = pd.DataFrame([{
                        'Date Time': parsed_datetime,
                        'Comment UUID': comment_uuid,
                        'Chat ID': chat_id,
                        'Chat Title': chat_title,
                        'User ID': user_id,
                        'Username': username,
                        'Comment': comment
                    }])
                    new_batch_dataframe = pd.concat(
                        [new_batch_dataframe, new_row],
                        axis=0,
                        ignore_index=True)

                    if message_count % 100 == 0:
                        print(
                            "Retrieving chat data: {}, {}, {}, {}, {}, {}, {}..."
                            .format(parsed_datetime, comment_uuid, chat_id,
                                    chat_title, user_id, username, comment))

                    if message_count % 1000 == 0:
                        print("\n")

                        dataframe, last_10_comment_uuids_dict = update_save_dataframe(
                            dataframe, new_batch_dataframe, dir_path,
                            chat_title)

                        new_batch_dataframe = pd.DataFrame(columns=[
                            'Date Time', 'Comment UUID', 'Chat ID',
                            'Chat Title', 'User ID', 'Username', 'Comment'
                        ])

                    message_count += 1

            else:
                update_save_dataframe(dataframe, new_batch_dataframe, dir_path,
                                      chat_title)

        print(
            "Data downloaded successfully. Please use crypto-sentiment-on-chart.ipynb next.\n"
        )


app.run(main(CHAT_ID_LIST))
