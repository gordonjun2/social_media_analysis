import pandas as pd
from datasets import load_dataset
from data_manager import clean_text, save_df


def download_hugging_face_datasets():

    # https://huggingface.co/datasets/StephanAkkerman/financial-tweets-crypto
    print(
        "Retrieving data from https://huggingface.co/datasets/StephanAkkerman/financial-tweets-crypto..."
    )
    financial_tweets_crypto_StephanAkkerman_df = pd.read_csv(
        "hf://datasets/StephanAkkerman/financial-tweets-crypto/crypto.csv")
    financial_tweets_crypto_StephanAkkerman_df = financial_tweets_crypto_StephanAkkerman_df[
        (financial_tweets_crypto_StephanAkkerman_df['tweet_type'] != 'retweet')
        & (financial_tweets_crypto_StephanAkkerman_df['timestamp'].notna())]
    financial_tweets_crypto_StephanAkkerman_df['timestamp'] = pd.to_datetime(
        financial_tweets_crypto_StephanAkkerman_df['timestamp'],
        format='ISO8601',
        errors='coerce')
    financial_tweets_crypto_StephanAkkerman_df = financial_tweets_crypto_StephanAkkerman_df.dropna(
        subset=['timestamp'])
    financial_tweets_crypto_StephanAkkerman_df[
        'timestamp'] = financial_tweets_crypto_StephanAkkerman_df[
            'timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    financial_tweets_crypto_StephanAkkerman_df = financial_tweets_crypto_StephanAkkerman_df.rename(
        columns={
            'timestamp': 'Date Time',
            'tweet_text': 'Comment',
        })
    financial_tweets_crypto_StephanAkkerman_df = financial_tweets_crypto_StephanAkkerman_df[
        ['Date Time', 'Comment']]
    financial_tweets_crypto_StephanAkkerman_df = financial_tweets_crypto_StephanAkkerman_df.sort_values(
        by='Date Time', ascending=True).reset_index(drop=True)

    # print(financial_tweets_crypto_StephanAkkerman_df.head())

    # https://huggingface.co/datasets/ckandemir/bitcoin_tweets_sentiment_kaggle
    print(
        "Retrieving data from https://huggingface.co/datasets/ckandemir/bitcoin_tweets_sentiment_kaggle..."
    )
    splits = {
        'train': 'data/train-00000-of-00001-cc8461398e266567.parquet',
        'test': 'data/test-00000-of-00001-922aa10406034550.parquet',
        'eval': 'data/eval-00000-of-00001-dc793d916ae447cb.parquet'
    }
    bitcoin_tweets_sentiment_kaggle_train_ckandemir_df = pd.read_parquet(
        "hf://datasets/ckandemir/bitcoin_tweets_sentiment_kaggle/" +
        splits["train"])
    bitcoin_tweets_sentiment_kaggle_test_ckandemir_df = pd.read_parquet(
        "hf://datasets/ckandemir/bitcoin_tweets_sentiment_kaggle/" +
        splits["test"])
    bitcoin_tweets_sentiment_kaggle_eval_ckandemir_df = pd.read_parquet(
        "hf://datasets/ckandemir/bitcoin_tweets_sentiment_kaggle/" +
        splits["eval"])
    bitcoin_tweets_sentiment_kaggle_ckandemir_df = pd.concat([
        bitcoin_tweets_sentiment_kaggle_train_ckandemir_df,
        bitcoin_tweets_sentiment_kaggle_test_ckandemir_df,
        bitcoin_tweets_sentiment_kaggle_eval_ckandemir_df
    ],
                                                             axis=0,
                                                             ignore_index=True)
    bitcoin_tweets_sentiment_kaggle_ckandemir_df = bitcoin_tweets_sentiment_kaggle_ckandemir_df[
        bitcoin_tweets_sentiment_kaggle_ckandemir_df['Date'].notna()]
    bitcoin_tweets_sentiment_kaggle_ckandemir_df['Date'] = pd.to_datetime(
        bitcoin_tweets_sentiment_kaggle_ckandemir_df['Date'],
        format='%Y-%m-%d')
    bitcoin_tweets_sentiment_kaggle_ckandemir_df[
        'Date'] = bitcoin_tweets_sentiment_kaggle_ckandemir_df[
            'Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
    bitcoin_tweets_sentiment_kaggle_ckandemir_df = bitcoin_tweets_sentiment_kaggle_ckandemir_df.rename(
        columns={
            'Date': 'Date Time',
            'text': 'Comment',
        })
    bitcoin_tweets_sentiment_kaggle_ckandemir_df = bitcoin_tweets_sentiment_kaggle_ckandemir_df[
        ['Date Time', 'Comment']]
    bitcoin_tweets_sentiment_kaggle_ckandemir_df = bitcoin_tweets_sentiment_kaggle_ckandemir_df.sort_values(
        by='Date Time', ascending=True).reset_index(drop=True)

    # print(bitcoin_tweets_sentiment_kaggle_ckandemir_df.head())

    # https://huggingface.co/datasets/Myashka/CryptoNews
    print(
        "Retrieving data from https://huggingface.co/datasets/Myashka/CryptoNews..."
    )
    dataset_dict = load_dataset("Myashka/CryptoNews")
    CryptoNews_train_Myashka_df = pd.DataFrame(dataset_dict['train'])
    CryptoNews_validation_Myashka_df = pd.DataFrame(dataset_dict['validation'])
    CryptoNews_Myashka_df = pd.concat(
        [CryptoNews_train_Myashka_df, CryptoNews_validation_Myashka_df],
        axis=0,
        ignore_index=True)
    CryptoNews_Myashka_df = CryptoNews_Myashka_df[
        CryptoNews_Myashka_df['created'].notna()]
    CryptoNews_Myashka_df['created'] = pd.to_datetime(
        CryptoNews_Myashka_df['created'])
    CryptoNews_Myashka_df['created'] = CryptoNews_Myashka_df[
        'created'].dt.strftime('%Y-%m-%d %H:%M:%S')
    CryptoNews_Myashka_df = CryptoNews_Myashka_df.rename(columns={
        'created': 'Date Time',
        'text': 'Comment',
    })
    CryptoNews_Myashka_df = CryptoNews_Myashka_df[['Date Time', 'Comment']]
    CryptoNews_Myashka_df = CryptoNews_Myashka_df.sort_values(
        by='Date Time', ascending=True).reset_index(drop=True)

    # print(CryptoNews_Myashka_df.head())

    # Concat all dataframes
    hugging_face_df = pd.concat([
        financial_tweets_crypto_StephanAkkerman_df,
        bitcoin_tweets_sentiment_kaggle_ckandemir_df, CryptoNews_Myashka_df
    ],
                                axis=0,
                                ignore_index=True)

    # Clean text and sort by date time
    hugging_face_df['Comment'] = hugging_face_df['Comment'].apply(clean_text)
    hugging_face_df = hugging_face_df[hugging_face_df['Comment'] != '']
    hugging_face_df['Date Time'] = pd.to_datetime(hugging_face_df['Date Time'])
    hugging_face_df = hugging_face_df.sort_values(
        by='Date Time', ascending=True).reset_index(drop=True)
    start_datetime = hugging_face_df.iloc[0]['Date Time']
    end_datetime = hugging_face_df.iloc[-1]['Date Time']

    # print(hugging_face_df.head())
    # print(hugging_face_df.tail())

    dir_path = './saved_data/hugging_face'
    save_df(hugging_face_df, dir_path, start_datetime, end_datetime)


print("\n")
download_hugging_face_datasets()
print(
    "Data downloaded successfully. Please use crypto-sentiment-on-chart.ipynb or social-media-summariser.ipynb next."
)
print("\n")
