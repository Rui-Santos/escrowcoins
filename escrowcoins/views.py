# Create your views here.
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response
import webescrow.escrowhandler as escrowhandler
import settings as settings
import os
from webescrow.forms import TransactionForm

def render_view(request,template,data):
    '''
    wrapper for rendering views , loads RequestContext
    @request  request object
    @template  string
    @data  tumple
    '''
    return render_to_response(
        template,data,
        context_instance=RequestContext(request)
        )

def landingpage(request):
    '''
    handles the index page , loads homepage when user is logged in
    @request  request object
    '''	
    if request.user.is_authenticated():
        return homepage(request)
    return render_view(request,'index.html',{})

def homepage(request):
    '''
    serves the escrow app , when the user is logged in
    @request  request object
    '''
    errors, result =(' ',False)
    if not os.path.exists(settings.SSSS_SPLIT):
        raise Exception("%s doesn't exist, check settings.py" % settings.SSSS_SPLIT)
    if request.method == "POST":
        form = TransactionForm(request.POST)   
        if form.is_valid():
            escrowhandler.post_handler(request.POST);
        else:
            errors = form.errors
    return render_view(request,'home.html',{'TransactionForm':TransactionForm,
        'escroweremail':settings.ESCROWER_EMAIL,
        'errors':errors}
        )

