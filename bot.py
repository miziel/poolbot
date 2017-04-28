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
        room.message("Current block's luck is %s%%" % str(luck))
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
        room.message("Overall pool luck is " + str(totalshares/totaldiff*100) + "%")
    
rooms = [""]
username = ""
password = ""

bot.easy_start(rooms,username,password)
