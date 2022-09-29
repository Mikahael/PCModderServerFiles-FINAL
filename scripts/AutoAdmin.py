import json
import getPermissionsHashes as gph
import bs

old_admin = gph.adminHashes
old_vip = gph.vipHashes

#Gives Admin To Rank 1
def admin(val):
    fi = open(bs.getEnvironment()['systemScriptsDirectory'] + '/pStats.json', 'r')
    pats = json.loads(fi.read())
    for pb_id in pats:
        rank_check = pats[pb_id]["rank"]
        if int(rank_check) == int(val):
            key1 = list(pats.keys())
            for i in key1:
                if pats[i]["rank"] == val:
                    old_admin.append(i)
                    new_admin = old_admin
    with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
        s = [ row for row in file ]
        s[0] = 'adminHashes = '+ str(new_admin) + '\n'
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py','w')
        for i in s:
            f.write(i)
        f.close()
    bs.screenMessage("Admins Updated",color = (0,1,0))

#Gives Vip To Rank 2
def vip(val):
    fi = open(bs.getEnvironment()['systemScriptsDirectory'] + '/pStats.json', 'r')
    pats = json.loads(fi.read())
    for pb_id in pats:
        rank_check = pats[pb_id]["rank"]
        if int(rank_check) == int(val):
            key1 = list(pats.keys())
            for i in key1:
                if pats[i]["rank"] == val:
                    old_vip.append(i)
                    new_vip = old_vip
    with open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py') as (file):
        s = [ row for row in file ]
        s[1] = 'vipHashes = '+ str(new_vip) + '\n'
        f = open(bs.getEnvironment()['systemScriptsDirectory'] + '/getPermissionsHashes.py','w')
        for i in s:
            f.write(i)
        f.close()
    bs.screenMessage("Vips Updated",color = (0,1,0))


#bs.getEnvironment()['systemScriptsDirectory'] + '/pStats.json'
"""
    fi = open(bs.getEnvironment()['systemScriptsDirectory'] + '/pStats.json', 'r')
    pats = json.loads(fi.read())
    for pb_id in pats:
        rank_check = pats[pb_id]["rank"]
        if int(rank_check) == 1:
            key1 = list(pats.keys())
            for i in key1:
                if pats[i]["rank"] == "1":
                    old_admin.append(i)
                    new_admin = old_admin
"""


