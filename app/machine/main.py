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
    print("Items Collected")
    
    for i in range(items.count()):
        item = items[i]
        print(f"Item: {item}")
        driver = getDriver(f"profile_{i}")
        print(f"Driver started")
        bot = Bots(driver)
        print(f"Boot targeted")
        t = threading.Thread(target=bot.bestbuy, args=(item.link, item.quantity, item.skip,), name=f'Bestbuy Bot {i}')
        print(f"Starting bot")
        t.start()
        print(f"BOT Started")
        threads.update({
            i:
            {
                'id': i,
                'driver' : driver,
                "item": item,
                'thread': t,
                'enabled': 1,
                'error': None
            }
        })


# def start_bot(index):
#     options = get_options()
#     index = int(index)
#     thread = threads[index]
#     driver = get_driver(options, thread['account'])
    
#     target = Automate(account=thread['account'], driver=driver)
#     t = threading.Thread(target=target.start, name=f'Deezer Bot {thread["id"]}')

#     threads[index].update(
#         {'thread':t, 'driver':driver}
#     )
    
#     t.start()
#     threads[index].update({
#                 'enabled': 1,
#                 'error': None
#     })


def quit_bot(index, witherror = False):
    thread = threads[int(index)]
    driver = thread['driver']
    driver.quit()
    thread.update(
        {'enabled':0, "error":witherror}
    )      

def get_threads():
    return threads