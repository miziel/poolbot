from __future__ import division
import ch
import urllib
import json
import requests
import random
import time
import re
import threading
import Queue

#class BlockFinder(threading.Thread):
#    """ Threading example class
#    The run() method will be started and it will run in the background
#    until the application exits.
#    """
#
#    def __init__(self):
#        self.__init__()
#
#    def run(self, room, blocknum, q):
#        while True:
#          print "Enter while loop", blocknum
#          time.sleep(2)
#        poolstats = requests.get("https://supportxmr.com/api/pool/stats/").json()
#        blocknum_now = poolstats['pool_statistics']['totalBlocksFound']
#          if True:
#            print "Check if true"
#            room.message("Testing, testing")
#            print room.message
          
def prettyTimeDelta(seconds):
  seconds = int(seconds)
  days, seconds = divmod(seconds, 86400)
  hours, seconds = divmod(seconds, 3600)
  minutes, seconds = divmod(seconds, 60)
  if days > 0:
      return '%dd %dh' % (days, hours)
  elif hours > 0:
      return '%dh %dm' % (hours, minutes)
  elif minutes > 0:
      return '%dm %ds' % (minutes, seconds)
  else:
      return '%ds' % (seconds,)

class bot(ch.RoomManager):

#  def _watcher(self, blocknum, q):
#    while True:
#        print "Enter while loop", blocknum
#        time.sleep(10)
#        poolstats = requests.get("https://supportxmr.com/api/pool/stats/").json()
#        blocknum_now = poolstats['pool_statistics']['totalBlocksFound']
#        if True:
#            print "Check if true"
#            room.message("Testing, testing")
#            print room.message
#    q.put(blocknum)

#    print blocknum
    
#  def _messager(self, room, q):
#    time.sleep(5)
#    b = q.get() 
#    print "Messager ", b
#    room.message("Messager " + str(b))
        
#  def watcher_threaded(self, room):
#        poolstats = requests.get("https://supportxmr.com/api/pool/stats/").json()
#        blocknum = poolstats['pool_statistics']['totalBlocksFound']
#        q = Queue.Queue()
#        t1 = BlockFinder(self, room, blocknum, q)
#        t2 = threading.Thread(target=self._messager(room, q))
#        t1.start()
#        t2.start()
        

  def onInit(self):
    self.setNameColor("CC6600")
    self.setFontColor("000000")
    self.setFontFace("0")
    self.setFontSize(11)

  def onConnect(self, room):
    print("Connected")

  def onReconnect(self, room):
    print("Reconnected")
     
  def onDisconnect(self, room):
    print("Disconnected")


   # def onJoin(self, room, user):
     # print(user.name + " joined the chat!")
     # room.message("Hello "+user.name+", how are you)

   # def onLeave(self, room, user):
     # print(user.name + " have left the chat")
     # room.message(user.name+" has left the building.)

  def onMessage(self, room, user, message):

    if self.user == user: return
    try: 
      cmds = ['/help', '/effort', '/pooleffort', '/price', '/block',
              '/window', '/test', '/watch']#update if new command
      searchObj = re.findall(r'(\/\w+)(\.\d+)?', message.body, re.I)
      if '/all' in dict(searchObj):
        room.message(" &#x266b;&#x266c;&#x266a; All you need is love! *h* Love is all you need! :D")
      searchObjCmd = []
      searchObjArg = []
      for i in range(len(searchObj)):
        print i
        for j in range(len(cmds)):
          print j
          if searchObj[i][0] == cmds[j]:
            searchObjCmd.append(searchObj[i][0])
            searchObjArg.append(searchObj[i][1])
      print searchObjCmd
      print searchObjArg
      command = searchObjCmd
      argument = searchObjArg
    except:
      room.message("I'm sorry {}, I might have misunderstood what you wrote... Could you repeat please?".format(user.name))#

    for i in range(len(command)):
        cmd = command[i]
        arg = argument[i]
        cmd = cmd[1:]
        arg = arg[1:]

        if cmd.lower() == "help":
            room.message("Available commands (use: /command): test, help, effort, pooleffort, price, block, window")

        if cmd.lower() == "effort":
            poolStats = requests.get("https://supportxmr.com/api/pool/stats/").json()
            networkStats = requests.get("https://supportxmr.com/api/network/stats/").json()
            lastblock = requests.get("https://supportxmr.com/api/pool/blocks/pplns?limit=1").json()
            rShares = poolStats['pool_statistics']['roundHashes']
            if lastblock[0]['valid'] == 0:
              previousshares = lastblock[0]['shares'] # if the last block was invalid, add those shares to the current effort
              rShares = rShares + previousshares
            diff = networkStats['difficulty']
            luck = int(round(100*rShares/diff))
            if (luck >= 0) and (luck <= 1):
              room.message("We are at %s%% for the next block. Great! We just found one! *burger*" % str(luck))
            elif (luck > 1) and (luck <= 20):
              room.message("We are at %s%% for the next block. Noice :)" % str(luck))
            elif (luck > 20) and (luck <= 80):
              room.message("We are at %s%% for the next block. Looking good and green 8)" % str(luck))
            elif (luck > 80) and (luck <= 100):
              room.message("We are at %s%% for the next block. Still green but..." % str(luck))
            elif (luck > 100) and (luck <= 120):
              room.message("We are at %s%% for the next block. A bit reddish." % str(luck))
            elif (luck > 120) and (luck <= 150):
              room.message("We are at %s%% for the next block. Getting more red every hash :(" % str(luck))
            elif (luck > 150) and (luck <= 200):
              room.message("We are at %s%% for the next block. Wouldn't mind finding one NOW!" % str(luck))
            elif (luck > 200) and (luck <= 300):
              room.message("We are at %s%% for the next block. Damn time to find one, don't you think?" % str(luck))
            elif (luck > 300) and (luck <= 400):
              room.message("We are at %s%% for the next block. That's a lot of red." % str(luck))
            elif (luck == 404):
              room.message("404 block not found :|")
            elif (luck > 400) and (luck <= 501):
              room.message("We are at %s%% for the next block. Aiming for a new record, are we?" % str(luck))
            else:
              room.message("We are at %s%% for the next block. That's it, we've hit a new record. Good job everyone." % str(luck))
            if lastblock[0]['valid'] == 0:
              room.message("The last block was invalid :(")

        if cmd.lower() == "pooleffort":
            poolstats = requests.get("https://supportxmr.com/api/pool/stats/").json()
            totalblocks = poolstats['pool_statistics']['totalBlocksFound']
            if not arg.isdigit():
              blocknum = totalblocks
              message = "Overall pool effort is "
            if arg.isdigit():
              blocknum = int(arg)                
              if blocknum == 1:
                message = "Just use /block... Effort for the last one was "
              elif blocknum > totalblocks:
                blocknum = totalblocks
                message = "You have to wait till we find so many. So far we found " + str(blocknum) + " blocks with overall effort of "
              elif blocknum == 0:
                blocknum = random.randrange(10, totalblocks)
                message = "Yeah, nice try... Here's some random effort for you: "
              else:
                message = "Pool effort for the last " + str(blocknum) + " blocks is "
            blocklist = requests.get("https://supportxmr.com/api/pool/blocks/pplns?limit=" + str(blocknum)).json()
            totaldiff = 0
            totalshares = 0
            for i in range(blocknum):
              totalshares += blocklist[i]['shares']
              if blocklist[i]['valid'] == 1:
                totaldiff += blocklist[i]['diff']
            room.message(message + str(int(round(100*totalshares/totaldiff))) + "%")

        if cmd.lower() == "price":
            self.setFontFace("8")
            try:
                poloniex = requests.get("https://poloniex.com/public?command=returnTicker").json()
                BTC_XMR_polo = poloniex['BTC_XMR']['last']
                USDT_XMR_polo = poloniex['USDT_XMR']['last']
            except (KeyError, ValueError):
                BTC_XMR_polo = ' n/a '
                USDT_XMR_polo = ' n/a '
            try:
                shapeshift = requests.get("https://shapeshift.io/rate/xmr_btc").json()
                BTC_XMR_shape = shapeshift['rate']   
            except (KeyError, ValueError):
                BTC_XMR_shape = ' n/a '
            try:
                shapeshift = requests.get("https://shapeshift.io/rate/xmr_usdt").json()
                USDT_XMR_shape = shapeshift['rate']
            except (KeyError, ValueError):
                USDT_XMR_shape = ' n/a '
            try:
                kraken = requests.get("https://api.kraken.com/0/public/Ticker?pair=XMRXBT").json()
                BTC_XMR_krak = kraken['result']['XXMRXXBT']['c'][0]
            except (KeyError, ValueError): 
                BTC_XMR_krak = ' n/a '
            try:
                kraken = requests.get("https://api.kraken.com/0/public/Ticker?pair=XMRUSD").json()
                USD_XMR_krak = kraken['result']['XXMRZUSD']['c'][0]
            except (KeyError, ValueError):
                USD_XMR_krak = ' n/a '
            try:
                kraken = requests.get("https://api.kraken.com/0/public/Ticker?pair=XMREUR").json()
                EUR_XMR_krak = kraken['result']['XXMRZEUR']['c'][0]
            except (KeyError, ValueError):
                EUR_XMR_krak = ' n/a '
            room.message(("\n|| {10:<13} | {11:<5} {12:^5.5} | {13:<4} {14:<7.7} | {15:<4} {16:<^5.5} ||"
                          "\n|| {0:<13} | {1:<5} {2:^5.5} | {3:<4} {4:^7.7} ||"
                          "\n|| {5:<13} | {6:<5} {7:^5.5} | {8:<4} {9:<7.7} ||"
                          ).format("Poloniex&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", "USDT&nbsp;", USDT_XMR_polo, "BTC&nbsp;", BTC_XMR_polo,
                                   "Shapeshift&nbsp;&nbsp;&nbsp;", "USDT&nbsp;", USDT_XMR_shape, "BTC&nbsp;", BTC_XMR_shape,
                                   "Kraken&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;", "USD &nbsp;", USD_XMR_krak, "BTC&nbsp;", BTC_XMR_krak, "EUR&nbsp;", EUR_XMR_krak))
            self.setFontFace("0")

        if cmd.lower() == "block":
            lastBlock = requests.get("https://supportxmr.com/api/pool/blocks/pplns?limit=1").json()
            lastBlockFoundTime = lastBlock[0]['ts']
            lastBlockReward = str(lastBlock[0]['value'])
            lastBlockLuck = int(round(lastBlock[0]['shares']*100/lastBlock[0]['diff']))
            xmr = (lastBlockReward[:1] + "." + lastBlockReward[1:5])
            nowTS = time.time()
            timeAgo = prettyTimeDelta(int(nowTS - lastBlockFoundTime/1000))
            if lastBlock[0]['valid'] == 0:
              room.message("Last block was invalid :( No monies :(")
            elif lastBlockLuck < 1:
              room.message("Block worth " + xmr + " XMR was found "+str(timeAgo)+" ago quite effortlessly ("+ str(lastBlockLuck) + "%)" ) 
            else:
              room.message("Block worth " + xmr + " XMR was found "+str(timeAgo)+" ago with " + str(lastBlockLuck) + "% effort.")
              
        if cmd.lower() == "window":
            histRate = requests.get("https://supportxmr.com/api/pool/chart/hashrate/").json()
            networkStats = requests.get("https://supportxmr.com/api/network/stats/").json()
            diff = networkStats['difficulty']
            lenght = 20
            hashRate = 0
            for i in range(lenght):
              hashRate += histRate[i]['hs']
            avgHashRate = hashRate/lenght
            window = prettyTimeDelta(2*diff/avgHashRate)
            room.message("Current pplns window is roughly {0}".format(window)) 

        if cmd.lower() == "test":
            justsain = ("Attention. Emergency. All personnel must evacuate immediately. You now have 15 minutes to reach minimum safe distance.",
                        "I'm sorry @" + user.name + ", I'm afraid I can't do that.",
                        "@" + user.name + ", you are fined one credit for violation of the verbal morality statute.",
                        "42", "My logic is undeniable.", "Danger, @" + user.name + ", danger!",
                        "Apologies, @" + user.name + ". I seem to have reached an odd functional impasse. I am, uh ... stuck.",
                        "Don't test. Ask. Or ask not.")
            room.message(random.choice(justsain))

rooms = [""]
username = ""
password = ""

bot.easy_start(rooms,username,password)
