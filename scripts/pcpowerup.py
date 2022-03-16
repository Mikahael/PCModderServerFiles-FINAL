#first mod released to the public by PC||Modder/PC231392/PC290717
#kindly do give some credit to me for those using.
#thankyou for using PC Server Files
#they work on all server files from 1.4.148 and up
#only could do this much my friends. No more time I have. Must leave. if had more time, would have added much more.
#thanks to all who supported me and are friends with me.
#without knight nor blitz, none of this would have been deemed possible
#final pc script. those who want to continue, use source code
#thanks to God
import bsPowerup
from bsPowerup import *
import bs
import bsSpaz
from fire import *
import fire
import bsUtils
from bsSpaz import Spaz
import spazPC
import random
import SnoBallz
import bsSomething
import newObjects
import objects as objs
import bsInternal

from bsPowerup import PowerupMessage, PowerupAcceptMessage, _TouchedMessage, PowerupFactory, Powerup

defaultPowerupInterval = 8000

class _TouchedMessage(object):
    pass

class PowerupFactory(object):
    """
    category: Game Flow Classes
    
    Wraps up media and other resources used by bs.Powerups.
    A single instance of this is shared between all powerups
    and can be retrieved via bs.Powerup.getFactory().

    Attributes:

       model
          The bs.Model of the powerup box.

       modelSimple
          A simpler bs.Model of the powerup box, for use in shadows, etc.

       texBox
          Triple-bomb powerup bs.Texture.

       texPunch
          Punch powerup bs.Texture.

       texIceBombs
          Ice bomb powerup bs.Texture.

       texStickyBombs
          Sticky bomb powerup bs.Texture.

       texShield
          Shield powerup bs.Texture.

       texImpactBombs
          Impact-bomb powerup bs.Texture.

       texHealth
          Health powerup bs.Texture.

       texLandMines
          Land-mine powerup bs.Texture.

       texCurse
          Curse powerup bs.Texture.

       healthPowerupSound
          bs.Sound played when a health powerup is accepted.

       powerupSound
          bs.Sound played when a powerup is accepted.

       powerdownSound
          bs.Sound that can be used when powerups wear off.

       powerupMaterial
          bs.Material applied to powerup boxes.

       powerupAcceptMaterial
          Powerups will send a bs.PowerupMessage to anything they touch
          that has this bs.Material applied.
    """

    def __init__(self):
        """
        Instantiate a PowerupFactory.
        You shouldn't need to do this; call bs.Powerup.getFactory()
        to get a shared instance.
        """

        self._lastPowerupType = None

        self.model = bs.getModel("powerup")
        self.modelSimple = bs.getModel("powerupSimple")

        self.texBomb = bs.getTexture("powerupBomb")
        self.texPunch = bs.getTexture("powerupPunch")
        self.texIceBombs = bs.getTexture("powerupIceBombs")
        self.texStickyBombs = bs.getTexture("powerupStickyBombs")
        self.texShield = bs.getTexture("powerupShield")
        self.texImpactBombs = bs.getTexture("powerupImpactBombs")
        self.texHealth = bs.getTexture("powerupHealth")
        self.texLandMines = bs.getTexture("powerupLandMines")
        self.texCurse = bs.getTexture("powerupCurse")
        self.texSloMo = bs.getTexture("achievementFlawlessVictory")
        self.textnt = bs.getTexture("achievementTNT")
        self.texStrongICE = bs.getTexture("menuButton")
        self.texSpeedBoots = bs.getTexture("achievementGotTheMoves")
        self.texChamp = bs.getTexture("achievementBoxer")
        self.texTroll = bs.getTexture("achievementOffYouGo")
        self.texCharacter = bs.getTexture("crossOut")
        self.texInvincible = bs.getTexture("achievementSuperPunch")
        self.texInvisible = bs.getTexture("ouyaOButton")
        self.texcurseBomb = bs.getTexture("windowHSmallVMed")
        self.texhybridBomb = bs.getTexture("bombButton")
        self.texiceImpact = bs.getTexture("gameCircleIcon")
        self.texBlastBomb = bs.getTexture("achievementOnslaught")
        self.texboomBomb = bs.getTexture("settingsIcon")
        self.texrevengeBomb = bs.getTexture("menuButton")
        self.texmultiBomb = bs.getTexture("levelIcon")
        self.textntExplode = bs.getTexture("achievementEmpty")
        self.texAntiGrav = bs.getTexture("achievementFootballShutout")
        self.texAche = bs.getTexture("achievementOnslaught")
        self.texRadius = bs.getTexture("achievementOnslaught")
        self.texSpunch = bs.getTexture("achievementSuperPunch")
        self.texNight = bs.getTexture("reflectionPowerup_+x")
        self.texAtomBomb = bs.getTexture("achievementCrossHair")
        self.texJumpFly = bs.getTexture("achievementOffYouGo")
        self.texSno = bs.getTexture("bunnyColor")
        self.texBlackHole = bs.getTexture("circleOutlineNoAlpha")
        self.texTouchMe = bs.getTexture("settingsIcon")
        self.texImpactShower = bs.getTexture("coin")
        self.texBubble = bs.getTexture("eggTex3")
        self.texMag = bs.getTexture("tickets")
        self.texPortal = bs.getTexture("ouyaOButton")
        self.texBlast = bs.getTexture("tnt")
        self.texMix = bs.getTexture("achievementEmpty")
        self.texknockBomb = bs.getTexture("eggTex1")
        self.texweedbomb = bs.getTexture("egg2")
        self.texgluebomb = bs.getTexture("logo")
        self.texspazBomb = bs.getTexture("cuteSpaz")
        self.texMartyrdom = bs.getTexture("achievementCrossHair")
        self.texSuperStar = bs.getTexture("levelIcon")
        self.texBlaster = bs.getTexture("egg3")
        self.texKnock = bs.getTexture("powerupPunch")
        self.texCrazy = bs.getTexture("achievementEmpty")#frozenbomb
        self.texportalBomb = bs.getTexture("egg4")
        self.texTeleBomb = bs.getTexture("egg")
        self.texFlyer = bs.getTexture("buttonPickUp")
        self.texBeachBall = bs.getTexture("achievementFootballShutout")
        self.texPuck = bs.getTexture("achievementTeamPlayer")
        self.texBomber = bs.getTexture("achievementEmpty")
        self.texPirate = bs.getTexture("jackIcon")
        self.texBotSpawner = bs.getTexture("bunnyIconColorMask")
        self.texCharacterPicker = bs.getTexture("achievementFlawlessVictory")
        self.texColorPicker = bs.getTexture("graphicsIcon")
        self.texVolcano = bs.getTexture("alienIconColorMask")
        self.texPlsTouchMe = bs.getTexture("achievementEmpty")
        self.texfireBomb = bs.getTexture("aliSplash")
        self.texEpicMine = bs.getTexture("achievementInControl")
        self.texPowerup = bs.getTexture("achievementMedalLarge")
        self.texIceMine = bs.getTexture("egg2")
        self.texStickyIce = bs.getTexture("eggTex2")
        self.texShockWave = bs.getTexture("heart")

        self.healthPowerupSound = bs.getSound("healthPowerup")
        self.powerupSound = bs.getSound("powerup01")
        self.powerdownSound = bs.getSound("powerdown01")
        self.dropSound = bs.getSound("boxDrop")
        self.superStarSound = bs.getSound("ooh") #for superstar

        # material for powerups
        self.powerupMaterial = bs.Material()

        # material for anyone wanting to accept powerups
        self.powerupAcceptMaterial = bs.Material()

        # pass a powerup-touched message to applicable stuff
        self.powerupMaterial.addActions(
            conditions=(("theyHaveMaterial",self.powerupAcceptMaterial)),
            actions=(("modifyPartCollision","collide",True),
                     ("modifyPartCollision","physical",False),
                     ("message","ourNode","atConnect",_TouchedMessage())))
                     
        self.powerupMaterial.addActions(actions=( ("modifyPartCollision","friction",0.75)))
        self.powerupMaterial.addActions(conditions=("theyHaveMaterial",bs.getSharedObject('pickupMaterial')),
                                      actions=( ("modifyPartCollision","collide",True) ) )

        # we dont wanna be picked u

        self.powerupMaterial.addActions(
            conditions=("theyHaveMaterial",
                        bs.getSharedObject('footingMaterial')),
            actions=(("impactSound",self.dropSound,0.5,0.1)))

        self._powerupDist = []
        for p,freq in getDefaultPowerupDistribution():
            for i in range(int(freq)):
                self._powerupDist.append(p)
                
    def getRandomPowerupType(self,forceType=None,excludeTypes=[]):
        """
        Returns a random powerup type (string).
        See bs.Powerup.powerupType for available type values.

        There are certain non-random aspects to this; a 'curse' powerup,
        for instance, is always followed by a 'health' powerup (to keep things
        interesting). Passing 'forceType' forces a given returned type while
        still properly interacting with the non-random aspects of the system
        (ie: forcing a 'curse' powerup will result
        in the next powerup being health).
        """
        if forceType:
            t = forceType
        else:
            # if the last one was a curse, make this one a health to
            # provide some hope
            if self._lastPowerupType == 'curse':
                t = 'health'
            else:
                while True:
                    t = self._powerupDist[
                        random.randint(0, len(self._powerupDist)-1)]
                    if t not in excludeTypes:
                        break
        self._lastPowerupType = t
        return t
        
def getDefaultPowerupDistribution():
    if fire.modded_powerups:
        return fire.powerup_dist
    else:
        return fire.regular_dist
        
class Powerup(bs.Actor):#PCModder
    """
    category: Game Flow Classes

    A powerup box.
    This will deliver a bs.PowerupMessage to anything that touches it
    which has the bs.PowerupFactory.powerupAcceptMaterial applied.

    Attributes:

       powerupType
          The string powerup type.  This can be 'tripleBombs', 'punch',
          'iceBombs', 'impactBombs', 'landMines', 'stickyBombs', 'shield',
          'health', or 'curse'.

       node
          The 'prop' bs.Node representing this box.
    """

    def __init__(self,position=(0,1,0),powerupType='tripleBombs',expire=True):
        """
        Create a powerup-box of the requested type at the requested position.

        see bs.Powerup.powerupType for valid type strings.
        """
        
        bs.Actor.__init__(self)

        factory = self.getFactory()
        self.powerupType = powerupType;
        self._powersGiven = False
        self.portal = None
        mScl = 1

        if powerupType == 'tripleBombs': tex = factory.texBomb
        elif powerupType == 'punch': tex = factory.texPunch
        elif powerupType == 'iceBombs': tex = factory.texIceBombs
        elif powerupType == 'impactBombs': tex = factory.texImpactBombs
        elif powerupType == 'landMines': tex = factory.texLandMines
        elif powerupType == 'epicMine': tex = factory.texEpicMine
        elif powerupType == 'stickyBombs': tex = factory.texStickyBombs
        elif powerupType == 'shield': tex = factory.texShield
        elif powerupType == 'health': tex = factory.texHealth
        elif powerupType == 'curse': tex = factory.texCurse
        elif powerupType == 'sloMo': tex = factory.texSloMo
        elif powerupType == 'tnt': tex = factory.textnt
        elif powerupType == 'strongICE': tex = factory.texStrongICE
        elif powerupType == 'speedBoots': tex = factory.texSpeedBoots
        elif powerupType == 'champ': tex = factory.texChamp
        elif powerupType == 'troll': tex = factory.texTroll
        elif powerupType == 'character': tex = factory.texCharacter
        elif powerupType == 'invisible': tex = factory.texInvisible
        elif powerupType == 'invincible': tex = factory.texInvincible
        elif powerupType == 'curseBomb': tex = factory.texcurseBomb
        elif powerupType == 'hybridBomb': tex = factory.texhybridBomb
        elif powerupType == 'iceImpact': tex = factory.texiceImpact
        elif powerupType == 'blastBomb': tex = factory.texBlastBomb
        elif powerupType == 'boomBomb': tex = factory.texboomBomb
        elif powerupType == 'revengeBomb': tex = factory.texrevengeBomb
        elif powerupType == 'multiBomb': tex = factory.texmultiBomb
        elif powerupType == 'tntExplode': tex = factory.textntExplode
        elif powerupType == "antiGrav": tex = factory.texAntiGrav
        elif powerupType == 'headache':tex = factory.texAche
        elif powerupType == 'radius':tex = factory.texRadius
        elif powerupType == 'spunch': tex = factory.texSpunch
        elif powerupType == 'night': tex = factory.texNight
        elif powerupType == 'atomBomb': tex = factory.texAtomBomb
        elif powerupType == 'jumpFly': tex = factory.texJumpFly
        elif powerupType == 'snoball': tex = factory.texSno
        elif powerupType == "blackHole": tex = factory.texBlackHole
        elif powerupType == "touchMe": tex = factory.texTouchMe
        elif powerupType == "impactShower": tex = factory.texImpactShower
        elif powerupType == "bubble": tex = factory.texBubble
        elif powerupType == "mag": tex = factory.texMag
        elif powerupType == "portal": tex = factory.texPortal
        elif powerupType == 'blast': tex = factory.texBlast
        elif powerupType == 'mix': tex = factory.texMix
        elif powerupType == 'knockBomb': tex = factory.texknockBomb
        elif powerupType == 'weedbomb': tex = factory.texweedbomb
        elif powerupType == 'gluebomb': tex = factory.texgluebomb
        elif powerupType == 'spazBomb': tex = factory.texspazBomb
        elif powerupType == 'martyrdom': tex = factory.texMartyrdom
        elif powerupType == 'superStar': tex = factory.texSuperStar
        elif powerupType == 'blaster': tex = factory.texBlaster
        elif powerupType == 'knock': tex = factory.texKnock
        elif powerupType == 'frozenBomb': tex = factory.texCrazy
        elif powerupType == 'portalBomb': tex = factory.texportalBomb
        elif powerupType == 'cursyBomb': tex = factory.texTouchMe
        elif powerupType == 'teleBomb': tex = factory.texTeleBomb
        elif powerupType == 'flyer': tex = factory.texFlyer
        elif powerupType == 'beachBall': tex = factory.texBeachBall
        elif powerupType == 'blastBot': tex = factory.texPuck
        elif powerupType == 'bomber': tex = factory.texBomber
        elif powerupType == 'pirateBot': tex = factory.texPirate
        elif powerupType == 'botSpawner': tex = factory.texBotSpawner
        elif powerupType == 'characterPicker': tex = factory.texCharacterPicker
        elif powerupType == 'colorPicker': tex = factory.texColorPicker
        elif powerupType == 'volcano': tex = factory.texVolcano
        elif powerupType == 'plsTouchMe': tex = factory.texPlsTouchMe
        elif powerupType == 'fireBomb': tex = factory.texfireBomb
        elif powerupType == 'powerup': tex = factory.texPowerup
        elif powerupType == 'iceMine': tex = factory.texIceMine
        elif powerupType == 'stickyIce': tex = factory.texStickyIce
        elif powerupType == 'shockWave': tex = factory.texShockWave
        elif powerupType == 'map': tex = factory.texPortal
        elif powerupType == 'curseShower': tex = factory.texCurse
        elif powerupType == 'spikeBomb': tex = factory.texShockWave; mScl = 0.0
        else: raise Exception("invalid powerupType: "+str(powerupType))

        if len(position) != 3: raise Exception("expected 3 floats for position")
        
        self.node = bs.newNode(
            'prop',
            delegate=self,
            attrs={'body':'crate',
                   'position':position,
                   'model':factory.model,
                   'lightModel':factory.modelSimple,
                   #'gravityScale':None
                   'colorTexture':tex,
                   'reflection':'powerup',
                   'reflectionScale':[1.0],
                   'materials':(factory.powerupMaterial,
                                bs.getSharedObject('objectMaterial'))})

        if powerupType =='spikeBomb':     
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.2, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.flash = bs.newNode("flash",
                        attrs={'position':self.node.position,
                               'size':0.7,
                               'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
            m.connectAttr('output', self.flash, 'position')
            bs.gameTimer(7000,self.flash.delete)  
            bs.animateArray(self.flash,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
                                              

        if fire.grav:
            self.node.gravityScale = 0
        prefixAnim = {0: (1, 0, 0), 250: (1, 1, 0), 250 * 2: (0, 1, 0), 250 * 3: (0, 1, 1), 250 * 4: (1, 0, 1),
                      250 * 5: (0, 0, 1), 250 * 6: (1, 0, 0)}
        color = (1,1,1)
        coler = ((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))        
        velocity=(0, 0, 0)      

        
        if fire.powIce:
            self._inv = bs.Timer(100, bs.Call(lambda self: bs.emitBGDynamics(
                    position = self.node.position,
                    count = 20, chunkType='ice',
                    scale=0.55, spread=0.6) if self.node.exists() else None, self), repeat = True)
                    
        if fire.powSplint:
            self._inv = bs.Timer(100, bs.Call(lambda self: bs.emitBGDynamics(
                    position = self.node.position,
                    count = 20, chunkType='splinter',
                    scale=0.55, spread=0.6) if self.node.exists() else None, self), repeat = True)
                    
        if fire.powSlime:#changed it to spark actually slime looks useless
            self._inv = bs.Timer(100, bs.Call(lambda self: bs.emitBGDynamics(
                    position = self.node.position,
                    count = 20, chunkType='spark',
                    scale=0.55, spread=0.6) if self.node.exists() else None, self), repeat = True)
                    
        if fire.powSweat:
            self._inv = bs.Timer(100, bs.Call(lambda self: bs.emitBGDynamics(
                    position = self.node.position,
                    count = 60, chunkType='sweat',
                    scale=2.0, spread=0.6) if self.node.exists() else None, self), repeat = True)
       
        if fire.powExplo:        
            explosion = bs.newNode("explosion", attrs={
                'position': self.node.position,
                'color': coler,
                'velocity': (velocity[0], max(-1.0, velocity[1]), velocity[2]),
                'radius': (1.3)})
        
        #bs.gameTimer(60,flash.delete)  
        if fire.flash:        
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.0, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.flash = bs.newNode("flash",
                        attrs={'position':self.node.position,
                               'size':0.7,
                               'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
            m.connectAttr('output', self.flash, 'position')
            bs.gameTimer(7000,self.flash.delete)  
            bs.animateArray(self.flash,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
                   
        if fire.powerupName:
            m = bs.newNode('math', owner=self.node, attrs={'input1': (0, 0.7, 0), 'operation': 'add'})
            self.node.connectAttr('position', m, 'input2')
            self.nodeText = bs.newNode('text',
                                       owner=self.node,
                                       attrs={'text': powerupType,
                                              'inWorld': True,
                                              'shadow': 1.0,
                                              'flatness': 1.0,
                                              'color': color,
                                              'scale': 0.0125,
                                              'hAlign': 'center'})
            m.connectAttr('output', self.nodeText, 'position')
            #bs.animate(self.nodeText, 'scale', {0: 0, 140: 0.16, 200: 0.01})
            if fire.animate:
                bs.animateArray(self.nodeText,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
                bs.emitBGDynamics(position=self.nodeText.position, velocity=self.node.position, count=75, scale=1.0, spread=1.3, chunkType='spark')
                                
        if fire.powerupShield:
            self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                           'position': (
                                                                               self.node.position[0],
                                                                               self.node.position[1],
                                                                               self.node.position[2] + 0.5),
                                                                           'radius': 1.2})
            self.node.connectAttr('position', self.nodeShield, 'position')
            #bs.animateArray(self.powerupShield,'gravityScale',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
            if fire.animate:
                bsUtils.animateArray(self.nodeShield, 'color', 3, prefixAnim, True)
            
        if fire.discoLights:
            self.nodeLight = bs.newNode('light',
                                        attrs={'position': self.node.position,
                                               'color': color,
                                               'radius': 0.25, #0.4 will make it nice and bright
                                               'volumeIntensityScale': 0.5})
            self.node.connectAttr('position', self.nodeLight, 'position') 
            bsUtils.animateArray(self.nodeLight, 'color', 3, prefixAnim, True)
            bs.animate(self.nodeLight, "intensity", {0:1.0, 1000:1.8, 2000:1.0}, loop = True)
            bs.gameTimer(8000,self.nodeLight.delete)  
            
        if fire.powerupTimer:
            self.powerupHurt = bs.newNode('shield', owner=self.node, attrs={'color':(1,1,1), 'radius':0.1, 'hurt':1, 'alwaysShowHealthBar':True})
            self.node.connectAttr('position',self.powerupHurt, 'position')
            bs.animate(self.powerupHurt, 'hurt', {0:0, defaultPowerupInterval-1000:1})

        # animate in..
        curve = bs.animate(self.node, "modelScale", {0: 0, 140: 1.6, 200: mScl})
        bs.gameTimer(200, curve.delete)

        if expire:
            bs.gameTimer(defaultPowerupInterval-2500,
                         bs.WeakCall(self._startFlashing))
            bs.gameTimer(defaultPowerupInterval-1000,
                         bs.WeakCall(self.handleMessage, bs.DieMessage()))
                         
    def delete_portal(self):
        if self.portal is not None and self.portal.exists():
            self.portal.delete()

    @classmethod
    def getFactory(cls):
        """
        Returns a shared bs.PowerupFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        if activity is None: raise Exception("no current activity")
        try: return activity._sharedPowerupFactory
        except Exception:
            f = activity._sharedPowerupFactory = PowerupFactory()
            return f
            
    def _startFlashing(self):
        if self.node.exists(): self.node.flashing = True
        
    def _flashBillboard(self,tex,spaz):
        spaz.node.billboardOpacity = 1.0
        spaz.node.billboardTexture = tex
        spaz.node.billboardCrossOut = False
        bs.animate(spaz.node,"billboardOpacity",{0:0.0,100:1.0,400:1.0,500:0.0})

    def _powerUpWearOffFlash(self,tex,spaz):
        if spaz.isAlive():
           spaz.node.billboardTexture = tex
           spaz.node.billboardOpacity = 1.0
           spaz.node.billboardCrossOut = True      
        
    def handleMessage(self, msg):
        self._handleMessageSanityCheck()

        if isinstance(msg, PowerupAcceptMessage):
            factory = self.getFactory()
            if self.powerupType == 'health':
                bs.playSound(factory.healthPowerupSound, 3,
                             position=self.node.position)
            bs.playSound(factory.powerupSound, 3, position=self.node.position)
            self._powersGiven = True
            self.handleMessage(bs.DieMessage())

        elif isinstance(msg, _TouchedMessage):
            if not self._powersGiven:
                node = bs.getCollisionInfo("opposingNode")
                if node is not None and node.exists():
                    if fire.lightning: # #light node done by me concept by esie-eyen and patronmodz
                        self.light = bs.newNode('light',
                        attrs={'position':self.node.position,
                               'color':(1.2,1.2,1.4),
                               'volumeIntensityScale': 2.35})
                        bs.animate(self.light,'intensity',{0:0,70:0.5,350:0},loop=False)
                        bs.gameTimer(500,self.light.delete)
                        
                    if self.powerupType == "volcano":
                        spaz=node.getDelegate()
                        self.volcano = bsSomething.Volcano(position=self.node.position, player=node.getDelegate().getPlayer())
                        self.volcano.erupt()
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                    elif self.powerupType == 'superStar':
                        self._powersGiven = True#mythB
                        spaz = node.getDelegate()
                        if spaz.isAlive():
                           bs.shakeCamera(1)
                           bsUtils.PopupText("Surprise!",color=(1,1,1),
                                                         scale=0.9,
                                                         offset=(0,-1,0),
                                                         position=(spaz.node.position[0],spaz.node.position[1]-1,spaz.node.position[2])).autoRetain()
                          # bs.playSound(bs.Powerup.getFactory().surpriseSound,position=spaz.node.position)
                           bs.emitBGDynamics(position=spaz.node.position,
                                             velocity=(0,1,0),
                                             count=random.randrange(30,70),scale=0.5,chunkType='spark')
                           spaz.node.handleMessage("knockout",3000)
                           spaz.node.handleMessage("impulse",spaz.node.position[0],spaz.node.position[1],spaz.node.position[2],
                                                           -spaz.node.velocity[0],-spaz.node.velocity[1],-spaz.node.velocity[2],
                                                           400,400,0,0,-spaz.node.velocity[0],-spaz.node.velocity[1],-spaz.node.velocity[2])
                        if self._powersGiven == True :                                                           
                           self.handleMessage(bs.DieMessage())
                    elif self.powerupType == 'portal':
                        t = bsSpaz.gPowerupWearOffTime
                        if self.node.position in objs.lastpos:
                            self.portal = objs.Portal(position1=None, r=0.9,
                                                      color=(random.random(), random.random(), random.random()),
                                                      activity=bs.getActivity())
                            bs.gameTimer(t, bs.Call(self.delete_portal))
                        else:
                            m = self.node.position
                            objs.lastpos.append(m)
                            self.portal = objs.Portal(position1=self.node.position, r=0.9,
                                                      color=(random.random(), random.random(), random.random()),
                                                      activity=bs.getActivity())
                            bs.gameTimer(t, bs.Call(self.delete_portal))
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        bsUtils.PopupText("TheGreat",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    elif self.powerupType == 'blaster':#bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'atomBomb').autoRetain()
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'blastBomb').autoRetain()
                        bs.Bomb((p[0]-0.43,p[1]+2,p[2]-0.25),velocity=(0,-6,0),bombType = 'blastBomb').autoRetain()
                        bs.Bomb((p[0],p[1]+4,p[2]+0.5),velocity=(0,-6,0),bombType = 'blastBomb').autoRetain()
                    elif self.powerupType == 'knock':
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'knockBomb').autoRetain()
                        bs.Bomb((p[0]-0.43,p[1]+2,p[2]-0.25),velocity=(0,-6,0),bombType = 'knockBomb').autoRetain()
                        bs.Bomb((p[0],p[1]+4,p[2]+0.5),velocity=(0,-6,0),bombType = 'knockBomb').autoRetain()
                    elif self.powerupType == 'touchMe':
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        bsSomething.Something((p[0],p[1]+2,p[2])).autoRetain()  
                        bsUtils.PopupText("Dimitry",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()
                    elif self.powerupType == 'map':
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        import bsMap
                        m = 'BridgitMap'
                        bsMap.ThePadMap().__init__()
                    elif self.powerupType == 'martyrdom':
                        spaz = node.getDelegate()
                        tex = bs.Powerup.getFactory().texSpunch
                        self._flashBillboard(tex,spaz)
                        def checkDead(): #FIXME
                         if spaz.hitPoints <= 0 and  ((spaz.lastPlayerHeldBy is not None
                            and spaz.lastPlayerHeldBy.exists()) or (spaz.lastPlayerAttackedBy is not None
                            and spaz.lastPlayerAttackedBy.exists() and bs.getGameTime() - spaz.lastAttackedTime < 4000)):
                            try: spaz.lastDeathPos = spaz.node.position #FIXME
                            except Exception: 
                                spaz.dropss = None
                            else: 
                               if not spaz.lastPlayerAttackedBy == spaz.getPlayer():
                                  dropBomb()
                                  spaz.dropss = None
                        def dropBomb():
                               #bs.playSound(bs.Powerup.getFactory().martyrdomSound,position=spaz.lastDeathPos)
                               drop0 = bs.Bomb(position=(spaz.lastDeathPos[0]+0.43,spaz.lastDeathPos[1]+4,spaz.lastDeathPos[2]-0.25),
                                            velocity=(0,-6,0),sourcePlayer=spaz.getPlayer(),#some math for perfect triangle
                                            bombType='sticky').autoRetain()
                               drop1 = bs.Bomb(position=(spaz.lastDeathPos[0]-0.43,spaz.lastDeathPos[1]+4,spaz.lastDeathPos[2]-0.25),
                                            velocity=(0,-6,0),sourcePlayer=spaz.getPlayer(),
                                            bombType='sticky').autoRetain()
                               drop2 = bs.Bomb(position=(spaz.lastDeathPos[0],spaz.lastDeathPos[1]+4,spaz.lastDeathPos[2]+0.5),
                                            velocity=(0,-6,0),sourcePlayer=spaz.getPlayer(),
                                            bombType='sticky').autoRetain()                                       
                        def checkVal(val):
                            self._powersGiven = True
                            if val and spaz.isAlive():
                               m = bs.newNode('math', owner=spaz, attrs={ 'input1':(0, 1.3, 0),
                                                                               'operation':'add' })
                               spaz.node.connectAttr('torsoPosition', m, 'input2')
                               activatedText = bsUtils.PopupText("ACTIVATED",color=(1,1,1),
                                                                   scale=0.7,
                                                                   offset=(0,-1,0)).autoRetain()
                               m.connectAttr('output', activatedText.node, 'position')
                               bsUtils.PopupText("MythB",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                               #bs.playSound(bs.Powerup.getFactory().martyrdomPickSound,position=spaz.node.position)
                               spaz.isDropped = True
                               spaz.dropss = bs.Timer(1,bs.Call(checkDead),repeat=True)
                        checkVal(True)
                        if self._powersGiven == True :
                           self.handleMessage(bs.DieMessage())
                    elif self.powerupType == 'bubble':
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        pos = self.node.position
                        bsUtils.PopupText("Froshlee14",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                        newObjects.Puas(position=(pos[0]-1,pos[1]+2,pos[2]),velocity=(random.randint(-6,6),5,random.randint(-6,6)),owner=self.node,sourcePlayer=self.node).autoRetain()
                        newObjects.Puas(position=(pos[0]+1,pos[1]+2,pos[2]),velocity=(random.randint(-6,6),5,random.randint(-6,6)),owner=self.node,sourcePlayer=self.node).autoRetain()                        
                    elif self.powerupType == "tnt":
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'tnt').autoRetain()  
                        #bsUtils.PopupText("TNT",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                    elif self.powerupType == "atomBomb":
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'atomBomb').autoRetain()  
                    elif self.powerupType == "tntExplode":
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'tnt').autoRetain()  
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'tnt').autoRetain()  
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'impact').autoRetain()  
                       # bsUtils.PopupText("TNT",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                    elif self.powerupType == "strongICE":
                        p = node.positionForward
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())    
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'ice').autoRetain()  
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'ice').autoRetain() 
                        bs.Bomb((p[0]+0.43,p[1]+4,p[2]-0.25),velocity=(0,-6,0),bombType = 'ice').autoRetain()     
                        #bsUtils.PopupText("ICY",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                    elif self.powerupType == "invincible":
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())            
            	        node.invincible = True         
                        def _inv():
                            node.invincible = False 
                        bs.gameTimer(8000,bs.Call(_inv)) 
                    elif self.powerupType == "speedBoots":
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())            
            	        node.hockey = True         
                        #bsUtils.PopupText("Speed away",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                    elif self.powerupType == 'snoball':
                        spaz = node.getDelegate()
                        SnoBallz.snoBall().getFactory().giveBallz(spaz)
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())
                    elif self.powerupType == "character":
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())      
                        node.color = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))
                        node.highlight = ((0+random.random()*6.5),(0+random.random()*6.5),(0+random.random()*6.5))  
                        node.nameColor = ((0+random.random()*1.5),(0+random.random()*1.5),(0+random.random()*1.5))       
                        #node.name += random.choice(['\nTHE BOSS','\nNOOB','\nPRO','\nKill Me','\nNooby'])  #extra
                        testingEvent = 0

                        event = random.randint(1,6) if testingEvent == 0 else testingEvent
                        print 'Thanks to Oore and PatronModz: ' + str(event) 

                        if event in [1]:                        
                            node.colorTexture = bs.getTexture('frostyColor')
                            node.colorMaskTexture = bs.getTexture('frostyColorMask')
                            node.headModel = bs.getModel('frostyHead')
                            node.upperArmModel = bs.getModel('kronkUpperArm')
                            node.torsoModel = bs.getModel('frostyTorso')
                            node.pelvisModel = bs.getModel('frostyPelvis')
                            node.foreArmModel = bs.getModel('frostyForeArm')
                            node.handModel = bs.getModel('frostyHand')
                            node.upperLegModel = bs.getModel('frostyUpperLeg')
                            node.lowerLegModel = bs.getModel('frostyLowerLeg')
                            node.toesModel = bs.getModel('frostyToes')
                            node.style = 'frosty'       
                            bsUtils.PopupText("Frosty The Snowman",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain() 
                        elif event in [2]:         
                            node.colorTexture = bs.getTexture('santaColor')
                            node.colorMaskTexture = bs.getTexture('santaColorMask')      
                            node.headModel = bs.getModel('santaHead')
                            node.upperArmModel = bs.getModel('santaUpperArm')
                            node.torsoModel = bs.getModel('santaTorso')
                            node.pelvisModel = bs.getModel('kronkPelvis')
                            node.foreArmModel = bs.getModel('santaForeArm')
                            node.handModel = bs.getModel('santaHand')
                            node.upperLegModel = bs.getModel('santaUpperLeg')
                            node.lowerLegModel = bs.getModel('santaLowerLeg')
                            node.toesModel = bs.getModel('santaToes')
                            node.style = 'santa'
                            bsUtils.PopupText("SANTA",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()    
                        elif event in [3]:           
                            node.colorTexture = bs.getTexture('wizardColor')
                            node.colorMaskTexture = bs.getTexture('wizardColorMask')                
                            node.headModel = bs.getModel('wizardHead')
                            node.upperArmModel = bs.getModel('wizardUpperArm')
                            node.torsoModel = bs.getModel('wizardTorso')
                            node.pelvisModel = bs.getModel('wizardPelvis')
                            node.foreArmModel = bs.getModel('wizardForeArm')
                            node.handModel = bs.getModel('wizardHand')
                            node.upperLegModel = bs.getModel('wizardUpperLeg')
                            node.lowerLegModel = bs.getModel('wizardLowerLeg')
                            node.toesModel = bs.getModel('wizardToes')
                            node.style = 'wizard'
                            bsUtils.PopupText("EVIL SCEPTER WIZARD MAN",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()   
                        elif event in [4]:           
                            node.colorTexture = bs.getTexture('pixieColor')
                            node.colorMaskTexture = bs.getTexture('pixieColorMask')                
                            node.headModel = bs.getModel('pixieHead')
                            node.upperArmModel = bs.getModel('pixieUpperArm')
                            node.torsoModel = bs.getModel('pixieTorso')
                            node.pelvisModel = bs.getModel('pixiePelvis')
                            node.foreArmModel = bs.getModel('pixieForeArm')
                            node.handModel = bs.getModel('pixieHand')
                            node.upperLegModel = bs.getModel('pixieUpperLeg')
                            node.lowerLegModel = bs.getModel('pixieLowerLeg')
                            node.toesModel = bs.getModel('pixieToes')
                            node.style = 'pixie'
                            bsUtils.PopupText("PIXIEL-ATED",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()   
                        elif event in [5]:           
                            node.colorTexture = bs.getTexture('cyborgColor')
                            node.colorMaskTexture = bs.getTexture('cyborgColorMask')                
                            node.headModel = bs.getModel('cyborgHead')
                            node.upperArmModel = bs.getModel('cyborgUpperArm')
                            node.torsoModel = bs.getModel('cyborgTorso')
                            node.pelvisModel = bs.getModel('cyborgPelvis')
                            node.foreArmModel = bs.getModel('cyborgForeArm')
                            node.handModel = bs.getModel('cyborgHand')
                            node.upperLegModel = bs.getModel('cyborgUpperLeg')
                            node.lowerLegModel = bs.getModel('cyborgLowerLeg')
                            node.toesModel = bs.getModel('cyborgToes')
                            node.style = 'cyborg'
                            bsUtils.PopupText("The Robo",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()    
                        elif event in [6]:    
                            node.colorTexture = bs.getTexture('ninjaColor')
                            node.colorMaskTexture = bs.getTexture('ninjaColorMask')                
                            node.headModel = bs.getModel('ninjaHead')
                            node.upperArmModel = bs.getModel('ninjaUpperArm')
                            node.torsoModel = bs.getModel('ninjaTorso')
                            node.pelvisModel = bs.getModel('ninjaPelvis')
                            node.foreArmModel = bs.getModel('ninjaForeArm')
                            node.handModel = bs.getModel('ninjaHand')
                            node.upperLegModel = bs.getModel('ninjaUpperLeg')
                            node.lowerLegModel = bs.getModel('ninjaLowerLeg')
                            node.toesModel = bs.getModel('ninjaToes')
                            node.style = 'ninja'
                            node.nameColor = (0,0,0)
                            node.color = (0,0,0)
                            node.highlight = (0,0,0)
                            bsUtils.PopupText("PC||Modder",color=(1,1,1),scale=1.5,position=self.node.position).autoRetain()                             
                    elif self.powerupType == "invisible":
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())      
                        node.name = ' '
                        node.style = 'agent'
                        node.headModel = None
                        node.torsoModel = None
                        node.pelvisModel = None
                        node.upperArmModel = None
                        node.foreArmModel = None
                        node.handModel = None
                        node.upperLegModel = None
                        node.lowerLegModel = None
                        node.toesModel = None      
                        #bsUtils.PopupText("Invisible",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()                                
                    elif self.powerupType == "troll":
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())            
                        node.handleMessage(bs.FreezeMessage())      
                        node.handleMessage(bs.FreezeMessage())      
                        node.handleMessage(bs.PowerupMessage(powerupType='curse'))
                        #bsUtils.PopupText("TRoLL",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                    elif self.powerupType == "champ":
                        self._powersGiven = True
                        self.handleMessage(bs.DieMessage())            
                        node.handleMessage(bs.PowerupMessage(powerupType = 'punch'))
                        node.handleMessage(bs.PowerupMessage(powerupType = 'shield'))
                        #bsUtils.PopupText("Champ",color=(1,2,1),scale=1.5,position=self.node.position).autoRetain()
                    else:
                        node.handleMessage(PowerupMessage(self.powerupType, sourceNode=self.node))

        elif isinstance(msg, bs.DieMessage):
            if self.node.exists():
                if (msg.immediate):
                    self.node.delete()
                else:
                    curve = bs.animate(self.node, "modelScale", {0:1,100:0})
                    bs.gameTimer(100, self.node.delete)
                    if fire.flash:
                        bs.gameTimer(100, self.flash.delete)
                    if fire.discoLights:
                        bs.gameTimer(100,self.nodeLight.delete)
                    if fire.powerupTimer:
                        bs.gameTimer(100, self.powerupHurt.delete)

        elif isinstance(msg ,bs.OutOfBoundsMessage):
            self.handleMessage(bs.DieMessage())

        elif isinstance(msg, bs.HitMessage):
            # dont die on punches (thats annoying)
            if msg.hitType != 'punch':
                self.handleMessage(bs.DieMessage())
        else:
            bs.Actor.handleMessage(self, msg)
            
#enjoy this my friends. Do give some credit and have a great day. :) its open sourced as well

bsPowerup.PowerupFactory = PowerupFactory
bsPowerup.Powerup = Powerup
bsPowerup.getDefaultPowerupDistribution = getDefaultPowerupDistribution
bsPowerup._TouchedMessage = _TouchedMessage