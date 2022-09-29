# -*- coding: utf-8 -*- 
import bs
import types
import bsInternal
import time
import threading
import fire
import getPermissionsHashes as gph
banned = list(set(gph.banlist.values()))
whitelist = list(set(gph.whitelist.values()))
old = []

class detect(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        try:
            global old
            roster = bsInternal._getGameRoster()
            if roster != old:
                #print roster
                for i in roster:
                    a = i['displayString']
                    if a in banned:
                       with bs.Context('UI'):
                           bsInternal._chatMessage(a + ", You are banned due to voilation of rules.") 
                       bsInternal._disconnectClient(int(i['clientID']))
                    if fire.whitelist:
                       if a not in whitelist:
                           with bs.Context('UI'):
                               bsInternal._chatMessage(a + ", Whitelist is turned on sir!")
                           bsInternal._disconnectClient(int(i['clientID']))
                old = roster
        except Exception as e:
            pass
        bs.realTimer(2000,self.run)
detect().start()
