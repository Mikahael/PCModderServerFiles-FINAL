from random import randint
import random
import bs
import math
import bsUtils

class PortalFactory(object):

    def __init__(self):
        self.shitModel = bs.getModel('bomb')
        self.turretModel = bs.getModel('bomb')
        self.badrockModel = bs.getModel('bomb')
        self.turretClosedModel = bs.getModel('bomb')
        self.companionCubeModel = bs.getModel('bomb')

        self.weightCubeTex = bs.getTexture('bg')
        self.minecraftTex = bs.getTexture('bg')
        self.companionCubeTex = bs.getTexture('bg')

        self.activateSound = bs.getSound('activateBeep')

        self.legoMaterial = bs.Material()
        self.legoMaterial.addActions(
            conditions=(('theyHaveMaterial', self.legoMaterial)),
            actions=('message', 'ourNode', 'atConnect', LegoConnect()))

        self.legoMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=('message', 'ourNode', 'atConnect',
                     LegoMessage()))

        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan', 200),
                        'and', ('theyAreOlderThan', 200),
                        'and', ('evalColliding',),
                        'and', (('theyHaveMaterial',
                                 bs.getSharedObject('footingMaterial')),
                                'or', ('theyHaveMaterial',
                                       bs.getSharedObject('objectMaterial')))),
            actions=(('message', 'ourNode', 'atConnect', ImpactMessage())))


class Something(bs.Actor): # TODO - give normal name)
    '''
    Just try do any object without bs.Bomb
'''
    def __init__(self, position=(0, 1, 0), velocity=(0,0,0), deathTimeout = (False, 0)):
        bs.Actor.__init__(self)
        activity = self.getActivity()
        self.rType=randint(0,2)
        self.color=self.getColor(self.rType)
        self.material=self.getMaterial(self.rType)
        self.bodyNode = bs.newNode(
            'prop',
            delegate=self,
            attrs={
                'extraAcceleration':(0,16,0),
                'body':'sphere',
                'position':position,
                'velocity':velocity,
                'materials':[
                    bs.getSharedObject('objectMaterial'),
                    self.material]
                })
        self.node = bs.newNode(
            'shield',
            owner=self.bodyNode,
            attrs={
                'color':self.color,
                'radius':0.7})
        self.bodyNode.connectAttr('position', self.node, 'position')
        if deathTimeout[0]:
            bs.gameTimer(deathTimeout[1], bs.Call(self.handleMessage, bs.DieMessage()))

    def getColor(self, i):
        self.colors=[(8,0,0),(0,0,4),(4,0,8)] # Health, freeze, curse
        return self.colors[i]

    def getMaterial(self, i):
        self.materialHealth=bs.Material()
        self.materialFreeze=bs.Material()
        self.materialCurse=bs.Material()
        
        
        # Setup Health  
        self.materialHealth.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('healt')))              
        # Setup Freeze
        self.materialFreeze.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('freeze')))     
        # Setup Curse
        self.materialCurse.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('curs')))
        self.materials=[self.materialHealth, self.materialFreeze, self.materialCurse]
        return self.materials[i]

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node is not None and self.node.exists():
                bs.playSound(bs.getSound('shatter'),
                             position = self.node.position)
                bs.emitBGDynamics(position = self.node.position,
                                  velocity = (0, 4, 0),
                                  count = 14, scale = 0.8,
                                  chunkType = 'spark', spread = 1.5)
            self.node.delete()
            self.bodyNode.delete()
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.bodyNode.delete()

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(
                "impulse", m.pos[0], m.pos[1], m.pos[2], m.velocity[0],
                m.velocity[1], m.velocity[2], 1.0 * m.magnitude,
                1.0 * m.velocityMagnitude, m.radius, 0, m.forceDirection[0],
                m.forceDirection[1], m.forceDirection[2])

        else:
            bs.Actor.handleMessage(self, m)



class BuildBlock(bs.Actor):
    
    def __init__(self, position=(0,1,0)):
        
        bs.Actor.__init__(self)

        # Where do we place block?
        self.loc=bs.newNode('shield',
                            attrs={'position':position,
                                   'radius':0.01})

        # Block
        self.body=bs.newNode('prop',
                             delegate=self,
                             attrs={'body':'box',
                                    'modelScale':1,
                                    'bodyScale':1,
                                    'model':bs.getModel('tnt'),
                                    'colorTexture':bs.getTexture('tnt'),
                                    'materials':[bs.getSharedObject('footingMaterial')]})
        self.loc.connectAttr('position', self.body, 'position')

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.body.delete()
            self.loc.delete()
            activity = self.getActivity()
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.body.delete()
            self.loc.delete()

        else:
            bs.Actor.handleMessage(self, m)

class MagicGenerator(bs.Actor):

    def __init__(self, position = (0,1,0), maxBalls = 5):

        bs.Actor.__init__(self)

        self.balls = []

        self.maxBalls = maxBalls

        self.node = bs.newNode('prop', delegate = self,
                               attrs = {
                                   'extraAcceleration':(0,18,0),
                                   'position':position,
                                   'model':bs.getModel('tnt'),
                                   'lightModel':bs.getModel('tnt'),
                                   'body':'crate',
                                   'shadowSize':0.5,
                                   'colorTexture':bs.getTexture('achievementFlawlessVictory'),
                                   'reflection':'soft',
                                   'reflectionScale':[1],
                                   'materials':[bs.getSharedObject('objectMaterial')]})
        self.timer = bs.Timer(5000, bs.Call(self.spawnBall), repeat = True)

    def spawnBall(self):
        for i in range(len(self.balls)):
            if not self.balls[i].node.exists():
                del self.balls[i]
                i -= 1

        if len(self.balls) >= self.maxBalls: return
        x, y, z = self.node.position
        y += 2
        self.balls.append(Something((x,y,z)))

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.HitMessage):
            bs.playSound(bs.getSound('shatter'),
                         position = self.node.position)
            bs.emitBGDynamics(position = self.node.position,
                              velocity = (0, 4, 0),
                              count = 14, scale = 0.8,
                              chunkType = 'spark', spread = 1.5)
            self.node.delete()
            self.timer = None

        else:
            bs.Actor.handleMessage(self, m)
            
class BlackHole(bs.Actor):

    def __init__(self, position=(0, 1, 0), autoExpand=True, scale=1,
                 doNotRandomize=False, infinity=False, owner=None):
        bs.Actor.__init__(self)
        self.shields = []
        if not doNotRandomize:
            self.position = (position[0] - 2 + random.random()*4,
                             position[1] + random.random()*2,
                             position[2] - 2 + random.random()*4)
        else:
            self.position = position

        self.scale = scale
        self.suckObjects = []
        self.owner = owner

        self.blackHoleMaterial = bs.Material()
        self.blackHoleMaterial.addActions(
            conditions=(('theyDontHaveMaterial',
                         bs.getSharedObject('objectMaterial')),
                        'and', ('theyHaveMaterial',
                                bs.getSharedObject('playerMaterial'))),
            actions=(('modifyPartCollision', 'collide', True),
                     ('modifyPartCollision', 'physical', False),
                     ('call', 'atConnect', self.touchedSpaz)))

        self.blackHoleMaterial.addActions(
            conditions=(('theyDontHaveMaterial',
                         bs.getSharedObject('playerMaterial')),
                        'and', ('theyHaveMaterial',
                                bs.getSharedObject('objectMaterial'))),
            actions=(('modifyPartCollision', 'collide', True),
                     ('modifyPartCollision', 'physical', False),
                     ('call', 'atConnect', self.touchedObj)))

        self.suckMaterial = bs.Material()
        self.suckMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial'))),
            actions=(('modifyPartCollision', 'collide', True),
                     ('modifyPartCollision', 'physical', False),
                     ('call', 'atConnect', self.touchedObjSuck)))

        self.node = bs.newNode('region', attrs={
            'position': (self.position[0], self.position[1], self.position[2]),
            'scale': (scale, scale, scale),
            'type': 'sphere',
            'materials': [self.blackHoleMaterial]})

        self.suckRadius = bs.newNode('region', attrs={
            'position': (self.position[0], self.position[1], self.position[2]),
            'scale': (scale, scale, scale),
            'type': 'sphere',
            'materials': [self.suckMaterial]})

        def dist():
            bs.emitBGDynamics(
                position=self.position,
                emitType='distortion',
                spread=6,
                count=100)

            if self.node.exists():
                bs.gameTimer(1000, dist)

        dist()
        if not infinity:
            self._dieTimer = bs.Timer(25000, bs.WeakCall(self.explode))

        scale1 = {
            0: (0, 0, 0),
            300: (self.scale, self.scale, self.scale)
        }

        scale2 = {
            0: (0, 0, 0),
            300: (self.scale*8, self.scale*8, self.scale*8)
        }

        bs.animateArray(self.node, 'scale', 3, scale1, True)
        bs.animateArray(self.suckRadius, 'scale', 3, scale2, True)

        for i in range(20):
            self.shields.append(
                bs.newNode('shield', attrs={
                    'color': (random.random(),
                              random.random(),
                              random.random()),
                    'radius': self.scale*2,
                    'position': self.position}))

        def sound():
            bs.playSound(bs.getSound('blackHole'))

        sound()
        if infinity:
            self.sound2 = bs.Timer(25000, bs.Call(sound), repeat=infinity)

    def addMass(self):
        self.scale += 0.15
        self.node.scale = (self.scale, self.scale, self.scale)
        for i in range(2):
            self.shields.append(
                bs.newNode('shield', attrs={
                    'color': (random.random(),
                              random.random(),
                              random.random()),
                    'radius': self.scale+0.15,
                    'position': self.position}))

    def explode(self):
        bs.emitBGDynamics(
            position=self.position,
            count=500,
            scale=1,
            spread=1.5,
            chunkType='spark')

        for i in self.shields:
            bs.animate(i, 'radius',
                       {0: 0, 200: i.radius*5})

        bs.Blast(
            position=self.position,
            blastRadius=10).autoRetain()

        for i in self.shields:
            i.delete()

        self.node.delete()
        self.suckRadius.delete()
        self.node.handleMessage(bs.DieMessage())
        self.suckRadius.handleMessage(bs.DieMessage())

    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')
        bs.Blast(
            position=node.position,
            blastType='turret').autoRetain()

        if node.exists():
            if self.owner.exists():
                node.handleMessage(
                    bs.HitMessage(
                        magnitude=1000.0,
                        sourcePlayer=self.owner.getDelegate().getPlayer()))

                try:
                    node.handleMessage(bs.DieMessage())
                except:
                    pass

                bs.shakeCamera(2)
            else:
                node.handleMessage(bs.DieMessage())

        self.addMass()

    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        bs.Blast(
            position=node.position,
            blastType='turret').autoRetain()

        if node.exists():
            node.handleMessage(bs.DieMessage())

    def touchedObjSuck(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.getNodeType() in ['prop', 'bomb']:
            self.suckObjects.append(node)

        for i in self.suckObjects:
            if i.exists():
                if i.sticky:
                    i.sticky = False
                    i.extraAcceleration = (0, 10, 0)
                else:
                    i.extraAcceleration = (
                        (self.position[0] - i.position[0])*8,
                        (self.position[1] - i.position[1])*25,
                        (self.position[2] - i.position[2])*8)

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()

            if self.suckRadius.exists():
                self.suckRadius.delete()

            self._updTimer = None
            self._suckTimer = None
            self.sound2 = None
            self.suckObjects = []

        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())

        elif isinstance(m, BlackHoleMessage):
            node = bs.getCollisionInfo('opposingNode')
            bs.Blast(
                position=self.position,
                blastType='normal').autoRetain()

            if not node.invincible:
                node.shattered = 2
                
class ShockWave(bs.Actor):#some bombdash stuff cause why not
    def __init__(self,position = (0,1,0),radius=2,speed = 200):
        bs.Actor.__init__(self)
        self.position = position
        
        self.shockWaveMaterial = bs.Material()
        self.shockWaveMaterial.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('playerMaterial'))),actions=(("modifyPartCollision","collide",True),
                                                      ("modifyPartCollision","physical",False),
                                                      ("call","atConnect", self.touchedSpaz)))
        self.shockWaveMaterial.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial')),'and',('theyDontHaveMaterial', bs.getSharedObject('playerMaterial'))),actions=(("modifyPartCollision","collide",True),
                                                      ("modifyPartCollision","physical",False),
                                                      ("call","atConnect", self.touchedObj)))
        self.radius = radius

        self.node = bs.newNode('region',
                       attrs={'position':(self.position[0],self.position[1],self.position[2]),
                              'scale':(0.1,0.1,0.1),
                              'type':'sphere',
                              'materials':[self.shockWaveMaterial]})
                              
        self.visualRadius = bs.newNode('shield',attrs={'position':self.position,'color':(0.05,0.05,0.1),'radius':0.1})
        
        bsUtils.animate(self.visualRadius,"radius",{0:0,speed:self.radius*2})
        bsUtils.animateArray(self.node,"scale",3,{0:(0,0,0),speed:(self.radius,self.radius,self.radius)},True)
        
        bs.gameTimer(speed+1,self.node.delete)
        bs.gameTimer(speed+1,self.visualRadius.delete)
        
        
    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')
        
        s = node.getDelegate()._punchPowerScale
        node.getDelegate()._punchPowerScale -= 0.3
        def re():
            node.getDelegate()._punchPowerScale = s
        bs.gameTimer(2000,re)
        
        bs.playSound(bs.getSound(random.choice(['shatter'])))
        node.handleMessage("impulse",node.position[0],node.position[1],node.position[2],
                                    -node.velocity[0],-node.velocity[1],-node.velocity[2],
                                    200,200,0,0,-node.velocity[0],-node.velocity[1],-node.velocity[2])
        flash = bs.newNode("flash",
                                   attrs={'position':node.position,
                                          'size':0.7,
                                          'color':(0,0.4+random.random(),1)})
                                          
        explosion = bs.newNode("explosion",
                               attrs={'position':node.position,
                                      'velocity':(node.velocity[0],max(-1.0,node.velocity[1]),node.velocity[2]),
                                      'radius':0.4,
                                      'big':True,
                                      'color':(0.3,0.3,1)})
        bs.gameTimer(400,explosion.delete)
                                          
        bs.emitBGDynamics(position=node.position,count=20,scale=0.5,spread=0.5,chunkType='spark')
        bs.gameTimer(60,flash.delete)
    
    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        bs.playSound(bs.getSound(random.choice(['shatter'])))

        node.handleMessage("impulse",node.position[0]+random.uniform(-2,2),node.position[1]+random.uniform(-2,2),node.position[2]+random.uniform(-2,2),
                                    -node.velocity[0]+random.uniform(-2,2),-node.velocity[1]+random.uniform(-2,2),-node.velocity[2]+random.uniform(-2,2),
                                    100,100,0,0,-node.velocity[0]+random.uniform(-2,2),-node.velocity[1]+random.uniform(-2,2),-node.velocity[2]+random.uniform(-2,2))
        flash = bs.newNode("flash",
                                   attrs={'position':node.position,
                                          'size':0.4,
                                          'color':(0,0.4+random.random(),1)})
                                          
        explosion = bs.newNode("explosion",
                               attrs={'position':node.position,
                                      'velocity':(node.velocity[0],max(-1.0,node.velocity[1]),node.velocity[2]),
                                      'radius':0.4,
                                      'big':True,
                                      'color':(0.3,0.3,1)})
        bs.gameTimer(400,explosion.delete)
                                          
        bs.emitBGDynamics(position=node.position,count=20,scale=0.5,spread=0.5,chunkType='spark')
        bs.gameTimer(60,flash.delete)
        
    def delete(self):
        self.node.delete()
        self.visualRadius.delete()
        
class cCube(bs.Actor):

    def __init__(self, position=(0, 1, 0), velocity=(0, 0, 0),
                 companion=False):
        bs.Actor.__init__(self)
        self.companion = companion
        self.light = None
        self.uptimer = None
        self.pickuped = None
        self.regenTimer = None
        self.checkerTimer = None

        factory = self.getFactory()

        self.cubeMaterial = bs.Material()
        self.cubeMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('dirtMaterial'))),
            actions=(('call', 'atConnect', self.shitHitsTheCube)))

        if companion:
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.tntModel,
                'lightModel': factory.tntModel,
                'body': 'crate',
                'shadowSize': 0.5,
                'colorTexture': factory.tntTex,
                'reflection': 'soft',
                'reflectionScale': [0.3],
                'materials': (bs.getSharedObject('objectMaterial'),
                              bs.getSharedObject('footingMaterial'),
                              self.cubeMaterial)})
        else:
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.companionCubeModel,
                'lightModel': factory.companionCubeModel,
                'body': 'crate',
                'shadowSize': 0.5,
                'colorTexture': factory.weightCubeTex,
                'reflection': 'soft',
                'reflectionScale': [0.3],
                'materials': (bs.getSharedObject('objectMaterial'),
                              bs.getSharedObject('footingMaterial'),
                              self.cubeMaterial)})

        def textSender():
            if self.node.exists():
                if self.companion and self.pickuped \
                        and bsInternal._getForegroundHostSession().narkomode:
                    bsUtils.PopupText(
                        random.choice([
                            'I love you',
                            'Hi',
                            'How are you?',
                            'I am alive',
                            'Now you can hear me',
                            'Dont forget me',
                            'BombDash forever',
                            'Nama come back',
                            'Do you know Chell?',
                            'GLaDOS kill my brothers',
                            'PLEASE DONT FIRE ME',
                            'Eric bring back the light',
                            'The cake is a lie',
                            'If life gives you lemons\ndont make the lemonade',
                            '09 Tartaros',
                            'Prometheus']),
                        color=(1, 0.1, 1),
                        scale=0.8,
                        position=self.node.position).autoRetain()

        bs.gameTimer(2000+random.randint(0, 3000), textSender, repeat=True)

    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        try:
            return activity._sharedPortalFactory
        except Exception:
            f = activity._sharedPortalFactory = PortalFactory()
            return f

    def shitHitsTheCube(self):
        node = bs.getCollisionInfo('opposingNode')
        bs.emitBGDynamics(
            position=node.position,
            count=30,
            scale=1.3,
            spread=0.1,
            chunkType='sweat')

        node.handleMessage(bs.DieMessage())

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()

        elif isinstance(m, bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()

        elif isinstance(m, bs.PickedUpMessage):
            self.pickuped = True
            self.node.extraAcceleration = (0, 25, 0)

            def up():
                self.node.extraAcceleration = (0, 40, 0)

            self.uptimer = bs.Timer(330, up)

            def checker():
                if self.node.exists() and \
                        (m is None or not m.node.exists()
                         or m.node.holdNode != self.node):
                    self.node.extraAcceleration = (0, 0, 0)
                    self.pickuped = False
                    self.checkerTimer = None

            self.checkerTimer = bs.gameTimer(100, checker, repeat=True)
            self.spazNode = m.node
            delegate = m.node.getDelegate()

            self.light = bs.newNode('light', attrs={
                'position': self.node.position,
                'color': (0, 1, 0),
                'volumeIntensityScale': 1.0,
                'intensity': 0.1,
                'radius': 0.6})

            m.node.connectAttr('position', self.light, 'position')

            def regen():
                if m is not None and m.node.exists() \
                        and m.node.getDelegate().hitPoints \
                        < m.node.getDelegate().hitPointsMax \
                        and self.pickuped:
                    delegate.hitPoints += 1
                    delegate._lastHitTime = None
                    delegate._numTimesHit = 0
                    m.node.hurt -= 0.001
                    bs.emitBGDynamics(
                        position=m.node.position,
                        velocity=(0, 3, 0),
                        count=int(3.0+random.random()*5),
                        scale=1.5,
                        spread=0.3,
                        chunkType='sweat')
                else:
                    if self.light is not None and self.light.exists():
                        self.light.delete()
                        self.regenTimer = None

            self.regenTimer = bs.Timer(10, regen, repeat=True)

        elif isinstance(m, bs.DroppedMessage):
            self.pickuped = False
            self.uptimer = None
            self.spazNode = None
            self.regenTimer = None
            self.checkerTimer = None
            self.node.extraAcceleration = (0, 0, 0)
            if self.light is not None and self.light.exists():
                self.light.delete()

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(
                'impulse', m.pos[0], m.pos[1], m.pos[2],
                m.velocity[0], m.velocity[1], m.velocity[2],
                m.magnitude, m.velocityMagnitude, m.radius,
                0, m.velocity[0], m.velocity[1], m.velocity[2])
            
class ImpactMessage(object):
    pass
            
class MagicSpell(bs.Actor):

    def __init__(self, position=(0, 10, 0), velocity=(0, 0, 0), owner=None):
        bs.Actor.__init__(self)
        self.owner = owner
        self.position = position
        self.velocity = velocity
        self.lastJumpTime = -9999
        self._jumpCooldown = 250
        self.m = None
        self.x = None
        self.y = None
        self.z = None
        self.s = 0
        self.r = 0.2
        self.isItSpaz = False
        self.maxR = 0.2
        self.revers = False
        self.off = False

        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan', 200),
                        'and', ('theyAreOlderThan', 200),
                        'and', ('evalColliding',),
                        'and', (('theyHaveMaterial',
                                 bs.getSharedObject('footingMaterial')),
                                'or', ('theyHaveMaterial',
                                       bs.getSharedObject('objectMaterial')))),
            actions=(('message', 'ourNode', 'atConnect', ImpactMessage())))
        
        self.impactBlastMaterial=bs.Material()        
        self.impactBlastMaterial.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('powerup')))

        self.node = bs.newNode('prop', delegate=self, attrs={
            'position': self.position,
            'model': bs.getModel('impactBomb'),
            'lightModel': bs.getModel('impactBomb'),
            'body': 'capsule',
            'velocity': self.velocity,
            'modelScale': 0.6,
            'bodyScale': 0.9,
            'shadowSize': 0.1,
            'reflection': 'soft',
            'reflectionScale': [2.0],
            'extraAcceleration': (0, 18, 0),
            'colorTexture': bs.getTexture('lava'),
            'materials': (bs.getSharedObject('footingMaterial'),
                          bs.getSharedObject('objectMaterial'),
                          self.impactBlastMaterial)})

        self.lightNode = bs.newNode('light', attrs={
            'position': self.position,
            'color': (1, 0.8, 0),
            'radius': 0.1,
            'volumeIntensityScale': 15.0})

        self.node.connectAttr('position', self.lightNode, 'position')
        self._emit = bs.Timer(15, bs.WeakCall(self.emit), repeat=True)
        self._emit1 = bs.Timer(35, bs.WeakCall(self.spawnParticles),
                               repeat=True)

        

        bs.playSound(bs.getSound('spell'))

    def spawnParticles(self):
        self.x = self.node.position[0]
        self.y = self.node.position[1]
        self.z = self.node.position[2]
        sin = math.sin(self.s) * self.r
        cos = math.cos(self.s) * self.r
        self.s += 0.4

        if self.r < 0:
            self.revers = True
        elif self.r > self.maxR:
            self.revers = False

        bs.emitBGDynamics(
            position=(self.x+cos, self.y, self.z+sin),
            velocity=(0, 0, 0),
            count=5,
            scale=0.4,
            spread=0,
            chunkType='spark')

    def emit(self):
        bs.emitBGDynamics(
            position=self.node.position,
            velocity=self.node.velocity,
            count=10,
            scale=0.4,
            spread=0.01,
            chunkType='spark')

    def impactSpaz(self):
        node = bs.getCollisionInfo('opposingNode')
        if node is not None:
            if isinstance(node.getDelegate(), bs.Spaz):
                self.node.handleMessage(bs.DieMessage())

                def setSpeed(val):
                    if node.exists():
                        setattr(node, 'hockey', val)

                setSpeed(True)

                self.shield = bs.newNode('scorch', owner=node, attrs={
                    'color': (random.random()*20,
                              random.random()*20,
                              random.random()*20),
                    'size': 0.4})

                bs.animate(self.shield, 'size',
                           {0: 1, 760: 0.4, 1520: 1}, loop=True)

                bs.animate(self.shield, 'presence',
                           {0: 1, 260: 0.4, 520: 1}, loop=True)

                node.connectAttr('positionCenter', self.shield, 'position')

                self.shield1 = bs.newNode('scorch', owner=node, attrs={
                    'color': (random.random()*20,
                              random.random()*20,
                              random.random()*20),
                    'size': 0.4})

                bs.animate(self.shield1, 'size',
                           {0: 0.7, 380: 0.4, 760: 0.7, 1440: 1, 1520: 0.7},
                           loop=True)

                bs.animate(self.shield1, 'presence',
                           {0: 0.7, 130: 0.4, 260: 0.7, 390: 1, 520: 0.7},
                           loop=True)

                node.connectAttr('positionCenter', self.shield1, 'position')

                self.shield2 = bs.newNode('scorch', owner=node, attrs={
                    'color': (random.random()*20,
                              random.random()*20,
                              random.random()*20),
                    'size': 0.4})

                bs.animate(self.shield2, 'size',
                           {0: 0.4, 380: 0.7, 760: 1, 1440: 0.7, 1520: 0.4},
                           loop=True)

                bs.animate(self.shield2, 'presence',
                           {0: 0.4, 130: 0.7, 260: 1, 390: 0.7, 520: 0.4},
                           loop=True)

                node.connectAttr('positionCenter', self.shield2, 'position')

                def onJumpPressSpec():
                    if not node.exists():
                        return

                    t = bs.getGameTime()
                    if t - self.lastJumpTime >= self._jumpCooldown \
                            and not self.off \
                            and not (node.knockout > 0.0 or node.frozen > 0):
                        node.jumpPressed = True
                        self.lastJumpTime = t
                        self._jumpCooldown = 750
                        node.handleMessage(
                            'impulse', node.position[0], node.position[1],
                            node.position[2], 0, 0, 0, 200, 200, 0, 0, 0, 1, 0)

                node.getDelegate().getPlayer().assignInputCall(
                    'jumpPress', onJumpPressSpec)

                if node is not None and node.exists():
                    node.getDelegate().superHealth(True)

                def spazEmit():
                    try:
                        bs.emitBGDynamics(
                            position=(node.position[0],
                                      node.position[1]-0.3,
                                      node.position[2]),
                            velocity=node.velocity,
                            count=15,
                            scale=0.4,
                            spread=0.01,
                            chunkType='spark')
                    except:
                        pass

                self.spaz_emit = bs.Timer(15, bs.Call(spazEmit), repeat=True)

                def offAllEffects():
                    self.shield.delete()
                    self.shield = None
                    self.shield1.delete()
                    self.shield1 = None
                    self.shield2.delete()
                    self.shield2 = None
                    self.off = True
                    self.spaz_emit = None
                    setSpeed(False)
                    if node is not None and node.exists():
                        try:
                            node.getDelegate().connectControlsToPlayer()
                            node.getDelegate().superHealth(False)
                        except:
                            pass

                bs.gameTimer(15000, bs.Call(offAllEffects))
            else:
                self.node.handleMessage(bs.DieMessage())

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
                self.lightNode.delete()
                self._emit = None
                self._emit1 = None

        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(bs.DieMessage())
            
class Artillery(object):

    def __init__(self, position=(0, 1, 0), target=None,
                 owner=None, bombType='impact', sourcePlayer=None):
        self.position = position
        self.owner = owner
        self.target = target
        self.bombType = bombType
        self.sourcePlayer = sourcePlayer
        self.radius = 60
        self.maxHeight = bs.getActivity().getMap().getDefBoundBox(
            'levelBounds')

        self.aimZone = bs.Material()
        self.aimZone.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(('modifyPartCollision', 'collide', True),
                     ('modifyPartCollision', 'physical', False),
                     ('call', 'atConnect', self.touchedSpaz)))

        self.node = bs.newNode('region', attrs={
            'position': self.position,
            'scale': (0.5, 0.5, 0.5),
            'type': 'sphere',
            'materials': [self.aimZone]})

        scale = {
            0: (0.5, 0.5, 0.5),
            100: (self.radius, self.radius, self.radius)
        }

        bs.animateArray(self.node, 'scale', 3, scale)

        bs.gameTimer(101, self.node.delete)
        bs.gameTimer(102, self.strike)

    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')
        if self.owner is not None:
            if not node == self.owner:
                self.target = node
                self.node.materials = [bs.Material()]
                bs.gameTimer(300, self.node.delete)

    def strike(self):
        if self.target is not None:
            def launchBomb():
                if self.target is not None and self.target.exists():
                    self.pos = self.target.position
                    b = bs.Bomb(
                        position=self.position,
                        velocity=(0, 5, 0),
                        bombType=self.bombType,
                        napalm=True).autoRetain()

                    b.node.extraAcceleration = (0, 700, 0)
                    b.node.velocity = (
                        b.node.velocity[0]+(self.pos[0]-b.node.position[0]),
                        10,
                        b.node.velocity[2]+(self.pos[2]-b.node.position[2]))

                    bs.playSound(bs.getSound('Aim'))

            bs.gameTimer(100, bs.Call(launchBomb))
            bs.gameTimer(200, bs.Call(launchBomb))
            bs.gameTimer(300, bs.Call(launchBomb))
            bs.gameTimer(400, bs.Call(launchBomb))
            bs.gameTimer(500, bs.Call(launchBomb))
            bs.gameTimer(700, bs.Call(launchBomb))
            bs.gameTimer(900, bs.Call(self.drop))

    def drop(self):
        def launchBombDrop():
            bs.playSound(bs.getSound('Aim'))
            b = bs.Bomb(
                position=(self.pos[0]+(-2+random.random()*4),
                          self.maxHeight[4],
                          self.pos[2]+(-2+random.random()*4)),
                velocity=(0, -100, 0),
                bombType=self.bombType,
                sourcePlayer=self.sourcePlayer).autoRetain()

            b.node.extraAcceleration = (0, -100, 0)

        bs.gameTimer(100, bs.Call(launchBombDrop))
        bs.gameTimer(300, bs.Call(launchBombDrop))
        bs.gameTimer(500, bs.Call(launchBombDrop))
        bs.gameTimer(700, bs.Call(launchBombDrop))
        bs.gameTimer(900, bs.Call(launchBombDrop))
        bs.gameTimer(1000, bs.Call(launchBombDrop))

class FloatingLandMine(bs.Actor):

    def __init__(self, position=(0,1,0)):
        bs.Actor.__init__(self)
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'landMine',
                                   'model':bs.getModel('landMine'),
                                   'colorTexture':bs.getTexture('bg'),
                                   'shadowSize':0.44,
                                   'reflection':'powerup',
                                   'reflectionScale':[5.0,1.5,1.0],
                                   'materials':[bs.getSharedObject('objectMaterial')],
                                   'lightModel':bs.getModel('landMine')})

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.PickedUpMessage):
            self.node.extraAcceleration = (0,60,0)

        else:
            bs.Actor.handleMessage(self, m)
            
class Flyer(bs.Actor):

    def __init__(self, position=(0,1,0)):#a bit differnt from our pal floating landmine by PC
        bs.Actor.__init__(self)
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'sphere',
                                   'model':bs.getModel('frostyPelvis'),
                                   'colorTexture':bs.getTexture('crossOutMask'),
                                   'shadowSize':0.44,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial')],
                                   'lightModel':bs.getModel('frostyPelvis')}) 

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.PickedUpMessage):
            self.node.extraAcceleration = (0,60,0)

        else:
            bs.Actor.handleMessage(self, m)
            
class BeachBall(bs.Actor):

    def __init__(self, position=(0,1,0)):#kinda of like the lego thingy by bombdash but recreated by PC
        bs.Actor.__init__(self)
        
        self.impactBlastMaterial=bs.Material()        
        self.impactBlastMaterial.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('slip')))
        
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'sphere',
                                   'model':bs.getModel('frostyPelvis'),
                                   'colorTexture':bs.getTexture('gameCircleIcon'),
                                   'shadowSize':0.44,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial'),self.impactBlastMaterial],
                                   'lightModel':bs.getModel('frostyPelvis')}) 

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.PickedUpMessage):
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))

        else:
            bs.Actor.handleMessage(self, m)
            
class BlastBot(bs.Actor):

    def __init__(self, position=(0,1,0)):#beast bot made by PC
        bs.Actor.__init__(self)
        
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'puck',
                                   'model':bs.getModel('puck'),
                                   'colorTexture':bs.getTexture('gameCircleIcon'),
                                   'shadowSize':0.44,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial')],
                                   'lightModel':bs.getModel('puck')}) 
                                   
        m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.8, 0), 'operation': 'add'})
        self.node.connectAttr('position', m, 'input2')
        self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'blastBot',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': (1,1,1),
                                              'scale': 0.0125,
                                              'hAlign': 'center'})
        m.connectAttr('output', self.nodeText, 'position')

        def end():
            if self.node.exists():
                self.node.delete()
        bs.gameTimer(8000,bs.Call(end))

        def text():
            if self.node.exists():
                bsUtils.PopupText("Bye-Bye!",color=(1,1,1),scale=1.0,position=self.node.position).autoRetain()#
        bs.gameTimer(7900,bs.Call(text))

        def _blast():    
            if self.node.exists():    
                bs.Blast(position = self.node.position,hitType = 'punch',blastRadius = 3).autoRetain()
        bs.gameTimer(1000,bs.Call(_blast),repeat=True)

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))#for some fun xd
            bs.emitBGDynamics(position = self.node.position,
                              velocity = (0, 4, 0),
                              count = 14, scale = 0.8,
                              chunkType = 'spark', spread = 1.5)

        else:
            bs.Actor.handleMessage(self, m)
            
class Bomber(bs.Actor):

    def __init__(self, position=(0,1,0)):#another beast bot made by PC
        bs.Actor.__init__(self)
        
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'puck',
                                   'model':bs.getModel('puck'),
                                   'colorTexture':bs.getTexture('gameCircleIcon'),
                                   'shadowSize':0.44,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial')],
                                   'lightModel':bs.getModel('puck')}) 
                                   
        m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.8, 0), 'operation': 'add'})
        self.node.connectAttr('position', m, 'input2')
        self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'bombBot',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': (1,1,1),
                                              'scale': 0.0125,
                                              'hAlign': 'center'})
        m.connectAttr('output', self.nodeText, 'position')
        
        def end():
            if self.node.exists():
                self.node.delete()
        bs.gameTimer(8000,bs.Call(end))

        def text():
            if self.node.exists():
                bsUtils.PopupText("Bye-Bye!",color=(1,1,1),scale=1.0,position=self.node.position).autoRetain()#
        bs.gameTimer(7900,bs.Call(text))
       
        def _blast():  
            if self.node.exists():
                k = random.choice(['ice','impact','sticky','landMine']) 
                bs.Bomb(position=self.node.position,velocity=((0+random.random()*20.0),(0+random.random()*20.0),(0+random.random()*20.0)),bombType = k).autoRetain()
                bs.Bomb(position=self.node.position,velocity=((0+random.random()*-20.0),(0+random.random()*-20.0),(0+random.random()*-20.0)),bombType = k).autoRetain()
                bs.Bomb(position=self.node.position,velocity=((0+random.random()*-20.0),(0+random.random()*-20.0),(0+random.random()*-20.0)),bombType = k).autoRetain()
                bs.Bomb(position=self.node.position,velocity=((0+random.random()*20.0),(0+random.random()*20.0),(0+random.random()*20.0)),bombType = k).autoRetain()
        bs.gameTimer(1000,bs.Call(_blast),repeat=True)

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))#for some fun xd
            bs.emitBGDynamics(position = self.node.position,
                              velocity = (0, 4, 0),
                              count = 14, scale = 0.8,
                              chunkType = 'spark', spread = 1.5)

        else:
            bs.Actor.handleMessage(self, m)
            
class BotSpawner(bs.Actor):

    def __init__(self, position=(0,1,0)):#another beast bot made by PC
        bs.Actor.__init__(self)
        
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'puck',
                                   'model':bs.getModel('puck'),
                                   'colorTexture':bs.getTexture('frostyIcon'),
                                   'shadowSize':0.44,
                                   'modelScale':0.0,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial')],
                                   'lightModel':bs.getModel('puck')}) 
                                   
        m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.2, 0), 'operation': 'add'})
        self.node.connectAttr('position', m, 'input2')
        self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'botSpawner',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': (1,1,1),
                                              'scale': 0.0125,
                                              'hAlign': 'center'})
        m.connectAttr('output', self.nodeText, 'position')
        
        self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                           'position': (
                                                                               self.node.position[0],
                                                                               self.node.position[1],
                                                                               self.node.position[2] + 0.5),
                                                                           'radius': 1.3})
        self.node.connectAttr('position', self.nodeShield, 'position')
        
        def end():
            if self.node.exists():
                self.node.delete()
        bs.gameTimer(20000,bs.Call(end))
        
        def text():
            if self.node.exists():
                bsUtils.PopupText("Bye-Bye!",color=(1,1,1),scale=1.0,position=self.node.position).autoRetain()
        bs.gameTimer(19000,bs.Call(text))
        
        def _bot():
                testingEvent = 0
                
                event = random.randint(1,5) if testingEvent == 0 else testingEvent
                #print 'PCName: ' + str(event)
                 
                if event in [1]:
                    #print 'PCName. The effect: Powerups'
                    self._bots = bs.BotSet()
                    bs.gameTimer(500,bs.Call(self._bots.spawnBot,bs.PirateBot,pos=self.node.position,spawnTime=2000))                    
                elif event == 2:
                    #print 'PCName. The effect: Powerups'
                    self._bots = bs.BotSet()
                    bs.gameTimer(500,bs.Call(self._bots.spawnBot,bs.BomberBotProStatic,pos=self.node.position,spawnTime=2000))                    
                elif event == 3:
                    #print 'PCName. The effect: Powerups'                	
                    self._bots = bs.BotSet()
                    bs.gameTimer(500,bs.Call(self._bots.spawnBot,bs.NinjaBot,pos=self.node.position,spawnTime=2000))                   
                elif event == 4:
                    #print 'PCName. The effect: Powerups'                	
                    self._bots = bs.BotSet()
                    bs.gameTimer(500,bs.Call(self._bots.spawnBot,bs.BunnyBot,pos=self.node.position,spawnTime=2000))                   
                elif event == 5:
                    #print 'PCName. The effect: Powerups'                	
                    self._bots = bs.BotSet()
                    bs.gameTimer(500,bs.Call(self._bots.spawnBot,bs.MelBot,pos=self.node.position,spawnTime=2000))    
        bs.gameTimer(5000,bs.Call(_bot),repeat=True)
        

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))#for some fun xd
            bs.emitBGDynamics(position = self.node.position,
                              velocity = (0, 4, 0),
                              count = 14, scale = 0.8,
                              chunkType = 'spark', spread = 1.5)

        else:
            bs.Actor.handleMessage(self, m)
            
class CharacterPicker(bs.Actor):

    def __init__(self, position=(0,1,0)):#another beast bot made by PC
        bs.Actor.__init__(self)
        
        self.impactBlastMaterial=bs.Material()        
        self.impactBlastMaterial.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('rchar')))
        
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'puck',
                                   'model':bs.getModel('puck'),
                                   'colorTexture':bs.getTexture('frostyIcon'),
                                   'shadowSize':0.44,
                                   'modelScale':0.0,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial'),self.impactBlastMaterial],
                                   'lightModel':bs.getModel('puck')}) 
                                   
        m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.2, 0), 'operation': 'add'})
        self.node.connectAttr('position', m, 'input2')
        self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'characterPicker',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': (1,1,1),
                                              'scale': 0.0125,
                                              'hAlign': 'center'})
        m.connectAttr('output', self.nodeText, 'position')
        
        self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                           'position': (
                                                                               self.node.position[0],
                                                                               self.node.position[1],
                                                                               self.node.position[2] + 0.5),
                                                                           'radius': 1.3})
        self.node.connectAttr('position', self.nodeShield, 'position')
        
        def end():
            if self.node.exists():
                self.node.delete()
        bs.gameTimer(8000,bs.Call(end))
        
        def text():
            if self.node.exists():
                bsUtils.PopupText("Bye-Bye!",color=(1,1,1),scale=1.0,position=self.node.position).autoRetain()
        bs.gameTimer(7900,bs.Call(text))


    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))#for some fun xd
            bs.emitBGDynamics(position = self.node.position,
                              velocity = (0, 4, 0),
                              count = 14, scale = 0.8,
                              chunkType = 'spark', spread = 1.5)

        else:
            bs.Actor.handleMessage(self, m)
            
class ColorPicker(bs.Actor):

    def __init__(self, position=(0,1,0)):#another beast bot made by PC
        bs.Actor.__init__(self)
        
        self.impactBlastMaterial=bs.Material()        
        self.impactBlastMaterial.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('rcolor')))
        
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'puck',
                                   'model':bs.getModel('puck'),
                                   'colorTexture':bs.getTexture('frostyIcon'),
                                   'shadowSize':0.44,
                                   'modelScale':0.0,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial'),self.impactBlastMaterial],
                                   'lightModel':bs.getModel('puck')}) 
                                   
        m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.2, 0), 'operation': 'add'})
        self.node.connectAttr('position', m, 'input2')
        self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'colorPicker',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': (1,1,1),
                                              'scale': 0.0125,
                                              'hAlign': 'center'})
        m.connectAttr('output', self.nodeText, 'position')
        
        self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                           'position': (
                                                                               self.node.position[0],
                                                                               self.node.position[1],
                                                                               self.node.position[2] + 0.5),
                                                                           'radius': 1.3})
        self.node.connectAttr('position', self.nodeShield, 'position')

        def end():
            if self.node.exists():
                self.node.delete()
        bs.gameTimer(8000,bs.Call(end))
        
        def text():
            if self.node.exists():
                bsUtils.PopupText("Bye-Bye!",color=(1,1,1),scale=1.0,position=self.node.position).autoRetain()
        bs.gameTimer(7900,bs.Call(text))
        

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))#for some fun xd
            bs.emitBGDynamics(position = self.node.position,
                              velocity = (0, 4, 0),
                              count = 14, scale = 0.8,
                              chunkType = 'spark', spread = 1.5)

        else:
            bs.Actor.handleMessage(self, m)            

# The volcano spews bombs and creates an impact bomb over everyone's head, though, at the cost of the user's life.
#made by VIRUS
class Volcano(bs.Actor):

    def __init__(self,position = (0,1,0),color = (1,0,0), player = None):
        bs.Actor.__init__(self)

        self.radius = .6
        self.position = position
        self.player = player
        self.color = color
        self.erupted = False

        self.volcanoMaterial = bs.Material()
        self.volcanoMaterial.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('playerMaterial'))),actions=(("modifyPartCollision","collide",True),
                                                      ("modifyPartCollision","physical",False),
                                                      ("message", "theirNode","atConnect",bs.DieMessage()),
                                                      ("call","atConnect", self.erupt)))

        self.node1 = bs.newNode('region',
                       attrs={'position':(self.position[0],self.position[1],self.position[2]),
                              'scale':(self.radius,self.radius,self.radius),
                              'materials':[self.volcanoMaterial]})
        self.light = bs.newNode('locator',attrs={'shape':'circle','position':(self.position[0],self.position[1]-2,self.position[2]),
                                         'color':(1,0,0),'opacity':0.5,
                                         'drawBeauty':True,'additive':True})
        bsUtils.animateArray(self.node1,"scale",3,{0:(0,0,0),500:(self.radius,self.radius,self.radius)})
        bs.gameTimer(10000,self.die)

    def erupt(self):
        for i in range(5):
            bs.gameTimer(i*10, bs.Call(self.spurt))
        if self.erupted == True: return
        self.erupted = True
        for player in bs.getActivity().players:#hehe this i will use with pleasure!!
            if player.isAlive() and player is not self.player:
                playerPos = player.actor.node.position
                bomb = bs.Bomb(position=(playerPos[0],playerPos[1]+6,playerPos[2]),velocity=(0,-1,0),bombType='impact',sourcePlayer=self.player).autoRetain()

    def spurt(self):
        bomb = bs.Bomb(position=(self.position[0],self.position[1]+2,self.position[2]),velocity=(6*random.random()-3,8,6*random.random()-3),sourcePlayer=self.player).autoRetain()
        bs.emitBGDynamics(position=self.position, velocity=(0,8,0), count=10)

    def die(self):
        self.node1.delete()
        self.light.delete()
        self.handleMessage(bs.DieMessage())
        
class PlsTouchMe(bs.Actor):

    def __init__(self, position=(0,1,0)):#beast bot made by PC
        bs.Actor.__init__(self)
        
        self.impactBlastMaterial=bs.Material()        
        self.impactBlastMaterial.addActions(
            conditions=((('theyAreOlderThan', 100),
                         'and', ('theyHaveMaterial',
                                 bs.getSharedObject('playerMaterial')))),
            actions=('message', 'theirNode','atConnect', bs.PowerupMessage('rrandom')))
        
        color = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))
        self.node = bs.newNode('prop', delegate=self,
                               attrs={
                                   'position':position,
                                   'body':'crate',
                                   'extraAcceleration':(0,15,0),
                                   'model':bs.getModel('powerup'),
                                   'colorTexture':bs.getTexture('achievementEmpty'),
                                   'shadowSize':0.44,
                                   'modelScale':1.85,
                                   'density': 999999999999,
                                   'bodyScale':1.85,
                                   'reflection':'powerup',
                                   'reflectionScale':color,
                                   'materials':[bs.getSharedObject('objectMaterial'),self.impactBlastMaterial],
                                   'lightModel':bs.getModel('powerupSimple')}) 
                                   
        m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.0, 0), 'operation': 'add'})
        self.node.connectAttr('position', m, 'input2')
        self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': 'luckyBlock',
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': (1,1,1),
                                              'scale': 0.0125,
                                              'hAlign': 'center'})
        m.connectAttr('output', self.nodeText, 'position')
        

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.timer = None
        
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.delete()
            self.timer = None

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))#for some fun xd
            bs.emitBGDynamics(position = self.node.position,
                              velocity = (0, 4, 0),
                              count = 14, scale = 0.8,
                              chunkType = 'spark', spread = 1.5)

        else:
            bs.Actor.handleMessage(self, m)

