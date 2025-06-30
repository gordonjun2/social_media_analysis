import os
from configparser import ConfigParser

root_dir = os.path.abspath(os.path.dirname(__file__))
config_file = os.path.join(root_dir, "private.ini")
cfg = ConfigParser()
cfg.read(config_file)

telegram = dict(cfg.items('telegram'))
TELEGRAM_API_KEY = int(telegram.get('telegram_api_key', 0))
TELEGRAM_HASH = telegram.get('telegram_hash', '')

CHAT_ID_LIST = [
    # -1002019095590, -1002134817341, -1001178977739, -1001827032034,
    # -1002129864451, -1001870913071, -1001164734593, -1001683662707,
    # -1001809898162, -1001718338599, -1001559038987, -1001848837618,
    # -1002062690940, -1001369518127, 941146023
    # 788105004,
    -4523641033
]

CHAT_ID_TO_GET_MEMBERS_LIST = [
    -1002081438683, -1002143108337, -1002445494815, -1002168179520
]
'''
    ~~~Examples of Crypto-related Channels and their Chat IDs~~~
    Anteater's Amazon: -1002019095590
    Anteater's Amazon Chat: -1002134817341
    Ape City Chat: -1001178977739
    HanSolarTG: -1001827032034
    ByteAI News: -1002129864451
    Moonbags Personal Notes: -1001870913071
    SpiderCrypto Trading Journal: -1001164734593
    Ian's Intel: -1001683662707
    Degen Trading House: -1001809898162
    Pepe Research: -1001718338599
    Noodles Trading: -1001559038987
    Crypto Narratives: -1001848837618
    Magimaxxing: -1002062690940
    POPCAT: -1002081438683
    NUB: -1002143108337
    Crypto Mumbles: -1001369518127
'''
