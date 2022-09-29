import bs,bsInternal
import random
from setchat import *
#you will need settings.py from our repository
inx = 0
def message():
    global inx
    if allow:
    	bsInternal._chatMessage(messageList[inx])
    	if inx < len(messageList):
        	inx+= 1
    	if inx == len(messageList):
        	inx = 0
CMT = chatMessageTime*1000
timer = bs.Timer(CMT,message,timeType='real',repeat=True)
