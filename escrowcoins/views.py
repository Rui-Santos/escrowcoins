# Create your views here.
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response
import webescrow.escrowhandler as escrowhandler
import settings as settings
import os
from webescrow.forms import TransactionForm
from webescrow.models import *
from datetime import datetime

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
        post_values = request.POST.copy()
        post_values['user'] = request.user.pk
        post_values['added'] = datetime.now().date()
        print datetime.now().date()
        form = TransactionForm(post_values)   
        if form.is_valid():
            transaction = form.save()
            print transaction 
            #escrowhandler.post_handler(request.POST);
        else:
            errors = form.errors
    return render_view(request,'home.html',{'TransactionForm':TransactionForm,
        'escroweremail':settings.ESCROWER_EMAIL,
        'errors':errors}
        )


def listtransactions(request):
    '''
    List transactions
    '''
    if not request.user.is_authenticated:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
    transactions = Transaction.objects.all().filter(user=request.user.pk)
    print transactions
    return render_view(request,'transactions.html',{'transactions':transactions}
        )