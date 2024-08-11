import time
import pandas as pd
from urllib.request import urlopen
import json


def get_jsonparsed_data(url):
    """
    Receive the content of ``url``, parse it as JSON and return the object.

    Parameters
    ----------
    url : str

    Returns
    -------
    dict
    """
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


#Biz has 10 pages

def update_dataframe():
dataframe = pd.DataFrame(columns=['Subject', 'Comment'])
list = len(data['threads'])
url = ("https://a.4cdn.org/biz/1.json")
data = get_jsonparsed_data(url)

    for i in range(0, list): 
        try:
            comment = data['threads'][i]['posts'][0]['com']
            subject = data['threads'][i]['posts'][0]['sub']
        except KeyError:
            subject = 'No subject'
        print(subject)
        print(comment + ' ,')
        dataframe = dataframe.append({'Subject':subject, 'Comment':comment}, ignore_index=True)
    return