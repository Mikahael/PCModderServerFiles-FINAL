import random
import bsUtils
import bsInternal
import bs
import math


class Floater(bs.Actor):
    def __init__(self, map):

        bs.Actor.__init__(self)

        self.controlled = False
        self.sourcePlayer = None

        self.floaterMaterial = bs.Material()
        self.floaterMaterial.addActions(
            conditions=('theyHaveMaterial',
                        bs.getSharedObject('playerMaterial')),
            actions=(('modifyNodeCollision', 'collide', True),
                     ('modifyPartCollision', 'physical', True)))
        self.floaterMaterial.addActions(
            conditions=(('theyDontHaveMaterial',
                         bs.getSharedObject('playerMaterial')), 'and',
                        ('theyHaveMaterial',
                         bs.getSharedObject('objectMaterial')), 'or',
                        ('theyHaveMaterial',
                         bs.getSharedObject('footingMaterial'))),
            actions=(('modifyPartCollision', 'physical', False), ))

        self.pos = map.getDefBoundBox('levelBounds')
        self.px = "random.uniform(self.pos[0],self.pos[3])"
        self.py = "random.uniform(self.pos[1],self.pos[4])"
        self.pz = "random.uniform(self.pos[2],self.pos[5])"
        # self.node = bs.newNode('prop',attrs={'position':(eval(self.px),eval(self.py),eval(self.pz)),'sticky':False,'body':'landMine','model':bs.getModel('landMine'),'colorTexture':bs.getTexture('logo'),'bodyScale':4.0,'reflection': 'powerup','density':99999999999999999,'reflectionScale': [1.0],'modelScale':4.0,'gravityScale':0,'shadowSize':0.1,'isAreaOfInterest':True,'materials':[bs.getSharedObject('footingMaterial'),self.floaterMaterial]})

        self.node = bs.newNode(
            'prop',
            delegate=self,
            owner=None,
            attrs={
                'position': (eval(self.px), eval(self.py), eval(self.pz)),
                'model':
                bs.getModel('landMine'),
                'lightModel':
                bs.getModel('landMine'),
                'body':
                'landMine',
                'bodyScale':
                4,
                'modelScale':
                4,
                'shadowSize':
                0.25,
                'density':
                9999999999999999999,
                'gravityScale':
                0.0,
                'colorTexture':
                bs.getTexture('logo'),
                'reflection':
                'soft',
                'reflectionScale': [0.25],
                'materials':
                [bs.getSharedObject('footingMaterial'), self.floaterMaterial]
            })
        #self.node.position = map.getDefPoints('flag')[0][:3]
        self.node2 = bs.newNode(
            'prop',
            owner=self.node,
            attrs={
                'position': (0, 0, 0),
                'sticky':
                False,
                'body':
                'sphere',
                'model':
                None,
                'colorTexture':
                bs.getTexture('logo'),
                'bodyScale':
                1.0,
                'reflection':
                'powerup',
                'density':
                99999999999999999,
                'reflectionScale': [1.0],
                'modelScale':
                1.0,
                'gravityScale':
                0,
                'shadowSize':
                0.1,
                'isAreaOfInterest':
                True,
                'materials':
                [bs.getSharedObject('objectMaterial'), self.floaterMaterial]
            })
        self.node.connectAttr('position', self.node2, 'position')
        #self.node.velocity = (0,0.1,0)
        # bs.gameTimer(500,bs.WeakCall(self.move))
        # bs.gameTimer(2000,bs.WeakCall(self.drop),True)
        self.move()

    def checkCanControl(self):
        if not self.node.exists():
            return False
        if not self.sourcePlayer.isAlive():
            self.dis()
            return False
        return True

    def con(self):
        self.controlled = True
        self.checkPlayerDie()

    def up(self):
        if not self.checkCanControl():
            return
        v = self.node.velocity
        self.node.velocity = (v[0], 7, v[2])

    def upR(self):
        if not self.checkCanControl():
            return
        v = self.node.velocity
        self.node.velocity = (v[0], 0, v[2])

    def down(self):
        if not self.checkCanControl():
            return
        v = self.node.velocity
        self.node.velocity = (v[0], -7, v[2])

    def downR(self):
        if not self.checkCanControl():
            return
        v = self.node.velocity
        self.node.velocity = (v[0], 0, v[2])

    def leftright(self, value):
        if not self.checkCanControl():
            return
        v = self.node.velocity
        self.node.velocity = (7 * value, v[1], v[2])

    def updown(self, value):
        if not self.checkCanControl():
            return
        v = self.node.velocity
        self.node.velocity = (v[0], v[1], -7 * value)

    def dis(self):
        if self.node.exists():
            self.controlled = False
            self.node.velocity = (0, 0, 0)
            self.move()

    def checkPlayerDie(self):
        if not self.controlled:
            return
        if self.sourcePlayer is None:
            return
        if self.sourcePlayer.isAlive():
            bs.gameTimer(100, self.checkPlayerDie)
            #posP = self.sourcePlayer.actor.node.position;posO = self.node.position
            # if bs.Vector(posP[0]-posO[0],posP[1]-posO[1],posP[2]-posO[2]).length() > 2.5:
            #p = self.node.position
            # self.sourcePlayer.actor.node.handleMessage(bs.StandMessage((p[0],p[1]-1.5,p[2])))
            #self.sourcePlayer.actor.node.holdNode = self.node2
            return
        else:
            self.dis()

    def distance(self, x1, y1, z1, x2, y2, z2):
        d = math.sqrt(
            math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) +
            math.pow(z2 - z1, 2) * 1.0)

        return d

    def drop(self):
        try:
            np = self.node.position
        except:
            np = (0, 0, 0)
        self.b = bs.Bomb(bombType=random.choice(
            ['normal', 'ice', 'sticky', 'impact', 'landMine', 'tnt']),
                         sourcePlayer=self.sourcePlayer,
                         position=(np[0], np[1] - 1, np[2]),
                         velocity=(0, -1, 0)).autoRetain()
        if self.b.bombType in ['impact', 'landMine']:
            self.b.arm()

    def move(self):
        px = eval(self.px)
        py = eval(self.py)
        pz = eval(self.pz)
        try:
            if self.node.exists():
                pn = self.node.position
                # time = self.distance(pn[0],pn[1],pn[2],px,py,pz)*2000
                dist = self.distance(pn[0], pn[1], pn[2], px, py, pz)
        except:
            time = 1000
            print 'Floater Time Error'
        if self.node.exists():
            # bsUtils.animateArray(self.node,'position',3,{0:self.node.position,time:(px,py,pz)})
            # bs.gameTimer(int(round(time)),bs.WeakCall(self.move))
            self.node.velocity = ((px - pn[0]) / dist, (py - pn[1]) / dist,
                                  (pz - pn[2]) / dist)
            if not self.controlled:
                bs.gameTimer(int(round(dist * 1000)), bs.WeakCall(self.move))

    def handleMessage(self, m):
        super(self.__class__, self).handleMessage(m)
        if isinstance(m, bs.DieMessage):
            self.node.delete()
            self.node2.delete()
        elif isinstance(m, bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())
