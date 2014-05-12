from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Game(models.Model):				#Overall Game Object
	name = models.CharField(max_length=200)		#name of the game
	start_time = models.DateTimeField()		#time to start
	end_time = models.DateTimeField()		#time game ends
	active = models.IntegerField(default=1)		#is the game active
	require_regcodes = models.IntegerField(default=0) #does the game require reg codes
	def __unicode__(self):
		return self.name





class Category(models.Model):				#categories for challegnes
	game = models.ForeignKey(Game)			#in which game
	name = models.CharField(max_length=200)		#name of the category
	
	def __unicode__(self):
                return self.name





class Challenge(models.Model):				#CTF challenges
	game = models.ForeignKey(Game)                  #in which game
	category = models.ForeignKey(Category)		#Category Associated
	name = models.CharField(max_length=200)		#Name of the challenge
	description = models.CharField(max_length=2000)	#description , pointers etc
	points = models.IntegerField(default=100)	#point value for the challenge
	active = models.IntegerField(default=0)		#is the challenge active
	key = models.CharField(max_length=200)		#scoring key for the challenge

	def __unicode__(self):
                return self.name



class Hint(models.Model):				#hints to be displayed for a given challenge
	game = models.ForeignKey(Game)                  #in which game
	challenge = models.ForeignKey(Challenge)	#challenge
	text = models.CharField(max_length=2000)	#hint text
	active = models.IntegerField(default=0)		#is the hint active

	def __unicode__(self):
                return self.text

class RegCodes(models.Model):				# valid once reg codes 
	code = models.CharField(max_length=200, null=True, blank=True) #codes
	used = models.IntegerField(default=0)				#is it used?

	def __unicode__(self):
		return self.code


class Competitor(models.Model):				#hold competiors (may extend the auth_user, dunno)
	game = models.ForeignKey(Game)                  #in which game
	user = models.OneToOneField(User)
	display_name = models.CharField(max_length=200)	#name to display
	affiliation = models.CharField(max_length=200, null=True, blank=True)	#affiliation text to display
	url = models.CharField(max_length=200, null=True, blank=True)		#url
	bad_keys = models.IntegerField(default=0)	#how many bad keys have they submitted
	points = models.IntegerField(default=0)		#current point total
	active = models.IntegerField(default=1)		#is the competitor active (ie allowed to play, score, count in standings)
	ipaddr = models.CharField(max_length=200, null=True, blank=True) #ip the competitor reged from
	regcode = models.ForeignKey(RegCodes, null=True) #code the competitor used to reg				   
	def __unicode__(self):
                return self.display_name



class Solved(models.Model):				#challenges solved
	game = models.ForeignKey(Game)                  #in which game
	competitor = models.ForeignKey(Competitor)	#by whom	
	challenge = models.ForeignKey(Challenge)	#which challenge
	points = models.IntegerField(default=0)		#how many points they got
	time = models.DateTimeField()			#when they did it

	

