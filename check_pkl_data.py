import pandas as pd
import pickle
import os

# Specify the path to your .pkl file
pkl_path = './saved_data/telegram/-4523641033-The Start of Something/comments_2024-09-20 23:39:44+00:00_2025-06-23 21:52:19+00:00.pkl'


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

        print("\nDataFrame shape:", df.shape)
