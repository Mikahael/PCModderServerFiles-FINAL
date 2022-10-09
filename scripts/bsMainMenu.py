import bs
import bsUtils
import bsUI
import bsSpaz
import random
import time
import weakref
import bsInternal

gDidInitialTransition = False
gStartTime = time.time()
    
class MainMenuActivity(bs.Activity):

    def __init__(self, settings={}):
        bs.Activity.__init__(self,settings)

    def onTransitionIn(self):
        import bsInternal
        bs.Activity.onTransitionIn(self)
        global gDidInitialTransition
        random.seed(123)
        self._logoNode = None
        self._customLogoTexName = None
        self._wordActors = []
        env = bs.getEnvironment()
        
        # FIXME - shouldn't be doing things conditionally based on whether
        # the host is vr mode or not (clients may not be or vice versa) -
        # any differences need to happen at the engine level
        # so everyone sees things in their own optimal way
        vrMode = bs.getEnvironment()['vrMode']

        if not bs.getEnvironment().get('toolbarTest', True):
            self.myName = bs.NodeActor(bs.newNode('text', attrs={
                'vAttach':'bottom',
                'hAlign':'center',
                'color':(1.0,1.0,1.0,1.0) if vrMode else (0.5,0.6,0.5,0.6),
                'flatness':1.0,
                'shadow':1.0 if vrMode else 0.5,
                'scale':(0.9 if (env['interfaceType'] == 'small' or vrMode)
                         else 0.7), # FIXME need a node attr for this
                'position':(0,10),
                'vrDepth':-10,
                'text':u'\xa9 2018 Eric Froemling'}))
        
        # throw up some text that only clients can see so they know that the
        # host is navigating menus while they're just staring at an
        # empty-ish screen..
        self._hostIsNavigatingText = bs.NodeActor(bs.newNode('text', attrs={
            'text':bs.Lstr(resource='hostIsNavigatingMenusText',
                           subs=[('${HOST}',
                                  bsInternal._getAccountDisplayString())]),
            'clientOnly':True,
            'position':(0,-200),
            'flatness':1.0,
            'hAlign':'center'}))
        if not gDidInitialTransition and hasattr(self,'myName'):
            bs.animate(self.myName.node, 'opacity', {2300:0,3000:1.0})

        # TEMP - testing hindi text
        if False:
            # bs.screenMessage("TESTING: "+'TST: "deivit \xf0\x9f\x90\xa2"')
            self.tTest = bs.NodeActor(bs.newNode('text', attrs={
                'vAttach':'center',
                'hAlign':'left',
                'color':(1,1,1,1),
                'shadow':1.0,
                'flatness':0.0,
                'scale':1,
                'position':(-500,-40),
                'text':('\xe0\xa4\x9c\xe0\xa4\xbf\xe0\xa4\xb8 \xe0\xa4\xad'
                        '\xe0\xa5\x80 \xe0\xa4\x9a\xe0\xa5\x80\xe0\xa5\x9b '
                        '\xe0\xa4\x95\xe0\xa5\x8b \xe0\xa4\x9b\xe0\xa5\x81'
                        '\xe0\xa4\x8f\xe0\xa4\x81\xe0\xa4\x97\xe0\xa5\x87 '
                        '\xe0\xa4\x89\xe0\xa4\xb8\xe0\xa4\xb8\xe0\xa5\x87 '
                        '\xe0\xa4\x9a\xe0\xa4\xbf\xe0\xa4\xaa\xe0\xa4\x95'
                        '\n\xe0\xa4\x9c\xe0\xa4\xbe\xe0\xa4\xaf\xe0\xa5\x87'
                        '\xe0\xa4\x82\xe0\xa4\x97\xe0\xa5\x87 .. \xe0\xa4'
                        '\x87\xe0\xa4\xb8\xe0\xa4\x95\xe0\xa4\xbe \xe0\xa4'
                        '\xae\xe0\xa5\x9b\xe0\xa4\xbe \xe0\xa4\xb2\xe0\xa5'
                        '\x87\xe0\xa4\x82 !')}))
        # TEMP - test emoji
        if False:
            # bs.screenMessage("TESTING: "+'TST: "deivit \xf0\x9f\x90\xa2"')
            self.tTest = bs.NodeActor(bs.newNode('text', attrs={
                'vAttach':'center',
                'hAlign':'left',
                'color':(1,1,1,1),
                'shadow':1.0,
                'flatness':1.0,
                'scale':1,
                'position':(-500,-40),
                'text':('TST: "deivit \xf0\x9f\x90\xa2"')}))
        # TEMP - testing something; forgot what
        if False:
            # bs.screenMessage("TESTING: "+'TST: "deivit \xf0\x9f\x90\xa2"')
            self.tTest = bs.NodeActor(bs.newNode('text', attrs={
                'vAttach':'center',
                'hAlign':'left',
                'color':(1,1,1,1),
                'shadow':1.0,
                'flatness':0.0,
                'scale':1,
                'position':(-500,0),
                'text':u('        \u3147\u3147                             '
                         '            \uad8c\ucc2c\uadfc                   '
                         '                        \uae40\uc6d0\uc7ac\n     '
                         '   \ub10c                                        '
                         '    \uc804\uac10\ud638\nlll\u0935\u093f\u0936\u0947'
                         '\u0937 \u0927\u0928\u094d\u092f\u0935\u093e'
                         '\u0926:\n')}))
        # TEMP - test chinese text
        if False:
            self.tTest = bs.NodeActor(bs.newNode('text', attrs={
                'vAttach':'center',
                'hAlign':'center',
                'color':(1,1,1,1),
                'shadow':1.0,
                'flatness':0.0,
                'scale':1,
                'position':(-400,-40),
                'text':('TST: "\xe8\x8e\xb7\xe5\x8f\x96\xe6\x9b\xb4\xe5\xa4'
                        '\x9a\xe5\x9b\xbe\xe6\xa0\x87"\n\xe6\x88\x90\xe5'
                        '\xb0\xb1\xe4\xb8\xad|         foo\n\xe8\xb4\xa6'
                        '\xe6\x88\xb7 \xe7\x99\xbb\xe9\x99\x86foo\nend"'
                        '\xe8\x8e\xb7\xe5\x8f\x96\xe6\x9b\xb4\xe5\xa4\x9a'
                        '\xe5\x9b\xbe\xe6\xa0\x87"\nend"\xe8\x8e\xb7\xe5'
                        '\x8f\x96\xe6\x9b\xb4\xe5\xa4\x9a\xe5\x9b\xbe\xe6'
                        '\xa0\x87"\nend2"\xe8\x8e\xb7\xe5\x8f\x96\xe6\x9b'
                        '\xb4\xe5\xa4\x9a\xe5\x9b\xbe\xe6\xa0\x87"\n')}))

        # FIXME - shouldn't be doing things conditionally based on whether
        # the host is vr mode or not (clients may not be or vice versa)
        # - any differences need to happen at the engine level
        # so everyone sees things in their own optimal way
        vrMode = env['vrMode']
        interfaceType = env['interfaceType']

        # in cases where we're doing lots of dev work lets
        # always show the build number
        forceShowBuildNumber = False

        if not bs.getEnvironment().get('toolbarTest', True):
            if env['debugBuild'] or env['testBuild'] or forceShowBuildNumber:
                if env['debugBuild']:
                    text = bs.Lstr(value='${V} (${B}) (${D})',
                                   subs=[('${V}', env['version']),
                                         ('${B}', str(env['buildNumber'])),
                                         ('${D}',bs.Lstr(resource='debugText')
                                         )])
                else:
                    text = bs.Lstr(value='${V} (${B})',
                                   subs=[('${V}', env['version']),
                                         ('${B}', str(env['buildNumber']))])
            else:
                text = bs.Lstr(value='${V}', subs=[('${V}', env['version'])])
            self.version = bs.NodeActor(bs.newNode('text', attrs={
                'vAttach':'bottom',
                'hAttach':'right',
                'hAlign':'right',
                'flatness':1.0,
                'vrDepth':-10,
                'shadow':1.0 if vrMode else 0.5,
                'color':(1,1,1,1) if vrMode else (0.5,0.6,0.5,0.7),
                'scale':0.9 if (interfaceType == 'small' or vrMode) else 0.7,
                'position':(-260,10) if vrMode else (-10,10),
                'text':text}))
            if not gDidInitialTransition:
                bs.animate(self.version.node,'opacity',{2300:0,3000:1.0})
            
        # throw in beta info..
        self.betaInfo = self.betaInfo2 = None
        if env['testBuild'] and not env['kioskMode']:
            self.betaInfo = bs.NodeActor(bs.newNode('text', attrs={
                'vAttach':'center',
                'hAlign':'center',
                'color':(1,1,1,1),
                'shadow':0.5,
                'flatness':0.5,
                'scale':1,
                'vrDepth':-60,
                'position':(230,125) if env['kioskMode'] else (230,35),
                'text':bs.Lstr(resource='testBuildText')}))
            if not gDidInitialTransition:
                bs.animate(self.betaInfo.node,'opacity',{1300:0,1800:1.0})

        model = bs.getModel('thePadLevel')
        treesModel = bs.getModel('trees')
        bottomModel = bs.getModel('thePadLevelBottom')
        testColorTexture = bs.getTexture('thePadLevelColor')
        treesTexture = bs.getTexture('treesColor')
        bgTex = bs.getTexture('menuBG')
        bgModel = bs.getModel('thePadBG')

        # (load these last since most platforms don't use them..)
        vrBottomFillModel = bs.getModel('thePadVRFillBottom')
        vrTopFillModel = bs.getModel('thePadVRFillTop')
        
        bsGlobals = bs.getSharedObject('globals')
        bsGlobals.cameraMode = 'rotate'

        if False:
            node = bs.newNode('timeDisplay', attrs={
                'timeMin':2000,
                'timeMax':10000,
                'showSubSeconds':True})
            self._fooText = bs.NodeActor(bs.newNode('text', attrs={
                'position':(0,-220),
                'flatness':1.0,
                'hAlign':'center'}))
            bsGlobals.connectAttr('gameTime', node, 'time2')
            node.connectAttr('output', self._fooText.node, 'text')
        
        tint = (1.14, 1.1, 1.0)
        bsGlobals.tint = tint
            
        bsGlobals.ambientColor = (1.06, 1.04, 1.03)
        bsGlobals.vignetteOuter = (0.45, 0.55, 0.54)
        bsGlobals.vignetteInner = (0.99, 0.98, 0.98)

        self.bottom = bs.NodeActor(bs.newNode('terrain', attrs={
            'model':bottomModel,
            'lighting':False,
            'reflection':'soft',
            'reflectionScale':[0.45],
            'colorTexture':testColorTexture}))
        self.vrBottomFill = bs.NodeActor(bs.newNode('terrain', attrs={
            'model':vrBottomFillModel,
            'lighting':False,
            'vrOnly':True,
            'colorTexture':testColorTexture}))
        self.vrTopFill = bs.NodeActor(bs.newNode('terrain', attrs={
            'model':vrTopFillModel,
            'vrOnly':True,
            'lighting':False,
            'colorTexture':bgTex}))
        self.terrain = bs.NodeActor(bs.newNode('terrain', attrs={
            'model':model,
            'colorTexture':testColorTexture,
            'reflection':'soft',
            'reflectionScale':[0.3]}))
        self.trees = bs.NodeActor(bs.newNode('terrain', attrs={
            'model':treesModel,
            'lighting':False,
            'reflection':'char',
            'reflectionScale':[0.1],
            'colorTexture':treesTexture}))
        self.bg = bs.NodeActor(bs.newNode('terrain', attrs={
            'model':bgModel,
            'color':(0.92,0.91,0.9),
            'lighting':False,
            'background':True,
            'colorTexture':bgTex}))
        textOffsetV = 0
        self._ts = 0.86

        self._language = None
        self._updateTimer = bs.Timer(1000, self._update, repeat=True)
        self._update()

        # hopefully this won't hitch but lets space these out anyway..
        bsInternal._addCleanFrameCallback(bs.WeakCall(self._startPreloads))

        random.seed()

        # on the main menu, also show our news..
        class News(object):
            
            def __init__(self,activity):
                self._valid = True
                self._messageDuration = 10000
                self._messageSpacing = 2000
                self._text = None
                self._activity = weakref.ref(activity)
                # if we're signed in, fetch news immediately..
                # otherwise wait until we are signed in
                self._fetchTimer = bs.Timer(1000,
                                            bs.WeakCall(self._tryFetchingNews),
                                            repeat=True)
                self._tryFetchingNews()

            # we now want to wait until we're signed in before fetching news
            def _tryFetchingNews(self):
                if bsInternal._getAccountState() == 'SIGNED_IN':
                    self._fetchNews()
                    self._fetchTimer = None
                
            def _fetchNews(self):
                try: launchCount = bs.getConfig()['launchCount']
                except Exception: launchCount = None
                global gLastNewsFetchTime
                gLastNewsFetchTime = time.time()
                
                # UPDATE - we now just pull news from MRVs
                news = bsInternal._getAccountMiscReadVal('n', None)
                if news is not None:
                    self._gotNews(news)

            def _changePhrase(self):

                global gLastNewsFetchTime
                
                # if our news is way out of date, lets re-request it..
                # otherwise, rotate our phrase
                if time.time()-gLastNewsFetchTime > 600.0:
                    self._fetchNews()
                    self._text = None
                else:
                    if self._text is not None:
                        if len(self._phrases) == 0:
                            for p in self._usedPhrases:
                                self._phrases.insert(0,p)
                        val = self._phrases.pop()
                        if val == '__ACH__':
                            vr = bs.getEnvironment()['vrMode']
                            bsUtils.Text(
                                bs.Lstr(resource='nextAchievementsText'),
                                color=(1,1,1,1) if vr else (0.95,0.9,1,0.4),
                                hostOnly=True,
                                maxWidth=200,
                                position=(-300, -35),
                                hAlign='right',
                                transition='fadeIn',
                                scale=0.9 if vr else 0.7,
                                flatness=1.0 if vr else 0.6,
                                shadow=1.0 if vr else 0.5,
                                hAttach="center",
                                vAttach="top",
                                transitionDelay=1000,
                                transitionOutDelay=self._messageDuration)\
                                   .autoRetain()
                            import bsAchievement
                            achs = [a for a in bsAchievement.gAchievements
                                    if not a.isComplete()]
                            if len(achs) > 0:
                                a = achs.pop(random.randrange(min(4,len(achs))))
                                a.createDisplay(-180, -35, 1000,
                                                outDelay=self._messageDuration,
                                                style='news')
                            if len(achs) > 0:
                                a = achs.pop(random.randrange(min(8,len(achs))))
                                a.createDisplay(180, -35, 1250,
                                                outDelay=self._messageDuration,
                                                style='news')
                        else:
                            s = self._messageSpacing
                            keys = {s:0, s+1000:1.0,
                                    s+self._messageDuration-1000:1.0,
                                    s+self._messageDuration:0.0}
                            bs.animate(self._text.node, "opacity",
                                       dict([[k,v] for k,v in keys.items()]))
                            self._text.node.text = val

            def _gotNews(self, news):
                
                # run this stuff in the context of our activity since we need
                # to make nodes and stuff.. should fix the serverGet call so it 
                activity = self._activity()
                if activity is None or activity.isFinalized(): return
                with bs.Context(activity):
                
                    self._phrases = []
                    # show upcoming achievements in non-vr versions
                    # (currently too hard to read in vr)
                    self._usedPhrases = (
                        ['__ACH__'] if not bs.getEnvironment()['vrMode']
                        else []) + [s for s in news.split('<br>\n') if s != '']
                    self._phraseChangeTimer = bs.Timer(
                        self._messageDuration+self._messageSpacing,
                        bs.WeakCall(self._changePhrase), repeat=True)

                    sc = 1.2 if (bs.getEnvironment()['interfaceType'] == 'small'
                                 or bs.getEnvironment()['vrMode']) else 0.8

                    self._text = bs.NodeActor(bs.newNode('text', attrs={
                        'vAttach':'top',
                        'hAttach':'center',
                        'hAlign':'center',
                        'vrDepth':-20,
                        'shadow':1.0 if bs.getEnvironment()['vrMode'] else 0.4,
                        'flatness':0.8,
                        'vAlign':'top',
                        'color':((1, 1, 1, 1) if bs.getEnvironment()['vrMode']
                                 else (0.7, 0.65, 0.75, 1.0)),
                        'scale':sc,
                        'maxWidth':900.0/sc,
                        'position':(0,-10)}))
                    self._changePhrase()
                    
        if not env['kioskMode'] and not env.get('toolbarTest', True):
            self._news = News(self)

        # bring up the last place we were, or start at the main menu otherwise
        with bs.Context('UI'):
            try: mainWindow = bsUI.gMainWindow
            except Exception: mainWindow = None

            # when coming back from a kiosk-mode game, jump to
            # the kiosk start screen.. if bsUtils.gRunningKioskModeGame:
            if bs.getEnvironment()['kioskMode']:
                bsUI.uiGlobals['mainMenuWindow'] = \
                     bsUI.KioskWindow().getRootWidget()
            # ..or in normal cases go back to the main menu
            else:
                if mainWindow == 'Gather':
                    bsUI.uiGlobals['mainMenuWindow'] = \
                        bsUI.GatherWindow(transition=None).getRootWidget()
                elif mainWindow == 'Watch':
                    bsUI.uiGlobals['mainMenuWindow'] = \
                        bsUI.WatchWindow(transition=None).getRootWidget()
                elif mainWindow == 'Team Game Select':
                    bsUI.uiGlobals['mainMenuWindow'] = \
                        bsUI.TeamsWindow(sessionType=bs.TeamsSession,
                                         transition=None).getRootWidget()
                elif mainWindow == 'Free-for-All Game Select':
                    bsUI.uiGlobals['mainMenuWindow'] = \
                        bsUI.TeamsWindow(sessionType=bs.FreeForAllSession,
                                         transition=None).getRootWidget()
                elif mainWindow == 'Coop Select':
                    bsUI.uiGlobals['mainMenuWindow'] = \
                        bsUI.CoopWindow(transition=None).getRootWidget()
                else: bsUI.uiGlobals['mainMenuWindow'] = \
                    bsUI.MainMenuWindow(transition=None).getRootWidget()

                # attempt to show any pending offers immediately.
                # If that doesn't work, try again in a few seconds
                # (we may not have heard back from the server)
                # ..if that doesn't work they'll just have to wait
                # until the next opportunity.
                if not bsUI._showOffer():
                    def tryAgain():
                        if not bsUI._showOffer():
                            # try one last time..
                            bs.realTimer(2000, bsUI._showOffer)
                    bs.realTimer(2000, tryAgain)
            
        gDidInitialTransition = True

    def _update(self):

        # update logo in case it changes..
        if self._logoNode is not None and self._logoNode.exists():
            customTexture = self._getCustomLogoTexName()
            if customTexture != self._customLogoTexName:
                self._customLogoTexName = customTexture
                self._logoNode.texture = bs.getTexture(
                    customTexture if customTexture is not None else 'logo')
                self._logoNode.modelOpaque = (
                    None if customTexture is not None else bs.getModel('logo'))
                self._logoNode.modelTransparent = (
                    None if customTexture is not None
                    else bs.getModel('logoTransparent'))
        
        # if language has changed, recreate our logo text/graphics
        l = bs.getLanguage()
        if l != self._language:
            self._language = l
            env = bs.getEnvironment()
            y = 20
            gScale = 1.1
            self._wordActors = []
            baseDelay = 1000
            delay = baseDelay
            delayInc = 20

            # come on faster after the first time
            if gDidInitialTransition:
                baseDelay = 0
                delay = baseDelay
                delayInc = 20
                
            # we draw higher in kiosk mode (make sure to test this
            # when making adjustments) for now we're hard-coded for
            # a few languages.. should maybe look into generalizing this?..
            if bs.getLanguage() == 'Chinese':
                baseX = -270
                x = baseX-20
                spacing = 85*gScale
                yExtra = 0 if env['kioskMode'] else 0
                self._makeLogo(x-110+50, 113+y+1.2*yExtra, 0.34*gScale,
                               delay=baseDelay+100,
                               customTexture='chTitleChar1', jitterScale=2.0,
                               vrDepthOffset=-30)
                x += spacing
                delay += delayInc
                self._makeLogo(x-10+50, 110+y+1.2*yExtra, 0.31*gScale,
                               delay=baseDelay+150,
                               customTexture='chTitleChar2',
                               jitterScale=2.0, vrDepthOffset=-30)
                x += 2.0 * spacing
                delay += delayInc
                self._makeLogo(x+180-140, 110+y+1.2*yExtra, 0.3*gScale,
                               delay=baseDelay+250,
                               customTexture='chTitleChar3', jitterScale=2.0,
                               vrDepthOffset=-30)
                x += spacing
                delay += delayInc
                self._makeLogo(x+241-120, 110+y+1.2*yExtra, 0.31*gScale,
                               delay=baseDelay+300,
                               customTexture='chTitleChar4', jitterScale=2.0,
                               vrDepthOffset=-30)
                x += spacing; delay += delayInc
                self._makeLogo(x+300-90, 105+y+1.2*yExtra, 0.34*gScale,
                               delay=baseDelay+350,
                               customTexture='chTitleChar5', jitterScale=2.0,
                               vrDepthOffset=-30)
                self._makeLogo(baseX+155, 146+y+1.2*yExtra, 0.28*gScale,
                               delay=baseDelay+200, rotate=-7)
            else:
                baseX = -170
                x = baseX-20
                spacing = 55*gScale
                yExtra = 0 if env['kioskMode'] else 0

                x1 = x
                delay1 = delay
                for shadow in (True, False):
                    x = x1
                    delay = delay1
                    self._makeWord('B', x-50, y-23+0.8*yExtra, scale=1.3*gScale,
                                   delay=delay, vrDepthOffset=3, shadow=shadow)
                    x += spacing
                    delay += delayInc
                    self._makeWord('m', x, y+yExtra, delay=delay, scale=gScale,
                                   shadow=shadow)
                    x += spacing*1.25
                    delay += delayInc
                    self._makeWord('b', x, y+yExtra-10, delay=delay,
                                   scale=1.1*gScale, vrDepthOffset=5,
                                   shadow=shadow)
                    x += spacing*0.85
                    delay += delayInc
                    self._makeWord('S', x, y-25+0.8*yExtra, scale=1.35*gScale,
                                   delay=delay, vrDepthOffset=14, shadow=shadow)
                    x += spacing
                    delay += delayInc
                    self._makeWord('q', x, y+yExtra, delay=delay, scale=gScale,
                                   shadow=shadow)
                    x += spacing*0.9
                    delay += delayInc
                    self._makeWord('u', x, y+yExtra, delay=delay, scale=gScale,
                                   vrDepthOffset=7, shadow=shadow)
                    x += spacing*0.9
                    delay += delayInc
                    self._makeWord('a', x, y+yExtra, delay=delay, scale=gScale,
                                   shadow=shadow)
                    x += spacing*0.64
                    delay += delayInc
                    self._makeWord('d', x, y+yExtra-10, delay=delay,
                                   scale=1.1*gScale, vrDepthOffset=6,
                                   shadow=shadow)
                self._makeLogo(baseX-28, 125+y+1.2*yExtra, 0.32*gScale,
                               delay=baseDelay)

    def _makeWord(self, word, x, y, scale=1.0, delay=0,
                  vrDepthOffset=0, shadow=False):
        if shadow:
            wordShadowObj = bs.NodeActor(bs.newNode('text', attrs={
                'position':(x,y),
                'big':True,
                'color':(0.0,0.0,0.2,0.08),
                'tiltTranslate':0.09,
                'opacityScalesShadow':False,
                'shadow':0.2,
                'vrDepth':-130,
                'vAlign':'center',
                'projectScale':0.97*scale,
                'scale':1.0,
                'text':word}))
            self._wordActors.append(wordShadowObj)
        else:
            wordObj = bs.NodeActor(bs.newNode('text', attrs={
                'position':(x,y),
                'big':True,
                'color':(1.2,1.15,1.15,1.0),
                'tiltTranslate':0.11,
                'shadow':0.2,
                'vrDepth':-40+vrDepthOffset,
                'vAlign':'center',
                'projectScale':scale,
                'scale':1.0,
                'text':word}))
            self._wordActors.append(wordObj)

        # add a bit of stop-motion-y jitter to the logo
        # (unless we're in VR mode in which case its best to leave things still)
        if not bs.getEnvironment()['vrMode']:
            if not shadow:
                c = bs.newNode("combine", owner=wordObj.node, attrs={'size':2})
            else:
                c = None
            if shadow:
                c2 = bs.newNode("combine", owner=wordShadowObj.node,
                                attrs={'size':2})
            else:
                c2 = None
            if not shadow:
                c.connectAttr('output',wordObj.node,'position')
            if shadow:
                c2.connectAttr('output',wordShadowObj.node,'position')
            keys = {}
            keys2 = {}
            timeV = 0
            for i in range(10):
                val = x+(random.random()-0.5)*0.8
                val2 = x+(random.random()-0.5)*0.8
                keys[timeV*self._ts] = val
                keys2[timeV*self._ts] = val2+5
                timeV += random.random() * 100
            if c is not None:
                bs.animate(c, "input0", keys, loop=True)
            if c2 is not None:
                bs.animate(c2, "input0", keys2, loop=True)
            keys = {}
            keys2 = {}
            timeV = 0
            for i in range(10):
                val = y+(random.random()-0.5)*0.8
                val2 = y+(random.random()-0.5)*0.8
                keys[timeV*self._ts] = val
                keys2[timeV*self._ts] = val2-9
                timeV += random.random() * 100
            if c is not None: bs.animate(c,"input1",keys,loop=True)
            if c2 is not None: bs.animate(c2,"input1",keys2,loop=True)

        if not shadow:
            bs.animate(wordObj.node, "projectScale",
                       {delay:0.0, delay+100:scale*1.1, delay+200:scale})
        else:
            bs.animate(wordShadowObj.node, "projectScale",
                       {delay:0.0, delay+100:scale*1.1, delay+200:scale})
    def _getCustomLogoTexName(self):
        if bsInternal._getAccountMiscReadVal('easter',False):
            return 'logoEaster'
        else:
            return None
                
        
    # pop the logo and menu in
    def _makeLogo(self, x, y, scale, delay, customTexture=None, jitterScale=1.0,
                  rotate=0, vrDepthOffset=0):
        # temp easter googness
        if customTexture is None:
            customTexture = self._getCustomLogoTexName()
        self._customLogoTexName = customTexture
        logo = bs.NodeActor(bs.newNode('image', attrs={
            'texture': bs.getTexture(customTexture if customTexture is not None
                                     else 'logo'),
            'modelOpaque':(None if customTexture is not None
                           else bs.getModel('logo')),
            'modelTransparent':(None if customTexture is not None
                                else bs.getModel('logoTransparent')),
            'vrDepth':-10+vrDepthOffset,
            'rotate':rotate,
            'attach':"center",
            'tiltTranslate':0.21,
            'absoluteScale':True}))
        self._logoNode = logo.node
        self._wordActors.append(logo)
        # add a bit of stop-motion-y jitter to the logo
        # (unless we're in VR mode in which case its best to leave things still)
        if not bs.getEnvironment()['vrMode']:
            c = bs.newNode("combine", owner=logo.node, attrs={'size':2})
            c.connectAttr('output', logo.node, 'position')
            keys = {}
            timeV = 0
            # gen some random keys for that stop-motion-y look
            for i in range(10):
                keys[timeV] = x+(random.random()-0.5)*0.7*jitterScale
                timeV += random.random() * 100
            bs.animate(c,"input0",keys,loop=True)
            keys = {}
            timeV = 0
            for i in range(10):
                keys[timeV*self._ts] = y+(random.random()-0.5)*0.7*jitterScale
                timeV += random.random() * 100
            bs.animate(c,"input1",keys,loop=True)
        else:
            logo.node.position = (x,y)

        c = bs.newNode("combine",owner=logo.node,attrs={"size":2})

        keys = {delay:0,delay+100:700*scale,delay+200:600*scale}
        bs.animate(c,"input0",keys)
        bs.animate(c,"input1",keys)
        c.connectAttr("output",logo.node,"scale")
            
    def _startPreloads(self):
        # FIXME - the func that calls us back doesn't save/restore state
        # or check for a dead activity so we have to do that ourself..
        if self.isFinalized(): return
        with bs.Context(self): _preload1()

        bs.gameTimer(500,lambda: bs.playMusic('Menu'))
        
        
# a second or two into the main menu is a good time to preload some stuff
# we'll need elsewhere to avoid hitches later on..
def _preload1():
    for m in ['plasticEyesTransparent', 'playerLineup1Transparent',
              'playerLineup2Transparent', 'playerLineup3Transparent',
              'playerLineup4Transparent', 'angryComputerTransparent',
              'scrollWidgetShort', 'windowBGBlotch']: bs.getModel(m)
    for t in ["playerLineup","lock"]: bs.getTexture(t)
    for tex in ['iconRunaround', 'iconOnslaught',
                'medalComplete', 'medalBronze', 'medalSilver',
                'medalGold', 'characterIconMask']: bs.getTexture(tex)
    bs.getTexture("bg")
    bs.Powerup.getFactory()
    bs.gameTimer(100,_preload2)

def _preload2():
    # FIXME - could integrate these loads with the classes that use them
    # so they don't have to redundantly call the load
    # (even if the actual result is cached)
    for m in ["powerup", "powerupSimple"]: bs.getModel(m)
    for t in ["powerupBomb", "powerupSpeed", "powerupPunch",
              "powerupIceBombs", "powerupStickyBombs", "powerupShield",
              "powerupImpactBombs", "powerupHealth"]: bs.getTexture(t)
    for s in ["powerup01", "boxDrop", "boxingBell", "scoreHit01",
              "scoreHit02", "dripity", "spawn", "gong"]: bs.getSound(s)
    bs.Bomb.getFactory()
    bs.gameTimer(100,_preload3)

def _preload3():
    for m in ["bomb", "bombSticky", "impactBomb"]: bs.getModel(m)
    for t in ["bombColor", "bombColorIce", "bombStickyColor",
              "impactBombColor", "impactBombColorLit"]: bs.getTexture(t)
    for s in ["freeze", "fuse01", "activateBeep", "warnBeep"]: bs.getSound(s)
    spazFactory = bs.Spaz.getFactory()
    # go through and load our existing spazzes and their icons
    # (spread these out quite a bit since theres lots of stuff for each)
    def _load(spaz):
        spazFactory._preload(spaz)
        # icons also..
        bs.getTexture(bsSpaz.appearances[spaz].iconTexture)
        bs.getTexture(bsSpaz.appearances[spaz].iconMaskTexture)
    # FIXME - need to come up with a standin texture mechanism or something
    # ..preloading won't scale too much farther..
    t = 50
    bs.gameTimer(200,_preload4)

def _preload4():
    for t in ['bar', 'meter', 'null', 'flagColor', 'achievementOutline']:
        bs.getTexture(t)
    for m in ['frameInset', 'meterTransparent', 'achievementOutline']:
        bs.getModel(m)
    for s in ['metalHit', 'metalSkid', 'refWhistle', 'achievement']:
        bs.getSound(s)
    bs.Flag.getFactory()
    bs.Powerup.getFactory()

class SplashScreenActivity(bs.Activity):

    def __init__(self,settings={}):
        bs.Activity.__init__(self,settings)
        self._part1Duration = 4000
        self._tex = bs.getTexture('aliSplash')
        self._tex2 = bs.getTexture('aliControllerQR')
        
    def _startPreloads(self):
        # FIXME - the func that calls us back doesn't save/restore state
        # or check for a dead activity so we have to do that ourself..
        if self.isFinalized(): return
        with bs.Context(self): _preload1()
        
    def onTransitionIn(self):
        import bsInternal
        bs.Activity.onTransitionIn(self)
        bsInternal._addCleanFrameCallback(bs.WeakCall(self._startPreloads))
        self._background = bsUtils.Background(fadeTime=500, startFaded=True,
                                              showLogo=False)
        self._part = 1
        self._image = bsUtils.Image(self._tex, transition='fadeIn',
                                    modelTransparent=bs.getModel('image4x1'),
                                    scale=(800, 200), transitionDelay=500,
                                    transitionOutDelay=self._part1Duration-1300)
        bs.gameTimer(self._part1Duration, self.end)

    def _startPart2(self):
        if self._part != 1: return
        self._part = 2
        self._image = bsUtils.Image(self._tex2, transition='fadeIn',
                                    scale=(400, 400), transitionDelay=0)
        t = bsUtils._translate('tips', 'If you are short on controllers, '
                               'install the \'${REMOTE_APP_NAME}\' app\n'
                               'on your mobile devices to use them '
                               'as controllers.')
        t = t.replace('${REMOTE_APP_NAME}',bsUtils._getRemoteAppName())
        self._text = bsUtils.Text(t, maxWidth=900, hAlign='center',
                                  vAlign='center', position=(0,270),
                                  color=(1,1,1,1), transition='fadeIn')
    def onSomethingPressed(self):
        self.end()

gFirstRun = True

class MainMenuSession(bs.Session):

    def __init__(self):
        bs.Session.__init__(self)
        self._locked = False
        # we have a splash screen only on ali currently..
        env = bs.getEnvironment()
        global gFirstRun
        if env['platform'] == 'android' \
           and env['subplatform'] == 'alibaba' \
           and gFirstRun:
            bsInternal._lockAllInput()
            self._locked = True
            self.setActivity(bs.newActivity(SplashScreenActivity))
            gFirstRun = False
        else:
            self.setActivity(bs.newActivity(MainMenuActivity))

    def onActivityEnd(self,activity,results):
        if self._locked:
            bsInternal._unlockAllInput()
        # any ending activity leads us into the main menu one..
        self.setActivity(bs.newActivity(MainMenuActivity))
        
    def onPlayerRequest(self,player):
        # reject player requests, but if we're in a splash-screen, take the
        # opportunity to tell it to leave
        # FIXME - should add a blanket way to capture all input for
        # cases like this
        activity = self.getActivity()
        if isinstance(activity, SplashScreenActivity):
            with bs.Context(activity): activity.onSomethingPressed()
        return False

