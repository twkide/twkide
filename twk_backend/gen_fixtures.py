
import sys
import random
import string
import json
from datetime import datetime

if len(sys.argv) != 3:
    print("Usage: " + sys.argv[0] + " <account prefix> <number of accounts>")
    assert False

random.seed(datetime.now())

numAcc = int(sys.argv[2])

students = []

for i in range(numAcc):
    # un = sys.argv[1] + ''.join(random.choices(string.digits, k=5))
    un = sys.argv[1] + str(i)
    pw = "password"
    print("student account: " + un + " , password = " + pw)
    students.append(
        { "model": "auth.user",
          "pk": i,
          "fields": {
            "username": un,
            "password": pw
          }
        }
    )

with open('output.json', 'w') as outfile:
    json.dump(students, outfile)

