from django.test import TestCase

# Create your tests here.
from random import randint
import time
from datetime import datetime
x = randint(0, 3)
print(x)
time.sleep(x)
print("star2t")

print(str(datetime.now())[:19])


x= '12.0'
y= '15'
print(float(x) + float(y))
