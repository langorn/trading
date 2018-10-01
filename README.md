# trading 
a stock analysis program

i am using pyalgotrade to implement my own strategy of buying stock.

you might need to have some basic technical knowledge( i am use sma20 - sma40)
https://www.investopedia.com/terms/s/sma.asp
http://www.cmoney.tw/notes/note-detail.aspx?nid=15977



How It works ?
simply type:
python3 sma_updown.py

you might also need to change the sma_updown's setting

feed = GenericBarFeed(Frequency.DAY, None, None)
feed.addBarsFromCSV("genting", "genting2.csv")   //replace with the stock name and the file name
instrument = "genting"

*** also remember your csv file need to same with the pyalgotrade format , otherwise , it wont work


Reference:
Pyalgotrade
http://gbeced.github.io/pyalgotrade/
