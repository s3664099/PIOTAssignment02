import datetime
from datetime import timedelta

x = datetime.datetime.now()
print(x)

x=datetime.datetime(2020,5,17,18)
print(x)

x=datetime.datetime(2020,4,21,13)
y=datetime.datetime(2020,4,21,18)
z=datetime.datetime.now()

if z>x and z<y:
	print("yes")
else:
	print("no")

x = x+ timedelta(days=4,hours=2)
y = y+ timedelta(days=4,hours=4)

print(x)
print(y)