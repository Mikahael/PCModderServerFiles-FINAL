#MadeBySobyDamn
import bs
from bsMap import *
import bsMap
import random
import fire

def __init__(self, vrOverlayCenterOffset=None):
        """
        Instantiate a map.
        """
        import bsInternal
        bs.Actor.__init__(self)
        self.preloadData = self.preload(onDemand=True)
        color = True
        def text():
                #bySoby
                #PC||Modder was here as well
                t = bs.newNode('text',
                       attrs={ 'text':u'Use verify for Verification! \n Use comp to complain!',
                              'scale':1.2,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':1.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{0: 0.0,500: 1.0,6500: 1.0,7000: 0.0})
                multiColor = {0:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))}
                if color:
                    bsUtils.animateArray(t,'color',3,multiColor,True)
                bs.gameTimer(7000,t.delete)
                ##
                t = bs.newNode('text',
                       attrs={ 'text':'Happiness is not by chance but by choice',
                              'scale':1.3,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':0.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{8500: 0.0,9000: 1.0,14500: 1.0,15000: 0.0})
                multiColor = {0:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))}
                if color:
                    bsUtils.animateArray(t,'color',3,multiColor,True)
                bs.gameTimer(15000,t.delete)
                #bySoby
                t = bs.newNode('text',
                       attrs={ 'text':'If one risks nothing, he risks more',
                              'scale':1.2,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':1.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{17500: 0.0,18500: 1.0,24500: 1.0,25000: 0.0})
                multiColor = {0:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))}
                if color:
                    bsUtils.animateArray(t,'color',3,multiColor,True)
                bs.gameTimer(25000,t.delete)
                #bySoby
                t = bs.newNode('text',
                       attrs={ 'text':u'Kindness is a language which the deaf can hear \n and the blind can see',
                              'scale':1.2,
                              'maxWidth':0,
                              'position':(0,139),
                              'shadow':0.5,
                              'flatness':0.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{27000: 0.0,27500: 1.0,33500: 1.0,34000: 0.0})
                multiColor = {0:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))}
                if color:
                    bsUtils.animateArray(t,'color',3,multiColor,True)
                bs.gameTimer(34000,t.delete)
                t = bs.newNode('text',
                       attrs={ 'text':'Respect others and play well \n No teaming',
                              'scale':1.2,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':1.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{36000: 0.0,36500: 1.0,42500: 1.0,43000: 0.0})
                multiColor = {0:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))}
                if color:
                    bsUtils.animateArray(t,'color',3,multiColor,True)
                bs.gameTimer(43000,t.delete)
                ##
                t = bs.newNode('text',
                       attrs={ 'text':'Welcome to server by PCModder',
                               'scale':1.2,
                              'maxWidth':0,
                              'position':(0,138),
                              'shadow':0.5,
                              'flatness':1.0,
                              'hAlign':'center',
                              'vAttach':'bottom'})
                bs.animate(t,'opacity',{45000: 0.0,45500: 1.0,50500: 1.0,51000: 0.0})
                multiColor = {0:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),1500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),2500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3000:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0)),3500:((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))}
                if color:
                    bsUtils.animateArray(t,'color',3,multiColor,True)
                bs.gameTimer(51000,t.delete)
        bs.gameTimer(3500,bs.Call(text))
        bs.gameTimer(56000,bs.Call(text),repeat = True)
        
        '''
        if fire.flashFloat:
            def path():
                self.flash = bs.newNode("flash",
                                attrs={'position':"position",
                                       'size':1.5,
                                       'color':((0+random.random()*1.0),(0+random.random()*1.0),(0+random.random()*1.0))})
                bs.animateArray(self.flash,'color',3,{0:(0,0,2),500:(0,2,0),1000:(2,0,0),1500:(2,2,0),2000:(2,0,2),2500:(0,1,6),3000:(1,2,0)},True)
                bsUtils.animateArray(self.flash,"position",3,{0:(1.830377363, 4.228850685, 3.803988636),10000:(4.148493267, 4.429165244, -6.588618549),20000:(-5.422572086, 4.228850685, 2.803988636),25000:(-6.859406739, 4.429165244, -6.588618549),30000:(-6.859406739, 4.429165244, -6.588618549),35000:(3.148493267, 4.429165244, -6.588618549),40000:(1.830377363, 4.228850685, 2.803988636),45000:(-5.422572086, 4.228850685, 2.803988636),50000:(-5.422572086, 4.228850685, 2.803988636),55000:(1.830377363, 4.228850685, 2.803988636),60000:(3.148493267, 4.429165244, -6.588618549),70000:(1.830377363, 4.228850685, 2.803988636),75000:(3.148493267, 4.429165244, -6.588618549),80000:(-5.422572086, 4.228850685, 2.803988636),90000:(-6.859406739, 4.429165244, -6.588618549),95000:(-6.859406739, 4.429165244, -6.588618549)},loop = True)    

                self.nodeShield = bs.newNode('shield', owner=self.node, attrs={'color': ((0+random.random()*6.0),(0+random.random()*6.0),(0+random.random()*6.0)),
                                                                           'position':"position",
                                                                           'radius': 1.5})
                bsUtils.animateArray(self.nodeShield,"position",3,{0:(1.830377363, 4.228850685, 3.803988636),10000:(4.148493267, 4.429165244, -6.588618549),20000:(-5.422572086, 4.228850685, 2.803988636),25000:(-6.859406739, 4.429165244, -6.588618549),30000:(-6.859406739, 4.429165244, -6.588618549),35000:(3.148493267, 4.429165244, -6.588618549),40000:(1.830377363, 4.228850685, 2.803988636),45000:(-5.422572086, 4.228850685, 2.803988636),50000:(-5.422572086, 4.228850685, 2.803988636),55000:(1.830377363, 4.228850685, 2.803988636),60000:(3.148493267, 4.429165244, -6.588618549),70000:(1.830377363, 4.228850685, 2.803988636),75000:(3.148493267, 4.429165244, -6.588618549),80000:(-5.422572086, 4.228850685, 2.803988636),90000:(-6.859406739, 4.429165244, -6.588618549),95000:(-6.859406739, 4.429165244, -6.588618549)},loop = True)                   
            bs.gameTimer(100,bs.Call(path))    
        else:
            def path():
                    p = bs.newNode('prop', attrs={'position':"position",'body':'sphere','model':bs.getModel('bombSticky'),'colorTexture':bs.getTexture('bombStickyColor'),'bodyScale':0.0,'reflection': 'powerup','density':9999999999999999,'reflectionScale': [1.0],'modelScale':4.0,'gravityScale':0,'shadowSize':0.0,'materials':[bs.getSharedObject('footingMaterial'),bs.getSharedObject('footingMaterial')]})
                    bsUtils.animateArray(p,"position",3,{0:(1.830377363, 4.228850685, 3.803988636),10000:(4.148493267, 4.429165244, -6.588618549),20000:(-5.422572086, 4.228850685, 2.803988636),25000:(-6.859406739, 4.429165244, -6.588618549),30000:(-6.859406739, 4.429165244, -6.588618549),35000:(3.148493267, 4.429165244, -6.588618549),40000:(1.830377363, 4.228850685, 2.803988636),45000:(-5.422572086, 4.228850685, 2.803988636),50000:(-5.422572086, 4.228850685, 2.803988636),55000:(1.830377363, 4.228850685, 2.803988636),60000:(3.148493267, 4.429165244, -6.588618549),70000:(1.830377363, 4.228850685, 2.803988636),75000:(3.148493267, 4.429165244, -6.588618549),80000:(-5.422572086, 4.228850685, 2.803988636),90000:(-6.859406739, 4.429165244, -6.588618549),95000:(-6.859406739, 4.429165244, -6.588618549)},loop = True)                

            bs.gameTimer(100,bs.Call(path))   
        ''' 

        vrMode = bs.getEnvironment()['vrMode']

        if not bs.getEnvironment().get('toolbarTest',True):
            self.modpack = bs.NodeActor(bs.newNode('text',
                                                  attrs={'vAttach':'bottom',
                                                         'hAttach':'right',
                                                         'hAlign':'right',
                                                         'color':((0+random.random()*4.5),(0+random.random()*4.5),(0+random.random()*4.5)),
                                                         'flatness':1.0,
                                                         'shadow':1.0,
                                                         'scale':0.85,
                                                         'position':(0,5),
                                                         'text':u'Owned by PCModder'}))    #adjust per name
        
        # set some defaults
        bsGlobals = bs.getSharedObject('globals')

        #better to do this way than in bsSpaz or spazPC
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