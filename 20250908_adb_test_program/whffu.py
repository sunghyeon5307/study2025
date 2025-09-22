import random

result =[]

for i in range(6):
    num=random.randint(1,100)
    if num not in result:
        result.append(num)

print(result)