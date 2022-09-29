# -*- coding: utf-8 -*-

import bs
import math

class BotFactory(object):
	
	def __init__(self):
		self.botModel = bs.getModel("impactBomb")
		self.botTexture = bs.getTexture("bg")
		self.targetSound = bs.getSound("activateBeep")
		self.popSound = bs.getSound("pop01")
	
class Bot(bs.Actor):
	
	def __init__(self, pos = (0, 1, 0), sourcePlayer = None):
		
		bs.Actor.__init__(self)
		
		factory = self.getFactory()

		self.targetSound = factory.targetSound
		self.popSound = factory.popSound
		
		if sourcePlayer is None:
			self.sourcePlayers = [bs.Player(None)]
		else:
                        self.sourcePlayers = [sourcePlayer]
		
		self.node = bs.newNode('prop', 
		delegate = self,
		attrs = {
			'body':'sphere',
			'position':pos,
			'velocity':(0, 0, 1), # Не менять на (0, 0, 0)!
			'model':factory.botModel,
			'colorTexture':factory.botTexture,
			'reflection':u'powerup',
			'reflectionScale':(10, 10, 0),
			'shadowSize':0.5,
			'extraAcceleration':(0, 20, 0),
                        'materials':[bs.getSharedObject("objectMaterial")]
		})
		bs.gameTimer(30000, bs.WeakCall(self.handleMessage, bs.DieMessage()))
		self._updTimer = bs.Timer(500, bs.WeakCall(self._update), repeat = True)
	
	def _update(self):
		minXDist = minYDist = minZDist = 999999
		mtx, mty, mtz = (0,0,0)
		xdist = ydist = zdist = 0
		ox, oy, oz = self.node.position
		for node in bs.getNodes():
			if node.getNodeType() == 'spaz':
                                if node.getDelegate() is None:
                                        continue
				if node.getDelegate().sourcePlayer in self.sourcePlayers:
					continue
				tx, ty, tz = node.position
				xdist = abs(tx - ox)
				ydist = abs(ty - oy)
				zdist = abs(tz - oz)
				if xdist < minXDist and ydist < minYDist and zdist < minZDist:
					minXDist, minYDist, minZDist = xdist, ydist, zdist
					ntx, nty, ntz = tx, ty, tz
		if minXDist > 8:
			return # Далеко(((
		if minYDist > 8:
			return # Далеко(((
		if minZDist > 8:
			return # Далеко(((
		self.getSourcePlayers()
		vel = [0, 0, 0]
		
		if ntx > ox:
			vel[0] = 5
		else:
			vel[0] = -5
		if nty > oy:
			vel[1] = 5
		else:
			vel[1] = -5
		if ntz > oz:
			vel[2] = 5
		else:
			vel[2] = -5
		bs.playSound(self.targetSound, position = self.node.position)
		bs.Blast(position = self.node.position,
                         hitType = 'punch',
                         sourcePlayer = self.sourcePlayers[0],
                         blastRadius = 1.2).autoRetain()
		self.node.velocity = vel
	
	def handleMessage(self, msg):
		if isinstance(msg, bs.DieMessage):
                        if not self.node.exists(): return
                        self._updTimer = None
                        bs.playSound(self.popSound, position = self.node.position)
			bs.PopupText("Goodbye!", position = self.node.position).autoRetain()
			self.node.delete()
		elif isinstance(msg, bs.OutOfBoundsMessage):
                        self.handleMessage(bs.DieMessage())
                else:
                        bs.Actor.handleMessage(self, msg)

        def getSourcePlayers(self):
                try:
                        self.sourcePlayers[0].getTeam()
                except Exception: # StandartError: invalid player
                        return # Если у нас bs.Player(None)
                
                # Мы же не хотим атаковать наших союзников?
                self.sourcePlayers = [self.sourcePlayers[0]]
                for team in bs.getActivity().teams:
                        if team is self.sourcePlayers[0].getTeam():
                                self.sourcePlayers += team.players
			
	@classmethod
	def getFactory(cls):
		activity = bs.getActivity()
		try: return activity._botFactory
		except Exception:
			activity._botFactory = f = BotFactory()
			return f
