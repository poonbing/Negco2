from datetime import datetime
import calendar

def calculate_shards(target):
    md2h = 75
    levelup = 10
    dailies = 10
    best_case = 3
    worst_case = 1
    average = 2
    count = 1
    week = 0
    best = 0
    av = 0
    worst = 0
    while True:
        week += ((md2h + 7*dailies)/levelup)
        best += week*best_case
        worst += week*worst_case
        av += week*average
        print(f"week {count} \n best case: {best} \n worst case: {worst} \n average: {av}")
        if worst > target:
            print(count)
            break
        count += 1

year = datetime.now().year
month = datetime.now().strftime("%m")
current_date = datetime.now().strftime("%d")
num_days = calendar.monthrange(year, int(month))[1]
print(year, month, current_date, num_days)