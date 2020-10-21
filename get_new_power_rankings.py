import numpy as np
from espn_api.football import League

def get_new_power_rankings(league,week=week):
    '''This script gets power rankings, given an already-connected league and a week to look at. Requires espn_api, numpy'''
    
    #Get what week most recently passed
    lastWeek = league.current_week
	
    if week:
        lastWeek = week
    
    #initialize dictionaries to stash the projected record/expected wins for each week, and to stash each team's score for each week
    projRecDicts = {i: {x: None for x in league.teams} for i in range(lastWeek)}
    teamScoreDicts = {i: {x: None for x in league.teams} for i in range(lastWeek)}
    
    #initialize the dictionary for the final power ranking
    powerRankingDict = {x: 0. for x in league.teams}
    
    
    for i in range(lastWeek): #for each week that has been played
        weekNumber = i+1      #set the week
        boxes = league.box_scores(weekNumber)	#pull box scores from that week
        for box in boxes:							#for each boxscore
            teamScoreDicts[i][box.home_team] = box.home_score	#plug the home team's score into the dict
            teamScoreDicts[i][box.away_team] = box.away_score	#and the away team's
            
        for team in teamScoreDicts[i].keys():		#for each team
            wins = 0
            losses = 0
            ties = 0
            oppCount = len(list(teamScoreDicts[i].keys()))-1	
            for opp in teamScoreDicts[i].keys():		#for each potential opponent
                if team==opp:							#skip yourself
                    continue
                if teamScoreDicts[i][team] > teamScoreDicts[i][opp]:	#win case
                    wins += 1
                if teamScoreDicts[i][team] < teamScoreDicts[i][opp]:	#loss case
                    losses += 1
                    
            if wins + losses != oppCount:			#in case of an unlikely tie
                ties = oppCount - wins - losses
                
            projRecDicts[i][team] = (float(wins) + (0.5*float(ties)))/float(oppCount) #store the team's projected record for that week
            
    for team in powerRankingDict.keys():			#for each team
        powerRankingDict[team] = np.sum(np.array([projRecDicts[i][team] for i in range(lastWeek)]))/float(lastWeek) #total up the expected wins from each week, divide by the number of weeks
        
    powerRankingDictSortedTemp = {k: v for k, v in sorted(powerRankingDict.items(), key=lambda item: item[1],reverse=True)} #sort for presentation purposes
    powerRankingDictSorted = {x: ('{:.3f}'.format(powerRankingDictSortedTemp[x])) for x in powerRankingDictSortedTemp.keys()}  #put into a prettier format
    return [(powerRankingDictSorted[x],x) for x in powerRankingDictSorted.keys()]    #return in the format that the bot expects