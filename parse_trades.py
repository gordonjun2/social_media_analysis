import pandas as pd
import pickle
import os

# Specify the path to your .pkl file
pkl_path = './saved_data/telegram/-4604107012-Crypto News Aggregator/comments_2025-03-16 18:12:57_2025-08-17 17:54:11.pkl'


def load_pickle_to_dataframe(file_path):
    """
    Load a pickle file and convert it to a pandas DataFrame
    
    Args:
        file_path (str): Path to the pickle file
        
    Returns:
        pd.DataFrame: The loaded DataFrame
    """
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file {file_path} does not exist")

        # Load the pickle file
        with open(file_path, 'rb') as f:
            data = pickle.load(f)

        # Convert to DataFrame if it's not already one
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        return data

    except Exception as e:
        print(f"Error loading the pickle file: {str(e)}")
        return None


def filter_and_join_simulated_trades(df):
    """
    Filter rows with 'Trade Simulated' in Comment, then left join twice
    to get the comments of the replied-to comments.

    Args:
        df (pd.DataFrame): Input DataFrame with at least 'Comment UUID', 'Comment', 'Reply to Comment UUID'
    
    Returns:
        pd.DataFrame: Filtered and joined DataFrame with renamed columns
    """
    if df is None or 'Comment' not in df.columns:
        print("Error: Invalid DataFrame or 'Comment' column not found")
        return None

    # Step 1: Filter for simulated trades
    filtered_df = df[df['Comment'].str.contains('Trade Simulated',
                                                case=False,
                                                na=False)].copy()

    # Step 2: First left join (a.'Reply to Comment UUID' = b.'Comment UUID')
    df_b = df[['Comment UUID', 'Comment', 'Reply to Comment UUID']].rename(
        columns={
            'Comment': 'Reply1_Comment',
            'Comment UUID': 'Comment_UUID_b',
            'Reply to Comment UUID': 'Reply_to_Comment_UUID_b'
        })
    merged_df = filtered_df.merge(df_b,
                                  how='left',
                                  left_on='Reply to Comment UUID',
                                  right_on='Comment_UUID_b')

    # Step 3: Second left join (df_b's Reply_to_Comment_UUID → df_c's Comment UUID)
    df_c = df[['Comment UUID', 'Comment']].rename(columns={
        'Comment UUID': 'Comment_UUID_c',
        'Comment': 'Reply2_Comment'
    })
    merged_df = merged_df.merge(
        df_c,
        how='left',
        left_on=
        'Reply_to_Comment_UUID_b',  # <-- join using df_b's reply-to field
        right_on='Comment_UUID_c')

    # Step 4: Keep only a.*, b.Comment, c.Comment
    cols_to_keep = list(
        filtered_df.columns) + ['Reply1_Comment', 'Reply2_Comment']
    final_df = merged_df[cols_to_keep]

    return final_df


def extract_trade_details(df):
    """
    Extract trading details from Comment column and create new columns for Symbol, Direction, and PnL
    
    Args:
        df (pd.DataFrame): Input DataFrame containing trade comments
        
    Returns:
        pd.DataFrame: DataFrame with new columns added
    """
    if df is None or df.empty:
        return df

    def extract_symbol(comment):
        try:
            for line in comment.splitlines():
                if 'Symbol:' in line:
                    return line.split('Symbol:')[1].strip()
        except:
            return None

    def extract_direction(comment):
        try:
            # Direction is the first word of the first line
            first_line = comment.splitlines()[0]
            return first_line.split()[1]  # 'LONG' → 'long', 'SHORT' → 'short'
        except:
            return None

    def extract_pnl(comment):
        try:
            before = after = None
            for line in comment.splitlines():
                if 'Before Capital:' in line:
                    before = float(
                        line.split('$')[1].split()[0].replace(',', '').strip())
                elif 'After Capital:' in line:
                    after = float(
                        line.split('$')[1].split()[0].replace(',', '').strip())
            if before is not None and after is not None:
                return after - before
        except:
            return None

    def extract_sentiment(row):
        try:
            # Try to find sentiment in each comment column
            for col in ['Comment', 'Reply1_Comment', 'Reply2_Comment']:
                if pd.isna(row[col]):
                    continue

                comment = row[col]
                for line in comment.splitlines():
                    if 'Sentiment:' in line:
                        # Extract percentage and convert to float
                        sentiment = line.split('Sentiment:')[1].strip()
                        # Remove % sign and convert to float
                        return float(sentiment.replace('%', '')) / 100
            return None
        except:
            return None

    # Create new columns
    df['Symbol'] = df['Comment'].apply(extract_symbol)
    df['Direction'] = df['Comment'].apply(extract_direction)
    df['PnL'] = df['Comment'].apply(extract_pnl)
    df['Sentiment Score'] = df.apply(extract_sentiment, axis=1)

    return df


if __name__ == "__main__":
    # Load the data
    df = load_pickle_to_dataframe(pkl_path)

    if df is not None:
        # Display basic information about the DataFrame
        print("\nDataFrame Info:")
        print(df.info())

        print("\nFirst few rows of the DataFrame:")
        print(df.head(10))

        print("\nLast few rows of the DataFrame:")
        print(df.tail(10))

        print("\nSome columns:")
        print(df[[
            'Date Time', 'Comment', 'Reply to Comment UUID', 'Reply to Comment'
        ]])

        print("\nDataFrame shape:", df.shape)

        # Filter and display simulated trades
        print("\nFiltering simulated trades...")
        simulated_trades = filter_and_join_simulated_trades(df)
        if simulated_trades is not None and not simulated_trades.empty:
            # Extract trade details
            simulated_trades = extract_trade_details(simulated_trades)

            print("\nFound simulated trades:")
            print(simulated_trades[[
                'Date Time', 'Comment', 'Symbol', 'Direction', 'PnL',
                'Sentiment Score'
            ]])
            print("\nNumber of simulated trades found:", len(simulated_trades))

            # Save to Excel file
            output_file = './saved_data/simulated_trades.xlsx'
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            simulated_trades.to_excel(output_file, index=False)
            print(f"\nSimulated trades saved to: {output_file}")
        else:
            print("\nNo simulated trades found in the data")
