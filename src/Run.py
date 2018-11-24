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
import requests
import commands.io
from contextlib import closing
import pymysql

s = openSocket()
joinRoom(s)
readbuffer = ""


def console(line):
    # gets if it is a user or twitch server
    if "PRIVMSG" in line:
        return False
    else:
        return True

def load_lists(item_type):
    items = []
    try:
        item_list = open("../config/" + item_type + "_list.txt", "r")
    except FileNotFoundError:
        print(item_type.title() + "list not found, creating new.")
    else:
        for line in item_list:
            items.append(line.strip())
        item_list.close()
    return items

mods = load_lists("mod")


def save_list(item_type):
    item_list = open(("../config/" + item_type + "_list.txt"), "w")
    if item_type == "mod":
        for mod in mods:
            print(mod, file = item_list)
    elif item_type == "pun":
        for pun in puns:
            print(pun, file = item_list)
    elif item_type == "quote":
        for quote in quotes:
            print(quote, file = item_list)
    elif item_type == "command":
        for command in commands.keys():
            print(str(command) + " " + str(commands[command]), file = item_list)
    item_list.close()


def new_item(input):
    new_item = []
    try:
        new_item = input.split()
        new_item = (" ").join(new_item[1:])
    except IndexError:
        sendMessage(s, '/w ' + user + ' Syntax: !command argument')
    else:
        return new_item


def sb(word):
    if "give" == word:
       try:       
           sbgive(message.split()[2],message.split()[3])
       except:           
           sendMessage(s, "Commands: !sb give <user> <runs>")
    elif "take" == word:
       try:
           sbtake(message.split()[2],message.split()[3])
       except:
           sendMessage(s, "Commands: !sb take <user> <runs>")
    elif "add" == word:
       try:
           sbadd(message.split()[2],message.split()[3])
       except:
           sendMessage(s, "Commands: !sb add <user> <tier level>")
    elif "finished" == word:
        finished()
    else:
        sendMessage(s, ">>Commands: !sb give|take|add <<")


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
   try:
       cursor.execute(sql)
       db.commit()
       bunnyinfo(user)
   except:
       db.rollback()
       sendMessage(s,"Error: unable to fetch data notify thinkllama")

   db.close()




def bunny(word,user):
    if "info" == word:
        try:
            bunnyinfo(user)
        except:
           sendMessage(s, "Commands: !bunny info")
    elif "run" == word:
       try:
           checkavail(user)
           bunnyrun(user,message.split()[2],message.split()[3],message.split()[4],message.split()[5])
       except:
           sendMessage(s, "Commands: !runs run <game name> <server> <key> <key level>")
    elif "list" == word:
        bunnylist()
    else:
        sendMessage(s, "Commands: !runs list,run,info")

def bunnyrun(user,wowuser,server,key,level):
   try:
       runs=checkavail(user)
       checkruns=int(runs)
       if runs <= "0": 
           sendMessage(s,"No more runs left sorry!")
       else:
           db = pymysql.connect(DBHOST,DBUSER,DBPASS,DB)
           cursor = db.cursor()
           sql = "Insert into runs(twitchuser,wowuser,server,keyname,finished) Values ('%s', '%s', '%s', '%s %s','no')" % (user,wowuser,server,key,level)
           try:
               cursor.execute(sql)
               db.commit()
               sendMessage(s,"%s your run has been added to the list." % (user))
           except:
               db.rollback()
               sendMessage(s,"Error: unable to fetch data notify thinkllama")

           db.close()
   except:
           sendMessage(s,"Are you a t3 sub? I can't find you")
           

def checkavail(user):
   db = pymysql.connect(DBHOST,DBUSER,DBPASS,DB)

   cursor = db.cursor()

   sql = "SELECT * FROM tiersubs where twitchuser = '%s' " % (user)
   try:
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       for row in results:
           twitchuser = row[1]
           runs = row[3]
           level = row[4]
           return runs
   except:
           sendMessage(s,"Error: unable to fetch data notify thinkllama")

   db.close()




def bunnyinfo(user):
   db = pymysql.connect(DBHOST,DBUSER,DBPASS,DB)

   cursor = db.cursor()

   sql = "SELECT * FROM tiersubs where twitchuser = '%s' " % (user) 
   try:
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       for row in results:
           twitchuser = row[1]
           runs = row[3]
           level = row[4]
           sendMessage(s,"%s you currently have %s runs and are currenly a Tier %s sub" % (twitchuser,runs,level))
   except:
           sendMessage(s,"Error: unable to fetch data notify thinkllama")

   db.close()



def bunnylist():
   db = pymysql.connect(DBHOST,DBUSER,DBPASS,DB)

   cursor = db.cursor()

   sql = "SELECT * FROM runs where finished like 'no'"
   sendMessage(s,">>Current run list:<<")           
   try:
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       mylist = []
       for row in results:
           twitchuser = row[1]
           key = row[4]
           sendMessage(s,"%s - %s" % (twitchuser,key))           
   except:
           sendMessage(s,"Error: unable to fetch data notify thinkllama")

   db.close()



def add_mod(input):
    if new_item(input) == CHANNEL:
        sendMessage(s, "...Dood, really?")
    elif new_item(input) in mods:
        sendMessage(s, "User is already a moderator.")
    else:
        mods.append(new_item(input))
        sendMessage(s, "Moderator added.")


def del_mod(input):
    if new_item(input) == CHANNEL:
        sendMessage(s, "Not possible.")
    elif new_item(input) in mods:
        mods.remove(new_item(input))
        sendMessage(s, "Moderator removed.")
    save_list("mod")

def add_item(input, item_type):
    if len(new_item(input)) >= 1:
        if item_type == "pun":
            puns.append(new_item(input))
            sendMessage(s, "Pun added.")
        elif item_type == "quote":
            quotes.append(new_item(input))
            sendMessage(s, "Quote added.")
        elif item_type == "mod":
            add_mod(input)
        elif item_type == "command":
            add_command(input)
        save_list(item_type)


while True:
    try:
        readbuffer = s.recv(1024)
        readbuffer = readbuffer.decode()
        temp = readbuffer.split("\n")
        readbuffer = readbuffer.encode()
        readbuffer = temp.pop()
    except:
        temp = ""
    for line in temp:
        if line == "":
            break
        # to prevent the bot being timed out
        if "PING" in line and console(line):
            msgg = "PONG :tmi.twitch.tv\r\n".encode()
            s.send(msgg)
            print(msgg)
            break
        # get user
        user = getUser(line)
        # get message sent by user
        message = getMessage(line)
        print(user + " : " + message)
        PMSG = "/w" + user + " "


###### COMMANDS ######


        first_word = message.split()[0]
                 

        if "!runs" == first_word:
            try:
                second_word = message.split()[1]
                bunny(second_word,user)
            except:
                sendMessage(s, "Commands: !runs list,run,info")

        if "!io" == first_word:
            try:
                realm = message.split()[1]
                name = message.split()[2]
                io(realm,name)
            except:
                sendMessage(s, "Usage: !io <realm> <character>")


        if "!super" == first_word:
            if user != CHANNEL and not user in mods:
                sendMessage(s, "You cannot run Super commands!")
            if user in mods:
                second_word = message.split()[1]
                sb(second_word)
            elif user == CHANNEL:
                try:
                    second_word = message.split()[1]
                    sb(second_word)
                except:
                    sendMessage(s, ">>Commands: !sb give|take|add <<")


        if "!addmod" == first_word:
            if user == CHANNEL:
                add_item(message, "mod")
            else:
                sendMessage(s, "Only the channel owner can add mods.")
        if "!delmod" == first_word:
            if user == CHANNEL:
                del_mod(message)
            else:
                sendMessage(s, "Only the channel owner can remove mods.")


        if "!test" == first_word:
           bunnyrun(user,message.split()[2],message.split()[3],message.split()[4],message.split()[5])

        if "!quit" == first_word:
            if user == CHANNEL:
                sendMessage(s, "Exiting.")
                time.sleep(0.7)
                sys.exit(0)

        if "!kill" == first_word:
            if user != CHANNEL and user in mods:
                sendMessage(s, "You cannot kill that which is immortal.")
            elif user == CHANNEL:
                sendMessage(s, "AAAGGGHHH!")
                time.sleep(0.7)
                sys.exit(0)

    time.sleep(0.7)
