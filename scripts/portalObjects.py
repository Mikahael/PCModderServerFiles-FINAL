import bs
import random
import bsUtils
import math
import bsVector
import copy


def setpositionSpan(self, positionSpan):
    self.positionSpan = positionSpan


def getRandomPosition(self, activity):
    if self.positionSpan is not None:
        ru = random.uniform
        ps = self.positionSpan
        return (ru(ps[0][0] - 1.0, ps[0][1] + 1.0), ps[1][1] + ru(0.1, 1.5),
                ru(ps[2][0] - 1.0, ps[2][1] + 1.0))
    else:
        pts = copy.copy(activity.getMap().ffaSpawnPoints)
        pts2 = activity.getMap().powerupSpawnPoints
        for i in pts2:
            pts.append(i)

        pos = [[999, -999], [999, -999], [999, -999]]
        for pt in pts:
            for i in range(3):
                pos[i][0] = min(pos[i][0], pt[i])
                pos[i][1] = max(pos[i][1], pt[i])

        setpositionSpan(self, pos)
        return getRandomPosition(self, activity)


class PortalFactory(object):
    def __init__(self):
        #self.companionCubeModel = bs.getModel('companionCube')
        #self.turretModel = bs.getModel('turret')
        #self.turretClosedModel = bs.getModel('turret_closed')

        #self.badrockModel = bs.getModel('badrock')
        #self.stickyCubeModel = bs.getModel('stickyCube')
        self.bubbleGeneratorModel = bs.getModel('box')
        #self.cakeModel = bs.getModel('cakeLowPoly')
        self.shitModel = bs.getModel('box')

        #self.cakeTex = bs.getTexture('cake')
        self.bubbleGeneratorTex = bs.getTexture('powerupShield')
        #self.minecraftTex = bs.getTexture('MinecraftTex')
        #self.companionCubeLitTex = bs.getTexture('companionCubeLit')
        #self.companionCubeTex = bs.getTexture('companionCube')
        #self.weightCubeLitTex = bs.getTexture('weightCubeLit')
        #self.weightCubeTex = bs.getTexture('weightCube')

        self.activateSound = bs.getSound('activateBeep')

        self.legoMaterial = bs.Material()
        self.legoMaterial.addActions(conditions=(('theyHaveMaterial',
                                                  self.legoMaterial)),
                                     actions=('message', 'ourNode',
                                              'atConnect', LegoConnect()))

        self.legoMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=('message', 'ourNode', 'atConnect',
                     FuckFuckFuckFuckingLego()))

        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan', 200), 'and',
                        ('theyAreOlderThan', 200), 'and', ('evalColliding', ),
                        'and', (('theyHaveMaterial',
                                 bs.getSharedObject('footingMaterial')), 'or',
                                ('theyHaveMaterial',
                                 bs.getSharedObject('objectMaterial')))),
            actions=(('message', 'ourNode', 'atConnect', ImpactMessage())))


class SplatMessage(object):
    pass


class ImpactMessage(object):
    pass


class LegoConnect(object):
    pass


class FuckFuckFuckFuckingLego(object):
    pass


class BlackHoleMessage(object):
    pass


class ParticlesCircle(object):
    pass


class TurretImpactMessage(object):
    pass


class dirtBombMessage(object):
    pass


class FireMessage(object):
    pass


def getUpim():
    import bsInternal
    bsInternal._getForegroundHostActivity(
    ).players[0].actor.node.materials = bsInternal._getForegroundHostActivity(
    ).players[0].actor.node.materials + (bs.getSharedObject('upim'), )


class UltraPunch(bs.Actor):
    def __init__(self, radius=2, speed=500, position=(0, 0, 0)):
        bs.Actor.__init__(self)
        self.position = position
        upim = bs.getSharedObject('upim')

        self.ultraPunchMaterial = bs.Material()
        self.ultraPunchMaterial.addActions(
            conditions=(('theyHaveMaterial', upim)),
            actions=(("modifyPartCollision", "collide", True),
                     ("modifyPartCollision", "physical", False)))
        self.ultraPunchMaterial.addActions(
            conditions=(('theyDontHaveMaterial', upim)),
            actions=(("modifyPartCollision", "collide", True),
                     ("modifyPartCollision", "physical", True)))

        self.radius = radius

        self.node = bs.newNode('region',
                               attrs={
                                   'position':
                                   (self.position[0], self.position[1],
                                    self.position[2]),
                                   'scale': (0.1, 0.1, 0.1),
                                   'type':
                                   'sphere',
                                   'materials': [self.ultraPunchMaterial]
                               })

        self.visualRadius = bs.newNode('shield',
                                       attrs={
                                           'position': self.position,
                                           'color': (0.3, 0, 0),
                                           'radius': 0.1
                                       })

        bsUtils.animate(self.visualRadius, "radius", {
            0: 0,
            speed: self.radius * 2
        })
        bsUtils.animateArray(self.node, "scale", 3, {
            0: (0, 0, 0),
            speed: (self.radius, self.radius, self.radius)
        }, True)

        bs.gameTimer(speed + 1, self.node.delete)
        bs.gameTimer(speed + 1, self.visualRadius.delete)


class ShockWave(bs.Actor):
    def __init__(self, position=(0, 1, 0), radius=2, speed=200):
        bs.Actor.__init__(self)
        self.position = position

        self.shockWaveMaterial = bs.Material()
        self.shockWaveMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedSpaz)))
        self.shockWaveMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial')), 'and',
                        ('theyDontHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedObj)))
        self.radius = radius

        self.node = bs.newNode('region',
                               attrs={
                                   'position':
                                   (self.position[0], self.position[1],
                                    self.position[2]),
                                   'scale': (0.1, 0.1, 0.1),
                                   'type':
                                   'sphere',
                                   'materials': [self.shockWaveMaterial]
                               })

        self.visualRadius = bs.newNode('shield',
                                       attrs={
                                           'position': self.position,
                                           'color': (0.05, 0.05, 0.1),
                                           'radius': 0.1
                                       })

        bsUtils.animate(self.visualRadius, "radius", {
            0: 0,
            speed: self.radius * 2
        })
        bsUtils.animateArray(self.node, "scale", 3, {
            0: (0, 0, 0),
            speed: (self.radius, self.radius, self.radius)
        }, True)

        bs.gameTimer(speed + 1, self.node.delete)
        bs.gameTimer(speed + 1, self.visualRadius.delete)

    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')

        s = node.getDelegate()._punchPowerScale
        node.getDelegate()._punchPowerScale -= 0.3

        def re():
            node.getDelegate()._punchPowerScale = s

        bs.gameTimer(2000, re)

        bs.playSound(
            bs.getSound(random.choice(['electro1', 'electro2', 'electro3'])))
        node.handleMessage("impulse", node.position[0], node.position[1],
                           node.position[2], -node.velocity[0],
                           -node.velocity[1], -node.velocity[2], 200, 200, 0,
                           0, -node.velocity[0], -node.velocity[1],
                           -node.velocity[2])
        flash = bs.newNode("flash",
                           attrs={
                               'position': node.position,
                               'size': 0.7,
                               'color': (0, 0.4 + random.random(), 1)
                           })

        explosion = bs.newNode("explosion",
                               attrs={
                                   'position':
                                   node.position,
                                   'velocity':
                                   (node.velocity[0],
                                    max(-1.0,
                                        node.velocity[1]), node.velocity[2]),
                                   'radius':
                                   0.4,
                                   'big':
                                   True,
                                   'color': (0.3, 0.3, 1)
                               })
        bs.gameTimer(400, explosion.delete)

        bs.emitBGDynamics(position=node.position,
                          count=20,
                          scale=0.5,
                          spread=0.5,
                          chunkType='spark')
        bs.gameTimer(60, flash.delete)

    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        bs.playSound(
            bs.getSound(random.choice(['electro1', 'electro2', 'electro3'])))

        node.handleMessage("impulse", node.position[0] + random.uniform(-2, 2),
                           node.position[1] + random.uniform(-2, 2),
                           node.position[2] + random.uniform(-2, 2),
                           -node.velocity[0] + random.uniform(-2, 2),
                           -node.velocity[1] + random.uniform(-2, 2),
                           -node.velocity[2] + random.uniform(-2, 2), 100, 100,
                           0, 0, -node.velocity[0] + random.uniform(-2, 2),
                           -node.velocity[1] + random.uniform(-2, 2),
                           -node.velocity[2] + random.uniform(-2, 2))
        flash = bs.newNode("flash",
                           attrs={
                               'position': node.position,
                               'size': 0.4,
                               'color': (0, 0.4 + random.random(), 1)
                           })

        explosion = bs.newNode("explosion",
                               attrs={
                                   'position':
                                   node.position,
                                   'velocity':
                                   (node.velocity[0],
                                    max(-1.0,
                                        node.velocity[1]), node.velocity[2]),
                                   'radius':
                                   0.4,
                                   'big':
                                   True,
                                   'color': (0.3, 0.3, 1)
                               })
        bs.gameTimer(400, explosion.delete)

        bs.emitBGDynamics(position=node.position,
                          count=20,
                          scale=0.5,
                          spread=0.5,
                          chunkType='spark')
        bs.gameTimer(60, flash.delete)

    def delete(self):
        self.node.delete()
        self.visualRadius.delete()


class Apple(bs.Actor):
    def __init__(self, position=(0, 6, 0)):
        bs.Actor.__init__(self)

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'model':
                                   bs.getModel('apple'),
                                   'lightModel':
                                   bs.getModel('apple'),
                                   'body':
                                   'box',
                                   'modelScale':
                                   0.8,
                                   'shadowSize':
                                   0.5,
                                   'reflection':
                                   'soft',
                                   'colorTexture':
                                   bs.getTexture('apple'),
                                   'materials':
                                   (bs.getSharedObject('footingMaterial'),
                                    bs.getSharedObject('objectMaterial'))
                               })

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())

        elif isinstance(m, bs.HitMessage):
            m.srcNode.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2], m.magnitude,
                                    m.velocityMagnitude, m.radius, 0,
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2])


class Napalm(bs.Actor):
    def __init__(self, position=(0, -0.1, 0), radius=1.2, time=5000):
        bs.Actor.__init__(self)
        self.radius = radius
        self.position = position if not position == (0, -0.1, 0) else (
            random.uniform(-4, 4), 0.1, random.uniform(-4, 4))
        self.stop = False
        self.sound = bs.getSound('fire')

        self.spawnSmoke(pos=self.position)
        self.spawnFire(pos=self.position)
        self.doSound(pos=self.position)

        self.firem = bs.Material()
        self.firem.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedSpaz)))
        self.firem.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial')), 'and',
                        ('theyDontHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedObj)))

        self.node = bs.newNode('region',
                               attrs={
                                   'position':
                                   (self.position[0], self.position[1],
                                    self.position[2]),
                                   'scale': (0.1, 0.1, 0.1),
                                   'type':
                                   'sphere',
                                   'materials': [self.firem]
                               })

        bsUtils.animateArray(self.node, "scale", 3, {
            0: (0, 0, 0),
            100: (self.radius / 2, self.radius / 2, self.radius / 2)
        }, True)

        self.fireLight = bs.newNode('light',
                                    attrs={
                                        'position': self.position,
                                        'color': (1, 0.4, 0),
                                        'volumeIntensityScale': 0.1,
                                        'intensity': 0.8,
                                        'radius': radius / 5
                                    })

        self.c2 = bs.animate(
            self.fireLight, "intensity", {
                0: random.uniform(0.8, 1.5),
                100: random.uniform(0.8, 1.5),
                200: random.uniform(0.8, 1.5),
                300: random.uniform(0.8, 1.5),
                400: random.uniform(0.8, 1.5),
                500: random.uniform(0.8, 1.5),
                600: random.uniform(0.8, 1.5),
                700: random.uniform(0.8, 1.5),
                800: random.uniform(0.8, 1.5),
                900: random.uniform(0.8, 1.5),
                1000: random.uniform(0.8, 1.5),
                1100: random.uniform(0.8, 1.5),
                1200: random.uniform(0.8, 1.5),
                1300: random.uniform(0.8, 1.5)
            }, True)
        self.c3 = bs.animateArray(
            self.fireLight, "color", 3, {
                0: (1, 0.4, 0),
                100: (1, 0.3, 0),
                200: (1, 0.6, 0),
                300: (1, 0.5, 0),
                400: (1, 0.2, 0),
                500: (1, 0.4, 0),
                600: (1, 0.3, 0)
            }, True)

        self.scorch = bs.newNode('scorch',
                                 attrs={
                                     'position': self.position,
                                     'size': radius * 0.5,
                                     'big': True,
                                     'color': (0.1, 0.0, 0.0)
                                 })
        self.c4 = bsUtils.animate(self.scorch, "presence", {
            0: 0.1,
            int(time / 3): radius
        })

        def stopIt():
            self.stop = True
            self.c2.delete()
            self.c4.delete()
            if self.node is not None and self.node.exists():
                self.node.delete()
            self.fireLight.delete()
            bsUtils.animate(self.scorch, "presence", {
                0: self.scorch.presence,
                8000: 0
            })
            bs.gameTimer(8001, self.scorch.delete)

        bs.gameTimer(time, stopIt)

    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.getNodeType() == 'spaz':
            if not node.getDelegate().fired:
                node.getDelegate().fire()

    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.exists():
            try:
                node.getDelegate().explode()
            except:
                pass

    def spawnSmoke(self, pos):
        pos = (pos[0] + random.uniform(-self.radius / 2, self.radius / 2),
               pos[1] + 0.2,
               pos[2] + random.uniform(-self.radius / 2, self.radius / 2))
        bs.emitBGDynamics(position=pos,
                          velocity=(0, 0, 0),
                          count=1,
                          emitType='tendrils',
                          tendrilType='smoke')
        if not self.stop:
            bs.gameTimer(1800, bs.Call(self.spawnSmoke, pos=self.position))

    def doSound(self, pos):
        bs.playSound(self.sound, position=pos)
        if not self.stop:
            bs.gameTimer(2900, bs.Call(self.doSound, pos=self.position))

    def spawnFire(self, pos):
        pos = (pos[0] + random.uniform(-self.radius / 2, self.radius / 2),
               pos[1],
               pos[2] + random.uniform(-self.radius / 2, self.radius / 2))

        # if math.sqrt((self.position[0]+pos[0])*(self.position[0]+pos[0]) + (self.position[2]+pos[2])*(self.position[2]+pos[2])) <= self.radius:
        bs.emitBGDynamics(position=(pos),
                          velocity=(0, 7, 0),
                          count=int(5 + random.random() * 5),
                          scale=random.random() * 2,
                          spread=random.random() * 0.2,
                          chunkType='sweat')
        if not self.stop:
            bs.gameTimer(5, bs.Call(self.spawnFire, self.position))
        # else:
        # if not self.stop:
        # bs.gameTimer(1,bs.Call(self.spawnFire,self.position))


class Shovel(bs.Actor):
    def __init__(self, position=(0, 1, 0), owner=None):

        bs.Actor.__init__(self)
        owner = bs.getActivity().players[0].actor.node

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'model':
                                   bs.getModel('shovel'),
                                   'lightModel':
                                   bs.getModel('shovel'),
                                   'body':
                                   'landMine',
                                   'shadowSize':
                                   0.5,
                                   'reflection':
                                   'soft',
                                   'colorTexture':
                                   bs.getTexture('shovel'),
                                   'materials':
                                   (bs.getSharedObject('footingMaterial'),
                                    bs.getSharedObject('objectMaterial'))
                               })

        m = bs.newNode('math',
                       owner=self.node,
                       attrs={
                           'input1': (1, 0, 0),
                           'operation': 'add'
                       })
        owner.connectAttr('torsoPosition', m, 'input2')
        m.connectAttr('output', self.node, 'position')

    # def update

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())

        elif isinstance(m, bs.HitMessage):
            m.srcNode.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2], m.magnitude,
                                    m.velocityMagnitude, m.radius, 0,
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2])


class Nuke(bs.Actor):
    def __init__(self, position=(0, 10, 0)):
        bs.Actor.__init__(self)
        bs.getActivity().stdEpic = bs.getSharedObject('globals').slowMotion
        self.impactBlastMaterial = bs.Material()
        self.impactBlastMaterial.addActions(
            conditions=(('weAreOlderThan', 200), 'and',
                        ('theyAreOlderThan', 200), 'and', ('evalColliding', ),
                        'and', (('theyHaveMaterial',
                                 bs.getSharedObject('footingMaterial')), 'or',
                                ('theyHaveMaterial',
                                 bs.getSharedObject('objectMaterial')))),
            actions=(('message', 'ourNode', 'atConnect', ImpactMessage())))

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'model':
                                   bs.getModel('nuke'),
                                   'lightModel':
                                   bs.getModel('nuke'),
                                   'body':
                                   'box',
                                   'modelScale':
                                   1.4,
                                   'bodyScale':
                                   1.4,
                                   'shadowSize':
                                   0.5,
                                   'reflection':
                                   'soft',
                                   'extraAcceleration': (0, 10, 0),
                                   'colorTexture':
                                   bs.getTexture('nuke'),
                                   'materials':
                                   (bs.getSharedObject('footingMaterial'),
                                    bs.getSharedObject('objectMaterial'),
                                    self.impactBlastMaterial)
                               })

        bs.playSound(bs.getSound('nukeFalling'))
        bs.getSharedObject('globals').slowMotion = True
        bs.gameTimer(2000, self.off)

    def off(self):
        bs.getSharedObject('globals').slowMotion = bs.getActivity().stdEpic

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())
        elif isinstance(m, ImpactMessage):
            bs.Blast(position=self.node.position, blastRadius=40).autoRetain()
            Toxic(position=self.node.position, radius=10, time=15000)
            self.node.handleMessage(bs.DieMessage())

        elif isinstance(m, bs.HitMessage):
            m.srcNode.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2], m.magnitude,
                                    m.velocityMagnitude, m.radius, 0,
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2])


class Number(bs.Actor):
    def __init__(self, position=(0, 1, 0), num=0, velocity=(0, 0, 0)):

        bs.Actor.__init__(self)
        self.node = bs.newNode(
            'prop',
            delegate=self,
            attrs={
                'position':
                position,
                'model':
                bs.getModel('one') if num == 1 else bs.getModel('zero'),
                'lightModel':
                bs.getModel('one') if num == 1 else bs.getModel('zero'),
                'body':
                'box',
                'velocity':
                velocity,
                'modelScale':
                0.8,
                'bodyScale':
                0.5,
                'shadowSize':
                0.5,
                'reflection':
                'soft',
                'colorTexture':
                bs.getTexture('greenTerminal'),
                'materials': (bs.getSharedObject('footingMaterial'),
                              bs.getSharedObject('objectMaterial'))
            })

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())

        elif isinstance(m, bs.HitMessage):
            m.srcNode.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2], m.magnitude,
                                    m.velocityMagnitude, m.radius, 0,
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2])


class Artillery(object):
    def __init__(self,
                 position=(0, 1, 0),
                 target=None,
                 owner=None,
                 bombType='impact',
                 sourcePlayer=None):

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
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedSpaz)))

        self.node = bs.newNode('region',
                               attrs={
                                   'position': self.position,
                                   'scale': (0.5, 0.5, 0.5),
                                   'type': 'sphere',
                                   'materials': [self.aimZone]
                               })

        bsUtils.animateArray(self.node, "scale", 3, {
            0: (0.5, 0.5, 0.5),
            100: (self.radius, self.radius, self.radius)
        })
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
                    b = bs.Bomb(position=self.position,
                                velocity=(0, 5, 0),
                                bombType=self.bombType).autoRetain()
                    b.node.extraAcceleration = (0, 700, 0)
                    b.node.velocity = (b.node.velocity[0] +
                                       (self.pos[0] - b.node.position[0]), 10,
                                       b.node.velocity[2] +
                                       (self.pos[2] - b.node.position[2]))

            # bs.gameTimer(100,bs.Call(launchBomb))
            # bs.gameTimer(200,bs.Call(launchBomb))
            # bs.gameTimer(300,bs.Call(launchBomb))
            # bs.gameTimer(400,bs.Call(launchBomb))
            # bs.gameTimer(500,bs.Call(launchBomb))
            # bs.gameTimer(700,bs.Call(launchBomb))
            bs.gameTimer(1, bs.Call(self.drop))

    def drop(self):
        if self.target is not None and self.target.exists():
            self.pos = self.target.position

        def launchBombDrop():
            if self.target is not None and self.target.exists():
                # b = bs.Bomb(position = (self.pos[0]+(-2+random.random()*4),self.maxHeight[4],self.pos[2]+(-2+random.random()*4)),velocity = (0,-100,0),bombType = self.bombType,sourcePlayer = self.sourcePlayer).autoRetain()
                b = bs.Bomb(position=(self.pos[0], self.maxHeight[4],
                                      self.pos[2]),
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


class DirtRain(object):
    def __init__(self):
        x = -10
        while x < 10:
            z = -10
            x += 1
            while z < 10:
                z += 1
                Clay(position=(x + random.random(), 1, z + random.random()),
                     velocity=(random.random(), random.random(),
                               random.random())).autoRetain()


class AutoAim(object):
    def __init__(self, whoControl, owner, aliveOnly=True):

        self.whoControl = whoControl
        self.owner = owner
        self.aliveOnly = aliveOnly
        self.target = None

        self.aimZoneSpaz = bs.Material()
        self.aimZoneSpaz.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedSpaz)))

        # self.aimZoneObject = bs.Material()
        # self.aimZoneObject.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial'))),actions=(("modifyPartCollision","collide",True),
        # ("modifyPartCollision","physical",False),
        # ("call","atConnect", self.touchedObject)))

        self.lookForSpaz()

    def lookForSpaz(self):
        self.whoControl.extraAcceleration = (0, 20, 0)
        self.node = bs.newNode(
            'region',
            attrs={
                'position':
                (self.whoControl.position[0], self.whoControl.position[1],
                 self.whoControl.position[2]) if self.whoControl.exists() else
                (0, 0, 0),
                'scale': (0.0, 0.0, 0.0),
                'type':
                'sphere',
                'materials': [self.aimZoneSpaz]
            })
        self.s = bsUtils.animateArray(self.node, "scale", 3, {
            0: (0.0, 0.0, 0.0),
            100: (60, 60, 60)
        })

        def explode():
            if not self.owner.exists():
                bs.Blast(position=self.whoControl.position,
                         blastRadius=0.3).autoRetain()
                self.whoControl.handleMessage(bs.DieMessage())

        bs.gameTimer(150, self.node.delete)
        bs.gameTimer(50, explode)

        def checkTarget():
            if self.target is None:
                explode()
            else:
                self.touchedSpaz()

        bs.gameTimer(151, checkTarget)

    # def lookForObject(self):

    # self.whoControl.extraAcceleration = (0,20,0)
    # self.node2 = bs.newNode('region',
    # attrs={'position':(self.whoControl.position[0],self.whoControl.position[1],self.whoControl.position[2]) if self.whoControl.exists() else (0,0,0),
    # 'scale':(0.0,0.0,0.0),
    # 'type':'sphere',
    # 'materials':[self.aimZoneObject]})
    # self.s = bsUtils.animateArray(self.node2,"scale",3,{0:(0.0,0.0,0.0),100:(60,60,60)})
    # def explode():
    # if not self.owner.exists():
    # bs.Blast(position = self.whoControl.position,blastRadius = 0.3).autoRetain()
    # self.whoControl.handleMessage(bs.DieMessage())
    # bs.gameTimer(150,self.node2.delete)
    # bs.gameTimer(50,explode)
    # def checkTarget():
    # if self.target is None:
    # if not self.owner.exists():
    # bs.Blast(position = self.whoControl.position,blastRadius = 0.3).autoRetain()
    # self.whoControl.handleMessage(bs.DieMessage())
    # else:
    # self.touchedObject()
    # bs.gameTimer(151,checkTarget)

    def go(self):
        if self.target is not None and self.whoControl is not None and self.whoControl.exists(
        ):
            try:
                self.whoControl.velocity = (
                    self.whoControl.velocity[0] +
                    (self.target.position[0] - self.whoControl.position[0]),
                    self.whoControl.velocity[1] +
                    (self.target.position[1] - self.whoControl.position[1]),
                    self.whoControl.velocity[2] +
                    (self.target.position[2] - self.whoControl.position[2]))
            except:
                pass
            bs.gameTimer(1, self.go)

    def touchedSpaz(self):
        try:
            node = bs.getCollisionInfo('opposingNode')
            if hasattr(node.getDelegate(),
                       '_updateAI') and node.getDelegate().isAlive():
                self.target = node
                self.s = None
                self.node.delete()
                self.whoControl.extraAcceleration = (0, 20, 0)
                self.go()
                return
            if not node == self.owner and node.getDelegate().isAlive(
            ) and self.owner.getDelegate().getPlayer().getTeam(
            ) != node.getDelegate().getPlayer().getTeam():
                self.target = node
                self.s = None
                self.node.delete()
                self.whoControl.extraAcceleration = (0, 20, 0)
                self.go()
        except:
            pass

    # def touchedObject(self):
    # node = bs.getCollisionInfo('opposingNode')
    # if node.exists() and node.getNodeType() != 'terrain':
    # self.target = node
    # self.s = None
    # self.node.delete()
    # self.whoControl.extraAcceleration = (0,20,0)
    # self.go()

    def off(self):
        def sa():
            self.target = None
            try:
                self.whoControl.extraAcceleration = (0, 0, 0)
            except:
                pass

        bs.gameTimer(2500, sa)


class Portal(bs.Actor):
    def __init__(self,
                 position1=(0, 1, 0),
                 position2=(3, 1, 0),
                 color=(random.random(), random.random(), random.random())):
        bs.Actor.__init__(self)

        self.radius = 1.1
        self.position1 = position1
        self.position2 = position2
        self.cooldown = False

        self.portal1Material = bs.Material()
        self.portal1Material.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.Portal1)))

        self.portal2Material = bs.Material()
        self.portal2Material.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.Portal2)))

        self.portal1Material.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial')),'and',('theyDontHaveMaterial', bs.getSharedObject('playerMaterial'))),actions=(("modifyPartCollision","collide",True),
                                                       ("modifyPartCollision","physical",False),
                                                       ("call","atConnect", self.objPortal1)))

        self.portal2Material.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('objectMaterial')),'and',('theyDontHaveMaterial', bs.getSharedObject('playerMaterial'))),actions=(("modifyPartCollision","collide",True),
                                                       ("modifyPartCollision","physical",False),
                                                       ("call","atConnect", self.objPortal2)))

        self.node1 = bs.newNode('region',
                                attrs={
                                    'position':
                                    (self.position1[0], self.position1[1],
                                     self.position1[2]),
                                    'scale': (0.1, 0.1, 0.1),
                                    'type':
                                    'sphere',
                                    'materials': [self.portal1Material]
                                })
        self.visualRadius = bs.newNode('shield',
                                       attrs={
                                           'position': self.position1,
                                           'color': color,
                                           'radius': 0.1
                                       })
        bsUtils.animate(self.visualRadius, "radius", {
            0: 0,
            500: self.radius * 2
        })
        bsUtils.animateArray(self.node1, "scale", 3, {
            0: (0, 0, 0),
            500: (self.radius, self.radius, self.radius)
        })

        self.node2 = bs.newNode('region',
                                attrs={
                                    'position':
                                    (self.position2[0], self.position2[1],
                                     self.position2[2]),
                                    'scale': (0.1, 0.1, 0.1),
                                    'type':
                                    'sphere',
                                    'materials': [self.portal2Material]
                                })
        self.visualRadius2 = bs.newNode('shield',
                                        attrs={
                                            'position': self.position2,
                                            'color': color,
                                            'radius': 0.1
                                        })
        bsUtils.animate(self.visualRadius2, "radius", {
            0: 0,
            500: self.radius * 2
        })
        bsUtils.animateArray(self.node2, "scale", 3, {
            0: (0, 0, 0),
            500: (self.radius, self.radius, self.radius)
        })
        bs.gameTimer(10000, self.node1.delete)
        bs.gameTimer(10000, self.node2.delete)
        bs.gameTimer(10000, self.visualRadius2.delete)
        bs.gameTimer(10000, self.visualRadius.delete)

    def cooldown1(self):
        self.cooldown = True

        def off():
            self.cooldown = False

        bs.gameTimer(10, off)

    def Portal1(self):
        node = bs.getCollisionInfo('opposingNode')
        node.handleMessage(bs.StandMessage(position=self.node2.position))

    def Portal2(self):
        node = bs.getCollisionInfo('opposingNode')
        node.handleMessage(bs.StandMessage(position=self.node1.position))

    def objPortal1(self):
        node = bs.getCollisionInfo('opposingNode')
        v = node.velocity
        if not self.cooldown:
            node.position = self.position2
            self.cooldown1()

        def vel():
            node.velocity = v

        bs.gameTimer(10, vel)

    def objPortal2(self):
        node = bs.getCollisionInfo('opposingNode')
        v = node.velocity
        if not self.cooldown:
            node.position = self.position1
            self.cooldown1()

        def vel():
            node.velocity = v

        bs.gameTimer(10, vel)


class Toxic(bs.Actor):
    def __init__(self, position=(0, 1, 0), radius=2.5, time=8000):
        self.position = position
        bs.Actor.__init__(self)

        self.poisonMaterial = bs.Material()
        self.poisonMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedSpaz)))
        self.radius = radius

        self.node = bs.newNode('region',
                               attrs={
                                   'position':
                                   (self.position[0], self.position[1],
                                    self.position[2]),
                                   'scale': (0.1, 0.1, 0.1),
                                   'type':
                                   'sphere',
                                   'materials': [self.poisonMaterial]
                               })

        self.visualRadius = bs.newNode('shield',
                                       attrs={
                                           'position': self.position,
                                           'color': (0.3, 1.2, 0.3),
                                           'radius': 0.1
                                       })

        bsUtils.animate(self.visualRadius, "radius", {
            0: 0,
            500: self.radius * 2
        })
        bsUtils.animateArray(self.node, "scale", 3, {
            0: (0, 0, 0),
            500: (self.radius, self.radius, self.radius)
        }, True)

        bs.gameTimer(7700, bs.WeakCall(self.anim))
        bs.gameTimer(time, self.node.delete)
        bs.gameTimer(time, self.visualRadius.delete)

    def anim(self):
        bsUtils.animate(self.visualRadius, "radius", {
            0: self.radius * 2,
            200: 0
        })
        bsUtils.animateArray(self.node, "scale", 3, {
            0: (self.radius, self.radius, self.radius),
            200: (0, 0, 0)
        })

    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')
        node.handleMessage("knockout", 5000)

    def delete(self):
        self.node.delete()
        self.visualRadius.delete()


class Poison(bs.Actor):
    def __init__(self, position=(0, 1, 0), radius=2.2, owner=None):
        ######################################
        # Dont ask me, how in works!         #
        # I am too lazy to use a factory!(2) #
        ######################################
        self.position = position
        bs.Actor.__init__(self)
        self.poisonMaterial = bs.Material()
        self.radius = radius
        self.poisonMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedSpaz)))
        self.node = bs.newNode('region',
                               owner=owner,
                               attrs={
                                   'position':
                                   (self.position[0], self.position[1],
                                    self.position[2]),
                                   'scale': (0.1, 0.1, 0.1),
                                   'type':
                                   'sphere',
                                   'materials': [self.poisonMaterial]
                               })
        self.visualRadius = bs.newNode('shield',
                                       attrs={
                                           'position': self.position,
                                           'color': (0.3, 0.3, 0),
                                           'radius': 0.1
                                       })
        bsUtils.animate(self.visualRadius, "radius", {
            0: 0,
            200: self.radius * 2,
            400: 0
        })
        bsUtils.animateArray(
            self.node, "scale", 3, {
                0: (0, 0, 0),
                200: (self.radius, self.radius, self.radius),
                400: (0, 0, 0)
            })
        bs.gameTimer(250, self.node.delete)
        bs.gameTimer(250, self.visualRadius.delete)
        bs.emitBGDynamics(position=self.position,
                          count=100,
                          emitType='tendrils',
                          tendrilType='smoke')

    def touchedSpaz(self):
        try:
            node = bs.getCollisionInfo('opposingNode')
            node.getDelegate().curse()
        except Exception as e:
            pass

    def delete(self):
        self.node.delete()
        self.visualRadius.delete()


class BlackHole(bs.Actor):
    def __init__(self,
                 position=(0, 1, 0),
                 autoExpand=True,
                 scale=1,
                 doNotRandomize=False,
                 infinity=False,
                 owner=None):
        bs.Actor.__init__(self)
        self.shields = []

        self.position = (
            position[0] - 2 + random.random() * 4,
            position[1] + random.random() * 2, position[2] - 2 +
            random.random() * 4) if not doNotRandomize else position
        self.scale = scale
        self.suckObjects = []

        self.owner = owner

        self.blackHoleMaterial = bs.Material()
        self.suckMaterial = bs.Material()
        self.blackHoleMaterial.addActions(
            conditions=(('theyDontHaveMaterial',
                         bs.getSharedObject('objectMaterial')), 'and',
                        ('theyHaveMaterial',
                         bs.getSharedObject('playerMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedSpaz)))

        self.blackHoleMaterial.addActions(
            conditions=(('theyDontHaveMaterial',
                         bs.getSharedObject('playerMaterial')), 'and',
                        ('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedObj)))

        self.suckMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial'))),
            actions=(("modifyPartCollision", "collide",
                      True), ("modifyPartCollision", "physical", False),
                     ("call", "atConnect", self.touchedObjSuck)))

        self.node = bs.newNode('region',
                               attrs={
                                   'position':
                                   (self.position[0], self.position[1],
                                    self.position[2]),
                                   'scale': (scale, scale, scale),
                                   'type':
                                   'sphere',
                                   'materials': [self.blackHoleMaterial]
                               })

        self.suckRadius = bs.newNode('region',
                                     attrs={
                                         'position':
                                         (self.position[0], self.position[1],
                                          self.position[2]),
                                         'scale': (scale, scale, scale),
                                         'type':
                                         'sphere',
                                         'materials': [self.suckMaterial]
                                     })

        def dist():
            bs.emitBGDynamics(position=self.position,
                              emitType='distortion',
                              spread=6,
                              count=100)
            if self.node.exists():
                bs.gameTimer(1000, dist)

        dist()

        if not infinity:
            self._dieTimer = bs.Timer(10000, bs.WeakCall(self.explode))
        bsUtils.animateArray(self.node, "scale", 3, {
            0: (0, 0, 0),
            300: (self.scale, self.scale, self.scale)
        }, True)
        bsUtils.animateArray(self.suckRadius, "scale", 3, {
            0: (0, 0, 0),
            300: (self.scale * 8, self.scale * 8, self.scale * 8)
        }, True)

        for i in range(20):
            self.shields.append(
                bs.newNode('shield',
                           attrs={
                               'color': (random.random(), random.random(),
                                         random.random()),
                               'radius':
                               self.scale * 2,
                               'position':
                               self.position
                           }))

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
                bs.newNode('shield',
                           attrs={
                               'color': (random.random(), random.random(),
                                         random.random()),
                               'radius':
                               self.scale + 0.15,
                               'position':
                               self.position
                           }))

    def explode(self):
        bs.emitBGDynamics(position=self.position,
                          count=500,
                          scale=1,
                          spread=1.5,
                          chunkType='spark')
        for i in self.shields:
            bsUtils.animate(i, "radius", {0: 0, 200: i.radius * 5})
        bs.Blast(position=self.position, blastRadius=20).autoRetain()
        for i in self.shields:
            i.delete()
        self.node.delete()
        self.suckRadius.delete()
        self.node.handleMessage(bs.DieMessage())
        self.suckRadius.handleMessage(bs.DieMessage())

    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')
        bs.Blast(position=node.position, blastType='turret').autoRetain()
        if node.exists():
            if self.owner.exists():
                try:
                    node.handleMessage(
                        bs.HitMessage(
                            magnitude=1000.0,
                            sourcePlayer=self.owner.getDelegate().getPlayer()))
                    node.handleMessage(bs.DieMessage())
                except:
                    pass
                bs.shakeCamera(2)
            else:
                node.handleMessage(bs.DieMessage())
        self.addMass()

    def touchedObj(self):
        node = bs.getCollisionInfo('opposingNode')
        bs.Blast(position=node.position, blastType='turret').autoRetain()
        if node.exists():
            node.handleMessage(bs.DieMessage())

    def touchedObjSuck(self):
        node = bs.getCollisionInfo('opposingNode')
        if node.getNodeType() in ['prop', 'bomb', 'spaz']:
            self.suckObjects.append(node)

        for i in self.suckObjects:
            if i.exists():
                if i.getNodeType() != 'spaz':
                    i.extraAcceleration = ((self.position[0] - i.position[0]) *
                                           8,
                                           (self.position[1] - i.position[1]) *
                                           25,
                                           (self.position[2] - i.position[2]) *
                                           8)
                # else:
                #i.handleMessage("impulse", i.position[0], i.position[1], i.position[2],(self.position[0] - i.position[0]),(self.position[1] - i.position[1]),(self.position[2] - i.position[2]), 5, 0, 0, (self.position[0] - i.position[0]),(self.position[1] - i.position[1]),(self.position[2] - i.position[2]))
                # dir(i)
                #i.node.extraAcceleration = ((self.position[0] - i.position[0])*8,(self.position[1] - i.position[1])*25,(self.position[2] - i.position[2])*8)

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
            print 'ww'
            node = bs.getCollisionInfo('opposingNode')
            bs.Blast(position=self.position, blastType='turret').autoRetain()
            if not node.invincible:
                node.shattered = 2


class Lego(bs.Actor):
    def __init__(self,
                 position=(0, 1, 0),
                 num=int(random.random() * 3),
                 colorNum=int(random.random() * 3),
                 velocity=(0, 0, 0)):

        # i am too lazy, to use factory
        factory = self.getFactory()
        bs.Actor.__init__(self)
        self.node = bs.newNode(
            'prop',
            delegate=self,
            attrs={
                'position':
                position,
                'model':
                bs.getModel('lego1') if num == 1 else
                bs.getModel('lego2') if num == 2 else bs.getModel('lego3'),
                'lightModel':
                bs.getModel('lego1') if num == 1 else
                bs.getModel('lego2') if num == 2 else bs.getModel('lego3'),
                'body':
                'landMine',
                'velocity':
                velocity,
                'modelScale':
                0.8,
                'bodyScale':
                0.8,
                'shadowSize':
                0.5,
                'colorTexture':
                bs.getTexture('yellow')
                if colorNum == 1 else bs.getTexture('blue')
                if colorNum == 2 else bs.getTexture('red'),
                'reflection':
                'powerup',
                'reflectionScale': [1.0],
                'materials': (factory.legoMaterial,
                              bs.getSharedObject('footingMaterial'),
                              bs.getSharedObject('objectMaterial'))
            })

    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        try:
            return activity._sharedPortalFactory
        except Exception:
            f = activity._sharedPortalFactory = PortalFactory()
            return f

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())
        elif isinstance(m, bs.PickedUpMessage):
            self.node.sticky = False
        elif isinstance(m, bs.DroppedMessage):
            self.node.sticky = False
        elif isinstance(m, LegoConnect):
            self.node.sticky = True
        elif isinstance(m, FuckFuckFuckFuckingLego):
            self.node.sticky = False
            node = bs.getCollisionInfo('opposingNode')
            node.handleMessage("impulse", node.position[0], node.position[1],
                               node.position[2], node.velocity[0], 3,
                               node.velocity[2], 45, 45, 0, 0,
                               node.velocity[0], 3, node.velocity[2])
        elif isinstance(m, bs.HitMessage):

            m.srcNode.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2], m.magnitude,
                                    m.velocityMagnitude, m.radius, 0,
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2])


class cCube(bs.Actor):
    def __init__(self,
                 position=(0, 1, 0),
                 velocity=(0, 0, 0),
                 companion=False):
        bs.Actor.__init__(self)
        factory = self.getFactory()
        self.light = None
        self.regenTimer = None
        self.uptimer = None

        self.cubeMaterial = bs.Material()
        self.cubeMaterial.addActions(
            conditions=(('theyHaveMaterial',
                         bs.getSharedObject('dirtMaterial'))),
            actions=(("call", "atConnect", self.shitHitsTheCube)))

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'velocity':
                                   velocity,
                                   'model':
                                   factory.companionCubeModel,
                                   'lightModel':
                                   factory.companionCubeModel,
                                   'body':
                                   'crate',
                                   'shadowSize':
                                   0.5,
                                   'colorTexture':
                                   factory.companionCubeTex if companion
                                   == True else factory.weightCubeTex,
                                   'reflection':
                                   'soft',
                                   'reflectionScale': [0.3],
                                   'materials':
                                   (bs.getSharedObject('objectMaterial'),
                                    bs.getSharedObject('footingMaterial'),
                                    self.cubeMaterial)
                               })

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
        bs.emitBGDynamics(position=node.position,
                          count=30,
                          scale=1.3,
                          spread=0.1,
                          chunkType='sweat')
        node.handleMessage(bs.DieMessage())

    def handleMessage(self, m):
        factory = self.getFactory()
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.PickedUpMessage):
            self.node.extraAcceleration = (0, 25, 0)

            def up():
                self.node.extraAcceleration = (0, 40, 0)

            self.uptimer = bs.Timer(330, up)

            def checker():
                if m is None or not m.node.exists():
                    self.node.extraAcceleration = (0, 0, 0)

            bs.gameTimer(100, checker)

            self.spazNode = m.node
            delegate = m.node.getDelegate()

            self.light = bs.newNode('light',
                                    attrs={
                                        'position': self.node.position,
                                        'color': (0, 1, 0),
                                        'volumeIntensityScale': 1.0,
                                        'intensity': 0.1,
                                        'radius': 0.6
                                    })
            m.node.connectAttr('position', self.light, 'position')

            def regen():
                if m is not None and m.node.exists() and m.node.getDelegate(
                ).hitPoints < m.node.getDelegate().hitPointsMax:
                    delegate.hitPoints += 1
                    delegate._lastHitTime = None
                    delegate._numTimesHit = 0
                    m.node.hurt -= 0.001
                    bs.emitBGDynamics(position=m.node.position,
                                      velocity=(0, 3, 0),
                                      count=int(3.0 + random.random() * 5),
                                      scale=1.5,
                                      spread=0.3,
                                      chunkType='sweat')

                else:
                    if self.light is not None and self.light.exists():
                        self.light.delete()
                        self.regenTimer = None

            self.regenTimer = bs.Timer(10, regen, repeat=True)

        elif isinstance(m, bs.DroppedMessage):
            self.regenTimer = None
            self.uptimer = None
            self.spazNode = None
            self.node.extraAcceleration = (0, 0, 0)
            if self.light is not None and self.light.exists():
                self.light.delete()

        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2], m.magnitude,
                                    m.velocityMagnitude, m.radius, 0,
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2])


class bubbleGenerator(bs.Actor):
    def __init__(self,
                 position=(0, 1, 0),
                 velocity=(random.random(), random.random(), random.random()),
                 speed=30,
                 sound=True):

        bs.Actor.__init__(self)

        factory = self.getFactory()

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'velocity':
                                   velocity,
                                   'model':
                                   factory.bubbleGeneratorModel,
                                   'lightModel':
                                   factory.bubbleGeneratorModel,
                                   'body':
                                   'crate',
                                   'bodyScale':
                                   1.0,
                                   'shadowSize':
                                   0.5,
                                   'colorTexture':
                                   factory.bubbleGeneratorTex,
                                   'reflection':
                                   'soft',
                                   'reflectionScale': [0.23],
                                   'materials':
                                   (factory.impactBlastMaterial,
                                    bs.getSharedObject('objectMaterial'))
                               })

        self.speed = speed
        if sound:
            bs.playSound(bs.getSound('motor'),
                         position=self.node.position,
                         volume=0.5)
        self.idiotizmAHeKOD()
        self._selfKiller = bs.Timer(26400, bs.Call(self.selfKill))

    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.FlagFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        try:
            return activity._sharedPortalFactory
        except Exception:
            f = activity._sharedPortalFactory = PortalFactory()
            return f

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m, bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()

    def idiotizmAHeKOD(self):
        self._worker = bs.Timer(self.speed,
                                bs.WeakCall(self.work),
                                repeat=True)

    def work(self):
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 3, random.random() * 3,
                         random.random() * 3),
               color=(random.random() + 1, random.random() + 1,
                      random.random() + 1),
               thrust=(random.random() * 6) + 19,
               size=random.random() * 0.6).autoRetain()

    def selfKill(self):
        bs.Blast(position=self.node.position).autoRetain()
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 5, random.random() * 5,
                         random.random() * 5),
               color=(random.random() + 0.2, random.random() + 0.2,
                      random.random() + 0.2),
               thrust=random.random() * 30,
               size=random.random() * 0.6).autoRetain()
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 5, random.random() * 5,
                         random.random() * 5),
               color=(random.random() + 0.2, random.random() + 0.2,
                      random.random() + 0.2),
               thrust=random.random() * 30,
               size=random.random() * 0.6).autoRetain()
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 5, random.random() * 5,
                         random.random() * 5),
               color=(random.random() + 0.2, random.random() + 0.2,
                      random.random() + 0.2),
               thrust=random.random() * 30,
               size=random.random() * 0.6).autoRetain()
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 5, random.random() * 5,
                         random.random() * 5),
               color=(random.random() + 0.2, random.random() + 0.2,
                      random.random() + 0.2),
               thrust=random.random() * 30,
               size=random.random() * 0.6).autoRetain()
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 5, random.random() * 5,
                         random.random() * 5),
               color=(random.random() + 0.2, random.random() + 0.2,
                      random.random() + 0.2),
               thrust=random.random() * 30,
               size=random.random() * 0.6).autoRetain()
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 5, random.random() * 5,
                         random.random() * 5),
               color=(random.random() + 0.2, random.random() + 0.2,
                      random.random() + 0.2),
               thrust=random.random() * 30,
               size=random.random() * 0.6).autoRetain()
        Bubble(position=(self.node.position[0] + random.random() * 0.3,
                         self.node.position[1] + 0.4,
                         self.node.position[2] + random.random() * 0.3),
               velocity=(random.random() * 5, random.random() * 5,
                         random.random() * 5),
               color=(random.random() + 0.2, random.random() + 0.2,
                      random.random() + 0.2),
               thrust=random.random() * 30,
               size=random.random() * 0.6).autoRetain()
        self._starterWorker = None
        self._worker = None
        self._motorSound = None
        self._selfKiller = None
        self.node.delete()


class Bubble(bs.Actor):
    def __init__(self,
                 position=(0, 1, 0),
                 velocity=(0, 0, 0),
                 size=0.5,
                 thrust=21,
                 color=(1, 1, 1)):

        bs.Actor.__init__(self)

        factory = self.getFactory()

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'velocity':
                                   velocity,
                                   'gravityScale':
                                   0,
                                   'body':
                                   'sphere',
                                   'bodyScale':
                                   size,
                                   'extraAcceleration': (0, thrust, 0),
                                   'materials':
                                   (factory.impactBlastMaterial,
                                    bs.getSharedObject('footingMaterial'))
                               })

        self.bubble = bs.newNode('shield',
                                 owner=self.node,
                                 attrs={
                                     'color': color,
                                     'radius': size - 0.3
                                 })

        self.node.connectAttr('position', self.bubble, 'position')

        self.bubble.alwaysShowHealthBar = False
        self.inv = True
        self._inv = bs.Timer(1000, bs.Call(self.invOff))

    @classmethod
    def getFactory(cls):
        activity = bs.getActivity()
        try:
            return activity._sharedPortalFactory
        except Exception:
            f = activity._sharedPortalFactory = PortalFactory()
            return f

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m, bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m, ImpactMessage) or isinstance(
                m, bs.PickedUpMessage) or isinstance(m, bs.HitMessage):
            if not self.inv:
                self.deadEffect()

    def invOff(self):
        self.inv = False
        self._inv = None

    def deadEffect(self):
        bsUtils.animate(self.bubble, 'radius', {
            0: self.bubble.radius,
            90: self.bubble.radius * 2.3
        })
        bs.emitBGDynamics(position=self.node.position,
                          count=50,
                          scale=0.4,
                          spread=0.5,
                          chunkType='spark')
        self.dieTimer = bs.Timer(22, bs.WeakCall(self.bubbleDie))

    def bubbleDie(self):
        self.node.delete()
        self.bubble.delete()


class Clay(bs.Actor):
    def __init__(self,
                 position=(0, 1, 0),
                 velocity=(0, 0, 0),
                 bomb=False,
                 banana=False,
                 owner=None):

        bs.Actor.__init__(self)

        self.dirtDieMaterial = bs.Material()
        self.dirtDieMaterial.addActions(conditions=(('weAreOlderThan', 2000)),
                                        actions=(("message",
                                                  "ourNode", "atConnect",
                                                  bs.DieMessage())))

        self.dirtDieMaterial.addActions(
            conditions=(("theyHaveMaterial",
                         bs.getSharedObject('playerMaterial')), 'and',
                        ('weAreYoungerThan', 2000)),
            actions=(("message", "ourNode", "atConnect", dirtBombMessage())))

        self.dirtDieMaterial.addActions(
            conditions=(("theyHaveMaterial",
                         bs.getSharedObject('footingMaterial')), 'and',
                        ('weAreYoungerThan', 2000)),
            actions=(("message", "ourNode", "atConnect", bs.DieMessage())))

        self.bomb = bomb
        self.owner = owner
        self.banana = banana

        self.node = bs.newNode(
            'prop',
            delegate=self,
            attrs={
                'position':
                position,
                'velocity':
                velocity,
                'model':
                bs.getModel("box") if not banana else bs.getModel("slice"),
                'body':
                'sphere',
                'bodyScale':
                0.3,
                'modelScale':
                0.15 if not banana else 0.4,
                'sticky':
                False,
                'colorTexture':
                bs.getTexture("dirt")
                if not banana else bs.getTexture("yellow"),
                'materials': (bs.getSharedObject('objectMaterial'),
                              bs.getSharedObject('dirtMaterial'))
            })
        if bomb and not banana:
            self.node.materials = self.node.materials + (
                self.dirtDieMaterial, )

        if banana:
            bs.gameTimer(1000 + random.randint(0, 500), bs.Call(self.explode))

        def stick():
            if self.node.exists():
                self.node.sticky = True

        bs.gameTimer(100, bs.Call(stick))

    def explode(self):
        bs.Blast(position=self.node.position,
                 sourcePlayer=self.owner,
                 notShake=True,
                 blastRadius=0.8,
                 notScorch=True).autoRetain()
        self.node.handleMessage(bs.DieMessage())

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, dirtBombMessage):
            if not self.banana:
                bs.Blast(position=self.node.position,
                         hitType='punch',
                         sourcePlayer=self.owner,
                         notShake=True,
                         blastRadius=0.5).autoRetain()
                self.node.handleMessage(bs.DieMessage())
        elif isinstance(m, bs.HitMessage):
            self.node.handleMessage("impulse", m.pos[0], m.pos[1], m.pos[2],
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2], m.magnitude,
                                    m.velocityMagnitude, m.radius, 0,
                                    m.velocity[0], m.velocity[1],
                                    m.velocity[2])


class BadRock(bs.Actor):
    def __init__(self,
                 position=(0, 1, 0),
                 velocity=(0, 0, 0),
                 owner=None,
                 sourcePlayer=None,
                 expire=True,
                 hit=True):

        bs.Actor.__init__(self)

        factory = self.getFactory()

        self.hit = hit

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'velocity':
                                   velocity,
                                   'model':
                                   factory.badrockModel,
                                   'lightModel':
                                   factory.badrockModel,
                                   'body':
                                   'crate',
                                   'bodyScale':
                                   1.09,
                                   'shadowSize':
                                   0.5,
                                   'colorTexture':
                                   factory.minecraftTex,
                                   'reflection':
                                   'soft',
                                   'reflectionScale': [0.23],
                                   'materials':
                                   (factory.impactBlastMaterial,
                                    bs.getSharedObject('footingMaterial'),
                                    bs.getSharedObject('objectMaterial'))
                               })
        self.expire = expire

    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.FlagFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        try:
            return activity._sharedPortalFactory
        except Exception:
            f = activity._sharedPortalFactory = PortalFactory()
            return f

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m, bs.OutOfBoundsMessage):
            if self.node.exists():
                self.node.delete()
        if isinstance(m, ImpactMessage):
            if self.hit == True:
                bs.Blast(position=self.node.position,
                         hitType='punch',
                         blastRadius=1).autoRetain()
            if self.expire == True:
                if self.node.exists():
                    self._lifeTime = bs.Timer(5000, bs.WeakCall(self.animBR))
                    self._clrTime = bs.Timer(5310, bs.WeakCall(self.clrBR))

    def animBR(self):
        if self.node.exists():
            bs.animate(self.node, "modelScale", {0: 1, 200: 0})

    def clrBR(self):
        if self.node.exists():
            self.node.delete()


class Turret(bs.Actor):
    def __init__(self,
                 position=(0, 2, 0),
                 velocity=(0, 0, 0),
                 different=False,
                 hasLaser=True,
                 mute=False):
        # hasLaser used in older versions
        bs.Actor.__init__(self)

        self.turretModel = bs.getModel('puck')
        self.turretClosedModel = bs.getModel('puck')
        self.turretTex = bs.getTexture('puckColor')
        self.mute = True
        self.turretMaterial = bs.Material()
        self.turretMaterial.addActions(
            conditions=(('weAreOlderThan', 200), 'and',
                        ('theyAreOlderThan', 200), 'and', ('evalColliding', ),
                        'and', (('theyHaveMaterial',
                                 bs.getSharedObject('footingMaterial')), 'or',
                                ('theyHaveMaterial',
                                 bs.getSharedObject('objectMaterial')))),
            actions=(('message', 'ourNode', 'atConnect',
                      TurretImpactMessage())))

        self.closed = True
        self.activated = False
        self.phrase = 1
        self.different = different

        self.node = bs.newNode('prop',
                               delegate=self,
                               attrs={
                                   'position':
                                   position,
                                   'velocity':
                                   velocity,
                                   'model':
                                   self.turretClosedModel,
                                   'lightModel':
                                   self.turretClosedModel,
                                   'body':
                                   'crate',
                                   'shadowSize':
                                   0.5,
                                   'colorTexture':
                                   self.turretTex,
                                   'reflection':
                                   'soft',
                                   'reflectionScale': [0.7],
                                   'materials':
                                   (bs.getSharedObject('footingMaterial'),
                                    bs.getSharedObject('objectMaterial'))
                               })

        # if not mute and not self.different: # for scene in main menu
        #     bs.playSound(bs.getSound(random.choice(['turret_activation','turret_autosearch','turret_hi','turret_see_you'])),position = self.node.position)

    def activate(self):
        if not self.mute:
            if not self.different:
                self.openTurret()
                if not self.activated:
                    self.activated = True

                    # bs.playSound(bs.getSound(random.choice(['turret_die1','turret_die2','turret_die3'])),position = self.node.position)

                    def shot():
                        bs.Blast(position=(self.node.position[0] +
                                           random.uniform(-2, 2),
                                           self.node.position[1] +
                                           random.uniform(-0.5, 0.5),
                                           self.node.position[2] +
                                           random.uniform(-2, 2)),
                                 blastType="turret",
                                 hitType='punch').autoRetain()

                    self._shotTimer = bs.Timer(50, bs.Call(shot), repeat=True)

                    def brokeTimer():
                        self._shotTimer = None
                        self.broke()

                    bs.gameTimer(2000, bs.Call(brokeTimer))

    def broke(self):
        def effect():
            if self.node.exists():
                bs.emitBGDynamics(position=self.node.position,
                                  count=int(2.0 + random.random() * 40),
                                  scale=0.5,
                                  spread=0.1,
                                  chunkType='spark')

        self._brokeTimer = bs.Timer(200, bs.Call(effect), repeat=True)
        self._explodeTimer = bs.Timer(8000, bs.WeakCall(self.explode))

    def openTurret(self):
        if self.node.exists():
            if not self.mute:
                if self.closed:
                    self.node.model = self.turretModel
                    bs.playSound(bs.getSound('servomotor'),
                                 position=self.node.position)
                    self.closed = False

    def explode(self):
        if self.node.exists():
            bs.Blast(position=self.node.position).autoRetain()
            self._brokeTimer = None
            self.node.handleMessage(bs.DieMessage())

    def handleMessage(self, m):
        if isinstance(m, bs.DieMessage):
            if self.node.exists():
                self.node.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.node.handleMessage(bs.DieMessage())
        elif isinstance(m, TurretImpactMessage):
            if not self.different:
                self.activate()
        elif isinstance(m, bs.PickedUpMessage):
            if not self.different and not self.mute:
                if not self.activated and not self.mute:
                    bs.playSound(bs.getSound(
                        random.choice([
                            'turret_pickup1', 'turret_pickup2',
                            'turret_pickup3'
                        ])),
                                 position=self.node.position)
                self.openTurret()
            else:
                # print str(self.node.getName()) +' is different'
                if self.phrase < 12:
                    bs.playSound(bs.getSound('turret_different_' +
                                             str(self.phrase)),
                                 position=self.node.position)
                    self.phrase += 1
        elif isinstance(m, bs.DroppedMessage):

            def addMaterial():
                self.node.materials = self.node.materials + \
                    (self.turretMaterial,)

            bs.gameTimer(50, bs.Call(addMaterial))
        elif isinstance(m, bs.HitMessage):
            if not self.different:
                self.activate()
