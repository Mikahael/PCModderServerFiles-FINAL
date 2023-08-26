import bs
import bsInternal
import settings

f_words= ['cum','cumshot','boob','boobies','tit','titz','fuck','fucker','shit','shithead','pussy','PuSSy','fucked','bitch','bitches','bietch','sex','Sex','bastard','Fuck','Fucker','Cum','Bitch']

name_filter = ['cum','cumshot','boob','boobies','tit','titz','fuck','fucker','shit','shithead','pussy','PuSSy','fucked','bitch','bitches','bietch','sex','Sex','bastard','Fuck','Fucker','Cum','Bitch']

warndict = {}

def check_id(cid):
    client = ''
    player_name = ''
    for i in bsInternal._getForegroundHostSession().players:
        if i.getInputDevice().getClientID() == cid:
            client = i.get_account_id()
            player_name = i.getName()
    return player_name

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
            player_name = check_id(cid)  # Corrected indentation
            #bs.screenMessage("Have a good day! ---> "+player_name, color=(1, 1, 1), transient=True, clients=[cid])
            bs.screenMessage(player_name+' ---> Kicked for violating chat filter', color=(1, 1, 1), transient=True)
            warndict.pop(cid)
        elif warndict[cid] == 0:
            warndict[cid] = 1

def warn(cid):
    if warndict[cid] == 0:
        bs.screenMessage("Warning!! Last Chance!", color = (1,1,1), transient=True, clients=[cid])
