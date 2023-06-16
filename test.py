import shelve
from datetime import datetime

year = datetime.now().year
month = datetime.now().strftime("%m")
with shelve.open(f'tracker{year}{month}') as db:
    for i in db:
        print(db[i])

with shelve.open('user') as db:
    for i in db:
        print(db[i])