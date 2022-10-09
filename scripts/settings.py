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

gameTexts = ['Welcome To Blitz Server','Use "/shop commands" to see commands available to buy.','Use "/shop effects" to see effects available and their price.','Use "/me" or "/stats" to see your '+bs.getSpecialChar('ticket')+' and your stats in this server', 'Use "/buy" to buy effects that you like','Use "/donate" to give some of your tickets to other players','Use "/scoretocash" to convert some of your score to '+bs.getSpecialChar('ticket')+'\nCurrent Rate: 5scores = '+bs.getSpecialChar('ticket')+'1']

questionDelay = 90 #60 #seconds
questionsList = {'Which virus is spreading currently?': 'corona', 'Which country Corona is originated?': 'china', 'Effiel Tower is located in which city?': 'paris', 'Largest Planet in our solar system?': 'jupiter',
       'add': None, 
       'multiply': None}

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
   '/freeze': 60, 
   '/freezeall': 100, 
   '/sleep': 40, 
   '/sleepall': 80, 
   '/thaw': 50, 
   '/thawall': 70, 
   '/kill': 80, 
   '/killall': 150, 
   '/end': 100, 
   '/hug': 60, 
   '/hugall': 100, 
   '/tint': 90, 
   '/sm': 50, 
   '/fly': 50, 
   '/flyall': 100, 
   '/heal': 50, 
   '/healall': 70, 
   '/gm': 200, 
   '/custom': 250}

availableEffects = {'ice': 500, 
   'sweat': 750, 
   'scorch': 500, 
   'glow': 400, 
   'distortion': 750, 
   'slime': 500, 
   'metal': 500, 
   'surrounder': 1000}

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
