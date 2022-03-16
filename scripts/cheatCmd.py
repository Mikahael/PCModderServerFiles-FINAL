# -*- coding: utf-8 -*-
#https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
#alot of the work has been done by PCModder
import bs
import bsInternal
import bsPowerup
import bsUtils
import random
import membersID as MID
import BuddyBunny
import os
import threading
import json
import fire
import settings




class cheatOptions(object):
    def __init__(self):
        self.all = True # just in case
       
        
        self.tint = None # needs for /nv
    
    def checkOwner(self,clientID): 
       
        client='kuchbhi'
        
        for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
        if client in MID.owners: 
            bs.screenMessage('Command Accepted',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
            
        else:
            bs.screenMessage('Command Denied',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))

    def checkMod(self,clientID): 
       
        client='kuchbhi'
        
        for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
        if client in MID.mods or client in MID.mod2 or client in MID.owners: 
            bs.screenMessage('Command Accepted',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
            
        else:
            bs.screenMessage('Command Denied',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
        

    def checkMember(self,clientID): 
       client='kuchbhi'
        
       for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
       if client in MID.mods or client in MID.members  or client in MID.vips or client in MID.owners or client in MID.mod2 or client in MID.vip2:   #member,vip,admin will have access
            bs.screenMessage('Command Accepted',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
           
       else:
            bs.screenMessage('Command Denied',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))

      
    def checkVip(self,clientID):
        client='kuchbhi'
        
        for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
        if client in MID.mods or client in MID.vips or  client in MID.owners or client in MID.mod2 or client in MID.vip2:         #only admin and vip can access
            bs.screenMessage('Command Accepted',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
            
        else:
            bs.screenMessage('Command Denied',color=(2,1,4), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))

    def kickByNick(self,nick):
        roster = bsInternal._getGameRoster()
        for i in roster:
            try:
                if i['players'][0]['nameFull'].lower().find(nick.encode('utf-8').lower()) != -1:
                    bsInternal._disconnectClient(int(i['clientID']))
            except:
                pass
      #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
    def opt(self,clientID,msg):
        nick=clientID
        if True:
            m = msg.split(' ')[0] # command
            a = msg.split(' ')[1:] # arguments
            
            activity = bsInternal._getForegroundHostActivity()
            with bs.Context(activity):
                if m == '/kick':
                    if self.checkMod(clientID):
                        if a == []:
                            bs.screenMessage('kick using name of clientID',color=(0,1,0), clients=[clientID], transient=True)
                        else:
                            if len(a[0]) > 3:
                                if(self.checkOwner(nick)!=True):
                                    
                                    self.kickByNick(a[0])
                                else:
                                    bs.screenMessage('cant kick owner',color=(1,0,0), clients=[clientID], transient=True)   
                            else:
                                try:
                                    

                                    s = int(a[0])
                                    for cl in bsInternal._getForegroundHostSession().players:
                                        if(cl.getInputDevice().getClientID()==s):
                                            accountid=cl.get_account_id()
  #defend your self from dhokebaaz admins......  
                                    if accountid in MID.owners:
                                        bs.screenMessage('cant kick owner',color=(1,0,0), clients=[clientID], transient=True)
                                    else:    
                                        
                                        bsInternal._disconnectClient(int(a[0]))
                                except:
                                    self.kickByNick(a[0])
                   
                elif m == '/getlost':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Using: /kick name or number of list')
                        else:
                            if len(a[0]) > 3:
                                self.kickByNick(a[0])
                            else:
                                try:
                                    s = int(a[0])
                                    bsInternal._disconnectClient(int(a[0]))
                                except:
                                    self.kickByNick(a[0])
                elif m == '/lister':     #Terible doesnt work, i have added better one. PCModder
                    if self.checkMember(nick):
                        bs.screenMessage('========For kick=======',color=(1,0,0), clients=[clientID], transient=True)
                        for i in bsInternal._getGameRoster():
                            try:
                                def delay():
                                    bs.screenMessage(i['players'][0]['nameFull'].encode('utf-8') + "     (/kick " + str(i['clientID'])+")",color=(1,0.4,0), clients=[clientID], transient=True)
                                bs.gameTimer(500,bs.Call(delay))
                                
                            except:
                                pass
                        bs.screenMessage('=================',color=(1,0,0), clients=[clientID], transient=True)
                        bs.screenMessage('========For Other Commands=======',color=(1,0.6,0.4), clients=[clientID], transient=True)
                        for s in bsInternal._getForegroundHostSession().players:
                            bs.screenMessage(s.getName() + "     "+ str(bsInternal._getForegroundHostSession().players.index(s)),color=(0.5,0.7,0.3), clients=[clientID], transient=True)
                elif m == '/ooh':
                    if a is not None and len(a) > 0:
                        s = int(a[0])
                        def oohRecurce(c):
                            bs.playSound(bs.getSound('ooh'),volume = 2)
                            c -= 1
                            if c > 0:
                                bs.gameTimer(int(a[1]) if len(a) > 1 and a[1] is not None else 1000,bs.Call(oohRecurce,c=c))
                        oohRecurce(c=s)
                    else:
                        bs.playSound(bs.getSound('ooh'),volume = 2)
                            
                elif m=='/me':
                    if a==[]:
                        playeraccountid=''   #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                        playername=''
                        for i in bsInternal._getForegroundHostActivity().players:
                
                            if i.getInputDevice().getClientID()==clientID:
                                
                                playeraccountid=i.get_account_id()
                                playername=i.getName()
                    else:
                        playeraccountid=''   #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                        playername=''
                        for i in bsInternal._getForegroundHostActivity().players:
                
                            if i.getInputDevice().getClientID()==int(a[0]):
                                
                                playeraccountid=i.get_account_id()
                                playername=i.getName()
                    if os.path.exists('stats.json'):
                        while True:
                            try:
                                with open('stats.json') as f:
                                    stats = json.loads(f.read())
                                    break
                            except Exception as (e):
                                print e
                                time.sleep(0.05)
                    else:
                        stats = {}
                    if playeraccountid not in stats:
                        bs.screenMessage('Not played any match yet',color=(0,1,1),clients=[clientID],transient=True)
                    else:    
                        killed=stats[playeraccountid]['killed']
                        kills=stats[playeraccountid]['kills']
                        
                        bs.screenMessage(playername+':'+' Kills:'+str(kills)+', Killed:'+str(killed)+', Matches:'+str(stats[playeraccountid]['played']),color=(0,1,1),clients=[clientID],transient=True)
                

                elif m == '/owner':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.owners
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.owners:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[5] = 'owners = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

                elif m == '/nooby':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.nooby
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.nooby:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[3] = 'nooby = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy


                elif m == '/vip2':#mod with no tag
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.vip2
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.vip2:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[42] = 'vip2 = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy


                elif m == '/mod2':#mod with no tag
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.mod2
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.mod2:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[41] = 'mod2 = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy


                elif m == '/ftrail':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.firetrail
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.firetrail:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[38] = 'firetrail = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                            
                elif m == '/strail':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.sparktrail
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.sparktrail:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[36] = 'sparktrail = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                            
                elif m == '/sltrail':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.slimetrail
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.slimetrail:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[37] = 'slimetrail = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                            
                elif m == '/wtrail':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.woodtrail
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.woodtrail:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[39] = 'woodtrail = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy


                elif m == '/mute':
                    if self.checkMod(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.muted
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.muted:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[7] = 'muted = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy


                elif m == '/mod':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.mods
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.mods:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[1] = 'mods = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                            
                elif m == '/white':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.whitelist
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.whitelist:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[6] = 'whitelist = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                            
                elif m == '/reject':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.rejected
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin +'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.rejected:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[8] = 'rejected = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

                elif m == '/vip':
                    if self.checkMod(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.vips
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.vips:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[2] = 'vips = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass                            
                elif m == '/btag':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.bombTag
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.bombTag:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[21] = 'bombTag = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/htag':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.helmetTag
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.helmetTag:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[20] = 'helmetTag = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/colortag':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.colorEffect
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.colorEffect:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[15] = 'colorEffect = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/ice':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.iceEffect
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.iceEffect:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[14] = 'iceEffect = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 

                elif m == '/smoke':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.smokeEffect
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.smokeEffect:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[13] = 'smokeEffect = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/light':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.lightEffect
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.lightEffect:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[16] = 'lightEffect = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/glow':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.glowEffect
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.glowEffect:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[17] = 'glowEffect = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/ctag':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.crownTag
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.crownTag:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[18] = 'crownTag = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/dtag':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.dragonTag
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.dragonTag:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[19] = 'dragonTag = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                            
                elif m == '/member':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.members
                        for client in bsInternal._getGameRoster():
                            if client['clientID']==clID:
                                cl_str = client['displayString']

                        for i in bsInternal._getForegroundHostActivity().players:
            
                            if i.getInputDevice().getClientID()==clID:
                                newadmin=i.get_account_id()       
                                if a[1] == 'add':
                                    
                                    updated_admins.append(newadmin)
                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersidlogged.txt",mode='a') as fi:
                                        fi.write(cl_str +' || '+newadmin+'\n')
                                        fi.close()
                                elif a[1] == 'remove':
                                   
                                    if newadmin in MID.members:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[4] = 'members = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass 
                elif m == '/playSound':
                    if a is not None and len(a) > 1:
                        s = int(a[1])
                        def oohRecurce(c):
                            bs.playSound(bs.getSound(str(a[0])),volume = 2)
                            c -= 1
                            if c > 0:
                                bs.gameTimer(int(a[2]) if len(a) > 2 and a[2] is not None else 1000,bs.Call(oohRecurce,c=c))
                        oohRecurce(c=s)
                    else:
                        bs.playSound(bs.getSound(str(a[0])),volume = 2)
                elif m == '/quit':
                    if self.checkOwner(nick):
                        bsInternal.quit()
                elif m == '/nv':
                    if self.tint is None:
                        self.tint = bs.getSharedObject('globals').tint
                    bs.getSharedObject('globals').tint = (0.5,0.7,1) if a == [] or not a[0] == u'off' else self.tint

                elif m == '/freeze': #shield
                    if self.checkVip(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /freeze all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.FreezeMessage())
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.actor.node.handleMessage(bs.FreezeMessage())
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.FreezeMessage())
                                 except Exception:
                                     bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)


                elif m == '/thaw': #shield
                    if self.checkVip(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /thaw all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.ThawMessage())
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.actor.node.handleMessage(bs.ThawMessage())
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.ThawMessage())
                                     #bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                                 except Exception:
                                     bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)

       
                
                elif m == '/kill': #shield
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /kill all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.DieMessage())
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.actor.node.handleMessage(bs.DieMessage())
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.DieMessage())
                                     #bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                                 except Exception:
                                     bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)


                elif m == '/curse': #shield
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /curse all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.curse()
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.actor.curse()
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].actor.curse()
                                     #bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                                 except Exception:
                                     bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)
          

                elif m == '/box':
                    if a == []:
                        
                        bs.screenMessage('Using: /box all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        try:
                            if a[0] == 'all':
                                if self.checkVip(nick):
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.torsoModel = bs.getModel("tnt")
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.colorMaskTexture= bs.getTexture("tnt")
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.colorTexture= bs.getTexture("tnt")
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.highlight = (1,1,1)
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.color = (1,1,1)
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.headModel = None
                                        except:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.style = "cyborg"
                                        except:
                                            pass
                            else:
                                n = int(a[0])
                                bs.getSession().players[n].actor.node.torsoModel = bs.getModel("tnt"); 
                                bs.getSession().players[n].actor.node.colorMaskTexture= bs.getTexture("tnt"); 
                                bs.getSession().players[n].actor.node.colorTexture= bs.getTexture("tnt") 
                                bs.getSession().players[n].actor.node.highlight = (1,1,1); 
                                bs.getSession().players[n].actor.node.color = (1,1,1); 
                                bs.getSession().players[n].actor.node.headModel = None; 
                                bs.getSession().players[n].actor.node.style = "cyborg";
                        except:
                           pass
                          
                
                elif m == '/mine':
                    if a == []:
                        
                        bs.screenMessage('Using: /mine all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        try:
                            if a[0] == 'all':
                                if self.checkVip(nick):
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.torsoModel = bs.getModel("landMine")
                                        except Exception:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.colorMaskTexture= bs.getTexture("landMine")
                                        except Exception:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.colorTexture= bs.getTexture("landMine")
                                        except Exception:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.highlight = (1,1,1)
                                        except Exception:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.color = (1,1,1)
                                        except Exception:
                                            pass
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.headModel = None
                                        except Exception:
                                            pass 
                                    for i in bs.getSession().players:
                                        try:
                                            i.actor.node.style = "cyborg"
                                        except Exception:
                                            pass 
                            else:
                                n = int(a[0])
                                bs.getSession().players[n].actor.node.torsoModel = bs.getModel("landMine"); 
                                bs.getSession().players[n].actor.node.colorMaskTexture= bs.getTexture("landMine"); 
                                bs.getSession().players[n].actor.node.colorTexture= bs.getTexture("landMine") 
                                bs.getSession().players[n].actor.node.highlight = (1,1,1); 
                                bs.getSession().players[n].actor.node.color = (1,1,1); 
                                bs.getSession().players[n].actor.node.headModel = None; 
                                bs.getSession().players[n].actor.node.style = "cyborg";
                        except:
                           pass           

                elif m == '/headless':   #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                    if a == []:
                        
                        bs.screenMessage('Using: /headless all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        if a[0]=='all':
                            for i in bs.getActivity().players:
                                try:
                                    if i.actor.exists():
                                       i.actor.node.headModel = None
                                       i.actor.node.style = "cyborg"
                                except Exception:
                                    pass
                                

                        elif len(a[0]) > 2:
                           for i in bs.getActivity().players:
                               try:
                                   if (i.getName()).encode('utf-8') == (a[0]):
                                      if i.actor.exists():
                                         i.actor.node.headModel = None
                                         i.actor.node.style = "cyborg"
                               except Exception:
                                   pass
                           bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))

                        else:
                             try:
                                 bs.getActivity().players[int(a[0])].actor.node.headModel = None
                                 bs.getActivity().players[int(a[0])].actor.node.style = "cyborg"
                                 bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                             except Exception:
                                bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)
    
                elif m == '/shield': #shield
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /shield all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'shield'))
                                           bsInternal._chatMessage('shield will give you Protection')
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'shield'))
                                             bsInternal._chatMessage('shield will give you Protection')
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'shield'))
                                     bsInternal._chatMessage('shield will give you Protection')
                                     bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                                 except Exception:
                                     bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)
                                 
                elif m == '/celebrate': #celebrate him
                    if a == []:
                       
                        bs.screenMessage('Using: /celebrate all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        if a[0]=='all':
                            for i in bs.getActivity().players:
                                try:
                                    if i.actor.exists():
                                       i.actor.node.handleMessage('celebrate', 30000)
                                except Exception:
                                    pass

                        elif len(a[0]) > 2:
                           for i in bs.getActivity().players:
                               try:
                                   if (i.getName()).encode('utf-8') == (a[0]):
                                      if i.actor.exists():
                                         i.actor.node.handleMessage('celebrate', 30000)
                               except Exception:
                                   pass
                                   
                        else:
                             try:
                                 bs.getActivity().players[int(a[0])].actor.node.handleMessage('celebrate', 30000)
                                 bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                             except Exception:
                                bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)
                      
                elif m == '/remove': #shield
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /remove all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.removeFromGame()
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.removeFromGame()
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].removeFromGame()
                                     bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                                 except Exception:
                                     bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)
   
                elif m == '/end':
                    if self.checkMod(nick):
                        try:
                            bsInternal._getForegroundHostActivity().endGame()
                        except:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                elif m == '/hug':
                    if a == []:
                        
                        bs.screenMessage('Using: /hug all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        try:
                            if a[0] == 'all':
                                if self.checkMod(nick):
                                    try:
                                        bsInternal._getForegroundHostActivity().players[0].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[1].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity().players[1].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[0].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity().players[3].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[2].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity().players[4].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[3].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity().players[5].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[6].actor.node
                                    except:
                                        pass
                                    try:
                                        bsInternal._getForegroundHostActivity().players[6].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[7].actor.node
                                    except:
                                        pass
                            else:
                                bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[int(a[1])].actor.node
                        except:
                            pass
                elif m == '/gm':
                    if self.checkOwner(nick):
                        if a == []:
                            for i in range(len(activity.players)):   #removed punch and shield ...no need as you are already invicible
                                if activity.players[i].getName().encode('utf-8').find(nick.encode('utf-8').replace('...','').replace(':','')) != -1:
                                    activity.players[i].actor.node.hockey = activity.players[i].actor.node.hockey == False
                                    activity.players[i].actor.node.invincible = activity.players[i].actor.node.invincible == False
                                    activity.players[i].actor._punchPowerScale = 5 if activity.players[i].actor._punchPowerScale == 1.2 else 1.2
                        else:
                            activity.players[int(a[0])].actor.node.hockey = activity.players[int(a[0])].actor.node.hockey == False
                            activity.players[int(a[0])].actor.node.invincible = activity.players[int(a[0])].actor.node.invincible == False
                            activity.players[int(a[0])].actor._punchPowerScale = 5 if activity.players[int(a[0])].actor._punchPowerScale == 1.2 else 1.2
                                 

                elif m == '/tint':
                    #if self.checkVip(nick):
                        if a == []:
                            k = ('Using: /tint R G B')
                            b = ('OR')
                            c = ('Using: /tint r bright speed')
                            bs.screenMessage(a,color=(1,1,1), clients=[clientID], transient=True)
                            bs.screenMessage(b,color=(1,1,1), clients=[clientID], transient=True)
                            bs.screenMessage(c,color=(1,1,1), clients=[clientID], transient=True)


                        else:
                            if a[0] == 'r':
                                m = 1.3 if a[1] is None else float(a[1])
                                s = 1000 if a[2] is None else float(a[2])
                                bsUtils.animateArray(bs.getSharedObject('globals'), 'tint',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(0,0,1*m),s*3:(1*m,0,0)},True)
                            else:
                                try:
                                    if a[1] is not None:
                                        bs.getSharedObject('globals').tint = (float(a[0]),float(a[1]),float(a[2]))
                                    else:
                                        bs.screenMessage('Error',color=(1,1,1), clients=[clientID], transient=True)

                                except:
                                    bs.screenMessage('Error',color=(1,1,1), clients=[clientID], transient=True)

                    
                elif m == '/sm':
                    if self.checkMod(nick):
                        bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion == False
                       
                


                elif m == '/spaz':
                    if a == []:
                        
                        bs.screenMessage('Using: /spaz all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        try:
                            if a[0] == 'all': #mr.smoothy
                                if self.checkVip(nick):
                                    if a[1] in ['ali','agent','bunny','cyborg','pixie','robot','alien','witch','wizard','bones','zoe']:
                                        for i in bs.getSession().players:
                                            t = i.actor.node
                                            try:
                                               
                                                t.colorTexture = bs.getTexture(a[1]+"Color")
                                                t.colorMaskTexture = bs.getTexture(a[1]+"ColorMask")
                                                
                                                t.headModel =     bs.getModel(a[1]+"Head")
                                                t.torsoModel =    bs.getModel(a[1]+"Torso")
                                                t.pelvisModel =   bs.getModel(a[1]+"Pelvis")
                                                t.upperArmModel = bs.getModel(a[1]+"UpperArm")
                                                t.foreArmModel =  bs.getModel(a[1]+"ForeArm")
                                                t.handModel =     bs.getModel(a[1]+"Hand")
                                                t.upperLegModel = bs.getModel(a[1]+"UpperLeg")
                                                t.lowerLegModel = bs.getModel(a[1]+"LowerLeg")
                                                t.toesModel =     bs.getModel(a[1]+"Toes")
                                                t.style = a[1]
                                            except:
                                                pass

                                    else:
                                        a = ('use ali,agent,bunny,cyborg,pixie,robot')
                                        b = ('alien,witch,wizard,bones,zoe')
                                        bs.screenMessage(a+b,color=(1,1,1), clients=[clientID], transient=True)

                            else:
                                if a[1] in ['ali','agent','bunny','cyborg','pixie','robot','alien','witch','wizard','bones','santa','zoe']:
                                    n = int(a[0])
                                    t = bs.getSession().players[n].actor.node
                                    t.colorTexture = bs.getTexture(a[1]+"Color")
                                    t.colorMaskTexture = bs.getTexture(a[1]+"ColorMask")
                                            
                                    t.headModel =     bs.getModel(a[1]+"Head")
                                    t.torsoModel =    bs.getModel(a[1]+"Torso")
                                    t.pelvisModel =   bs.getModel(a[1]+"Pelvis")
                                    t.upperArmModel = bs.getModel(a[1]+"UpperArm")
                                    t.foreArmModel =  bs.getModel(a[1]+"ForeArm")
                                    t.handModel =     bs.getModel(a[1]+"Hand")
                                    t.upperLegModel = bs.getModel(a[1]+"UpperLeg")
                                    t.lowerLegModel = bs.getModel(a[1]+"LowerLeg")
                                    t.toesModel =     bs.getModel(a[1]+"Toes")
                                    t.style = a[1]
                        except:
                           pass

                elif m == '/inv':
                    if a == []:
                        
                        bs.screenMessage('Using: /inv all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        try:
                            if a[0] == 'all':
                                if self.checkVip(nick):
                                    for i in bs.getSession().players:
                                        t = i.actor.node
                                        try:
                                           
                                              #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                                            t.headModel =     None
                                            t.torsoModel =    None
                                            t.pelvisModel =   None
                                            t.upperArmModel = None
                                            t.foreArmModel =  None
                                            t.handModel =     None
                                            t.upperLegModel = None
                                            t.lowerLegModel = None
                                            t.toesModel =     None
                                            t.style = "cyborg"
                                        except:
                                            pass
                            else:
                                n = int(a[0])
                                t = bs.getSession().players[n].actor.node
                                                                        
                                t.headModel =     None
                                t.torsoModel =    None
                                t.pelvisModel =   None
                                t.upperArmModel = None
                                t.foreArmModel =  None
                                t.handModel =     None
                                t.upperLegModel = None
                                t.lowerLegModel = None
                                t.toesModel =     None
                                t.style = "cyborg"
                        except:
                           pass
                elif m == '/cameraMode':
                    if self.checkMod(nick):
                        try:
                            if bs.getSharedObject('globals').cameraMode == 'follow':
                                bs.getSharedObject('globals').cameraMode = 'rotate'
                            else:
                                bs.getSharedObject('globals').cameraMode = 'follow'
                        except:
                            pass
              
                elif m == '/lm444':   
                    arr = []
                    for i in range(100):
                        try:
                            arr.append(bsInternal._getChatMessages()[-1-i])
                        except:
                            pass
                    arr.reverse()
                    for i in arr:
                        bsInternal._chatMessage(i)
                elif m == '/gp':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Using: /gp number of list')
                        else:
                            s = bsInternal._getForegroundHostSession()
                            for i in s.players[int(a[0])].getInputDevice()._getPlayerProfiles():
                                try:
                                    bsInternal._chatMessage(i)
                                except:
                                    pass
                elif m == '/icy':
                    if self.checkMod(nick):
                        bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node = bsInternal._getForegroundHostActivity().players[int(a[1])].actor.node
                elif m == '/fly':
                    if True:
                        if a == []:
                            bs.screenMessage('Use /fly or /fly all',color=(1,1,1), clients=[clientID], transient=True)

                            
                        else:
                            if self.checkMod(nick):
                                if a[0] == 'all':
                                    for i in bsInternal._getForegroundHostActivity().players:
                                        i.actor.node.fly = True
                                else:
                                    bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.fly = bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.fly == False
                elif m == '/floorReflection':
                    if self.checkVip(nick):
                        bs.getSharedObject('globals').floorReflection = bs.getSharedObject('globals').floorReflection == False
                elif m == '/ac':
                    #if self.checkVip(nick):
                        if a == []:
                            bsInternal._chatMessage('Using: /ac R G B')
                            bsInternal._chatMessage('OR')
                            bsInternal._chatMessage('Using: /ac r bright speed')
                        else:
                            if a[0] == 'r':
                                m = 1.3 if a[1] is None else float(a[1])
                                s = 1000 if a[2] is None else float(a[2])
                                bsUtils.animateArray(bs.getSharedObject('globals'), 'ambientColor',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(0,0,1*m),s*3:(1*m,0,0)},True)
                            else:
                                try:
                                    if a[1] is not None:
                                        bs.getSharedObject('globals').ambientColor = (float(a[0]),float(a[1]),float(a[2]))
                                    else:
                                        bs.screenMessage('Error!',color = (1,0,0))
                                except:
                                    bs.screenMessage('Error!',color = (1,0,0))
                elif m == '/iceOff':
                    try:
                        activity.getMap().node.materials = [bs.getSharedObject('footingMaterial')]
                        activity.getMap().isHockey = False
                    except:
                        pass
                    try:
                        activity.getMap().floor.materials = [bs.getSharedObject('footingMaterial')]
                        activity.getMap().isHockey = False
                    except:
                        pass
                    for i in activity.players:
                        i.actor.node.hockey = False
                elif m == '/maxPlayers':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Using: /maxPlayers count of players')
                        else:
                            try:
                                bsInternal._getForegroundHostSession()._maxPlayers = int(a[0])
                                bsInternal._setPublicPartyMaxSize(int(a[0]))
                                bsInternal._chatMessage('Players limit set to '+str(int(a[0])))
                            except:
                                bs.screenMessage('Error!',color = (1,0,0))
                            '''
                elif m == '/heal':
                    if a == []:
                        bsInternal._chatMessage('Using: /heal all or number of list')
                    else:
                        try:
                            bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'health'))
                        except:
                            pass      original heal command new one modified by mr.smoothy

                        '''
                elif m == '/heal': #shield
                    if a == []:
                        
                        bs.screenMessage('Using: /heal all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                    else:
                        if a[0]=='all':
                            if self.checkMod(nick):
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'health'))
                                          
                                    except Exception:
                                        pass
                        if len(a[0]) > 2:
                           for i in bs.getActivity().players:
                               try:
                                   if (i.getName().lower()).encode('utf-8') == (a[0]):
                                      if i.actor.exists():
                                         i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'health'))
                                         
                               except Exception:
                                   pass
                           bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                        else:
                             try:
                                 bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'health'))
                                 
                                 bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                             except Exception:
                                 bsInternal._chatMessage('PLAYER NOT FOUND')       

                elif m == '/punch': #shield
                    if self.checkVip(nick):
                        if a == []:
                            for i in range(len(activity.players)):
                                bs.getActivity().players[i].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))
                               
                            bsInternal._chatMessage('MUST USE PLAYER ID OR NICK')
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))
                                          
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))
                                             
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))
                                    
                                     bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                                 except Exception:
                                     bsInternal._chatMessage('PLAYER NOT FOUND')

                
                elif m == '/gift': #random powerup
                    if self.checkMod(nick):
                        powerss=['shield','punch','curse','health']
                        if True:
                            if True:
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.PowerupMessage(powerupType = powerss[random.randrange(0,4)]))
                                           
                                    except Exception:
                                        pass
                                     
                elif m == '/reset':
                    type='soft'
                    rs=0
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.reflection = type
                        bsInternal._getForegroundHostActivity().getMap().node.reflectionScale = rs
                    except:
                        pass
                    try:
                        bsInternal._getForegroundHostActivity().getMap().bg.reflection = type
                        bsInternal._getForegroundHostActivity().getMap().bg.reflectionScale = rs
                    except:
                        pass
                    try:
                        bsInternal._getForegroundHostActivity().getMap().floor.reflection = type
                        bsInternal._getForegroundHostActivity().getMap().floor.reflectionScale = rs
                    except:
                        pass
                    try:
                        bsInternal._getForegroundHostActivity().getMap().center.reflection = type
                        bsInternal._getForegroundHostActivity().getMap().center.reflectionScale = rs
                    except:
                        pass
                    bs.getSharedObject('globals').ambientColor = (0,0,0)
                    bs.getSharedObject('globals').tint = (1,1,1)

                elif m== '/disco':  #naacho benchod
                    times=[0]
                    def discoRed():
                        bs.getSharedObject('globals').tint = (1,.6,.6)
                        bs.gameTimer(230,bs.Call(discoBlue))
                    def discoBlue():
                        bs.getSharedObject('globals').tint = (.6,1,.6)
                        bs.gameTimer(230,bs.Call(discoGreen))
                    def discoGreen():
                        
                        bs.getSharedObject('globals').tint = (.6,.6,1)
                        if times[0]<10:
                            times[0]+=1

                            bs.gameTimer(230,bs.Call(discoRed))
                        else:
                            bs.getSharedObject('globals').tint = (1,1,1)
                    bs.gameTimer(300,bs.Call(discoRed))   

        
                elif m == '/reflections':
                    #if self.checkMod(nick):
                        if a == [] or len(a) < 2:
                            bsInternal._chatMessage('Using: /reflections type(1/0) scale')
                        rs = [int(a[1])]
                        type = 'soft' if int(a[0]) == 0 else 'powerup'
                        try:
                            bsInternal._getForegroundHostActivity().getMap().node.reflection = type
                            bsInternal._getForegroundHostActivity().getMap().node.reflectionScale = rs
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().bg.reflection = type
                            bsInternal._getForegroundHostActivity().getMap().bg.reflectionScale = rs
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().floor.reflection = type
                            bsInternal._getForegroundHostActivity().getMap().floor.reflectionScale = rs
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().center.reflection = type
                            bsInternal._getForegroundHostActivity().getMap().center.reflectionScale = rs
                        except:
                            pass
                elif m == '/shatter':
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /shatter all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0] == 'all':
                                if self.checkMod(nick):
                                    for i in bsInternal._getForegroundHostActivity().players:
                                        i.actor.node.shattered = int(a[1])
                            else:
                                bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.shattered = int(a[1])
                

                elif m == '/sleep':
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /sleep all or number of list',color=(0,0,1), clients=[clientID], transient=True)
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage("knockout",5000)
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage("knockout",5000)
                                
                elif m == '/iceBomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceBombs'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceBombs'))
                elif m == '/iceImpact':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceImpactBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceImpactBomb'))
                elif m == '/stickyBomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyBombs'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyBombs'))
                elif m == '/stickyice':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyIce'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyIce'))
                elif m == '/powerup':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'powerup'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'powerup'))
                elif m == '/icemine':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceMine'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceMine'))
                elif m == '/weedbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'weedbomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'weedbomb'))
                elif m == '/gluebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'gluebomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'gluebomb'))
                elif m == '/goldenBomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'goldenBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'goldenBomb'))
                elif m == '/mj':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'mj'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'mj'))
                elif m == '/colorpicker':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'colorPicker'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'colorPicker'))
                elif m == '/characterpicker':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'characterPicker'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'characterPicker'))
                elif m == '/bomber':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'bomber'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'bomber'))
                elif m == '/blastbot':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blastBot'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blastBot'))
                elif m == '/botspawner':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'botSpawner'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'botSpawner'))
                elif m == '/beachball':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'beachBall'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'beachBall'))
                elif m == '/flyer':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'flyer'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'flyer'))
                elif m == '/blackhole':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blackHole'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blackHole'))
                elif m == '/dronestrike':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'impactShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'impactShower'))
                elif m == '/jumpfly':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'jumpFly'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'jumpFly'))
                elif m == '/portalbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'portalBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'portalBomb'))
                elif m == '/spunch':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'spunch'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'spunch'))
                elif m == '/blast':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blast'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blast'))
                elif m == '/cursybomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'cursyBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'cursyBomb'))
                elif m == '/triple':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'tripleBombs'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'tripleBombs'))#this were to begin
                elif m == '/multibomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'multiBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'multiBomb'))
                elif m == '/spazbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'spazBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'spazBomb'))
                elif m == '/telebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'teleBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'teleBomb'))
                elif m == '/antigrav':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'antiGrav'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'antiGrav'))
                elif m == '/curseShower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'curseShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'curseShower'))
                elif m == '/bomber':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'bomber'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'bomber'))
                elif m == '/iceimpact':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceImpact'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceImpact'))
                elif m == '/blastbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blastBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'blastBomb'))
                elif m == '/headache':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'headache'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'headache'))#here
                elif m == '/revengebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'revengeBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'revengeBomb'))
                elif m == '/boombomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'boomBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'boomBomb'))
                elif m == '/impactbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'impactBombs'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'impactBombs'))
                elif m == '/cursebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'curseBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'curseBomb'))
                elif m == '/stickybomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyBombs'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyBombs'))
                elif m == '/icebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceBombs'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceBombs'))
                elif m == '/pirate':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'pirateBot'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'pirateBot'))
                                
                elif m == '/normalshower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'normalShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'normalShower'))
                                
                elif m == '/stickyshower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'stickyShower'))
                                
                elif m == '/iceshower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceShower'))
                                
                elif m == '/glueshower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'glueShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'glueShower'))
                                
                elif m == '/cursyshower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'curseShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'curseShower'))
                                
                elif m == '/impactshower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'touchShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'touchShower'))
                                
                elif m == '/pwpShower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'pwpShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'pwpShower'))
                                
                elif m == '/frozenshower':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'frozenShower'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'frozenShower'))
                                
                elif m == '/slimesnow':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'slimeSnow'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'slimeSnow'))
                                
                elif m == '/splintersnow':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'splinterSnow'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'splinterSnow'))
                                
                elif m == '/icesnow':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceSnow'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'iceSnow'))
                                
                elif m == '/sparksnow':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'sparkSnow'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'sparkSnow'))
                               
                elif m == '/sweatsnow':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'sweatSnow'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'sweatSnow'))
                                
                elif m == '/frozenbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bsInternal._chatMessage('Pick all or one specific Person')
                            bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'frozenBomb'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'frozenBomb'))

                elif m == '/cmr':
                    if self.checkVip(nick):
                        if a == []:
                            time = 8000
                        else:
                            time = int(a[0])
                            
                            op = 0.08
                            std = bs.getSharedObject('globals').vignetteOuter
                            bsUtils.animateArray(bs.getSharedObject('globals'),'vignetteOuter',3,{0:bs.getSharedObject('globals').vignetteOuter,17000:(0,1,0)})
                            
                        try:
                            bsInternal._getForegroundHostActivity().getMap().node.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().bg.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().bg.node.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().node1.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().node2.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().node3.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().steps.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().floor.opacity = op
                        except:
                            pass
                        try:
                            bsInternal._getForegroundHostActivity().getMap().center.opacity = op
                        except:
                            pass
                            
                        def off():
                            op = 1
                            try:
                                bsInternal._getForegroundHostActivity().getMap().node.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().bg.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().bg.node.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().node1.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().node2.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().node3.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().steps.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().floor.opacity = op
                            except:
                                pass
                            try:
                                bsInternal._getForegroundHostActivity().getMap().center.opacity = op
                            except:
                                pass
                            bsUtils.animateArray(bs.getSharedObject('globals'),'vignetteOuter',3,{0:bs.getSharedObject('globals').vignetteOuter,100:std})
                        bs.gameTimer(time,bs.Call(off))             

                elif m == '/bombNameFalse': 
                    bs.screenMessage("BombName Turned OFF")       
                    bsInternal._chatMessage('/bomb_name False') 
                elif m == '/bombNameTrue': 
                    bs.screenMessage("BombName Turned ON")       
                    bsInternal._chatMessage('/bomb_name True')       
                elif m == '/bombTimerFalse': 
                    bs.screenMessage("BombTimer Turned OFF")       
                    bsInternal._chatMessage('/bomb_Timer False') 
                elif m == '/bombTimerTrue': 
                    bs.screenMessage("BombTimer Turned ON")       
                    bsInternal._chatMessage('/bomb_Timer True')        
                elif m == '/bombModelFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("BombModel Turned OFF")       
                     bsInternal._chatMessage('/bomb_Model False') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[29] = "bombModel = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/bombModelTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("BombModel Turned ON")       
                     bsInternal._chatMessage('/bomb_Model True')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[29] = "bombModel = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                    
                elif m == '/powerupTimerFalse': 
                    bs.screenMessage("Powerup Timer Turned OFF")       
                    bsInternal._chatMessage('/powerup_Timer False') 
                elif m == '/powerupTimerTrue': 
                    bs.screenMessage("Powerup Timer Turned ON")       
                    bsInternal._chatMessage('/powerup_Timer True')        
                elif m == '/powerupNameFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Powerup Name Turned OFF")       
                     bsInternal._chatMessage('/powerup_Name False') 
                elif m == '/powerupNameTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Powerup Name Turned ON")       
                     bsInternal._chatMessage('/powerup_Name True')    
                elif m == '/powerupShieldFalse':
                    if self.checkMod(nick): 
                     bs.screenMessage("Powerup Shield Turned OFF")       
                     bsInternal._chatMessage('/powerup_Shield False') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[7] = "powerupShield = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/powerupShieldTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Powerup Shield Turned ON")       
                     bsInternal._chatMessage('/powerup_Shield True') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[7] = "powerupShield = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/discoLightFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("DiscoLights Turned OFF")       
                     bsInternal._chatMessage('/disco_Lights False') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[9] = "discoLights = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/discoLightTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("DiscoLights Turned ON")       
                     bsInternal._chatMessage('/disco_Lights True')   
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[9] = "discoLights = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/animateFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Colors Turned OFF")       
                     bsInternal._chatMessage('/ani_mate False') 
                elif m == '/animateTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Colors Turned ON")       
                     bsInternal._chatMessage('/ani_mate True')  
                elif m == '/charFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Char Turned OFF")       
                     bsInternal._chatMessage('/ch_ar False') 
                elif m == '/charTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Char Turned ON")       
                     bsInternal._chatMessage('/ch_ar True')   
                elif m == '/hpFalse':
                    if self.checkMod(nick): 
                     bs.screenMessage("HP Turned OFF")       
                     bsInternal._chatMessage('/h_p False') 
                elif m == '/hpTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("HP Turned ON")       
                     bsInternal._chatMessage('/h_p True')      
                elif m == '/tagFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("PC Tag Turned OFF")       
                     bsInternal._chatMessage('/ta_g False') 
                elif m == '/tagTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("PC Tag Turned ON")       
                     bsInternal._chatMessage('/ta_g True')        
                elif m == '/muteFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Muted is turned OFF")       
                     bsInternal._chatMessage('/mut_e False') 
                elif m == '/muteTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Mute is turned ON")       
                     bsInternal._chatMessage('/mute_e True')    
                elif m == '/pwpFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Powerups Turned OFF")       
                     bsInternal._chatMessage('/pw_p False') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[39] = "pwp = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/pwpTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Powerups Turned ON")       
                     bsInternal._chatMessage('/pw_p True')  
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[39] = "pwp = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                    
                elif m == '/powerupsFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("PC POWERUPS Turned OFF")       
                     bsInternal._chatMessage('/pc False') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[43] = "modded_powerups = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/powerupsTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("PC POWERUP Turned ON")       
                     bsInternal._chatMessage('/pc True') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[43] = "modded_powerups = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                    
                elif m == '/colorFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Color Turned OFF")       
                     bsInternal._chatMessage('/col False') 
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[17] = "colory = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/colorTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Color Turned ON")       
                     bsInternal._chatMessage('/col True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[17] = "colory = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                    
                elif m == '/whiteFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Whitelist Turned OFF")       
                     bsInternal._chatMessage('/whi_te False') 
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[1] = "whitelist = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()
                elif m == '/whiteTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Whitelist Turned ON")       
                     bsInternal._chatMessage('/whi_te True')    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[1] = "whitelist = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()        
                elif m == '/ptFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Popup Text Turned OFF")       
                     bsInternal._chatMessage('/pop False')    
                elif m == '/ptTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Popup Text Turned ON")       
                     bsInternal._chatMessage('/pop True')     
                elif m == '/nightFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Night Mode Turned OFF")       
                     bsInternal._chatMessage('/n_v False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[194] = "night = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/nightTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Night Mode Turned ON")       
                     bsInternal._chatMessage('/n_v True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[194] = "night = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()         
                elif m == '/flashFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Flash Mode Turned OFF")       
                     bsInternal._chatMessage('/fl_ash False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[196] = "flash = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/flashTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Flash Mode Turned ON")       
                     bsInternal._chatMessage('/fl_ash True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[196] = "flash = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                 
                elif m == '/ploFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Explosion Mode Turned OFF")       
                     bsInternal._chatMessage('/ex_plo False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[199] = "powExplo = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/ploTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Explosion Mode Turned ON")       
                     bsInternal._chatMessage('/ex_plo True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[199] = "powExplo = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()             
                elif m == '/floaterFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Navdeep Floater Turned On")       
                     bsInternal._chatMessage('/float_er False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[202] = "flashFloat = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/floaterTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("PC Floater Turned On")       
                     bsInternal._chatMessage('/float_er True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[202] = "flashFloat = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()  
                     #dfsfsfwefw                    
                elif m == '/glovefFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Gloves Turned Off PERM")       
                     bsInternal._chatMessage('/glo_ve False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[206] = "defaultBoxingGloves = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/glovefTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Gloves Turned On PERM")       
                     bsInternal._chatMessage('/glo_ve True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[206] = "defaultBoxingGloves = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()      
                     #dfsfsfwefw                    
                elif m == '/shieldfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Shield Turned Off PERM")       
                     bsInternal._chatMessage('/shi_eld False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[208] = "defaultShields = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/shieldfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Shield Turned On PERM")       
                     bsInternal._chatMessage('/shi_eld True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[208] = "defaultShields = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                     
                     #dfsfsfwefw                    
                elif m == '/rcharfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Random Char Turned Off PERM")       
                     bsInternal._chatMessage('/r_char False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[211] = "rchar = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/rcharfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Random Char Turned On PERM")       
                     bsInternal._chatMessage('/r_char True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[211] = "rchar = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()      
                     #wiwwiwi                    
                elif m == '/wizardfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Wizard Char Turned Off PERM")       
                     bsInternal._chatMessage('/wiz_ard False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[213] = "wizard = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/wizardfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Wizard Char Turned On PERM")       
                     bsInternal._chatMessage('/wiz_ard True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[213] = "wizard = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                     #wiwwiwi                    
                elif m == '/pixiefFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Pixie Char Turned Off PERM")       
                     bsInternal._chatMessage('/pix_ie False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[215] = "pixie = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/pixiefTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Pixie Char Turned On PERM")       
                     bsInternal._chatMessage('/pix_ie True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[215] = "pixie = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()         
                     #wiwwiwi                    
                elif m == '/ninjafFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ninja Char Turned Off PERM")       
                     bsInternal._chatMessage('/nin_ja False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[217] = "ninja = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/ninjafTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ninja Char Turned On PERM")       
                     bsInternal._chatMessage('/nin_ja True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[217] = "ninja = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()              
                     #wiwwiwi                    
                elif m == '/frostyfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Frosty Char Turned Off PERM")       
                     bsInternal._chatMessage('/fro_sty False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[219] = "frosty = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/frostyfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Frosty Char Turned On PERM")       
                     bsInternal._chatMessage('/fro_sty True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[219] = "frosty = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()      
                     #wiwwiwi                    
                elif m == '/pengufFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Pengu Char Turned Off PERM")       
                     bsInternal._chatMessage('/pen_gu False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[221] = "pengu = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/pengufTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Pengu Char Turned On PERM")       
                     bsInternal._chatMessage('/pen_gu True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[221] = "pengu = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()         
                     #wiwwiwi                    
                elif m == '/alifFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ali Char Turned Off PERM")       
                     bsInternal._chatMessage('/al_i False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[223] = "ali = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/alifTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ali Char Turned On PERM")       
                     bsInternal._chatMessage('/al_i True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[223] = "ali = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                        
                     #wiwwiwi                    
                elif m == '/robotfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Robot Char Turned Off PERM")       
                     bsInternal._chatMessage('/rob_ot False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[225] = "robot = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/robotfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Robot Char Turned On PERM")       
                     bsInternal._chatMessage('/rob_ot True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[225] = "robot = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()            
                     #wiwwiwi                    
                elif m == '/santafFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Santa Char Turned Off PERM")       
                     bsInternal._chatMessage('/san_ta False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[227] = "santa = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/santafTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Santa Char Turned On PERM")       
                     bsInternal._chatMessage('/san_ta True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[227] = "santa = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                     
                     #wiwwiwi                    
                elif m == '/impactfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Impact Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/imp_act False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[230] = "impact_bomb = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/impactfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Impact Bomb Turned On PERM")       
                     bsInternal._chatMessage('/imp_act True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[230] = "imp_act = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()        
                     #wiwwiwi                    
                elif m == '/icefFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ice Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/ic_e False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[232] = "ice_bomb = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/icefTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ice Bomb Turned On PERM")       
                     bsInternal._chatMessage('/ic_e True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[232] = "ice_bomb = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()           
                     #wiwwiwi                    
                elif m == '/stickyfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Sticky Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/sti_cky False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[234] = "sticky_bomb = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/stickyfTrue':
                    if self.checkMod(nick): 
                     bs.screenMessage("Sticky Bomb Turned On PERM")       
                     bsInternal._chatMessage('/sti_cky True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[234] = "sticky_bomb = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/spikefFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Spike Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/spi_ke False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[236] = "spike_bomb = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/spikefTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Spike Bomb Turned On PERM")       
                     bsInternal._chatMessage('/spi_ke True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[236] = "spike_bomb = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()      
                     #heheheheh
                elif m == '/shockfFalse':
                    if self.checkMod(nick): 
                     bs.screenMessage("Shock Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/sho_ck False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[238] = "shock_wave = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/shockfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Shock Bomb Turned On PERM")       
                     bsInternal._chatMessage('/sho_ck True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[238] = "shock_wave = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                     #heheheheh
                elif m == '/spazfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Spaz Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/spa_z False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[240] = "spaz_bomb = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/spazfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Spaz Bomb Turned On PERM")       
                     bsInternal._chatMessage('/spa_z True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[240] = "spaz_bomb = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()         
                     #heheheheh
                elif m == '/knockfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Knock Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/kno_ck False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[242] = "knock_bomb = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/knockfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Knock Bomb Turned On PERM")       
                     bsInternal._chatMessage('/kno_ck True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[242] = "knock_bomb = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()     
                     #heheheheh
                elif m == '/gluefFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Glue Bomb Turned Off PERM")       
                     bsInternal._chatMessage('/gl_ue False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[244] = "glue_bomb = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/gluefTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Glue Bomb Turned On PERM")       
                     bsInternal._chatMessage('/gl_ue True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[244] = "glue_bomb = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()        
                     #heheheheh
                elif m == '/pwpicefFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ice Emition Turned Off PERM")       
                     bsInternal._chatMessage('/pwp_ice False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[249] = "powIce = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/pwpicefTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Ice Emition Turned On PERM")       
                     bsInternal._chatMessage('/pwp_ice True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[249] = "powIce = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()     
                     #heheheheh
                elif m == '/pwpsplintfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Splinter Emition Turned Off PERM")       
                     bsInternal._chatMessage('/pwp_splint False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[251] = "powSplint = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/pwpsplintfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Splinter Emition Turned On PERM")       
                     bsInternal._chatMessage('/pwp_splint True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[251] = "powSplint = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()      
                     #heheheheh
                elif m == '/pwpslimefFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Slime Emition Turned Off PERM")       
                     bsInternal._chatMessage('/pwp_slime False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[253] = "powSlime = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/pwpslimefTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Slime Emition Turned On PERM")       
                     bsInternal._chatMessage('/pwp_slime True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[253] = "powSlime = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()  
                     #heheheheh
                elif m == '/pwpsweatfFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Sweat Emition Turned Off PERM")       
                     bsInternal._chatMessage('/pwp_sweat False')   
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[255] = "powSweat = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/pwpsweatfTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Sweat Emition Turned On PERM")       
                     bsInternal._chatMessage('/pwp_sweat True')  
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[255] = "powSweat = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()      
                elif m == '/verificationFalse': 
                    if self.checkMod(nick):
                     bs.screenMessage("Server Verification turned OFF")  
                     settings.enableVerification = False       
                     #                    
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[5] = "enableVerification = False\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()       
                elif m == '/verificationTrue': 
                    if self.checkMod(nick):
                     bs.screenMessage("Server Verification turned ON")  
                     settings.enableVerification = True     
                     #
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
                     list_of_lines = a_file.readlines()
                     list_of_lines[5] = "enableVerification = True\n"
                     a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
                     a_file.writelines(list_of_lines)
                     a_file.close()                       


                elif m == '/': 
                    if self.checkVip(nick):
                        if a == []:        
                            bsInternal._chatMessage('Special CHAT for Admin only')                                
                        else: 
                            try:       
                            #bs.screenMessage((a[0]),color = (1,1,1))     
                                bsUtils.ZoomText(
                                   (a[0]), maxWidth=800, lifespan=2500, jitter=2.0, position=(0, 180),
                                   flash=False, color=((0+random.random()*0.5),(0+random.random()*0.5),(0+random.random()*0.5)),
                                   trailColor=((0+random.random()*4.5),(0+random.random()*4.5),(0+random.random()*4.5))).autoRetain()
                            except:
                                 bs.screenMessage('Error has Occured',color = (1,1,1))            

                elif m == '//': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bsInternal._chatMessage('Special CHAT for Owner only')                                
                        else: 
                            try:       
                            #bs.screenMessage((a[0]),color = (1,1,1))     
                                k = (a[0])
                                bsUtils.ZoomText(
                                   k, maxWidth=800, lifespan=2500, jitter=2.0, position=(0, 180),
                                   flash=False, color=(0.93 * 1.25, 0.9 * 1.25, 1.0 * 1.25),
                                   trailColor=(0.15, 0.05, 1.0, 0.0)).autoRetain()
                            except:
                                bs.screenMessage('Error has Occured',color = (1,1,1))                                     
                    
                elif m == '/comp': 
                    if a == []:        
                        bs.screenMessage('Use /comp to complain Ex - /hekillingme\n DONT USE SPACES or it wont work',color=(1,1,1), clients=[clientID], transient=True)                         
                    else: 
                        try:       
                            bs.screenMessage('This command has been replaced with comp. Use comp for complains!',color = (1,1,1))
                        except:
                            bs.screenMessage('Complaint not send, resend',color = (1,1,1))         

                elif m == '/name': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bsInternal._chatMessage('Simply Change server name with east')
                            bsInternal._chatMessage('Server will restart after name applied')                        
                        else: 
                            try:       
                                bsInternal._setPublicPartyName((a[0]))
                                bs.screenMessage('Party Name has been change to '+(a[0]))
                            except:
                                bs.screenMessage('Party Name not changed',color = (1,1,1))  

                elif m == '/pvt': 
                    if self.checkOwner(nick):
                        if a == []:                               
                            bsInternal._chatMessage('Use /pvt to make server pvt or public')
                            bsInternal._chatMessage('Use True for pvt and false for public')   
                        elif a[0] == 'True':
                            try:
                                bsInternal._setPublicPartyEnabled(False)
                                bs.screenMessage('Server has been Made Private')
                            except:
                                bs.screenMessage('Server has not been made Private')
                        elif a[0] == 'False':
                            try:
                                bsInternal._setPublicPartyEnabled(True)
                                bs.screenMessage('Server has been Made Public')
                            except:
                                bs.screenMessage('Server has not been made Public')
                            
                elif m == '/bomb_name':
                    import fire
                    if a[0] == "False":
                        #bs.screenMessage("shieldBomb = False")#it wont work this way so i found another way to do above
                        fire.bombName = False
                    elif a[0] == "True":
                        #bs.screenMessage("shieldBomb = False")
                        fire.bombName = True                
                elif m == '/bomb_Timer':
                    import fire
                    if a[0] == "False":
                        fire.bombTimer = False
                    elif a[0] == "True":
                        fire.bombTimer = True   
                elif m == '/bomb_Model':
                    import fire
                    if a[0] == "False":
                        fire.bombModel = False
                    elif a[0] == "True":
                        fire.bombModel = True                        
                elif m == '/powerup_Timer':
                    import fire
                    if a[0] == "False":
                        fire.powerupTimer = False 
                    elif a[0] == "True":
                        fire.powerupTimer = True      
                elif m == '/powerup_Name':
                    import fire
                    if a[0] == "False":
                        fire.powerupName = False
                    elif a[0] == "True":
                        fire.powerupName = True                             
                elif m == '/powerup_Shield':
                    import fire
                    if a[0] == "False":
                        fire.powerupShield = False
                    elif a[0] == "True":
                        fire.powerupShield = True                              
                elif m == '/disco_Lights':
                    import fire
                    if a[0] == "False":
                        fire.discoLights = False
                    elif a[0] == "True":
                        fire.discoLights = True     
                elif m == '/ani_mate':
                    import fire
                    if a[0] == "False":
                        fire.animate = False 
                    elif a[0] == "True":
                        fire.animate = True                           
                elif m == '/col':
                    import fire
                    if a[0] == "False":
                        fire.colory = False
                    elif a[0] == "True":
                        fire.colory = True    
                elif m == '/ch_ar':
                    import fire
                    if a[0] == "False":
                        fire.randomChar = False
                    elif a[0] == "True":
                        fire.randomChar = True                      
                elif m == '/h_p':
                    import fire
                    if a[0] == "False":
                        fire.hp = False
                    elif a[0] == "True":
                        fire.hp = True                     
                elif m == '/ta_g':
                    import fire
                    if a[0] == "False":
                        fire.tag = False
                    elif a[0] == "True":
                        fire.tag = True      
                elif m == '/frosty':#dont use this one
                    import fire
                    if a[0] == "False":
                        fire.frosty = False 
                    elif a[0] == "True":
                        fire.frosty = True       
                elif m == '/textMap':#dont use this one
                    import fire
                    if a[0] == "False":
                        fire.textMap = False
                    elif a[0] == "True":
                        fire.textMap = True     
                elif m == '/powSet':#dont use this one
                    import fire
                    if a[0] == "False":
                        fire.powSet = False
                    elif a[0] == "True":
                        fire.powSet = True        
                elif m == '/pw_p':
                    import fire
                    if a[0] == "False":
                        fire.pwp = False
                    elif a[0] == "True":
                        fire.pwp = True             
                elif m == '/pc':
                    import fire
                    if a[0] == "False":
                        fire.modded_powerups = False
                    elif a[0] == "True":
                        fire.modded_powerups = True       
                elif m == '/pop':
                    import fire
                    if a[0] == "False":
                        fire.nameP = False
                    elif a[0] == "True":
                        fire.nameP = True     
                elif m == '/light':
                    import fire
                    if a[0] == "False":
                        fire.lightning = False
                    elif a[0] == "True":
                        fire.lightning = True     
                elif m == '/whi_te':
                    import fire
                    if a[0] == "False":
                        fire.whitelist = False
                    elif a[0] == "True":
                        fire.whitelist = True     
                elif m == '/n_v':
                    import fire
                    if a[0] == "False":
                        fire.night = False
                    elif a[0] == "True":
                        fire.night = True  
                elif m == '/fl_ash':
                    import fire
                    if a[0] == "False":
                        fire.flash = False
                    elif a[0] == "True":
                        fire.flash = True  
                elif m == '/ex_plo':
                    import fire
                    if a[0] == "False":
                        fire.powExplo = False
                    elif a[0] == "True":
                        fire.powExplo = True  
                elif m == '/float_er':
                    import fire
                    if a[0] == "False":
                        fire.flashFloat = False
                    elif a[0] == "True":
                        fire.flashFloat = True  
                elif m == '/glo_ve':
                    import fire
                    if a[0] == "False":
                        fire.defaultBoxingGloves = False
                    elif a[0] == "True":
                        fire.defaultBoxingGloves = True  
                elif m == '/shi_eld':
                    import fire
                    if a[0] == "False":
                        fire.defaultShields = False
                    elif a[0] == "True":
                        fire.defaultShields = True  
                elif m == '/r_char':
                    if self.checkOwner(nick):
                        import fire
                        if a[0] == "False":
                            fire.rchar = False
                        elif a[0] == "True":
                            fire.rchar = True  
                elif m == '/ses':
                    import wow
                    if a[0] == "False":
                        wow.ses = False
                    elif a[0] == "True":
                        wow.ses = True  
                elif m == '/wiz_ard':
                    import fire
                    if a[0] == "False":
                        fire.wizard = False
                    elif a[0] == "True":
                        fire.wizard = True  
                        wow.ses = True  
                elif m == '/pix_ie':
                    import fire
                    if a[0] == "False":
                        fire.pixie = False
                    elif a[0] == "True":
                        fire.pixie = True  
                elif m == '/nin_ja':
                    import fire
                    if a[0] == "False":
                        fire.ninja = False
                    elif a[0] == "True":
                        fire.ninja = True  
                elif m == '/fro_sty':
                    import fire
                    if a[0] == "False":
                        fire.frosty = False
                    elif a[0] == "True":
                        fire.frosty = True  
                elif m == '/pen_gu':
                    import fire
                    if a[0] == "False":
                        fire.pengu = False
                    elif a[0] == "True":
                        fire.pengu = True  
                elif m == '/al_i':
                    import fire
                    if a[0] == "False":
                        fire.ali = False
                    elif a[0] == "True":
                        fire.ali = True  
                elif m == '/rob_ot':
                    import fire
                    if a[0] == "False":
                        fire.robot = False
                    elif a[0] == "True":
                        fire.robot = True  
                elif m == '/san_ta':
                    import fire
                    if a[0] == "False":
                        fire.santa = False
                    elif a[0] == "True":
                        fire.santa = True  
                elif m == '/imp_act':
                    import fire
                    if a[0] == "False":
                        fire.impact_bomb = False
                    elif a[0] == "True":
                        fire.impact_bomb = True  
                elif m == '/ic_e':
                    import fire
                    if a[0] == "False":
                        fire.ice_bomb = False
                    elif a[0] == "True":
                        fire.ice_bomb = True  
                elif m == '/sti_cky':
                    import fire
                    if a[0] == "False":
                        fire.sticky_bomb = False
                    elif a[0] == "True":
                        fire.sticky_bomb = True  
                elif m == '/spi_ke':
                    import fire
                    if a[0] == "False":
                        fire.spike_bomb = False
                    elif a[0] == "True":
                        fire.spike_bomb = True  
                elif m == '/sho_ck':
                    import fire
                    if a[0] == "False":
                        fire.shock_wave = False
                    elif a[0] == "True":
                        fire.shock_wave = True 
                elif m == '/spa_z':
                    import fire
                    if a[0] == "False":
                        fire.spaz_bomb = False
                    elif a[0] == "True":
                        fire.spaz_bomb = True 
                elif m == '/kno_ck':
                    import fire
                    if a[0] == "False":
                        fire.knock_bomb = False
                    elif a[0] == "True":
                        fire.knock_bomb = True 
                elif m == '/gl_ue':
                    import fire
                    if a[0] == "False":
                        fire.glue_bomb = False
                    elif a[0] == "True":
                        fire.glue_bomb = True 
                elif m == '/pwp_splint':
                    import fire
                    if a[0] == "False":
                        fire.powSplint = False
                    elif a[0] == "True":
                        fire.powSplint = True 
                elif m == '/pwp_sweat':
                    import fire
                    if a[0] == "False":
                        fire.powSweat = False
                    elif a[0] == "True":
                        fire.powSweat = True 
                elif m == '/pwp_slime':
                    import fire
                    if a[0] == "False":
                        fire.powSlime = False
                    elif a[0] == "True":
                        fire.powSlime = True 
                elif m == '/pwp_ice':
                    import fire
                    if a[0] == "False":
                        fire.powIce = False
                    elif a[0] == "True":
                        fire.powIce = True 
                elif m == '/mut_e':
                    import fire
                    if a[0] == "False":
                        fire.muteAll = False
                    elif a[0] == "True":
                        fire.muteAll = True 
                elif m == '/muteOn':
                    settings.muteAll = True
                    bs.screenMessage('All are muted!') 
                elif m == '/muteOff':
                    settings.muteAll = False
                    bs.screenMessage('Mute turned off!')
                elif m == '/clear':
                    MID.verify = []
                    bs.screenMessage('Verification has been cleared!')
                elif m == '/clear_ban':
                    MID.verify = []
                    bs.screenMessage('Ban has been cleared!')


                        
                elif m == '/egg1':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg1')
                    except:
                        pass                  
                elif m == '/egg2':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg2')
                    except:
                        pass                        
                elif m == '/egg3':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg3')
                    except:
                        pass                        
                elif m == '/egg4':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg4')
                    except:
                        pass                        
                elif m == '/crossOut':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('crossOut')
                    except:
                        pass
                elif m == '/crossOutMask':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('crossOutMask')
                    except:
                        pass
                elif m == '/ouyaU':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('ouyaUbutton')
                    except:
                        pass
                elif m == '/ouyaO':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('ouyaObutton')
                    except:
                        pass
                elif m == '/rgb':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('rgbStripes')
                    except:
                        pass
                elif m == '/ouyaA':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('ouyaAbutton')
                    except:
                        pass
                elif m == '/heel':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('achievementStayinAlive')
                    except:
                        pass
                elif m == '/tnt':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('achievementTNT')
                    except:
                        pass
                elif m == '/ali':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('aliColor')
                    except:
                        pass
                elif m == '/icon':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('graphicsIcon')
                    except:
                        pass
                elif m == '/level':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('levelIcon')
                    except:
                        pass
                elif m == '/eg1':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('eggTex1')
                    except:
                        pass
                elif m == '/eg2':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('eggTex2')
                    except:
                        pass
                elif m == '/eg3':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('eggTex3')
                    except:
                        pass
                elif m == '/emoji':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('fontExtras2')
                    except:
                        pass
                elif m == '/flag':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('flagColor')
                    except:
                        pass
                elif m == '/b':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.self.model = bs.getModel('tnt')
                    except:
                        pass
                elif m == '/circle':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('gameCircleIcon')
                    except:
                        pass
                elif m == '/opera':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('operaSingerIconColorMask')
                    except:
                        pass
                elif m == '/she':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('powerupShield')
                    except:
                        pass
                elif m == '/impac':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('impactBombColor')
                    except:
                        pass
                        
                elif m=='/power':
                    bs.screenMessage('Type any powerup name in lower case EX: stickybomb all', clients=[clientID], transient=True)
                    bs.screenMessage('Few Powerups are wired||Admin and Owner', clients=[clientID], transient=True)
                    bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/texxHelp':
                    if self.checkMod(nick):
                     bs.screenMessage('Change Map Tex: /impac /she /egg1 /egg2 /egg3 /egg4 /eg1 /eg2 /eg3 /flag /icon /opera ', clients=[clientID], transient=True)
                     bs.screenMessage('/ali /emoji /level /tnt /heel /ouyaA /ouyaO /ouyaU /crossOut /crossOutMask', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                    
                elif m=='/texHelp':
                    if self.checkMod(nick):
                     bs.screenMessage('Special Map Colors: /m /f /g /g2 /r /r2 /r3 /r4 /vb /vb2 /o', clients=[clientID], transient=True)
                     bs.screenMessage('Thanks to |Da Rocker| for INSPIRATION', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/rdisco':
                    if self.checkMod(nick):
                     bs.screenMessage('Exquisite DiscoLight Command Very Bright: /el', clients=[clientID], transient=True)
                     bs.screenMessage('Use with Caution I am not responsible', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/snowy':
                    if self.checkMod(nick):
                     bs.screenMessage('Special Snowfall: /sweatsnow /splintersnow /sparksnow /slimesnow', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/shower':
                    bs.screenMessage('Special Shower: /cursyshower /stickyshower /impactshower /iceshower /glueshower /normalshower /frozenshower', clients=[clientID], transient=True)
                    bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/mode':
                    if self.checkMod(nick):
                     bs.screenMessage('Server Configs: /powerupShield /powerupName /tag /hp /discoLight /bombModel', clients=[clientID], transient=True)
                     bs.screenMessage('/bombName /(char)+f /plo /pt /color /char /animate /pwp /powerups', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/mode2':
                    if self.checkMod(nick):
                     bs.screenMessage('Server Configs 2:  /flash /floater /spikeModel /white /name /pvt', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/config':
                    if self.checkMod(nick):
                     bs.screenMessage('Special Server Configs: /mode /mode2 /maps /snow /shower (Use True or False)', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m=='/info':
                    bs.screenMessage('Server fully modded by PC||Modder or PC||231392', clients=[clientID], transient=True)
                    bs.screenMessage('Special thanks to Blitz and SobyDamn', clients=[clientID], transient=True)
                    
                elif m=='/m':
                    bsInternal._chatMessage('/tint 0 0 1')      
                    bsInternal._chatMessage('beuh')              
                    bsInternal._chatMessage('/tint 2 0 0')      
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))                    
                    
                elif m=='/f':
                    bsInternal._chatMessage('/reflections -12 -12 -12')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv')   
                    bsInternal._chatMessage('/tint 1 1 1')     
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))                    

                elif m=='/g':
                    bsInternal._chatMessage('/reflections 12 12 12')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv')  
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))       

                elif m=='/o':
                    bsInternal._chatMessage('/ac 12 12 12')      
                    bsInternal._chatMessage('/reflections -12 -12 -12')              
                    bsInternal._chatMessage('/ac 12 12 12')  
                    bsInternal._chatMessage('/ac 1 1 1')  
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))                                        

                elif m=='/g2':
                    bsInternal._chatMessage('/reflections 12 20 12')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv')      
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
                    
                elif m=='/r3':
                    bsInternal._chatMessage('/reflections -20 -15 -30')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv')      
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
                    
                elif m=='/el':
                    bsInternal._chatMessage('/ac r 12 12 12')      
                    bsInternal._chatMessage('/r')              
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
                    
                elif m=='/r4':
                    bsInternal._chatMessage('/reflections -500 -500 -500')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv')   
                    bsInternal._chatMessage('/tint 1 1 1')   
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
                    
                elif m=='/vb2':
                    bsInternal._chatMessage('/reflections -12 500 -100')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv')    
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))                    
                    
                elif m=='/vb':
                    bsInternal._chatMessage('/reflections 100 100 100')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv') 
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
                    
                elif m=='/r2':
                    bsInternal._chatMessage('/reflections -100 -100 -100')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv') 
                    
                elif m=='/snowe':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/flag')      
                     bsInternal._chatMessage('/g2')              
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/snowe2':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/crossOutMask')      
                     bsInternal._chatMessage('/o')              
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/red':#works on app need to check if work on server!
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/crossOutMask')      
                     bsInternal._chatMessage('/g2')              
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/dark':
                    if self.checkMod(nick):  
                     bsInternal._chatMessage('/crossOutMask')      
                     bsInternal._chatMessage('/r2')                    
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/colorful':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/crossOutMask')      
                     bsInternal._chatMessage('/g2') 
                     bsInternal._chatMessage('/tint 1 1 1')                   
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/smooth':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/heel')      
                     bsInternal._chatMessage('/g2') 
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/dirt':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/impac')      
                     bsInternal._chatMessage('/g2') 
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/dirt2':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/impac')      
                     bsInternal._chatMessage('/r') 
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/pink':
                    if self.checkOwner(nick):
                     bsInternal._chatMessage('/level')      
                     bsInternal._chatMessage('/r') 
                    # bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/yellow':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/egg4')      
                     bsInternal._chatMessage('/r') 
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/smooth2':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/heel')      
                     bsInternal._chatMessage('/r') 
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/orange':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/ali')      
                     bsInternal._chatMessage('/f')              
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/orange2':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/ali')      
                     bsInternal._chatMessage('/o')              
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/red2':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/crossOutMask')      
                     bsInternal._chatMessage('/f')              
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/red3':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/crossOutMask')      
                     bsInternal._chatMessage('/g')              
                    # bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/red4':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/crossOutMask')      
                     bsInternal._chatMessage('/o')              
                    # bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    
                elif m=='/blue':
                    if self.checkMod(nick):
                     bsInternal._chatMessage('/egg2')      
                     bsInternal._chatMessage('/g2')              
                     #bs.screenMessage(bs.getSpecialChar('logoFlat'))

                elif m=='/r':
                    bsInternal._chatMessage('/reflections -21 -23 -21')      
                    bsInternal._chatMessage('/tint 0 0 1')              
                    bsInternal._chatMessage('/nv')         
                    bsInternal._chatMessage('/tint 1 1 1')      
                    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))                    
                   
                elif m == '/rules':
                    bs.screenMessage('Respect is Key here and use ethical manners for speech', clients=[clientID], transient=True)
                    bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m == '/cmd':
                    bs.screenMessage('For Admins: /maps /texHelp /texxHelp /rdisco /power /', clients=[clientID], transient=True)
                    bs.screenMessage('For Owners: /config // and all', clients=[clientID], transient=True)
                    bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m == '/maps':
                    if self.checkMod(nick):
                     bs.screenMessage('New Maps Tex: /snowe /snowe2 /blue /red /red2 /red3 /red4 /orange /orange2', clients=[clientID], transient=True)
                     bs.screenMessage('/pink /yellow /dirt /dirt2 /dark /smooth /smooth2 /colorful', clients=[clientID], transient=True)
                     bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                elif m == '/ip':
                    import socket
                    hostname = socket.gethostname()
                    local_ip = socket.gethostbyname(hostname)
                    bs.screenMessage('Server IP == '+local_ip,color=(1,1,1), clients=[clientID], transient=True)
                    bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)
                    
                        
                elif m=='/contact':
                    bs.screenMessage('Discord PCModder#7995 or email pc231392@gmail.com', clients=[clientID], transient=True)
                    bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)

                          
                elif m == '/help':
                    bs.screenMessage('Available commands to use: /info /contact /ip /cmds /rules', clients=[clientID], transient=True)
                    bs.screenMessage('Use /mail or /comp to send complaints to owner through Email', clients=[clientID], transient=True)
                    bs.screenMessage('All rights to PC||231392', clients=[clientID], transient=True)

                elif m == '/list': #list of current players id
                    if self.checkVip(nick):
                     bsInternal._chatMessage("==========PLAYER KICK IDS==========")
                     for i in bsInternal._getGameRoster():
                         try:
                             bsInternal._chatMessage(i['players'][0]['nameFull'] + "     kick ID " + str(i['clientID']))
                         except Exception:
                             pass
                     bsInternal._chatMessage("==========PLAYER IDS=============")
                     for s in bsInternal._getForegroundHostSession().players:
                         bsInternal._chatMessage(s.getName() +"  ID = "+ str(bsInternal._getForegroundHostSession().players.index(s)))
                    
                elif m == '/id':
                    for i in bsInternal._getForegroundHostActivity().players:
            
                        if i.getInputDevice().getClientID()==clientID:client=i.get_account_id()
                    bruh = True
                    if bruh: 
                        bs.screenMessage('Your Account ID ---> '+i.get_account_id(),color=(2,1,4), clients=[clientID], transient=True)
                        bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    else:
                        bs.screenMessage('Error has Occured',color=(2,1,4), clients=[clientID], transient=True)

                elif m == '/ffaMode': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bsInternal._chatMessage('Switch to FFA GameMode')                                
                        else: 
                            try:          
                                import bsTeamGame
                                #bsTeamGame.gDefaultTeamColors = ((1,1,1), (2,2,2))
                                k = bs.FreeForAllSession
                                bsInternal._newHostSession(k)
                                bsUtils._getDefaultFreeForAllPlaylist()
                                bs.screenMessage('GameMode Changed to FFA')
                            except:
                                bs.screenMessage('Error has Occured',color = (1,1,1))  

                elif m == '/teamMode': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bsInternal._chatMessage('Switch to Teams GameMode')                                
                        else: 
                            try:           
                                import bsTeamGame
                                #bsTeamGame.gDefaultTeamColors = ((1,1,1), (2,2,2))
                                k = bs.TeamsSession
                                bsInternal._newHostSession(k)
                                bs.screenMessage('GameMode Changed to TEAMS')
                                playlist = bsUtils._getDefaultTeamsPlaylist()
                                bsUtils._filterPlaylist(playlist, k, removeUnOwned=False,markUnOwned=True)
                            except:
                                bs.screenMessage('Error has Occured',color = (1,1,1))  
                        
                elif m == '/mail': #it works :) done full by PC||231392
                    if a == []:        
                        bsInternal._chatMessage('Use /comp to complain||Write Your Name')        
                        bsInternal._chatMessage('Do not use spaces EX: thisguykillme')        
                        bsInternal._chatMessage('All rights to PC||231392')                          
                    else: 
                        try:       
                            import smtplib
                            
                            sender_email = "pc231392@gmail.com"
                            rec_email = "pc231392@gmail.com"
                            password = "kuri@2004"
                            message = (a[0])

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender_email, password)
                            print("Login success")
                            server.sendmail(sender_email, rec_email, message)
                            print("Email has been sent to ", rec_email)
                            bs.screenMessage('Complaint sent to Owner through Email',color = (1,1,1))  
                        except:
                            bs.screenMessage('Complaint not send, resend',color = (1,1,1))  
                            
                elif m == '/email': #it works :) send anyone an email special by PC||231392
                    if a == []:        
                        bsInternal._chatMessage('Use /comp to complain||Write Your Name')        
                        bsInternal._chatMessage('Do not use spaces EX: thisguykillme')        
                        bsInternal._chatMessage('All rights to PC||231392')                          
                    else: 
                        try:       
                            import smtplib
                            
                            sender_email = "pc231392@gmail.com"
                            rec_email = (a[0])
                            password = "kuri@2004"
                            message = (a[1])

                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login(sender_email, password)
                            print("Login success")
                            server.sendmail(sender_email, rec_email, message)
                            print("Email has been sent to ", rec_email)
                            bs.screenMessage('Complaint sent to Owner through Email',color = (1,1,1))  
                        except:
                            bs.screenMessage('Complaint not send, resend',color = (1,1,1))  

                elif m == '/gtest': #it works :) send anyone an email special by PC||231392
                    if a == []:        
                        bsInternal._chatMessage('Use /comp to complain||Write Your Name')        
                        bsInternal._chatMessage('Do not use spaces EX: thisguykillme')        
                        bsInternal._chatMessage('All rights to PC||231392')                          
                    else: 
                        try:       
                            import smtplib                          
                            smtpServer='smtp.gmail.com'      
                            fromAddr='pc231392@gmail.com'         
                            toAddr='pc231392@gmail.com'     
                            text= "This is a test of sending email from within Python."
                            server = smtplib.SMTP(smtpServer,25)
                            server.ehlo()
                            server.starttls()
                            server.sendmail(fromAddr, toAddr, text) 
                            server.quit()                            
                            bs.screenMessage('Complaint sent to Owner through Email',color = (1,1,1))  
                        except:
                            bs.screenMessage('Complaint not send, resend',color = (1,1,1))  


                   
            
c = cheatOptions()

def cmnd(msg,clientID):
    if bsInternal._getForegroundHostActivity() is not None:
    
        c.opt(clientID,msg)
bs.realTimer(5000,bs.Call(bsInternal._setPartyIconAlwaysVisible,True))

import bsUI
bs.realTimer(10000,bs.Call(bsUI.onPartyIconActivate,(0,0)))## THATS THE TRICKY PART check ==> 23858 bsUI / _handleLocalChatMessage

#for help contact mr.smoothy#5824 on discord
