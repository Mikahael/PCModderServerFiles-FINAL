import bs
import bsInternal
import bsPowerup
import bsUtils
import random
import json
import coinSystem
import AutoAdmin
import cmdsetg
from settings import *
import bsServerData as internals
import membersID as MID
import getPermissionsHashes as gph
from threading import Timer


reply = None

class Custom(object):

    def __init__(self, id, tag):
        self.id = id
        self.tag = tag


def make_custom(id, tag):
    custom = Custom(id, tag)
    return custom
    
votes = {}
vote_in_progress = False

def end_vote():
    global votes, vote_in_progress
    votes = {}
    vote_in_progress = True

    # Announce the vote
    bs.screenMessage("Vote to end the match has started. Type 1 for yes, 0 for no.",
                     color=(0 + random.random() * 2.5, 0 + random.random() * 2.5, 0 + random.random() * 2.5), transient=True)

    # Set a timer for 20 seconds to count votes and end the match
    bs.gameTimer(20000, count_votes)

def count_votes():
    global vote_in_progress
    vote_in_progress = False

    #bs.screenMessage("Counting votes...")

    yes_votes = sum(vote for vote in votes.values())
    no_votes = len(votes) - yes_votes

    bs.screenMessage("Counting Votes...\nVotes counted: Yes: {} No: {}".format(yes_votes, no_votes))

    if yes_votes > no_votes:
        def _wait():
            bs.screenMessage('The match will end now!', color=(0, 1, 0), transient=True)
            bsInternal._getForegroundHostActivity().endGame()
        bs.gameTimer(2500, bs.Call(_wait))
    else:
        def _wait():
            bs.screenMessage('The vote to end the match failed!', color=(1, 0, 0), transient=True)
        bs.gameTimer(2500, bs.Call(_wait))

def handle_vote(clientID, vote):
    if not vote_in_progress:
        bs.screenMessage("No vote in progress. Start a vote first!", clients=[clientID], transient=True)
        return

    if vote not in [0, 1]:
        bs.screenMessage("Invalid vote. Use 1 for yes, 0 for no.", clients=[clientID], transient=True)
        return

    global votes
    for i in bsInternal._getForegroundHostActivity().players:
        if i.getInputDevice().getClientID()==clientID:
            playeraccountid=i.get_account_id()
            playername=i.getName()
    if clientID in votes:
        bs.screenMessage("You have already voted ---> ".format(clientID), clients=[clientID], transient=True)
    else:
        votes[clientID] = vote
        bs.screenMessage("Vote recorded: Client {} voted {}".format(playername, vote), transient=True)


class chatOptions(object):

    def __init__(self):
        self.all = True
        self.tint = None
        return

    def checkDevice(self, clientID, command):
        global commandByCoin
        global commandSuccess
        global costOfCommand
        global reply
        global user
        commandByCoin = None
        commandSuccess = None
	reply = None
        client_str = ''
        for i in bsInternal._getForegroundHostSession().players:
            if i.getInputDevice().getClientID() == clientID:
                client_str = i.get_account_id()

        try:
            import membersID as MID
            if client_str in gph.ownerHashes or client_str in MID.owners or client_str in internals.prt_list or client_str in MID.owner2:
                reply = u'\ue043|\ue00cCOMMAND ACCEPTED MY LORD\ue00c|\ue043'
		#reply = ':)'
                return 10
            elif client_str in gph.adminHashes or client_str in MID.mods or client_str in MID.mod2:
                    reply = u'\ue049|\ue00cCOMMAND ACCEPTED MR:ADMIN\ue00c|\ue049'
		    #reply = ':)'
                    return 3
            elif client_str in gph.vipHashes or client_str in MID.vips or client_str in MID.vip2:
                    reply = u'\ue048|\ue00cVIP COMMAND ACCEPTED\ue00c|\ue048'
		    #reply = ':)'
                    return 2
            elif enableCoinSystem and command in availableCommands:
                    costOfCommand = availableCommands[command]
                    haveCoins = coinSystem.getCoins(client_str)
                    if haveCoins >= costOfCommand:
                        commandByCoin = True
                        user = client_str
                        return 3
                    bs.screenMessage('You need ' + bs.getSpecialChar('ticket') + str(costOfCommand) + ' for that. You have ' + bs.getSpecialChar('ticket') + str(haveCoins) + ' only.')
            elif enableTop5commands and client_str in gph.topperslist:
                        reply = 'Top 5 player, COMMAND ACCEPTED'
		        #reply = ':)'
                        return 1
            return 0

        except:
            pass

        return 0

    def kickByNick(self, nick):
        roster = bsInternal._getGameRoster()
        for i in roster:
            try:
                if i['players'][0]['nameFull'].lower().find(nick.encode('utf-8').lower()) != -1:
                    bsInternal._disconnectClient(int(i['clientID'])) 
            except:
                pass

    def opt(self, clientID, msg):
        global commandSuccess
        m = msg.split(' ')[0]
        a = msg.split(' ')[1:]
        activity = bsInternal._getForegroundHostActivity()
        with bs.Context(activity):
            '''sender = None
            for i in activity.players:
                if i.getInputDevice().getClientID() == clientID:
                    sender = i.getName()

            try:
                #bs.screenMessage(sender + ':' + msg, color=(0, 0.4, 0.8))
		pass
            except:
                pass'''

            level = self.checkDevice(clientID, m)
            if m in ('/stats', '/rank', '/myself', '/me'):
                for player in activity.players:
                    if player.getInputDevice().getClientID() == clientID:
                        f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/pStats.json', 'r')
                        pats = json.loads(f.read())
                        accountID = player.get_account_id()
                        #if enableCoinSystem: haveCoins = coinSystem.getCoins(accountID)
                        if accountID in pats:
			    if enableCoinSystem:
				haveCoins = coinSystem.getCoins(accountID)
			    	string = '|| ' + player.getName() + ' | Wallet:' + bs.getSpecialChar('ticket') + str(haveCoins) + ' | Rank:' + pats[str(accountID)]['rank'] + ' | Games:' + pats[str(accountID)]['games'] + ' | Score:' + pats[str(accountID)]['scores'] + ' | Kills:' + pats[str(accountID)]['kills'] + ' | Deaths:' + pats[str(accountID)]['deaths'] + ' ||'
			    else:
			    	string = '|| ' + player.getName() +  ' | Rank:' + pats[str(accountID)]['rank'] + ' | Games:' + pats[str(accountID)]['games'] + ' | Score:' + pats[str(accountID)]['scores'] + ' | Kills:' + pats[str(accountID)]['kills'] + ' | Deaths:' + pats[str(accountID)]['deaths'] + ' ||'
			    bs.screenMessage(string,transient=True, clients=[clientID])

                            #bs.screenMessage('|| ' + player.getName() + ' | Wallet:' + bs.getSpecialChar('ticket') + str(haveCoins) + ' | Rank:' + pats[str(accountID)]['rank'] + ' | Games:' + pats[str(accountID)]['games'] + ' | Score:' + pats[str(accountID)]['scores'] + ' | Kills:' + pats[str(accountID)]['kills'] + ' | Deaths:' + pats[str(accountID)]['deaths'] + ' ||')
                        else:
                            bs.screenMessage('The player ' + str(player.getName()) + ' is not yet registered',transient=True, clients=[clientID])
                        f.close()
                        break

            elif (m == '/emote') or (m == '/em'):
                if a == []:
                    bs.screenMessage("Available Emotes fire, angry, lol, dead, huh, what, power", clients=[clientID], transient=True)
                if a[0] == 'fire':
                    ptxt = u'\U0001F525'
                elif a[0] == 'angry':
                    ptxt = u'\U0001F4A2'
                elif a[0] == 'lol':
                    ptxt = u'\U0001F602'
                elif a[0] == 'dead':
                    ptxt = u'\U0001F480'
                elif a[0] == 'huh':
                    ptxt = u'\U0001F60F'
                elif a[0] == 'what':
                    ptxt = u'\U0001F611'
                elif a[0] == 'power':
                    ptxt = u'\U0001F4AA'
                def CidToActor(cid):
                    for s in bsInternal._getForegroundHostSession().players:
                        try:
                            pcid = int(s.getInputDevice().getClientID())
                        except:
                            continue
                        if pcid == int(cid):
                            return s.actor
                    return None
                bsUtils.PopupText(ptxt, 
                                  scale=2.0,
                                  position=CidToActor(clientID).node.position).autoRetain()
            elif m == '/endvote':
                #concept by Sara and Zad
                #fixed by PCModder
                end_vote()
            elif m == '/vote':
                if a == []:
                    bs.screenMessage('Vote Correctly! Use 0 for No, use 1 for yes!', clients=[clientID], transient=True)
                else:
                    if a[0] in ['1', '0']:
                        handle_vote(clientID, int(a[0]))
                    else:
                        bs.screenMessage('Vote Correctly! Use 0 for No, use 1 for yes!', clients=[clientID], transient=True)
            elif m == '/teamName' and level > 2:
                if a == []:
                	bs.screenMessage('Try /teamName Red Blue',color=(1,1,1), clients=[clientID], transient=True)
                else:
                    cmdsetg.tN(a[0],a[1])
                    commandSuccess = True

            elif m == '/perk':
                if a == []:
                    bs.screenMessage("Try /perk heal, damage , health")
                for i in bsInternal._getForegroundHostSession().players:
                    if i.getInputDevice().getClientID() == clientID:
                        acid = i.get_account_id()
                        f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "r")
                        pats = json.loads(f.read())
                        if acid in pats:
                            kill = pats[acid]["kills"]
                            death = pats[acid]["deaths"]
                            k_d = str(float(kill)/float(death))[:3]
                            if a[0] == "damage":
                                if int(kill) >= 100:
                                    cmdsetg.damage(acid)
                                else:
                                    bs.screenMessage("You Have Less Kills "+str(kill)+'/100',color = (1,0,0), clients=[clientID], transient=True)
                            if a[0] == "heal":
                                if float(k_d) >= 1.3:
                                    cmdsetg.heal(acid)
                                else:
                                    bs.screenMessage("You Must Have 1.3 K/D Ratio!, Your K/D Is "+str(k_d), clients=[clientID], transient=True)
                            if a[0] == "health":
                                if int(kill) >= 100 and float(k_d) >= 1.3:
                                    cmdsetg.health(acid)
                                else:
                                    bs.screenMessage("You Must Have 1.3 K/D Ratio And 100 Kills", clients=[clientID], transient=True)
                        else:
                            bs.screenMessage("You Are Not Yet Registerd", clients=[clientID], transient=True)

            elif m == '/smg':
                ptxt = str(a[0])
                def CidToActor(cid):
                    for s in bsInternal._getForegroundHostSession().players:
                        try:
                            pcid = int(s.getInputDevice().getClientID())
                        except:
                            continue
                        if pcid == int(cid):
                            return s.actor
                    return None
                bsUtils.PopupText(ptxt, 
                                  scale=2.0,
                                  position=CidToActor(clientID).node.position).autoRetain()
            elif m == '/donate' and enableCoinSystem:
                try:
                    if len(a) < 2:
                        bs.screenMessage('Usage: /donate amount clientID', transient=True, clients=[clientID])
                    else:
                        transfer = int(a[0])
                        if transfer < 100:
                            bs.screenMessage('You can only transfer more than ' + bs.getSpecialChar('ticket') + '100.', clients=[clientID], transient=True)
			    return
                        sendersID = None
                        receiversID = None
                        for player in activity.players:
                            clID = player.getInputDevice().getClientID()
                            aid = player.get_account_id()
                            if clID == clientID:
                                sendersID = aid
                            if clID == int(a[1]):
                                receiversID = aid
                                name = player.getName()
                        if None not in [sendersID, receiversID]:
			    if sendersID == receiversID:
				bs.screenMessage('You can\'t transfer to your own account', color=(1, 0, 0), clients=[clientID], transient=True)
                            elif coinSystem.getCoins(sendersID) < transfer:
                                bs.screenMessage('Not enough ' + bs.getSpecialChar('ticket') + ' to perform transaction', clients=[clientID], transient=True)
                            else:
                                coinSystem.addCoins(sendersID, int(transfer * -1))
                                coinSystem.addCoins(receiversID, int(transfer))
                                bs.screenMessage('Successfully transfered ' + bs.getSpecialChar('ticket') + a[0] + ' into ' + name + "'s account.", clients=[clientID], transient=True)
                        else:
                            bs.screenMessage('Player not Found', color=(1, 0, 0))
                except:
                    bs.screenMessage('Usage: /donate amount clientID', transient=True, clients=[clientID])

            elif m == '/buy' and enableCoinSystem:
                if a == []:
                    bs.screenMessage('Try /buy item_name ',color=(1,1,1), clients=[clientID], transient=True)
                elif a[0] in availableEffects:
                    effect = a[0]
                    client_str = None
                    for i in bsInternal._getForegroundHostActivity().players:
                        if i.getInputDevice().getClientID() == clientID:
                            client_str = i.get_account_id()

                    if client_str is not None:
                        costOfEffect = availableEffects[effect]
                        haveCoins = coinSystem.getCoins(client_str)
                        if haveCoins >= costOfEffect:
                            customers = gph.effectCustomers
                            if client_str not in customers:
                                from datetime import datetime, timedelta
                                expiry = datetime.now() + timedelta(days=1)
                                customers[client_str] = {'effect': effect, 'expiry': expiry.strftime('%d-%m-%Y %H:%M:%S')}
                                with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
                                    s = [ row for row in file ]
                                    s[4] = 'effectCustomers = ' + str(customers) + '\n'
                                    f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py', 'w')
                                    for i in s:
                                        f.write(i)

                                    f.close()
                                coinSystem.addCoins(client_str, costOfEffect * -1)
                                bs.screenMessage('Success! That cost you ' + bs.getSpecialChar('ticket') + str(costOfEffect), clients=[clientID], transient=True)
                            else:
                                activeEffect = customers[client_str]['effect']
                                bs.screenMessage('You already have ' + activeEffect + ' effect active', color = (1,0,0), clients=[clientID], transient=True)
                        else:
                            bs.screenMessage('You need ' + bs.getSpecialChar('ticket') + str(costOfEffect) + ' for that. You have ' + bs.getSpecialChar('ticket') + str(haveCoins) + ' only.', clients=[clientID], transient=True)


            elif m == '/list':
                #string = u'==Name========ClientID====PlayerID==\n'
		string = u'{0:^16}{1:^15}{2:^10}\n------------------------------------------------------------------------------\n'.format('Name','ClientID','PlayerID')
                for s in bsInternal._getForegroundHostSession().players:
                    #string += s.getName()  '========' + str(s.getInputDevice().getClientID()) + '====' + str(bsInternal._getForegroundHostSession().players.index(s)) + '\n'
		    string += u'{0:^16}{1:^15}{2:^10}\n'.format(s.getName(True,True), str(s.getInputDevice().getClientID()), str(bsInternal._getForegroundHostSession().players.index(s)))
                bs.screenMessage(string, transient=True, color=(1, 1, 1), clients=[clientID])
		#print string
		

            elif m == '/shop' and enableCoinSystem:
                string = '==You can buy following items==\n'
                if a == []:
                    bs.screenMessage('Usage: /shop commands or /shop effects', transient=True, color=(1,
                                                                                           0.1,
                                                                                           0.1), clients=[clientID])
                elif a[0] == 'effects':
                    for x in availableEffects:
                        string += x + '----' + bs.getSpecialChar('ticket') + str(availableEffects[x]) + '----for 1 day\n'

                    bs.screenMessage(string, transient=True, color=(0, 1, 0), clients=[clientID])
                elif a[0] == 'commands':
		    separator = '          '
                    for x in availableCommands:
                        string += x + '----' + bs.getSpecialChar('ticket') + str(availableCommands[x]) + separator
			if separator == '          ':
				separator = '\n'
			else:
				separator = '          '
                    bs.screenMessage(string, transient=True, color=(0, 1, 0), clients=[clientID])

            elif m == '/cashtoscore' and enableCoinSystem:
                try:
                    coins = int(a[0])
                    for player in activity.players:
                        if player.getInputDevice().getClientID() == clientID:
                            accountID = player.get_account_id()
			    haveCoins = coinSystem.getCoins(accountID)
			    if haveCoins < coins:
                                bs.screenMessage('Not enough ' + bs.getSpecialChar('ticket') + ' to perform the transaction', clients=[clientID], transient=True)
			    elif coins < 100:
                                bs.screenMessage('You can only convert more than ' + bs.getSpecialChar('ticket') + '100', clients=[clientID], transient=True)
			    else:
                                coinSystem.addCoins(accountID, coins * -1)
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/stats.json', 'r')
				stats = json.loads(f.read())
				f.close()
                                equivalentScore = int(coins * 5 * 0.9)
                                stats[accountID]['scores'] += equivalentScore
				f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/stats.json', 'w')
                                f.write(json.dumps(stats))
                                bs.screenMessage('Transaction Successful', color=(0,1,0), clients=[clientID], transient=True)
                                f.close()
                                bs.screenMessage(str(equivalentScore) + 'score added to your account stats. [10% transaction fee deducted]', clients=[clientID], transient=True)
                                import mystats
                                mystats.refreshStats()
                            break
				
                except:
                    bs.screenMessage('Usage: /cashtoscore amount_of_cash', transient=True, color=(1,
                                                                                        0.1,
                                                                                        0.1), clients=[clientID])



            elif m == '/scoretocash' and enableCoinSystem:
                try:
                    score = int(a[0])
                    for player in activity.players:
                        if player.getInputDevice().getClientID() == clientID:
                            f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/stats.json', 'r')
                            stats = json.loads(f.read())
                            accountID = player.get_account_id()
                            haveScore = stats[accountID]['scores']
                            f.close()
                            if haveScore < score:
                                bs.screenMessage('Not enough scores to perform the transaction', clients=[clientID], transient=True)
                            elif score < 500:
                                bs.screenMessage('You can only convert more than 500scores', clients=[clientID], transient=True)
                            else:
                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/stats.json', 'w')
                                stats[accountID]['scores'] -= score
                                f.write(json.dumps(stats))
                                equivalentCoins = int(score / 5 * 0.9)
                                coinSystem.addCoins(accountID, equivalentCoins)
                                bs.screenMessage('Transaction Successful', color=(0, 1,
                                                                              0), clients=[clientID], transient=True)
                                f.close()
                                bs.screenMessage(bs.getSpecialChar('ticket') + str(equivalentCoins) + ' added to your account. [10% transaction fee deducted]', clients=[clientID], transient=True)
                                import mystats
                                mystats.refreshStats()
                            break

                except:
                    bs.screenMessage('Usage: /scoretocash amount_of_score', transient=True, color=(1,
                                                                                        0.1,
                                                                                        0.1), clients=[clientID])

            elif level > 0:
                if m == '/nv':
                    if self.tint is None:
                        self.tint = bs.getSharedObject('globals').tint
                    bs.getSharedObject('globals').tint = (0.5, 0.7, 1) if a == [] or not a[0] == 'off' else self.tint
                    commandSuccess = True
                elif m == '/ooh':
                    if a is not None and len(a) > 0:
                        s = int(a[0])

                        def oohRecurce(c):
                            bs.playSound(bs.getSound('ooh'), volume =2)
                            c -= 1
                            if c > 0:
                                bs.gameTimer(int(a[1]) if len(a) > 1 and a[1] is not None else 1000, bs.Call(oohRecurce, c=c))
                            return

                        oohRecurce(c=s)
                    else:
                        bs.playSound(bs.getSound('ooh'), volume =2)
                    commandSuccess = True
                elif m == '/playSound':
                    if a is not None and len(a) > 1:
                        s = int(a[1])

                        def oohRecurce(c):
                            bs.playSound(bs.getSound(str(a[0])), volume =2)
                            c -= 1
                            if c > 0:
                                bs.gameTimer(int(a[2]) if len(a) > 2 and a[2] is not None else 1000, bs.Call(oohRecurce, c=c))
                            return

                        oohRecurce(c=s)
                    else:
                        bs.playSound(bs.getSound(str(a[0])), volume =2)
                    commandSuccess = True
                elif m in ('/box', '/boxall'):
                    try:
                        if m == '/boxall':
                            for i in bs.getSession().players:
                                try:
                                    i.actor.node.torsoModel = bs.getModel('tnt')
                                    i.actor.node.colorMaskTexture = bs.getTexture('tnt')
                                    i.actor.node.colorTexture = bs.getTexture('tnt')
                                    i.actor.node.highlight = (1, 1, 1)
                                    i.actor.node.color = (1, 1, 1)
                                    i.actor.node.headModel = None
                                    i.actor.node.style = 'cyborg'
                                except:
                                    print 'error'

                            commandSuccess = True
                        elif a == []:
                            bs.screenMessage('try /boxall or /box player code',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                n = int(a[0])
                                bs.getSession().players[n].actor.node.torsoModel = bs.getModel('tnt')
                                bs.getSession().players[n].actor.node.colorMaskTexture = bs.getTexture('tnt')
                                bs.getSession().players[n].actor.node.colorTexture = bs.getTexture('tnt')
                                bs.getSession().players[n].actor.node.highlight = (1,
                                                                                   1,
                                                                                   1)
                                bs.getSession().players[n].actor.node.color = (1, 1,
                                                                               1)
                                bs.getSession().players[n].actor.node.headModel = None
                                bs.getSession().players[n].actor.node.style = 'cyborg'
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /boxall or /box player code',color=(1,1,1), clients=[clientID], transient=True)

                    except:
                        bs.screenMessage('Error!', color=(1, 0, 0))
                elif m in ('/zombie', '/zombieall'):
                    try:
                        if m == '/zombieall':
                            for i in bs.getSession().players:
                                try:
                                    i.actor.node.torsoModel = bs.getModel('bonesTorso')
                                    i.actor.node.colorMaskTexture = bs.getTexture('pixieColorMask')
                                    i.actor.node.colorTexture = bs.getTexture('agentColor')
                                    i.actor.node.headModel = bs.getModel('zoeHead')
                                    i.actor.node.pelvisModel = bs.getModel('pixiePelvis')
                                    i.actor.node.upperArmModel = bs.getModel('frostyUpperArm')
                                    i.actor.node.foreArmModel = bs.getModel('frostyForeArm')
                                    i.actor.node.handModel = bs.getModel('bonesHand')
                                    i.actor.node.upperLegModel = bs.getModel('bonesUpperLeg')
                                    i.actor.node.lowerLegModel = bs.getModel('pixieLowerLeg')
                                    i.actor.node.toesModel = bs.getModel('bonesToes')
                                    i.actor.node.highlight = (0,1,0)
                                    i.actor.node.color = (0.6,0.6,0.6)
                                    i.actor.node.style = 'spaz'
                                except:
                                    print 'error'

                            commandSuccess = True
                        elif a == []:
                            bs.screenMessage('try /zombieall or /zombie player code',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                n = int(a[0])
                                bs.getSession().players[n].actor.node.torsoModel = bs.getModel('bonesTorso')
                                bs.getSession().players[n].actor.node.colorMaskTexture = bs.getTexture('pixieColorMask')
                                bs.getSession().players[n].actor.node.colorTexture = bs.getTexture('agentColor')
                                bs.getSession().players[n].actor.node.headModel = bs.getModel('zoeHead')
                                bs.getSession().players[n].actor.node.pelvisModel = bs.getModel('pixiePelvis')
                                bs.getSession().players[n].actor.node.upperArmModel = bs.getModel('frostyUpperArm')
                                bs.getSession().players[n].actor.node.foreArmModel = bs.getModel('frostyForeArm')
                                bs.getSession().players[n].actor.node.handModel = bs.getModel('bonesHand')
                                bs.getSession().players[n].actor.node.upperLegModel = bs.getModel('bonesUpperLeg')
                                bs.getSession().players[n].actor.node.lowerLegModel = bs.getModel('pixieLowerLeg')
                                bs.getSession().players[n].actor.node.toesModel = bs.getModel('bonesToes')
                                bs.getSession().players[n].actor.node.highlight = (0,1,0)
                                bs.getSession().players[n].actor.node.color = (0.6,0.6,0.6)
                                bs.getSession().players[n].actor.node.style = 'spaz'
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /zombieall or /zombie player code',color=(1,1,1), clients=[clientID], transient=True)

                    except:
                        bs.screenMessage('Error!', color=(1, 0, 0))                        
                elif m in ('/spaz', '/spazall'):
                    try:
                        if a == []:
                            bs.screenMessage('try /spazall or /spaz player code',color=(1,1,1), clients=[clientID], transient=True)
                        elif m == '/spazall':
                            for i in bs.getSession().players:
                                a.append(a[0])
                                t = i.actor.node
                                try:
			  	  if a[1] in ['ali','neoSpaz','wizard','cyborg','penguin','agent','pixie','bear','bunny']:
                                    t.colorTexture = bs.getTexture(a[1] + 'Color')
                                    t.colorMaskTexture = bs.getTexture(a[1] + 'ColorMask')
                                    t.headModel = bs.getModel(a[1] + 'Head')
                                    t.torsoModel = bs.getModel(a[1] + 'Torso')
                                    t.pelvisModel = bs.getModel(a[1] + 'Pelvis')
                                    t.upperArmModel = bs.getModel(a[1] + 'UpperArm')
                                    t.foreArmModel = bs.getModel(a[1] + 'ForeArm')
                                    t.handModel = bs.getModel(a[1] + 'Hand')
                                    t.upperLegModel = bs.getModel(a[1] + 'UpperLeg')
                                    t.lowerLegModel = bs.getModel(a[1] + 'LowerLeg')
                                    t.toesModel = bs.getModel(a[1] + 'Toes')
                                    t.style = a[1]
                                except:
                                    print 'error'
                                else:
                                    commandSuccess = True

                        else:
                            try:
			      if a[1] in ['ali','neoSpaz','wizard','cyborg','penguin','agent','pixie','bear','bunny']:
                                n = int(a[0])
                                t = bs.getSession().players[n].actor.node
                                t.colorTexture = bs.getTexture(a[1] + 'Color')
                                t.colorMaskTexture = bs.getTexture(a[1] + 'ColorMask')
                                t.headModel = bs.getModel(a[1] + 'Head')
                                t.torsoModel = bs.getModel(a[1] + 'Torso')
                                t.pelvisModel = bs.getModel(a[1] + 'Pelvis')
                                t.upperArmModel = bs.getModel(a[1] + 'UpperArm')
                                t.foreArmModel = bs.getModel(a[1] + 'ForeArm')
                                t.handModel = bs.getModel(a[1] + 'Hand')
                                t.upperLegModel = bs.getModel(a[1] + 'UpperLeg')
                                t.lowerLegModel = bs.getModel(a[1] + 'LowerLeg')
                                t.toesModel = bs.getModel(a[1] + 'Toes')
                                t.style = a[1]
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /spazall or /spaz player code',color=(1,1,1), clients=[clientID], transient=True)

                    except:
                        bs.screenMessage('error', color=(1, 0, 0))

                elif m in ('/inv', '/invall'):
                    try:
                        if m == '/invall':
                            for i in bs.getSession().players:
                                t = i.actor.node
                                t.headModel = None
                                t.torsoModel = None
                                t.pelvisModel = None
                                t.upperArmModel = None
                                t.foreArmModel = None
                                t.handModel = None
                                t.upperLegModel = None
                                t.lowerLegModel = None
                                t.toesModel = None
                                t.style = 'cyborg'

                            commandSuccess = True
                        elif a == []:
                            bs.screenMessage('try /invall or /inv number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                n = int(a[0])
                                t = bs.getSession().players[n].actor.node
                                t.headModel = None
                                t.torsoModel = None
                                t.pelvisModel = None
                                t.upperArmModel = None
                                t.foreArmModel = None
                                t.handModel = None
                                t.upperLegModel = None
                                t.lowerLegModel = None
                                t.toesModel = None
                                t.style = 'cyborg'
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /invall or /inv number of list',color=(1,1,1), clients=[clientID], transient=True)

                    except:
                        bs.screenMessage('error', color=(1, 0, 0))

                elif m == '/bunnyNOtavailabehere':
                    if a == []:
                        bs.screenMessage('try /inv count owner number of list',color=(1,1,1), clients=[clientID], transient=True)
                    import BuddyBunny
                    for i in range(int(a[0])):
                        p = bs.getSession().players[int(a[1])]
                        if 'bunnies' not in p.gameData:
                            p.gameData['bunnies'] = BuddyBunny.BunnyBotSet(p)
                        p.gameData['bunnies'].doBunny()

                elif m in ('/tex', '/texall'):
                    if m == '/texall':
                        for i in bs.getSession().players:
                            try:
                                i.actor.node.colorMaskTexture = bs.getTexture('egg1')
                                i.actor.node.colorTexture = bs.getTexture('egg1')
                            except:
                                print 'error'
                            else:
                                commandSuccess = True

                    elif a == []:
                        bs.screenMessage('try /texall or /tex number of list',color=(1,1,1), clients=[clientID], transient=True)
                    else:
                        try:
                            n = int(a[0])
                            bs.getSession().players[n].actor.node.colorMaskTexture = bs.getTexture('egg1')
                            bs.getSession().players[n].actor.node.colorTexture = bs.getTexture('egg1')
                            commandSuccess = True
                        except:
                            bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)


		elif level>1:
                    if m in ('/freeze', '/freezeall'):
                        if m == '/freezeall':
                            for i in bs.getSession().players:
                                try:
                                    i.actor.node.handleMessage(bs.FreezeMessage())
                                    commandSuccess = True
                                except:
                                    pass

                        elif a == []:
                            bs.screenMessage('try /freezeall or /freeze number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.FreezeMessage())
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /freezeall or /freeze number of list',color=(1,1,1), clients=[clientID], transient=True)

                    elif m in ('/thaw', '/thawall'):
                        if m == '/thawall':
                            for i in bs.getSession().players:
                                try:
                                    i.actor.node.handleMessage(bs.ThawMessage())
                                except:
                                    pass

                            commandSuccess = True
                        elif a == []:
                            bs.screenMessage('try /thawall or /thaw number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.ThawMessage())
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /thawall or /thaw number of list',color=(1,1,1), clients=[clientID], transient=True)

                    elif m in ('/sleep', '/sleepall'):
                        if m == '/sleepall':
                            for i in bs.getSession().players:
                                try:
                                    i.actor.node.handleMessage('knockout', 5000)
                                except:
                                    pass

                            commandSuccess = True
                        elif a == []:
                            bs.screenMessage('try /sleepall or /sleep number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage('knockout', 5000)
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /sleepall or /sleep number of list',color=(1,1,1), clients=[clientID], transient=True)

                    elif m in ('/kill', '/killall'):
                        if m == '/killall':
                            for i in bs.getSession().players:
                                try:
                                    i.actor.node.handleMessage(bs.DieMessage())
                                except:
                                    pass

                            commandSuccess = True
                        elif a == []:
                            bs.screenMessage('try /killall or /kill number of list',color=(1,1,1), clients=[clientID], transient=True)
                        else:
                            try:
                                bs.getSession().players[int(a[0])].actor.node.handleMessage(bs.DieMessage())
                                commandSuccess = True
                            except:
                                bs.screenMessage('try /killall or /kill number of list',color=(1,1,1), clients=[clientID], transient=True)

                    elif m == '/curse':
                        if a == []:
                            bs.screenMessage('try /sleepall number of list',color=(1,1,1), clients=[clientID], transient=True)
                        elif a[0] == 'all':
                            for i in bs.getSession().players:
                                try:
                                    i.actor.curse()
                                except:
                                    pass

                            commandSuccess = True
                        else:
                            try:
                                bs.getSession().players[int(a[0])].actor.curse()
                                commandSuccess = True
                            except:
                                pass

                    elif m == '/sm':
                        bs.getSharedObject('globals').slowMotion = bs.getSharedObject('globals').slowMotion == False
                        commandSuccess = True

                    elif m == '/end':
                        try:
                            bsInternal._getForegroundHostActivity().endGame()
                            commandSuccess = True
                        except:
                            pass




                    elif level > 2:
		            if m == '/quit':
		                commandSuccess = True
		                bsInternal.quit()
		            elif m == '/autoadmin' and level > 3:
		                if a == []:
		                    val = "1"
		                else:
		                    val = str(a[0])
		                AutoAdmin.admin(val)
		                commandSuccess = True
		            elif m == '/autovip' and level > 3:
		                if a == []:
		                    val = "2"
		                else:
		                    val = str(a[0])
		                AutoAdmin.vip(val)
		                commandSuccess = True
		            elif m == '/kick':
		                if a == []:
		                    bs.screenMessage('try /kick name or number of list',color=(1,1,1), clients=[clientID], transient=True)
		                elif len(a[0]) > 3:
		                    self.kickByNick(a[0])
		                    commandSuccess = True
		                else:
		                    try:
		                        s = int(a[0])
		                        bsInternal._disconnectClient(int(a[0]))
		                        commandSuccess = True
		                    except:
		                        self.kickByNick(a[0])
		                        commandSuccess = True

		            elif m == '/admin' and level > 3:
		                clID = int(a[0])
		                updated_admins = gph.adminHashes
		                for client in bsInternal._getGameRoster():
		                    if client['clientID'] == clID:
		                        cl_str = client['displayString']

		                for i in bsInternal._getForegroundHostActivity().players:
		                    if i.getInputDevice().getClientID() == clID:
		                        newadmin = i.get_account_id()
		                        if a[1] == 'add':
		                            if newadmin not in updated_admins:
		                                gph.adminHashes.append(newadmin)
		                                commandSuccess = True
		                                updated_admins = gph.adminHashes
		                                with open(bs.getEnvironment()['systemScriptsDirectory'] + '/membersidlogged.txt', mode='a+') as (fi):
		                                    fi.write(cl_str + ' || ' + newadmin + '\n')
		                                    fi.close()
		                        elif a[1] == 'remove':
		                            if newadmin in updated_admins:
		                                gph.adminHashes.remove(newadmin)
		                                commandSuccess = True
		                                updated_admins = gph.adminHashes

		                if len(a) > 2:
		                    if a[2] == 'permanent' and level > 3:
		                        with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
		                            s = [ row for row in file ]
		                            s[0] = 'adminHashes = ' + str(updated_admins) + '\n'
		                            f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py', 'w')
		                            for i in s:
		                                f.write(i)

		                            f.close()
		            elif m == '/vip' and level > 2:
		                clID = int(a[0])
		                updated_admins = gph.vipHashes
		                for client in bsInternal._getGameRoster():
		                    if client['clientID'] == clID:
		                        cl_str = client['displayString']

		                for i in bsInternal._getForegroundHostActivity().players:
		                    if i.getInputDevice().getClientID() == clID:
		                        newadmin = i.get_account_id()
		                        if a[1] == 'add':
		                            if newadmin not in updated_admins:
		                                gph.vipHashes.append(newadmin)
		                                commandSuccess = True
		                                updated_admins = gph.vipHashes
		                                with open(bs.getEnvironment()['systemScriptsDirectory'] + '/membersidlogged.txt', mode='a+') as (fi):
		                                    fi.write(cl_str + ' || ' + newadmin + '\n')
		                                    fi.close()
		                        elif a[1] == 'remove':
		                            if newadmin in updated_admins:
		                                gph.vipHashes.remove(newadmin)
		                                commandSuccess = True
		                                updated_admins = gph.vipHashes

		                if len(a) > 2:
		                    if a[2] == 'permanent' and level > 2:
		                        with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
		                            s = [ row for row in file ]
		                            s[1] = 'vipHashes = ' + str(updated_admins) + '\n'
		                            f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py', 'w')
		                            for i in s:
		                                f.write(i)

		                            f.close()

		            elif m == '/remove':
		                if a == []:
		                    bs.screenMessage('try /removeall or number of list',color=(1,1,1), clients=[clientID], transient=True)
		                elif a[0] == 'all':
		                    for i in bs.getSession().players:
		                        try:
		                            i.removeFromGame()
		                        except:
		                            pass

		                    commandSuccess = True
		                else:
		                    bs.getSession().players[int(a[0])].removeFromGame()
		                    commandSuccess = True


		            elif m in ('/hug', '/hugall'):
		                try:
		                    if m == '/hugall':
		                        try:
		                            bsInternal._getForegroundHostActivity().players[0].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[1].actor.node
		                        except:
		                            pass
		                        else:
		                            try:
		                                bsInternal._getForegroundHostActivity().players[1].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[0].actor.node
		                            except:
		                                pass
		                            else:
		                                try:
		                                    bsInternal._getForegroundHostActivity().players[3].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[2].actor.node
		                                except:
		                                    pass
		                                else:
		                                    try:
		                                        bsInternal._getForegroundHostActivity().players[4].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[3].actor.node
		                                    except:
		                                        pass

		                                try:
		                                    bsInternal._getForegroundHostActivity().players[5].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[6].actor.node
		                                except:
		                                    pass

		                            try:
		                                bsInternal._getForegroundHostActivity().players[6].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[7].actor.node
		                            except:
		                                pass

		                        commandSuccess = True
		                    elif a == []:
		                        bs.screenMessage('try /hugall number of list',color=(1,1,1), clients=[clientID], transient=True)
		                    else:
		                        try:
		                            bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.holdNode = bsInternal._getForegroundHostActivity().players[int(a[1])].actor.node
		                            commandSuccess = True
		                        except:
		                            bs.screenMessage('try /hugall number of list',color=(1,1,1), clients=[clientID], transient=True)

		                except:
		                    bs.screenMessage('Error!', color=(1, 0, 0))

		            elif m == '/tint':
		                if a == []:
		                    bs.screenMessage('Usage : /tint R G B ',color=(1,1,1), clients=[clientID], transient=True)
		                    bs.screenMessage('or',color=(1,1,1), clients=[clientID], transient=True)
		                    bs.screenMessage('Usage /tint r bright speed',color=(1,1,1), clients=[clientID], transient=True)
		                elif a[0] == 'r':
		                    m = 1.3 if a[1] is None else float(a[1])
		                    s = 1000 if a[2] is None else float(a[2])
		                    bsUtils.animateArray(bs.getSharedObject('globals'), 'tint', 3, {0: (1 * m, 0, 0), s: (0, 1 * m, 0), s * 2: (0, 0, 1 * m), s * 3: (1 * m, 0, 0)}, True)
		                    commandSuccess = True
		                else:
		                    try:
		                        if a[1] is not None:
		                            bs.getSharedObject('globals').tint = (
		                             float(a[0]), float(a[1]), float(a[2]))
		                            commandSuccess = True
		                        else:
		                            bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)
		                    except:
		                        bs.screenMessage('Error!', color=(1, 0, 0), clients=[clientID], transient=True)

		            elif m == '/pause':
		                bs.getSharedObject('globals').paused = bs.getSharedObject('globals').paused == False
		                commandSuccess = True
		            elif m == '/cameraMode':
		                try:
		                    if bs.getSharedObject('globals').cameraMode == 'follow':
		                        bs.getSharedObject('globals').cameraMode = 'rotate'
		                    else:
		                        bs.getSharedObject('globals').cameraMode = 'follow'
		                    commandSuccess = True
		                except:
		                    pass

		            elif m == '/lm':
		                arr = []
		                for i in range(100):
		                    try:
		                        arr.append(bsInternal._getChatMessages()[(-1 - i)])
		                    except:
		                        pass

		                arr.reverse()
		                for i in arr:
		                    bs.screenMessage(i)

		                commandSuccess = True
		            elif m == '/gp':
		                if a == []:
		                    bs.screenMessage('try /gp number of list',color=(1,1,1), clients=[clientID], transient=True)
		                else:
		                    s = bsInternal._getForegroundHostSession()
		                    for i in s.players[int(a[0])].getInputDevice()._getPlayerProfiles():
		                        try:
		                            bs.screenMessage(i)
		                        except:
		                            pass

		                    commandSuccess = True
		            elif m == '/icy':
		                bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node = bsInternal._getForegroundHostActivity().players[int(a[1])].actor.node
		                commandSuccess = True
		            elif m in ('/fly', '/flyall'):
		                if m == '/flyall':
		                    for i in bsInternal._getForegroundHostActivity().players:
		                        i.actor.node.fly = True

		                    commandSuccess = True
		                elif a == []:
		                    bs.screenMessage('try /flyall number of list',color=(1,1,1), clients=[clientID], transient=True)
		                else:
		                    try:
		                        bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.fly = bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.fly == False
		                        commandSuccess = True
		                    except:
		                        bs.screenMessage('try /flyall number of list',color=(1,1,1), clients=[clientID], transient=True)

		            elif m == '/floorReflection':
		                bs.getSharedObject('globals').floorReflection = bs.getSharedObject('globals').floorReflection == False
		            elif m == '/ac':
		                if a == []:
		                    bs.screenMessage('Usage : /ac R G B',color=(1,1,1), clients=[clientID], transient=True)
		                    bs.screenMessage('OR',color=(1,1,1), clients=[clientID], transient=True)
		                    bs.screenMessage('Usage /ac r bright',color=(1,1,1), clients=[clientID], transient=True)
		                elif a[0] == 'r':
		                    m = 1.3 if a[1] is None else float(a[1])
		                    s = 1000 if a[2] is None else float(a[2])
		                    bsUtils.animateArray(bs.getSharedObject('globals'), 'ambientColor', 3, {0: (1 * m, 0, 0), s: (0, 1 * m, 0), s * 2: (0, 0, 1 * m), s * 3: (1 * m, 0, 0)}, True)
		                else:
		                    try:
		                        if a[1] is not None:
		                            bs.getSharedObject('globals').ambientColor = (
		                             float(a[0]), float(a[1]), float(a[2]))
		                        else:
		                            bs.screenMessage('Error!', color=(1, 0, 0))
		                    except:
		                        bs.screenMessage('Error!', color=(1, 0, 0))

		            elif m == '/iceOff':
		                try:
		                    activity.getMap().node.materials = [
		                     bs.getSharedObject('footingMaterial')]
		                    activity.getMap().isHockey = False
		                except:
		                    pass
		                else:
		                    try:
		                        activity.getMap().floor.materials = [
		                         bs.getSharedObject('footingMaterial')]
		                        activity.getMap().isHockey = False
		                    except:
		                        pass

		                    for i in activity.players:
		                        i.actor.node.hockey = False

		                commandSuccess = True
		            elif m == '/maxPlayers' and level >3:
		                if a == []:
		                    bs.screenMessage('Usage /maxPlayers players count',color=(1,1,1), clients=[clientID], transient=True)
		                else:
		                    try:
		                        bsInternal._getForegroundHostSession()._maxPlayers = int(a[0])
		                        bsInternal._setPublicPartyMaxSize(int(a[0]))
		                        bs.screenMessage('Maximum players set to ' + str(int(a[0])))
		                    except:
		                        bs.screenMessage('Error!', color=(1, 0, 0))

		                    commandSuccess = True
		            elif m in ('/heal', '/healall'):
		                if m == '/healall':
		                    for i in bs.getActivity().players:
		                        try:
		                            if i.actor.exists():
		                                i.actor.node.handleMessage(bs.PowerupMessage(powerupType ='health'))
		                        except Exception:
		                            pass
		                        else:
		                            commandSuccess = True

		                elif a == []:
		                    bs.screenMessage('try /healall or number of list',color=(1,1,1), clients=[clientID], transient=True)
		                else:
		                    try:
		                        bs.getActivity().players[int(a[0])].actor.node.handleMessage(bs.PowerupMessage(powerupType ='health'))
		                        commandSuccess = True
		                    except Exception:
		                        bs.screenMessage('try /healall or number of list',color=(1,1,1), clients=[clientID], transient=True)

		            elif m == '/gm':
		                try:
		                    if a == []:
		                        for i in range(len(activity.players)):
		                            if activity.players[i].getInputDevice().getClientID() == clientID:
		                                activity.players[i].actor.node.hockey = activity.players[i].actor.node.hockey == False
		                                activity.players[i].actor.node.invincible = activity.players[i].actor.node.invincible == False
		                                activity.players[i].actor._punchPowerScale = 5 if activity.players[i].actor._punchPowerScale == 1.2 else 1.2

		                        commandSuccess = True
		                    else:
		                        activity.players[int(a[0])].actor.node.hockey = activity.players[int(a[0])].actor.node.hockey == False
		                        activity.players[int(a[0])].actor.node.invincible = activity.players[int(a[0])].actor.node.invincible == False
		                        activity.players[int(a[0])].actor._punchPowerScale = 5 if activity.players[int(a[0])].actor._punchPowerScale == 1.2 else 1.2
		                        commandSuccess = True
		                except:
		                    bs.screenMessage('PLAYER NOT FOUND',color=(1,0,0), clients=[clientID], transient=True)

		            elif m == '/reflections':
		                if len(a) < 2:
			                bs.screenMessage('Usage: /reflections type(1/0) scale',color=(1,1,1), clients=[clientID], transient=True)
		                else:
		                    rs = [
		                     int(a[1])]
		                    typee = 'soft' if int(a[0]) == 0 else 'powerup'
		                    try:
		                        bsInternal._getForegroundHostActivity().getMap().node.reflection = typee
		                        bsInternal._getForegroundHostActivity().getMap().node.reflectionScale = rs
		                        print 'node'
		                    except:
		                        pass
		                    else:
		                        try:
		                            bsInternal._getForegroundHostActivity().getMap().bg.reflection = typee
		                            bsInternal._getForegroundHostActivity().getMap().bg.reflectionScale = rs
		                            print 'bg'
		                        except:
		                            pass
		                        else:
		                            try:
		                                bsInternal._getForegroundHostActivity().getMap().floor.reflection = typee
		                                bsInternal._getForegroundHostActivity().getMap().floor.reflectionScale = rs
		                                print 'floor'
		                            except:
		                                pass

		                        try:
		                            bsInternal._getForegroundHostActivity().getMap().center.reflection = typee
		                            bsInternal._getForegroundHostActivity().getMap().center.reflectionScale = rs
		                            print 'center'
		                        except:
		                            pass

		                    commandSuccess = True
		            elif m == '/shatter':
		                if a == []:
		                    bs.screenMessage('Usage: /shatter all number of list',color=(1,1,1), clients=[clientID], transient=True)
		                elif a[0] == 'all':
		                    for i in bsInternal._getForegroundHostActivity().players:
		                        i.actor.node.shattered = int(a[1])

		                    commandSuccess = True
		                else:
		                    bsInternal._getForegroundHostActivity().players[int(a[0])].actor.node.shattered = int(a[1])
		                    commandSuccess = True
		            elif m == '/cm':
		                if a == []:
		                    time = 8000
		                else:
		                    time = int(a[0])
		                    op = 0.08
		                    std = bs.getSharedObject('globals').vignetteOuter
		                    bsUtils.animateArray(bs.getSharedObject('globals'), 'vignetteOuter', 3, {0: bs.getSharedObject('globals').vignetteOuter, 17000: (0, 1, 0)})
		                try:
		                    bsInternal._getForegroundHostActivity().getMap().node.opacity = op
		                except:
		                    pass
		                else:
		                    try:
		                        bsInternal._getForegroundHostActivity().getMap().bg.opacity = op
		                    except:
		                        pass
		                    else:
		                        try:
		                            bsInternal._getForegroundHostActivity().getMap().bg.node.opacity = op
		                        except:
		                            pass
		                        else:
		                            try:
		                                bsInternal._getForegroundHostActivity().getMap().node1.opacity = op
		                            except:
		                                pass
		                            else:
		                                try:
		                                    bsInternal._getForegroundHostActivity().getMap().node2.opacity = op
		                                except:
		                                    pass

		                                try:
		                                    bsInternal._getForegroundHostActivity().getMap().node3.opacity = op
		                                except:
		                                    pass

		                            try:
		                                bsInternal._getForegroundHostActivity().getMap().steps.opacity = op
		                            except:
		                                pass

		                        try:
		                            bsInternal._getForegroundHostActivity().getMap().floor.opacity = op
		                        except:
		                            pass

		                    try:
		                        bsInternal._getForegroundHostActivity().getMap().center.opacity = op
		                    except:
		                        pass

		                def off():
		                    op = 1
		                    try:
		                        bsInternal._getForegroundHostActivity().getMap().node.opacity = op
		                    except:
		                        pass
		                    else:
		                        try:
		                            bsInternal._getForegroundHostActivity().getMap().bg.opacity = op
		                        except:
		                            pass
		                        else:
		                            try:
		                                bsInternal._getForegroundHostActivity().getMap().bg.node.opacity = op
		                            except:
		                                pass
		                            else:
		                                try:
		                                    bsInternal._getForegroundHostActivity().getMap().node1.opacity = op
		                                except:
		                                    pass
		                                else:
		                                    try:
		                                        bsInternal._getForegroundHostActivity().getMap().node2.opacity = op
		                                    except:
		                                        pass

		                                    try:
		                                        bsInternal._getForegroundHostActivity().getMap().node3.opacity = op
		                                    except:
		                                        pass

		                                try:
		                                    bsInternal._getForegroundHostActivity().getMap().steps.opacity = op
		                                except:
		                                    pass

		                            try:
		                                bsInternal._getForegroundHostActivity().getMap().floor.opacity = op
		                            except:
		                                pass

		                        try:
		                            bsInternal._getForegroundHostActivity().getMap().center.opacity = op
		                        except:
		                            pass

		                    bsUtils.animateArray(bs.getSharedObject('globals'), 'vignetteOuter', 3, {0: bs.getSharedObject('globals').vignetteOuter, 100: std})

		                bs.gameTimer(time, bs.Call(off))
		            elif m == '/help':
		                bs.screenMessage(bs.Lstr(resource='help1').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help2').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help3').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help4').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help5').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help6').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help7').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help8').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help9').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help10').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help11').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help12').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help13').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help14').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help15').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help16').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help17').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help18').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help19').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help20').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help21').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help22').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help23').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help24').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help25').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help26').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help27').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help28').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help29').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help30').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help31').evaluate())
		                bs.screenMessage(bs.Lstr(resource='help32').evaluate())
		            elif level > 3:
		                if m == '/partyname':
		                    if True:
		                        if a == []:
		                            bs.screenMessage('Usage: /partyname name of party',color=(1,1,1), clients=[clientID], transient=True)
		                        else:
		                            #print 'value of a[0] = ' + a[0]
		                            name = a[0].replace('_', ' ')
		                            try:
		                                bsInternal._setPublicPartyName(name)
		                                bs.screenMessage('Party name changed to "' + name + '"')
		                                commandSuccess = True
		                            except:
		                                bs.screenMessage('failed to change', clients=[clientID], transient=True)

		                elif m == '/settings':
		                    if a == []:
		                        bs.screenMessage('Usage: /settings numbers in list',color=(1,1,1), clients=[clientID], transient=True)
		                        bs.screenMessage('List of setting',color=(1,1,1), clients=[clientID], transient=True)
		                        bs.screenMessage('1. Shield on bomb',color=(1,1,1), clients=[clientID], transient=True)
		                        bs.screenMessage('2. Light on bomb',color=(1,1,1), clients=[clientID], transient=True)
		                        bs.screenMessage('3. Name on bomb',color=(1,1,1), clients=[clientID], transient=True)
		                        bs.screenMessage('4. Night mode',color=(1,1,1), clients=[clientID], transient=True)
		                    t = int(a[1])
		                    if a[0] == "1":
		                        cmdsetg.sB(t)
		                        commandSuccess = True
		                    if a[0] == "2":
		                    	cmdsetg.bL(t)
		                    	commandSuccess = True
		                    if a[0] == "3":
		                    	cmdsetg.bN(t)
		                    	commandSuccess = True
		                    if a[0] == "4":
		                    	cmdsetg.nM(t)
		                    	commandSuccess = True

		                elif m == '/public':
		                    if True:
		                        if a == []:
		                            bs.screenMessage('Usage /public 0 or 1',color=(1,1,1), clients=[clientID], transient=True)
		                        elif a[0] == '0':
		                            try:
		                                bsInternal._setPublicPartyEnabled(False)
		                                bs.screenMessage('Party is Private')
		                                commandSuccess = True
		                            except:
		                                bs.screenMessage('failed to change')

		                        elif a[0] == '1':
		                            try:
		                                bsInternal._setPublicPartyEnabled(True)
		                                bs.screenMessage('Party is Public')
		                                commandSuccess = True
		                            except:
		                                bs.screenMessage('failed to change')

		                        else:
		                            bs.screenMessage('Usage /public 0 or 1',color=(1,1,1), clients=[clientID], transient=True)
		                elif m == '/id':
		                    if True:
		                        clID = int(a[0])
		                        for i in bsInternal._getForegroundHostActivity().players:
		                            if i.getInputDevice().getClientID() == clID:
		                                bs.screenMessage(i.get_account_id())
		                                commandSuccess = True


		                elif m == '/customtag':
		                    if True:
		                        clID = int(a[0])
		                        for i in bsInternal._getForegroundHostActivity().players:
		                            if i.getInputDevice().getClientID() == clID:
		                                newadmin = i.get_account_id()
		                                if a[1] == 'add':
		                                    gph.customtagHashes.append(newadmin)
		                                    commandSuccess = True
		                                elif a[1] == 'remove':
		                                    if newadmin in gph.dragonHashes:
		                                        gph.customtagHashes.remove(newadmin)
		                                        commandSuccess = True

		                elif m == '/clear':
		                    if True:
		                        gph.customlist = []
		                        gph.customtagHashes = []
		                        gph.dragonHashes = []
		                        gph.adminHashes = []

		                elif m == '/white':
		                    if a != []:
		                        whiteId = None
					aid = None
		                        try:
		                            clID = int(a[0])
					    for i in bsInternal._getGameRoster():
						if i['clientID'] == clID:
						    aid = i['displayString']
		                            	    for i in bsInternal._getForegroundHostActivity().players:
		                                	if i.getInputDevice().getClientID() == clID:
		                                    	    whiteId = i.get_account_id()
		                                    	    name = i.getName()

		                            if aid is not None:
						gph.whitelist[whiteId] = aid
		                                with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
		                                    s = [ row for row in file ]
		                                    s[19] = 'whitelist = ' + str(gph.whitelist) + '\n'
		                                    f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py', 'w')
		                                    for i in s:
		                                        f.write(i)
		                                    f.close();reload(gph)
		                                commandSuccess = True
		                        except Exception:
		                            bs.screenMessage('player not found', clients=[clientID], transient=True)

		                elif m == '/ban':
		                    if a != []:
		                        bannedId = None
					aid = None
		                        try:
		                            clID = int(a[0])
					    for i in bsInternal._getGameRoster():
						if i['clientID'] == clID:
						    aid = i['displayString']
		                            	    for i in bsInternal._getForegroundHostActivity().players:
		                                	if i.getInputDevice().getClientID() == clID:
		                                    	    bannedID = i.get_account_id()
		                                    	    name = i.getName()

		                            if aid is not None:
						gph.banlist[bannedID] = aid
		                                with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
		                                    s = [ row for row in file ]
		                                    s[2] = 'banlist = ' + str(gph.banlist) + '\n'
		                                    f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py', 'w')
		                                    for i in s:
		                                        f.write(i)
		                                    f.close()
		                                bs.screenMessage('banned ' + name)
		                                bsInternal._disconnectClient(clID)
		                                commandSuccess = True
		                        except Exception:
		                            bs.screenMessage('player not found', clients=[clientID], transient=True)

		                elif m == '/custom':
		                    try:
		                        attributes = len(a)
		                        clID = int(a[0])
		                        for i in bsInternal._getForegroundHostActivity().players:
		                            if i.getInputDevice().getClientID() == clID:
		                                customer = i.get_account_id()
		                                if a[1] == 'add':
		                                    if customer in gph.customlist:
		                                        gph.customlist.pop(customer)
		                                    try:
		                                        if attributes > 2:
		                                            tag = a[2]
		                                            if '\\' in tag:
		                                                tag = tag.replace('\\d', ('\\ue048').decode('unicode-escape')) 	#Dragon
		                                                tag = tag.replace('\\c', ('\\ue043').decode('unicode-escape'))	#Crown	
		                                                tag = tag.replace('\\h', ('\\ue049').decode('unicode-escape'))	#Helmet
		                                                tag = tag.replace('\\s', ('\\ue046').decode('unicode-escape'))	#skull
		                                                tag = tag.replace('\\n', ('\\ue04b').decode('unicode-escape'))	#ninja star
		                                                tag = tag.replace('\\f', ('\\ue04f').decode('unicode-escape'))	#fireball
		                                            gph.customlist[customer] = tag
		                                            if attributes > 3:
		                                                if a[3] == 'permanent' and level > 5:
		                                                    with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
		                                                        s = [ row for row in file ]
		                                                        s[5] = 'customlist = ' + str(gph.customlist) + '\n'
		                                                        f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py', 'w')
		                                                        for i in s:
		                                                            f.write(i)

		                                                        f.close()
		                                    except:
		                                        print 'inside exception but adding into customHashes'
		                                        gph.customtagHashes.append(customer)

		                                    commandSuccess = True
		                                elif a[1] == 'remove':
		                                    if customer in gph.customtagHashes:
		                                        gph.customtagHashes.remove(customer)
		                                        commandSuccess = True
		                                    if customer in gph.customlist:
		                                        gph.customlist.pop(customer)
		                                        commandSuccess = True
		                                    if attributes > 2:
		                                        if a[2] == 'permanent':
		                                            with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
		                                                s = [ row for row in file ]
		                                                s[5] = 'customlist = ' + str(gph.customlist) + '\n'
		                                                f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py', 'w')
		                                                for i in s:
		                                                    f.write(i)

		                                                f.close()

		                    except:
		                        pass

		                elif m == '/whois':
					try:
						clID = int(a[0])
						ID = ''
				                for i in bsInternal._getForegroundHostActivity().players:
				                    if i.getInputDevice().getClientID() == clID:
				                        ID = i.get_account_id()
							name = i.getName(True,True)
						if ID is not '':
						    with open('logPlayers.json','r') as f:
							allPlayers = json.loads(f.read())
							allID = allPlayers[ID]
							string = 'Login ID of %s is:' %name
							for i in allID:
								#bs.screenMessage(i)
								string += '\n' + i
				                        	#commandSuccess = True
							bs.screenMessage(string, transient=True, color=(1, 1, 1), clients=[clientID])
					except:
						print 'who is exception'
							
		                elif m == '/text':
					from BsTextOnMap import texts
					if a == []:
						bs.screenMessage('Usage: /text showall or /text add [text] or /text del [textnumber]',color=(1,1,1), clients=[clientID], transient=True)
					elif a[0] == 'add' and len(a)>1:
						#get whole sentence from argument list
						newText = u''
						for i in range(1,len(a)):
							newText += a[i] + ' '
						#print newText
						texts.append(newText)

						#write to file
		                                with open(bs.getEnvironment()['systemScriptsDirectory'] + '/BsTextOnMap.py') as (file):
		                                    s = [ row for row in file ]
		                                    s[0] = 'texts = ' + str(texts) + '\n'
		                                    f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/BsTextOnMap.py', 'w')
		                                    for i in s:
		                                        f.write(i)
		                                    f.close()
						    commandSuccess=True
					elif a[0] == 'showall':
						for i in range(len(texts)):
							#print texts(i)
							bs.screenMessage(str(i) + '. ' + texts[i], clients=[clientID], transient=True)
						commandSuccess=True
					elif a[0] == 'del' and len(a)>1:
					    try:
						if len(texts) > 1:
							texts.pop(int(a[1]))
							#write to file
				                        with open(bs.getEnvironment()['systemScriptsDirectory'] + '/BsTextOnMap.py') as (file):
				                            s = [ row for row in file ]
				                            s[0] = 'texts = ' + str(texts) + '\n'
				                            f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/BsTextOnMap.py', 'w')
				                            for i in s:
				                                f.write(i)
				                            f.close()
							    commandSuccess=True
						else:
							bs.screenMessage("At least one text should be present",(1,0,0), clients=[clientID], transient=True)
					    except:
						pass
					else:
						bs.screenMessage('Usage: /text showall or /text add [text] or /text del [textnumber]',color=(1,1,1), clients=[clientID], transient=True)
		                elif m == '/whoinqueue':
				        def _onQueueQueryResult(result):
					    #print result, ' is result'
					    inQueue = result['e']
					    #print inQueue, ' is inQueue'
					    string = 'No one '
					    if inQueue != []:
						string = ''
						for queue in inQueue:
							#print queue[3]
							string += queue[3] + ' '
					    bs.screenMessage(string + 'is in the queue', clients=[clientID], transient=True)
							
					bsInternal._addTransaction(
						{'type': 'PARTY_QUEUE_QUERY', 'q': "p_S-l150a7a1d-0f12-43de-a3bf-467a7a5bcd72_1029295_13.233.116.32_43210"},
						callback=bs.Call(_onQueueQueryResult))
					bsInternal._runTransactions()					

                else:
                    bs.screenMessage('Failed', color=(1, 0, 0), clients=[clientID], transient=True)
        return


c = chatOptions()


def cmd(msg, clientID):
    c.opt(clientID, msg)
    if commandSuccess:
        if commandByCoin:
            coinSystem.addCoins(user, costOfCommand * -1)
            bs.screenMessage('Success! That cost you ' + bs.getSpecialChar('ticket') + str(costOfCommand), clients=[clientID], transient=True)
        else:
	  try:
		with bs.Context(bsInternal._getForegroundHostActivity()):
			bs.screenMessage(reply, color=(0.1,1,0.1))
            		#bs.screenMessage(reply)
	  except:
		pass
    return
