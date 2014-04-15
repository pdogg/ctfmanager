
from django import template
from ctfweb.models import *

register = template.Library()

@register.filter
def filthassolved(comp, chall):
#given a competitor and challenge
#return True if the competitor has solced the challenge
#return False if the competitor has NOT solved the challenge
	print comp
	print chall
        if Solved.objects.filter(challenge=chall, competitor=comp).count():
                return True
        else:
                return False

