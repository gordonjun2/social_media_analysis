# social-media-analysis

### **Overview**
This repository contains a collection of Jupyter notebooks designed to analyse social media content in 4chan, Twitter, and possibly more. The notebooks cover various tasks such as post summarization, sentiment analysis, and identifying buzz topics. Currently, only free data from 4chan and Hugging Face are collected. By leveraging the free 4chan API, this project aims to provide insights into what people are talking about on 4chan, offering an alternative to platforms like Twitter where data collection might involve costs. This analysis can be particularly useful for understanding trends, sentiments, and emerging topics in the 4chan community.
<br>
<br>

### Included Analyses
Please look into the respective Jupyter notebook for more explanations and details.

1. **Social Media Summariser** (*social-media-summariser.ipynb*)

This notebook demonstrates a comprehensive analysis of social media posts from selected social media source, such as 4chan, Twitter (Hugging Face dataset), and Telegram. It focuses on retrieving data to create a word cloud of the most frequently mentioned terms. Additionally, the notebook employs a Hugging Face language model to summarise the content.

The primary goal is to analyze sentiment and trends within the cryptocurrency communities. By integrating these insights with various trading strategies, users can enhance their understanding of market sentiment and potentially improve their trading decisions.
<br>
<br>

### Notes
- This is a **personal project** of mine and was not created under any entity.
- Please be aware that the results provided by this project might not be 100% accurate due to potential bugs.
- Please do not rely on this software to make financial decisions. **NFA**.
<br>

### Future Updates
- Sentiment analysis
- Understanding buzz topics
<br>

### Data Sources, APIs & Models
- 4chan API
    - [Documentation](https://github.com/4chan/4chan-API)
    - DO NOT NEED KEYS
    - Endpoints to use:
        - GET https://a.4cdn.org/boards.json (A list of all boards and their attributes.)
        - GET https://a.4cdn.org/&lt;board&gt;/&lt;page no.&gt;.json (A list of threads and their preview replies from a specified index page.)
        - GET https://a.4cdn.org/&lt;board&gt;/thread/&lt;thread post no.&gt;.json (A full list of posts in a single thread.)
- Hugging Face Models
    - Suggested models:
        - [rittik9/Pegasus-finetuned-tweet-summary](https://huggingface.co/rittik9/Pegasus-finetuned-tweet-summary)
        - [mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization](https://huggingface.co/mrm8488/bert-small2bert-small-finetuned-cnn_daily_mail-summarization)
        - [Mr-Vicky-01/Bart-Finetuned-conversational-summarization](https://huggingface.co/Mr-Vicky-01/Bart-Finetuned-conversational-summarization)
- Pyrogram for Telegram API
    - [Documentation](https://docs.pyrogram.org/)
    - TELEGRAM API KEYS REQUIRED
        - Refer to [here](https://core.telegram.org/api/obtaining_api_id)
<br>

### **Installation**
1. Clone the repository using
    ```
    git clone https://github.com/gordonjun2/social-media-analysis.git
    ```
2. Navigate to the root directory of the repository.
    ```
    cd social-media-analysis
    ```
3. Create a Python virtual environment for this project.
    ```
    python3 -m venv venv
    ```
4. Activate the Python virtual environment.
    ```
    source venv/bin/activate
    ```
5. Install required packages.
    ```
    pip install -r requirements.txt
    ```
6. Install jupyter kernel for the virtual environment.
    ```
    python -m ipykernel install --user --name venv --display-name "social-media-analysis"
    ```
<br>

### How to Use

#### 4chan Data Download
- Run the command below to download the data:
    ```
    python data_manager.py
    ```
- When prompted 'Enter the board name to scrape: ', key in the 4chan's board name.
- The data will be downloaded as *.pkl* file in the ***saved_data/4chan/*** directory.
- The data will be updated whenever the download command is ran. The dataframe in the *.pkl* will increase in size.

#### Hugging Face Data Download
- Run the command below to download the data:
    ```
    python download_hugging_face_data.py
    ```
- The data will be downloaded as *.pkl* file in the ***saved_data/hugging_face/*** directory.

#### Telegram Data Download
- Rename private keys file.
    ```
    mv private_template.ini private.ini
    ```
- Obtain Telegram *api_id* and *api_hash* and paste it into the private keys file.
    - TELEGRAM_API_KEY: *api_id*
    - TELEGRAM_HASH: *api_hash*
- Save the private keys file.
- Open up the ```config.py``` and modify the *CHAT_ID_LIST* to contain the Chat IDs of the channel you want to scrape the data from.
    - To get the Chat ID of the channel, use Telegram Web and click on the channel.
    - The web URL contains the Chat ID.
        ```
        eg.
        https://web.telegram.org/a/#-1002081438683

        -1002081438683 is the Chat ID.
        ```
- Run the command below to download the data:
    ```
    python scrape_telegram_data.py
    ```
- The data will be downloaded as *.pkl* file in the ***saved_data/telegram/*** directory.

#### Analysis
- After the data is downloaded, you can start to use the Jupyter notebooks.
- To open the Jupyter notebook, run
    ```
    jupyter notebook <selected .ipynb>

    Eg.
    jupyter notebook social-media-summariser.ipynb
    ```
- Continue to follow the instructions and explanations in the respective notebook to perform the analysis.
- To execute the cell in the notebook, press 'SHIFT' + 'ENTER'.
<br>
