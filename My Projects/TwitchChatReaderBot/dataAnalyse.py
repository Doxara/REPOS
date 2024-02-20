import asyncio
import datetime
import re
import time
from tkinter import filedialog as fd
import os
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from operator import itemgetter

list_all_del_symb = '<>!&?*^%$#()\\/{}[]"№+-=' + "'"

time_start_chating = 0
time_start_end_chating = 0


def readFileToDict(pathToFile):
    ff = open(pathToFile, 'r', encoding='utf-8')
    # словарь со всеми данными
    dict = {'messages': []}
    for line in ff:
        if line != "\n":
            mes = line.split(":")
            for i in range(len(mes)):
                mes[i] = mes[i].replace("\n", "")
            mes[1] = mes[1][1:-1]
            mesDict = {'time': float(mes[0]), 'username': mes[1], 'mes': mes[2]}
            dict['messages'].append(mesDict)
    return dict


async def printUsers(usersInfo, allUniqueUsers):
    while True:
        nick = input()
        printUserMessages(usersInfo['users'][allUniqueUsers.index(nick)])


def printUserMessages(user):
    print(f"Никнейм: {user['name']}")
    for mes in user['mes']:
        print(f'[{time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(mes[1]))}] {mes[0]}')


def printUserInfo(user):
    print(f"Никнейм: {user['name']}")
    print(f"Всего символов написано: {user['allNumOfSymb']}")
    print(f"Сообщений написано: {user['numOfMes']}")
    print(f"Средняя длина слова: {user['midLenOfWords']}")
    print(f"Средняя длина сообщения: {user['midSymbInMes']}")
    print(f"Среднее количество слов в сообщении: {user['midWordInMes']}")
    print(f"Тегал других {user['numOfTagsOth']} раз")
    print(f"Тегнули {user['numOfTagsHim']} раз")
    print(f'Используемые слова:\n{user["wordsUsed"]}')
    if user['dontTagOth']:
        print("Не тегает других, хотя его тегали")
    print("_________________________________________________")


def printUsersInfo(usersInfo, allUniqueUsers):
    for it in usersInfo['users']:
        printUserInfo(it)


async def main():
    allWordsForStream = {}

    pathNow = os.path.dirname(os.path.abspath(__file__))

    nameOfFile = fd.askopenfilename(title='Выбери файл для анализа', defaultextension='txt', initialdir=pathNow)

    print(nameOfFile)

    # словарь со всеми данными
    data = readFileToDict(nameOfFile)

    time_start_chating = data['messages'][0]['time']
    time_start_end_chating = data['messages'][-1]['time']
    print(
        f'Начало в {time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(time_start_chating))} и окончание в {time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(time_start_end_chating))}')

    # словаь с информацией о каждом пользователе
    # nick и все сообщения пользователя
    usersInfo = {'users': []}

    # кто упоминал и кого упоминал
    tagNames = {}

    allMessages = len(data['messages'])
    print('Всего сообщений:', allMessages)
    allSymb = 0
    for i in range(len(data['messages'])):
        allSymb += len(data['messages'][i]['mes'])
    print('Всего символов:', allSymb)

    numOfAllUniqueUsers = 0

    # Уникальные пользователи
    allUniqueUsers = []
    # ОБРАБОТКА ВСЕХ ДАННЫХ
    for i in range(len(data['messages'])):

        data_usr_time = data['messages'][i]['time']
        data_usr_name = data['messages'][i]['username']
        data_usr_mes = data['messages'][i]['mes']
        edit_mes = re.sub(r"https?://[^,\s]+,?", "", data_usr_mes)
        for symb in '.,:;':
            edit_mes = edit_mes.replace(symb, ' ')
        for symb in list_all_del_symb:
            edit_mes = edit_mes.replace(symb, '')

        if data_usr_name not in allUniqueUsers:
            tagNames[data_usr_name[:].lower()] = []
            allUniqueUsers.append(data_usr_name)
            userDict = {'name': data_usr_name, 'mes': [[edit_mes, data_usr_time]], 'allNumOfSymb': len(data_usr_mes)}

            userDict['numOfMes'] = 0
            userDict['midLenOfWords'] = 0
            userDict['midSymbInMes'] = 0
            userDict['midWordInMes'] = 0
            userDict['numOfTagsHim'] = 0
            userDict['numOfTagsOth'] = 0
            userDict['dontTagOth'] = False

            usersInfo['users'].append(userDict)
        else:
            for j in range(len(usersInfo['users'])):
                usr_name = usersInfo['users'][j].get('name')
                # print('usr_name=',usr_name)
                if usr_name == data['messages'][i]['username']:
                    usersInfo['users'][j]['mes'].append([edit_mes, data_usr_time])
                    usersInfo['users'][j]['allNumOfSymb'] += len(data_usr_mes)

        # анализ слов в сообщении
        words_in_edit_mes = edit_mes.split(" ")
        for k in range(len(words_in_edit_mes)):
            if len(words_in_edit_mes[k]) > 0:
                words_in_edit_mes[k] = words_in_edit_mes[k].replace(" ", '')
        for word in words_in_edit_mes:
            if word != '':
                if word[0] == '@' and word[:2] != '@ ':
                    # фиксируем все упоминания людей
                    tagNames[data_usr_name[:].lower()].append(word[1:].lower())
                else:
                    wordInLow = word.lower()
                    if wordInLow in allWordsForStream:
                        allWordsForStream[wordInLow] += 1
                    else:
                        allWordsForStream[wordInLow] = 0

    allWordArr = allWordsForStream.items()
    allWordArr = sorted(allWordArr, key=itemgetter(1),reverse=True)
    numOfTop = len(allWordArr) if len(allWordArr) < 20 else 20
    if numOfTop != 0:
        print(f'Топ {numOfTop} слов по частоте упоминания:')
        for i in range(numOfTop):
            index = i+1
            print('[%2d]' % index + f' {allWordArr[i][0]} - {allWordArr[i][1]}')



    numOfAllUniqueUsers = len(allUniqueUsers)
    print('Всего разных пользователей:', numOfAllUniqueUsers)

    numOfMessages = []

    for it in usersInfo['users']:
        it['wordsUsed'] = {}
        # print("Никнейм:", it['name'])
        # print("MES:",it['mes'])
        k = len(it['mes'])

        # print('Количество сообщений написанных пользователем:', k)
        numOfMessages.append((it['name'], k))
        it['numOfMes'] = k
        sum = 0
        numOfWords = 0
        sumLensOfWords = 0
        for messages in it['mes']:
            sum += len(messages) - 1
            for mes in messages[:-1]:
                words = mes.split(' ')
                wordWithoutTag = []
                for word in words:
                    if words[0] != '@' and word != '':
                        wordWithoutTag.append(word)
                        sumLensOfWords += len(word)
                        if word.lower() in it['wordsUsed']:
                            it['wordsUsed'][word.lower()] += 1
                        else:
                            it['wordsUsed'][word.lower()] = 1
                numOfWords += len(wordWithoutTag)

        if numOfWords != 0:
            it['midLenOfWords'] = sumLensOfWords / numOfWords
        else:
            it['midLenOfWords'] = 0

        if k != 0:
            it['midSymbInMes'] = sum / k
            it['midWordInMes'] = numOfWords / k
        else:
            it['midSymbInMes'] = 0

    numOfMessages = sorted(numOfMessages, key=itemgetter(1))
    numOfTop = 10
    if len(numOfMessages) < 10:
        numOfTop = len(numOfMessages)
    if numOfTop > 0:
        print(f'Топ {numOfTop} по сообщениям, людей:')
        for i in range(-1, -numOfTop - 1, -1):
            print('[%2d]' % -i + f'{numOfMessages[i][0]} : {numOfMessages[i][1]} сообщений')

    # print('Тэги людей:')
    tags = list(tagNames.items())
    numOfAllTags = 0
    maxTags = 0
    whoMaxTags = ''

    howManyAnyTags = []

    howManyNotTag = 0
    someOneTags = []
    allTags = []

    for it in tags:
        numOfAllTags += len(it[1])
        if len(it[1]) > 0:
            # usersInfo['users'][it[0]]['numOfTagsOth'] = len(it[1])
            # print(f"{it[0]} тегнул других {len(it[1])} раз")
            ind = allUniqueUsers.index(it[0])
            usersInfo['users'][ind]['numOfTagsOth'] = len(it[1])
            allTags = list(it[1] + allTags)
            howManyAnyTags.append((it[0], len(it[1])))
        else:
            howManyNotTag += 1
        if len(it[1]) > maxTags:
            maxTags = len(it[1])
            whoMaxTags = it[0]

    howManyAnyTags = sorted(howManyAnyTags, key=itemgetter(1))

    print('Всего тегов людей:', numOfAllTags)
    print('Людей которые никого не тегали:', howManyNotTag)

    numOfTop = 10
    if len(howManyAnyTags) < 10:
        numOfTop = len(howManyAnyTags)
    # print(f'Больше всего тегал {whoMaxTags}. Тегнул других {maxTags} раз')
    if numOfTop > 0:
        print(f'Топ {numOfTop} по людям, кто тегал:')
        for i in range(-1, -numOfTop - 1, -1):
            print('[%2d]' % -i + f'{howManyAnyTags[i][0]} : {howManyAnyTags[i][1]} раз')

    howManyWhomTags = Counter(allTags)

    numOfTop = 10

    list_howManyWhomTags = sorted(list(howManyWhomTags.items()), key=itemgetter(1))

    if len(howManyWhomTags) < 10:
        numOfTop = len(howManyWhomTags)

    for i in range(len(list_howManyWhomTags)):
        if list_howManyWhomTags[i][0] in allUniqueUsers:
            usersInfo['users'][allUniqueUsers.index(list_howManyWhomTags[i][0])]['numOfTagsHim'] = \
            list_howManyWhomTags[i][1]
        list_howManyWhomTags[i] = (list_howManyWhomTags[i][0], list_howManyWhomTags[i][1])

    if numOfTop > 0:
        print(f'Топ {numOfTop} по людям, кого тегали:')
        for i in range(-1, -numOfTop - 1, -1):
            print('[%2d]' % -i + f'{list_howManyWhomTags[i][0]} : {list_howManyWhomTags[i][1]} раз')

    whoNeverTag = []
    allWhoTags = []
    for it in howManyAnyTags:
        allWhoTags.append(it[0])

    for it in list_howManyWhomTags:
        if it[0] not in allWhoTags and it[0] != '':
            whoNeverTag.append(it[0])
            if it[0] in allUniqueUsers:
                usersInfo['users'][allUniqueUsers.index(it[0])]['dontTagOth'] = True

    whoNeverTag.reverse()

    print('Люди кого тегали, но кто никого не тегал:')
    for it in whoNeverTag:
       print(it)

    printUsersInfo(usersInfo, allUniqueUsers)

    # Временные метки в виде массива дробных чисел
    timestamps = []

    firstTime = data['messages'][0]['time']
    for it in data['messages']:
        timestamps.append(float(it['time']) - firstTime)

    # Создание списка минутных интервалов
    minutes = [int(timestamp // 60) for timestamp in timestamps]

    # Подсчет количества меток на каждую минуту
    count = {}
    for minute in minutes:
        count[minute] = count.get(minute, 0) + 1

    # Разделение словаря на ключи и значения

    times = [float(it) for it in list(count.keys())]
    y = list(count.values())

    # x = [time.strftime("%H:%M:%S",time.gmtime(it)) for it in times]
    x = list(count.keys())
    # Вывод данных на график
    plt.figure(figsize=(10, 5))
    # Отображение гистограммы
    plt.bar(x, y, width=0.8, align='edge')

    plt.xlabel('Минуты')
    plt.ylabel('Количество сообщений')
    plt.title('Количество сообщений на каждую минуту')
    plt.show()

    task = asyncio.create_task(printUsers(usersInfo, allUniqueUsers))
    await task


asyncio.run(main())
