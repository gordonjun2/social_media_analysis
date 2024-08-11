from data_manager import *

pd.set_option('display.max_columns', None)

file_path = './saved_data/4chan/biz/2024-08-05 21:02:24_2024-08-11 17:49:43.pkl'

dataframe = load_df(file_path)

print(dataframe.head())
print(dataframe.tail())
