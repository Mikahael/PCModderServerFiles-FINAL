import bs
from datetime import datetime
date = datetime.now().strftime('%d')
#dont REMOVE any of the settings.
#
enableTop5effects = True
enableTop5commands = False
enableCoinSystem = True
ownerPerk = False
muteAll = False
enableVerification = False

enableStats = True

print('Enable Stats: ', enableStats)
#More Settings On setchat.py
spamProtection=True

shieldBomb = True #shield on bomb

bombLights = True #light on bomb

bombName = True #name on bomb

bigBomb = False #hehe extra

k_msg = False #Killing Message

k_pop = True #Killing Message PopUp

nightMode = True

enableChatFilter = True

showTextsInBottom = False

coinTexts = ['Welcome to Vortex Official','Use "/shop commands" to see commands available to buy.','Use "/shop effects" to see effects available and their price.','Use "/me" or "/stats" to see your '+bs.getSpecialChar('ticket')+' and your stats in this server', 'Server modded by PCMODDER and Vortex']

questionDelay = 60 #60 #seconds
questionsList = {'Who is the owner of Server?': 'vortex', 'Who modded the server?': 'pcmodder','What language does bombsquad run on?': 'python','What is easy to get into but hard to get out of?': 'trouble', "If you don't keep me, I'll break. What am I?" : 'promise', 'What do you call a bear without ears?' : 'b', 'What is the largest planet in our solar system?' : 'jupiter', 'add': None, 'multiply': None}

availableCommands = {'/nv': 50, 
   '/ooh': 5, 
   '/playSound': 10, 
   '/box': 30, 
   '/boxall': 60, 
   '/spaz': 50, 
   '/spazall': 100, 
   '/inv': 40, 
   '/invall': 80, 
   '/tex': 20, 
   '/texall': 40, 
   '/freeze': 600, 
   '/freezeall': 1000, 
   '/sleep': 400, 
   '/sleepall': 800, 
   '/thaw': 500, 
   '/thawall': 700, 
   '/kill': 800, 
   '/killall': 1500, 
   '/end': 250, 
   '/hug': 60, 
   '/hugall': 100, 
   '/tint': 190, 
   '/sm': 100, 
   '/fly': 50, 
   '/flyall': 1000, 
   '/heal': 150, 
   '/healall': 170, 
   '/gm': 1200, 
   '/custom': 250}

availableEffects = {'ice': 50, 
   'sweat': 75, 
   'scorch': 50, 
   'glow': 40, 
   'distortion': 70, 
   'slime': 50, 
   'metal': 50, 
   'surrounder': 100}

nameOnPowerUps = True  # Whether or not to show the powerup's name on top of powerups

shieldOnPowerUps = True  # Whether or not to add shield on powerups

discoLightsOnPowerUps = True  # Whether or not to show disco lights on powerup's location

FlyMaps = False  # Whether or not to enable the 3D flying maps in games playlist

floater = False

auto_night = True

def return_yielded_game_texts():
    for text in gameTexts:
        yield text


def return_players_yielded(bs):
    for player in bs.getSession().players:
        yield player
