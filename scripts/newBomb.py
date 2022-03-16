import bs
import bsSpaz
import bsBomb
import bsUtils
from bsBomb import Bomb, ExplodeMessage, ArmMessage, WarnMessage, Blast, BombFactory, \
    ExplodeHitMessage, ImpactMessage, SplatMessage
import random
import fire
import random
import bsPowerup
import pcpowerup
import bsMap


class AimForOpponent(object):
    def __init__(self, bomb, owner):

        self.bomb = bomb
        self.owner = owner
        self.target = None

        self.aimZoneSpaz = bs.Material()
        self.aimZoneSpaz.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('playerMaterial'))),
                                    actions=(("modifyPartCollision", "collide", True),
                                             ("modifyPartCollision", "physical", False),
                                             ("call", "atConnect", self.touchedSpaz)))

        self.lookForSpaz()

    def lookForSpaz(self):
        # To slow down the movement of the bomb towards the target and put the bomb over the head of the target.
        self.bomb.extraAcceleration = (0, 20, 0)
        self.node = bs.newNode('region',
                               attrs={'position': (self.bomb.position[0], self.bomb.position[1],
                                                   self.bomb.position[2]) if self.bomb.exists() else (
                                   0, 0, 0),
                                      'scale': (0.0, 0.0, 0.0),
                                      'type': 'sphere',
                                      'materials': [self.aimZoneSpaz]})
        self.s = bsUtils.animateArray(self.node, "scale", 3, {0: (0.0, 0.0, 0.0), 50: (60, 60, 60), 100: (90, 90, 90)},
                                      True)

        bs.gameTimer(150, self.node.delete)

        def checkTarget():
            if self.target is not None:
                self.touchedSpaz()

        bs.gameTimer(151, checkTarget)

    def go(self):
        if self.target is not None and self.bomb is not None and self.bomb.exists():
            self.bomb.velocity = (
                self.bomb.velocity[0] + (self.target.position[0] - self.bomb.position[0]),
                self.bomb.velocity[1] + (self.target.position[1] - self.bomb.position[1]),
                self.bomb.velocity[2] + (self.target.position[2] - self.bomb.position[2]))
            bs.gameTimer(1, self.go)

    def touchedSpaz(self):
        try:
            node = bs.getCollisionInfo('opposingNode')
        except AttributeError:
            return
        if not node == self.owner and node.getDelegate().isAlive() \
                and node.getDelegate().getPlayer().getTeam() != self.owner.getDelegate().getPlayer().getTeam():
            self.target = node
            self.s = None
            self.node.delete()
            self.bomb.extraAcceleration = (0, 200, 0)
            self.go()


class AntiGravArea(object):
    """For making the area to give the spaz upward force."""

    def __init__(self, position, radius):
        self.position = (position[0], position[1] + 1, position[2])
        self.radius = radius
        color = (random.random(), random.random(), random.random())
        self.material = bs.Material()
        self.material.addActions(conditions=(('theyHaveMaterial', bs.getSharedObject('playerMaterial'))),
                                 actions=(("modifyPartCollision", "collide", True),
                                          ("modifyPartCollision", "physical", False),
                                          ("call", "atConnect", self.touchedSpaz)))
        self.node = bs.newNode('region',
                               attrs={'position': (self.position[0], self.position[1], self.position[2]),
                                      'scale': (self.radius, self.radius, self.radius),
                                      'type': 'sphere',
                                      'materials': [self.material]})
        self.visualRadius = bs.newNode('shield', attrs={'position': self.position, 'color': color, 'radius': 0.1})
        bsUtils.animate(self.visualRadius, "radius", {0: 0, 500: self.radius * 2})
        bsUtils.animateArray(self.node, "scale", 3, {0: (0, 0, 0), 500: (self.radius, self.radius, self.radius)})

    def delete(self):
        if self.node.exists():
            self.node.delete()
        if self.visualRadius.exists():
            self.visualRadius.delete()

    def touchedSpaz(self):
        node = bs.getCollisionInfo('opposingNode')

        def raiseSpaz():
            if node.getDelegate().isAlive():
                node.handleMessage("impulse", node.position[0], node.position[1] + 0.5, node.position[2], 0, 5, 0,
                                   3, 10, 0, 0, 0, 5, 0)
                bs.gameTimer(50, raiseSpaz)
        raiseSpaz()


class NewBombFactory(BombFactory):
    def __init__(self):
        BombFactory.__init__(self)
        self.newTex = bs.getTexture("achievementOnslaught")
        self.bombModel = bs.getModel('bomb')
        self.stickyBombModel = bs.getModel('bombSticky')
        self.impactBombModel = bs.getModel('impactBomb')
        self.landMineModel = bs.getModel('landMine')
        self.epicMineModel = bs.getModel('landMine')
        self.powerupModel = bs.getModel('landMine')
        self.tntModel = bs.getModel('tnt')
        self.curseBombModel = bs.getModel('impactBomb')
        self.knockBombModel = bs.getModel('impactBomb')
        self.weedbombModel = bs.getModel('frostyHead')
        self.hybridBombModel = bs.getModel('impactBomb')
        self.iceImpactModel = bs.getModel('impactBomb')
        self.blastBombModel = bs.getModel('bomb')
        self.boomBombModel = bs.getModel('impactBomb')
        self.revengeBombModel = bs.getModel('bomb')
        self.gluebombModel = bs.getModel('bombSticky')
        self.atomBombModel = bs.getModel('bomb')
        self.spazBombModel = bs.getModel('neoSpazHead')
        self.frozenBombModel = bs.getModel('bomb')
        self.portalBombModel = bs.getModel('bombSticky')
        self.cursyBombModel = bs.getModel('frostyHead')
        self.teleBombModel = bs.getModel('frostyHead')
        self.iceMineModel = bs.getModel('landMine')
        self.stickyIceModel = bs.getModel('bombSticky')
        self.shockWaveModel = bs.getModel('bomb')

        self.regularTex = bs.getTexture('bombColor')
        self.iceTex = bs.getTexture('bombColorIce')
        self.stickyTex = bs.getTexture('bombStickyColor')
        self.impactTex = bs.getTexture('impactBombColor')
        self.impactLitTex = bs.getTexture('impactBombColorLit')
        self.landMineTex = bs.getTexture('landMine')
        self.epicMineTex = bs.getTexture('crossOutMask')
        self.landMineLitTex = bs.getTexture('landMineLit')
        self.tntTex = bs.getTexture('tnt')
        self.curseBombTex = bs.getTexture('bg')
        self.knockBombTex = bs.getTexture('egg2')
        self.weedbombTex = bs.getTexture('egg3')
        self.hybridBombTex = bs.getTexture('bg')
        self.iceImpactTex = bs.getTexture('levelIcon')
        self.blastBombTex = bs.getTexture('crossOutMask')
        self.boomBombTex = bs.getTexture('graphicsIcon')
        self.revengeBombTex = bs.getTexture('gameCircleIcon')
        self.gluebombTex = bs.getTexture('tickets')
        self.atomBombTex = bs.getTexture('gameCircleIcon')
        self.spazBombTex = bs.getTexture('neoSpazColor')
        self.frozenBombTex = bs.getTexture('achievementFlawlessVictory')
        self.portalBombTex = bs.getTexture('levelIcon')
        self.cursyBombTex = bs.getTexture('sparks')
        self.teleBombTex = bs.getTexture('sparks')
        self.fireBombTex = bs.getTexture('egg1')
        self.iceMineTex = bs.getTexture('egg2')
        self.iceMineLitTex = bs.getTexture('bombColorIce')
        self.stickyIceTex = bs.getTexture('egg4')
        self.shockWaveTex = bs.getTexture('achievementEmpty')
        
        self.powerupTex = bs.getTexture('powerupPunch')
        self.powerupTex1 = bs.getTexture('powerupShield')
        self.powerupTex2 = bs.getTexture('powerupImpactBombs')
        self.powerupTex3 = bs.getTexture('powerupHealth')
        self.powerupTex4 = bs.getTexture('powerupIceBombs')
        self.powerupTex5 = bs.getTexture('powerupBomb')
        self.powerupTex6 = bs.getTexture('powerupSpeed')

        self.newImpactBlastMaterial = bs.Material()
        self.newImpactBlastMaterial.addActions(
            conditions=(('weAreOlderThan', 200),
                        'and', ('theyAreOlderThan', 200),
                        'and', ('evalColliding',),
                        'and', ('theyDontHaveMaterial', bs.getSharedObject('playerMaterial')),
                        'and', ('theyHaveMaterial', self.bombMaterial),
                        'and', ('theyDontHaveMaterial', self.newImpactBlastMaterial)),
            actions=(('message', 'ourNode', 'atConnect', ImpactMessage())))


class NewBlast(Blast):
    def __init__(self, position=(0, 1, 0), velocity=(0, 0, 0), blastRadius=2.0,
                 blastType="normal", sourcePlayer=None, hitType='explosion',
                 hitSubType='normal'):
        bs.Actor.__init__(self)

        factory = Bomb.getFactory()

        self.blastType = blastType
        self.sourcePlayer = sourcePlayer

        self.hitType = hitType;
        self.hitSubType = hitSubType;

        # blast radius
        self.radius = blastRadius

        # set our position a bit lower so we throw more things upward
        self.node = bs.newNode('region', delegate=self, attrs={
            'position': (position[0], position[1] - 0.1, position[2]),
            'scale': (self.radius, self.radius, self.radius),
            'type': 'sphere',
            'materials': (factory.blastMaterial,
                          bs.getSharedObject('attackMaterial'))})

        bs.gameTimer(50, self.node.delete)

        # throw in an explosion and flash
        explosion = bs.newNode("explosion", attrs={
            'position': position,
            'velocity': (velocity[0], max(-1.0, velocity[1]), velocity[2]),
            'radius': self.radius,
            'big': (self.blastType == 'tnt')})
        if self.blastType == "ice":
            explosion.color = (0, 0.05, 0.4)
        elif self.blastType == 'spazBomb':
            explosion.color = (1,1,1)
        elif self.blastType == 'iceMine':
            explosion.color = (-4,2,5)
        elif self.blastType == 'stickyIce':
            explosion.color = (0,2,5)

        bs.gameTimer(1000, explosion.delete)

        if self.blastType != 'ice' or self.blastType != 'iceMine':
            bs.emitBGDynamics(position=position, velocity=velocity,
                              count=int(1.0 + random.random() * 4),
                              emitType='tendrils', tendrilType='thinSmoke')
        bs.emitBGDynamics(
            position=position, velocity=velocity,
            count=int(4.0 + random.random() * 4), emitType='tendrils',
            tendrilType='ice' if self.blastType == 'ice' else 'smoke')
        bs.emitBGDynamics(
            position=position, emitType='distortion',
            spread=1.0 if self.blastType == 'tnt' else 2.0)

        # and emit some shrapnel..
        if self.blastType == 'ice':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=30, spread=2.0, scale=0.4,
                                  chunkType='ice', emitType='stickers');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'iceMine':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=40, spread=2.0, scale=0.4,
                                  chunkType='ice', emitType='stickers');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'fireBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position,velocity=(0,10,0),count=100,scale=4,spread=0.4+random.random()*0.7,chunkType='sweat')
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'atomBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='slime');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='slime');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='slime',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'frozenBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='ice',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='ice',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='ice');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bits
            
        elif self.blastType == 'spikeBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='ice',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='ice',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='ice');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'teleBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='ice',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='ice',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='ice');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'sticky':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='slime');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='slime');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='slime',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'stickyIce':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='slime');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='slime',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='ice');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'cursyBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='metal',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='metal',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='metal');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'portalBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8),
                                  spread=0.7, chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.5,
                                  spread=0.7, chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=15, scale=0.6, chunkType='metal',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='metal',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(6.0 + random.random() * 12),
                                  scale=0.8, spread=1.5, chunkType='metal');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'iceImpact':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='ice');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='ice');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit

        elif self.blastType == 'impact':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'curseBomb':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'knockBomb':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'weedbomb':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'hybridBomb':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'boomBomb':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'shockWave':  # regular bomb shrapnel
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit

        elif self.blastType == 'headache':  # regular bomb shrapnel

            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'revengeBomb':  # regular bomb shrapnel

            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit
            
        elif self.blastType == 'gluebomb': # regular bomb shrapnel
            def _doEmit():
                g = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g.delete)
                g1 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g1.delete)
                g2 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g2.delete)
                g3 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g3.delete)
                g4 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g4.delete)
                g5 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g5.delete)
                g6 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g6.delete)
                g7 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g7.delete)
                g8 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g8.delete)
                g9 = bs.newNode('prop', delegate=self, attrs={'position':(position[0]-1+random.random()*3,position[1]+random.random()*2,position[2]-1+random.random()*3),'velocity':(0,0,0),'body':'sphere','shadowSize':0.3,'sticky':True,'colorTexture':factory.impactTex,'bodyScale':1.5})
                bs.gameTimer(6500,g9.delete)
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                bs.emitBGDynamics(position=(position[0]-1+random.random()*2,position[1]+random.random(),position[2]-1+random.random()*2),velocity=(0,0,0),count=5,scale=7.5,chunkType='slime',emitType='stickers');
                #bs.emitBGDynamics(position=position,emitType='distortion',spread=6,count = 100);
            bs.gameTimer(50,_doEmit) # looks better if we delay a bit
            
        elif self.blastType == 'spazBomb':
            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8), scale=2.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0+random.random()*8), scale=2.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=2.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0+random.random()*15), scale=2.8,
                                  spread=25.5, chunkType='spark');
            bs.gameTimer(50,_doEmit)
            
        elif self.blastType == 'blastBomb':  # regular bomb shrapnel

            def _doEmit():
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.8,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(4.0 + random.random() * 8), scale=0.4,
                                  chunkType='metal');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=20, scale=0.7, chunkType='spark',
                                  emitType='stickers');
                bs.emitBGDynamics(position=position, velocity=velocity,
                                  count=int(8.0 + random.random() * 15), scale=0.8,
                                  spread=1.5, chunkType='spark');

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit


        else:  # regular or land mine bomb shrapnel

            def _doEmit():

                if self.blastType != 'tnt':
                    bs.emitBGDynamics(position=position, velocity=velocity,

                                      count=int(4.0 + random.random() * 8),

                                      chunkType='rock');

                    bs.emitBGDynamics(position=position, velocity=velocity,

                                      count=int(4.0 + random.random() * 8),

                                      scale=0.5, chunkType='rock');

                bs.emitBGDynamics(position=position, velocity=velocity,

                                  count=30,

                                  scale=1.0 if self.blastType == 'tnt' else 0.7,

                                  chunkType='spark', emitType='stickers');

                bs.emitBGDynamics(position=position, velocity=velocity,

                                  count=int(18.0 + random.random() * 20),

                                  scale=1.0 if self.blastType == 'tnt' else 0.8,

                                  spread=1.5, chunkType='spark');

                # tnt throws splintery chunks

                if self.blastType == 'tnt':
                    def _emitSplinters():
                        bs.emitBGDynamics(position=position, velocity=velocity,

                                          count=int(20.0 + random.random() * 25),

                                          scale=0.8, spread=1.0,

                                          chunkType='splinter');

                    bs.gameTimer(10, _emitSplinters)

                # every now and then do a sparky one

                if self.blastType == 'tnt' or random.random() < 0.1:
                    def _emitExtraSparks():
                        bs.emitBGDynamics(position=position, velocity=velocity,

                                          count=int(10.0 + random.random() * 20),

                                          scale=0.8, spread=1.5,

                                          chunkType='spark');

                    bs.gameTimer(20, _emitExtraSparks)

            bs.gameTimer(50, _doEmit)  # looks better if we delay a bit

        light = bs.newNode('light', attrs={

            'position': position,

            'volumeIntensityScale': 10.0,

            'color': ((0.6, 0.6, 1.0) if self.blastType == 'ice'

                      else (1, 0.3, 0.1))})

        s = random.uniform(0.6, 0.9)

        scorchRadius = lightRadius = self.radius

        if self.blastType == 'tnt':
            lightRadius *= 1.4

            scorchRadius *= 1.15

            s *= 3.0

        iScale = 1.6

        bsUtils.animate(light, "intensity", {

            0: 2.0 * iScale, int(s * 20): 0.1 * iScale,

            int(s * 25): 0.2 * iScale, int(s * 50): 17.0 * iScale, int(s * 60): 5.0 * iScale,

            int(s * 80): 4.0 * iScale, int(s * 200): 0.6 * iScale,

            int(s * 2000): 0.00 * iScale, int(s * 3000): 0.0})

        bsUtils.animate(light, "radius", {

            0: lightRadius * 0.2, int(s * 50): lightRadius * 0.55,

            int(s * 100): lightRadius * 0.3, int(s * 300): lightRadius * 0.15,

            int(s * 1000): lightRadius * 0.05})

        bs.gameTimer(int(s * 3000), light.delete)

        # make a scorch that fades over time

        scorch = bs.newNode('scorch', attrs={

            'position': position,

            'size': scorchRadius * 0.5,

            'big': (self.blastType == 'tnt')})

        scorch.color = (random.random(), random.random(), random.random())
        if self.blastType == 'ice' or self.blastType == 'iceMine':
            scorch.color = (1, 1, 1.5)
        elif self.blastType == 'spazBomb':
            scorch.color = (1,1,1)        

        bsUtils.animate(scorch, "presence", {3000: 1, 13000: 0})

        bs.gameTimer(13000, scorch.delete)

        if self.blastType == 'ice' or self.blastType == 'ice':
            bs.playSound(factory.hissSound, position=light.position)
            
        elif self.blastType == 'spazBomb':
            bs.playSound(bs.getSound('spazFall01'))

        p = light.position

        bs.playSound(factory.getRandomExplodeSound(), position=p)

        bs.playSound(factory.debrisFallSound, position=p)

        bs.shakeCamera(intensity=5.0 if self.blastType == 'tnt' else 1.0)

        if self.blastType == 'tnt':
            bs.playSound(factory.getRandomExplodeSound(), position=p)

            def _extraBoom():
                bs.playSound(factory.getRandomExplodeSound(), position=p)

            bs.gameTimer(250, _extraBoom)

            def _extraDebrisSound():
                bs.playSound(factory.debrisFallSound, position=p)

                bs.playSound(factory.woodDebrisFallSound, position=p)

            bs.gameTimer(400, _extraDebrisSound)

    def handleMessage(self, msg):
        self._handleMessageSanityCheck()

        if isinstance(msg, bs.DieMessage):
            self.node.delete()

        elif isinstance(msg, ExplodeHitMessage):
            node = bs.getCollisionInfo("opposingNode")
            if node is not None and node.exists():
                t = self.node.position

                # new
                mag = 2000.0
                if self.blastType == 'ice': mag *= 0.5
                elif self.blastType == 'teleBomb': mag *= 0.45
                elif self.blastType == 'landMine': mag *= 2.5
                elif self.blastType == 'iceMine': mag *= 0.0
                elif self.blastType == 'epicMine': mag *= 1.5
                elif self.blastType == 'powerup': mag *= 1.5
                elif self.blastType == 'tnt': mag *= 2.0
                elif self.blastType == 'antiGrav': mag *= 0.1
                elif self.blastType == 'curseBomb': mag*= 0.0
                elif self.blastType == 'knockBomb': mag*= 0.0
                elif self.blastType == 'weedbomb': mag*= 0.5
                elif self.blastType == 'hybridBomb': mag*= 0.25
                elif self.blastType == 'iceImpact': mag*= 0.0
                elif self.blastType == 'boomBomb': mag*= 0.0
                elif self.blastType == 'shockWave': mag*= 0.6
                elif self.blastType == 'blastBomb': mag*= 0.4
                elif self.blastType == 'revengeBomb': mag*= 0.4
                elif self.blastType == 'gluebomb': mag*= 0.4
                elif self.blastType == 'atomBomb': mag*= 1.5
                elif self.blastType == 'frozenBomb': mag*= 0.0
                elif self.blastType == 'cursyBomb': mag*= 0.0
                elif self.blastType == 'portalBomb': mag*= 0.55
                elif self.blastType == 'fireBomb': mag *= 1.0
                elif self.blastType == 'stickyIce': mag *= 0.0
                elif self.blastType == 'spikeBomb': mag *= 0.7

                node.handleMessage(bs.HitMessage(
                    pos=t,
                    velocity=(0,0,0),
                    magnitude=mag,
                    hitType=self.hitType,
                    hitSubType=self.hitSubType,
                    radius=self.radius,
                    sourcePlayer=self.sourcePlayer))
                if self.blastType == "ice" or self.blastType == "iceImpact" or self.blastType == "iceMine" or self.blastType == "stickyIce":
                    bs.playSound(Bomb.getFactory().freezeSound, 10, position=t)
                    node.handleMessage(bs.FreezeMessage())
                elif self.blastType == "portalBomb":#fix curse
                    import objects as objs
                    self.portal = objs.Portal(position1=None, r=0.9,
                                                      color=(random.random(), random.random(), random.random()),
                                                      activity=bs.getActivity())
                elif self.blastType == "cursyBomb":
                    node.handleMessage(bs.PowerupMessage(powerupType='cursy'))#cursy
                elif self.blastType == "teleBomb":
                    mapBounds = self.getActivity().getMap().spawnPoints
                    node.handleMessage("stand", random.uniform(mapBounds[0][0], mapBounds[1][0]), random.uniform(mapBounds[0][1], mapBounds[1][1]), random.uniform(mapBounds[0][2], mapBounds[1][2]), random.randrange(0,360))
                    self._teleported = True
                    node.handleMessage("knockout", 45.0)
                elif self.blastType == "knockBomb":
                    node.handleMessage("knockout", 1000.7)
                    node.handleMessage("knockout", 400.7)
                elif self.blastType == "epicMine":
                    bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion == False
                    node.handleMessage(bs.PowerupMessage(powerupType='light'))
                    def _slowMo():
                        bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion == False
                    bs.gameTimer(5000,bs.Call(_slowMo))
                elif self.blastType == "blastBomb":
                    bs.Blast(position=self.node.position, velocity=(0,0,0), blastRadius=3,blastType="normal", sourcePlayer=None, hitType='explosion',hitSubType='normal').autoRetain()
                    bs.Blast(position=self.node.position, velocity=(0,0,0), blastRadius=3,blastType="normal", sourcePlayer=None, hitType='explosion',hitSubType='normal').autoRetain()
                    bs.Blast(position=self.node.position, velocity=(0,0,0), blastRadius=3,blastType="normal", sourcePlayer=None, hitType='explosion',hitSubType='normal').autoRetain()
                elif self.blastType == "boomBomb":
                    node.handleMessage(bs.PowerupMessage(powerupType='boom'))#boom
                elif self.blastType == "shockWave":
                    node.handleMessage(bs.PowerupMessage(powerupType='shock'))#boom
                elif self.blastType == "frozenBomb":
                    node.handleMessage(bs.PowerupMessage(powerupType='crazy'))#boom
                elif self.blastType == "revengeBomb":
                    node.handleMessage(bs.PowerupMessage(powerupType='revengeHit'))
                elif self.blastType == "weedbomb" and not node.getNodeType() != 'spaz':
                    bs.playSound(Bomb.getFactory().hissSound, 9, position=t)#sobydamn
                    def weed():
                	    node.handleMessage("knockout",10000)
                    bs.gameTimer(2000,bs.Call(weed)) #delay (forgot about the epic)
                    bs.gameTimer(5500,bs.Call(weed))
                    bs.gameTimer(8500,bs.Call(weed))
                    def hiccups():
                    	bs.emitBGDynamics(position=(node.position[0],node.position[1]-1.2,node.position[2]), velocity=(0,0.05,0), count=random.randrange(100,270), scale=1+random.random(), spread=0.71, chunkType='sweat') #reminds me of tom and jerry
                    bs.gameTimer(1000,bs.Call(hiccups))
                    bs.gameTimer(2500,bs.Call(hiccups)) #showing we are alive
                    bs.gameTimer(5000,bs.Call(hiccups))
                    bs.gameTimer(7500,bs.Call(hiccups))
                    def look():
                    	bubble = bsUtils.PopupText("high",color=(1,1,1), scale=0.7, randomOffset=0.2, offset=(0,-1,0), position=(node.position[0],node.position[1]-1.2,node.position[2])).autoRetain()
                    bs.gameTimer(1500,bs.Call(look))
                    bs.gameTimer(3000,bs.Call(look))
                    bs.gameTimer(8000,bs.Call(look))
                    def look():
                    	text = bsUtils.PopupText("OO",color=(1, 1, 1), scale=0.75, randomOffset=0.2, offset=(0,-1,0), position=(node.position[0],node.position[1]-1.2,node.position[2])).autoRetain()
                    bs.gameTimer(1460,bs.Call(look))
                    bs.gameTimer(2960,bs.Call(look))
                    bs.gameTimer(5460,bs.Call(look))
                    bs.gameTimer(7960,bs.Call(look))
                elif self.blastType == "curseBomb":
                    node.handleMessage(bs.PowerupMessage(powerupType='curse'))
                    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, -0.6, 0), 'operation': 'add'})
                    self.node.connectAttr('position', m, 'input2')
                    self.nodeShield = bs.newNode('shield', attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                           'position': self.node.position,
                                                                           'radius': 2.0})
                    m.connectAttr('output', self.nodeShield, 'position')
                    bs.gameTimer(300,self.nodeShield.delete)  

        else:
            bs.Actor.handleMessage(self, msg)


class NewBomb(Bomb):
    def __init__(self, position=(0, 1, 0), velocity=(0, 0, 0), bombType='normal',
                 blastRadius=2.0, sourcePlayer=None, owner=None):
        bs.Actor.__init__(self)

        factory = self.getFactory()

        if not bombType in ('headache', 'ice', 'impact', 'landMine', 'normal', 'sticky', 'tnt', 'antiGrav','curseBomb','iceImpact',
                            'blastBomb','boomBomb','revengeBomb','atomBomb','hybridBomb','knockBomb','weedbomb','gluebomb','spazBomb',
                            'frozenBomb','portalBomb','cursyBomb','teleBomb','fireBomb','epicMine','powerup','iceMine','stickyIce',
                            'shockWave','spikeBomb'):
            raise Exception("invalid bomb type: " + bombType)
        self.bombType = bombType

        self._exploded = False

        if self.bombType == 'sticky' or self.bombType == 'stickyIce': self._lastStickySoundTime = 0

        self.blastRadius = blastRadius
        if self.bombType == 'ice': self.blastRadius *= 1.2
        elif self.bombType == 'impact': self.blastRadius *= 0.7
        elif self.bombType == 'landMine': self.blastRadius *= 0.7
        elif self.bombType == 'iceMine': self.blastRadius *= 0.7
        elif self.bombType == 'epicMine': self.blastRadius *= 0.7
        elif self.bombType == 'powerup': self.blastRadius *= 0.7
        elif self.bombType == 'boomBomb': self.blastRadius *= 0.7
        elif self.bombType == 'shockWave': self.blastRadius *= 0.7
        elif self.bombType == 'tnt': self.blastRadius *= 1.45
        elif self.bombType == 'blastBomb': self.blastRadius *= 1.0
        elif self.bombType == 'revengeBomb': self.blastRadius *= 0.7
        elif self.bombType == 'gluebomb': self.blastRadius *= 0.7
        elif self.bombType == 'atomBomb': self.blastRadius *= 6.5
        elif self.bombType == 'spazBomb': self.blastRadius *= 0.75
        elif self.bombType == 'frozenBomb': self.blastRadius *= 0.8
        elif self.bombType == 'portalBomb': self.blastRadius *= 0.8
        elif self.bombType == 'cursyBomb': self.blastRadius *= 0.8
        elif self.bombType == 'teleBomb': self.blastRadius *= 1.2
        elif self.bombType == 'fireBomb': self.blastRadius *= 0.7
        elif self.bombType == 'spikeBomb': self.blastRadius *= 0.7

        self._explodeCallbacks = []

        # the player this came from
        self.sourcePlayer = sourcePlayer

        # by default our hit type/subtype is our own, but we pick up types of
        # whoever sets us off so we know what caused a chain reaction
        self.hitType = 'explosion'
        self.hitSubType = self.bombType

        # if no owner was provided, use an unconnected node ref
        if owner is None: owner = bs.Node(None)

        # the node this came from
        self.owner = owner

        # adding footing-materials to things can screw up jumping and flying
        # since players carrying those things
        # and thus touching footing objects will think they're on solid ground..
        # perhaps we don't wanna add this even in the tnt case?..
        if self.bombType == 'tnt':
            materials = (factory.bombMaterial,
                         bs.getSharedObject('footingMaterial'),
                         bs.getSharedObject('objectMaterial'))
        else:
            materials = (factory.bombMaterial,
                         bs.getSharedObject('objectMaterial'))

        if self.bombType == 'impact': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'headache': materials = materials + (factory.newImpactBlastMaterial,)
        elif self.bombType == 'landMine': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'iceMine': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'epicMine': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'powerup': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'blastBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'revengeBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'gluebomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'cursyBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'frozenBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'portalBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'atomBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'teleBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'spikeBomb': materials = materials + (factory.landMineNoExplodeMaterial,)
        elif self.bombType == 'antiGrav': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'curseBomb': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'knockBomb': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'weedbomb': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'hybridBomb': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'iceImpact': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'boomBomb': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'shockWave': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'spazBomb': materials = materials + (factory.impactBlastMaterial,)
        elif self.bombType == 'fireBomb': materials = materials + (factory.impactBlastMaterial,)

        if self.bombType == 'sticky' or self.bombType == 'stickyIce':
            materials = materials + (factory.stickyMaterial,)
        else:
            materials = materials + (factory.normalSoundMaterial,)

        if self.bombType == 'landMine':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.landMineModel,
                'lightModel': factory.landMineModel,
                'body': 'landMine',
                'shadowSize': 0.44,
                'colorTexture':factory.landMineTex,
                'reflection': 'powerup',
                'reflectionScale': [1.0],
                'materials': materials})
                
        elif self.bombType == 'iceMine':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.iceMineModel,
                'lightModel': factory.iceMineModel,
                'body': 'landMine',
                'shadowSize': 0.44,
                'colorTexture':factory.iceMineTex,
                'reflection': 'powerup',
                'reflectionScale': [1.0],
                'materials': materials})
                
        elif self.bombType == 'epicMine':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.landMineModel,
                'lightModel': factory.landMineModel,
                'body': 'landMine',
                'shadowSize': 0.44,
                'colorTexture': factory.epicMineTex,
                'reflection': 'powerup',
                'reflectionScale': [1.0],
                'materials': materials})

        elif self.bombType == 'powerup':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': bs.getModel('powerup'),
                'lightModel': bs.getModel('powerupSimple'),
                'body': 'box',
                'modelScale':1.1,
                'bodyScale':1.1,
                'shadowSize': 0.5,
                'colorTexture': random.choice([factory.powerupTex,
                                               factory.powerupTex1,
                                               factory.powerupTex2,
                                               factory.powerupTex3,
                                               factory.powerupTex4,
                                               factory.powerupTex5,
                                               factory.powerupTex6]),
                'reflection': 'powerup',
                'reflectionScale': [1.0],
                'materials': materials})

        elif self.bombType == 'tnt':
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': factory.tntModel,
                'lightModel': factory.tntModel,
                'body': 'crate',
                'shadowSize': 0.5,
                'colorTexture': factory.tntTex,
                'reflection': 'soft',
                'reflectionScale': [0.23],
                'materials': materials})

        elif self.bombType == 'impact':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.impactBombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.impactTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})
                
        elif self.bombType == 'curseBomb':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.curseBombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.curseBombTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})
                
        elif self.bombType == 'knockBomb':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.knockBombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.knockBombTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})
                
        elif self.bombType == 'weedbomb':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.weedbombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.weedbombTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})
                
        elif self.bombType == 'boomBomb':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.boomBombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.boomBombTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})
                
        elif self.bombType == 'shockWave':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.shockWaveModel,
                'shadowSize': 0.3,
                'colorTexture': factory.shockWaveTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})
                
        elif self.bombType == 'spazBomb':
            fuseTime = 20000
            bs.playSound(bs.getSound('spazImpact01'))
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position':position,
                'velocity':velocity,
                'body':'sphere',
                'model':factory.spazBombModel,
                'shadowSize':0.3,
                'modelScale':4.028,
                'colorTexture':factory.spazBombTex,
                'reflection':'powerup',
                'reflectionScale':[1.5],
                'materials':materials})
            bsUtils.animate(self.node,"modelScale",{0:0, 200:1.3, 260:1})    
            #bsUtils.animateArray(self.node,"position",3,{0:(random.randint(0,3), random.randint(0,3), random.randint(0,3)),10000:(random.randint(0,3), random.randint(0,3), random.randint(0,3)),95000:(random.randint(0,3), random.randint(0,3), random.randint(0,3))},loop = True)              
                
        elif self.bombType == 'iceImpact':
            fuseTime = 20000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.iceImpactModel,
                'shadowSize': 0.3,
                'colorTexture': random.choice([factory.iceImpactTex,
                                               factory.newTex,
                                               factory.fireBombTex]),
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})

        elif self.bombType == 'antiGrav':
            fuseTime = 30000
            self.node = bs.newNode('prop', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'body': 'sphere',
                'model': factory.impactBombModel,
                'shadowSize': 0.3,
                'colorTexture': factory.newTex,
                'reflection': 'powerup',
                'reflectionScale': [1.5],
                'materials': materials})
                
        elif self.bombType == 'fireBomb':
            fuseTime = 20000
            self.node = bs.newNode('prop',
                                   delegate=self,
                                   attrs={'position':position,
                                          'velocity':velocity,
                                          'body':'sphere',
                                          'model':factory.impactBombModel,
                                          'shadowSize':0.3,
                                          #'bodyScale':modelSize,
                                          'colorTexture':factory.fireBombTex,
                                          'reflection':'powerup',
                                          'reflectionScale':[1.5],
                                          'materials':materials})
            self._trailTimer = bs.Timer(10,bs.WeakCall(self._addTrail),repeat=True)

        else:
            fuseTime = 3000
            if self.bombType == 'sticky':
                sticky = True
                model = factory.stickyBombModel
                rType = 'sharper'
                rScale = 1.8
            elif self.bombType == 'stickyIce':
                sticky = True
                model = factory.stickyIceModel
                rType = 'sharper'
                rScale = 1.8
            elif self.bombType == 'teleBomb':
                sticky = False
                model = factory.teleBombModel
                rType = 'sharper'
                rScale = 1.8
            else:
                sticky = False
                model = factory.bombModel
                rType = 'sharper'
                rScale = 1.8
            if self.bombType == 'ice': tex = factory.iceTex
            elif self.bombType == 'spikeBomb': tex = factory.iceTex
            elif self.bombType == 'blastBomb': tex = factory.blastBombTex
            elif self.bombType == 'frozenBomb': tex = factory.frozenBombTex
            elif self.bombType == 'atomBomb': tex = factory.atomBombTex
            elif self.bombType == 'revengeBomb': tex = factory.revengeBombTex
            elif self.bombType == 'gluebomb': tex = factory.gluebombTex
            elif self.bombType == 'portalBomb': tex = factory.portalBombTex
            elif self.bombType == 'cursyBomb': tex = factory.cursyBombTex
            elif self.bombType == 'sticky': tex = factory.stickyTex
            elif self.bombType == 'stickyIce': tex = factory.stickyIceTex
            elif self.bombType == 'teleBomb': tex = factory.teleBombTex
            elif self.bombType == 'headache': fuseTime = 13000; tex = factory.newTex; model = factory.impactBombModel
            else: tex = factory.regularTex
            self.node = bs.newNode('bomb', delegate=self, attrs={
                'position': position,
                'velocity': velocity,
                'model': model,
                #'bodyScale': 0.6,
                'shadowSize': 0.3,
                'colorTexture': tex,
                'sticky': sticky,
                'owner': owner,
                'reflection': rType,
                'reflectionScale':[rScale] if bombType != 'normal' else ((0+random.random()*20.0),(0+random.random()*20.0),(0+random.random()*20.0)),
                'materials': materials})

            sound = bs.newNode('sound', owner=self.node, attrs={
                'sound': factory.fuseSound,
                'volume': 0.25})
            self.node.connectAttr('position', sound, 'position')
            bsUtils.animate(self.node, 'fuseLength', {0: 1.0, fuseTime: 0.0})

        # light the fuse!!!
        if self.bombType not in ('landMine', 'tnt','epicMine','powerup','iceMine'):
            bs.gameTimer(fuseTime, bs.WeakCall(self.handleMessage, ExplodeMessage()))
            animate = True
            prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),
                          250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)}

            if fire.bombName:
                m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.5, 0), 'operation': 'add'})
                self.node.connectAttr('position', m, 'input2')
                self.nodeText = bs.newNode('text',
                                           owner=self.node,
                                           attrs={'text': bombType,
                                                  'inWorld': True,
                                                  'shadow': 1.0,
                                                  'flatness': 1.0,
                                                  'color': (1,1,1),
                                                  'scale': 0.0,
                                                  'hAlign': 'center'})
                m.connectAttr('output', self.nodeText, 'position')
                bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.0125, 200: 0.01})
                if fire.animate:
                    bs.animateArray(self.nodeText,'color',3,{0:(2,2,0),600:(2,0,0),900:(0,2,0),1200:(0,0,2),1500:(2,0,2), 1800:(2,1,0),2100:(0,2,2),2400:(2,2,0)},True)
                    bs.emitBGDynamics(position=self.nodeText.position, velocity=self.node.position, count=200, scale=1.4, spread=2.01, chunkType='spark')

            if fire.animate:               
                self.shield = bs.newNode('shield', owner=self.node,
                attrs={'color':(0,0,1),'radius':0.9})
                self.node.connectAttr('position', self.shield, 'position')   
                bs.animate(self.shield,'radius',{0:0.9,200:1,400:0.9},True)
                bsUtils.animateArray(self.shield, 'color', 3, prefixAnim, True)
                
            if fire.animate:
                self.nodeLight = bs.newNode('light', owner=self.node,
                attrs={'position': self.node.position,
                'color': (0,0,1),'radius': 0.1,'volumeIntensityScale': 0.2})
                self.node.connectAttr('position', self.nodeLight, 'position')
                bs.animateArray(self.nodeLight,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True) 
                #bs.animate(self.nodeLight, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)
            
            bts = ('sticky','ice','revengeBomb','normal','blastBomb','hybridBomb','gluebomb','frozenBomb','cursyBomb',
                   'portalBomb','teleBomb','stickyIce','spikeBomb')#thats the trick for impact bombs :)
            if fire.bombTimer:
                if bombType in bts:
                    defaultPowerupInterval = 4000
                    self.powerupHurt = bs.newNode('shield', owner=self.node, attrs={'color':(1,1,1), 'radius':0.1, 'hurt':1, 'alwaysShowHealthBar':True})
                    self.node.connectAttr('position',self.powerupHurt, 'position')
                    bs.animate(self.powerupHurt, 'hurt', {0:0, defaultPowerupInterval-1000:1})
                    bs.gameTimer(defaultPowerupInterval-1000, bs.Call(self.do_delete))

            if fire.bombModel:    
                if self.bombType == bombType:
                    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, -0.03, 0), 'operation': 'add'})
                    self.node.connectAttr('position', m, 'input2')
                    self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                                'position': (
                                                                                    self.node.position[0],
                                                                                    self.node.position[1],
                                                                                    self.node.position[2] + 0.5),
                                                                                'radius': 0.5125})
                    m.connectAttr('output', self.nodeShield, 'position')
                    #bs.animate(self.shield,'radius',{0:0.9,200:1,400:0.9},True)
                    curve = bsUtils.animate(self.node,"modelScale",{0:0, 200:0.0, 260:1})
                    bs.gameTimer(200,curve.delete)
                    
            if fire.spikeModel:
                if self.bombType == bombType:
                    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, -0.03, 0), 'operation': 'add'})
                    self.node.connectAttr('position', m, 'input2')
                    self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                                'position': (
                                                                                    self.node.position[0],
                                                                                    self.node.position[1],
                                                                                    self.node.position[2] + 0.5),
                                                                                'radius': 0.5125})
                    m.connectAttr('output', self.nodeShield, 'position')
                    #bs.animate(self.shield,'radius',{0:0.9,200:1,400:0.9},True)
                    curve = bsUtils.animate(self.node,"modelScale",{0:0, 200:0.0, 260:1})
                    bs.gameTimer(200,curve.delete)
                    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.1, 0), 'operation': 'add'})
                    self.node.connectAttr('position', m, 'input2')
                    self.flash = bs.newNode("flash", owner=self.node,
                                                        attrs={'position':self.node.position,
                                                               'size':0.3,
                                                               'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
                    m.connectAttr('output', self.flash, 'position')
                    bs.gameTimer(7000,self.flash.delete)  
                    bs.animateArray(self.flash,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)

            if self.bombType == 'spikeBomb':
                    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, -0.03, 0), 'operation': 'add'})
                    self.node.connectAttr('position', m, 'input2')
                    self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                                'position': (
                                                                                    self.node.position[0],
                                                                                    self.node.position[1],
                                                                                    self.node.position[2] + 0.5),
                                                                                'radius': 0.5125})
                    m.connectAttr('output', self.nodeShield, 'position')
                    #bs.animate(self.shield,'radius',{0:0.9,200:1,400:0.9},True)
                    curve = bsUtils.animate(self.node,"modelScale",{0:0, 200:0.0, 260:1})
                    bs.gameTimer(200,curve.delete)
                    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.1, 0), 'operation': 'add'})
                    self.node.connectAttr('position', m, 'input2')
                    self.flash = bs.newNode("flash", owner=self.node,
                                                        attrs={'position':self.node.position,
                                                               'size':0.3,
                                                               'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
                    m.connectAttr('output', self.flash, 'position')
                    bs.gameTimer(7000,self.flash.delete)  
                    bs.animateArray(self.flash,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
            
            if fire.atomModel:    
                if self.bombType == 'atomBomb':
                    curve = bsUtils.animate(self.node,"modelScale",{0:0, 200:3.0, 260:1})
                    bs.gameTimer(200,curve.delete)       
                elif self.bombType == 'spazBomb':
                    curve = bsUtils.animate(self.node,"modelScale",{0:0, 200:1.3, 260:1})
                    bs.gameTimer(200,curve.delete)           
                elif self.bombType == 'teleBomb':
                    curve = bsUtils.animate(self.node,"modelScale",{0:0, 200:1.8, 260:1})
                    bs.gameTimer(200,curve.delete)                          
            
    def _handleDropped(self, m):
        if self.bombType == 'landMine' or self.bombType == 'epicMine' or self.bombType == 'powerup' or self.bombType == 'iceMine':
            self.armTimer = \
                bs.Timer(1250, bs.WeakCall(self.handleMessage, ArmMessage()))

        # once we've thrown a sticky bomb we can stick to it..
        elif self.bombType == 'sticky' or self.bombType == 'stickyIce':
            def _safeSetAttr(node, attr, value):
                if node.exists(): setattr(node, attr, value)

            bs.gameTimer(
                250, lambda: _safeSetAttr(self.node, 'stickToOwner', True))

        elif self.bombType == 'headache':
            AimForOpponent(self.node, self.owner)
            
    def do_delete(self):
        if self.node is not None and self.node.exists():
            if hasattr(self, "powerupHurt") and self.powerupHurt.exists():
                bs.gameTimer(100, self.powerupHurt.delete)

    def _addTrail(self):
        if self.node.exists():
            bs.emitBGDynamics(position=self.node.position,velocity=(0,1,0),count=50,spread=0.05,scale=4,chunkType='sweat')
        else: 
            self._trailTimer = None


    def _handleHit(self, msg):
        if self.bombType == 'headache' and msg.hitType == 'punch':
            self.handleMessage(ExplodeMessage())
        isPunch = (msg.srcNode.exists() and msg.srcNode.getNodeType() == 'spaz')

        # normal bombs are triggered by non-punch impacts..
        # impact-bombs by all impacts

        if (not self._exploded and not isPunch
                or self.bombType in ['impact', "antiGrav", 'landMine','curseBomb','iceImpact','boomBomb','hybridBomb',
                                     'knockBomb','weedbomb','spazBomb','fireBomb','epicMine','powerup','iceMine',
                                     'shockWave']):
            # also lets change the owner of the bomb to whoever is setting
            # us off.. (this way points for big chain reactions go to the
            # person causing them)
            if msg.sourcePlayer not in [None]:
                self.sourcePlayer = msg.sourcePlayer

                # also inherit the hit type (if a landmine sets off by a bomb,
                # the credit should go to the mine)
                # the exception is TNT.  TNT always gets credit.
                if self.bombType != 'tnt':
                    self.hitType = msg.hitType
                    self.hitSubType = msg.hitSubType

            bs.gameTimer(100 + int(random.random() * 100),
                         bs.WeakCall(self.handleMessage, ExplodeMessage()))
        self.node.handleMessage(
            "impulse", msg.pos[0], msg.pos[1], msg.pos[2],
            msg.velocity[0], msg.velocity[1], msg.velocity[2],
            msg.magnitude, msg.velocityMagnitude, msg.radius, 0,
            msg.velocity[0], msg.velocity[1], msg.velocity[2])

        if msg.srcNode.exists():
            pass

    def _handleImpact(self, m):
        node, body = bs.getCollisionInfo("opposingNode", "opposingBody")
        # if we're an impact bomb or anti-gravity bomb and we came from this node, don't explode...
        # alternately if we're hitting another impact-bomb from the same source,
        # don't explode...
        try:
            nodeDelegate = node.getDelegate()
        except Exception:
            nodeDelegate = None
        if node is not None and node.exists():
            if (self.bombType == 'impact' and
                    (node is self.owner
                     or (isinstance(nodeDelegate, Bomb)
                         and nodeDelegate.bombType == 'impact'
                         and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'antiGrav' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'antiGrav'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'curseBomb' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'curseBomb'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'knockBomb' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'knockBomb'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'spazBomb' and
                (node is self.owner
                 or (isinstance(nodeDelegate, Bomb)
                     and nodeDelegate.bombType == 'spazBomb'
                     and nodeDelegate.owner is self.owner))):
                return   
            elif (self.bombType == 'weedbomb' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'weedbomb'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'hybridBomb' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'hybridBomb'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'iceImpact' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'iceImpact'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'boomBomb' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'boomBomb'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'shockWave' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'shockWave'
                       and nodeDelegate.owner is self.owner))):
                return
            elif (self.bombType == 'fireBomb' and
                  (node is self.owner
                   or (isinstance(nodeDelegate, Bomb)
                       and nodeDelegate.bombType == 'fireBomb'
                       and nodeDelegate.owner is self.owner))):
                return
            else:
                self.handleMessage(ExplodeMessage())
                
    def arm(self):
        """
        Arms land-mines and impact-bombs so
        that they will explode on impact.
        """
        if not self.node.exists(): return
        factory = self.getFactory()
        if self.bombType == 'landMine':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':30,
                    'inputTextures':(factory.landMineLitTex,
                                     factory.landMineTex)})
            bs.gameTimer(500,self.textureSequence.delete)
            # we now make it explodable.
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,
                                         factory.landMineBlastMaterial))
            self.textureSequence.connectAttr('outputTexture',
                                         self.node, 'colorTexture')
            bs.playSound(factory.activateSound, 0.5, position=self.node.position)
            
        elif self.bombType == 'iceMine':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':30,
                    'inputTextures':(factory.iceMineLitTex,
                                     factory.iceMineTex)})
            bs.gameTimer(500,self.textureSequence.delete)
            # we now make it explodable.
            bs.gameTimer(250,bs.WeakCall(self._addMaterial,
                                         factory.landMineBlastMaterial))
            self.textureSequence.connectAttr('outputTexture',#i moved the textureSequence to here to fix something for a powerup
                                         self.node, 'colorTexture')
            bs.playSound(factory.activateSound, 0.5, position=self.node.position)
            
        elif self.bombType == 'impact':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':100,
                    'inputTextures':(factory.impactLitTex,
                                     factory.impactTex,
                                     factory.impactTex)})
            bs.gameTimer(250, bs.WeakCall(self._addMaterial,
                                          factory.landMineBlastMaterial))
            self.textureSequence.connectAttr('outputTexture',
                                         self.node, 'colorTexture')
            bs.playSound(factory.activateSound, 0.5, position=self.node.position)
            
        elif self.bombType == 'epicMine':
            self.textureSequence = \
                bs.newNode('textureSequence', owner=self.node, attrs={
                    'rate':100,
                    'inputTextures':(factory.epicMineTex,
                                     factory.epicMineTex,
                                     factory.epicMineTex)})
            bs.gameTimer(250, bs.WeakCall(self._addMaterial,
                                          factory.landMineBlastMaterial))
            self.textureSequence.connectAttr('outputTexture',
                                         self.node, 'colorTexture')
            bs.playSound(factory.activateSound, 0.5, position=self.node.position)
            
        elif self.bombType == 'powerup':
            bs.gameTimer(250, bs.WeakCall(self._addMaterial,
                                          factory.landMineBlastMaterial))
        else:
            raise Exception('arm() should only be called '
                            'on land-mines or impact bombs')
                            
        '''self.textureSequence.connectAttr('outputTexture',#done through a new way to help the bombType 'powerup' 
                                         self.node, 'colorTexture')
        bs.playSound(factory.activateSound, 0.5, position=self.node.position)'''

    def _handleDie(self, msg):
        if self.bombType == "antiGrav" and self.node.exists():
            aga = AntiGravArea(position=self.node.position, radius=self.blastRadius)
            bs.gameTimer(7000, aga.delete)
        self.node.delete()

    def handleMessage(self, msg):
        if isinstance(msg, ExplodeMessage):
            self.explode()
        elif isinstance(msg, ImpactMessage):
            self._handleImpact(msg)
        elif isinstance(msg, bs.PickedUpMessage):
            # change our source to whoever just picked us up *only* if its None
            # this way we can get points for killing bots with their own bombs
            # hmm would there be a downside to this?...
            if self.sourcePlayer is not None:
                self.sourcePlayer = msg.node.sourcePlayer
        elif isinstance(msg, SplatMessage):
            self._handleSplat(msg)
        elif isinstance(msg, bs.DroppedMessage):
            self._handleDropped(msg)
        elif isinstance(msg, bs.HitMessage):
            self._handleHit(msg)
        elif isinstance(msg, bs.DieMessage):
            self._handleDie(msg)
        elif isinstance(msg, bs.OutOfBoundsMessage):
            self._handleOOB(msg)
        elif isinstance(msg, ArmMessage):
            self.arm()
        elif isinstance(msg, WarnMessage):
            self._handleWarn(msg)
        else:
            bs.Actor.handleMessage(self, msg)


bsBomb.Bomb = NewBomb
bs.Bomb = NewBomb
bsBomb.Blast = NewBlast
bs.Blast = NewBlast
bsBomb.BombFactory = NewBombFactory
bs.BombFactory = NewBombFactory
