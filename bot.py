from __future__ import division
from math import erf, sqrt
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

class bot(ch.RoomManager):
  _lastFoundBlockNum = 0
  _lastFoundBlockLuck = 0
  _lastFoundBlockValue = 0
  _lastFoundBlockTime = 0

  def getLastFoundBlockNum(self):
    try:
      poolstats = requests.get("https://supportxmr.com/api/pool/stats/").json()
      blockstats = requests.get("https://supportxmr.com/api/pool/blocks/pplns?limit=1").json()
      self._lastFoundBlockNum = poolstats['pool_statistics']['totalBlocksFound']
      self._lastFoundBlockLuck = int(round(blockstats[0]['shares']*100/blockstats[0]['diff']))
      self._lastFoundBlockValue = str(round(blockstats[0]['value']/1000000000000, 5))
      self._lastFoundBlockTime = poolstats['pool_statistics']['lastBlockFoundTime']
    except:
      pass          

  def onInit(self):
    self.setNameColor("CC6600")
    self.setFontColor("000000")
    self.setFontFace("0")
    self.setFontSize(11)
    self.getLastFoundBlockNum()          

  def onConnect(self, room):
    print("Connected")
     
  def onReconnect(self, room):
    print("Reconnected")
     
  def onDisconnect(self, room):
    print("Disconnected")

  def checkForNewBlock(self, room):
    prevBlockNum = self._lastFoundBlockNum
    prevBlockTime = self._lastFoundBlockTime
    if prevBlockNum == 0: #check for case we cant read the number
      return
    self.getLastFoundBlockNum()
    if self._lastFoundBlockNum > prevBlockNum:
      BlockTimeAgo = prettyTimeDelta(int(self._lastFoundBlockTime - prevBlockTime))
      room.message("*burger* #" + str(self._lastFoundBlockNum) + " | &#x26cf; " + str(self._lastFoundBlockLuck
) + "% | &#x23F0; " + str(BlockTimeAgo)+ " | &#x1DAC; " + self._lastFoundBlockValue)

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
              '/window', '/test', '/normalluck', '/watch']#update if new command
      searchObj = re.findall(r'(\/\w+)(\.\d+)?', message.body, re.I)
      if '/all' in searchObj:
      #  command = ['/effort', '/pooleffort', '/block', '/window' , '/price']
        room.message(" &#x266b;&#x266c;&#x266a; All you need is love! *h* Love is all you need! :D")
      searchObjCmd = []
      searchObjArg = []
      for i in range(len(searchObj)):
        #print(i) # this is for debugging I suppose, right?
        for j in range(len(cmds)):
          #print(j) # as above
          if searchObj[i][0] == cmds[j]:
            searchObjCmd.append(searchObj[i][0])
            searchObjArg.append(searchObj[i][1])
      #print(searchObjCmd) # same
      #print(searchObjArg) # same
      command = searchObjCmd
      argument = searchObjArg
    except:
      room.message("I'm sorry {}, I might have misunderstood what you wrote... Could you repeat please?".format(user.name))

    for i in range(len(command)):
        cmd = command[i]
        arg = argument[i]
        cmd = cmd[1:]
        arg = arg[1:]

        if cmd.lower() == "help":
            room.message("Available commands (use: /command): test, help, effort, pooleffort, price, block, window, normalluck")
          
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
            if rShares == 0:
              room.message("Until further notice I make 0% effort. I'm tired. Ask someone else.")
            elif (luck >= 0) and (luck <= 1):
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
            elif (luck > 300) and (luck <= 500):
              room.message("We are at %s%% for the next block. That's a lot of red." % str(luck))
            elif (luck == 404):
              room.message("404 block not found :|")
            elif (luck > 500) and (luck <= 715):
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
            if arg.isdigit(): # no need to include the case blocknum < 0, because when writing "-1" the '-' will be picked up as a non-digit first, thus triggering the previous if
              blocknum = int(arg)                
              if blocknum == 1:
                message = "Just use /block... Effort for the last one was "
              elif blocknum > totalblocks:
                blocknum = totalblocks
                message = "You have to wait till we find so many. So far we found " + str(blocknum) + " blocks, with an overall effort of "
              elif blocknum == 0:
                blocknum = random.randrange(10, totalblocks)
                message = "Yeah, nice try... Here's some random effort for you: "
              elif blocknum == totalblocks:
                message = "Overall pool effort is "
              else:
                message = "Pool effort for the last " + str(blocknum) + " blocks is "
            blocklist = requests.get("https://supportxmr.com/api/pool/blocks/pplns?limit=" + str(blocknum)).json()
            totalshares = 0
            valids = 0
            lucks = []
            # Average effort is the average of all efforts: sum of efforts / number of valid blocks.
            # Gotta walk the list in reverse, so that we go through the blocks in the order they
            # were found. Otherwise, invalids will mess up the values, since their shares would go into
            # the previous block instead of the following one.
            for i in reversed(range(blocknum)):
              totalshares += blocklist[i]['shares']
              if blocklist[i]['valid'] == 1:
                diff = blocklist[i]['diff']
                lucks.append(totalshares/diff)
                valids += 1
                totalshares = 0
              # Disregard the following if block: if the last block was invalid, it will not be taken
              # into account until a valid one is found.
              #if blocklist[blocknum]['valid'] == 0: # I'll leave this here anyway :D
                #lucks.append(totalshares/diff)
                # If the last block was invalid, temporarily pretend that it's valid and take it
                # into accound. The displayed value will be incorrect until a valid block is found.
                # Given the number of blocks found by the pool already, the impact will be negligible.
            totaleffort = sum(lucks)/valids

            room.message(message + str(int(round(100*totaleffort))) + "%")

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
            length = 20
            hashRate = 0
            for i in range(length):
              hashRate += histRate[i]['hs']
            avgHashRate = hashRate/length
            window = prettyTimeDelta(2*diff/avgHashRate)
            room.message("Current pplns window is roughly {0}".format(window))

        if cmd.lower() == "normalluck":
            poolstats = requests.get("https://supportxmr.com/api/pool/stats/").json()
            totalblocks = poolstats['pool_statistics']['totalBlocksFound']
            blocks = requests.get('https://supportxmr.com/api/pool/blocks?limit=' + str(totalblocks)).json()
            if not arg.isdigit():
              blocknum = totalblocks # the message for this case is handled in the "blocknum == totalblocks" case
              startmessage = "Compared to the average, the overall standard deviation for this pool is "
            if arg.isdigit(): # no need to include the case blocknum < 0, because when writing "-1" the '-' will be picked up as a non-digit first, thus triggering the previous if
              blocknum = int(arg)                
              if blocknum == 1:
                startmessage = "Standard deviation for the last block was "
              elif blocknum > totalblocks:
                blocknum = totalblocks
                startmessage = "You have to wait till we find so many. So far we found " + str(blocknum) + " blocks with an overall standard deviation of "
              elif blocknum == 0:
                blocknum = random.randrange(10, totalblocks)
                startmessage = "Yeah, nice try... Here's some random result for you.\nStandard deviation for the last " + str(blocknum) + " blocks was "
              elif blocknum == totalblocks:
                startmessage = "Compared to the average, the overall standard deviation for this pool is "
              else:
                startmessage = "Compared to the average, the standard deviation for the last " + str(blocknum) + " blocks is "
            # approximates the binomial distribution using a normal one, close enough ;)
            #for bl in [10, 50, None]:
            bl = blocknum
            #print(bl)
            share_sum = sum(b['shares'] for b in blocks[:bl])
            diff_sum = sum(b['diff'] for b in blocks[:bl])
#            bl = len(blocks[:bl]) # this line is useless without the for loop
            #print(bl)
            avg_diff = diff_sum / bl
            mu = share_sum / avg_diff - 0.5
            sigma2 = share_sum / avg_diff * (1 - 1 / avg_diff)
            bias = (bl - mu) / sqrt(sigma2)
            prob = (0.5 + 0.5 * erf(bias / sqrt(2)))*100
            room.message("{} {:.2f}\nProbability to be worse: {:.5f}%".format(startmessage, bias, prob))
            #room.message("blocks: %i - std deviations better than the mode: %.2f - probability to be worse: %.5f" % (bl, bias, prob))

        if cmd.lower() == "test":
            justsain = ("Attention. Emergency. All personnel must evacuate immediately. You now have 15 minutes to reach minimum safe distance.",
                        "I'm sorry @" + user.name + ", I'm afraid I can't do that.",
                        "@" + user.name + ", you are fined one credit for violation of the verbal morality statute.",
                        "42", "My logic is undeniable.", "Danger, @" + user.name + ", danger!",
                        "Apologies, @" + user.name + ". I seem to have reached an odd functional impasse. I am, uh ... stuck.",
                        "Don't test. Ask. Or ask not.", "This is my pool. There are many like it, but this one is mine!")
            room.message(random.choice(justsain))

rooms = ["testroom3"] #list rooms you want the bot to connect to
username = "poolbot2" #for tests can use your own - triger bot as anon
password = ""

bot.easy_start(rooms,username,password)
