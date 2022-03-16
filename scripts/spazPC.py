#thanks to froshlee14 here
#all modding is done by PC||231392 including importation and most of it is my work.
#admin sys work is fully mines
#thanks to God
from bsSpaz import Spaz, SpazFactory, PlayerSpazHurtMessage, PlayerSpazDeathMessage, PlayerSpaz, _PickupMessage, _PunchHitMessage, _CurseExplodeMessage, _BombDiedMessage, RespawnIcon
from bsSpaz import *
import bs
import bsUtils
import random
import weakref
import bsInternal
import fire
import bsSomething
import portalObjects#my final stand
import newObjects

oldSpazInit = Spaz.__init__
def newSpazInit(self, *args, **kwargs):
    oldSpazInit(self, *args, **kwargs)
    #self.bombType = 'impact'#self.bombTypeDefault
    self._hasMagZone = False
    self._teleported = False
    self.iceImpactCount = 0
    self.curseBombCount = 0
    self.cursyBombCount = 0
    self.epicMineCount = 0
    self.iceMineCount = 0
    self.powerupCount = 0
    self.fireBombCount = 0
    self.shockWaveCount = 0
    self.boomBombCount = 0
    self.antiGravCount = 0
    self.headacheCount = 0
    self.portalBombCount = 0
    self._tint = bs.getSharedObject('globals').tint
    self._name = self.node.name
    self._head = self.node.headModel
    self._torso = self.node.torsoModel
    self._pelvis = self.node.pelvisModel
    self._upperArm = self.node.upperArmModel
    self._foreArm = self.node.foreArmModel
    self._hand = self.node.handModel
    self._upperLeg = self.node.upperLegModel
    self._lowerLeg = self.node.lowerLegModel
    self._toes = self.node.toesModel
    #for default gameplay
    if fire.defaultBoxingGloves: self.equipBoxingGloves()
    if fire.defaultShields: self.equipShields()
    #for default char
    if fire.rchar: self.node.handleMessage(bs.PowerupMessage(powerupType = 'rchar'))
    if fire.frosty: self.node.handleMessage(bs.PowerupMessage(powerupType = 'frosty'))
    if fire.wizard: self.node.handleMessage(bs.PowerupMessage(powerupType = 'wizard'))
    if fire.ali: self.node.handleMessage(bs.PowerupMessage(powerupType = 'ali'))
    if fire.santa: self.node.handleMessage(bs.PowerupMessage(powerupType = 'santa'))
    if fire.robot: self.node.handleMessage(bs.PowerupMessage(powerupType = 'robot'))
    if fire.pengu: self.node.handleMessage(bs.PowerupMessage(powerupType = 'pengu'))
    if fire.pixie: self.node.handleMessage(bs.PowerupMessage(powerupType = 'pixie'))
    if fire.ninja: self.node.handleMessage(bs.PowerupMessage(powerupType = 'ninja'))
    #for default bombs
    if fire.impact_bomb: self.bombType = 'impact'
    if fire.sticky_bomb: self.bombType = 'sticky'
    if fire.ice_bomb: self.bombType = 'ice'
    if fire.spike_bomb: self.bombType = 'spikeBomb'
    if fire.shock_wave: self.bombType = 'shockWave'
    if fire.knock_bomb: self.bombType = 'knockBomb'
    if fire.spaz_bomb: self.bombType = 'spazBomb'
    if fire.glue_bomb: self.bombType = 'gluebomb'
    
    prefix = random.choice([u'\ue048THE BOSS\ue048',u'\ue00cNOOBY\ue00c',u'\ue00cTERMINATOR\ue00c',u'\ue043KillMePls\ue043',u'\ue043GrandMaster\ue043',u'\ue048LEGENDARY\ue048'])

    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.8, 0), 'operation': 'add'})
    self.node.connectAttr('position', m, 'input2')
    self._hpText = bs.newNode('text', owner=self.node,
                               attrs={'text':'', 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
    m.connectAttr('output', self._hpText, 'position')
    bs.animate(self._hpText, 'scale', {0: 0.0, 100: 0.008})
    if fire.hp: self._hpText.text = 'HP: ' + str(int(self.hitPoints))
    else: self._hpText.text = ''
    
    m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 1.35, 0), 'operation': 'add'})
    self.node.connectAttr('position', m, 'input2')
    self._pcText = bs.newNode('text', owner=self.node,
                               attrs={'text':'', 'inWorld':True,
                                      'shadow':1.0,'flatness':1.0,
                                      'color':(1,1,1),'scale':0.0,
                                      'hAlign':'center'})
    m.connectAttr('output', self._pcText, 'position')
    bs.animate(self._pcText, 'scale', {0: 0.0, 100: 0.008})
    if fire.tag: self._pcText.text = prefix
    else: self._pcText.text = ''
    
    #bsGlobals = bs.getSharedObject('globals')
    #if fire.night:
    #    bsGlobals.tint = (0.5,0.7,1)
    #else:
    #    bsGlobals.tint = (1.2,1.17,1.1)
    # need to do another way because of special map tex.
    
Spaz.__init__ = newSpazInit

def onJumpfly(self):
        """
        Called to 'press jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        t = bs.getGameTime()
        if t - self.lastJumpTime >= self._jumpCooldown:
            self.node.handleMessage("impulse",self.node.position[0],self.node.position[1]-2,self.node.position[2],self.node.velocity[0]*0,20 +0.01*(t - self.lastJumpTime),self.node.velocity[2]*0,10,5,0,0,self.node.velocity[0]*-0.1,20 + 0.01*(t - self.lastJumpTime),self.node.velocity[2]*0)
            self.node.handleMessage("impulse",self.node.position[0],self.node.position[1],self.node.position[2],self.node.velocity[0]*0,20 +0.01*(t - self.lastJumpTime),self.node.velocity[2]*0,10,5,0,0,self.node.velocity[0]*-0.1,20 + 0.01*(t - self.lastJumpTime),self.node.velocity[2]*0)
            self.node.jumpPressed = True
            self.lastJumpTime = t
        self._turboFilterAddPress('jump')

def pconPunchPress(self):
        """
        Called to 'press punch' on this spaz;
        used for player or AI connections.
        """
        if (not self.node.exists()
            or self.frozen
            or self.node.knockout > 0.0): return
        t = bs.getGameTime()
        if t - self.lastPunchTime >= self._punchCooldown:
            if self.punchCallback is not None:
                self.punchCallback(self)
            self._punchedNodes = set() # reset this..
            self.lastPunchTime = t
            if fire.colory:
                self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
                self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))   
            self.node.punchPressed = True
            if not self.node.holdNode.exists():
                bs.gameTimer(100, bs.WeakCall(self._safePlaySound,
                                              self.getFactory().swishSound,
                                              0.8))
        self._turboFilterAddPress('punch')
        
def pconPickUpPress(self):
        """
        Called to 'press pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        t = bs.getGameTime()
        if t - self.lastPickupTime >= self._pickupCooldown:
            if fire.randomChar:
                testingEvent = 0
                        
                event = random.randint(1,11) if testingEvent == 0 else testingEvent                
                    
                if event in [1]:
                    self.node.colorTexture = bs.getTexture('frostyColor')
                    self.node.colorMaskTexture = bs.getTexture('frostyColorMask')
                    self.node.headModel = bs.getModel('frostyHead')
                    self.node.upperArmModel = bs.getModel('kronkUpperArm')
                    self.node.torsoModel = bs.getModel('frostyTorso')
                    self.node.pelvisModel = bs.getModel('frostyPelvis')
                    self.node.foreArmModel = bs.getModel('frostyForeArm')
                    self.node.handModel = bs.getModel('frostyHand')
                    self.node.upperLegModel = bs.getModel('frostyUpperLeg')
                    self.node.lowerLegModel = bs.getModel('frostyLowerLeg')
                    self.node.toesModel = bs.getModel('frostyToes')
                    self.node.style = 'frosty'       
                    
                elif event == 2:  
                    self.node.colorTexture = bs.getTexture('santaColor')
                    self.node.colorMaskTexture = bs.getTexture('santaColorMask')      
                    self.node.headModel = bs.getModel('santaHead')
                    self.node.upperArmModel = bs.getModel('santaUpperArm')
                    self.node.torsoModel = bs.getModel('santaTorso')
                    self.node.pelvisModel = bs.getModel('kronkPelvis')
                    self.node.foreArmModel = bs.getModel('santaForeArm')
                    self.node.handModel = bs.getModel('santaHand')
                    self.node.upperLegModel = bs.getModel('santaUpperLeg')
                    self.node.lowerLegModel = bs.getModel('santaLowerLeg')
                    self.node.toesModel = bs.getModel('santaToes')
                    self.node.style = 'santa'

                elif event == 3:     
                    self.node.colorTexture = bs.getTexture('bonesColor')
                    self.node.colorMaskTexture = bs.getTexture('bonesColorMask')                
                    self.node.headModel = bs.getModel('bonesHead')
                    self.node.upperArmModel = bs.getModel('bonesUpperArm')
                    self.node.torsoModel = bs.getModel('bonesTorso')
                    self.node.pelvisModel = bs.getModel('bonesPelvis')
                    self.node.foreArmModel = bs.getModel('bonesForeArm')
                    self.node.handModel = bs.getModel('bonesHand')
                    self.node.upperLegModel = bs.getModel('bonesUpperLeg')
                    self.node.lowerLegModel = bs.getModel('bonesLowerLeg')
                    self.node.toesModel = bs.getModel('bonesToes')
                    self.node.style = 'bones'
                    
                elif event == 4:      
                    self.node.colorTexture = bs.getTexture('melColor')
                    self.node.colorMaskTexture = bs.getTexture('melColorMask')                
                    self.node.headModel = bs.getModel('melHead')
                    self.node.upperArmModel = bs.getModel('melUpperArm')
                    self.node.torsoModel = bs.getModel('melTorso')
                    self.node.pelvisModel = bs.getModel('kronkPelvis')
                    self.node.foreArmModel = bs.getModel('melForeArm')
                    self.node.handModel = bs.getModel('melHand')
                    self.node.upperLegModel = bs.getModel('melUpperLeg')
                    self.node.lowerLegModel = bs.getModel('melLowerLeg')
                    self.node.toesModel = bs.getModel('melToes')
                    self.node.style = 'mel'
                    
                elif event == 5:    
                    self.node.colorTexture = bs.getTexture('ninjaColor')
                    self.node.colorMaskTexture = bs.getTexture('ninjaColorMask')                
                    self.node.headModel = bs.getModel('ninjaHead')
                    self.node.upperArmModel = bs.getModel('ninjaUpperArm')
                    self.node.torsoModel = bs.getModel('ninjaTorso')
                    self.node.pelvisModel = bs.getModel('ninjaPelvis')
                    self.node.foreArmModel = bs.getModel('ninjaForeArm')
                    self.node.handModel = bs.getModel('ninjaHand')
                    self.node.upperLegModel = bs.getModel('ninjaUpperLeg')
                    self.node.lowerLegModel = bs.getModel('ninjaLowerLeg')
                    self.node.toesModel = bs.getModel('ninjaToes')
                    self.node.style = 'ninja'

                elif event == 6:           
                    self.node.colorTexture = bs.getTexture('aliColor')
                    self.node.colorMaskTexture = bs.getTexture('aliColorMask')                
                    self.node.headModel = bs.getModel('aliHead')
                    self.node.upperArmModel = bs.getModel('aliUpperArm')
                    self.node.torsoModel = bs.getModel('aliTorso')
                    self.node.pelvisModel = bs.getModel('aliPelvis')
                    self.node.foreArmModel = bs.getModel('aliForeArm')
                    self.node.handModel = bs.getModel('aliHand')
                    self.node.upperLegModel = bs.getModel('aliUpperLeg')
                    self.node.lowerLegModel = bs.getModel('aliLowerLeg')
                    self.node.toesModel = bs.getModel('aliToes')
                    self.node.style = 'ali'

                elif event == 7:           
                    self.node.colorTexture = bs.getTexture('bearColor')
                    self.node.colorMaskTexture = bs.getTexture('bearColorMask')                
                    self.node.headModel = bs.getModel('bearHead')
                    self.node.upperArmModel = bs.getModel('bearUpperArm')
                    self.node.torsoModel = bs.getModel('bearTorso')
                    self.node.pelvisModel = bs.getModel('bearPelvis')
                    self.node.foreArmModel = bs.getModel('bearForeArm')
                    self.node.handModel = bs.getModel('bearHand')
                    self.node.upperLegModel = bs.getModel('bearUpperLeg')
                    self.node.lowerLegModel = bs.getModel('bearLowerLeg')
                    self.node.toesModel = bs.getModel('bearToes')
                    self.node.style = 'bear'
                    
                elif event == 8:           
                    self.node.colorTexture = bs.getTexture('penguinColor')
                    self.node.colorMaskTexture = bs.getTexture('penguinColorMask')                
                    self.node.headModel = bs.getModel('penguinHead')
                    self.node.upperArmModel = bs.getModel('penguinUpperArm')
                    self.node.torsoModel = bs.getModel('penguinTorso')
                    self.node.pelvisModel = bs.getModel('penguinPelvis')
                    self.node.foreArmModel = bs.getModel('penguinForeArm')
                    self.node.handModel = bs.getModel('penguinHand')
                    self.node.upperLegModel = bs.getModel('penguinUpperLeg')
                    self.node.lowerLegModel = bs.getModel('penguinLowerLeg')
                    self.node.toesModel = bs.getModel('penguinToes')
                    self.node.style = 'penguin'
                    
                elif event == 9:           
                    self.node.colorTexture = bs.getTexture('wizardColor')
                    self.node.colorMaskTexture = bs.getTexture('wizardColorMask')                
                    self.node.headModel = bs.getModel('wizardHead')
                    self.node.upperArmModel = bs.getModel('wizardUpperArm')
                    self.node.torsoModel = bs.getModel('wizardTorso')
                    self.node.pelvisModel = bs.getModel('wizardPelvis')
                    self.node.foreArmModel = bs.getModel('wizardForeArm')
                    self.node.handModel = bs.getModel('wizardHand')
                    self.node.upperLegModel = bs.getModel('wizardUpperLeg')
                    self.node.lowerLegModel = bs.getModel('wizardLowerLeg')
                    self.node.toesModel = bs.getModel('wizardToes')
                    self.node.style = 'spaz'

                elif event == 10:           
                    self.node.colorTexture = bs.getTexture('pixieColor')
                    self.node.colorMaskTexture = bs.getTexture('pixieColorMask')                
                    self.node.headModel = bs.getModel('pixieHead')
                    self.node.upperArmModel = bs.getModel('pixieUpperArm')
                    self.node.torsoModel = bs.getModel('pixieTorso')
                    self.node.pelvisModel = bs.getModel('pixiePelvis')
                    self.node.foreArmModel = bs.getModel('pixieForeArm')
                    self.node.handModel = bs.getModel('pixieHand')
                    self.node.upperLegModel = bs.getModel('pixieUpperLeg')
                    self.node.lowerLegModel = bs.getModel('pixieLowerLeg')
                    self.node.toesModel = bs.getModel('pixieToes')
                    self.node.style = 'pixie'
                    
                elif event == 11:           
                    self.node.colorTexture = bs.getTexture('cyborgColor')
                    self.node.colorMaskTexture = bs.getTexture('cyborgColorMask')                
                    self.node.headModel = bs.getModel('cyborgHead')
                    self.node.upperArmModel = bs.getModel('cyborgUpperArm')
                    self.node.torsoModel = bs.getModel('cyborgTorso')
                    self.node.pelvisModel = bs.getModel('cyborgPelvis')
                    self.node.foreArmModel = bs.getModel('cyborgForeArm')
                    self.node.handModel = bs.getModel('cyborgHand')
                    self.node.upperLegModel = bs.getModel('cyborgUpperLeg')
                    self.node.lowerLegModel = bs.getModel('cyborgLowerLeg')
                    self.node.toesModel = bs.getModel('cyborgToes')
                    self.node.style = 'cyborg'
            self.node.pickUpPressed = True
            self.lastPickupTime = t
        self._turboFilterAddPress('pickup')

def pchandleMessage(self, msg):
        self._handleMessageSanityCheck()

        if isinstance(msg, bs.PickedUpMessage):
            self.node.handleMessage("hurtSound")
            self.node.handleMessage("pickedUp")
            # this counts as a hit
            self._numTimesHit += 1

        elif isinstance(msg, bs.ShouldShatterMessage):
            # eww; seems we have to do this in a timer or it wont work right
            # (since we're getting called from within update() perhaps?..)
            bs.gameTimer(1, bs.WeakCall(self.shatter))

        elif isinstance(msg, bs.ImpactDamageMessage):
            # eww; seems we have to do this in a timer or it wont work right
            # (since we're getting called from within update() perhaps?..)
            bs.gameTimer(1, bs.WeakCall(self._hitSelf, msg.intensity))

        elif isinstance(msg, bs.PowerupMessage):
            if self._dead: return True
            if self.pickUpPowerupCallback is not None:
                self.pickUpPowerupCallback(self)

            if fire.nameP: bsUtils.PopupText(msg.powerupType.upper() + "!",
                             color=(1, 1, 1),
                             scale=1.2,
                             position=self.node.position).autoRetain()#thanks to logic
                
            if fire.lightning: # #light node done by me concept by esie-eyen and patronmodz
                self.light = bs.newNode('light',
                attrs={'position':self.node.position,
                       'color':(1.2,1.2,1.4),
                       'volumeIntensityScale': 2.35})
                bs.animate(self.light,'intensity',{0:0,70:0.5,350:0},loop=False)
                bs.gameTimer(500,self.light.delete)

            if (msg.powerupType == 'tripleBombs'):
                tex = bs.Powerup.getFactory().texBomb
                self._flashBillboard(tex)
                self.setBombCount(3)
                if self.powerupsExpire:
                    self.node.miniBillboard1Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard1StartTime = t
                    self.node.miniBillboard1EndTime = t+gPowerupWearOffTime
                    self._multiBombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._multiBombWearOffFlash))
                    self._multiBombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._multiBombWearOff))
            elif (msg.powerupType == 'triple'):
                self.setBombCount(3)
            elif (msg.powerupType == 'multiBomb'):
                tex = bs.Powerup.getFactory().texBomb
                self._flashBillboard(tex)
                bsUtils.PopupText("HardCore",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                self.setBombCount(999)
                if self.powerupsExpire:
                    self.node.miniBillboard1Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard1StartTime = t
                    self.node.miniBillboard1EndTime = t+gPowerupWearOffTime
                    self._multiBombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._multiBombWearOffFlash))
                    self._multiBombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._multiBombWearOff))
            elif msg.powerupType == 'landMines':
                self.setLandMineCount(min(self.landMineCount+3, 3))
            elif msg.powerupType == 'epicMine':
                self.setepicMineCount(min(self.epicMineCount+3, 3))
            elif msg.powerupType == 'iceMine':
                self.seticeMineCount(min(self.iceMineCount+3, 3))
            elif msg.powerupType == 'powerup':
                self.setpowerupCount(min(self.powerupCount+3, 3))
            elif msg.powerupType == 'cursyBomb':
                self.setcursyBombCount(min(self.cursyBombCount+1, 1))
            elif msg.powerupType == 'fireBomb':
                self.setfireBombCount(min(self.fireBombCount+5, 5))
            elif msg.powerupType == 'shockWave':
                self.setshockWaveCount(min(self.shockWaveCount+5, 5))
            elif msg.powerupType == 'antiGrav':
                self.setAntiGravCount(min(self.antiGravCount + 3, 3))
                bsUtils.PopupText("TheGreat",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
            elif msg.powerupType == 'headache':
                self.setHeadacheCount(self.headacheCount + 3)
                bsUtils.PopupText("TheGreat",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                
            elif msg.powerupType == 'light':
                self.light = bs.newNode('light',
                attrs={'position':self.node.position,
                       'color':(0,1,6),#(1.2,1.2,1.4),
                       'radius':0.5,
                       'volumeIntensityScale': 2.35})
                bs.animate(self.light,'intensity',{0:0,70:0.5,350:0},loop=False)
                bs.animate(self.light,'radius',{0:3.0,300:5,600:0}) 
                bs.gameTimer(500,self.light.delete)
                bs.emitBGDynamics(position=self.node.position,velocity=(0,0,0),count=600,spread=0.7,chunkType='ice');
                bs.screenMessage(u'\ue048EPIX MODE\ue048')                
                
            elif msg.powerupType == 'slip':
                self.node.handleMessage("impulse", self.node.position[0], self.node.position[1],
                               self.node.position[2], self.node.velocity[0], 3,
                               self.node.velocity[2], 45, 45, 0, 0,
                               self.node.velocity[0], 3, self.node.velocity[2])
            elif msg.powerupType == 'blast':
            	radius = random.choice([0.5,1.0,1.5,2.0])
            	type = random.choice(['ice','normal','sticky','tnt'])           
            	pos = self.node.position
            	bs.Blast(position=pos,blastRadius=radius,blastType=type).autoRetain()
                bsUtils.PopupText("Esie-Eyen",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                self._blast = True                
                if self._blast == True:
                    if type == 'ice': bs.screenMessage("Type: Ice",color=(1,1,1))
                    elif type == 'normal': bs.screenMessage("Type: Normal",color=(1,1,1))
                    elif type == 'sticky': bs.screenMessage("Type: Sticky",color=(1,1,1))
                    elif type == 'tnt': bs.screenMessage("Type: Tnt",color=(1,1,1))
                    if radius == 0.5: bs.screenMessage("Radius: 0.5",color=(1,1,1))
                    elif radius == 1.0: bs.screenMessage("Radius: 1.0",color=(1,1,1))
                    elif radius == 1.5: bs.screenMessage("Radius: 1.5",color=(1,1,1))
                    elif radius == 2.0: bs.screenMessage("Radius: 2.0",color=(1,1,1))
            elif msg.powerupType == 'mix':
            	pow = random.choice(['tripleBombs','iceBombs','punch','impactBombs','landMines','stickyBombs','shield','health','curse'])
                pos = self.node.position
                bs.Powerup(position=pos,powerupType=pow).autoRetain()
                bs.emitBGDynamics(position=self.node.position,velocity=self.node.velocity,count=int(14.0+random.random()*70),scale=1.4,spread=3.5,chunkType='spark');
                bsUtils.PopupText("Esie-Eyen",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                self._mix = True                
                if self._mix == True:
                    if pow == 'tripleBombs': bs.screenMessage("Triple Bombs",color=(1,1,1))
                    elif pow == 'iceBombs': bs.screenMessage("Ice Bombs",color=(1,1,1))
                    elif pow == 'punch': bs.screenMessage("Boxing Gloves",color=(1,1,1))
                    elif pow == 'impactBombs': bs.screenMessage("Impact Bombs",color=(1,1,1))
                    elif pow == 'landMines': bs.screenMessage("Land Mines",color=(1,1,1))
                    elif pow == 'stickyBombs': bs.screenMessage("Sticky Bombs",color=(1,1,1))
                    elif pow == 'shield': bs.screenMessage("Energy Shield",color=(1,1,1))
                    elif pow == 'health': bs.screenMessage("Health Kit",color=(1,1,1))
                    elif pow == 'curse': bs.screenMessage("Curse",color=(1,1,1))
                    self._light = True           
                if self._light == True:
                    color = random.choice([(5.0,0.2,0.2),(0.2,5.0,0.2),(0.2,0.2,5.0)])
                    self.light = bs.newNode('light',
                    attrs={'position':self.node.position,
                               'color':(1.2,1.2,1.4),
                               'volumeIntensityScale': 0.35})
                    bs.animate(self.light,'intensity',{0:0,70:0.5,350:0},loop=False)
                    bs.gameTimer(500,self.light.delete)  
            elif msg.powerupType == 'frozenBomb':
                self.bombType = 'frozenBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if fire.lightning:
                    self.light = bs.newNode('light',
                    attrs={'position':self.node.position,
                           'color':(1.2,1.2,1.4),
                           'volumeIntensityScale': 2.35})
                    bs.animate(self.light,'intensity',{0:0,70:0.5,350:0},loop=False)
                    bs.gameTimer(500,self.light.delete)  
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer( gPowerupWearOffTime-2000,
                                  bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))

            elif msg.powerupType == 'impactBombs':
                self.bombType = 'impact'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if fire.lightning:
                    self.light = bs.newNode('light',
                    attrs={'position':self.node.position,
                           'color':(1.2,1.2,1.4),
                           'volumeIntensityScale': 2.35})
                    bs.animate(self.light,'intensity',{0:0,70:0.5,350:0},loop=False)
                    bs.gameTimer(500,self.light.delete)  
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer( gPowerupWearOffTime-2000,
                                  bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif msg.powerupType == 'portalBomb':
                self.setportalBombCount(min(self.portalBombCount+1, 1))
            elif msg.powerupType == 'curseBomb':
                self.setcurseBombCount(min(self.curseBombCount+3, 3))
                
            elif msg.powerupType == 'iceImpact':
                self.seticeImpactCount(min(self.iceImpactCount+3, 3))
                bsUtils.PopupText("Dimitry",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
            elif msg.powerupType == 'radius':
                self.blastRadius = 5.5
                bsUtils.PopupText("ShayPlays",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
            elif msg.powerupType == 'spunch':
                self._punchPowerScale = 1.3
                self._punchCooldown = 130
                self._hasBoxingGloves = False
                self.node.boxingGloves = 0
                bsUtils.PopupText("SobyDamn",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                tex = bs.Powerup.getFactory().texSpunch
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.boxingGlovesFlashing = 0
                    self.node.miniBillboard3Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard3StartTime = t
                    self.node.miniBillboard3EndTime = t+gPowerupWearOffTime
                    self._boxingGlovesWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._glovesWearOffFlash))
                    self._boxingGlovesWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._glovesWearOff)) 
            elif msg.powerupType =='cursy':                   
                def _speed():
                    self.node.handleMessage(bs.PowerupMessage(powerupType = random.choice(['curse','health'])))
                bs.gameTimer(350,bs.Call(_speed),repeat=True)     
                
            elif msg.powerupType =='shatter': 
                def shatter():            
                    self.node.handleMessage(bs.DieMessage())
                bs.gameTimer(500,bs.Call(shatter))                 
                
            elif msg.powerupType =='jumpy':                   
                def _speed():
                    self.node.jumpPressed = True
                    self.node.jumpPressed = False
                    self.node.punchPressed = True
                    self.node.punchPressed = False
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
                bs.gameTimer(350,bs.Call(_speed),repeat=True)     
            elif msg.powerupType == 'crazy':
                def _speed():
                    self.node.frozen = random.choice([True,False])
                    #if self.node.frozen == True: bsUtils.PopupText("Weee",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                bs.gameTimer(350,bs.Call(_speed),repeat=True)     
            elif msg.powerupType == 'mag':
                if self._hasMagZone: return
                tex = bs.Powerup.getFactory().texMag
                self._flashBillboard(tex)
                newObjects.MagneticZone(owner = self.node)
                self._hasMagZone = True
                bsUtils.PopupText("Froshlee14",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard3Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard3StartTime = t
                    self.node.miniBillboard3EndTime = t+gPowerupWearOffTime
                    self._magWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-2000,bs.Call(_magWearOffFlash,self))                                 
            elif msg.powerupType == 'impactShower':#thanks to logic and bombdash

                class zone(object):
                    def __init__(self, player):
                        self.pos = player.actor.node.position
                        self.zone = bs.newNode('light',
                                               owner=player.actor.node,
                                               attrs={
                                                   'position': self.pos,
                                                   'color': (0.5, 0.5, 1),
                                                   'intensity': 10,
                                                   'heightAttenuated': True
                                               })
                        bsUtils.animate(self.zone, 'radius', {0: 0, 300: 0.05})
                        bsUtils.animate(self.zone, 'radius', {1700: 0.05, 2000: 0})
                        bs.gameTimer(2000, self.zone.delete)

            # def strike():
            #     activity = bsInternal._getForegroundHostActivity()
            #     for player in activity.players:
            #         if player.actor is not None and player.actor.isAlive() and player.getTeam() != self.sourcePlayer.getTeam():
            #             blast = Blast(position=player.actor.node.position,velocity=player.actor.node.velocity,
            #                                             blastRadius=3,blastType='landmine',sourcePlayer=self.sourcePlayer).autoRetain()
            #             player.actor.node.shattered = 3
            #     bs.shakeCamera(5)
                import portalObjects
                activity = bsInternal._getForegroundHostActivity()
                for player in activity.players:
                    if player.actor is not None and player.actor.isAlive(
                    ) and player.getTeam() != self.sourcePlayer.getTeam():
                        zone(player)
                        portalObjects.Artillery(target=player.actor.node,
                                                sourcePlayer=self.sourcePlayer)

                bs.screenMessage('%s called in a drone strike!' %
                                 self.sourcePlayer.getName(),
                                 color=(1, 1, 1))
                bsUtils.PopupText("BombDash/Logic",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
            # bs.gameTimer(500,strike)
            
            elif msg.powerupType == 'tnt':
                p = self.node.positionForward
                bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0), sourcePlayer = self.sourcePlayer,bombType = 'tnt').autoRetain()
                bs.Bomb((p[0]-0.43,p[1]+2,p[2]-0.25),velocity=(0,-6,0), sourcePlayer = self.sourcePlayer,bombType = 'tnt').autoRetain()
                bs.Bomb((p[0],p[1]+4,p[2]+0.5),velocity=(0,-6,0), sourcePlayer = self.sourcePlayer,bombType = 'tnt').autoRetain()
                
            elif msg.powerupType == 'pirateBot':
                self._bots = bs.BotSet()
                bs.gameTimer(1000,bs.Call(self._bots.spawnBot,bs.PirateBot,pos=self.node.position,spawnTime=3000))
                bs.gameTimer(1000,bs.Call(self._bots.spawnBot,bs.PirateBot,pos=self.node.position,spawnTime=5000))
                bs.gameTimer(1000,bs.Call(self._bots.spawnBot,bs.PirateBot,pos=self.node.position,spawnTime=7000))
                bs.screenMessage('RUN!!')
            
            elif msg.powerupType == 'jumpFly':
            	player = self.getPlayer()
            	player.assignInputCall('jumpPress', self.onJumpfly)
                tex = bs.Powerup.getFactory().texJumpFly
                if self.powerupsExpire:
                    self.node.miniBillboard3Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard3StartTime = t
                    self.node.miniBillboard3EndTime = t+gPowerupWearOffTime
                    self._jumpFlyWearOffFlashTimer = bs.Timer(gPowerupWearOffTime-1000,bs.WeakCall(self._jumpFlyWearOffFlash))
                    self._jumpFlyWearOffTimer = bs.Timer(gPowerupWearOffTime,bs.WeakCall(self._jumpFlyWearOff))    
            elif msg.powerupType == 'night':
                tex = bs.Powerup.getFactory().texNight
                self._flashBillboard(tex)
                tint = (0.2,0.3,0.4)
                bsUtils.animateArray(bs.getSharedObject('globals'),'tint',3,{0:bs.getSharedObject('globals').tint,2000:tint})
                bsUtils.PopupText("ShayPlays",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain() 
                def night():
                    tint = (0.5,0.7,1)
                    bsUtils.animateArray(bs.getSharedObject('globals'),'tint',3,{0:bs.getSharedObject('globals').tint,2000:tint})
                    bs.screenMessage('Morning!')
                bs.gameTimer(20000,bs.Call(night),repeat=False)
                   
            elif msg.powerupType == 'frosty':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent                
                    
                if event in [1]:
                    self.node.colorTexture = bs.getTexture('frostyColor')
                    self.node.colorMaskTexture = bs.getTexture('frostyColorMask')
                    self.node.headModel = bs.getModel('frostyHead')
                    self.node.upperArmModel = bs.getModel('kronkUpperArm')
                    self.node.torsoModel = bs.getModel('frostyTorso')
                    self.node.pelvisModel = bs.getModel('frostyPelvis')
                    self.node.foreArmModel = bs.getModel('frostyForeArm')
                    self.node.handModel = bs.getModel('frostyHand')
                    self.node.upperLegModel = bs.getModel('frostyUpperLeg')
                    self.node.lowerLegModel = bs.getModel('frostyLowerLeg')
                    self.node.toesModel = bs.getModel('frostyToes')
                    self.node.style = 'frosty'    
                    #bsUtils.PopupText("FrostY",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()    

            elif msg.powerupType == 'santa':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent                
                    
                if event in [1]:
                    self.node.colorTexture = bs.getTexture('santaColor')
                    self.node.colorMaskTexture = bs.getTexture('santaColorMask')      
                    self.node.headModel = bs.getModel('santaHead')
                    self.node.upperArmModel = bs.getModel('santaUpperArm')
                    self.node.torsoModel = bs.getModel('santaTorso')
                    self.node.pelvisModel = bs.getModel('kronkPelvis')
                    self.node.foreArmModel = bs.getModel('santaForeArm')
                    self.node.handModel = bs.getModel('santaHand')
                    self.node.upperLegModel = bs.getModel('santaUpperLeg')
                    self.node.lowerLegModel = bs.getModel('santaLowerLeg')
                    self.node.toesModel = bs.getModel('santaToes')
                    self.node.style = 'santa'    

            elif msg.powerupType == 'ninja':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent   
                
                if event in [1]:  
                    self.node.colorTexture = bs.getTexture('ninjaColor')
                    self.node.colorMaskTexture = bs.getTexture('ninjaColorMask')                
                    self.node.headModel = bs.getModel('ninjaHead')
                    self.node.upperArmModel = bs.getModel('ninjaUpperArm')
                    self.node.torsoModel = bs.getModel('ninjaTorso')
                    self.node.pelvisModel = bs.getModel('ninjaPelvis')
                    self.node.foreArmModel = bs.getModel('ninjaForeArm')
                    self.node.handModel = bs.getModel('ninjaHand')
                    self.node.upperLegModel = bs.getModel('ninjaUpperLeg')
                    self.node.lowerLegModel = bs.getModel('ninjaLowerLeg')
                    self.node.toesModel = bs.getModel('ninjaToes')
                    self.node.style = 'ninja'   

            elif msg.powerupType == 'ali':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent   
                
                if event in [1]:  
                    self.node.colorTexture = bs.getTexture('aliColor')
                    self.node.colorMaskTexture = bs.getTexture('aliColorMask')                
                    self.node.headModel = bs.getModel('aliHead')
                    self.node.upperArmModel = bs.getModel('aliUpperArm')
                    self.node.torsoModel = bs.getModel('aliTorso')
                    self.node.pelvisModel = bs.getModel('aliPelvis')
                    self.node.foreArmModel = bs.getModel('aliForeArm')
                    self.node.handModel = bs.getModel('aliHand')
                    self.node.upperLegModel = bs.getModel('aliUpperLeg')
                    self.node.lowerLegModel = bs.getModel('aliLowerLeg')
                    self.node.toesModel = bs.getModel('aliToes')
                    self.node.style = 'ali'     

            elif msg.powerupType == 'wizard':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent   
                
                if event in [1]:  
                    self.node.colorTexture = bs.getTexture('wizardColor')
                    self.node.colorMaskTexture = bs.getTexture('wizardColorMask')                
                    self.node.headModel = bs.getModel('wizardHead')
                    self.node.upperArmModel = bs.getModel('wizardUpperArm')
                    self.node.torsoModel = bs.getModel('wizardTorso')
                    self.node.pelvisModel = bs.getModel('wizardPelvis')
                    self.node.foreArmModel = bs.getModel('wizardForeArm')
                    self.node.handModel = bs.getModel('wizardHand')
                    self.node.upperLegModel = bs.getModel('wizardUpperLeg')
                    self.node.lowerLegModel = bs.getModel('wizardLowerLeg')
                    self.node.toesModel = bs.getModel('wizardToes')
                    self.node.style = 'spaz' 
                    
            elif msg.powerupType == 'pixie':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent   
                
                if event in [1]:  
                    self.node.colorTexture = bs.getTexture('pixieColor')
                    self.node.colorMaskTexture = bs.getTexture('pixieColorMask')                
                    self.node.headModel = bs.getModel('pixieHead')
                    self.node.upperArmModel = bs.getModel('pixieUpperArm')
                    self.node.torsoModel = bs.getModel('pixieTorso')
                    self.node.pelvisModel = bs.getModel('pixiePelvis')
                    self.node.foreArmModel = bs.getModel('pixieForeArm')
                    self.node.handModel = bs.getModel('pixieHand')
                    self.node.upperLegModel = bs.getModel('pixieUpperLeg')
                    self.node.lowerLegModel = bs.getModel('pixieLowerLeg')
                    self.node.toesModel = bs.getModel('pixieToes')
                    self.node.style = 'pixie' 

            elif msg.powerupType == 'robot':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent   
                
                if event in [1]:                      
                    self.node.colorTexture = bs.getTexture('cyborgColor')
                    self.node.colorMaskTexture = bs.getTexture('cyborgColorMask')                
                    self.node.headModel = bs.getModel('cyborgHead')
                    self.node.upperArmModel = bs.getModel('cyborgUpperArm')
                    self.node.torsoModel = bs.getModel('cyborgTorso')
                    self.node.pelvisModel = bs.getModel('cyborgPelvis')
                    self.node.foreArmModel = bs.getModel('cyborgForeArm')
                    self.node.handModel = bs.getModel('cyborgHand')
                    self.node.upperLegModel = bs.getModel('cyborgUpperLeg')
                    self.node.lowerLegModel = bs.getModel('cyborgLowerLeg')
                    self.node.toesModel = bs.getModel('cyborgToes')
                    self.node.style = 'cyborg'
                    
            elif msg.powerupType == 'pengu':
   
                testingEvent = 0
                        
                event = random.randint(1,1) if testingEvent == 0 else testingEvent  
                
                if event in [1]:                 
                    self.node.colorTexture = bs.getTexture('penguinColor')
                    self.node.colorMaskTexture = bs.getTexture('penguinColorMask')                
                    self.node.headModel = bs.getModel('penguinHead')
                    self.node.upperArmModel = bs.getModel('penguinUpperArm')
                    self.node.torsoModel = bs.getModel('penguinTorso')
                    self.node.pelvisModel = bs.getModel('penguinPelvis')
                    self.node.foreArmModel = bs.getModel('penguinForeArm')
                    self.node.handModel = bs.getModel('penguinHand')
                    self.node.upperLegModel = bs.getModel('penguinUpperLeg')
                    self.node.lowerLegModel = bs.getModel('penguinLowerLeg')
                    self.node.toesModel = bs.getModel('penguinToes')
                    self.node.style = 'penguin'
                    
            elif msg.powerupType == 'rchar':
   
                testingEvent = 0
                        
                event = random.randint(1,11) if testingEvent == 0 else testingEvent                    
                    
                if event in [1]:
                    self.node.colorTexture = bs.getTexture('frostyColor')
                    self.node.colorMaskTexture = bs.getTexture('frostyColorMask')
                    self.node.headModel = bs.getModel('frostyHead')
                    self.node.upperArmModel = bs.getModel('kronkUpperArm')
                    self.node.torsoModel = bs.getModel('frostyTorso')
                    self.node.pelvisModel = bs.getModel('frostyPelvis')
                    self.node.foreArmModel = bs.getModel('frostyForeArm')
                    self.node.handModel = bs.getModel('frostyHand')
                    self.node.upperLegModel = bs.getModel('frostyUpperLeg')
                    self.node.lowerLegModel = bs.getModel('frostyLowerLeg')
                    self.node.toesModel = bs.getModel('frostyToes')
                    self.node.style = 'frosty'    
                    bsUtils.PopupText("FrostY",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()                    
                    
                elif event == 2:  
                    self.node.colorTexture = bs.getTexture('santaColor')
                    self.node.colorMaskTexture = bs.getTexture('santaColorMask')      
                    self.node.headModel = bs.getModel('santaHead')
                    self.node.upperArmModel = bs.getModel('santaUpperArm')
                    self.node.torsoModel = bs.getModel('santaTorso')
                    self.node.pelvisModel = bs.getModel('kronkPelvis')
                    self.node.foreArmModel = bs.getModel('santaForeArm')
                    self.node.handModel = bs.getModel('santaHand')
                    self.node.upperLegModel = bs.getModel('santaUpperLeg')
                    self.node.lowerLegModel = bs.getModel('santaLowerLeg')
                    self.node.toesModel = bs.getModel('santaToes')
                    self.node.style = 'santa'
                    bsUtils.PopupText("Santa",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                elif event == 3:     
                    self.node.colorTexture = bs.getTexture('bonesColor')
                    self.node.colorMaskTexture = bs.getTexture('bonesColorMask')                
                    self.node.headModel = bs.getModel('bonesHead')
                    self.node.upperArmModel = bs.getModel('bonesUpperArm')
                    self.node.torsoModel = bs.getModel('bonesTorso')
                    self.node.pelvisModel = bs.getModel('bonesPelvis')
                    self.node.foreArmModel = bs.getModel('bonesForeArm')
                    self.node.handModel = bs.getModel('bonesHand')
                    self.node.upperLegModel = bs.getModel('bonesUpperLeg')
                    self.node.lowerLegModel = bs.getModel('bonesLowerLeg')
                    self.node.toesModel = bs.getModel('bonesToes')
                    self.node.style = 'bones'
                    bsUtils.PopupText("Bones",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                elif event == 4:      
                    self.node.colorTexture = bs.getTexture('melColor')
                    self.node.colorMaskTexture = bs.getTexture('melColorMask')                
                    self.node.headModel = bs.getModel('melHead')
                    self.node.upperArmModel = bs.getModel('melUpperArm')
                    self.node.torsoModel = bs.getModel('melTorso')
                    self.node.pelvisModel = bs.getModel('kronkPelvis')
                    self.node.foreArmModel = bs.getModel('melForeArm')
                    self.node.handModel = bs.getModel('melHand')
                    self.node.upperLegModel = bs.getModel('melUpperLeg')
                    self.node.lowerLegModel = bs.getModel('melLowerLeg')
                    self.node.toesModel = bs.getModel('melToes')
                    self.node.style = 'mel'
                    bsUtils.PopupText("Chef Mel",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                elif event == 5:    
                    self.node.colorTexture = bs.getTexture('ninjaColor')
                    self.node.colorMaskTexture = bs.getTexture('ninjaColorMask')                
                    self.node.headModel = bs.getModel('ninjaHead')
                    self.node.upperArmModel = bs.getModel('ninjaUpperArm')
                    self.node.torsoModel = bs.getModel('ninjaTorso')
                    self.node.pelvisModel = bs.getModel('ninjaPelvis')
                    self.node.foreArmModel = bs.getModel('ninjaForeArm')
                    self.node.handModel = bs.getModel('ninjaHand')
                    self.node.upperLegModel = bs.getModel('ninjaUpperLeg')
                    self.node.lowerLegModel = bs.getModel('ninjaLowerLeg')
                    self.node.toesModel = bs.getModel('ninjaToes')
                    self.node.style = 'ninja'
                    bsUtils.PopupText("Secret Ninja",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                elif event == 6:           
                    self.node.colorTexture = bs.getTexture('aliColor')
                    self.node.colorMaskTexture = bs.getTexture('aliColorMask')                
                    self.node.headModel = bs.getModel('aliHead')
                    self.node.upperArmModel = bs.getModel('aliUpperArm')
                    self.node.torsoModel = bs.getModel('aliTorso')
                    self.node.pelvisModel = bs.getModel('aliPelvis')
                    self.node.foreArmModel = bs.getModel('aliForeArm')
                    self.node.handModel = bs.getModel('aliHand')
                    self.node.upperLegModel = bs.getModel('aliUpperLeg')
                    self.node.lowerLegModel = bs.getModel('aliLowerLeg')
                    self.node.toesModel = bs.getModel('aliToes')
                    self.node.style = 'ali'
                    bsUtils.PopupText("ALI",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                elif event == 7:           
                    self.node.colorTexture = bs.getTexture('bearColor')
                    self.node.colorMaskTexture = bs.getTexture('bearColorMask')                
                    self.node.headModel = bs.getModel('bearHead')
                    self.node.upperArmModel = bs.getModel('bearUpperArm')
                    self.node.torsoModel = bs.getModel('bearTorso')
                    self.node.pelvisModel = bs.getModel('bearPelvis')
                    self.node.foreArmModel = bs.getModel('bearForeArm')
                    self.node.handModel = bs.getModel('bearHand')
                    self.node.upperLegModel = bs.getModel('bearUpperLeg')
                    self.node.lowerLegModel = bs.getModel('bearLowerLeg')
                    self.node.toesModel = bs.getModel('bearToes')
                    self.node.style = 'bear'
                    bsUtils.PopupText("BEAR",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                elif event == 8:           
                    self.node.colorTexture = bs.getTexture('penguinColor')
                    self.node.colorMaskTexture = bs.getTexture('penguinColorMask')                
                    self.node.headModel = bs.getModel('penguinHead')
                    self.node.upperArmModel = bs.getModel('penguinUpperArm')
                    self.node.torsoModel = bs.getModel('penguinTorso')
                    self.node.pelvisModel = bs.getModel('penguinPelvis')
                    self.node.foreArmModel = bs.getModel('penguinForeArm')
                    self.node.handModel = bs.getModel('penguinHand')
                    self.node.upperLegModel = bs.getModel('penguinUpperLeg')
                    self.node.lowerLegModel = bs.getModel('penguinLowerLeg')
                    self.node.toesModel = bs.getModel('penguinToes')
                    self.node.style = 'penguin'
                    bsUtils.PopupText("Pengu",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                elif event == 9:           
                    self.node.colorTexture = bs.getTexture('wizardColor')
                    self.node.colorMaskTexture = bs.getTexture('wizardColorMask')                
                    self.node.headModel = bs.getModel('wizardHead')
                    self.node.upperArmModel = bs.getModel('wizardUpperArm')
                    self.node.torsoModel = bs.getModel('wizardTorso')
                    self.node.pelvisModel = bs.getModel('wizardPelvis')
                    self.node.foreArmModel = bs.getModel('wizardForeArm')
                    self.node.handModel = bs.getModel('wizardHand')
                    self.node.upperLegModel = bs.getModel('wizardUpperLeg')
                    self.node.lowerLegModel = bs.getModel('wizardLowerLeg')
                    self.node.toesModel = bs.getModel('wizardToes')
                    self.node.style = 'spaz'
                    bsUtils.PopupText("Spazy",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                elif event == 10:           
                    self.node.colorTexture = bs.getTexture('pixieColor')
                    self.node.colorMaskTexture = bs.getTexture('pixieColorMask')                
                    self.node.headModel = bs.getModel('pixieHead')
                    self.node.upperArmModel = bs.getModel('pixieUpperArm')
                    self.node.torsoModel = bs.getModel('pixieTorso')
                    self.node.pelvisModel = bs.getModel('pixiePelvis')
                    self.node.foreArmModel = bs.getModel('pixieForeArm')
                    self.node.handModel = bs.getModel('pixieHand')
                    self.node.upperLegModel = bs.getModel('pixieUpperLeg')
                    self.node.lowerLegModel = bs.getModel('pixieLowerLeg')
                    self.node.toesModel = bs.getModel('pixieToes')
                    self.node.style = 'pixie'
                    bsUtils.PopupText("Pixie",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                elif event == 11:           
                    self.node.colorTexture = bs.getTexture('cyborgColor')
                    self.node.colorMaskTexture = bs.getTexture('cyborgColorMask')                
                    self.node.headModel = bs.getModel('cyborgHead')
                    self.node.upperArmModel = bs.getModel('cyborgUpperArm')
                    self.node.torsoModel = bs.getModel('cyborgTorso')
                    self.node.pelvisModel = bs.getModel('cyborgPelvis')
                    self.node.foreArmModel = bs.getModel('cyborgForeArm')
                    self.node.handModel = bs.getModel('cyborgHand')
                    self.node.upperLegModel = bs.getModel('cyborgUpperLeg')
                    self.node.lowerLegModel = bs.getModel('cyborgLowerLeg')
                    self.node.toesModel = bs.getModel('cyborgToes')
                    self.node.style = 'cyborg'
                    bsUtils.PopupText("Robot",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
            elif msg.powerupType == 'rrandom':
                
                def _bruh():
                    testingEvent = 0
                        
                    event = random.randint(1,11) if testingEvent == 0 else testingEvent                    
                    
                    if event in [1]:
                        self.node.handleMessage(bs.PowerupMessage(powerupType='boomBomb'))
                        bsUtils.PopupText("BoomBomb",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()                    
                    
                    elif event == 2:  
                        self.node.handleMessage(bs.PowerupMessage(powerupType='blackHole'))
                        bsUtils.PopupText("BlackHole",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                    elif event == 3:     
                        self.node.handleMessage(bs.PowerupMessage(powerupType='frozenBomb'))
                        bsUtils.PopupText("FrozenBomb",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                    elif event == 4:      
                        self.node.handleMessage(bs.PowerupMessage(powerupType='curse'))
                        bsUtils.PopupText("Curse",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                    elif event == 5:    
                        self.node.handleMessage(bs.PowerupMessage(powerupType='health'))
                        bsUtils.PopupText("Health",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                    elif event == 6:           
                        self.node.handleMessage(bs.PowerupMessage(powerupType='punch'))
                        bsUtils.PopupText("Gloves",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                    elif event == 7:           
                        self.node.handleMessage(bs.PowerupMessage(powerupType='shield'))
                        bsUtils.PopupText("Shield",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                    elif event == 8:           
                        self.node.handleMessage(bs.PowerupMessage(powerupType='spunch'))
                        bsUtils.PopupText("Spunch",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                    elif event == 9:           
                        self.node.handleMessage(bs.PowerupMessage(powerupType='blastBot'))
                        bsUtils.PopupText("Blast",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()

                    elif event == 10:           
                        self.node.handleMessage(bs.PowerupMessage(powerupType='knockBomb'))
                        bsUtils.PopupText("Knock",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    
                    elif event == 11:           
                        self.node.handleMessage(bs.PowerupMessage(powerupType='curseShower'))
                        bsUtils.PopupText("CurseShower",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                bs.gameTimer(1000,bs.Call(_bruh))
                    
            elif msg.powerupType == 'hybridBomb':
                self.bombType = 'hybridBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif msg.powerupType == 'bye':
                def _bm():
                    self.node.handleMessage(bs.DieMessage())
                bs.gameTimer(500,bs.Call(_bm))
            elif msg.powerupType == 'spikeBomb':
                self.bombType = 'spikeBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif msg.powerupType == 'gluebomb':
                self.bombType = 'gluebomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                bsUtils.PopupText("SobyDam",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))               
            elif msg.powerupType == 'spazBomb':
                self.bombType = 'spazBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                bsUtils.PopupText("ShayPlays",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))                                             
            elif msg.powerupType == 'knockBomb':
                self.bombType = 'knockBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif msg.powerupType == 'teleBomb':
                self.bombType = 'teleBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif msg.powerupType == 'weedbomb':
                self.bombType = 'weedbomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                bsUtils.PopupText("SobyDamn",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
                                 
            elif msg.powerupType == 'blastBomb':
                self.bombType = 'blastBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
                                 
            elif msg.powerupType == 'boomBomb':
                self.setboomBombCount(min(self.boomBombCount+5, 5))
            elif msg.powerupType == 'revengeBomb':
                self.bombType = 'revengeBomb'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif msg.powerupType == 'rcolor':
                self.node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
                self.node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))  
            elif msg.powerupType == 'colorPicker':
                p = self.node.positionForward
                bsSomething.ColorPicker((p[0],p[1]+2,p[2])).autoRetain() 
            elif msg.powerupType == 'plsTouchMe':
                p = self.node.positionForward
                bsSomething.PlsTouchMe((p[0],p[1]+2,p[2])).autoRetain() 
            elif msg.powerupType == 'characterPicker':
                p = self.node.positionForward
                bsSomething.CharacterPicker((p[0],p[1]+2,p[2])).autoRetain() 
            elif msg.powerupType == 'bomber':
                p = self.node.positionForward
                bsSomething.Bomber((p[0],p[1]+2,p[2])).autoRetain() 
            elif msg.powerupType == 'blastBot':
                p = self.node.positionForward
                bsSomething.BlastBot((p[0],p[1]+2,p[2])).autoRetain()
            elif msg.powerupType == 'botSpawner':
                p = self.node.positionForward
                bsSomething.BotSpawner((p[0],p[1]+2,p[2])).autoRetain()
            elif msg.powerupType == 'beachBall':
                p = self.node.positionForward
                bsSomething.BeachBall((p[0],p[1]+2,p[2])).autoRetain()
            elif msg.powerupType == 'flyer':
                p = self.node.positionForward
                bsSomething.Flyer((p[0],p[1]+2,p[2])).autoRetain()
            elif msg.powerupType == 'blackHole':
                p = self.node.positionForward
                bsSomething.BlackHole((p[0],p[1]+2,p[2])).autoRetain()
                bsUtils.PopupText("BombDash",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
            elif msg.powerupType == 'stickyBombs':
                self.bombType = 'sticky'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
                                 
            elif msg.powerupType == 'shock':
                self._colorRain = bs.Timer(100,bs.WeakCall(self.dropP),repeat = False)
                self._color1Rain = bs.Timer(300,bs.WeakCall(self.dropP),repeat = False)
                self._color2Rain = bs.Timer(500,bs.WeakCall(self.dropP),repeat = False)                                 
                                 
            elif msg.powerupType == 'stickyIce':
                self.bombType = 'stickyIce'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif msg.powerupType == 'revengeHit':
                bsUtils.PopupText("4 sec to Revenge",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                def _boom():
                    self.node.handleMessage(bs.DieMessage())
                    bsUtils.PopupText(u"\ue003Revenged!!\ue003",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                bs.gameTimer(4000,bs.Call(_boom))
            elif msg.powerupType == 'boom':
                bsUtils.PopupText(u"\ue003BOOM\ue003",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                p = self.node.positionForward
                bs.Blast((p[0], p[1] - 1.0, p[2]),(0,1,0),2.0, 'impact', None, 'punch').autoRetain()
                self.node.handleMessage(bs.PowerupMessage(powerupType = 'health'))
                def _boom():
                    self.node.handleMessage(bs.PowerupMessage(powerupType = 'health'))
                    bsUtils.PopupText(u"\ue003Healed Up!!\ue003",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                bs.gameTimer(1500,bs.Call(_boom))
                
            elif msg.powerupType == 'punch':
                self._hasBoxingGloves = True
                tex = bs.Powerup.getFactory().texPunch
                self._flashBillboard(tex)
                self.equipBoxingGloves()
                if self.powerupsExpire:
                    self.node.boxingGlovesFlashing = 0
                    self.node.miniBillboard3Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard3StartTime = t
                    self.node.miniBillboard3EndTime = t+gPowerupWearOffTime
                    self._boxingGlovesWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._glovesWearOffFlash))
                    self._boxingGlovesWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._glovesWearOff))
                                 
            elif msg.powerupType == 'punchs':
                self._hasBoxingGloves = True
                self.equipBoxingGloves()
                                 
            elif msg.powerupType == 'shield':
                factory = self.getFactory()
                # let's allow powerup-equipped shields to lose hp over time
                self.equipShields(
                    decay=True if factory.shieldDecayRate > 0 else False)
            elif msg.powerupType == 'normalShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.Bomb(position=p,velocity=v, sourcePlayer = self.sourcePlayer,bombType = 'normal').autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
            elif msg.powerupType == 'stickyShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.Bomb(position=p,velocity=v, sourcePlayer = self.sourcePlayer,bombType = 'sticky').autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
            elif msg.powerupType == 'iceShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.Bomb(position=p,velocity=v, sourcePlayer = self.sourcePlayer,bombType = 'ice').autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
            elif msg.powerupType == 'touchShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.Bomb(position=p,velocity=v, sourcePlayer = self.sourcePlayer,bombType = 'impact').autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
            elif msg.powerupType == 'glueShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.Bomb(position=p,velocity=v, sourcePlayer = self.sourcePlayer,bombType = 'gluebomb').autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
            elif msg.powerupType == 'cursyShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.Bomb(position=p,velocity=v, sourcePlayer = self.sourcePlayer,bombType = 'cursyBomb').autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
            elif msg.powerupType == 'frozenShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.Bomb(position=p,velocity=v, sourcePlayer = self.sourcePlayer,bombType = 'frozenBomb').autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
                
            elif msg.powerupType == 'curseShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    k = bs.Powerup(position=(p), powerupType=random.choice(["curse","health"]), expire=True).autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
                
            elif msg.powerupType == 'pwpShower':
                def snowfall():
                    p = (-7.3+15.3*random.random(), 11, -5.5+2.1*random.random())#got from meteor shower position :D
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    k = bs.Powerup(position=(p), powerupType=random.choice(["curse","health","punch","shield","impactBombs","iceBombs","stickyBombs"]), expire=True).autoRetain()
                bs.gameTimer(650,bs.Call(snowfall),repeat = True)
                
            elif msg.powerupType == 'curse':
                self.curse()
            elif msg.powerupType == 'sloMo':
                bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion == False
                bsUtils.PopupText(u"\ue00eSLO-MO!\ue00e",color=(1,0.5,0),scale=1.5,position=self.node.position).autoRetain()
                bs.getSharedObject('globals').tint = (0.6,0.6,0.9)
                bs.emitBGDynamics(position=self.node.position,velocity=(0,0,0),count=600,spread=0.7,chunkType='ice');
                
            elif msg.powerupType == 'slimeSnow':
                def snowfall():
                    p = (-10+(random.random()*30),15,-10+(random.random()*30))
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.emitBGDynamics(position=p,velocity=v,count=10,scale=1+random.random(),spread=0,chunkType='slime')
                bs.gameTimer(20,bs.Call(snowfall),repeat = True)
                
            elif msg.powerupType == 'splinterSnow':
                def snowfall():
                    p = (-10+(random.random()*30),15,-10+(random.random()*30))
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.emitBGDynamics(position=p,velocity=v,count=10,scale=1+random.random(),spread=0,chunkType='splinter')
                bs.gameTimer(20,bs.Call(snowfall),repeat = True)
                
            elif msg.powerupType == 'iceSnow':
                def snowfall():
                    p = (-10+(random.random()*30),15,-10+(random.random()*30))
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.emitBGDynamics(position=p,velocity=v,count=10,scale=1+random.random(),spread=0,chunkType='ice')
                bs.gameTimer(20,bs.Call(snowfall),repeat = True)
                
            elif msg.powerupType == 'sparkSnow':
                def snowfall():
                    p = (-10+(random.random()*30),15,-10+(random.random()*30))
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.emitBGDynamics(position=p,velocity=v,count=10,scale=1+random.random(),spread=0,chunkType='spark')
                bs.gameTimer(20,bs.Call(snowfall),repeat = True)
                
            elif msg.powerupType == 'sweatSnow':
                def snowfall():
                    p = (-10+(random.random()*30),15,-10+(random.random()*30))
                    v = ((-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0), -50.0,(-5.0+random.random()*30.0) * (-1.0 if p[0] > 0 else 1.0))
                    bs.emitBGDynamics(position=p,velocity=v,count=10,scale=1+random.random(),spread=0,chunkType='sweat')
                bs.gameTimer(20,bs.Call(snowfall),repeat = True)

            elif (msg.powerupType == 'iceBombs'):
                self.bombType = 'ice'
                tex = self._getBombTypeTex()
                bsUtils.PopupText("Sticky", color = self.node.color,scale = 1.7, position = self.node.position).autoRetain()
                self._flashBillboard(tex)
                if self.powerupsExpire:
                    self.node.miniBillboard2Texture = tex
                    t = bs.getGameTime()
                    self.node.miniBillboard2StartTime = t
                    self.node.miniBillboard2EndTime = t+gPowerupWearOffTime
                    self._bombWearOffFlashTimer = \
                        bs.Timer(gPowerupWearOffTime-2000,
                                 bs.WeakCall(self._bombWearOffFlash))
                    self._bombWearOffTimer = \
                        bs.Timer(gPowerupWearOffTime,
                                 bs.WeakCall(self._bombWearOff))
            elif (msg.powerupType == 'health'):
                if self._cursed:
                    self._cursed = False
                    # remove cursed material
                    factory = self.getFactory()
                    for attr in ['materials', 'rollerMaterials']:
                        materials = getattr(self.node, attr)
                        if factory.curseMaterial in materials:
                            setattr(self.node, attr,
                                    tuple(m for m in materials
                                          if m != factory.curseMaterial))
                    self.node.curseDeathTime = 0
                self.hitPoints = self.hitPointsMax
                self._flashBillboard(bs.Powerup.getFactory().texHealth)
                self.node.hurt = 0
                self._lastHitTime = None
                self._numTimesHit = 0
                
            self.node.handleMessage("flash")
            if msg.sourceNode.exists():
                msg.sourceNode.handleMessage(bs.PowerupAcceptMessage())
            return True

        elif isinstance(msg, bs.FreezeMessage):
            if not self.node.exists(): return
            if self.node.invincible == True:
                bs.playSound(self.getFactory().blockSound, 1.0,
                             position=self.node.position)
                return
            if self.shield is not None: return
            if not self.frozen:
                self.frozen = True
                self.node.frozen = 1
                bs.gameTimer(5000, bs.WeakCall(self.handleMessage,
                                               bs.ThawMessage()))
                # instantly shatter if we're already dead
                # (otherwise its hard to tell we're dead)
                if self.hitPoints <= 0:
                    self.shatter()

        elif isinstance(msg, bs.ThawMessage):
            if self.frozen and not self.shattered and self.node.exists():
                self.frozen = False
                self.node.frozen = 0
                
        elif isinstance(msg, bs.HitMessage):
            if not self.node.exists(): return
            if self.node.invincible == True:
                bs.playSound(self.getFactory().blockSound,
                             1.0, position=self.node.position)
                return True

            # if we were recently hit, don't count this as another
            # (so punch flurries and bomb pileups essentially count as 1 hit)
            gameTime = bs.getGameTime()
            if self._lastHitTime is None or gameTime-self._lastHitTime > 1000:
                self._numTimesHit += 1
                self._lastHitTime = gameTime
            
            mag = msg.magnitude * self._impactScale
            velocityMag = msg.velocityMagnitude * self._impactScale

            damageScale = 0.22

            # if they've got a shield, deliver it to that instead..
            if self.shield is not None:

                if msg.flatDamage: damage = msg.flatDamage * self._impactScale
                else:
                    # hit our spaz with an impulse but tell it to only return
                    # theoretical damage; not apply the impulse..
                    self.node.handleMessage(
                        "impulse", msg.pos[0], msg.pos[1], msg.pos[2],
                        msg.velocity[0], msg.velocity[1], msg.velocity[2],
                        mag , velocityMag, msg.radius, 1,
                        msg.forceDirection[0], msg.forceDirection[1],
                        msg.forceDirection[2])
                    damage = damageScale * self.node.damage

                self.shieldHitPoints -= damage

                self.shield.hurt = (1.0 - float(self.shieldHitPoints)
                                    /self.shieldHitPointsMax)
                # its a cleaner event if a hit just kills the shield
                # without damaging the player..
                # however, massive damage events should still be able to
                # damage the player.. this hopefully gives us a happy medium.
                maxSpillover = self.getFactory().maxShieldSpilloverDamage
                if self.shieldHitPoints <= 0:
                    # fixme - transition out perhaps?..
                    self.shield.delete()
                    self.shield = None
                    bs.playSound(self.getFactory().shieldDownSound, 1.0,
                                 position=self.node.position)
                    # emit some cool lookin sparks when the shield dies
                    t = self.node.position
                    bs.emitBGDynamics(position=(t[0], t[1]+0.9, t[2]),
                                      velocity=self.node.velocity,
                                      count=random.randrange(20, 30), scale=1.0,
                                      spread=0.6, chunkType='spark')

                else:
                    bs.playSound(self.getFactory().shieldHitSound, 0.5,
                                 position=self.node.position)

                # emit some cool lookin sparks on shield hit
                bs.emitBGDynamics(position=msg.pos,
                                  velocity=(msg.forceDirection[0]*1.0,
                                            msg.forceDirection[1]*1.0,
                                            msg.forceDirection[2]*1.0),
                                  count=min(30, 5+int(damage*0.005)),
                                  scale=0.5, spread=0.3, chunkType='spark')

                # if they passed our spillover threshold,
                # pass damage along to spaz
                if self.shieldHitPoints <= -maxSpillover:
                    leftoverDamage = -maxSpillover-self.shieldHitPoints
                    shieldLeftoverRatio = leftoverDamage/damage

                    # scale down the magnitudes applied to spaz accordingly..
                    mag *= shieldLeftoverRatio
                    velocityMag *= shieldLeftoverRatio
                else:
                    return True # good job shield!
            else: shieldLeftoverRatio = 1.0

            if msg.flatDamage:
                damage = (msg.flatDamage * self._impactScale
                          * shieldLeftoverRatio)
            else:
                # hit it with an impulse and get the resulting damage
                self.node.handleMessage(
                    "impulse", msg.pos[0], msg.pos[1], msg.pos[2],
                    msg.velocity[0], msg.velocity[1], msg.velocity[2],
                    mag, velocityMag, msg.radius, 0,
                    msg.forceDirection[0], msg.forceDirection[1],
                    msg.forceDirection[2])

                damage = damageScale * self.node.damage
            self.node.handleMessage("hurtSound")

            # play punch impact sound based on damage if it was a punch
            if msg.hitType == 'punch':

                self.onPunched(damage)
                if damage > 0 and damage < 100:
                    bsUtils.PopupText(u"harder",color=(1,1,1),scale=1.6,position=self.node.position).autoRetain()
                    bsUtils.showDamageCount('-' + str(int(damage)) + " points", msg.pos, msg.forceDirection)
                if damage > 200 and damage < 450:
                    bsUtils.showDamageCount('-' + str(int(damage)) + " points", msg.pos, msg.forceDirection)
                    bsUtils.PopupText(u"noob",color=(1,1,1),scale=1.6,position=self.node.position).autoRetain()
                if damage > 450 and damage < 800:
                    bsUtils.showDamageCount('-' + str(int(damage/10)) + "%", msg.pos, msg.forceDirection)
                    bsUtils.PopupText(u"better",color=(1,1,1),scale=1.6,position=self.node.position).autoRetain()
                if damage > 801 and damage < 1109:
                    bsUtils.showDamageCount('-' + str(int(damage/10)) + "%", msg.pos, msg.forceDirection)
                    bsUtils.PopupText(u"\ue048GrandMaster\ue048",color=(1,1,1),scale=1.6,position=self.node.position).autoRetain()
                if damage > 1110 and damage < 1500:
                    bsUtils.showDamageCount('-' + str(int(damage/10)) + "%", msg.pos, msg.forceDirection)
                    bsUtils.PopupText(u"\ue048BOSSS\ue048",color=(1,1,1),scale=1.6,position=self.node.position).autoRetain()
                    p = self.node.positionForward
                    bsSomething.BlackHole((p[0],p[1]+2,p[2])).autoRetain()
                    #bs.screenMessage('BlackHole Summoned with dat PUNCH',color=(1,1,1))
                    bs.screenMessage('%s summoned a BlackHole with dat PUNCH!' % self.sourcePlayer.getName(), color=(1, 1, 1))
                    
                if msg.hitSubType == 'superPunch':
                    try: bs.playSound(self.getFactory().punchSoundStronger, 1.0, position=msg.pos)
                    except: pass 
                if damage > 500:
                    sounds = self.getFactory().punchSoundsStrong
                    sound = sounds[random.randrange(len(sounds))]
                    if damage > 1000:
                        bs.emitBGDynamics(position=msg.pos,
                                      chunkType='spark',
                                      velocity=(msg.forceDirection[0]*1.3*1.5,
                                                msg.forceDirection[1]*1.3*1.5+5.0,
                                                msg.forceDirection[2]*1.3*1.5),
                                      count=min(300, 105+int(damage*0.44)) if damage < 30000 else 580,
                                      scale=0.9,
                                      spread=0.28);
                    bs.emitBGDynamics(position=msg.pos,
                                  chunkType='sweat',
                                  velocity=(msg.forceDirection[0]*1.3*2,
                                            msg.forceDirection[1]*1.3*2+5.0,
                                            msg.forceDirection[2]*1.3*2),
                                  count=min(150, 75+int(damage*0.44)) if damage <= 1000 else 155,
                                  scale=0.65,
                                  spread=0.21);
                else: sound = self.getFactory().punchSound
                try: bs.playSound(sound, 1.0, position=msg.pos)
                except: pass
                self.realPos = msg.pos
                bs.emitBGDynamics(position=msg.pos,
                                  velocity=(msg.forceDirection[0]*0.5,
                                            msg.forceDirection[1]*0.5,
                                            msg.forceDirection[2]*0.5),
                                  count=min(10, 1+int(damage*0.0025)),
                                  scale=0.3, spread=0.03);

                bs.emitBGDynamics(position=msg.pos,
                                  chunkType='sweat',
                                  velocity=(msg.forceDirection[0]*1.3,
                                            msg.forceDirection[1]*1.3+5.0,
                                            msg.forceDirection[2]*1.3),
                                  count=min(30, 1+int(damage*0.04)),
                                  scale=0.9,
                                  spread=0.28);
                # momentary flash
                hurtiness = damage*0.003
                hurtiness += min(hurtiness, 750 * 0.003)
                punchPos = (msg.pos[0]+msg.forceDirection[0]*0.02,
                            msg.pos[1]+msg.forceDirection[1]*0.02,
                            msg.pos[2]+msg.forceDirection[2]*0.02)
                flashColor = (1.0, 0.8, 0.4)
                light = bs.newNode("light",
                                   attrs={'position':punchPos,
                                          'radius':0.12+hurtiness*0.12,
                                          'intensity':0.3*(1.0+1.0*hurtiness),
                                          'heightAttenuated':False,
                                          'color':flashColor})
                bs.gameTimer(60, light.delete)


                flash = bs.newNode("flash",
                                   attrs={'position':punchPos,
                                          'size':0.17+0.17*hurtiness,
                                          'color':flashColor})
                if fire.punchFlash:
                    bs.gameTimer(200, flash.delete)
                else:
                    bs.gameTimer(60, flash.delete)

            if msg.hitType == 'impact':
                bs.emitBGDynamics(position=msg.pos,
                                  velocity=(msg.forceDirection[0]*2.0,
                                            msg.forceDirection[1]*2.0,
                                            msg.forceDirection[2]*2.0),
                                  count=min(10, 1+int(damage*0.01)),
                                  scale=0.4, spread=0.1);
            if self.hitPoints > 0:
                # its kinda crappy to die from impacts, so lets reduce
                # impact damage by a reasonable amount if it'll keep us alive
                if msg.hitType == 'impact' and damage > self.hitPoints:
                    # drop damage to whatever puts us at 10 hit points,
                    # or 200 less than it used to be whichever is greater
                    # (so it *can* still kill us if its high enough)
                    newDamage = max(damage-200, self.hitPoints-10)
                    damage = newDamage
                self.node.handleMessage("flash")
                # if we're holding something, drop it
                if damage > 0.0 and self.node.holdNode.exists():
                    self.node.holdNode = bs.Node(None)
                self.hitPoints -= damage
                self.node.hurt = 1.0 - float(self.hitPoints)/self.hitPointsMax
                # if we're cursed, *any* damage blows us up
                if self._cursed and damage > 0:
                    bs.gameTimer(50, bs.WeakCall(self.curseExplode,
                                                 msg.sourcePlayer))
                # if we're frozen, shatter.. otherwise die if we hit zero
                if self.frozen and (damage > 200 or self.hitPoints <= 0):
                    self.shatter()
                elif self.hitPoints <= 0:
                    self.node.handleMessage(bs.DieMessage(how='impact'))

            # if we're dead, take a look at the smoothed damage val
            # (which gives us a smoothed average of recent damage) and shatter
            # us if its grown high enough
            if self.hitPoints <= 0:
                damageAvg = self.node.damageSmoothed * damageScale
                if damageAvg > 1000:
                    self.shatter()
                    
            if fire.hp: self._hpText.text = 'HP: ' + str(int(self.hitPoints))
            else: self._hpText.text = ''

        elif isinstance(msg, _BombDiedMessage):
            self.bombCount += 1
        
        elif isinstance(msg, bs.DieMessage):
            wasDead = self._dead
            self._dead = True
            self.hitPoints = 0
            if msg.immediate:
                self.node.delete()
            elif self.node.exists():
                self.node.hurt = 1.0
                if self.playBigDeathSound and not wasDead:
                    bs.playSound(self.getFactory().singlePlayerDeathSound)
                self.node.dead = True
                bs.gameTimer(2000, self.node.delete)

        elif isinstance(msg, bs.OutOfBoundsMessage):
            # by default we just die here
            self.handleMessage(bs.DieMessage(how='fall'))
        elif isinstance(msg, bs.StandMessage):
            self._lastStandPos = (msg.position[0], msg.position[1],
                                  msg.position[2])
            self.node.handleMessage("stand", msg.position[0], msg.position[1],
                                    msg.position[2], msg.angle)
        elif isinstance(msg, _CurseExplodeMessage):
            self.curseExplode()
        elif isinstance(msg, _PunchHitMessage):
            node = bs.getCollisionInfo("opposingNode")

            # only allow one hit per node per punch
            if (node is not None and node.exists()
                and not node in self._punchedNodes):
                
                punchMomentumAngular = (self.node.punchMomentumAngular
                                        * self._punchPowerScale)
                punchPower = self.node.punchPower * self._punchPowerScale

                # ok here's the deal:  we pass along our base velocity for use
                # in the impulse damage calculations since that is a more
                # predictable value than our fist velocity, which is rather
                # erratic. ...however we want to actually apply force in the
                # direction our fist is moving so it looks better.. so we still
                # pass that along as a direction ..perhaps a time-averaged
                # fist-velocity would work too?.. should try that.
                
                # if its something besides another spaz, just do a muffled punch
                # sound
                if node.getNodeType() != 'spaz':
                    sounds = self.getFactory().impactSoundsMedium
                    sound = sounds[random.randrange(len(sounds))]
                    bs.playSound(sound, 1.0, position=self.node.position)

                t = self.node.punchPosition
                punchDir = self.node.punchVelocity
                v = self.node.punchMomentumLinear

                self._punchedNodes.add(node)
                node.handleMessage(
                    bs.HitMessage(
                        pos=t,
                        velocity=v,
                        magnitude=punchPower*punchMomentumAngular*110.0,
                        velocityMagnitude=punchPower*40,
                        radius=0,
                        srcNode=self.node,
                        sourcePlayer=self.sourcePlayer,
                        forceDirection = punchDir,
                        hitType='punch',
                        hitSubType=('superPunch' if self._hasBoxingGloves
                                    else 'default')))

                # also apply opposite to ourself for the first punch only
                # ..this is given as a constant force so that it is more
                # noticable for slower punches where it matters.. for fast
                # awesome looking punches its ok if we punch 'through'
                # the target
                mag = -400.0
                if self._hockey: mag *= 0.5
                if len(self._punchedNodes) == 1:
                    self.node.handleMessage("kickBack", t[0], t[1], t[2],
                                            punchDir[0], punchDir[1],
                                            punchDir[2], mag)

        elif isinstance(msg, _PickupMessage):
            opposingNode, opposingBody = bs.getCollisionInfo('opposingNode',
                                                            'opposingBody')

            if opposingNode is None or not opposingNode.exists(): return True

            # dont allow picking up of invincible dudes
            try:
                if opposingNode.invincible == True: return True
            except Exception: pass

            # if we're grabbing the pelvis of a non-shattered spaz, we wanna
            # grab the torso instead
            if (opposingNode.getNodeType() == 'spaz'
                and not opposingNode.shattered and opposingBody == 4):
                opposingBody = 1

            # special case - if we're holding a flag, dont replace it
            # ( hmm - should make this customizable or more low level )
            held = self.node.holdNode
            if (held is not None and held.exists()
                and held.getNodeType() == 'flag'): return True
            self.node.holdBody = opposingBody # needs to be set before holdNode
            self.node.holdNode = opposingNode
        else:
            bs.Actor.handleMessage(self, msg)
            
def dropBomb(self):
        """
        Tell the spaz to drop one of his bombs, and returns
        the resulting bomb object.
        If the spaz has no bombs or is otherwise unable to
        drop a bomb, returns None.
        """

        if (self.landMineCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.epicMineCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.iceMineCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.powerupCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.iceImpactCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.curseBombCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.boomBombCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.antiGravCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.headacheCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.portalBombCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.cursyBombCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.fireBombCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        elif (self.shockWaveCount <= 0 and self.bombCount <= 0) or self.frozen:
            return
        p = self.node.positionForward
        v = self.node.velocity

        if self.landMineCount > 0:
            droppingBomb = False
            self.setLandMineCount(self.landMineCount-1)
            bombType = 'landMine'
        elif self.epicMineCount > 0:
            droppingBomb = False
            self.setepicMineCount(self.epicMineCount-1)
            bombType = 'epicMine'
        elif self.iceMineCount > 0:
            droppingBomb = False
            self.seticeMineCount(self.iceMineCount-1)
            bombType = 'iceMine'
        elif self.powerupCount > 0:
            droppingBomb = False
            self.setpowerupCount(self.powerupCount-1)
            bombType = 'powerup'
        elif self.iceImpactCount > 0:
            droppingBomb = False
            self.seticeImpactCount(self.iceImpactCount-1)
            bombType = 'iceImpact'
        elif self.curseBombCount > 0:
            droppingBomb = False
            self.setcurseBombCount(self.curseBombCount-1)
            bombType = 'curseBomb'
        elif self.boomBombCount > 0:
            droppingBomb = False
            self.setboomBombCount(self.boomBombCount-1)
            bombType = 'boomBomb'
        elif self.antiGravCount > 0:
            droppingBomb = False
            self.setAntiGravCount(self.antiGravCount - 1)
            bombType = 'antiGrav'
        elif self.headacheCount > 0:
            droppingBomb = False
            self.setHeadacheCount(self.headacheCount - 1)
            bombType = 'headache'
        elif self.portalBombCount > 0:
            droppingBomb = False
            self.setportalBombCount(self.portalBombCount - 1)
            bombType = 'portalBomb'
        elif self.cursyBombCount > 0:
            droppingBomb = False
            self.setcursyBombCount(self.cursyBombCount - 1)
            bombType = 'cursyBomb'
        elif self.fireBombCount > 0:
            droppingBomb = False
            self.setfireBombCount(self.fireBombCount - 1)
            bombType = 'fireBomb'
        elif self.shockWaveCount > 0:
            droppingBomb = False
            self.setshockWaveCount(self.shockWaveCount - 1)
            bombType = 'shockWave'
        else:
            droppingBomb = True
            bombType = self.bombType

        bomb = bs.Bomb(position=(p[0], p[1] - 0.0, p[2]),
                       velocity=(v[0], v[1], v[2]),
                       bombType=bombType,
                       blastRadius=self.blastRadius,
                       sourcePlayer=self.sourcePlayer,
                       owner=self.node).autoRetain()

        if droppingBomb:
            self.bombCount -= 1
            bomb.node.addDeathAction(bs.WeakCall(self.handleMessage,
                                                 _BombDiedMessage()))
        self._pickUp(bomb.node)

        for c in self._droppedBombCallbacks: c(self, bomb)
        
        return bomb
        
def lightningBolt(self, position=(0, 10, 0), radius=10):
        bs.shakeCamera(2)
        tint = bs.getSharedObject('globals').tint
        light = bs.newNode('light',
                           attrs={
                               'position': position,
                               'color': (0.2, 0.2, 0.4),
                               'volumeIntensityScale': 1.0,
                               'radius': radius
                           })
        bs.gameTimer(500,self.light.delete)  
        
def seticeImpactCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.iceImpactCount = count
        if self.node.exists():
            if self.iceImpactCount != 0:
                self.node.counterText = 'x'+str(self.iceImpactCount)
                self.node.counterTexture = bs.Powerup.getFactory().texiceImpact
            else:
                self.node.counterText = ''
                
def setcurseBombCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.curseBombCount = count
        if self.node.exists():
            if self.curseBombCount != 0:
                self.node.counterText = 'x'+str(self.curseBombCount)
                self.node.counterTexture = bs.Powerup.getFactory().texcurseBomb
            else:
                self.node.counterText = ''
                
def setportalBombCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.portalBombCount = count
        if self.node.exists():
            if self.portalBombCount != 0:
                self.node.counterText = 'x'+str(self.portalBombCount)
                self.node.counterTexture = bs.Powerup.getFactory().texportalBomb
            else:
                self.node.counterText = ''
                
def setboomBombCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.boomBombCount = count
        if self.node.exists():
            if self.boomBombCount != 0:
                self.node.counterText = 'x'+str(self.boomBombCount)
                self.node.counterTexture = bs.Powerup.getFactory().texboomBomb
            else:
                self.node.counterText = ''
                
def setepicMineCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.epicMineCount = count
        if self.node.exists():
            if self.epicMineCount != 0:
                self.node.counterText = 'x'+str(self.epicMineCount)
                self.node.counterTexture = bs.Powerup.getFactory().texEpicMine
            else:
                self.node.counterText = ''
                
def seticeMineCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.iceMineCount = count
        if self.node.exists():
            if self.iceMineCount != 0:
                self.node.counterText = 'x'+str(self.iceMineCount)
                self.node.counterTexture = bs.Powerup.getFactory().texIceMine
            else:
                self.node.counterText = ''
                
def setpowerupCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.powerupCount = count
        if self.node.exists():
            if self.powerupCount != 0:
                self.node.counterText = 'x'+str(self.powerupCount)
                self.node.counterTexture = bs.Powerup.getFactory().texPowerup
            else:
                self.node.counterText = ''
                
def setcursyBombCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.cursyBombCount = count
        if self.node.exists():
            if self.cursyBombCount != 0:
                self.node.counterText = 'x'+str(self.cursyBombCount)
                self.node.counterTexture = bs.Powerup.getFactory().texcurseBomb
            else:
                self.node.counterText = ''
                
def setfireBombCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.fireBombCount = count
        if self.node.exists():
            if self.fireBombCount != 0:
                self.node.counterText = 'x'+str(self.fireBombCount)
                self.node.counterTexture = bs.Powerup.getFactory().texfireBomb
            else:
                self.node.counterText = ''
                
def setshockWaveCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.shockWaveCount = count
        if self.node.exists():
            if self.shockWaveCount != 0:
                self.node.counterText = 'x'+str(self.shockWaveCount)
                self.node.counterTexture = bs.Powerup.getFactory().texShockWave
            else:
                self.node.counterText = ''
                
def setHeadacheCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.headacheCount = count
        if self.node.exists():
            if self.headacheCount != 0:
                self.node.counterText = 'x' + str(self.headacheCount)
                self.node.counterTexture = bs.Powerup.getFactory().texAche
            else:
                self.node.counterText = ''
                

def setAntiGravCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.antiGravCount = count
        if self.node.exists():
            if self.antiGravCount != 0:
                self.node.counterText = 'x' + str(self.antiGravCount)
                self.node.counterTexture = bs.Powerup.getFactory().texAntiGrav
            else:
                self.node.counterText = ''
                
def _nightWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = bs.Powerup.getFactory().texNight
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True
            
def _nightWearOff(self):
        factory = self.getFactory()
        bs.getSharedObject('globals').tint = (0.5,0.7,1)
        t = bs.playSound(bs.getSound('morning'))
        t = bs.screenMessage("!Morning!", color=(0, 0.5, 0.8))
        if self.node.exists():
            self.node.billboardOpacity = 0.0
            
def _jumpFlyWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = bs.Powerup.getFactory().texJumpFly
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True
            
def _jumpFlyWearOff(self):
    	player = self.getPlayer()
    	player.assignInputCall('jumpPress', self.onJumpPress)
        if self.node.exists():
            self.node.billboardOpacity = 0.0      
            
def _magWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = bs.Powerup.getFactory().texJumpFly
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True
            
def pc_getBombTypeTex(self):
        bombFactory = bs.Powerup.getFactory()
        if self.bombType == 'sticky': return bombFactory.texStickyBombs
        elif self.bombType == 'stickyIce': return bombFactory.texStickyIce
        elif self.bombType == 'ice': return bombFactory.texIceBombs
        elif self.bombType == 'impact': return bombFactory.texImpactBombs
        elif self.bombType == 'curseBomb': return bombFactory.texcurseBomb
        elif self.bombType == 'iceImpact': return bombFactory.texiceImpact
        elif self.bombType == 'blastBomb': return bombFactory.texBlastBomb
        elif self.bombType == 'boomBomb': return bombFactory.texboomBomb
        elif self.bombType == 'cursyBomb': return bombFactory.texcurseBomb
        elif self.bombType == 'revengeBomb': return bombFactory.texrevengeBomb
        elif self.bombType == 'hybridBomb': return bombFactory.texhybridBomb
        elif self.bombType == 'knockBomb': return bombFactory.texknockBomb
        elif self.bombType == 'weedbomb': return bombFactory.texweedbomb
        elif self.bombType == 'gluebomb': return bombFactory.texgluebomb
        elif self.bombType == 'spazBomb': return bombFactory.texspazBomb
        elif self.bombType == 'frozenBomb': return bombFactory.texspazBomb
        elif self.bombType == 'portalBomb': return bombFactory.texportalBomb
        elif self.bombType == 'teleBomb': return bombFactory.texTeleBomb
        elif self.bombType == 'fireBomb': return bombFactory.texfireBomb
        elif self.bombType == 'powerup': return bombFactory.texPowerup
        elif self.bombType == 'spikeBomb': return bombFactory.texShockWave
        else: raise Exception()
                
def dropP(self):
    bsSomething.ShockWave(position = (self.node.position[0],self.node.position[1]-0.5,self.node.position[2]))

Spaz.handleMessage = pchandleMessage
Spaz.RespawnIcon = RespawnIcon
Spaz._getBombTypeTex = pc_getBombTypeTex
Spaz.onPunchPress = pconPunchPress
Spaz.onPickUpPress = pconPickUpPress
Spaz.dropP = dropP
Spaz.dropBomb = dropBomb
Spaz.seticeImpactCount = seticeImpactCount
Spaz.setepicMineCount = setepicMineCount
Spaz.seticeMineCount = seticeMineCount
Spaz.setcurseBombCount = setcurseBombCount
Spaz.setpowerupCount = setpowerupCount
Spaz.setportalBombCount = setportalBombCount
Spaz.setcursyBombCount = setcursyBombCount
Spaz.setfireBombCount = setfireBombCount
Spaz.setshockWaveCount = setshockWaveCount
Spaz.setboomBombCount = setboomBombCount
Spaz.setAntiGravCount = setAntiGravCount
Spaz.setHeadacheCount = setHeadacheCount
Spaz.lightningBolt = lightningBolt
Spaz._nightWearOff = _nightWearOff
Spaz._nightWearOffFlash = _nightWearOffFlash
Spaz.onJumpfly = onJumpfly
Spaz._jumpFlyWearOffFlash = _jumpFlyWearOffFlash
Spaz._jumpFlyWearOff = _jumpFlyWearOff
Spaz._magWearOffFlash = _magWearOffFlash