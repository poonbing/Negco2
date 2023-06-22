import shelve

with shelve.open('tracker202306') as db:
    for i in db:
        print(db[i])

with shelve.open('user') as db:
    print(db['1'])