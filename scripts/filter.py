import bs
import bsInternal
import settings

f_words = ["fuck","shit","tits","nigg","69","bastard","cum"]

name_filter = ['cum','cumshot','boob','tit','titz','fuck','fucker','shit','shithead','pussy','PuSSy','fucked','bitch','bitches','bietch','sex','Sex','bastard','Fuck','Fucker','Cum','Bitch','devil','luci']

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
			bs.screenMessage("Kicking For Misbehave", color = (1,0,0))
			warndict.pop(cid)
		elif warndict[cid] == 0:
			warndict[cid] = 1

def warn(clientID):
	if settings.enableChatFilter:
		bs.screenMessage("Warning!!! Do Not Misbehave", color = (1,0,0), transient=True, clients=[clientID])
    	if warndict[clientID] == 0:
    		bs.screenMessage("Last Chance Warning 1/2", color = (1,0,0), transient=True, clients=[clientID])
