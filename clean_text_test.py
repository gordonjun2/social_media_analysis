import re
import unicodedata
from data_manager import *

# Example usage:
corpus = [
    "Nice 9% pre market move for $para, pump my calls Uncle Buffett.......... 🤑",
    "Check out this amazing deal on www.crypto.com!",
    "RT @username Wow! Bitcoin hit $60K!",
    "これはテストです。",  # Japanese text for "This is a test."
    "Send Bitcoin to 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa or contact support.",
    "Send Ethereum to 0xAb5801a7D398351b8bE11C439e05C5B3259aec9B or check 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "Donate Solana to 9xZyLXz4aBnAYWgNuTkpsU8d2KQVoPe4F3NDSUENY3yD or visit http://crypto.com",
    "Bullish on moons",
    '<span>&gt;bitcoin&;s price is going to the moon</span>',
    '<a href=\"#p58831614\" class=\"quotelink\">&gt;&gt;58831614</a><br>We fucking won!!!!!',
    "https://open.spotify.com/show/64hmk<wbr>mXpetPEVGPlExkDGl<br><br><span class=\"quote\">&gt;ex-board member Holly Etlin makes claim that what happened to Bed Bath &amp; Beyond has not happened except in cases of fraud</span><br>https://www.reddit.com/r/Teddy/comm<wbr>ents/1945r00/holly_etlins_statement<wbr>_regarding_bbby_potentially/<br><span class=\"quote\">&gt;Share Buyback Fraud Explained</span><br>https://threadreaderapp.com/thread/<wbr>1749490369258250493.html<br><br><span class=\"quote\">&gt;Do companies state that they face bankruptcy...but then *suddenly* do a 180 &quot;Reverse Uno&quot;, squeeze short sellers and bring riches to shareholders?</span><br>https://reddit.com/r/BBBY/comments/<wbr>16ohoy3/do_companies_sometimes_offi<wbr>cially_state_that_they/<br><br><span class=\"quote\">&gt;How Can BBBYQ Exit Chapter 11 In A Way That Benefits Shareholders</span><br>https://reddit.com/r/BBBY/comments/<wbr>15r9jgh/guess_whos_back_salvatores_<wbr>back/<br><br><span class=\"quote\">&gt;End Game: DTC and NSCC are screwed as the DTC just proved shareholders should Directly Register Shares (DRS)</span><br>https://reddit.com/r/Superstonk/com<wbr>ments/13a3yh1/end_game_dtc_and_nscc<wbr>_are_screwed_as_the_dtc_just/<br><br>bbby &quot;class action&quot; case against RC<br>CASE NUMBER: 1:22-cv-02541-TNM<br>https://www.courtlistener.com/docke<wbr>t/64916203/si-v-bed-bath-beyond-cor<wbr>poration/<br><br>Ryan Cohen&#039;s 16b short swing rule was dismissed the other day. But his &quot;pump and dump&quot; case is still active and may be holding things up.<br><br>previous thread:<br><a href=\"/biz/thread/58800198#p58800198\" class=\"quotelink\">&gt;&gt;58800198</a>"
]

cleaned_corpus = [clean_text(post) for post in corpus]
print(cleaned_corpus)
