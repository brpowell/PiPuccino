import ystockquote
from time import sleep
from random import shuffle
from multiprocessing import Process

def load_screen():
    while True:
        lcd.message("Yahoo!    [*   ]\n    Stocks"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Stocks"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Stocks"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [   *]\n    Stocks"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Stocks"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Stocks"); sleep(0.5); lcd.clear()
        lcd.message("Yahoo!    [*   ]\n    Stocks"); sleep(0.5); lcd.clear()

loading_loop = Process(target=load_screen)

#LCD welcome
lcd.backlight(lcd.TEAL)
loading_loop.start()
sleep(1.5)

stock_list = config.get('stocks', 'list').split(',')
print(stock_list)
shuffle(stock_list)

def get_info(list):
    stocks = {}
    for s in stock_list:
        print(s)
        results = ystockquote.get_all(s)

        price = float(results['price'])
        price_change = results['change']
        #print(str(price)+'\n'+price_change)
        start = price - float(price_change)

        price_change = "%s%.2f " % (price_change[:1], float(price_change[1:]))
        percent_change = "%.2f%s" % (abs((100 - (start/price)*100)), '%')

        info = {'symbol': s, 'price':price, 'pricechange':price_change, 'percentchange':percent_change}
        stocks[s] = info
    return stocks

def run_display(stocks):
    while True:
        for s in stock_list:
            lcd.clear()
            lcd.message(stocks[s]['symbol'] + '  $' + str(stocks[s]['price']) + '\n' + stocks[s]['pricechange'] + stocks[s]['percentchange'])

            if stocks[s]['pricechange'][:1]=='+': lcd.backlight(lcd.GREEN)
            else: lcd.backlight(lcd.RED)

            sleep(5)

#Try to fetch stock info, otherwise fail screen
try: 
    stocks = get_info(stock_list)
    connection = True
except:
    connection = False
    lcd.clear()
    lcd.message("Yahoo!    [fail]\n    Stocks")

loading_loop.terminate()
if connection:
    display_loop = Process(target=run_display, args=(stocks,))
    display_loop.start()

while True:
    if lcd.buttonPressed(lcd.SELECT):
        break
display_loop.terminate()