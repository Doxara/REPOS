import re
import socket
import config
import time
from datetime import datetime
import sys

if __name__ == '__main__':
    botNamesList = []
    botNamesList.append("moobot")
    botNamesList.append("streamelements")
    botNamesList.append("nightbot")
    botNamesList.append("wizebot")
    botNamesList.append("murrhq")
    


    streamerNick = 'Insize'

    if len(sys.argv) > 1:
        streamerNick = sys.argv[1]
    else:
        print('Введи стримера:')
        ss = input()
        streamerNick = ss
    nameOfStream = ''
    nameOfStream = input()

    print("Select streamer:", streamerNick)

    flag = 0
    dateNow = datetime.now().date()

    print(dateNow)
    
    if nameOfStream != '' and nameOfStream != '-':
        fileName = f"log_{streamerNick}_{dateNow}_{nameOfStream}.txt"
    else:
        fileName = f"log_{streamerNick}_{dateNow}.txt"

    s = socket.socket()
    s.connect((config.HOST, config.PORT))
    s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(streamerNick).encode("utf-8"))
    chat_message = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    while True:
        response = s.recv(1024*4).decode("utf-8")

        if flag >= 2:
            if response == "PING :tmi.twitch.tv\r\n":
                print("пришел пинг\n")
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            else:
                messages = response.split("\r\n")[:-1]

                for message in messages:
                    usrname = re.search(r"\w+", message).group(0)
                    mes = chat_message.sub("", message)

                    if usrname not in botNamesList and 'http://' not in mes and 'https://' not in mes:
                        print(f"{datetime.now()}:[S][{usrname}]:{mes}")
                        file = open(fileName, "a", encoding="utf-8")
                        try:
                            file.write(f"{time.time()}:[{usrname}]:{mes}\n\n")
                        except NameError:
                            print("Except=", NameError)
                        file.close()
                    else:
                        print(f"{datetime.now()}:[-][{usrname}]:{mes}")

        else:
            flag += 1
