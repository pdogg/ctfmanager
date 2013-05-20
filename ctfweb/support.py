from ctfweb.models import *
import datetime

GAME = 1


def currentgame():
# returns an instance of the current game
	try:
		gameinstance = Game.objects.get(id=GAME)
	except Game.DoesNotExist:
		print "DEBUG BAD STUFF - NO CURRENT GAME!"
		return False
	return gameinstance


def gameisrunning(game):
	
	now = datetime.datetime.now()
	startime = game.start_time
	endtime = game.end_time
	
	if (now < startime) or (now > endtime) :
		return False
	else:
		return True

def currentplayer(request):
#returs a competitor instance for the current player
        if not request.user.is_authenticated():
                print "DEBUG BAD STUFF - currentplayer called with no current player authenticated... this will end poorly"

	
        try:
                compinstance = Competitor.objects.get(user=request.user.id)
        except Competitor.DoesNotExist:
                print "DEBUG BAD STUFF - NO CURRENT COMPETITOR FOR AUTH USER " + request.user.username
                return False
        return compinstance


def hassolved(comp, chall):
#given a competitor and challenge
#return True if the competitor has solced the challenge
#return False if the competitor has NOT solved the challenge
 	
        if Solved.objects.filter(challenge=chall, competitor=comp).count():
		return True
	else:
		return False



def solve(comp, chall):
#called when competitor comp solves a challenge chall objects
#handles scoreing and updates Solved - returns True if all goes well
	
	if not hassolved(comp, chall):

	   if comp.active and chall.active :
	   
 	      comp.points += chall.points
              comp.save()
              solvedrecord = Solved(game=currentgame(), competitor=comp, challenge=chall, points=chall.points, time=datetime.datetime.now())
	      solvedrecord.save()

	   else:
		print "DEBUG BAD STUFF support.solve - " + comp + " " + chall + " Something NOT ACTIVE - Doing nothing! "
                return False
	

	else:
	    	print "DEBUG BAD STUFF support.solve - Competitor " + comp + " already solved " + chall + " DUPLICATE SOLVE - Doing nothing! "
		return False

def washstring(string):
# return a lowercased string with specail characters removed
	outstring = ''.join(e for e in string if e.isalnum())
	return outstring.lower()
