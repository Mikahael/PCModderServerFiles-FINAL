# -*- coding: utf-8 -*-
import bs
import bsUtils
import weakref
import random
import math
import time
import base64
import os,json
import bsInternal
import getPermissionsHashes as gph
from thread import start_new_thread
#from VirtualHost import DB_Handler,Language,MainSettings,_execSimpleExpression
import bsSpaz
from bsSpaz import _BombDiedMessage,_CurseExplodeMessage,_PickupMessage,_PunchHitMessage,gBasePunchCooldown,gBasePunchPowerScale,gPowerupWearOffTime,PlayerSpazDeathMessage,PlayerSpazHurtMessage
#from codecs import BOM_UTF8
import settings
import membersID as MID
import fire
import filter


class PermissionForEffect(object):
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


class PermissionEffect(object):
    def __init__(self, position=(0, 1, 0), owner=None, prefix='ADMIN', prefixColor=(1, 1, 1),
                 prefixAnim=None, prefixAnimate=True,type = 1):
        if prefixAnim is None:
            prefixAnim = {0: (1, 1, 1), 500: (0.5, 0.5, 0.5)}
        self.position = position
        self.owner = owner

        # nick
        # text
        # color
        # anim
        # animCurve
        # particles


        # prefix
        if type == 1:
            m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.80, 0), 'operation': 'add'})
        else:
            m = bs.newNode('math', owner=self.owner, attrs={'input1': (0, 1.50, 0), 'operation': 'add'})
        self.owner.connectAttr('position', m, 'input2')

        self._Text = bs.newNode('text',
                                owner=self.owner,
                                attrs={'text': prefix,  # prefix text
                                       'inWorld': True,
                                       'shadow': 1.2,
                                       'flatness': 1.0,
                                       'color': prefixColor,
                                       'scale': 0.0,
                                       'hAlign': 'center'})

        m.connectAttr('output', self._Text, 'position')

        bs.animate(self._Text, 'scale', {0: 0.0, 1000: 0.01})  # smooth prefix spawn

        # animate prefix
        if prefixAnimate:
            bsUtils.animateArray(self._Text, 'color', 3, prefixAnim, True)  # animate prefix color

class SurroundBallFactory(object):
    def __init__(self):
        self.bonesTex = bs.getTexture("powerupCurse")
        self.bonesModel = bs.getModel("bonesHead")
        self.bearTex = bs.getTexture("bearColor")
        self.bearModel = bs.getModel("bearHead")
        self.aliTex = bs.getTexture("aliColor")
        self.aliModel = bs.getModel("aliHead")
        self.b9000Tex = bs.getTexture("cyborgColor")
        self.b9000Model = bs.getModel("cyborgHead")
        self.frostyTex = bs.getTexture("frostyColor")
        self.frostyModel = bs.getModel("frostyHead")
        self.cubeTex = bs.getTexture("crossOutMask")
        self.cubeModel = bs.getModel("powerup")
        try:
            self.mikuModel = bs.getModel("operaSingerHead")
            self.mikuTex = bs.getTexture("operaSingerColor")
        except:bs.PrintException()


        self.ballMaterial = bs.Material()
        self.impactSound = bs.getSound("impactMedium")
        self.ballMaterial.addActions(actions=("modifyNodeCollision", "collide", False))


class SurroundBall(bs.Actor):
    def __init__(self, spaz, shape="bones"):
        if spaz is None or not spaz.isAlive():
            return

        bs.Actor.__init__(self)

        self.spazRef = weakref.ref(spaz)

        factory = self.getFactory()

        s_model, s_texture = {
            "bones": (factory.bonesModel, factory.bonesTex),
            "bear": (factory.bearModel, factory.bearTex),
            "ali": (factory.aliModel, factory.aliTex),
            "b9000": (factory.b9000Model, factory.b9000Tex),
            "miku": (factory.mikuModel, factory.mikuTex),
            "frosty": (factory.frostyModel, factory.frostyTex),
            "RedCube": (factory.cubeModel, factory.cubeTex)
        }.get(shape, (factory.bonesModel, factory.bonesTex))

        self.node = bs.newNode("prop",
                               attrs={"model": s_model,
                                      "body": "sphere",
                                      "colorTexture": s_texture,
                                      "reflection": "soft",
                                      "modelScale": 0.5,
                                      "bodyScale": 0.1,
                                      "density": 0.1,
                                      "reflectionScale": [0.15],
                                      "shadowSize": 0.6,
                                      "position": spaz.node.position,
                                      "velocity": (0, 0, 0),
                                      "materials": [bs.getSharedObject("objectMaterial"), factory.ballMaterial]
                                      },
                               delegate=self)

        self.surroundTimer = None
        self.surroundRadius = 1.0
        self.angleDelta = math.pi / 12.0
        self.curAngle = random.random() * math.pi * 2.0
        self.curHeight = 0.0
        self.curHeightDir = 1
        self.heightDelta = 0.2
        self.heightMax = 1.0
        self.heightMin = 0.1
        self.initTimer(spaz.node.position)

    def getTargetPosition(self, spazPos):
        p = spazPos
        pt = (p[0] + self.surroundRadius * math.cos(self.curAngle),
              p[1] + self.curHeight,
              p[2] + self.surroundRadius * math.sin(self.curAngle))
        self.curAngle += self.angleDelta
        self.curHeight += self.heightDelta * self.curHeightDir
        if self.curHeight > self.heightMax or self.curHeight < self.heightMin:
            self.curHeightDir = -self.curHeightDir

        return pt

    def initTimer(self, p):
        self.node.position = self.getTargetPosition(p)
        self.surroundTimer = bs.Timer(30, bs.WeakCall(self.circleMove), repeat=True)

    def circleMove(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        p = spaz.node.position
        pt = self.getTargetPosition(p)
        pn = self.node.position
        d = [pt[0] - pn[0], pt[1] - pn[1], pt[2] - pn[2]]
        speed = self.getMaxSpeedByDir(d)
        self.node.velocity = speed

    @staticmethod
    def getMaxSpeedByDir(direction):
        k = 7.0 / max((abs(x) for x in direction))
        return tuple(x * k for x in direction)

    def handleMessage(self, m):
        bs.Actor.handleMessage(self, m)
        if isinstance(m, bs.DieMessage):
            if self.surroundTimer is not None:
                self.surroundTimer = None
            self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())

    def getFactory(cls):
        activity = bs.getActivity()
        if activity is None: raise Exception("no current activity")
        try:
            return activity._sharedSurroundBallFactory
        except Exception:
            f = activity._sharedSurroundBallFactory = SurroundBallFactory()
            return f


class Enhancement(bs.Actor):
    def __init__(self, spaz, player):
        bs.Actor.__init__(self)
        self.sourcePlayer = player
        self.spazRef = weakref.ref(spaz)
        self.spazNormalColor = spaz.node.color
        self.Decorations = []
        self.Enhancements = []
        self._powerScale = 1.0
        self._armorScale = 1.0
        self._lifeDrainScale = None
        self._damageBounceScale = None
        self._remoteMagicDamge = False
        self._MulitPunch = None
        self._AntiFreeze = 1.0
        self.fallWings = 0
        
        self.checkDeadTimer = None
        self._hasDead = False
        self.light = None

	flag = 0
        profiles = []
        profiles = self.sourcePlayer.getInputDevice()._getPlayerProfiles()  


	cl_str = self.sourcePlayer.get_account_id()
        playeraccountid= self.sourcePlayer.get_account_id()
	clID = self.sourcePlayer.getInputDevice().getClientID()
	#print cl_str, clID
        cName = player.getName()
        bright = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
	
	
	import filter
        ban = filter.name_filter
	
        for word in ban:
            if word in cName.lower(): 
                try:
                    def wow():
                        bsInternal._disconnectClient(int(clID))
                    bs.gameTimer(30,bs.Call(wow))
                    bs.screenMessage(u'\ue043 You have used bad name in Server! \ue043\n Server kicking ---> '+cName,color=bright, clients=[clID], transient=True)
                    print('Player joined game with bad Name Auto Kick ---> Success')
                    print('Players Unique ID ---> '+playeraccountid+' Name used ---> '+cName)
                    import socket
                    hostname = socket.gethostname()
                    local_ip = socket.gethostbyname(hostname)
                    import datetime
                    now = datetime.datetime.now()
                    import platform
                    f = open("kickLog.txt", "a")
                    f.write('Player '+cName+' joined the server with bad name. Auto Kick ---> Success\n')
                    f.write(cName+' Unique ID == '+playeraccountid+'\n')
                    f.write('Time Joined == '+now.strftime("%Y-%m-%d %H:%M:%S"+'\n'))
                    f.write('IP Address == '+local_ip+'\n')
                    f.write('Device Name == '+hostname+'\n')
                    f.write('Device Info == '+platform.system()+'\n')
                    f.write('-----------------------------------------------------------------\n')
                except:
                    pass

        neet = self.spazRef()
        if playeraccountid in MID.owners:
            if settings.ownerPerk:
                spaz = self.spazRef()
                spaz.node.handleMessage(bs.PowerupMessage(powerupType = 'punchs'))
                spaz.node.color = (9,9,9)
                spaz.node.handleMessage('celebrate',5000)
            
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
            neet.node.handleMessage(bs.PowerupMessage(powerupType = 'triple'))           
            
        if playeraccountid in MID.bombMan:
            neet.bombType = random.choice(['ice','sticky','impact','gluebomb','iceImpact','weedbomb']) 
            clID = self._player.getInputDevice().getClientID()
            bs.screenMessage('bombType == '+self.bombType,color=bright, clients=[clID], transient=True)

        if playeraccountid in MID.iceMan:
            neet.bombType = 'ice' 

        if playeraccountid in MID.spazBombMan:
            neet.bombType = 'spazBomb' 
            
        if playeraccountid in MID.radiusMan:
            neet.blastRadius = 5.5
            
        if playeraccountid in MID.morLife:
            neet.hitPoints += 500
            
        if playeraccountid in MID.impactMan:
            neet.bombType = 'impact' 
            
        if playeraccountid in MID.glueMan:
            neet.bombType = 'gluebomb' 
            
        if playeraccountid in MID.speedMan:
            neet.node.hockey = True  

        if playeraccountid in MID.crownTag:      
            tag = u'\ue043'+player.getName()+u'\ue043'         
            m = bs.newNode('math', owner=neet.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            neet.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=neet.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn  

        if playeraccountid in MID.dragonTag:        
            tag = u'\ue048'+player.getName()+u'\ue048'        
            m = bs.newNode('math', owner=neet.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            neet.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=neet.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn 

        if playeraccountid in MID.helmetTag:        
            tag = u'\ue049'+player.getName()+u'\ue049'       
            m = bs.newNode('math', owner=neet.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            neet.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=neet.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn 

        if playeraccountid in MID.bombTag:        
            tag = u'\ue00c'+player.getName()+u'\ue00c'         
            m = bs.newNode('math', owner=neet.node, attrs={'input1': (0, 1.45, 0), 'operation': 'add'})
            neet.node.connectAttr('position', m, 'input2')
            self._pcText = bs.newNode('text', owner=neet.node,
                               attrs={'text':tag, 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
            m.connectAttr('output', self._pcText, 'position') 
            bs.animate(self._pcText, 'scale', {0: 0.0, 1000: 0.01}) #smooth prefix spawn    

        if playeraccountid in MID.invMan:
            neet.node.name = ''
            neet.style = 'agent'
            neet.node.headModel = None
            neet.node.torsoModel = None
            neet.node.pelvisModel = None
            neet.node.upperArmModel = None
            neet.node.foreArmModel = None
            neet.node.handModel = None
            neet.node.upperLegModel = None
            neet.node.lowerLegModel = None
            neet.node.toesModel = None      

        if playeraccountid in MID.nooby:  
            neet.node.handleMessage(bs.PowerupMessage(powerupType = 'bye'))

        if playeraccountid in MID.glowEffect: 
            self.light = bs.newNode('light', owner=neet.node, attrs={'position':neet.node.position,'intensity': 1.0,'radius': 0.3, 'color': (random.random()*2.45,random.random()*2.45,random.random()*2.45)})
            neet.node.connectAttr('position', self.light, 'position')
            bs.animate(self.light, "radius", {0:0, 140:0.04, 200:0.09, 400:0.078})
            bs.animate(self.light, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)
            bsUtils.animateArray(self.light, "color", 3, {0:(self.light.color[0], self.light.color[1], self.light.color[2]), 1000:(self.light.color[0]-0.4, self.light.color[1]-0.4, self.light.color[2]-0.4), 1500:(self.light.color[0], self.light.color[1], self.light.color[2])}, True)

        if playeraccountid in MID.lightEffect:
            self.nodeLight = bs.newNode('light',
                                        attrs={'position': neet.node.position,
                                               'color': (0,0,1),
                                               'radius': 0.1,
                                               'volumeIntensityScale': 0.5})
            neet.node.connectAttr('position', self.nodeLight, 'position')
            bs.animateArray(self.nodeLight,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
            bs.animate(self.nodeLight, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)
    
        if playeraccountid in MID.colorEffect:
            bs.animateArray(neet.node,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)

        if playeraccountid in MID.sparkEffect:
            def log():
                bs.emitBGDynamics(
                    position = self.neet,
                    count = 20, chunkType='spark',
                    scale=0.3, spread=0.6)
            bs.gameTimer(100,bs.Call(log),repeat=True) 

        '''import fire #needed
        if fire.whitelist:    
            if playeraccountid not in MID.whitelist:
                bs.screenMessage(u'\ue043 Account not Whitelisted sorry Contact Owner \ue043\n Server kicking '+cName,color=bright, clients=[clID], transient=True)
                def kick():
                    bsInternal._disconnectClient(int(clID))
                bs.gameTimer(30,bs.Call(kick)) '''
   
        if playeraccountid not in MID.verify:
            if settings.enableVerification:    
               #
               bs.screenMessage(u'\ue043 Verify yourself to play You have 30 seconds before server kicks! \ue043\n Type verify for verification and rejoin!',color=bright, clients=[clID], transient=True)
               def chk():
                   bs.screenMessage(u'\ue043 Type verify for Verification and rejoin! \ue043\n 20 seconds left to Verify',color=bright, clients=[clID], transient=True)
               bs.gameTimer(10000,bs.Call(chk))
   
               def chk1():
                   bs.screenMessage(u'\ue043 Type verify for Verification and rejoin! \ue043\n 10 seconds left to Verify',color=bright, clients=[clID], transient=True)
               bs.gameTimer(20000,bs.Call(chk1))
   

               def wowy():
                   bsInternal._disconnectClient(clID)
                   bs.screenMessage(u'\ue043 Account has not been Verified to Play! \ue043\n Server Kicking '+playeraccountid ,color=bright, clients=[clID], transient=True)
               bs.gameTimer(30000,bs.Call(wowy))

               def wow():
                   bsInternal._disconnectClient(clID)
                   bs.screenMessage(u'\ue043 Account has not been Verified! \ue043\n Server Kicking Player '+playeraccountid ,color=bright, clients=[clID], transient=True)
               bs.gameTimer(31000,bs.Call(wow))#just in case!

        if playeraccountid in MID.rejected:
            #
            bs.screenMessage(u"\ue043 Server has banned your Entry! \ue043\n Contact Owner for unban!", color=((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)), clients=[clID], transient=True)
            try:
                def wow():
                    bsInternal._disconnectClient(int(clID))
                bs.gameTimer(30,bs.Call(wow))
                print('Banned Player '+cName+' trying to join server Auto Kick = Success')
                print(cName+' Unique ID ---> '+playeraccountid)
                import socket
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                import datetime
                now = datetime.datetime.now()
                import platform
                f = open("banLog.txt", "a")
                f.write('Banned Player '+cName+' trying to join server. Auto Kick = Success\n')
                f.write(cName+' Unique ID ---> '+playeraccountid+'\n')
                f.write('Time Joined == '+now.strftime("%Y-%m-%d %H:%M:%S"+'\n'))
                f.write('IP Address == '+local_ip+'\n')
                f.write('Device Name == '+hostname+'\n')
                f.write('Device Info == '+platform.system()+'\n')
                f.write('-----------------------------------------------------------------\n')
                f.close()
            except:
                pass

        if profiles == [] or profiles == {}:
            profiles = bs.getConfig()['Player Profiles']

	def getTag(*args):
		  #if alreadyHasTag: return True
		  #profiles = self._player.getInputDevice()._getPlayerProfiles()
		  for p in profiles:
		    if '/tag' in p:
		     try:
			      tag = p.split(' ')[1]
			      if '\\' in tag:
				#print tag + ' before'
				tag =tag.replace('\d','\ue048'.decode('unicode-escape'))
				tag =tag.replace('\c','\ue043'.decode('unicode-escape'))
				tag =tag.replace('\h','\ue049'.decode('unicode-escape'))
				tag =tag.replace('\s','\ue046'.decode('unicode-escape'))
				tag =tag.replace('\\n','\ue04b'.decode('unicode-escape'))
				tag =tag.replace('\\f','\ue04f'.decode('unicode-escape'))
			      	#print tag + ' after'		
			      return tag
		     except:
			pass   
		  return '0'

        try:
		if cl_str in gph.effectCustomers:
			effect = gph.effectCustomers[cl_str]["effect"]
			if effect == 'ice':
				self.snowTimer = bs.Timer(500, bs.WeakCall(self.emitIce), repeat=True)
			elif effect == 'sweat':
				self.smokeTimer = bs.Timer(40, bs.WeakCall(self.emitSmoke), repeat=True)
			elif effect == 'scorch':
				self.scorchTimer = bs.Timer(500, bs.WeakCall(self.update_Scorch), repeat=True)
			elif effect == 'glow':
				self.addLightColor((1, 0.6, 0.4));self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)
			elif effect == 'distortion':
				self.DistortionTimer = bs.Timer(1000, bs.WeakCall(self.emitDistortion), repeat=True)
			elif effect == 'slime':
				self.slimeTimer = bs.Timer(250, bs.WeakCall(self.emitSlime), repeat=True)
			elif effect == 'metal':
				self.metalTimer = bs.Timer(500, bs.WeakCall(self.emitMetal), repeat=True)
			elif effect == 'surrounder':
				self.surround = SurroundBall(spaz, shape="bones")
                elif cl_str in gph.surroundingObjectEffect:
		    self.surround = SurroundBall(spaz, shape="bones")
		    flag = 1
                elif cl_str in gph.sparkEffect:
                    self.sparkTimer = bs.Timer(100, bs.WeakCall(self.emitSpark), repeat=True)
		    flag = 1
                elif cl_str in gph.smokeEffect:
		    self.smokeTimer = bs.Timer(40, bs.WeakCall(self.emitSmoke), repeat=True)
		    flag = 1
                elif cl_str in gph.scorchEffect:
		    self.scorchTimer = bs.Timer(500, bs.WeakCall(self.update_Scorch), repeat=True)
		    flag = 1
                elif cl_str in gph.distortionEffect:
		    self.DistortionTimer = bs.Timer(1000, bs.WeakCall(self.emitDistortion), repeat=True)
		    flag = 1
                elif cl_str in gph.glowEffect:
		    self.addLightColor((1, 0.6, 0.4));self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)
		    flag = 1
                elif cl_str in gph.iceEffect:
		    self.snowTimer = bs.Timer(500, bs.WeakCall(self.emitIce), repeat=True)
		    flag = 1
                elif cl_str in gph.slimeEffect:
		    self.slimeTimer = bs.Timer(250, bs.WeakCall(self.emitSlime), repeat=True)
		    flag = 1
                elif cl_str in gph.metalEffect:
		    self.metalTimer = bs.Timer(500, bs.WeakCall(self.emitMetal), repeat=True)
		    flag = 1
	
		if cl_str in gph.customlist:
			    PermissionEffect(owner = spaz.node,prefix =gph.customlist[cl_str],prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.customtagHashes  or cl_str in gph.topperslist:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue047M3mBeR\ue047'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.ownerHashes:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue048O|W|N|E|R\ue048'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.adminHashes:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue04cA.D.M.I.N\ue04c'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in gph.vipHashes:	
			    tag = getTag(1)
			    if tag == '0': tag = u'[V.I.P+]'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in MID.mods:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue043MOD\ue043'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in MID.owners:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue048O|W|N|E|R\ue048'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in MID.mod2:
			    tag = getTag(1)
			    if tag == '0': tag = u''
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in MID.smokeEffect:
                	    smokeEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                elif cl_str in MID.splinterEffect:
                	    splinterEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                elif cl_str in MID.metalEffect:
                	    metalEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                elif cl_str in MID.iceEffect:
                	    iceEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                elif cl_str in MID.slimeEffect:
                	    slimeEffect(owner = self.node,prefix = u'',prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)})
                elif cl_str in MID.rejected:
			    tag = getTag(1)
			    if tag == '0': tag = u'Annoying'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = None)
                elif cl_str in MID.muted:
			    tag = getTag(1)
			    if tag == '0': tag = u'Muted'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = None)
                elif cl_str in MID.vips:
			    tag = getTag(1)
			    if tag == '0': tag = u'[V.I.P+]'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in MID.vip2:
			    tag = getTag(1)
			    if tag == '0': tag = u''
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in MID.nooby:
			    tag = getTag(1)
			    if tag == '0': tag = u'Nooby'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
                elif cl_str in MID.members:
			    tag = getTag(1)
			    if tag == '0': tag = u'\ue047[MEMBER]ue047'
			    PermissionEffect(owner = spaz.node,prefix = tag,prefixAnim = {0: (1,0,0), 250: (0,1,0),250*2:(0,0,1),250*3:(1,0,0)})
        except:
                pass

	if settings.enableStats:

	    if os.path.exists(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json"):
		f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "r")
		#pats = json.loads(f.read())
		aid = str(self.sourcePlayer.get_account_id())
		pats = {}
		try:
		    pats = json.loads(f.read())	
		except Exception:
		    bs.printException()
		if aid in pats:
		    rank = pats[aid]["rank"]
		    kill = pats[aid]["kills"]
		    death = pats[aid]["deaths"]
		    if int(rank) < 6:
			#dragon='?' crown=? fireball=?	ninja=? skull=?	
			if rank == '1':
				icon = '?' #crown
				if flag == 0 and settings.enableTop5effects: self.neroLightTimer = bs.Timer(500, bs.WeakCall(self.neonLightSwitch,("shine" in self.Decorations),("extra_Highlight" in self.Decorations),("extra_NameColor" in self.Decorations)),repeat = True)
			elif rank == '2': 
				icon = '?' #dragon
				if flag ==0 and settings.enableTop5effects: self.smokeTimer = bs.Timer(40, bs.WeakCall(self.emitSmoke), repeat=True)
			elif rank == '3': 
				icon ='?' #helmet'
				if flag == 0 and settings.enableTop5effects: self.addLightColor((1, 0.6, 0.4));self.scorchTimer = bs.Timer(500, bs.WeakCall(self.update_Scorch), repeat=True)
			elif rank == '4': 
				icon = '?' #fireball
				if flag ==0 and settings.enableTop5effects: self.metalTimer = bs.Timer(500, bs.WeakCall(self.emitMetal), repeat=True)

			else: 
				icon = '?' #bull head  
				if flag==0 and settings.enableTop5effects: self.addLightColor((1, 0.6, 0.4));self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)
			display = icon + '#' + str(rank) +icon
		        PermissionEffect(owner = spaz.node,position=(0,2,0),prefix = display,prefixAnim = {0: (1,1,1)},type = 2)
		    else:
			display = '#' + str(rank)
		        PermissionEffect(owner=spaz.node, position=(0,2,0), prefix=u'#' + str(pats[str(player.get_account_id())]["rank"]),
		                     prefixAnim={0: (1,1,1)},type=2)
	

        if "smoke" and "spark" and "snowDrops" and "slimeDrops" and "metalDrops" and "Distortion" and "neroLight" and "scorch" and "HealTimer" and "KamikazeCheck" not in self.Decorations:
            #self.checkDeadTimer = bs.Timer(150, bs.WeakCall(self.checkPlayerifDead), repeat=True)

            if self.sourcePlayer.isAlive() and isinstance(self.sourcePlayer.actor,bs.PlayerSpaz) and self.sourcePlayer.actor.node.exists():
                #print("OK")
                self.sourcePlayer.actor.node.addDeathAction(bs.Call(self.handleMessage,bs.DieMessage()))


    def checkPlayerifDead(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.checkDeadTimer = None
            self.handleMessage(bs.DieMessage())
            return
    def update_Scorch(self):
        spaz = self.spazRef()
        if spaz is not None and spaz.isAlive() and spaz.node.exists():
            color = (random.random(),random.random(),random.random())
            if not hasattr(self,"scorchNode") or self.scorchNode == None:
                self.scorchNode = None
                self.scorchNode = bs.newNode("scorch",attrs={"position":(spaz.node.position),"size":1.17,"big":True})
                spaz.node.connectAttr("position",self.scorchNode,"position")
            bsUtils.animateArray(self.scorchNode,"color",3,{0:self.scorchNode.color,500:color})
        else:
            self.scorchTimer = None
            self.scorchNode.delete()
            self.handleMessage(bs.DieMessage())
        
    def neonLightSwitch(self,shine,Highlight,NameColor):
        spaz = self.spazRef()
        if spaz is not None and spaz.isAlive() and spaz.node.exists():
            color = (random.random(),random.random(),random.random())
            if NameColor:
                bsUtils.animateArray(spaz.node,"nameColor",3,{0:spaz.node.nameColor,500:bs.getSafeColor(color)})
            if shine:color = tuple([min(10., 10 * x) for x in color])
            bsUtils.animateArray(spaz.node,"color",3,{0:spaz.node.color,500:color})
            if Highlight:
                #print spaz.node.highlight
                color = (random.random(),random.random(),random.random())
                if shine:color = tuple([min(10., 10 * x) for x in color])
                bsUtils.animateArray(spaz.node,"highlight",3,{0:spaz.node.highlight,500:color})
        else:
            self.neroLightTimer = None
            self.handleMessage(bs.DieMessage())

 
    def addLightColor(self, color):
        self.light = bs.newNode("light", attrs={"color": color,
                                                "heightAttenuated": False,
                                                "radius": 0.4})
        self.spazRef().node.connectAttr("position", self.light, "position")
        bsUtils.animate(self.light, "intensity", {0: 0.1, 250: 0.3, 500: 0.1}, loop=True)
        
    def emitDistortion(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position,emitType="distortion",spread=1.0)
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity,count=random.randint(1,5),emitType="tendrils",tendrilType="smoke")

        
    def emitSpark(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity, count=random.randint(1,10), scale=2, spread=0.2,
                          chunkType="spark")
    def emitIce(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position , velocity=spaz.node.velocity, count=random.randint(2,8), scale=0.4, spread=0.2,
                          chunkType="ice")
    def emitSmoke(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity, count=random.randint(1,10), scale=2, spread=0.2,
                          chunkType="sweat")
    def emitSlime(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position , velocity=spaz.node.velocity, count=random.randint(1,10), scale=0.4, spread=0.2,
                          chunkType="slime")
    def emitMetal(self):
        spaz = self.spazRef()
        if spaz is None or not spaz.isAlive() or not spaz.node.exists():
            self.handleMessage(bs.DieMessage())
            return
        bs.emitBGDynamics(position=spaz.node.position, velocity=spaz.node.velocity, count=random.randint(2,8), scale=0.4, spread=0.2,
                          chunkType="metal")

    def handleMessage(self, m):
        #self._handleMessageSanityCheck()
        
        if isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())
        elif isinstance(m, bs.DieMessage):
            if hasattr(self,"light") and self.light is not None:self.light.delete()
            if hasattr(self,"smokeTimer"):self.smokeTimer = None
            if hasattr(self,"surround"):self.surround = None
            if hasattr(self,"sparkTimer"):self.sparkTimer = None
            if hasattr(self,"snowTimer"):self.snowTimer = None
            if hasattr(self,"metalTimer"):self.metalTimer = None
            if hasattr(self,"DistortionTimer"):self.DistortionTimer = None
            if hasattr(self,"slimeTimer"):self.slimeTimer = None
            if hasattr(self,"KamikazeCheck"):self.KamikazeCheck = None
            if hasattr(self,"neroLightTimer"):self.neroLightTimer = None
            if hasattr(self,"checkDeadTimer"):self.checkDeadTimer = None
            if hasattr(self,"HealTimer"):self.HealTimer = None
            if hasattr(self,"scorchTimer"):self.scorchTimer = None
            if hasattr(self,"scorchNode"):self.scorchNode = None
            if not self._hasDead:
                spaz = self.spazRef()
                #print str(spaz) + "Spaz"
                if spaz is not None and spaz.isAlive() and spaz.node.exists():
                    spaz.node.color = self.spazNormalColor
                killer = spaz.lastPlayerAttackedBy if spaz is not None else None
                try:
                    if killer in (None,bs.Player(None)) or killer.actor is None or not killer.actor.exists() or killer.actor.hitPoints <= 0:killer = None
                except:killer = None
                #if hasattr(self,"hasDead") and not self.hasDead:
                
                self._hasDead = True
            
        bs.Actor.handleMessage(self, m)


def _Modify_BS_PlayerSpaz__init__(self, color=(1, 1, 1), highlight=(0.5, 0.5, 0.5), character="Spaz", player=None,
                           powerupsExpire=True):
    if player is None: player = bs.Player(None)

    bsSpaz.Spaz.__init__(self, color=color, highlight=highlight, character=character, sourcePlayer=player,
                     startInvincible=True, powerupsExpire=powerupsExpire)
    self.lastPlayerAttackedBy = None  # FIXME - should use empty player ref
    self.lastAttackedTime = 0
    self.lastAttackedType = None
    self.heldCount = 0
    self.lastPlayerHeldBy = None  # FIXME - should use empty player ref here
    self._player = player

    # grab the node for this player and wire it to follow our spaz (so players" controllers know where to draw their guides, etc)
    if player.exists():
        playerNode = bs.getActivity()._getPlayerNode(player)
        self.node.connectAttr("torsoPosition", playerNode, "position")
    
    self.HasEnhanced = False
    self.Enhancement = Enhancement(self, self.sourcePlayer).autoRetain()

bsSpaz.PlayerSpaz.__init__ = _Modify_BS_PlayerSpaz__init__
