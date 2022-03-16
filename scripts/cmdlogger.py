import bsInternal#made by blitz
def log(msg,clientID):
    for i in bsInternal._getForegroundHostActivity().players:
        if i.getInputDevice().getClientID()==clientID:#not used. PCModder has made better one.
            client=i.get_account_id()
            name=i.getName()
	f = open("log.txt","a")
	f.write(name+"----->"+client+"------>"+ msg+"\n")
	f.close()
