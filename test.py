import numpy
from datetime import datetime as dt
from datetime import timedelta

openTime = dt(2019, 3, 5, 6, 0, 0)
closingTime = dt(2019, 3, 5, 21, 0, 0)
def random_min_max(min, max, size):
    result = numpy.random.rand(size) * (max - min) + min
    return result

def random_avg_int(avg, size):
    result = numpy.round(numpy.random.normal(loc=avg, size=size)).astype(int)
    print(numpy.mean(result))
    print(numpy.min(result))
    print(numpy.max(result))
    return result

def random_min_max_int(min, max, size):
    result = numpy.round(numpy.random.rand(size) * (max - min) + min).astype(int)
    print(numpy.mean(result))
    print(numpy.min(result))
    print(numpy.max(result))
    return result

def random_avg_min_max_int(min, avg, max, size):
    result1 = random_avg_int(avg, round(size * 0.98))
    result2 = random_min_max_int(min, max, round(size * 0.02))
    result = numpy.concatenate((result1, result2))
    print(numpy.mean(result))
    print(numpy.min(result))
    print(numpy.max(result))
    return result

print("General Time Spent")
test = random_avg_min_max_int(6, 25, 75, 10000)


print("\ntime spent avg")
test = random_avg_int(10, 100)

print("\ntime spent min max")
test = random_min_max_int(45,60,100)

print("\nTime In")
test = random_min_max(openTime, closingTime, 5000)
a = {}
t = []
for i in test:
    if i.day not in t:
        t.append(i.day)
    hour = i.hour
    if hour == 21:
        print(i)
    if hour not in a:
        a[hour] = 1
    else:
        a[hour] += 1
print(t)
sum = 0
kc = 0
for key, value in a.items():
    print (key, ":", value)
    sum += value
    kc += 1
print("sum", sum)
print("number of hours", kc)

a = {"a": 5, "b": 0, "c": 20}
print(a)
b = {"a": 15, "b": 20, "c": 0}
print(b)
from collections import Counter


def merge_dicts(dict_1, dict_2):
    return dict(Counter(dict_1) + Counter(dict_2))


print(merge_dicts(a,b))

