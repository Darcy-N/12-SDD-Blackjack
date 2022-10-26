import os
import sys

def clear():
  os.system('cls||clear')

card_list = []

def card_loader(path):
    for i in os.listdir(path):
        if not i.startswith('.'):
            card_list.append(i)
        else:
            pass # 👏 GO 👏 AWAY 👏 .DS_Store 👏
    return card_list