import uuid
from datetime import datetime


list=[]
list2=[]
list3=[]
list4=[]
list5=[]
list6=[]
for i in range(16):
    print(uuid.uuid4())
    list.append(3.5583)
    list2.append(6.1)
    list3.append(0.1017)
    list4.append(1.0167)
    list5.append(2.0333)
    list6.append(3.5583+6.1+0.1017+1.0167+2.0333)
current_day = datetime.now().day
print(list)
print(list2)
print(list3)
print(list4)
print(list5)
print(list6)