import ch
import urllib, json, requests

##### TRIALS & TRIBULATIONS :)
#url1 = "https://supportxmr.com/api/pool/stats/"
#url2 = "https://supportxmr.com/api/network/stats/"
#jsonDataPool = urllib.urlopen(url1)
#jsonDataNetwork = urllib.urlopen(url2)
#jsonToPython1 = json.loads(jsonDataPool.read())
#jsonToPython2 = json.loads(jsonDataNetwork.read())
#  
#print jsonToPython1['pool_statistics']['roundHashes']
#print jsonToPython2['difficulty']
#diff = jsonToPython2['difficulty']
#rShares = jsonToPython1['pool_statistics']['roundHashes']*100
#print ("diff = ",diff)
#print ("rShares = ", rShares)
#luck = int(rShares/diff)
#print luck,"%"
  
class bot(ch.RoomManager):
  
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

  def onMessage(self, room, user, message):

    if self.user == user: return
    
    print("[{0}] {1}: {2}".format(room.name, user.name, message.body))
    
    try:
      cmd, args = message.body.split(" ", 1)
    except:
      cmd, args = message.body, ""
      
    if cmd[0] == "/":
      prfx = True
      cmd = cmd[1:]
    else:
      prfx = False
      
    if cmd.lower() == "luck" and prfx:
        url1 = "https://supportxmr.com/api/pool/stats/"
        url2 = "https://supportxmr.com/api/network/stats/"
        jsonDataPool = urllib.urlopen(url1)
        jsonDataNetwork = urllib.urlopen(url2)
        jsonToPython1 = json.loads(jsonDataPool.read())
        jsonToPython2 = json.loads(jsonDataNetwork.read())
        rShares = jsonToPython1['pool_statistics']['roundHashes']*100
        diff = jsonToPython2['difficulty']
        luck = int(rShares/diff)
        if (luck > 0) and (luck <= 1):
          room.message("Current block's luck is %s%% - seems like we just found one! *burger*" % str(luck))
        elif (luck > 1) and (luck <= 20):
          room.message("Current block's luck is %s%% - nice and low :)" % str(luck))
        elif (luck > 20) and (luck <= 80):
          room.message("Current block's luck is %s%% - looking good and green 8)" % str(luck))
        elif (luck > 80) and (luck <= 100):
          room.message("Current block's luck is %s%% - still green but..." % str(luck))
        elif (luck > 100) and (luck <= 120):
          room.message("Current block's luck is %s%% - a bit reddish." % str(luck))
        elif (luck > 120) and (luck <= 150):
          room.message("Current block's luck is %s%% - getting more red every hash :(" % str(luck))
        elif (luck > 150) and (luck <= 200):
          room.message("Current block's luck is %s%% - wouldn't mind finding one NOW!" % str(luck))
        elif (luck > 200) and (luck <= 300):
          room.message("Current block's luck is %s%% - damn time to find one, don't you think?" % str(luck))
        elif (luck > 300) and (luck <= 400):
          room.message("Current block's luck is %s%% - that's a lot of red." % str(luck))
        else:
          room.message("Current block's luck is %s%% - aiming for a new record, are we?" % str(luck))
    if cmd.lower() == "poolluck" and prfx:
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
        room.message("Overall pool luck is " + str(totalshares*100/totaldiff) + "%")
    if cmd.lower() == "price" and prfx: 
        poloniex = requests.get("https://poloniex.com/public?command=returnTicker").json()
        BTC_XMR_polo = poloniex['BTC_XMR']['last']
        USDT_XMR_polo = poloniex['USDT_XMR']['last']
        cryptocompare = requests.get("https://min-api.cryptocompare.com/data/price?fsym=XMR&tsyms=BTC,USD").json()
        BTC_XMR_cc = cryptocompare['BTC']
        USD_XMR_cc = cryptocompare['USD']
        room.message("|| Poloniex | BTC {0} | USDT {1} || Cryptocompare | BTC {2} | USD {3} ||".format(BTC_XMR_polo[0:7], USDT_XMR_polo[0:5], BTC_XMR_cc, USD_XMR_cc))

rooms = [""] #list rooms you want the bot to connect to
username = "" #for tests can use your own - triger bot as anon
password = ""

bot.easy_start(rooms,username,password)
