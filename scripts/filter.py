import bs
import bsInternal
import settings

f_words= ['cum','cumshot','boob','boobies','tit','titz','fuck','fucker','shit','shithead','pussy','PuSSy','fucked','bitch','bitches','bietch','sex','Sex','bastard','Fuck','Fucker','Cum','Bitch']

name_filter = ['cum','cumshot','boob','boobies','tit','titz','fuck','fucker','shit','shithead','pussy','PuSSy','fucked','bitch','bitches','bietch','sex','Sex','bastard','Fuck','Fucker','Cum','Bitch']

warndict = {}

def k(cid):
	if cid in warndict:
		print(cid,"Already Exsist")
	else:
		warndict.update({cid:0})

def check(cid):
	global warndict
	if settings.enableChatFilter:
		if warndict[cid] == 1:
			bsInternal._disconnectClient(int(cid))
			bs.screenMessage("Kicking For Misbehave", color = (1,1,1), transient=True, clients=[clientID])
			warndict.pop(cid)
		elif warndict[cid] == 0:
			warndict[cid] = 1

def warn(clientID):
	if settings.enableChatFilter:
		bs.screenMessage("Warning!!! Do Not Misbehave", color = (1,1,1), transient=True, clients=[clientID])
    	if warndict[clientID] == 0:
    		bs.screenMessage("Last Chance Warning 1/2", color = (1,1,1), transient=True, clients=[clientID])
