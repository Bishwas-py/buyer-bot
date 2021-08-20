import sys
import pathlib
path = str(pathlib.Path(__file__).parent.absolute()).replace('\\','/')
from selenium import webdriver
import threading
from chromedriver_py import binary_path # this will get you the path variable
from.additionals import getDriver
from.bot import Bots
from..models import Items

threads = dict()

def threader():
    items = Items.objects.all()
    
    for i in range(items.count()):
        item = items[i]
        driver = getDriver(item.profile)
        bot = Bots(driver)
        t = threading.Thread(target=bot.bestbuy, args=(item, i,), name=f'Bestbuy Bot {i}')
        t.start()
        threads.update({
            i:
            {
                'driver' : driver,
                "item": item,
                'enabled': 1,
                'error': None
            }
        })


def run_isolated_bot(index:int):
    thread = threads[index]
    item = thread['item']
    driver = getDriver(f"profile/{item.profile}")
    bot = Bots(driver)
    thread = threads[index]
    t = threading.Thread(target=bot.bestbuy, args=(item, index,), name=f'Bestbuy Bot {index}')
    t.start()
    thread.update({
        'driver': driver,
        'enabled': 1,
        'error': None
    })


def quit_bot(index:int, witherror = False):
    thread = threads[int(index)]
    driver = thread['driver']
    driver.quit()
    thread.update(
        {'enabled':0, "error":witherror}
    )


def quit_all_bot():
    for index in list(threads):
        thread = threads[index]
        driver = thread['driver']
        driver.quit()
        thread.update(
            {'enabled':0, "error":False}
        )
    
    
def get_threads():
    return threads