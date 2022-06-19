from imp import reload
import random
import math
import json
import sys

words_list = list("abcdefghijklmnopqrstuvwxyz")


resolution = 49
middle_row = int((resolution / 2) + 1)
range_num = int(math.sqrt(resolution))

result = []

# get random word from list


def getRandomWord(word_list):
    return random.choice(word_list)


def diagonalDown(x, y):
    if (x == 1 and y == 7) or (x == 2 and y == 6) or (x == 3 and y == 5) or (x == 4 and y == 4) or (x == 5 and y == 3) or (x == 6 and y == 2) or (x == 7 and y == 1):
        return True
    else:
        return False


words_list = list("abcdefghijklmnopqrstuvwxyz")
middle_row = int((resolution / 2) + 1)
range_num = range(int(math.sqrt(resolution)))
counter = 0
for i in range_num:
    arr = []
    for l in range_num:
        x = l + 1
        y = i + 1
        arr.append({
            "word": random.choice(words_list),
            "x": x,
            "y": y,
            "checked": True if diagonalDown(x, y) else False
        })
        if diagonalDown(x, y):
            counter += 1
    result.append(arr)


print("RESULT ")
print(f"{result}")


def concat(arr):
    result = []
    for i in range(len(arr)):
        for l in range(len(arr[i])):
            result.append(arr[i][l])
    return result


concated = concat(result)


def isCheckedVertical(arr):
    resolution = 7
    for i in range(resolution):
        checked_amount = 0
        for word in arr:
            if word.get("x") == i and word.get("checked"):
                print("passed")
                checked_amount += 1
            elif word.get("x") == i and not word.get("checked"):
                checked_amount = 0
                break
        if checked_amount == resolution:
            return True
    return False


def isCheckedHorizontal(arr):
    resolution = 7
    for i in range(resolution):
        checked_amount = 0
        for word in arr:
            if word.get("y") == i and word.get("checked"):
                print("passed")
                checked_amount += 1
            elif word.get("y") == i and not word.get("checked"):
                checked_amount = 0
                break
        if checked_amount == resolution:
            return True


def isCheckedDiagonalIndexUp(arr):
    resolution = 7
    checked_amount = 0
    for i in range(resolution):
        if arr[i][i].get("checked"):
            print("passed")
            checked_amount += 1
        else:
            checked_amount = 0
            break
    if(checked_amount == resolution):
        return True
    else:
        return False


def isCheckedDiagonalIndexDown(arr):
    resolution = 7
    checked_amount = 0
    for i in range(resolution):
        y = i + 1
        x = resolution - i
        print(x, y)
        for word in arr:
            if word.get("x") == x and word.get("y") == y and word.get("checked"):
                print("passed")
                checked_amount += 1
            else:
                continue
    if(checked_amount == resolution):
        return True


print("------- X -------")

for word in concated:
    if diagonalDown(word.get("x"), word.get("y")):
        print(f"{word}")


foo = isCheckedDiagonalIndexDown(concated)


# get all words from txt file in root folder and split by space


def getWords():
    with open("./words.txt") as f:
        return f.read().split()


print("------- TEEXT -------")

text = getWords()

print(text)


print("------- CMD -------")


print(sys.argv)
cmd_arr = sys.argv

for i, arg in enumerate(cmd_arr):
    obj = dict()
    if(arg == "-wordfile"):
        obj["wordfile"] = cmd_arr[i + 1]
    if(arg == "-grid"):
        obj["resolution"] = cmd_arr[i + 1]
    if(arg == "-maxplayers"):
        obj["maxplayers"] = cmd_arr[i + 1]


# Get timestamp in form YYYY-MM-DD-HH-MM-SS
def getTimestamp():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


print(getTimestamp())
