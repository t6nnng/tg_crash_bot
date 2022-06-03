import telebot, pymysql, random, json
from telebot import types
import randx
from threading import Timer

token = '5546304370:AAHIkBGtKKIa491g0vnriQ3Ngq2IwoLQvcE'
b = telebot.TeleBot(token)

kb = types.ReplyKeyboardMarkup(resize_keyboard=True)

balB = types.KeyboardButton(text="/balance")
roundB = types.KeyboardButton(text="/roundinfo")
kb.add(balB)
kb.add(roundB)

Round = []
lasttime = 45
isEnd = False
Next = randx.rand()
print(Next)

@b.message_handler(commands=['start', 'help'])
def start(m):
    b.send_message(m.chat.id, "Привет! В этом сообщении расскажу как играть.\n\n", reply_markup=kb)

@b.message_handler(commands=['balance'])
def balance(m):
    bal = 0
    with open("data.json", "r") as dat:
        data = json.load(dat)
        try:
            bal = data[str(m.from_user.username)]
        except:
            Str = ""
            with open("data.json", "r") as file:
                Str = file.read()[:len(Str)-1]

            with open("data.json", "w") as file:
                Id = str(m.from_user.username)
                Str2 = Str + f', "{Id}' +'":100' + "}"
                file.write(Str2)
                bal = 100
                
    b.send_message(m.chat.id, m.from_user.first_name + ", твой баланс: " + str(bal) + "$")

@b.message_handler(commands=['next'], func=lambda m: m.from_user.username == "t6nnng")
def next(m):
    global Next
    b.send_message(m.from_user.id, Next)

@b.message_handler(commands=['end'], func=lambda m: m.from_user.username == "t6nnng")
def end(m):
    global lasttime
    lasttime = 1
    b.send_message(m.from_user.id, "Success")

@b.message_handler(commands=['add'])
def add(m):
    if m.from_user.username == "t6nnng":
        words = m.text.split()
        bal = 0
        with open("data.json", "r") as dat:
            data = json.load(dat)
            data[words[1]] = int(data[words[1]]) + int(words[2])
            with open("data.json", "w") as file:
                json.dump(data, file)

        b.send_message(m.from_user.id, "Success")

@b.message_handler(commands=['bet'])
def bet(m):
    global Round
    words = m.text.split()
    with open("data.json", "r") as file:
        data = json.load(file)
        try:
            if int(data[m.from_user.username]) >= int(round(float(words[1]))):
                with open("data.json", "w") as file1:
                    data[m.from_user.username] -= int(round(float(words[1])))
                    json.dump(data, file1)
                Round += [[m.from_user.username, int(round(float(words[1]))), float(words[2])]]
                b.send_message(m.chat.id, m.from_user.first_name + ", твоя ставка принята!")
            else:
                b.send_message(m.chat.id, m.from_user.first_name + ", на твоём балансе недостаточно средств!")
        except:
            b.send_message(m.chat.id, "Неправильная формулировка запроса! ps: Макар, пиши нормально!")

@b.message_handler(commands=['roundinfo'])
def roundinfo(m):
    message = f"До конца раунда осталось {lasttime} секунд.\n\nСтавки:\n"
    for item in Round:
        message += f"{item[0]}: {item[1]}$\n"

    b.send_message(m.chat.id, message)
    

def onescnd():
    global lasttime, isEnd, Round, Next
    if lasttime <= 0:
        
        message = f"Итоги раунда! Выпало число {Next}!\n\nИтоги ставок:\n"
        for item in Round:
            if int(item[2]) <= Next:
                message += f"{item[0]}, {item[1]}$ * {item[2]}x = {round(int(item[1]) * float(item[2]))}$\n"
                with open("data.json", "r") as file:
                    data = json.load(file)
                    with open("data.json", "w") as file1:
                        data[item[0]] += round(int(item[1]) * float(item[2]))
                        json.dump(data, file1)
            else:
                message += f"{item[0]}, ставка на {item[2]}x провалилась!\n"
        
        b.send_message("-617445059", message)
        Next = randx.rand()
        print(Next)
        Round = []
        lasttime = 45
    else:
        lasttime -= 1
    t = Timer(1,onescnd)
    t.start()

onescnd()

b.polling(none_stop = True)
