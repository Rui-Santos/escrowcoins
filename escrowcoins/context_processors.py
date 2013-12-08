from django.conf import settings


def global_vars(request):
	LOGGED_IN = False
	if request.user.is_authenticated():
		LOGGED_IN = True
	return{'APP_NAME': settings.APP_NAME,'BASE_URL':settings.BASE_URL,'LOGGED_IN':LOGGED_IN}
