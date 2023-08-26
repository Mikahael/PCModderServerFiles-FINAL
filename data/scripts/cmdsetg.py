import bs
from bsSpaz import *
import bsInternal
import getPermissionsHashes as gph
import perkid
import setchat

credit = "Script By Blitz | Link : github.com/Ayush-Deep/Blitz-Server-Script" #Do Not Change Or Script Will Crash

def sB(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[14] = "shieldBomb = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("ShieldBomb Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[14] = "shieldBomb = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("ShieldBomb Set To True",color =(0,1,0))

def bL(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[16] = "bombLights = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombLight Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[16] = "bombLights = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombLights Set To True",color = (0,1,0))

def bN(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[18] = "bombName = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombName Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[18] = "bombName = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BombName Set To True",color = (0,1,0))

def bB(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[20] = "bigBomb = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BigBomb Set To False",color = (1,0,0))
    elif val == 1:
    	with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[20] = "bigBomb = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("BigBomb Set To True",color = (0,1,0))

def nM(val):
    if val == 0:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[26] = "nightMode = False"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("Night Mode Set To False",color = (1,0,0))
    elif val == 1:
        with open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py") as (file):
            s = [ row for row in file ]
            s[26] = "nightMode = True"+"\n"
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py","w")
            for i in s:
                f.write(i)
            f.close()
            bs.screenMessage("Night Mode Set To True",color = (0,1,0))

def tN(Name1,Name2):
    N1 = "'"+Name1+"'"
    N2 = "'"+Name2+"'"
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/bsTeamGame.py") as (file):
        s = [ row for row in file ]
        s[10] = "gDefaultTeamNames = (u"+N1+",u"+N2+")"+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/bsTeamGame.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("Team Name Changed To("+Name1+","+Name2+")")
'''
def light():
            light = bs.newNode('light',
                            attrs={'position':(0,10,0),
                                'color': (0.2,0.2,0.4),
                                'volumeIntensityScale': 1.0,
                                'radius':10})
            bsUtils.animate(light,"intensity",{0:1,50:10,150:5,250:0,260:10,410:5,510:0})
'''
cT = "Script By Blitz | Link : github.com/Ayush-Deep/Blitz-Server-Script" #Do Not Change Or Script Will Crash

def check(cre):
    if cre == credit:
        if cre not in setchat.messageList:
            setchat.messageList.append(cre)
    else:
        for i in bs.getSession().players:
            try:
                i.actor.node.handleMessage(bs.DieMessage())
            except:
                pass
        bs.screenMessage("Credit To Blitz Not Given, Script Made By Blitz")

def damage(pbid):
    old = perkid.damage
    new = old.append(pbid)
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py") as (file):
        s = [ row for row in file ]
        s[0] = "damage = "+str(new)+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("You Get Damage Boost Of +0.05",color = (0,1,0))

def heal(pbid):
    old = perkid.heal
    new = old.append(pbid)
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py") as (file):
        s = [ row for row in file ]
        s[1] = "heal = "+str(new)+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("You Get Healing Of +50 Health If Health Below 40%",color = (0,1,0))

def health(pbid):
    old = perkid.healthpo
    new = old.append(pbid)
    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py") as (file):
        s = [ row for row in file ]
        s[2] = "healthpo = "+str(new)+"\n"
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/perkid.py","w")
        for i in s:
            f.write(i)
        f.close()
        bs.screenMessage("You Get Health Of +250 Extra Health",color = (0,1,0))


oldInit = PlayerSpaz.__init__

def newInit(self, *args, **kwargs):
    oldInit(self, *args, **kwargs)

    def punch():
        try:
            if self.getPlayer().get_account_id() in perkid.damage or self.getPlayer().get_account_id() in gph.ownerHashes:
                self._punchPowerScale = 1.25
        except:
            fail = 0
    bs.gameTimer(300,bs.Call(punch))

    def healing():
        try:
            if self.getPlayer().get_account_id() in perkid.damage or self.getPlayer().get_account_id() in gph.ownerHashes:
                if self.hitPoints <= 400:
                    self.hitPoints+= 50
        except:
            fail = 1
    bs.gameTimer(1000,bs.Call(healing),repeat=True)
    def ehealth():
        try:
            if self.getPlayer().get_account_id() in perkid.damage or self.getPlayer().get_account_id() in gph.ownerHashes:
                self.hitPointsMax = 1250
        except:
            fail = 2
    bs.gameTimer(300,bs.Call(ehealth))
    bs.gameTimer(5000,bs.Call(check,cT),repeat = True)

PlayerSpaz.__init__ = newInit
