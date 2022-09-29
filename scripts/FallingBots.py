#Made by Froshlee14
import bs,random, bsSpaz, bsUtils
from bsSpaz import _PunchHitMessage

class NewPlayerSpaz(bs.PlayerSpaz):
    def handleMessage(self,m):
        if isinstance(m, bs.HitMessage):
            for p in bs.getActivity().players:
                if m.sourcePlayer == p: return
            super(self.__class__, self).handleMessage(m)
        else: super(self.__class__, self).handleMessage(m)

class FrostyBot(bsSpaz.SpazBot):
    character = 'Frosty'
    color = (0.5,0.5,1)
    highlight = (1,0.5,0)
    defaultBombType = 'ice'
    static = True
    defaultBombCount = 1
	
    def handleMessage(self,m):
        if isinstance(m, bs.FreezeMessage):pass
        else: super(self.__class__, self).handleMessage(m)
		
class FroshBot(bsSpaz.MelBot):
    color=(1,1,1)
    highlight=(0.2,1,1)
    character = 'Bernard'
    punchiness = 0.1
    throwDistMax = 0.9
    defaultBombType = 'landMine'
    defaultBombCount = 5
	
class CrazyBot(bsSpaz.MelBot):
    character = 'Taobao Mascot'
    throwRate = 4.0
    defaultBombCount = 5

    def handleMessage(self,m):
        super(self.__class__, self).handleMessage(m)
        self._color = bs.Timer(100,bs.WeakCall(self._changeColor),repeat=True)

    def _changeColor(self):
        if self.isAlive():
            self.node.color = (random.random()*2,random.random()*2,random.random()*2)
            self.bombType = random.choice(['ice','normal','sticky'])

class RobotBot(bsSpaz.ToughGuyBot):
    color=(0.5,0.5,0.5)
    highlight=(0,10,0)
    character = 'B-9000'
    run = True
    chargeSpeedMin = 0.3
    chargeSpeedMax = 1.0

class PascalBot(bsSpaz.SpazBot):
    color=(0,0,3)
    highlight=(0.2,0.2,1)
    character = 'Pascal'
    bouncy = True
    run = True
    punchiness = 0.8
    throwiness = 0.1
    chargeSpeedMin = 0.3
    chargeSpeedMax = 0.5

    def handleMessage(self,m):
        if isinstance(m, _PunchHitMessage):
            node = bs.getCollisionInfo("opposingNode")
            try: node.handleMessage(bs.FreezeMessage())
            except Exception: print('Cant freeze')
            bs.playSound(bs.getSound('freeze'))
            super(self.__class__, self).handleMessage(m)
        else: super(self.__class__, self).handleMessage(m)

class BugBot(bsSpaz.NinjaBot):
    character = 'Bones'
    throwiness = 0.4
    defaultBombType = 'tnt'

    def handleMessage(self,m):
        super(self.__class__, self).handleMessage(m)
        self._color = bs.Timer(200,bs.WeakCall(self._bug),repeat=True)

    def _bug(self):
        if self.isAlive():
            if self.run: self.node.run = 20

def bsGetAPIVersion():
    return 4

def bsGetGames():
    return [FallingBots]

class FallingBots(bs.TeamGameActivity):

    @classmethod
    def getName(cls):
        return 'Falling Bots'
    
    @classmethod
    def getDescription(cls,sessionType):
        return 'Better than meteor shower.'
		
    @classmethod
    def getScoreInfo(cls):
        return {'scoreName': 'Score',
                'scoreType': 'points'}

    @classmethod
    def getSupportedMaps(cls,sessionType):
        return ['Rampage']

    @classmethod
    def getSettings(cls,sessionType):
        return [
                ("Equip Boxing Gloves",{'default':True}),
                ("Equip Shield",{'default':False}),
                ("Max Bots",{'minValue':5,'maxValue':20,'default':6,'increment':1}),				
                ("Include melee bots",{'default':True}),
                ("Include bomber bots",{'default':True}),
                ("Include extra bots",{'default':True}),
                ("Epic Mode",{'default':False}),
                ("Time Limit",{'choices':[('None',0),('1 Minute',60),
                                        ('2 Minutes',120),('5 Minutes',300),
                                        ('10 Minutes',600),('20 Minutes',1200)],'default':0}),]
    
    @classmethod
    def supportsSessionType(cls,sessionType):
        return True if (issubclass(sessionType,bs.TeamsSession)
                        or issubclass(sessionType,bs.FreeForAllSession)
                        or issubclass(sessionType,bs.CoopSession)) else False

    def __init__(self,settings):
        bs.TeamGameActivity.__init__(self,settings)
        if self.settings['Epic Mode']: self._isSlowMotion = True
        self._scoreBoard = bs.ScoreBoard()
        self.announcePlayerDeaths = True
        self._lastPlayerDeathTime = None
        
    def onTransitionIn(self):
        bs.TeamGameActivity.onTransitionIn(self, music='Epic' if self.settings['Epic Mode'] else 'Survival')

    def onTeamJoin(self,team):
        team.gameData['score'] = 0
        if self.hasBegun(): self._updateScoreBoard()
		
    def onBegin(self):
        bs.TeamGameActivity.onBegin(self)
        self._updateScoreBoard()
        self._bots = bs.BotSet()

        delay = 4000
        for i in range(self.settings['Max Bots']):
            bPos = (-7.3+15.3*random.random(),10,-5.5+2.1*random.random())
            bs.gameTimer(delay,bs.Call(self._bots.spawnBot,self._getRandomBotType(),pos=bPos,spawnTime=0))
            delay += 300

    def _getRandomBotType(self):
        bt = [bs.BomberBot]
        melee = [bs.NinjaBot, bs.BunnyBot, PascalBot,RobotBot,bs.ToughGuyBot,]
        if self.settings['Include melee bots']:
            for bot in melee:
                bt.append(bot)
        bomber = [bs.ChickBot,bs.MelBot, bs.BomberBot,FrostyBot,CrazyBot,]
        if self.settings['Include bomber bots']:
            for bot in bomber:
                bt.append(bot)
        extra = [bs.PirateBot, BugBot,FroshBot,]
        if self.settings['Include extra bots']:
            for bot in extra:
                bt.append(bot)
        return (random.choice(bt))
		
    def onPlayerJoin(self, player):
        if self.hasBegun():
            bs.screenMessage(
                bs.Lstr(
                    resource='playerDelayedJoinText',
                    subs=[('${PLAYER}', player.getName(full=True))]),
                color=(0, 1, 0))
            return
        self.spawnPlayer(player)

    def onPlayerLeave(self, player):
        bs.TeamGameActivity.onPlayerLeave(self, player)
        self._checkEndGame()

    def spawnPlayer(self, player):
        position = self.getMap().getFFAStartPosition(self.players)
        angle = None
        name = player.getName()
        lightColor = bsUtils.getNormalizedColor(player.color)
        displayColor = bs.getSafeColor(player.color, targetIntensity=0.75)

        spaz = NewPlayerSpaz(color=player.color,
                             highlight=player.highlight,
                             character=player.character,
                             player=player)
        player.setActor(spaz)
        player.gameData['boxes'] = 0

        spaz.node.name = name
        spaz.node.nameColor = displayColor
        spaz.connectControlsToPlayer(enablePickUp=False)
        if self.settings['Equip Boxing Gloves']:
            spaz.equipBoxingGloves()
        if self.settings['Equip Shield']:
            spaz.equipShields()
		 
        spaz.playBigDeathSound = True
        self.scoreSet.playerGotNewSpaz(player, spaz)

        spaz.handleMessage(bs.StandMessage(position, angle if angle is not None else random.uniform(0, 360)))
        t = bs.getGameTime()
        bs.playSound(self._spawnSound, 1, position=spaz.node.position)
        light = bs.newNode('light', attrs={'color':lightColor})
        spaz.node.connectAttr('position', light, 'position')
        bsUtils.animate(light, 'intensity', {0:0, 250:1, 500:0})
        bs.gameTimer(500, light.delete)

    def handleMessage(self,m):

        if isinstance(m,bs.PlayerSpazDeathMessage):
            bs.TeamGameActivity.handleMessage(self,m)
            bs.gameTimer(1000,self._checkEndGame)
        elif isinstance(m,bs.SpazBotDeathMessage):
            pts,importance = m.badGuy.getDeathPoints(m.how)
            if m.killerPlayer is not None:
                try: target = m.badGuy.node.position
                except Exception: target = None
                try:
                    killerPlayer = m.killerPlayer
                    self.scoreSet.playerScored(killerPlayer,pts,target=target,kill=True,screenMessage=False,importance=importance)
                    killerPlayer.getTeam().gameData['score'] += pts
                    self._updateScoreBoard()
                except Exception: pass
            self._onSpazBotDied(m)
            bs.TeamGameActivity.handleMessage(self,m)
        else:
            bs.TeamGameActivity.handleMessage(self,m)
			
    def _onSpazBotDied(self,DeathMsg):
        bPos= (-7.3+15.3*random.random(),10,-5.5+2.1*random.random())
        self._bots.spawnBot(self._getRandomBotType(),pos=bPos,spawnTime=950)
        pos = DeathMsg.badGuy.node.position

    def _checkEndGame(self):
        livingTeamCount = 0
        for team in self.teams:
            for player in team.players:
                if player.isAlive():
                    livingTeamCount += 1
                    break
        if livingTeamCount <= 0: self.endGame()
		
    def _updateScoreBoard(self):
        for team in self.teams:
            self._scoreBoard.setTeamValue(team, team.gameData['score'])
 
    def endGame(self):
        results = bs.TeamGameResults()
        for t in self.teams: results.setTeamScore(t,t.gameData['score'])
        self.end(results=results)