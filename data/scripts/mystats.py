"""
mystats module for BombSquad version 1.4.143
Provides functionality for dumping player stats to disk between rounds.
To use this, add the following 2 lines to bsGame.ScoreScreenActivity.onBegin():
import mystats
mystats.update(self.scoreSet) 
"""
import threading
import json
import os
import urllib2
import bs
# where our stats file and pretty html output will go
statsfile = bs.getEnvironment()['systemScriptsDirectory'] + "/stats.json"
htmlfile = 'index.html'


def refreshStats():
        # lastly, write a pretty html version.
        # our stats url could point at something like this...
        with open(statsfile) as f:
            stats = json.loads(f.read())

        f=open(htmlfile, 'w')       
	f.write('<head><meta charset="UTF-8"><title>Stats for BROTHERS IN ARMS </title></head><body>\n<table style="width:80%"><tr><td><b>Name</b></td><td><b>Score</b></td><td><b>Kills</b></td><td><b>Deaths</b></td></tr><br>')
        json_data = {}
        entries = [(a['scores'], a['kills'], a['deaths'], a['name_html'],
                     a['games'], a['aid']) for a in stats.values()]
        # this gives us a list of kills/names sorted high-to-low
        entries.sort(reverse=True)
        rank = 0
        toppers = {}
        pStats = {}
	toppersIDs=[]
        for entry in entries:
            rank += 1
            scores = str(entry[0])            
            kills = str(entry[1])
            deaths = str(entry[2])
            name = entry[3].encode('utf-8')            
            games = str(entry[4])
            aid = str(entry[5])            
            if rank < 6:
		toppersIDs.append(aid)
            pStats[str(aid)] = {"rank": str(rank),
                                "scores": str(scores),
                                "games": str(games),
                                "deaths": str(deaths),
                                "kills": str(kills)}
            """try:
                kd = str(float(kills) / float(deaths))[:3]
            except Exception:
                kd = "0.0"
            try:
                average_score = str(float(scores) / float(games))[:3]
            except Exception:
                average_score = "0"  """
	    f.write('\n<tr><td>'+name+'</td><td>'+scores+'</td><td>'+kills+'</td><td>'+deaths+'</td></tr>')
	f.write('</body>')
	f.close()
        f2 = open(bs.getEnvironment()['systemScriptsDirectory'] + "/pStats.json", "w")
        f2.write(json.dumps(pStats))
        f2.close()
	import settings
	if settings.enableTop5commands:
		import getPermissionsHashes as gph
		gph.topperslist = toppersIDs
		"""
		with open(bs.getEnvironment()['systemScriptsDirectory'] + "/getPermissionsHashes.py") as file:
			s = [row for row in file]
			s[3] = 'topperslist = ' + str(toppersIDs) + '\n'
			f = open(bs.getEnvironment()['systemScriptsDirectory'] + "/getPermissionsHashes.py",'w')
			for i in s:
				f.write(i)
			f.close()"""


def update(score_set):
    """
    Given a Session's ScoreSet, tallies per-account kills
    and passes them to a background thread to process and
    store.
    """ 
    # look at score-set entries to tally per-account kills for this round

    account_kills = {}
    account_deaths = {}
    account_scores = {}

    for p_entry in score_set.getValidPlayers().values():
        account_id = p_entry.getPlayer().get_account_id()
        if account_id is not None:
            account_kills.setdefault(account_id, 0)  # make sure exists
            account_kills[account_id] += p_entry.accumKillCount
            account_deaths.setdefault(account_id, 0)  # make sure exists
            account_deaths[account_id] += p_entry.accumKilledCount
            account_scores.setdefault(account_id, 0)  # make sure exists
            account_scores[account_id] += p_entry.accumScore
    # Ok; now we've got a dict of account-ids and kills.
    # Now lets kick off a background thread to load existing scores
    # from disk, do display-string lookups for accounts that need them,
    # and write everything back to disk (along with a pretty html version)
    # We use a background thread so our server doesn't hitch while doing this.
    UpdateThread(account_kills, account_deaths, account_scores).start()

class UpdateThread(threading.Thread):
    def __init__(self, account_kills, account_deaths, account_scores):
        threading.Thread.__init__(self)
        self._account_kills = account_kills
        self.account_deaths = account_deaths
        self.account_scores = account_scores
    def run(self):
        # pull our existing stats from disk
        if os.path.exists(statsfile):
            with open(statsfile) as f:
                stats = json.loads(f.read())
        else:
            stats = {}
            
        # now add this batch of kills to our persistant stats
        for account_id, kill_count in self._account_kills.items():
            # add a new entry for any accounts that dont have one
            if account_id not in stats:
                # also lets ask the master-server for their account-display-str.
                # (we only do this when first creating the entry to save time,
                # though it may be smart to refresh it periodically since
                # it may change)
                url = 'http://bombsquadgame.com/accountquery?id=' + account_id
                response = json.loads(
                    urllib2.urlopen(urllib2.Request(url)).read())
                name_html = response['name_html']
                stats[account_id] = {'kills': 0, 'deaths': 0, 'scores': 0, 'name_html': name_html,
                                     'games': 0, 'aid': ""}
            # now increment their kills whether they were already there or not
            stats[account_id]['kills'] += kill_count
            stats[account_id]['deaths'] += self.account_deaths[account_id]
            stats[account_id]['scores'] += self.account_scores[account_id]
            # also incrementing the games played and adding the id
            stats[account_id]['games'] += 1
            stats[account_id]['aid'] = str(account_id)
	# dump our stats back to disk
	with open(statsfile, 'w') as f:
	    f.write(json.dumps(stats))
	# aaand that's it!  There IS no step 27!
        print 'Added', len(self._account_kills), ' account\'s stats entries.'
 
	refreshStats()


 
