import curses
from curses import panel 
import pickle
import os
import urllib
import urllib.parse
import urllib.request
import time
import ssl
import sys
# PYTHON SMS REPEATER WITH PROOVL SMS API CONNECTION
# https://github.com/aarnhub
# MAX LIMIT YOU CAN CHANGE - line 102 (by default 15)
def mainmenu():  
    hedr()
    key = 0
    if not os.path.exists('smsrepdb.pickle'):
         smsrepeater.addstr(11, 4, "1 STEP => SETUP API SETTINGS", curses.color_pair(3))
    else:
         smsrepeater.addstr(11, 4, "                            ")
    smsrepeater.addstr(12, 4, "[ A ] SEND SMS")
    smsrepeater.addstr(13, 4, "[ B ] API SETTINGS")
    smsrepeater.addstr(14, 4, "[ Q ] QUIT")
    smsrepeater.addstr(15, 4, "Choose button on keyboard: ", curses.color_pair(2))
    try:
        key = smsrepeater.getch(15,30)
        smsrepeater.addch(15,31,key)
        if key == ord('a') or key == ord('A'):
            smsrepeater.clear()
            curses.endwin()
            smsrep()
        elif key == ord('b') or key == ord('B'):
            smsrepeater.clear()
            settings()
        elif key == ord('q') or key == ord('Q'):
            curses.endwin()
            print("bye")
            sys.exit()
        else: 
            smsrepeater.refresh()
            smsrepeater.addstr(16, 6, "Wrong key press detected...")
            mainmenu()
    except:         
      smsrepeater.refresh()
def settings():
    hedr()
    key = 0
    smsrepeater.addstr(12, 4, "[ A ] CHANGE SETTINGS")
    smsrepeater.addstr(13, 4, "[ B ] BACK")
    smsrepeater.addstr(14, 4, "Choose button on keyboard: ", curses.color_pair(2))

    try:
        key = smsrepeater.getch(14,30)
        smsrepeater.addch(14,30,key)
        if key == ord('a') or key == ord('A'):
            smsrepeater.clear()
            settapi()
        elif key == ord('b') or key == ord('B'):
            smsrepeater.clear()
            mainmenu()
        else: 
            smsrepeater.refresh()
            smsrepeater.addstr(18, 6, "Wrong key press detected...")
            settings()
    except:   
            smsrepeater.refresh()
def smsrep():
  print("\033[H\033[J")
  print (""" 
  \x1B[32m    ___ __  __ ___                                                   
│    / __|  \/  / __|                                                  
│    \__ \ |\/| \__ \                                                  
│    |___/_|  |_|___/                                                  
│    ___ ___ ___ ___   _ _____ ___ ___                                 
│   | _ \ __| _ \ __| /_\_   _| __| _ \                               
│   |   / _||  _/ _| / _ \| | | _||   /                                
│   |_|_\___|_| |___/_/ \_\_| |___|_|_\ 
 
  SMS Repeater: github.com/aarnhub \033[1;0m
  """)   
  try:
              with open('smsrepdb.pickle', 'rb') as rfp:
               otput = pickle.load(rfp)
              from2 = otput[0]
              user1 = otput[1]
              token1 = otput[2]       
  except:
    print("\033[1;33mAfter sending, please check Api settings. It can't be empty \033[1;0m")
    from2 = "44555555555"
    user1 = "Empty"
    token1 = "Empty"
  finally:   
    user = user1  
    token = token1 
    from1 = from2  
    print("\033[1;33mSettings SID:" + from1 + " UID:" + user + " token:" + token + "\033[1;0m")
    int_string = input("  \033[1;32m 1.Enter phone numbers, separated by comma:\033[1;0m\n")
    input_string2 = input("  \033[1;32m 2.Enter Text and press Enter:\033[1;0m\n")
    while True:
      try:
        user_number = int(input("  \033[1;32m 3.How many times repeate SMS to this numbers? (min 1 - 15 max):\033[1;0m\n"))
        assert 0 < user_number < 15  # MAX LIMIT 15 
      except ValueError:
        print("  \033[1;31mNot a number! Please enter a number.\033[1;0m")
      except AssertionError:
        print("  \033[1;31mPlease enter a number between 1 and 15\033[1;0m")
      else:     
        numbers = int_string.split(",")
        n = int(user_number)
        messagesSent = 0
        host = "https://www.proovl.com/api/send.php?"
        hdr = { 'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)' }
        for x in range (n): 
          for x in numbers:
            messagesSent += 1
            params = {
            "user": user,       
            "token": token,
            "from": from1,
            "text": input_string2,
            "to": x}
            try:
              _create_unverified_https_context = ssl._create_unverified_context
            except AttributeError:
              pass
            else:
              ssl._create_default_https_context = _create_unverified_https_context
            query_string = urllib.parse.urlencode(params)   
            http_req = host + query_string
            req = urllib.request.Request(http_req, headers=hdr)
            f = urllib.request.urlopen(req)
            txt = (f.read().decode('utf-8'))
            z = txt.split(";")
            time.sleep(0.5)
            print("\033[1;32mProgress: {}/{}\033[1;0m".format(messagesSent, len(numbers)), (x),("" + z[1] + ""))
          if z[0] == "Error":
            print("\033[1;31m== Error. Text messages not sent ==\033[1;0m")
          else:
            print("\033[1;32m== All messages has been sent! ==\033[1;0m")
        else:  
          f.close()
          if input("Send new message? \033[1;32m(Y/N)\033[1;0m").strip().upper() != 'Y':
            print("\033[H\033[J")
            mainmenu()
            return
          else:
            print("\033[H\033[J")
            smsrep()
def settapi():
          curses.endwin()
          print("\033[H\033[J")
          print (""" 
  \x1B[32m    ___ __  __ ___                                                   
│    / __|  \/  / __|                                                  
│    \__ \ |\/| \__ \                                                  
│    |___/_|  |_|___/                                                  
│    ___ ___ ___ ___   _ _____ ___ ___                                 
│   | _ \ __| _ \ __| /_\_   _| __| _ \                               
│   |   / _||  _/ _| / _ \| | | _||   /                                
│   |_|_\___|_| |___/_/ \_\_| |___|_|_\
  
  SMS Repeater: github.com/aarnhub \033[1;0m
  """)  
          input_number = input("  \033[1;32m1.Enter www.Proovl.com Phone number\033[1;0m\n")
          input_userid = input("  \033[1;32m2.Enter www.Proovl.com UserID\033[1;0m\n") 
          input_token = input("   \033[1;32m3.Enter www.Proovl.com Token\033[1;0m\n") 
          try:
              os.system('color 1f')
              with open('smsrepdb.pickle', 'wb') as wfp:
               pickle.dump((input_number, input_userid, input_token), wfp, protocol=pickle.HIGHEST_PROTOCOL)

              with open('smsrepdb.pickle', 'rb') as rfp:
               otput = pickle.load(rfp)
 
              smsrepeater.addstr(17, 4, "Number: " + otput[0] )
              smsrepeater.addstr(18, 4, "UserID: " + otput[1] )
              smsrepeater.addstr(19, 4, "Token: " + otput[2] )    
          except:
              print("Something wrong. Check files permissions.")
          finally:
              print("\033[H\033[J")
              mainmenu()
              return   
def hedr():
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    height, width = smsrepeater.getmaxyx()
    smsrepeater.border(0)
    smsrepeater.addstr(1,4,"  ___ __  __ ___", curses.color_pair(1))
    smsrepeater.addstr(2,4," / __|  \/  / __|", curses.color_pair(1)) 
    smsrepeater.addstr(3,4," \__ \ |\/| \__ \ ", curses.color_pair(1)) 
    smsrepeater.addstr(4,4," |___/_|  |_|___/", curses.color_pair(1))
    smsrepeater.addstr(5,4," ___ ___ ___ ___   _ _____ ___ ___", curses.color_pair(1))
    smsrepeater.addstr(6,4,"| _ \ __| _ \ __| /_\_   _| __| _ \ ", curses.color_pair(1))
    smsrepeater.addstr(7,4,"|   / _||  _/ _| / _ \| | | _||   /", curses.color_pair(1))
    smsrepeater.addstr(8,4,"|_|_\___|_| |___/_/ \_\_| |___|_|_\ ", curses.color_pair(1))
    smsrepeater.addstr(10, 4, " SMS Repeater: github.com/aarnhub   ", curses.color_pair(1))      
    #smsrepeater.endwin()
def LogicLoop():
    mainmenu()
try:
    smsrepeater = curses.initscr()
    hedr()
    LogicLoop()
finally:
    print(":)")
    curses.endwin()
    sys.exit()
    
