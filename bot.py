import ch
import urllib, json

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
       room.message("Current luck is %s%%" % str(luck))
    
rooms = [""]
username = ""
password = ""

bot.easy_start(rooms,username,password)
