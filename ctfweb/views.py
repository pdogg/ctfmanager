from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, loader
from ctfweb.models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, views
from ctfweb.support import *


def index(request):
	return HttpResponse("You shouldn't be here... Go to http://ctfboard.ctf/ and start over please...")



def allchallenges(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/ctfweb/login/")    
	else:
		auth_player = currentplayer(request)	   
       
	if not gameisrunning(currentgame()):
		return genericerror(request, "Game Not Running!")

        category_list = Category.objects.order_by("name")

	return render(request, "ctfweb/challenges.html", {'category_list': category_list, 'auth_player': auth_player})



def challenge(request, challenge_id):

        if not gameisrunning(currentgame()):
                return genericerror(request, "Game Not Running!")

        if not request.user.is_authenticated():
                return HttpResponseRedirect("/ctfweb/login/")
        else:
                auth_player = currentplayer(request)

	
	chall = get_object_or_404(Challenge, pk=challenge_id)
	numsolved = Solved.objects.filter(challenge=chall, competitor=auth_player)

	if numsolved:
		unsolved = False
	else:
		unsolved = True

	try:
	   hints = Hint.objects.filter(challenge=challenge_id, active=1)
	except Hint.DoesNotExist:
	   hints = 0

	return render(request, 'ctfweb/challenge.html', {'chall': chall, 'hints' : hints, 'unsolved': unsolved})


def competitordetail(request, comp_id):
	if not gameisrunning(currentgame()):
                return genericerror(request, "Game Not Running!")

        if not request.user.is_authenticated():
                return HttpResponseRedirect("/ctfweb/login/")
        else:
                auth_player = currentplayer(request)

	competitor = get_object_or_404(Competitor, pk=comp_id)
	numsolved = Solved.objects.filter(competitor=competitor).count()
	
	if numsolved:
		solved_list=Solved.objects.filter(competitor=competitor)
	else:
		solved_list=''

	
	return render(request, 'ctfweb/competitordetail.html', {'numsolved': numsolved, 'competitor': competitor, 'solved_list': solved_list})
		






def submitkey(request, challenge_id):
	
        if not gameisrunning(currentgame()):
                return genericerror(request, "Game Not Running!")
        if not request.user.is_authenticated():
                return HttpResponseRedirect("/ctfweb/login/")
        else:
                auth_player = currentplayer(request)


	chall = Challenge.objects.get(id=challenge_id)
	
	if chall:
	   if chall.active:
	     if washstring(chall.key) == washstring(request.POST['keysubmit']) :

                if not hassolved(auth_player, chall):

			solve(auth_player, chall)
			return genericerror(request, "Correct Key! Challenge : " + chall.name + " solved\n " + str(chall.points) + " points awarded!")
			
		else:
			return genericerror(request, "Already Solved")

             else:

		comp = auth_player
		comp.bad_keys += 1
		comp.save()
                return genericerror(request, "Bad Key!") 	
	
	   else: #not active
	     return genericerror(request, "Not active! Go Away")

	else:
	     return genericerror(request, "No challenge by that name! Go Away")



def scoreboard(request):
	score_list = Competitor.objects.order_by('points').exclude(active=0).reverse()
	game = currentgame()
	now = datetime.datetime.now()
	if now < game.start_time:
		status = " not running yet! Starts in: " + str(game.start_time - now)
	else:
		if now > game.end_time:
			status = "Game Over!"
		else:
			status = str(game.end_time - now) + " remaining"


	return render(request, "ctfweb/scoreboard.html", {'score_list': score_list, 'status' : status})

	

def genericerror(request, errorstring):
	return render(request, "ctfweb/genericerror.html", {'errorstring': errorstring})


def registerform(request):
	
	if request.user.is_authenticated():
                return genericerror(request, "You're already authenticated... GTFO")
        else:
                game = currentgame()
		return render(request, "ctfweb/registerform.html", {'usingregcodes': game.require_regcodes})



def registerformerror(request, fieldstring):
	game = currentgame()
        errorrecall = True
	if request.user.is_authenticated():
                return genericerror(request, "You're already authenticated... GTFO")
        else:
		return render(request, "ctfweb/registerform.html", {'fieldstring': fieldstring, 'errorrecall': errorrecall, 'usingregcodes': game.require_regcodes})

	

def registerprocess(request):
	game = currentgame()
	error = False
	errorstring =''

	if request.POST['username'] == '':
		errorstring += ' username'
		error=True
	

	if request.POST['password'] == '':
                errorstring += ' password'
                error=True

	if request.POST['passwordconfirm'] == '':
                errorstring += ' passwordconfirm'
                error=True

	if request.POST['displayname'] == '':
                errorstring += ' displayname'
                error=True

	if (len(request.POST['displayname']) >= 50) or (len(request.POST['affiliation']) >= 50) :
		errorstring += ' really long displayname or affiliation - be nice'
		error=True

	if request.POST['email'] == '':
                errorstring += ' email'
                error=True

	if request.POST['passwordconfirm'] != request.POST['password'] :
                errorstring += ' ** password confirmation does not match password**'
                error=True

	
	
	if User.objects.filter(username__exact=request.POST['username']).count():
			errorstring += ' duplicate username: ' + request.POST['username']
			error=True	
  	
	if game.require_regcodes :
		try:
		   	code = RegCodes.objects.get(code=request.POST['regcode'])
		        if code.used :
        	                errorstring += ' registration code has been used'
	                        error = True

		except RegCodes.DoesNotExist:
			errorstring += ' invalid registration code'
			error = True
			
	

	if Competitor.objects.filter(display_name=request.POST['displayname']).count():
			errorstring += " duplicate displayname: " + request.POST['displayname']
			error=True
	

	if error:
		return registerformerror(request, errorstring)
	else:
		user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
		comp = Competitor(game=currentgame(), user=user, display_name=request.POST['displayname'], affiliation=request.POST['affiliation'], url=request.POST['url'], points=0, bad_keys=0, active=1, ipaddr=get_client_ip(request), regcode=None)
		if game.require_regcodes and code :
			comp.regcode = code
			code.used = 1
			code.save()
		comp.save()
		return genericerror (request, "User Created - Please Login")


def logout_view(request):
	logout(request)	
	return genericerror(request, "Logged Out...")

		
# Create your views here.
