import bs
from bsSpaz import *
import bsSpaz
import bsUtils
import random
import fire
import bsInternal
import membersID as MID
import os
import json
import settings

class PermissionEffect(object):
    def __init__(self,position = (0,1,0),owner = None,prefix = 'ADMIN',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = True,particles = True):
        self.position = position
        self.owner = owner
        
         #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

        
        def a():
            self.emit()
            
        #particles    
        if particles:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)
            
        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.55, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')
        
        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':1.2,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':0.0,
                                             'hAlign':'center'})
                                             
        m.connectAttr('output', self._Text, 'position')
        
        node = bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn
        
        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color
        
    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=10,
                              scale=0.3+random.random()*1.1,
                              spread=0.1,
                              chunkType='sweat')
                              #emitType = 'stickers')
                              
class iceEffect(object):
    def __init__(self,position = (0,1,0),owner = None,prefix = 'ADMIN',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = True,particles = True):
        self.position = position
        self.owner = owner
        
         #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

        
        def a():
            self.emit()
            
        #particles    
        if particles:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)
            
        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.55, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')
        
        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':1.2,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':0.0,
                                             'hAlign':'center'})
                                             
        m.connectAttr('output', self._Text, 'position')
        
        node = bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn
        
        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color
        
    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=4,
                              scale=0.8,
                              spread=0.1,
                              chunkType='ice')
                              #emitType = 'stickers')

class slimeEffect(object):
    def __init__(self,position = (0,1,0),owner = None,prefix = 'ADMIN',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = True,particles = True):
        self.position = position
        self.owner = owner
        
         #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

        
        def a():
            self.emit()
            
        #particles    
        if particles:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)
            
        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.55, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')
        
        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':1.2,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':0.0,
                                             'hAlign':'center'})
                                             
        m.connectAttr('output', self._Text, 'position')
        
        node = bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn
        
        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color
        
    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=5,
                              scale=0.5,
                              spread=0.1,
                              chunkType='slime',
                              emitType = 'stickers')
                              

class smokeEffect(object):
    def __init__(self,position = (0,1,0),owner = None,prefix = 'ADMIN',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = True,particles = True):
        self.position = position
        self.owner = owner
        
         #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

        
        def a():
            self.emit()
            
        #particles    
        if particles:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)
            
        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.55, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')
        
        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':1.2,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':0.0,
                                             'hAlign':'center'})
                                             
        m.connectAttr('output', self._Text, 'position')
        
        node = bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn
        
        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color
        
    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=int(1.0+random.random()*4),
                              scale=0.5,
                              spread=0.1,
                              emitType='tendrils',tendrilType='smoke')
                              
class splinterEffect(object):
    def __init__(self,position = (0,1,0),owner = None,prefix = 'ADMIN',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = True,particles = True):
        self.position = position
        self.owner = owner
        
         #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

        
        def a():
            self.emit()
            
        #particles    
        if particles:
            self.timer = bs.Timer(10,bs.Call(a),repeat = True)
            
        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.55, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')
        
        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':1.2,
                                             'flatness':1.0,
                                             'color':prefixColor,
                                             'scale':0.0,
                                             'hAlign':'center'})
                                             
        m.connectAttr('output', self._Text, 'position')
        
        node = bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn
        
        #animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color',3, prefixAnim,True) #animate prefix color
        
    def emit(self):
        if self.owner.exists():
            vel = 4
            bs.emitBGDynamics(position=(self.owner.torsoPosition[0]-0.25+random.random()*0.5,self.owner.torsoPosition[1]-0.25+random.random()*0.5,self.owner.torsoPosition[2]-0.25+random.random()*0.5),
                              velocity=((-vel+(random.random()*(vel*2)))+self.owner.velocity[0]*2,(-vel+(random.random()*(vel*2)))+self.owner.velocity[1]*4,(-vel+(random.random()*(vel*2)))+self.owner.velocity[2]*2),
                              count=int(1.0+random.random()*4),
                              scale=0.5,
                              spread=0.1,
                              chunkType='splinter')
                              
class rankEffect(object):
    def __init__(self,position = (0,1,0),owner = None,prefix = 'ADMIN',prefixColor = (1,1,1),prefixAnim = {0:(1,1,1),500:(0.5,0.5,0.5)},prefixAnimate = True,particles = True):
        self.position = position
        self.owner = owner
        
         #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy

            
        #prefix
        m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.65, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')
        
        self._Text = bs.newNode('text',
                                      owner=self.owner,
                                      attrs={'text':prefix, #prefix text
                                             'inWorld':True,
                                             'shadow':1.2,
                                             'flatness':1.0,
                                             'color':(1,1,1),
                                             'scale':0.0,
                                             'hAlign':'center'})
                                             
        m.connectAttr('output', self._Text, 'position')
        
        node = bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn
                              
def __init__(self,color=(1,1,1),highlight=(0.5,0.5,0.5),character="Spaz",player=None,powerupsExpire=True):
        """
        Create a spaz for the provided bs.Player.
        Note: this does not wire up any controls;
        you must call connectControlsToPlayer() to do so.
        """
        #https://github.com/imayushsaini/Bombsquad-Mr.Smoothy-Admin-Powerup-Server
        # convert None to an empty player-ref
        if player is None: player = bs.Player(None)
        
        Spaz.__init__(self,color=color,highlight=highlight,character=character,sourcePlayer=player,startInvincible=True,powerupsExpire=powerupsExpire)
        self.lastPlayerAttackedBy = None # FIXME - should use empty player ref
        self.lastAttackedTime = 0
        self.lastAttackedType = None
        self.heldCount = 0
        self.lastPlayerHeldBy = None # FIXME - should use empty player ref here
        self._player = player
		
		
        
        profiles = []
        profiles = self._player.getInputDevice()._getPlayerProfiles()
        
        stats = False# have it turned off, logs kills not rank

        if stats:
            if os.path.exists(bs.getEnvironment()['systemScriptsDirectory'] + "/stats.json"):
                f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/stats.json", "r")
                #aid = str(pats[str(player.get_account_id())]["rank"])
                jd = {}
                try:
                    jd = json.loads(f.read())
                    aid = str(self.sourcePlayer.get_account_id())
                except Exception:
                    bs.printException()
                if aid in jd:
                    kill = jd[aid]["kills"]
                    if stats:
                        rankEffect(owner=self.node, prefix=''+str(jd[str(player.get_account_id())]["kills"]),prefixAnim = {0: (1,1,1)})
                    else:
                        rankEffect(owner=self.node, prefix='?',prefixAnim = {0: (1,1,1)})

        ###
        cName=player.getName()
        

        clID = self._player.getInputDevice().getClientID()
        

          #  https://github.com/imayushsaini/Bombsquad-modded-server-Mr.Smoothy
       
       # bsInternal._chatMessage(str(clID)+'clid')
       # bsInternal._chatMessage(str(self._player.get_account_id()))
       # bsInternal._chatMessage(str(self._player.getID()))
        cl_str = []
        
        ban = 'cum','cumshot','boob','boobies','tit','titz','fuck','fucker','shit','shithead','pussy','PuSSy','fucked','bitch','bitches','bietch','sex','Sex','bastard','Fuck','Fucker','Cum','Bitch','69'
        
        for word in ban:
            if word in cName.lower(): 
                def wow():
                    bsInternal._disconnectClient(int(player.getInputDevice().getClientID()))
                bs.gameTimer(30,bs.Call(wow))
                bs.screenMessage('You have used bad name!\n Server kicking '+cName,color=(1,1,1), clients=[clID], transient=True)
                print('Player joined game with bad Name Auto Kick = Success')
                print('Players Unique ID == '+self._player.get_account_id()+' Name used == '+player.getName())
                import socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                import datetime
                now = datetime.datetime.now()
                import platform
                f = open("kickLog.txt", "a")
                f.write('Player '+player.getName()+' joined the server with bad name. Auto Kick = Success\n')
                f.write(player.getName()+' Unique ID == '+self._player.get_account_id()+'\n')
                f.write('Time Joined == '+now.strftime("%Y-%m-%d %H:%M:%S"+'\n'))
                f.write('IP Address == '+local_ip+'\n')
                f.write('Device Name == '+hostname+'\n')
                f.write('Device Info == '+platform.system()+'\n')
                f.write('-----------------------------------------------------------------\n')
                f.close()
            
        col = '#'
        
        for word in col:
            if word in cName.lower():
                self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
                self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
                
        char = 'ninja','wizard','ali','pixie','robot','frosty','santa','pengu'
        
        for word in char:
            if word in cName.lower():
                self.node.handleMessage(bs.PowerupMessage(powerupType = word))
        
        duh = 'wow'        
        if cName[0]=='' or cName in duh:
            self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
            self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))

        playeraccountid=self._player.get_account_id()

        if playeraccountid in MID.owners:
            if settings.ownerPerk:
                self.node.handleMessage(bs.PowerupMessage(powerupType = 'punchs'))
                self.node.color = (9,9,9)
                self.node.handleMessage('celebrate',5000)
            
            self.modpack = bs.NodeActor(bs.newNode('text',
                                                  attrs={'vAttach':'bottom',
                                                         'hAttach':'right',
                                                         'hAlign':'right',
                                                         'color':(1,1,1),
                                                         'flatness':1.0,
                                                         'shadow':1.0,
                                                         'scale':0.85,
                                                         'position':(-200,5),
                                                         'text':u'\ue048Owners Are Playing\ue048'}))    

        if playeraccountid in MID.tripleMan:
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'triple'))           
            
        if playeraccountid in MID.bombMan:
            self.bombType = random.choice(['ice','sticky','impact','gluebomb','iceImpact','weedbomb']) 
            clID = self._player.getInputDevice().getClientID()
            bs.screenMessage('bombType == '+self.bombType,color=(1,1,1), clients=[clID], transient=True)


        if playeraccountid in MID.iceMan:
            self.bombType = 'ice' 

        if playeraccountid in MID.slimetrail:
            self._inv = bs.Timer(300, bs.Call(lambda self: bs.emitBGDynamics(
                     position = self.node.position,
                     count = 1, chunkType='slime',
                     scale=0.6, spread=0.01) if self.node.exists() else None, self), repeat = True)   

        if playeraccountid in MID.sparktrail:
            self._inv = bs.Timer(100, bs.Call(lambda self: bs.emitBGDynamics(
                     position = self.node.position,
                     count = 1, chunkType='spark',
                     scale=0.3, spread=0.01) if self.node.exists() else None, self), repeat = True)   

        if playeraccountid in MID.firetrail:
            self._inv = bs.Timer(100, bs.Call(lambda self: bs.emitBGDynamics(
                     position = self.node.position,
                     count = 1, chunkType='sweat',
                     scale=0.9, spread=0.01) if self.node.exists() else None, self), repeat = True)    

        if playeraccountid in MID.woodtrail:
            self._inv = bs.Timer(200, bs.Call(lambda self: bs.emitBGDynamics(
                     position = self.node.position,
                     count = 1, chunkType='splinter',
                     scale=0.6, spread=0.01) if self.node.exists() else None, self), repeat = True)       
            
        if playeraccountid in MID.spazBombMan:
            self.bombType = 'spazBomb' 
            
        if playeraccountid in MID.radiusMan:
            self.blastRadius = 5.5
            
        if playeraccountid in MID.morLife:
            self.hitPoints += 500
            
        if playeraccountid in MID.impactMan:
            self.bombType = 'impact' 
            
        if playeraccountid in MID.glueMan:
            self.bombType = 'gluebomb' 
            
        if playeraccountid in MID.speedMan:
            self.node.hockey = True     
        
        if playeraccountid in MID.crownTag:      
            tag = u'\ue043'+player.getName()+u'\ue043'         
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=self.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn            

        if playeraccountid in MID.dragonTag:        
            tag = u'\ue048'+player.getName()+u'\ue048'
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=self.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn       

        if playeraccountid in MID.helmetTag:        
            tag = u'\ue049'+player.getName()+u'\ue049'
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=self.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn          

        if playeraccountid in MID.bombTag:        
            tag = u'\ue00c'+player.getName()+u'\ue00c'
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=self.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn                 
            
        if playeraccountid in MID.invMan:
            self.node.name = ''
            self.style = 'agent'
            self.node.headModel = None
            self.node.torsoModel = None
            self.node.pelvisModel = None
            self.node.upperArmModel = None
            self.node.foreArmModel = None
            self.node.handModel = None
            self.node.upperLegModel = None
            self.node.lowerLegModel = None
            self.node.toesModel = None      

        if playeraccountid in MID.nooby:  
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'bye'))
 
        if playeraccountid in MID.glowEffect: 
            self.light = bs.newNode('light', owner=self.node, attrs={'position':self.node.position,'intensity': 1.0,'radius': 0.3, 'color': (random.random()*2.45,random.random()*2.45,random.random()*2.45)})
            self.node.connectAttr('position', self.light, 'position')
            bs.animate(self.light, "radius", {0:0, 140:0.04, 200:0.09, 400:0.078})
            bs.animate(self.light, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)
            bsUtils.animateArray(self.light, "color", 3, {0:(self.light.color[0], self.light.color[1], self.light.color[2]), 1000:(self.light.color[0]-0.4, self.light.color[1]-0.4, self.light.color[2]-0.4), 1500:(self.light.color[0], self.light.color[1], self.light.color[2])}, True)

        if playeraccountid in MID.lightEffect:
            self.nodeLight = bs.newNode('light',
                                        attrs={'position': self.node.position,
                                               'color': (0,0,1),
                                               'radius': 0.1,
                                               'volumeIntensityScale': 0.5})
            self.node.connectAttr('position', self.nodeLight, 'position')
            bs.animateArray(self.nodeLight,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
            bs.animate(self.nodeLight, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)
            
        if playeraccountid in MID.colorEffect:
            bs.animateArray(self.node,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
            
        if fire.whitelist:    
            if playeraccountid not in MID.whitelist:
                clID = self._player.getInputDevice().getClientID()
                bs.screenMessage('Account not Whitelisted sorry Contact Owner\n Server kicking '+player.getName(),color=(1,1,1), clients=[clID], transient=True)
                def kick():
                    bsInternal._disconnectClient(int(player.getInputDevice().getClientID()))
                bs.gameTimer(30,bs.Call(kick)) 
                
        if playeraccountid in MID.sparkEffect:
            def log():
                bs.emitBGDynamics(
                    position = self.node,
                    count = 20, chunkType='spark',
                    scale=0.3, spread=0.6)
            bs.gameTimer(100,bs.Call(log),repeat=True)      

        '''if playeraccountid in MID.iceEffect:
            def log():
                bs.emitBGDynamics(
                    position = self.node.position,
                    count = 20, chunkType='ice',
                    scale=0.3, spread=0.6)
            bs.gameTimer(100,bs.Call(log),repeat=True)   '''              

        if playeraccountid in MID.rejected:
            clID = self._player.getInputDevice().getClientID()
            bs.screenMessage(u"\ue043 Server has banned your Entry! \ue043\n Contact Owner for unban!", color=((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)), clients=[clID], transient=True)
            def wow():
                bsInternal._disconnectClient(int(player.getInputDevice().getClientID()))
            bs.gameTimer(30,bs.Call(wow))
            print('Banned Player '+player.getName()+' trying to join server Auto Kick = Success')
            print(player.getName()+' Unique ID == '+playeraccountid)
            import socket
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            import datetime
            now = datetime.datetime.now()
            import platform
            f = open("banLog.txt", "a")
            f.write('Banned Player '+cName+' trying to join server. Auto Kick = Success\n')
            f.write(player.getName()+' Unique ID == '+playeraccountid+'\n')
            f.write('Time Joined == '+now.strftime("%Y-%m-%d %H:%M:%S"+'\n'))
            f.write('IP Address == '+local_ip+'\n')
            f.write('Device Name == '+hostname+'\n')
            f.write('Device Info == '+platform.system()+'\n')
            f.write('-----------------------------------------------------------------\n')
            f.close()

        if playeraccountid not in MID.verify:
            if settings.enableVerification:    
               clID = self._player.getInputDevice().getClientID()
               bs.screenMessage('Verify yourself to play You have 30 seconds before server kicks!\n Type verify for verification and rejoin!',color=(1,1,1), clients=[clID], transient=True)
               def chk():
                   bs.screenMessage('Type verify for Verification and rejoin\n 20 seconds left to Verify',color=(1,1,1), clients=[clID], transient=True)
               bs.gameTimer(10000,bs.Call(chk))
   
               def chk1():
                   bs.screenMessage('Type verify for Verification and rejoin\n 10 seconds left to Verify',color=(1,1,1), clients=[clID], transient=True)
               bs.gameTimer(20000,bs.Call(chk1))
   

               def wowy():
                   bsInternal._disconnectClient(clID)
                   bs.screenMessage('Account has not been Verified to Play\n Server Kicking '+playeraccountid ,color=(1,1,1), clients=[clID], transient=True)
               bs.gameTimer(30000,bs.Call(wowy))

               def wow():
                   bsInternal._disconnectClient(clID)
                   bs.screenMessage('Account has not been Verified\n Server Kicking Player '+playeraccountid ,color=(1,1,1), clients=[clID], transient=True)
               bs.gameTimer(31000,bs.Call(wow))#just in case!
     
        
        ##
        if profiles == [] or profiles == {}:
            profiles = bs.getConfig()['Player Profiles']

        for p in profiles:
            try:
                if playeraccountid in MID.mods:
                    PermissionEffect(owner = self.node,prefix = u'\ue048MOD\ue048',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.owners:
                    PermissionEffect(owner = self.node,prefix = u'\ue048O|W|N|E|R\ue048',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.mod2:
                    PermissionEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.smokeEffect:
                    smokeEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.splinterEffect:
                    splinterEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.metalEffect:
                    metalEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.iceEffect:
                    iceEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.slimeEffect:
                    slimeEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.rejected:
                    PermissionEffect(owner = self.node,prefix = u'ANNOYING',prefixAnim = {0: (1,1,1)})
                    break
                if playeraccountid in MID.muted:
                    PermissionEffect(owner = self.node,prefix = u'Muted',prefixAnim = {0: (1,1,1)})
                    break
                if playeraccountid in MID.vips:
                    PermissionEffect(owner = self.node,prefix = u'\ue043VIP\ue043',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.vip2:
                    PermissionEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break
                if playeraccountid in MID.nooby:
                    PermissionEffect(owner = self.node,prefix = u'NOOBY',prefixAnim = {0: (1,1,1)})
                    break
                if playeraccountid in MID.members:
                    PermissionEffect(owner = self.node,prefix = u"\ue047MEMBER\ue047",prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                    break      
                
                 
            except:
                pass

        # grab the node for this player and wire it to follow our spaz (so players' controllers know where to draw their guides, etc)
        if player.exists():
            playerNode = bs.getActivity()._getPlayerNode(player)
            self.node.connectAttr('torsoPosition',playerNode,'position')

    

bsSpaz.PlayerSpaz.__init__ = __init__




