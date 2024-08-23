from pyrogram import Client
import json
import pandas as pd
import os
from datetime import datetime
import warnings
from data_manager import delete_files
from config import TELEGRAM_API_KEY, TELEGRAM_HASH, CHAT_ID_TO_GET_MEMBERS_LIST


def save_dict_to_json(dict, dir_path, current_datetime):

    cached_file_path = '{}/chat_members_{}.json'.format(
        dir_path, current_datetime)

    os.makedirs(dir_path, exist_ok=True)
    with open(cached_file_path, 'w') as file:
        json.dump(dict, file)


warnings.filterwarnings("ignore")

CONFIG = {
    "telegram_api_id": TELEGRAM_API_KEY,
    "telegram_hash": TELEGRAM_HASH,
}

app = Client("text_scraper",
             CONFIG["telegram_api_id"],
             CONFIG["telegram_hash"],
             takeout=True,
             sleep_threshold=10)

all_members_info_dict = {}


async def main():
    async with app:
        for chat_id in CHAT_ID_TO_GET_MEMBERS_LIST:
            chat_info = await app.get_chat(chat_id)
            chat_title = chat_info.title

            print("\nRetrieving chat members data from: {} ({})...".format(
                chat_title, chat_id))

            dir_path = './saved_data/telegram/{}'.format(
                str(chat_id) + '-' + chat_title)
            files_to_delete = []

            if os.path.exists(dir_path):
                files = os.listdir(dir_path)
                if files:
                    for file in files:
                        if not file.endswith('.json'):
                            continue

                        file_path = dir_path + '/' + file
                        files_to_delete.append(file_path)

            try:
                async for member in app.get_chat_members(chat_id):
                    if member.user != None:
                        if member.user.is_bot == False and member.user.is_scam == False and member.user.is_fake == False:
                            all_members_info_dict[member.user.id] = {
                                "username": member.user.username,
                            }

                current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                delete_files(files_to_delete)
                save_dict_to_json(all_members_info_dict, dir_path,
                                  current_datetime)
                print("Saved {}'s chat members data on {}".format(
                    chat_title, current_datetime))
                print("\n")
            except Exception as e:
                print(
                    "Failed to retrieve chat members data from: {} ({}) due to"
                    .format(chat_title, chat_id))
                print(e)
                print("\n")
                continue

        print("Data downloaded successfully.")


app.run(main())
print("\n")
