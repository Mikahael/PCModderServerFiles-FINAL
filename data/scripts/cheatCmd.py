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
import getPermissionsHashes as gph
import settings_powerups as set_pwp
import bsServerData as internals
import settings_bombs as set_bomb
import settings_spaz as set_spaz




class cheatOptions(object):
    def __init__(self):
        self.all = True # just in case
       
        
        self.tint = None # needs for /nv
    
    def checkOwner(self,clientID): 
       
        client='kuchbhi'
        
        for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
        if client in MID.owners or client in gph.ownerHashes or client in MID.owner2 or client in internals.prt_list:
            bs.screenMessage('All rights to PCModder!',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
            
        else:
            bs.screenMessage('Command Denied',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))

    def checkMod(self,clientID): 
       
        client='kuchbhi'
        
        for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
        if client in MID.mods or client in MID.mod2 or client in MID.owners or client in gph.ownerHashes or client in gph.adminHashes or client in MID.owner2:
            bs.screenMessage('All rights to PCModder!',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
            
        else:
            bs.screenMessage('Command Denied',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
        

    def checkMember(self,clientID): 
       client='kuchbhi'
        
       for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
       if client in MID.mods or client in MID.members  or client in MID.vips or client in MID.owners or client in MID.mod2 or client in MID.vip2 or client in gph.ownerHashes or client in gph.adminHashes or client in gph.vipHashes or client in MID.owner2:  #member,vip,admin will have access
            bs.screenMessage('All rights to PCModder!',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
           
       else:
            bs.screenMessage('Command Denied',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))

      
    def checkVip(self,clientID):
        client='kuchbhi'
        
        for i in bsInternal._getForegroundHostActivity().players:
            
            if i.getInputDevice().getClientID()==clientID:
                client=i.get_account_id()
        
        if client in MID.mods or client in MID.vips or  client in MID.owners or client in MID.mod2 or client in MID.vip2 or client in gph.ownerHashes or client in gph.adminHashes or client in gph.vipHashes or client in MID.owner2:     #only admin and vip can access
            bs.screenMessage('Command Accepted',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))
            return True
            
        else:
            bs.screenMessage('Command Denied',color=(1,1,1), clients=[clientID], transient=True)
            #bs.screenMessage(bs.getSpecialChar('logoFlat'))

    def kickByNick(self,nick):
        roster = bsInternal._getGameRoster()
        for i in roster:
            try:
                if i['players'][0]['nameFull'].lower().find(nick.encode('utf-8').lower()) != -1:
                    bsInternal._disconnectClient(int(i['clientID']))
            except:
                pass
                
    def listPlayerIDs(self, clientID):
        if self.checkMod(clientID):  # Only mods and owners can access this command
            activity = bsInternal._getForegroundHostActivity()
            with bs.Context(activity):
                player_info = []
                for player in bsInternal._getForegroundHostSession().players:
                    name = player.getName()
                    pid = player.get_account_id()
                    player_info.append(name+': '+pid)

                # Display the list of player names and pbids to the client who issued the command
                bs.screenMessage('Player Names and Account IDs (pbids):\n' + '\n'.join(player_info),
                                 color=(1, 1, 1), clients=[clientID], transient=True)
                                 
    def setPlayerName(self, clientID, msg):
        if self.checkMod(clientID):  # Only mods and owners can access this command
            activity = bsInternal._getForegroundHostActivity()
            with bs.Context(activity):
                try:
                    target_name = msg.split(' ')[0]
                    new_name = msg.split(' ')[1]
                    
                    # Find the target player based on the provided name
                    target_player = None
                    for player in bsInternal._getForegroundHostSession().players:
                        if player.getName().lower() == target_name.lower():
                            target_player = player
                            break
                    
                    if target_player is not None:
                        # Change the target player's name
                        target_player.getInternalNode().sessionPlayerName = new_name
                        bs.screenMessage('Changed the name of '+target_name+' to '+new_name,
                                         color=(0, 1, 0), clients=[clientID], transient=True)
                    else:
                        bs.screenMessage('Player '+target_name+' not found.', color=(1, 0, 0),
                                         clients=[clientID], transient=True)
                except IndexError:
                    bs.screenMessage('Usage: ?setname <old_name> <new_name>', color=(1, 0, 0),
                                     clients=[clientID], transient=True)


      #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
    def opt(self,clientID,msg):
        nick=clientID
        if True:
            m = msg.split(' ')[0] # command
            a = msg.split(' ')[1:] # arguments
            password = 'test'
            
            activity = bsInternal._getForegroundHostActivity()
            with bs.Context(activity):
                if m == '?kick':
                    if self.checkMod(clientID):
                        if a == []:
                            bs.screenMessage('kick using name of clientID',color=(0,1,0), clients=[clientID], transient=True)
                        else:
                            if len(a[0]) > 3:
                                if a[1] == password:
                                    if(self.checkOwner(nick)!=True):
                                        self.kickByNick(a[0])
                                    else:
                                        bs.screenMessage('You cant kick owner!',color=(1,0,0), clients=[clientID], transient=True)  
                                else:
                                    bs.screenMessage(u'\ue048Password Incorrect!\ue048',color=(1,1,1), clients=[clientID], transient=True)
                            else:
                                try:
                                    s = int(a[0])
                                    for cl in bsInternal._getForegroundHostSession().players:
                                        if(cl.getInputDevice().getClientID()==s):
                                            accountid=cl.get_account_id()
                                    if a[1] == password:
                                        if accountid in MID.owners:
                                            bs.screenMessage('cant kick owner',color=(1,0,0), clients=[clientID], transient=True)
                                        else:    
                                            bsInternal._disconnectClient(int(a[0]))
                                    else:
                                        bs.screenMessage(u'\ue048Password Incorrect!\ue048',color=(1,1,1), clients=[clientID], transient=True)
                                except:
                                    if a[1] == password:
                                        self.kickByNick(a[0])
                                    else:
                                        bs.screenMessage(u'\ue048Password Incorrect!\ue048',color=(1,1,1), clients=[clientID], transient=True)
                                    
                elif m == '?hi':
                    if a == []:
                        bs.screenMessage('Please provide Password as well!',color=(1,1,1), clients=[clientID], transient=True)
                    elif a[0] == password:
                        bs.screenMessage('HI!',color=(1,1,1), clients=[clientID], transient=True)
                    else:
                        bs.screenMessage(u'\ue048Password Incorrect!\ue048',color=(1,1,1), clients=[clientID], transient=True)
                elif m == '?pid':
                    self.listPlayerIDs(clientID)
                elif m == '?setname':
                    self.setPlayerName(clientID, ' '.join(a))  # Pass the entire message as a parameter
                   
                elif m == '?getlost':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Using: /kick name or number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            if len(a[0]) > 3:
                                self.kickByNick(a[0])
                            else:
                                try:
                                    s = int(a[0])
                                    bsInternal._disconnectClient(int(a[0]))
                                except:
                                    self.kickByNick(a[0])
                elif m == '?lister':     #Terible doesnt work, i have added better one. PCModder
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
                elif m == '?ooh':
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
                            
                elif m=='?me':
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
                
                elif m == '?owner2':
                    if self.checkOwner(nick):
                        clID = int(a[0])
                        updated_admins=[]
                        updated_admins=MID.owner2
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
                                   
                                    if newadmin in MID.owner2:
                                        updated_admins.remove(newadmin)

                        if True:

                            with open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py") as file:
                                s = [row for row in file]
                               
                                s[45] = 'owner2 = '+ str(updated_admins)+ '\n'
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/membersID.py",'w')
                                for i in s:
                                    f.write(i)
                                f.close()
                                reload(MID)
                        else:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

                elif m == '?owner':
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

                elif m == '?nooby':
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
                            



                elif m == '?vip2':#mod with no tag
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


                elif m == '?mod2':#mod with no tag
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


                elif m == '?mute':
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


                elif m == '?mod':
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
                            
                elif m == '?white':
                    if self.checkMod(nick):
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
                            
                elif m == '?reject':
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

                elif m == '?vip':
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
                elif m == '?btag':
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
                            
                elif m == '?htag':
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
                            
                elif m == '?colortag':
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
                            
                elif m == '?ice':
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

                elif m == '?smoke':
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
                            
                elif m == '?light':
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
                            
                elif m == '?glow':
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
                            
                elif m == '?ctag':
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
                            
                elif m == '?dtag':
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
                            
                elif m == '?member':
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
                elif m == '?playSound':
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
                elif m == '?quit':
                    if self.checkOwner(nick):
                        bsInternal.quit()
                elif m == '?nv':
                    if self.checkVip(nick):
                        if self.tint is None:
                            self.tint = bs.getSharedObject('globals').tint
                        bs.getSharedObject('globals').tint = (0.5,0.7,1) if a == [] or not a[0] == u'off' else self.tint

                elif m == '?freeze': #shield
                    if self.checkVip(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /freeze all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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


                elif m == '?thaw': #shield
                    if self.checkVip(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /thaw all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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

       
                
                elif m == '?kill': #shield
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /kill all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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


                elif m == '?curse': #shield
                    if self.checkMod(nick):
                        if a == []:
                           
                            bs.screenMessage('Using: /curse all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
          

                elif m == '?box':
                    if a == []:
                        
                        bs.screenMessage('Using: /box all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
                          
                
                elif m == '?mine':
                    if a == []:
                        
                        bs.screenMessage('Using: /mine all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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

                elif m == '?headless':   #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                    if a == []:
                        
                        bs.screenMessage('Using: /headless all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
    
                elif m == '?shield': #shield
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /shield all or number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            if a[0]=='all':
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'shield'))
                                           bs.screenMessage('Shield will give you protection',color=(1,1,1), clients=[clientID], transient=True)
                                    except Exception:
                                        pass
                            if len(a[0]) > 2:
                               for i in bs.getActivity().players:
                                   try:
                                       if (i.getName().lower()).encode('utf-8') == (a[0]):
                                          if i.actor.exists():
                                             i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'shield'))
                                             bs.screenMessage('Shield will give you protection',color=(1,1,1), clients=[clientID], transient=True)
                                   except Exception:
                                       pass
                               bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                            else:
                                 try:
                                     bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'shield'))
                                     bs.screenMessage('Shield will give you protection',color=(1,1,1), clients=[clientID], transient=True)
                                     bsInternal._chatMessage(bs.getSpecialChar('logoFlat'))
                                 except Exception:
                                     bs.screenMessage('PLAYER NOT FOUND',color=(1,1,1), clients=[clientID], transient=True)
                                 
                elif m == '?celebrate': #celebrate him
                    if a == []:
                       
                        bs.screenMessage('Using: /celebrate all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
                      
                elif m == '?remove': #shield
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /remove all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
   
                elif m == '?end':
                    if self.checkMod(nick):
                        try:
                            bsInternal._getForegroundHostActivity().endGame()
                        except:
                            pass  #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
                elif m == '?hug':
                    if a == []:
                        
                        bs.screenMessage('Using: /hug all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?gm':
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
                                 

                elif m == '?tint':
                    if self.checkVip(nick):
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
                                bsUtils.animateArray(bs.getSharedObject('globals'), 'tint',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(1,1,1*m),s*3:(1*m,0,0)},True)
                            else:
                                try:
                                    if a[1] is not None:
                                        bs.getSharedObject('globals').tint = (float(a[0]),float(a[1]),float(a[2]))
                                    else:
                                        bs.screenMessage('Error',color=(1,1,1), clients=[clientID], transient=True)

                                except:
                                    bs.screenMessage('Error',color=(1,1,1), clients=[clientID], transient=True)

                    
                elif m == '?sm':
                    if self.checkMod(nick):
                        bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion == False
                       
                


                elif m == '?spaz':
                    if a == []:
                        
                        bs.screenMessage('Using: /spaz all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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

                elif m == '?inv':
                    if a == []:
                        
                        bs.screenMessage('Using: /inv all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?cameraMode':
                    if self.checkMod(nick):
                        try:
                            if bs.getSharedObject('globals').cameraMode == 'follow':
                                bs.getSharedObject('globals').cameraMode = 'rotate'
                            else:
                                bs.getSharedObject('globals').cameraMode = 'follow'
                        except:
                            pass
              
                elif m == '?lm444':   
                    arr = []
                    for i in range(100):
                        try:
                            arr.append(bsInternal._getChatMessages()[-1-i])
                        except:
                            pass
                    arr.reverse()
                    for i in arr:
                        bsInternal._chatMessage(i)
                elif m == '?gp':
                    if self.checkMod(nick):
                        if a == []:
                        	bs.screenMessage('Using: /gp number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            s = bsInternal._getForegroundHostSession()
                            for i in s.players[int(a[0])].getInputDevice()._getPlayerProfiles():
                                try:
                                    bsInternal._chatMessage(i)
                                except:
                                    pass
                elif m == '?icy':
                    if self.checkMod(nick):
                        bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node = bsInternal._getForegroundHostActivity().players[int(a[1])].actor.node
                elif m == '?fly':
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
                elif m == '?floorReflection':
                    if self.checkVip(nick):
                        bs.getSharedObject('globals').floorReflection = bs.getSharedObject('globals').floorReflection == False
                elif m == '?ac':
                    if self.checkVip(nick):
                        if a == []:
                            bs.screenMessage('Using: /ac R G B',color=(1,1,1), clients=[clientID], transient=True)
                            bs.screenMessage('OR',color=(1,1,1), clients=[clientID], transient=True)
                            bs.screenMessage('Using: /ac r bright speed',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            if a[0] == 'r':
                                m = 1.3 if a[1] is None else float(a[1])
                                s = 1000 if a[2] is None else float(a[2])
                                bsUtils.animateArray(bs.getSharedObject('globals'), 'ambientColor',3, {0: (1*m,0,0), s: (0,1*m,0),s*2:(1,1,1*m),s*3:(1*m,0,0)},True)
                            else:
                                try:
                                    if a[1] is not None:
                                        bs.getSharedObject('globals').ambientColor = (float(a[0]),float(a[1]),float(a[2]))
                                    else:
                                        bs.screenMessage('Error!',color = (1,0,0))
                                except:
                                    bs.screenMessage('Error!',color = (1,0,0))
                elif m == '?iceOff':
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
                elif m == '?maxplayers':
                    if self.checkMod(nick):
                        if a == []:
                        	bs.screenMessage('Using: /maxplayers count of players',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                bsInternal._getForegroundHostSession()._maxPlayers = int(a[0])
                                bsInternal._setPublicPartyMaxSize(int(a[0]))
                                bsInternal._chatMessage('Players limit set to '+str(int(a[0])))
                            except:
                                bs.screenMessage('Error!',color = (1,0,0))
                            '''
                elif m == '?heal':
                    if a == []:
                        bsInternal._chatMessage('Using: /heal all or number of list')
                    else:
                        try:
                            bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'health'))
                        except:
                            pass      original heal command new one modified by mr.smoothy

                        '''
                elif m == '?heal': #shield
                    if a == []:
                        
                        bs.screenMessage('Using: /heal all or number of list',color=(1,1,1), clients=[clientID], transient=True)
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
                                 bs.screenMessage('Player Not Found',color=(1,1,1), clients=[clientID], transient=True)

                elif m == '?punch': #shield
                    if self.checkVip(nick):
                        if a == []:
                            for i in range(len(activity.players)):
                                bs.getActivity().players[i].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))
                               
                            bs.screenMessage('Must use Player id or Nick',color=(1,1,1), clients=[clientID], transient=True)
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
                                     bs.screenMessage('Player Not Found',color=(1,1,1), clients=[clientID], transient=True)

                elif m == '?sedlyf': #random powerup
                    if self.checkMod(nick):
                        powerss=['shield','punch','spunch','health']
                        if True:
                            if True:
                                for i in bs.getActivity().players:
                                    try:
                                        if i.actor.exists():
                                           i.actor.node.handleMessage(bs.PowerupMessage(powerupType = powerss[random.randrange(0,4)]))
                                           
                                    except Exception:
                                        pass

                
                elif m == '?gift': #random powerup
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
                                     
                elif m == '?reset':
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

                elif m== '?disco':  #naacho benchod
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

        
                elif m == '?reflections':
                    if self.checkMod(nick):
                        if a == [] or len(a) < 2:
                            bs.screenMessage('Using /reflections Type (1/0) Scale',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?shatter':
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /shatter all or number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            if a[0] == 'all':
                                if self.checkMod(nick):
                                    for i in bsInternal._getForegroundHostActivity().players:
                                        i.actor.node.shattered = int(a[1])
                            else:
                                bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.shattered = int(a[1])
                

                elif m == '?sleep':
                    if self.checkMod(nick):
                        if a == []:
                            
                            bs.screenMessage('Using: /sleep all or number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage("knockout",5000)
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage("knockout",5000)
                                
                elif m == '?icebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?iceimpact':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?stickybomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?stickyice':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?powerup':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?icemine':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?weedbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?gluebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?colorpicker':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'colorPicker'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'colorPicker'))
                elif m == '?charpicker':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'characterPicker'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'characterPicker'))
                elif m == '?bomber':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)         
                        else:
                            if a[0] == 'all':
                                for i in bs.getSession().players:
                                    try:
                                        i.actor.node.handleMessage(bs.PowerupMessage(powerupType = 'bomber'))
                                    except:
                                        pass
                            else:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType = 'bomber'))
                elif m == '?blastbot':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?botspawner':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?beachball':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?flyer':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?blackhole':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?dronestrike':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?jumpfly':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?portalbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?spunch':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?blast':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?cursybomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?triple':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?multibomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?spazbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?telebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?antigrav':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?curseshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?bomber':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?iceimpact':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?blastbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?headache':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?revengebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?boombomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?impactbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?cursebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?stickybomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?icebomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                elif m == '?pirate':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?normalshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?stickyshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?iceshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?glueshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?cursyshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?impactshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?pwpShower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?frozenshower':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?slimesnow':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?splintersnow':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?icesnow':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?sparksnow':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                               
                elif m == '?sweatsnow':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?frozenbomb':
                    if self.checkMod(nick):
                        if a == []:
                            bs.screenMessage('Pick All or One Specific Player',color=(1,1,1), clients=[clientID], transient=True)
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

                elif m == '?cmr':
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
                        
                #this is the new system for configuration commands.
                elif m == '?gluef': 
                    if self.checkMod(nick):
                        if set_spaz.glue_bomb == True:
                            set_spaz.glue_bomb = False
                            gluebombFalse()
                        else:
                            set_spaz.glue_bomb = True
                            gluebombTrue()
                        k = set_spaz.glue_bomb
                        bs.screenMessage('Glue bomb turned ---> '+str(k)) 
                elif m == '?impactf': 
                    if self.checkMod(nick):
                        if set_spaz.impact_bomb == True:
                            set_spaz.impact_bomb = False
                            impactbombFalse()
                        else:
                            set_spaz.impact_bomb = True
                            impactbombTrue()
                        k = set_spaz.impact_bomb
                        bs.screenMessage('Impact bomb turned ---> '+str(k)) 
                elif m == '?icef': 
                    if self.checkMod(nick):
                        if set_spaz.ice_bomb == True:
                            set_spaz.ice_bomb = False
                            icebombFalse()
                        else:
                            set_spaz.ice_bomb = True
                            icebombTrue()
                        k = set_spaz.ice_bomb
                        bs.screenMessage('Ice bomb turned ---> '+str(k)) 
                elif m == '?shockf': 
                    if self.checkMod(nick):
                        if set_spaz.shock_wave == True:
                            set_spaz.shock_wave = False
                            shockwaveFalse()
                        else:
                            set_spaz.shock_wave = True
                            shockwaveTrue()
                        k = set_spaz.shock_wave
                        bs.screenMessage('Shock bomb turned ---> '+str(k)) 
                elif m == '?spikef': 
                    if self.checkMod(nick):
                        if set_spaz.spike_bomb == True:
                            set_spaz.spike_bomb = False
                            spikebombFalse()
                        else:
                            set_spaz.spike_bomb = True
                            spikebombTrue()
                        k = set_spaz.spike_bomb
                        bs.screenMessage('Spike bomb turned ---> '+str(k))
                elif m == '?stickyf': 
                    if self.checkMod(nick):
                        if set_spaz.sticky_bomb == True:
                            set_spaz.sticky_bomb = False
                            stickybombFalse()
                        else:
                            set_spaz.sticky_bomb = True
                            stickybombTrue()
                        k = set_spaz.sticky_bomb
                        bs.screenMessage('Sticky bomb turned ---> '+str(k))
                elif m == '?spazf': 
                    if self.checkMod(nick):
                        if set_spaz.spaz_bomb == True:
                            set_spaz.spaz_bomb = False
                            spazbombFalse()
                        else:
                            set_spaz.spaz_bomb = True
                            spazbombTrue()
                        k = set_spaz.spaz_bomb
                        bs.screenMessage('Spaz bomb turned ---> '+str(k))
                elif m == '?knockf': 
                    if self.checkMod(nick):
                        if set_spaz.knock_bomb == True:
                            set_spaz.knock_bomb = False
                            knockbombFalse()
                        else:
                            set_spaz.knock_bomb = True
                            knockbombTrue()
                        k = set_spaz.knock_bomb
                        bs.screenMessage('Knock bomb turned ---> '+str(k)) 
                elif m == '?powslime': 
                    if self.checkMod(nick):
                        if set_pwp.powSlime == True:
                            set_pwp.powSlime = False
                            powlimeFalse()
                        else:
                            set_pwp.powSlime = True
                            powslimeTrue()
                        k = set_pwp.powSlime
                        bs.screenMessage('Pwp slime turned ---> '+str(k)) 
                elif m == '?powsplint': 
                    if self.checkMod(nick):
                        if set_pwp.powSplint == True:
                            set_pwp.powSplint = False
                            pwpsplintFalse()
                        else:
                            set_pwp.powSplint = True
                            pwpsplintTrue()
                        k = set_pwp.powSplint
                        bs.screenMessage('Pwp splint turned ---> '+str(k)) 
                elif m == '?powsweat': 
                    if self.checkMod(nick):
                        if set_pwp.powSweat == True:
                            set_pwp.powSweat = False
                            powsweatFalse()
                        else:
                            set_pwp.powSweat = True
                            powsweatTrue()
                        k = set_pwp.powSweat
                        bs.screenMessage('Pwp sweat turned ---> '+str(k))    
                elif m == '?powice': 
                    if self.checkMod(nick):
                        if set_pwp.powIce == True:
                            set_pwp.powIce = False
                            powiceFalse()
                        else:
                            set_pwp.powIce = True
                            powiceTrue()
                        k = set_pwp.powIce
                        bs.screenMessage('Pwp ice turned ---> '+str(k))    
                elif m == '?santaf': 
                    if self.checkMod(nick):
                        if set_spaz.santa == True:
                            set_spaz.santa = False
                            santaFalse()
                        else:
                            set_spaz.santa = True
                            santaTrue()
                        k = set_spaz.santa
                        bs.screenMessage('Santa Char turned ---> '+str(k))   
                elif m == '?robotf': 
                    if self.checkMod(nick):
                        if set_spaz.robot == True:
                            set_spaz.robot = False
                            robotFalse()
                        else:
                            set_spaz.robot = True
                            robotTrue()
                        k = set_spaz.robot
                        bs.screenMessage('Robot Char turned ---> '+str(k))  
                elif m == '?alif': 
                    if self.checkMod(nick):
                        if set_spaz.ali == True:
                            set_spaz.ali = False
                            aliFalse()
                        else:
                            set_spaz.ali = True
                            aliTrue()
                        k = set_spaz.ali
                        bs.screenMessage('Ali Char turned ---> '+str(k))     
                elif m == '?ninjaf': 
                    if self.checkMod(nick):
                        if set_spaz.ninja == True:
                            set_spaz.ninja = False
                            ninjaFalse()
                        else:
                            set_spaz.ninja = True
                            ninjaTrue()
                        k = set_spaz.ninja
                        bs.screenMessage('Ninja Char turned ---> '+str(k))  
                elif m == '?glovef': 
                    if self.checkMod(nick):
                        if set_spaz.defaultBoxingGloves == True:
                            set_spaz.defaultBoxingGloves = False
                            defaultgloveFalse()
                        else:
                            set_spaz.defaultBoxingGloves = True
                            defaultgloveTrue()
                        k = set_spaz.defaultBoxingGloves
                        bs.screenMessage('Default Gloves turned ---> '+str(k))  
                elif m == '?flash':
                    if self.checkMod(nick):
                        if set_pwp.flash == True:
                            set_pwp.flash = False
                            flashmodeFalse()
                        else:
                            set_pwp.flash = True
                            flashmodeTrue()
                        k = set_pwp.flash
                        bs.screenMessage('Flash mode turned ---> '+str(k)) 
                elif m == '?whitelist': 
                    if self.checkMod(nick):
                        if fire.whitelist == True:
                            fire.whitelist = False
                            whitelistFalse()
                        else:
                            fire.whitelist = True 
                            whitelistTrue()
                            def wait():
                                bsInternal.quit()
                            bs.gameTimer(200, bs.Call(wait))
                        k = fire.whitelist
                        if k == True:
                            bs.screenMessage('Rejoin the Game : Whitelist mode turned ---> True')
                            bs.screenMessage('Whitelist mode turned ---> '+str(k)) 
                        else:
                            bs.screenMessage('Whitelist mode turned ---> '+str(k))
                elif m == '?color': 
                    if self.checkMod(nick):
                        if set_spaz.colory == True:
                            set_spaz.colory = False
                            colormodeFalse()
                        else:
                            set_spaz.colory = True
                            colormodeTrue()
                        k = set_spaz.colory
                        bs.screenMessage('Color mode turned ---> '+str(k))
                elif m == '?pwp': 
                    if self.checkMod(nick):
                        if set_spaz.pwp == True:
                            set_spaz.pwp = False
                            pwpboxFalse()
                        else:
                            set_spaz.pwp = True
                            pwpboxTrue()
                        k = set_spaz.pwp
                        bs.screenMessage('Powerups turned ---> '+str(k))
                elif m == '?vanilla': 
                    if self.checkMod(nick):
                        if set_pwp.vanilla == False and set_pwp.modded_powerups == False:
                            set_pwp.vanilla = True
                            vanillaTrue()
                        else:
                            set_pwp.vanilla = False
                            vanillaFalse()
                        k = set_pwp.vanilla
                        bs.screenMessage('Vanilla Dist turned ---> '+str(k))
                elif m == '?powerups': 
                    if self.checkMod(nick):
                        if set_pwp.vanilla == False and set_pwp.modded_powerups == False:
                            set_pwp.modded_powerups = True
                            pcpowerupsTrue()
                        else:
                            set_pwp.modded_powerups = False
                            pcpowerupsFalse()
                        k = set_pwp.modded_powerups
                        bs.screenMessage('PC Pwps turned ---> '+str(k))
                elif m == '?discolight': 
                    if self.checkMod(nick):
                        if set_pwp.discoLights == True:
                            set_pwp.discoLights = False
                            discolightFalse()
                        else:
                            set_pwp.discoLights = True
                            discolightTrue()
                        k = set_pwp.discoLights
                        bs.screenMessage('DiscoLight turned ---> '+str(k))
                elif m == '?pwpshield': 
                    if self.checkMod(nick):
                        if set_pwp.powerupShield == True:
                            set_pwp.powerupShield = False
                            powerupshieldFalse()
                        else:
                            set_pwp.powerupShield = True
                            powerupshieldTrue()
                        k = set_pwp.powerupShield
                        bs.screenMessage('Powerup Shield turned ---> '+str(k))
                elif m == '?bombmodel': 
                    if self.checkMod(nick):
                        if set_bomb.bombModel == True:
                            set_bomb.bombModel = False
                            bombmodelFalse()
                        else:
                            set_bomb.bombModel = True
                            bombmodelTrue()
                        k = set_bomb.bombModel
                        bs.screenMessage('Bomb model turned ---> '+str(k))
                elif m == '?plo': 
                    if self.checkMod(nick):
                        if set_pwp.powExplo == True:
                            set_pwp.powExplo = False
                            powexploFalse()
                        else:
                            set_pwp.powExplo = True
                            powexploTrue()
                        k = set_pwp.powExplo
                        bs.screenMessage('Explosion mode turned ---> '+str(k))  
                elif m == '?shieldf': 
                    if self.checkMod(nick):
                        if set_spaz.defaultShields == True:
                            set_spaz.defaultShields = False
                            defaultshieldFalse()
                        else:
                            set_spaz.defaultShields = True
                            defaultshieldTrue()
                        k = set_spaz.defaultShields
                        bs.screenMessage('Defualt Shield turned ---> '+str(k))  
                elif m == '?rchar': 
                    if self.checkMod(nick):
                        if set_spaz.rchar == True:
                            set_spaz.rchar = False
                            rcharFalse()
                        else:
                            set_spaz.rchar = True
                            rcharTrue()
                        k = set_spaz.rchar
                        bs.screenMessage('Random Char turned ---> '+str(k))  
                elif m == '?wizardf': 
                    if self.checkMod(nick):
                        if set_spaz.wizard == True:
                            set_spaz.wizard = False
                            wizardFalse()
                        else:
                            set_spaz.wizard = True
                            wizardTrue()
                        k = set_spaz.wizard
                        bs.screenMessage('Wizard Char turned ---> '+str(k))  
                elif m == '?pixief': 
                    if self.checkMod(nick):
                        if set_spaz.pixie == True:
                            set_spaz.pixie = False
                            pixieFalse()
                        else:
                            set_spaz.pixie = True
                            pixieTrue()
                        k = set_spaz.pixie
                        bs.screenMessage('Pixie Char turned ---> '+str(k))  
                elif m == '?frostyf': 
                    if self.checkMod(nick):
                        if set_spaz.frosty == True:
                            set_spaz.frosty = False
                            frostyFalse()
                        else:
                            set_spaz.frosty = True
                            frostyTrue()
                        k = set_spaz.frosty
                        bs.screenMessage('Frosty Char turned ---> '+str(k))                         
                elif m == '?penguf': 
                    if self.checkMod(nick):
                        if set_spaz.pengu == True:
                            set_spaz.pengu = False
                            penguFalse()
                        else:
                            set_spaz.pengu = True
                            penguTrue()
                        k = set_spaz.pengu
                        bs.screenMessage('Pengu Char turned ---> '+str(k))                           
                elif m == '?verification': 
                    if self.checkMod(nick):
                        if settings.enableVerification == True:
                            settings.enableVerification = False
                            verificationFalse()
                        else:
                            settings.enableVerification = True
                            verificationTrue()
                        k = settings.enableVerification
                        bs.screenMessage('Server verification turned ---> '+str(k))        
                elif m == '?floater': 
                    if self.checkMod(nick):
                        playerlist = bsInternal._getForegroundHostActivity(
                        ).players
                        if not hasattr(bsInternal._getForegroundHostActivity(),
                                       'flo'):
                            import floater
                            bsInternal._getForegroundHostActivity().flo = floater.Floater(bsInternal._getForegroundHostActivity()._mapType())
                        floater = bsInternal._getForegroundHostActivity().flo
                        if floater.controlled:
                            bs.screenMessage(
                                'Floater is already being controlled',
                                color=(1, 0, 0))
                            return
                        for i in playerlist:
                            if i.getInputDevice().getClientID() == clientID:
                                clientID = i.getInputDevice().getClientID()
                                bs.screenMessage(
                                    'You\'ve Gained Control Over The Floater!\nPress Bomb to Throw Bombs and Punch to leave!\nYou will automatically get released after some time!',
                                    clients=[clientID],
                                    transient=True,
                                    color=(0, 1, 1))

                                def dis(i, floater):
                                    i.actor.node.invincible = False
                                    i.resetInput()
                                    i.actor.connectControlsToPlayer()
                                    floater.dis()

                                # bs.gameTimer(15000,bs.Call(dis,i,floater))
                                ps = i.actor.node.position
                                i.actor.node.invincible = True
                                floater.node.position = (ps[0], ps[1] + 1.5,
                                                         ps[2])
                                i.actor.node.holdNode = bs.Node(None)
                                i.actor.node.holdNode = floater.node2
                                i.actor.disconnectControlsFromPlayer()
                                i.resetInput()
                                floater.sourcePlayer = i
                                floater.con()
                                i.assignInputCall('pickUpPress', floater.up)
                                i.assignInputCall('pickUpRelease', floater.upR)
                                i.assignInputCall('jumpPress', floater.down)
                                i.assignInputCall('jumpRelease', floater.downR)
                                i.assignInputCall('bombPress', floater.drop)
                                i.assignInputCall('punchPress',
                                                  bs.Call(dis, i, floater))
                                i.assignInputCall('upDown', floater.updown)
                                i.assignInputCall('leftRight',
                                                  floater.leftright)
                    '''
                    if self.checkMod(nick):
                        if settings.floater == True:
                            settings.floater = False
                            floaterFalse()
                        else:
                            settings.floater = True
                            floaterTrue()
                        k = settings.floater
                        bs.screenMessage('Floater turned ---> '+str(k))    
                    '''


                elif m == '?': 
                    if self.checkVip(nick):
                        if a == []:        
                            bs.screenMessage('Special Chat For Admin',color=(1,1,1), clients=[clientID], transient=True)
                        else: 
                            try:       
                            #bs.screenMessage((a[0]),color = (1,1,1))     
                                bsUtils.ZoomText(
                                   (a[0]), maxWidth=800, lifespan=2500, jitter=2.0, position=(0, 180),
                                   flash=False, color=((0+random.random()*0.5),(0+random.random()*0.5),(0+random.random()*0.5)),
                                   trailColor=((0+random.random()*4.5),(0+random.random()*4.5),(0+random.random()*4.5))).autoRetain()
                            except:
                                 bs.screenMessage('Error has Occured',color = (1,1,1))            

                elif m == '??': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bs.screenMessage('Special Chat For Owner Only',color=(1,1,1), clients=[clientID], transient=True)
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
                    
                elif m == '?comp': 
                    if a == []:        
                        bs.screenMessage('Use /comp to complain Ex - /hekillingme\n DONT USE SPACES or it wont work',color=(1,1,1), clients=[clientID], transient=True)                         
                    else: 
                        try:       
                            bs.screenMessage('This command has been replaced with comp. Use comp for complains!',color = (1,1,1))
                        except:
                            bs.screenMessage('Complaint not send, resend',color = (1,1,1))         

                elif m == '?name': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bs.screenMessage('Simply Change server name with east',color=(1,1,1), clients=[clientID], transient=True)
                            bs.screenMessage('Server will restart after name applied',color=(1,1,1), clients=[clientID], transient=True)                
                        else: 
                            try:       
                                bsInternal._setPublicPartyName((a[0]))
                                bs.screenMessage('Party Name has been change to '+(a[0]))
                            except:
                                bs.screenMessage('Party Name not changed',color = (1,1,1))  

                elif m == '?pvt': 
                    if self.checkOwner(nick):
                        if a == []:                               
                            bs.screenMessage('Use /pvt to make server private or public',color=(1,1,1), clients=[clientID], transient=True)
                            bs.screenMessage('Use True for pvt and false for public',color=(1,1,1), clients=[clientID], transient=True)
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
                                
                elif m == '?bombname': 
                    if self.checkMod(nick):
                        if set_bomb.bombName == True:
                            set_bomb.bombName = False
                        else:
                            set_bomb.bombName = True
                        k = set_bomb.bombName
                        bs.screenMessage('Bomb name turned ---> '+str(k))      
                elif m == '?bombtimer': 
                    if self.checkMod(nick):
                        if set_bomb.bombTimer == True:
                            set_bomb.bombTimer = False
                        else:
                            set_bomb.bombTimer = True
                        k = set_bomb.bombTimer
                        bs.screenMessage('Bomb timer turned ---> '+str(k))                           
                elif m == '?poweruptimer': 
                    if self.checkMod(nick):
                        if set_pwp.powerupTimer == True:
                            set_pwp.powerupTimer = False
                        else:
                            set_pwp.powerupTimer = True
                        k = set_pwp.powerupTimer
                        bs.screenMessage('Powerup timer turned ---> '+str(k))                           
                elif m == '?powerupname': 
                    if self.checkMod(nick):
                        if set_pwp.powerupName == True:
                            set_pwp.powerupName = False
                        else:
                            set_pwp.powerupName = True
                        k = set_pwp.powerupName
                        bs.screenMessage('Powerup name turned ---> '+str(k))                  
                elif m == '?animate': 
                    if self.checkMod(nick):
                        if set_pwp.animate == True:
                            set_pwp.animate = False
                        else:
                            set_pwp.animate = True
                        k = set_pwp.animate
                        bs.screenMessage('Animation turned ---> '+str(k))                  
                elif m == '?randomchar': 
                    if self.checkMod(nick):
                        if set_spaz.randomChar == True:
                            set_spaz.randomChar = False
                        else:
                            set_spaz.randomChar = True
                        k = set_spaz.randomChar
                        bs.screenMessage('Random char turned ---> '+str(k))                  
                elif m == '?hp': 
                    if self.checkMod(nick):
                        if set_spaz.hp == True:
                            set_spaz.hp = False
                            settings.enableStats = True
                        else:
                            set_spaz.hp = True
                            settings.enableStats = False
                        k = set_spaz.hp
                        bs.screenMessage('HP tag turned ---> '+str(k))                  
                elif m == '?tag': 
                    if self.checkMod(nick):
                        if set_spaz.tag == True:
                            set_spaz.tag = False
                            settings.enableStats = True
                        else:
                            set_spaz.tag = True
                            settings.enableStats = False
                        k = set_spaz.tag
                        bs.screenMessage('Free tag turned ---> '+str(k))                  
                elif m == '?pop': 
                    if self.checkMod(nick):
                        if set_spaz.nameP == True:
                            set_spaz.nameP = False
                        else:
                            set_spaz.nameP = True
                        k = set_spaz.nameP
                        bs.screenMessage('Popup text turned ---> '+str(k))                  
                elif m == '?lightning': 
                    if self.checkMod(nick):
                        if set_pwp.lightning == True:
                            set_pwp.lightning = False
                        else:
                            set_pwp.lightning = True
                        k = set_pwp.lightning
                        bs.screenMessage('Powerup lightning turned ---> '+str(k))                       
                elif m == '?clearverification':
                    if self.checkMod(nick):
                        MID.verify = []
                        bs.screenMessage('Verification has been cleared!')
                elif m == '?clearban':
                    if self.checkMod(nick):
                        MID.verify = []
                        bs.screenMessage('Ban has been cleared!')
                elif m == '?muteall':
                    if settings.muteAll == True:
                        settings.muteAll = False
                        muteOff()
                    else:
                        settings.muteAll = True
                        muteOn()
                    k = settings.muteAll
                    bs.screenMessage('Muting everyone turned --> '+str(k))

                        
                elif m == '?egg1':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg1')
                    except:
                        pass                  
                elif m == '?egg2':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg2')
                    except:
                        pass                        
                elif m == '?egg3':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg3')
                    except:
                        pass                        
                elif m == '?egg4':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('egg4')
                    except:
                        pass                        
                elif m == '?crossOut':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('crossOut')
                    except:
                        pass
                elif m == '?crossOutMask':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('crossOutMask')
                    except:
                        pass
                elif m == '?ouyaU':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('ouyaUbutton')
                    except:
                        pass
                elif m == '?ouyaO':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('ouyaObutton')
                    except:
                        pass
                elif m == '?rgb':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('rgbStripes')
                    except:
                        pass
                elif m == '?ouyaA':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('ouyaAbutton')
                    except:
                        pass
                elif m == '?heel':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('achievementStayinAlive')
                    except:
                        pass
                elif m == '?tnt':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('achievementTNT')
                    except:
                        pass
                elif m == '?ali':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('aliColor')
                    except:
                        pass
                elif m == '?icon':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('graphicsIcon')
                    except:
                        pass
                elif m == '?level':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('levelIcon')
                    except:
                        pass
                elif m == '?eg1':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('eggTex1')
                    except:
                        pass
                elif m == '?eg2':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('eggTex2')
                    except:
                        pass
                elif m == '?eg3':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('eggTex3')
                    except:
                        pass
                elif m == '?emoji':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('fontExtras2')
                    except:
                        pass
                elif m == '?flag':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('flagColor')
                    except:
                        pass
                elif m == '?b':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.self.model = bs.getModel('tnt')
                    except:
                        pass
                elif m == '?circle':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('gameCircleIcon')
                    except:
                        pass
                elif m == '?opera':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('operaSingerIconColorMask')
                    except:
                        pass
                elif m == '?she':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('powerupShield')
                    except:
                        pass
                elif m == '?impac':
                    try:
                        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture('impactBombColor')
                    except:
                        pass
                        
                elif m=='?power':
                    if self.checkMod(nick):
                     bs.screenMessage('Type any powerup name in lower case EX: stickybomb all', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m=='?snowy':
                    if self.checkMod(nick):
                     bs.screenMessage('Special Snowfall: ?sweatsnow, ?splintersnow, ?sparksnow, ?slimesnow', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m=='?shower':
                    if self.checkMod(nick):
                     bs.screenMessage('Special Shower: ?cursyshower, ?stickyshower, ?impactshower, ?iceshower, ?glueshower, ?normalshower, ?frozenshower', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m=='?mode':
                    if self.checkMod(nick):
                     bs.screenMessage('Server Configs: ?powerupshield, ?powerupname, ?tag, ?hp, ?discolight, ?bombmodel', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
 
                elif m=='?mode3':
                    if self.checkMod(nick):
                     bs.screenMessage('?bombName, ?(char)+f, ?plo, ?pop, ?animate, ?pwp, ?powerups', clients=[clientID], transient=True)
                     bs.screenMessage('?rchar, ?randomchar, ?color', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                     
                elif m=='?mode2':
                    if self.checkMod(nick):
                     bs.screenMessage('?flash, ?floater, ?white, ?name, ?pvt, ?shieldf, ?glovef', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                     
                elif m=='?server':
                     bs.screenMessage('Server configs: ?mode, ?mode2, ?mode3', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m=='?config':
                    if self.checkMod(nick):
                     bs.screenMessage('Special Server Configs: ?server, ?maps, ?snowy, ?shower', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m=='?info':
                    bs.screenMessage('Server fully modded by PC||Modder or PC||231392', clients=[clientID], transient=True)
                    bs.screenMessage('Special thanks to Blitz and SobyDamn and Vivek', clients=[clientID], transient=True) 
                    
                elif m=='?snowe':
                    if self.checkMod(nick):              
                     texture(tex='flagColor')
                     g2()
                    
                elif m=='?snowe2':
                    if self.checkMod(nick):
                     texture(tex='crossOutMask')      
                     o()
                    
                elif m=='?red':
                    if self.checkMod(nick):     
                     texture(tex='crossOutMask')
                     g2()
                    
                elif m=='?dark':
                    if self.checkMod(nick):        
                     texture(tex='crossOutMask')
                     r2()
                    
                elif m=='?colorful':
                    if self.checkMod(nick):                   
                     texture(tex='crossOutMask')
                     g2()
                     tint(a=1, b=1, c=1)
                    
                elif m=='?smooth':
                    if self.checkMod(nick): 
                     texture(tex='achievementStayinAlive')                     
                     g2()
                    
                elif m=='?dirt':
                    if self.checkMod(nick):
                     texture(tex='impactBombColor')
                     g2()
                    
                elif m=='?dirt2':
                    if self.checkMod(nick):
                     texture(tex='impactBombColor')
                     r()
                    
                elif m=='?pink':
                    if self.checkMod(nick):
                     texture(tex='levelIcon')
                     r()
                    
                elif m=='?yellow':
                    if self.checkMod(nick):
                     texture(tex='egg4')     
                     r()
                    
                elif m=='?smooth2':
                    if self.checkMod(nick):
                     texture(tex='achievementStayinAlive')
                     r()
                    
                elif m=='?orange':
                    if self.checkMod(nick):
                     texture(tex='aliColor')
                     ff()
                    
                elif m=='?orange2':
                    if self.checkMod(nick):
                     texture(tex='aliColor')
                     o()
                    
                elif m=='?red2':
                    if self.checkMod(nick):
                     texture(tex='crossOutMask')
                     ff()
                    
                elif m=='?red3':
                    if self.checkMod(nick):
                     texture(tex='crossOutMask')
                     g()
                    
                elif m=='?red4':
                    if self.checkMod(nick): 
                     texture(tex='crossOutMask')                     
                     o()                     
                    
                elif m=='?blue':
                    if self.checkMod(nick):
                     texture(tex='egg2')
                     g2()                     
                   
                elif m == '?rules':
                    bs.screenMessage('Respect is Key here and use ethical manners for speech', clients=[clientID], transient=True)
                    #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m == '?cmd':
                    bs.screenMessage('Use: ?maps, ?power, ?, ??, comp', clients=[clientID], transient=True)
                    bs.screenMessage('For Owners: ?config, and all', clients=[clientID], transient=True)
                    #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                   
                elif m == '?comp':
                    bs.screenMessage('Send complaint to server: use ?comp+urmsg', clients=[clientID], transient=True)
                    #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
 
                elif m == '?maps':
                    if self.checkMod(nick):
                     bs.screenMessage('Use: ?map1, ?map2', clients=[clientID], transient=True)
                     
                elif m == '?map1':
                    if self.checkMod(nick):
                     bs.screenMessage('New Maps Tex: ?snowe ?snowe2 ?blue ?red ?red2 ?red3 ?red4 ?orange ?orange2', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m == '?map2':
                    if self.checkMod(nick):
                     bs.screenMessage('New Maps: ?pink ?yellow ?dirt ?dirt2 ?dark ?smooth ?smooth2 ?colorful', clients=[clientID], transient=True)
                     #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                elif m == '?ip':
                    import socket
                    hostname = socket.gethostname()
                    local_ip = socket.gethostbyname(hostname)
                    bs.screenMessage('Server IP == '+local_ip,color=(1,1,1), clients=[clientID], transient=True)
                    #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)
                    
                        
                elif m=='?contact':
                    bs.screenMessage('Join the discord StormX or StormSquad!', clients=[clientID], transient=True)
                    #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)

                          
                elif m == '?help':
                    bs.screenMessage('Available commands to use: ?info ?contact ?ip ?cmd ?rules', clients=[clientID], transient=True)
                    #bs.screenMessage('All rights to PCModder', clients=[clientID], transient=True)

                elif m == '?list': #list of current players id
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
                    
                elif m == '?id':
                    for i in bsInternal._getForegroundHostActivity().players:
            
                        if i.getInputDevice().getClientID()==clientID:client=i.get_account_id()
                    bruh = True
                    if bruh: 
                        bs.screenMessage('Your Account ID ---> '+i.get_account_id(),color=(1,1,1), clients=[clientID], transient=True)
                        bs.screenMessage(bs.getSpecialChar('logoFlat'))
                    else:
                        bs.screenMessage('Error has Occured',color=(1,1,1), clients=[clientID], transient=True)

                elif m == '?ffaMode': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bs.screenMessage('Switch To FFA game Mode',color=(1,1,1), clients=[clientID], transient=True)
                        else: 
                            try:          
                                import bsTeamGame
                                #bsTeamGame.gDefaultTeamColors = ((1,1,1), (2,2,2))
                                k = bs.FreeForAllSession
                                bsInternal._newHostSession(k)
                                bsUtils._getDefaultFreeForAllPlaylist()
                                bs.screenMessage('GameMode Changed to FFA',color=(1,1,1), clients=[clientID], transient=True)
                            except:
                                bs.screenMessage('Error has Occured',color=(1,1,1), clients=[clientID], transient=True)

                elif m == '?teamMode': 
                    if self.checkOwner(nick):
                        if a == []:        
                            bs.screenMessage('Switch To Teams GameMode',color=(1,1,1), clients=[clientID], transient=True)
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

    
c = cheatOptions()

def cmnd(msg,clientID):
    if bsInternal._getForegroundHostActivity() is not None:
    
        c.opt(clientID,msg)
bs.realTimer(5000,bs.Call(bsInternal._setPartyIconAlwaysVisible,True))

import bsUI
bs.realTimer(10000,bs.Call(bsUI.onPartyIconActivate,(0,0)))

def r():
    reflections(a=-23, b=-23)                
    tint(a=0, b=0, c=1)         
    tint(a=0.5, b=0.7, c=1)
    tint(a=1, b=1, c=1)                    


def tint(a=(5), b=(2), c=(-1)):
    bs.getSharedObject('globals').tint = (float(a),float(b),float(c))
def ac(a=(5), b=(2), c=(-1)):
    bs.getSharedObject('globals').ambientColor = (float(a),float(b),float(c))

def reflections(a=(5), b=(2)):
    rs = [int(b)]
    type = 'soft' if int(a) == 0 else 'powerup'
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
        bsInternal._getForegroundHostActivity().getMap().floor.reflection = type#house of memories, viva la vida
        bsInternal._getForegroundHostActivity().getMap().floor.reflectionScale = rs
    except:
        pass
    try:
        bsInternal._getForegroundHostActivity().getMap().center.reflection = type
        bsInternal._getForegroundHostActivity().getMap().center.reflectionScale = rs
    except:
        pass

def texture(tex='gameCircleIcon'):
    try:
        bsInternal._getForegroundHostActivity().getMap().node.colorTexture = bs.getTexture(str(tex))
    except:
        pass
def floaterTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[91] = "floater = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def floaterFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[91] = "floater = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def muteOn():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[9] = "muteAll = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def muteOff():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[9] = "muteAll = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def verificationTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[10] = "enableVerification = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def verificationFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[10] = "enableVerification = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powsweatTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[21] = "powSweat = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powsweatFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[21] = "powSweat = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def pwpsplintTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[17] = "powSplint = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def pwpsplintFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[17] = "powSplint = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powslimeTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[19] = "powSlime = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powslimeFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[19] = "powSlime = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powiceTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[15] = "powIce = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powiceFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[15] = "powIce = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def gluebombTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[71] = "glue_bomb = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def gluebombFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[71] = "glue_bomb = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def knockbombTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[67] = "knock_bomb = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def knockbombFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[67] = "knock_bomb = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def spazbombTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[69] = "spaz_bomb = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def spazbombFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[69] = "spaz_bomb = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def shockwaveTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[65] = "shock_wave = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def shockwaveFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[65] = "shock_wave = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def spikebombTrue():#
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[63] = "spike_bomb = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def spikebombFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[63] = "spike_bomb = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def stickybombTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[59] = "sticky_bomb = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def stickybombFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[59] = "sticky_bomb = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def icebombTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[61] = "ice_bomb = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def icebombFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[61] = "ice_bomb = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def impactbombTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[57] = "impact_bomb = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def impactbombFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[57] = "impact_bomb = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def santaTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[42] = "santa = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def santaFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[42] = "santa = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def robotTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[44] = "robot = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def robotFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[44] = "robot = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def aliTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[40] = "ali = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def alieFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[40] = "ali = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def penguTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[46] = "pengu = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def penguFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[46] = "pengu = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def frostyTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[36] = "frosty = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def frostyFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[36] = "frosty = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def ninjaTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[50] = "ninja = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def ninjaFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[50] = "ninja = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def pixieTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[48] = "pixie = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def pixieFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[48] = "pixie = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def wizardTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[38] = "wizard = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def wizardFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[38] = "wizard = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def rcharTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[34] = "rchar = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def rcharFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[34] = "rchar = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def defaultshieldTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[15] = "defaultShields = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def defaultshieldFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[15] = "defaultShields = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def defaultgloveTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[13] = "defaultBoxingGloves = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def defaultgloveFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[13] = "defaultBoxingGloves = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def flashmodeTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[28] = "flash = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def flashmodeFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[28] = "flash = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close() 
def powexploTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[26] = "powExplo = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powexploFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[26] = "powExplo = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def whitelistTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[6] = "whitelist = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def whitelistFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[6] = "whitelist = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/fire.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def colormodeTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[23] = "colory = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def colormodeFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[23] = "colory = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def pcpowerupsTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[6] = "modded_powerups = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def pcpowerupsFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[6] = "modded_powerups = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def vanillaTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[8] = "vanilla = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def vanillaFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[8] = "vanilla = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def pwpboxTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[7] = "pwp = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def pwpboxFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[7] = "pwp = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_spaz.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def discolightTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[36] = "discoLights = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def discolightFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[36] = "discoLights = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def powerupshieldTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[34] = "powerupShield = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def powerupshieldFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[34] = "powerupShield = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_powerups.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def bombmodelTrue():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_bombs.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[9] = "bombModel = True\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_bombs.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()  
def bombmodelFalse():
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_bombs.py",'r')
    list_of_lines = a_file.readlines()
    list_of_lines[9] = "bombModel = False\n"
    a_file = open(bs.getEnvironment()['systemScriptsDirectory'] + "/settings_bombs.py",'w')
    a_file.writelines(list_of_lines)
    a_file.close()
def m():
    tint(a=0, b=0, c=1)
    tint(a=2, b=0, c=0)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))    
def ff():
    reflections(a=-12, b=-12)
    tint(a=0, b=0, c=1)
    tint(a=0.5, b=0.7, c=1)
    tint(a=1, b=1, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8)) 
def g():
    reflections(a=12, b=12)
    tint(a=0, b=0, c=1)
    tint(a=0.5, b=0.7, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
def o():
    ac(a=12, b=12, c=12)
    reflections(a=-12, b=-12)
    ac(a=12, b=12, c=12)
    ac(a=1, b=1, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
def r3():
    reflections(a=-20, b=-15)
    tint(a=0, b=0, c=1)
    tint(a=0.5, b=0.7, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
def el():
    ac(a=12, b=12, c=12)
    bsInternal._chatMessage('?r')
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
def r4():
    reflections(a=-500, b=-500)
    tint(a=0, b=0, c=1)
    tint(a=0.5, b=0.7, c=1)
    tint(a=1, b=1, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
def vb2():
    reflections(a=-12, b=500)
    tint(a=0, b=0, c=1)
    tint(a=0.5, b=0.7, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
def vb():
    reflections(a=100, b=100)
    tint(a=0, b=0, c=1)
    tint(a=0.5, b=0.7, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))
def r2():
    reflections(a=-100, b=-100)
    tint(a=0, b=0, c=1)
    tint(a=0.5, b=0.7, c=1)
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))   
def g2():
    reflections(a=12, b=20)                          
    tint(a=0, b=0, c=1)                    
    tint(a=0.5, b=0.7, c=1)   
    bs.screenMessage("Thanks to Rocker", color=(0, 0.5, 0.8))    
    
'''    
    # ba_meta require api 7
import _ba,ba
import random
import datetime
now = datetime.datetime.now()
time = now.strftime("%Y-%m-%d %H:%M:%S"+'\n')

# ba_meta export plugin
class test(ba.Plugin):
    def __init__(self):
        self.change_bsuuid()
        #self.get_pb_id()
        #not done yet

    def change_bsuuid(self):
        #
        #
        #get the current AccountID
        a = ba.app.config
        accountid = a['Local Account Name']
        ba.screenmessage('Current ID ---> '+accountid)
        ba.AppConfig.commit(a)
        #
        #random bsuuid generator
        generator = str(random.randrange(000000,999999))
        #
        #
        #thanks to OnurV2 for path-help
        #should work on windows and linux?
        #identify the path
        #
        platform = ba.app.platform
        plugin_path = ba.app.python_directory_user
        self._bs_path = '/'.join(plugin_path.split('/' if platform == 'linux' else '\\')[0:-1])
        #
        #
        #
        #save the new bsuuid
        a_file = open(self._bs_path+'/.bsuuid','r')
        list_of_lines = a_file.readlines()
        list_of_lines[0] = generator
        a_file = open(self._bs_path+'/.bsuuid','w')
        a_file.writelines(list_of_lines)
        a_file.close()  
        #
        #
        #
        #log the old bsuuid
        f = open('bsuuid_hist.txt', "a")
        f.write('Old BSUUID ---> '+generator+'\n')
        f.write('Old AccountID ---> '+accountid+'\n')
        f.write('Time --->' +time)
        f.write('---------->\n')
        f.close()
        #
        #
        #
        #
        #Such mods created are not intended to cause damages, but simply the loopholes exist
        #done by PCMODDER
'''
