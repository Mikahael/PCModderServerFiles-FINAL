import bs
import bsInternal
#import settings

f_words = ["mc","bc","fuck","bsdk",'shit','puto','chutiya','bitch','pussy']

enableChatFilter = True

warndict = {}

def k(cid):
	if cid in warndict:
		print(cid,"Already Exsist")
	else:
		warndict.update({cid:0})

def check(cid):
	global warndict
	if enableChatFilter:
		if warndict[cid] == 1:
			bsInternal._disconnectClient(int(cid))
			bs.screenMessage("Server kicking Abuser", color = (1,1,1))
			warndict.pop(cid)
		elif warndict[cid] == 0:
			warndict[cid] = 1

def warn(clientID):
	if enableChatFilter:
		bs.screenMessage("Kindly do not say bad words", color = (1,1,1), transient=True, clients=[clientID])
    	if warndict[clientID] == 0:
    		bs.screenMessage("Dont Repeat Please 1/2", color = (1,1,1), transient=True, clients=[clientID])