import os
import time
import threading
os.chdir("web")

args_lst = [
    "python manage.py runserver 8081",
    "start chrome --app=http://127.0.0.1:8081"
]

for i in range(len(args_lst)):    
    t = threading.Thread(target=os.system, args=(args_lst[i],))
    t.start()
    time.sleep(2)
