import bs,random,bsUtils,bsMap, bsGame,bsBomb,bsSpaz, bsVector,weakref
from bsUtils import Background,animate
from bsMap import *
from bsMap import _maps

def _haveNewProOptions():
    return True
bsUtils._haveProOptions = _haveNewProOptions

#Maybe in the future, but no for now
#def _haveNewPro():
#    return True
#bsUtils._havePro = _haveNewPro

class SpikesFactory(object):
    def __init__(self):
        self.puasModel = bs.getModel('flash')
        
        self.puasTex = bs.getTexture('bg')            
            
        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan',200),
                        'and',('theyAreOlderThan',200),
                        'and',('evalColliding',),
                        'and',(('theyHaveMaterial',bs.getSharedObject('footingMaterial')),
                               'or',('theyHaveMaterial',bs.getSharedObject('objectMaterial')))),
            actions=(('message','ourNode','atConnect',ImpactMessage())))
			
        self.bounceMaterial = bs.Material()		
        self.bounceMaterial.addActions(
            conditions=(('theyHaveMaterial',bs.getSharedObject('footingMaterial'))),
            actions=(('modifyPartCollision','collide',True),
                     ('modifyPartCollision','physical',True),
                     ('message','ourNode','atConnect',BounceMessage())))
        self.bounceMaterial.addActions(actions=( ("modifyPartCollision","friction",-2)))

class ImpactMessage(object):
    pass
	
class BounceMessage(object):
    pass     

class Puas(bs.Actor):
    def __init__(self,position=(0,0,0),velocity = (0,0,0),owner = None,sourcePlayer = None,expire = True,hit = True):
    
        bs.Actor.__init__(self)
        
        factory = self.getFactory()

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={'position':position,
                                      'velocity':velocity,
                                      'model':factory.puasModel,
                                      'lightModel':factory.puasModel,
                                      'body':'crate',
                                      'modelScale':0.35,
                                      'shadowSize':0.2,                                       
                                      'colorTexture':factory.puasTex,
                                      'materials':(factory.impactBlastMaterial,bs.getSharedObject('objectMaterial'))})
                                      
        if owner is None: owner = bs.Node(None)

        self.hit = hit
        self.owner = owner
        self.expire = expire
                                      
    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        try: return activity._sharedSpikesFactory
        except Exception:
            f = activity._sharedSpikesFactory = SpikesFactory()
            return f
            
    def handleMessage(self,m):
        if isinstance(m,bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m,bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m,ImpactMessage):
            node = bs.getCollisionInfo("opposingNode")
            if self.hit == True and not node is self.owner:
                bs.Blast(position = self.node.position,hitType = 'punch',blastRadius = 1).autoRetain()
            if self.expire == True:
                if self.node.exists():
                    self._lifeTime = bs.Timer(20000,bs.WeakCall(self.animBR))
                    self._clrTime = bs.Timer(20310,bs.WeakCall(self.clrBR))
            
    def animBR(self):
        if self.node.exists():
            bs.animate(self.node,"modelScale",{0:1,200:0})
        
    def clrBR(self):
        if self.node.exists():
            self.node.delete()
			
##newObjects.GoldenBomb(position=(pos[0]+1,pos[1]+2,pos[2]),velocity=(0,0,0)).autoRetain()

class BombCoin(bs.Actor):
    def __init__(self,position=(0,0,0),velocity = (0,0,0),damping = 10,gravity=0):
        bs.Actor.__init__(self)
		
        self.playMaterial = bs.Material()
        self.playMaterial.addActions(
            conditions=(('theyHaveMaterial',bs.getSharedObject('playerMaterial'))),
            actions=(('message','ourNode','atConnect',bs.HitMessage())))

        self.node = bs.newNode('prop',delegate=self,
                               attrs={'position':position,
                                      'velocity':velocity,
                                      'model':bs.getModel('puck'),
                                      'gravityScale':gravity,
                                      'damping':damping,
									  'modelScale': 0.5,
									  'bodyScale': 0.5,
                                      'reflection':'soft',
                                      'reflectionScale':[1.2],
                                      'body':'puck',
                                      'shadowSize':0.2,                                       
                                      'colorTexture':bs.getTexture('aliColor'),
                                      'materials':(bs.getSharedObject('objectMaterial'),self.playMaterial)})
									  
    def handleMessage(self,m):
        if isinstance(m,bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m,bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m,bs.HitMessage):
            if m.sourcePlayer == None: return
            bs.Blast(position = self.node.position,hitType = 'punch',blastRadius = 1).autoRetain()
            self.showGoldenMessage()
            self.registerGoldenBomb()
            self.node.handleMessage(bs.DieMessage())
            
    def showGoldenMessage(self):
        import bsMainMenu
        import bsInternal
        self._inGame = not isinstance(bsInternal._getForegroundHostSession(),bsMainMenu.MainMenuSession)
        if self._inGame:
            self.msg = bs.NodeActor(bs.newNode('text',
                         attrs={'vAttach':'top' , 'hAttach':'center',
                         'text':bs.Lstr(resource='dailyRewardsWindow.foundedBombCoinText'), 'hAlign':'left',
                         'vAlign':'center', 'shadow':1.0,
                         'flatness':1.0, 'color':(1,1,0),
                         'scale':1.2,'position':(-160,200)}))
            msgPos = self.msg.node.position
            self.img = bs.NodeActor(bs.newNode('image',attrs={'texture':bs.getTexture('coin'),
                       'position':(-200,200),'rotate':0,
                       'scale':(80,80), 'opacity':1.0,
                       'absoluteScale':True,'attach':'topCenter'}))
            imgPos = self.img.node.position
            bsUtils.animateArray(self.msg.node,"position",2,{0:msgPos,1000:(-160,-70),3000:(-160,-70),4000:(-160,200)})
            self.color = bsUtils.animateArray(self.msg.node,"color",3,{0:(1,1,1),200:(0,1,0),400:(1,1,1)},True)
            bsUtils.animateArray(self.img.node,"position",2,{0:imgPos,1000:(-200,-70),3000:(-200,-70),4000:(-200,200)})
            bs.playSound(bs.getSound('fanfare'))
            bs.gameTimer(4000,self.deleteMsg)
        else:
            bs.realTimer(100, bsUI3.GotGoldenBombWindow())
			
    def deleteMsg(self):
        self.img.node.delete()
        self.msg.node.delete()
        self.color = None
		
    def registerGoldenBomb(self):
        bsExtras.setC(bin(int(bsExtras.getC(),2)+int('1',2)))
			
class MagneticZone(bs.Actor):
    def __init__(self,position = (0,1,0),scale = 10,infinity = False,owner = None):
        bs.Actor.__init__(self)
        self.shields = []
        
        self.position = (position[0],position[1],position[2])
        self.scale = scale
        self.suckObjects = []
        self.owner = owner
        
        self.blackHoleMaterial = bs.Material()
        self.suckMaterial = bs.Material()
                                                  
        self.suckMaterial.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial'))),
                                                      actions=(("modifyPartCollision","collide",True),
                                                      ("modifyPartCollision","physical",False),
                                                      ("call","atConnect", self.touchedObj)))
                              
        self.suckRadius = bs.newNode('region',
                       attrs={'position':(self.position[0],self.position[1],self.position[2]),
                              'scale':(scale,scale,scale),
                              'type':'sphere',
                              'materials':[self.suckMaterial]})
                              
        
        if not infinity: self._dieTimer = bs.Timer(20000,bs.WeakCall(self.finish))
        bsUtils.animateArray(self.suckRadius,"scale",3,{0:(0,0,0),300:(self.scale*8,self.scale*8,self.scale*8)},True)
        
    def finish(self):
        self.suckRadius.delete()
        self.suckRadius.handleMessage(bs.DieMessage())
        for i in self.suckObjects:
            if i.exists(): i.extraAcceleration = (0,0,0)
		
    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.getNodeType() in ['prop']:#,'bomb']:
            self.suckObjects.append(node)

        if self.owner.exists():
            for i in self.suckObjects:
                if i.exists(): i.extraAcceleration = ((self.owner.position[0] - i.position[0])*6,(self.owner.position[1] - i.position[1])*6,(self.owner.position[2] - i.position[2])*6)
        else: self.finish()
							   
class VolcanoEruption(bs.Actor):
    def __init__(self, position=(0,0,0)):
        bs.Actor.__init__(self)

        self.position = position
        bs.gameTimer((random.randrange(20000,40000)),self.startEruption)
		
    def startEruption(self):
        bs.playSound(bs.getSound('alarm'))
        bsUtils.animateArray(bs.getSharedObject('globals'),'tint',3,{0:bs.getSharedObject('globals').tint,500:(1,0,0),1000:bs.getSharedObject('globals').tint,
                                                                     1500:bs.getSharedObject('globals').tint,2000:(1,0,0),2500:bs.getSharedObject('globals').tint,
                                                                     3000:bs.getSharedObject('globals').tint,3500:(1,0,0),4000:bs.getSharedObject('globals').tint})
        self.rain = bs.Timer(200,bs.WeakCall(self.dropB),repeat = True)
        bs.gameTimer(20000,self.endEruption)
		
    def endEruption(self):
        self.rain = None
        bs.gameTimer((random.randrange(20000,40000)),self.startEruption)

    def dropB(self):
        vel = ((random.randrange(-8,8)),(random.randrange(10,13)),(random.randrange(-6,6)))
        bs.Bomb(position=self.position,velocity=vel,bombType = 'lava').autoRetain()

class TimeSet(bs.Actor):
    def __init__(self, time='auto'):
        bs.Actor.__init__(self)
        self.mapsTints = {
            'Big G':{'day':(1.1, 1.2, 1.3),'night':(0.2, 0.3, 0.4)},
            'Aniversary':{'day':(1.0,1.0,1.0),'night':(0.1,0.1,0.1)},
            'Bomb Island':{'day':(1.2,1.2,1.0),'night':(0.2,0.2,0.0)},
            'Bridgit':{'day':(1.1, 1.2, 1.3),'night':(0.2, 0.3, 0.4)},
            'Chinese Temple':{'day':(0.9,1.0,1.1),'night':(0.1,0.2,0.3)},
            'Colliseum':{'day':(1.0,1.05,1.1),'night':(0.15,0.2,0.15)},
            'Courtyard':{'day':(1.2, 1.17, 1.1),'night':(0.3, 0.27, 0.2)},
            'Crag Castle':{'day':(1.15, 1.05, 0.75),'night':(0.25, 0.15, 0.05)},
            'Dominoes':{'day':(1.1,1.2,1.3),'night':(0.2,0.3,0.4)},
            'Doom Shroom':{'day':(0.82, 1.10, 1.15),'night':(0.02, 0.20, 0.25)},
            'Wooden Spinner':{'day':(0.9,0.9,0.9),'night':(0.2,0.2,0.2)},
            'Fortress':{'day':(0.9,0.9,0.9),'night':(0.2,0.2,0.2)},
            'Happy Thoughts':{'day':(1.3, 1.23, 1.0),'night':(0.3, 0.23, 0.0)},
            'Hockey Stadium':{'day':(1.2,1.3,1.33),'night':(0.2,0.3,0.33)},
            'Football Stadium':{'day':(1.3, 1.2, 1.0),'night':(0.3, 0.2, 0.0)},
            'Mini Laptop':{'day':(1,1,1),'night':(0.2,0.2,0.2)},
            'Mini Stadium':{'day':(0.8,0.8,0.8),'night':(0.15,0.15,0.15)},
            'Monkey Face':{'day':(1.0, 1.15, 1.15),'night':(0.1, 0.25, 0.25)},
            'Origami':{'day':(0.9,0.9,0.9),'night':(0.12,0.12,0.12)},
            'Rampage':{'day':(1.2, 1.1, 0.97),'night':(0.2, 0.1, 0.07)},
            'Tower D':{'day':(1.15, 1.11, 1.03),'night':(0.25, 0.21, 0.13)},
            'Roundabout':{'day':(1.0, 1.05, 1.1),'night':(0.2, 0.25, 0.3)},
            'Step Right Up':{'day':(1.2, 1.1, 1.0),'night':(0.3, 0.2, 0.1)},
            'Table':{'day':(1.0,1.0,1.0),'night':(0.12,0.12,0.12)},
            'The Pad':{'day':(1.1, 1.1, 1.0),'night':(0.2, 0.2, 0.1)},
            'U.F.O':{'day':(0.8,0.8,0.8),'night':(0.12,0.12,0.12)},
            'Volcano':{'day':(1.2,1.2,1.0),'night':(0.2,0.2,0.0)},
            'Windows':{'day':(1,1,1),'night':(0.2,0.2,0.2)},
            'Wooden Labyrinth':{'day':(1.0,1.0,1.0),'night':(0.2,0.2,0.2)},
            'Zigzag':{'day':(1.0, 1.15, 1.15),'night':(0.2,0.35,0.35)},
            'Tip Top':{'day':(0.8, 0.9, 1.3),'night':(0.1, 0.2, 0.6)},
            'Pilars':{'day':(1.0,1.0,1.0),'night':(0.2, 0.2, 0.2)},
            'Simulation Room':{'day':(1.0,1.0,1.0),'night':(0.2, 0.2, 0.2)},
        }
        self.map = bs.getActivity().getMap().getName()
        for map in self.mapsTints:
            if map == self.map:
                self.actualMap = self.mapsTints[map]
                break
		
        if time == 'Day': self.setDay()
        elif time == 'Night': self.setNight()
        else: self.automatic()
		
    def setDay(self):
        tint = self.actualMap['day']
        bsUtils.animateArray(bs.getSharedObject('globals'),'tint',3,{0:bs.getSharedObject('globals').tint,2000:tint})
        self.setTime(False)
		
    def setNight(self):
        tint = self.actualMap['night']
        bsUtils.animateArray(bs.getSharedObject('globals'),'tint',3,{0:bs.getSharedObject('globals').tint,2000:tint})
        self.setTime(True)
		
    def automatic(self):
        if self.getActualTime(): self.setDay()
        else: self.setNight()
		
    def setTime(self,value):
        bs.getConfig()["smpSettings"]['night'] =  value
        bs.writeConfig()
		
    def getActualTime(self):
        return bs.getConfig()["smpSettings"]["night"]
		
class FlyZones(bs.Actor):
    def __init__(self,):
        bs.Actor.__init__(self)
        self.zone = bs.getActivity().getMap().defs.boxes['flyZone']
        self._updateTimer = bs.Timer(100,self.update,repeat = True)
		
    def update(self):
        for player in bs.getActivity().players:
            if player.exists():
                if player.isAlive():
                    pos = player.actor.node.position
                    if bs.isPointInBox(pos,self.zone):
                        player.actor.node.fly = True
                    else: player.actor.node.fly = False
					
class GravityZones(bs.Actor):
    def __init__(self,scale=0,end=False,lifeSpan=18000,players=False):
        bs.Actor.__init__(self)
        self.objects = []
        self.scale = scale
        zone = bs.getActivity().getMap().defs.boxes['levelBounds']
        
        self.blackHoleMaterial = bs.Material()
        self.suckMaterial = bs.Material()                    
        self.suckMaterial.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial'))),
                                                      actions=(("modifyPartCollision","collide",True),
                                                      ("modifyPartCollision","physical",False),
                                                      ("call","atConnect", self.touchedObj)))
													  
        self.suckRadius = bs.newNode('region',attrs={'position':zone[0:3],
                              'scale':zone[6:9], 'type':'box','materials':[self.suckMaterial]})
					
        if players: self.updateTimer = bs.Timer(58,self.update,repeat = True)		
							  
        if end: self.dieTimer = bs.Timer(lifeSpan,bs.WeakCall(self.finish))
		
    def update(self):
        for player in bs.getActivity().players:
            if player.exists():
                if player.isAlive():
                    pos = player.actor.node.position
                    try:
                        player.actor.node.handleMessage("impulse",pos[0],pos[1]+.5,pos[2],0,5,0,3,10,0,0, 0,5,0)
                    except Exception: pass
		
    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.getNodeType() in ['prop','bomb']:
            self.objects.append(node)
            node.gravityScale = self.scale
			
    def finish(self):
        self.suckRadius.delete()
        self.suckRadius.handleMessage(bs.DieMessage())
        self.updateTimer = None
        for i in self.objects:
            if i.exists():
                i.extraAcceleration = (0,0,0)
                i.gravityScale = 1

class Water(bs.Actor):
    def __init__(self,x=0,end=False,lifeSpan=18000):
        bs.Actor.__init__(self)
        self.objects = []
        self.x = x
        zone = bs.getActivity().getMap().defs.boxes['levelBounds']
        
        self.blackHoleMaterial = bs.Material()
        self.objMat = bs.Material()                    
        self.objMat.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial'))),
                                            actions=(("modifyPartCollision","collide",True),
                                            ("modifyPartCollision","physical",False),
                                            ("call","atConnect", self.touchedObj)))
													  
        self.suckRadius = bs.newNode('region',attrs={'position':zone[0:3],
                              'scale':zone[6:9], 'type':'box','materials':[self.objMat]})
					
        self.updateTimer = bs.Timer(200,self.update,repeat = True)		
							  
        if end: self.dieTimer = bs.Timer(lifeSpan,bs.WeakCall(self.finish))
		
    def update(self):
        for obj in self.objects:
            if obj.exists() and obj.position[1] > self.x:
                try:
                    obj.gravityScale = 1
                except Exception: pass
            else:
                try:
                    obj.gravityScale = -0.3
                    vel = obj.velocity
                    obj.velocity = (vel[0]*0.7,vel[1]*0.4,vel[2]*0.7)
                except Exception: pass
		
    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.getNodeType() in ['prop','bomb']:
            self.objects.append(node)
            node.gravityScale = 0.3
			
    def finish(self):
        self.suckRadius.delete()
        self.suckRadius.handleMessage(bs.DieMessage())
        self.updateTimer = None
        for i in self.objects:
            if i.exists():
                i.extraAcceleration = (0,0,0)
                i.gravityScale = 1
