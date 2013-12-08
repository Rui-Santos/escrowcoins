# Create your views here.
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response



def render_view(request,template,data):
	return render_to_response(
        template,data,
        context_instance=RequestContext(request)
    )

def landingpage(request):
    #if request.user.is_authenticated():
    #    return HttpResponseRedirect(settings.BASE_URL+"home")
    #return render(request,'index.html')
    return render_view(request,'index.html',{})


def testingpage(request):
	from django.core.mail import send_mail
	send_mail('Testing Email', 'Here is the message.', 'madradavid@yahoo.com',['madradavid@yahoo.com'], fail_silently=False)
	return render_view(request,'test.html',{})

