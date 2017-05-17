import ch
import urllib
import json
import requests
import random
import time
import re

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

class BackgroundTimer(Thread):
  def run(self):
    while 1:
      Time.sleep(60)
      poolStats = requests.get("https://supportxmr.com/api/pool/stats/").json()
      networkStats = requests.get("https://supportxmr.com/api/network/stats/").json()
      rShares = poolStats['pool_statistics']['roundHashes']
      diff = networkStats['difficulty']
      effort = int(100*rShares/diff)
      if (effort >= 0) and (effort <= 1):
        room.message("*burger*")

  def onInit(self):
    self.setNameColor("505050")
    self.setFontColor("000000")
    self.setFontFace("Arial")
    self.setFontSize(11)

  def onConnect(self, room):
    print("Connected")

  def onReconnect(self, room):
    print("Reconnected")

  def onDisconnect(self, room):
    print("Disconnected")

rooms = [""] #list rooms you want the bot to connect to
username = "" #for tests can use your own - triger bot as anon
password = ""
bot.easy_start(rooms,username,password)

class bot(ch.RoomManager):

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
    self.reconnect()

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
              '/window', '/test']#update if new command
      searchObj = re.findall(r'(/\w+)', message.body, re.I)
      if '/all' in searchObj:
        command = ['/effort', '/pooleffort', '/block', '/window' , '/price']
      elif searchObj:
        if '/luck' in searchObj and user.name == 'm5m400':
          searchObj[searchObj.index('/luck')] = '/effort'
          command = list(set(cmds) & set(searchObj))
          command.reverse()
        else:
          command = list(set(cmds) & set(searchObj))
          command.reverse()
      else:
        command = []
    except:
      room.message("I'm sorry {}, I might have misunderstood what you wrote... Could you repeat please?".format(user.name))

    for i in range(len(command)):
        cmd = command[i]

    #    try:
    #      cmd, args = message.body.split(" ", 1)
    #    except:
    #      cmd, args = message.body, ""

        try:
            if cmd[0] == "/":
                prfx = True
                cmd = cmd[1:]
            else:
                prfx = False
        except:
            room.message("I'm sorry, I might have a reading problem... Could you please repeat that @{}?".format(user.name))

        if cmd.lower() == "help" and prfx:
            room.message("Available commands (use: /command): test, help, effort, pooleffort, price, block, window")
          
        if cmd.lower() == "effort" and prfx:
            poolStats = requests.get("https://supportxmr.com/api/pool/stats/").json()
            networkStats = requests.get("https://supportxmr.com/api/network/stats/").json()
            rShares = poolStats['pool_statistics']['roundHashes']
            diff = networkStats['difficulty']
            luck = int(100*rShares/diff)
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
            else:
              room.message("We are at %s%% for the next block. Aiming for a new record, are we?" % str(luck))

        if cmd.lower() == "pooleffort" and prfx:
            poolstats = requests.get("https://supportxmr.com/api/pool/stats/").json()
            blocknum = poolstats['pool_statistics']['totalBlocksFound']
            blocklist = requests.get("https://supportxmr.com/api/pool/blocks/pplns?limit=" + str(blocknum)).json()
            totaldiff = 0
            totalshares = 0
            startingblock = 1  # number of the starting block from which to scan the list
            for i in reversed(range(0, blocknum-startingblock+1)): 
              totalshares += blocklist[i]['shares']
              if blocklist[i]['valid'] == 1:
                totaldiff += blocklist[i]['diff']
            room.message("Overall pool effort is " + str(100*totalshares/totaldiff) + "%")

        if cmd.lower() == "price" and prfx:
            self.setFontFace("8")
            poloniex = requests.get("https://poloniex.com/public?command=returnTicker").json()
            BTC_XMR_polo = poloniex['BTC_XMR']['last']
            USDT_XMR_polo = poloniex['USDT_XMR']['last']
            cryptocompare = requests.get("https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=BTC,USD").json()
            BTC_XMR_cc = cryptocompare['BTC']
            USD_XMR_cc = cryptocompare['USD']
            try:
                shapeshift = requests.get("https://shapeshift.io/rate/xmr_btc").json()
                BTC_XMR_shape = shapeshift['rate']   
            except KeyError:
                BTC_XMR_shape = ' n/a '
            try:
                shapeshift = requests.get("https://shapeshift.io/rate/xmr_usdt").json()
                USDT_XMR_shape = shapeshift['rate']
            except KeyError:
                USDT_XMR_shape = ' n/a '
            kraken = requests.get("https://api.kraken.com/0/public/Ticker?pair=XMRXBT").json()
            BTC_XMR_krak = kraken['result']['XXMRXXBT']['c'][0]
            kraken = requests.get("https://api.kraken.com/0/public/Ticker?pair=XMRUSD").json()
            USD_XMR_krak = kraken['result']['XXMRZUSD']['c'][0]
            kraken = requests.get("https://api.kraken.com/0/public/Ticker?pair=XMREUR").json()
            EUR_XMR_krak = kraken['result']['XXMRZEUR']['c'][0]
            room.message(("\n|| {10:<10} | {11:<5} {12:^5.5} | {13:<4} {14:^7.7} | {15:<4} {16:<^5.5} ||"
                          "\n|| {0:<10} | {1:<5} {2:^5.5} | {3:<4} {4:^7.7} ||"
                          "\n|| {5:<10} | {6:<5} {7:^5.5} | {8:<4} {9:^7.7} ||"
                          ).format("Poloniex&nbsp;&nbsp;", "USDT ", USDT_XMR_polo, "BTC&nbsp;", BTC_XMR_polo,
                                   "Shapeshift", "USDT ", USDT_XMR_shape, "BTC&nbsp;", BTC_XMR_shape,
                                   "Kraken&nbsp;&nbsp;&nbsp;&nbsp;", "USD &nbsp;", USD_XMR_krak, "BTC&nbsp;", BTC_XMR_krak, "EUR&nbsp;", EUR_XMR_krak))
            self.setFontFace("0")

        if cmd.lower() == "block" and prfx:
            lastBlock = requests.get("https://supportxmr.com/api/pool/blocks/pplns?limit=1").json()
            lastBlockFoundTime = lastBlock[0]['ts']
            lastBlockReward = str(lastBlock[0]['value'])
            lastBlockLuck = int(lastBlock[0]['shares']*100/lastBlock[0]['diff'])
            xmr = (lastBlockReward[:1] + "." + lastBlockReward[1:5])
            nowTS = time.time()
            timeAgo = prettyTimeDelta(int(nowTS - lastBlockFoundTime/1000))
            if lastBlockLuck < 1:
              room.message("Block worth " + xmr + " XMR was found "+str(timeAgo)+" ago quite efortlessly ("+ str(lastBlockLuck) + "%)" ) 
            else:
              room.message("Block worth " + xmr + " XMR was found "+str(timeAgo)+" ago with " + str(lastBlockLuck) + "% effort.")
              
        if cmd.lower() == "window" and prfx:
            histRate = requests.get("https://supportxmr.com/api/pool/chart/hashrate/").json()
            networkStats = requests.get("https://supportxmr.com/api/network/stats/").json()
            diff = networkStats['difficulty']
            l = len(histRate)
            hashRate = 0
            for i in range(l):
              hashRate += histRate[i]['hs']
            avgHashRate = hashRate/l
            window = prettyTimeDelta(2*diff/avgHashRate)
            room.message("Current payout window is roughly {0}".format(window)) 

        if cmd.lower() == "test" and prfx:
            justsain = ("Attention. Emergency. All personnel must evacuate immediately. You now have 15 minutes to reach minimum safe distance.",
                        "I'm sorry @" + user.name + ", I'm afraid I can't do that.",
                        "@" + user.name + ", you are fined one credit for violation of the verbal morality statute.",
                        "42", "My logic is undeniable.", "Danger, @" + user.name + ", danger!",
                        "Apologies, @" + user.name + ". I seem to have reached an odd functional impasse. I am, uh ... stuck.",
                        "Don't test. Ask. Or ask not.")
            room.message(random.choice(justsain))

rooms = [""] #list rooms you want the bot to connect to
username = "" #for tests can use your own - triger bot as anon
password = ""

timer = BackgroundTimer()
timer.start()
bot.easy_start(rooms,username,password)
