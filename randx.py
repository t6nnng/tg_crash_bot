import random

item_chances = {
    '1to2': 75,
    '2to5': 40,
    '5to10': 15,
    '10to100': 5,
    '100to10000': 1,
    '0': 5
}

def rand():
    a = ""
    b = 0.0
    selected = random.choices(list(item_chances.keys()), weights=list(item_chances.values()))
    for item in set(selected):
        a = item

    if a == "1to2":
        b = random.uniform(1,2)
        b = round(b, 2)
    elif a == "2to5":
        b = random.uniform(2,5)
        b = round(b, 2)
    elif a == "5to10":
        b = random.uniform(5,10)
        b = round(b, 2)
    elif a == "10to100":
        b = random.uniform(10,100)
        b = round(b, 2)
    elif a == "100to10000":
        b = random.uniform(100,10000)
        b = round(b, 2)
    elif a == "0":
        pass

    return b

