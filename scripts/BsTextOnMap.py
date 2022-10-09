#MadeBySobyDamn
import bs
from bsMap import *
import bsMap
import bsInternal
import json
import cmdsetg
import time
import settings

num = 0

def __init__(self, vrOverlayCenterOffset=None):
        """
        Instantiate a map.
        """
        import bsInternal
        bs.Actor.__init__(self)
        self.preloadData = self.preload(onDemand=True)
        def text():
                #bySoby
                t = bs.newNode('text',
                       attrs={ 'text':u'You can only dance around destiny for so long\n until fate pulls you in',
                              'scale':1,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':1.2,
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                bs.gameTimer(7000,t.delete)
                ##
                t = bs.newNode('text',
                       attrs={ 'text':u'Welcome to the server by PCModder and Vivek!',
                              'scale':1.3,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':0.0,
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{8500: 0.0,9000: 1.0,14500: 1.0,15000: 0.0})
                bs.gameTimer(15000,t.delete)
                #bySoby
                t = bs.newNode('text',
                       attrs={ 'text':u'Happiness is not by chance but by choice',
                              'scale':1,
                              'maxWidth':0,
                              'position':(0,138),
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'shadow':0.5,
                              'flatness':1.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{17500: 0.0,18500: 1.0,24500: 1.0,25000: 0.0})
                bs.gameTimer(25000,t.delete)
                #bySoby..............................Dont Edit This
                t = bs.newNode('text',
                       attrs={ 'text':u'Kindness is a language which the deaf can hear \n and the blind can see',
                              'scale':1.2,
                              'maxWidth':0,
                              'position':(0,139),
                              'shadow':0.5,
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'flatness':0.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{27000: 0.0,27500: 1.0,33500: 1.0,34000: 0.0})
                bs.gameTimer(34000,t.delete)
                t = bs.newNode('text',
                       attrs={ 'text':u'Respect others and play well \n No teaming',
                              'scale':0.8,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':1.0,
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{36000: 0.0,36500: 1.0,42500: 1.0,43000: 0.0})
                bs.gameTimer(43000,t.delete)
                ##
                t = bs.newNode('text',
                       attrs={ 'text':u'Today is the tomorrow you spoke of yesterday',
                               'scale': 1,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':1.0,
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{45000: 0.0,45500: 1.0,50500: 1.0,51000: 0.0})
                bs.gameTimer(51000,t.delete)
        bs.gameTimer(3500,bs.Call(text))
        bs.gameTimer(56000,bs.Call(text),repeat = True)
        import fire
        if fire.stats_shower:
         def stats_shower():
          try:
            global num
            global scr
            p_list = []
            n_list = []
            s_list = []
            s_itr = iter(s_list)
            for i in bsInternal._getForegroundHostSession().players:
                Name = i.getName()
                n_list.append(Name)
                pb_id = i.get_account_id()
                p_list.append(pb_id)
            f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "r")
            stats = json.loads(f.read())
            for p in range(int(len(p_list))):
                if p_list[p] in stats:
                    player_stat = stats[str(p_list[p])]
                    s_msg = str(n_list[p].encode("utf-8"))+"'s Stats This Season:\n"+"Rank "+str(player_stat["rank"])+", "+str(player_stat["scores"]) + " scores, " + str(player_stat["kills"]) + " kills, " + str(player_stat["deaths"]) + " deaths."
                    s_list.append(s_msg)
                else:
                    s_msg = str((n_list[p].encode("utf-8")))+"Is not Registered"
                    s_list.append(s_msg)
            t = bs.newNode('text',
                       attrs={ 'text':s_list[num],
                              'scale':1.0,
                              'maxWidth':0,
                              'position':(250,650),
                              'shadow':0.5,
                              'flatness':1.0,
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'hAlign':'center',
                              'vAttach':'bottom'})
            bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
            bs.gameTimer(7000,t.delete)
            p = bs.newNode('text',
                       attrs={ 'text':cmdsetg.credit,
                              'scale':1.0,
                              'maxWidth':0,
                              'position':(-100,50),
                              'shadow':0.5,
                              'flatness':1.0,
                              'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                              'hAlign':'center',
                              'vAttach':'bottom'})
            bs.animate(p,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
            bs.gameTimer(7000,p.delete)
            if num < len(s_list):
                num+= 1
            if num == len(s_list):
                num*= 0
            if num > len(s_list):
                num*= 0
          except:
           pass
         bs.gameTimer(3000,bs.Call(stats_shower))
         bs.gameTimer(10000,bs.Call(stats_shower),repeat = True)

        vrMode = bs.getEnvironment()['vrMode']

        if not bs.getEnvironment().get('toolbarTest',True):
            self.modpack = bs.NodeActor(bs.newNode('text',
                                                  attrs={'vAttach':'bottom',
                                                         'hAttach':'right',
                                                         'hAlign':'right',
                                                         'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),
                                                         'flatness':1.0,
                                                         'shadow':1.0,
                                                         'scale':0.85,
                                                         'position':(-50,5),
                                                         'text':u'\ue048PCModder\ue048'}))    #adjust per name

        if settings.floater:
         if fire.pcfloater:
            def path():
                try:
                    self.flash = bs.newNode("flash",
                                attrs={'position':"position",
                                       'size':1.5,
                                       'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
                    bs.animateArray(self.flash,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
                    bsUtils.animateArray(self.flash,"position",3,{0:(1.830377363, 4.228850685, 3.803988636),10000:(4.148493267, 4.429165244, -6.588618549),20000:(-5.422572086, 4.228850685, 2.803988636),25000:(-6.859406739, 4.429165244, -6.588618549),30000:(-6.859406739, 4.429165244, -6.588618549),35000:(3.148493267, 4.429165244, -6.588618549),40000:(1.830377363, 4.228850685, 2.803988636),45000:(-5.422572086, 4.228850685, 2.803988636),50000:(-5.422572086, 4.228850685, 2.803988636),55000:(1.830377363, 4.228850685, 2.803988636),60000:(3.148493267, 4.429165244, -6.588618549),70000:(1.830377363, 4.228850685, 2.803988636),75000:(3.148493267, 4.429165244, -6.588618549),80000:(-5.422572086, 4.228850685, 2.803988636),90000:(-6.859406739, 4.429165244, -6.588618549),95000:(-6.859406739, 4.429165244, -6.588618549)},loop = True)    

                    self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                              'position':"position",
                                                                              'radius': 1.5})
                    #bs.animateArray(self.nodeShield,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)    
                    bsUtils.animateArray(self.nodeShield,"position",3,{0:(1.830377363, 4.228850685, 3.803988636),10000:(4.148493267, 4.429165244, -6.588618549),20000:(-5.422572086, 4.228850685, 2.803988636),25000:(-6.859406739, 4.429165244, -6.588618549),30000:(-6.859406739, 4.429165244, -6.588618549),35000:(3.148493267, 4.429165244, -6.588618549),40000:(1.830377363, 4.228850685, 2.803988636),45000:(-5.422572086, 4.228850685, 2.803988636),50000:(-5.422572086, 4.228850685, 2.803988636),55000:(1.830377363, 4.228850685, 2.803988636),60000:(3.148493267, 4.429165244, -6.588618549),70000:(1.830377363, 4.228850685, 2.803988636),75000:(3.148493267, 4.429165244, -6.588618549),80000:(-5.422572086, 4.228850685, 2.803988636),90000:(-6.859406739, 4.429165244, -6.588618549),95000:(-6.859406739, 4.429165244, -6.588618549)},loop = True)                   
                except:
                    pass
            bs.gameTimer(100,bs.Call(path))    
         else:
            def path():
                try:
                    p = bs.newNode('prop', attrs={'position':"position",'body':'sphere','model':bs.getModel('frostyHead'),'colorTexture':bs.getTexture('frostyIcon'),'bodyScale':0.0,'reflection': 'powerup','density':9999999999999999,'reflectionScale': [1.0],'modelScale':4.0,'gravityScale':0,'shadowSize':0.0,'materials':[bs.getSharedObject('footingMaterial'),bs.getSharedObject('footingMaterial')]})
                    bsUtils.animateArray(p,"position",3,{0:(1.830377363, 4.228850685, 3.803988636),10000:(4.148493267, 4.429165244, -6.588618549),20000:(-5.422572086, 4.228850685, 2.803988636),25000:(-6.859406739, 4.429165244, -6.588618549),30000:(-6.859406739, 4.429165244, -6.588618549),35000:(3.148493267, 4.429165244, -6.588618549),40000:(1.830377363, 4.228850685, 2.803988636),45000:(-5.422572086, 4.228850685, 2.803988636),50000:(-5.422572086, 4.228850685, 2.803988636),55000:(1.830377363, 4.228850685, 2.803988636),60000:(3.148493267, 4.429165244, -6.588618549),70000:(1.830377363, 4.228850685, 2.803988636),75000:(3.148493267, 4.429165244, -6.588618549),80000:(-5.422572086, 4.228850685, 2.803988636),90000:(-6.859406739, 4.429165244, -6.588618549),95000:(-6.859406739, 4.429165244, -6.588618549)},loop = True)                
                except:
                    pass
            bs.gameTimer(100,bs.Call(path))
        
        # set some defaults
        bsGlobals = bs.getSharedObject('globals')
        # area-of-interest bounds
        aoiBounds = self.getDefBoundBox("areaOfInterestBounds")
        if aoiBounds is None:
            print 'WARNING: no "aoiBounds" found for map:',self.getName()
            aoiBounds = (-1,-1,-1,1,1,1)
        bsGlobals.areaOfInterestBounds = aoiBounds
        # map bounds
        mapBounds = self.getDefBoundBox("levelBounds")
        if mapBounds is None:
            print 'WARNING: no "levelBounds" found for map:',self.getName()
            mapBounds = (-30,-10,-30,30,100,30)
        bsInternal._setMapBounds(mapBounds)
        # shadow ranges
        try: bsGlobals.shadowRange = [
                self.defs.points[v][1] for v in 
                ['shadowLowerBottom','shadowLowerTop',
                 'shadowUpperBottom','shadowUpperTop']]
        except Exception: pass
        # in vr, set a fixed point in space for the overlay to show up at..
        # by default we use the bounds center but allow the map to override it
        center = ((aoiBounds[0]+aoiBounds[3])*0.5,
                  (aoiBounds[1]+aoiBounds[4])*0.5,
                  (aoiBounds[2]+aoiBounds[5])*0.5)
        if vrOverlayCenterOffset is not None:
            center = (center[0]+vrOverlayCenterOffset[0],
                      center[1]+vrOverlayCenterOffset[1],
                      center[2]+vrOverlayCenterOffset[2])
        bsGlobals.vrOverlayCenter = center
        bsGlobals.vrOverlayCenterEnabled = True
        self.spawnPoints = self.getDefPoints("spawn") or [(0,0,0,0,0,0)]
        self.ffaSpawnPoints = self.getDefPoints("ffaSpawn") or [(0,0,0,0,0,0)]
        self.spawnByFlagPoints = (self.getDefPoints("spawnByFlag")
                                  or [(0,0,0,0,0,0)])
        self.flagPoints = self.getDefPoints("flag") or [(0,0,0)]
        self.flagPoints = [p[:3] for p in self.flagPoints] # just want points
        self.flagPointDefault = self.getDefPoint("flagDefault") or (0,1,0)
        self.powerupSpawnPoints = self.getDefPoints("powerupSpawn") or [(0,0,0)]
        self.powerupSpawnPoints = \
            [p[:3] for p in self.powerupSpawnPoints] # just want points
        self.tntPoints = self.getDefPoints("tnt") or []
        self.tntPoints = [p[:3] for p in self.tntPoints] # just want points
        self.isHockey = False
        self.isFlying = False
        self._nextFFAStartIndex = 0
        
bsMap.Map.__init__ = __init__
