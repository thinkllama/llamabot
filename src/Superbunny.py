import random
import time
import sys
from Read import getUser, getMessage
from Socket import openSocket, sendMessage
from Initialize import joinRoom
from Settings import CHANNEL
from Settings import DBUSER
from Settings import DBPASS
from Settings import DBHOST
from Settings import DB
import pymysql

def sb(word):
    if "give" == word:
        sbgive(message.split()[2],message.split()[3])
    elif "take" == word:
        sbtake(message.split()[2],message.split()[3])
    elif "add" == word:
        sbadd(message.split()[2],message.split()[3])
    elif "finished" == word:
        finished()
    else:
        sendMessage(s, "Commands: !sb give|take")


def sbgive(user,runs):
   db = pymysql.connect(DBHOST,DBUSER,DBPASS,DB)

   cursor = db.cursor()

   sql = "UPDATE tiersubs SET runs = runs + %s where twitchuser = '%s'" % (runs,user)
   try:
       cursor.execute(sql)
       db.commit()
       bunnyinfo(user)
   except:
       db.rollback()
       sendMessage(s,"Error: unable to fetch data notify thinkllama")

   db.close()

def sbtake(user,runs):
   db = pymysql.connect(DBHOST,DBUSER,DBPASS,DB)

   cursor = db.cursor()

   sql = "UPDATE tiersubs SET runs = runs - %s where twitchuser = '%s'" % (runs,user)
   try:
       cursor.execute(sql)
       db.commit()
       bunnyinfo(user)
   except:
       db.rollback()
       sendMessage(s,"Error: unable to fetch data notify thinkllama")

   db.close()

def sbadd(user,level):
   db = pymysql.connect(DBHOST,DBUSER,DBPASS,DB)

   cursor = db.cursor()

   sql = "Insert into tiersubs(twitchuser,runs,level) Values ('%s', '3', '%s')" % (user,level)
   print(sql)
   try:
       cursor.execute(sql)
       db.commit()
       bunnyinfo(user)
   except:
       db.rollback()
       sendMessage(s,"Error: unable to fetch data notify thinkllama")

   db.close()
