import ystockquote
from time import sleep
from multiprocessing import Process


def load_screen():
    lcd.clear()
    while True:
        lcd.message("Yahoo!    [*   ]\n    Stocks"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Stocks"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Stocks"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [   *]\n    Stocks"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [  * ]\n    Stocks"); sleep(0.2); lcd.clear()
        lcd.message("Yahoo!    [ *  ]\n    Stocks"); sleep(0.2); lcd.clear()


def get_info(lst):
    """
    @param lst: Retrieve stock information
    @return: Dictionary; Key=stockcode value=dictionary of values for stock
    """
    stocks = {}
    for s in lst:
        results = ystockquote.get_all(s)

        price = round(float(results['price']), 2)
        price_change = results['change']
        start = price - float(price_change)

        price_change = "%s%.2f " % (price_change[:1], float(price_change[1:]))
        percent_change = "%.2f%s" % (abs((100 - (start/price)*100)), '%')

        info = {'symbol': s, 'price':price, 'pricechange':price_change, 'percentchange':percent_change}
        stocks[s] = info
    return stocks


def run_display(s_list):
    global stock_list
    while True:
        for s in stock_list:
            lcd.clear()
            lcd.message(s_list[s]['symbol'] + '   $' + str(s_list[s]['price']) + '\n' + s_list[s]['pricechange'] + s_list[s]['percentchange'])

            if stocks[s]['pricechange'][:1] == '+':
                lcd.backlight(lcd.GREEN)
            else:
                lcd.backlight(lcd.RED)

            sleep(5)

#Settings
stock_list = config.get('ystocks', 'list').split(',')

#Starting up
lcd.message("Yahoo!\n    Stocks")
lcd.backlight(lcd.TEAL)
loading_loop = Process(target=load_screen)
sleep(1)
loading_loop.start()

#Try to fetch and parse stocks
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

if connection:
    display_loop.terminate()