# Create your views here.
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response,render, get_object_or_404
import webescrow.escrowhandler as escrowhandler
import settings as settings
import os
from webescrow.forms import TransactionForm
from webescrow.models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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

def landing_page(request):
    '''
    handles the index page , loads homepage when user is logged in
    @request  request object
    '''	
    if request.user.is_authenticated():
        return home_page(request)
    return render_view(request,'index.html',{})

@login_required
def home_page(request):
    '''
    serves the escrow app , when the user is logged in
    @request  request object
    '''
    errors, result, notification =(' ',False,{})
    if not os.path.exists(settings.SSSS_SPLIT):
        raise Exception("%s doesn't exist, check settings.py" % settings.SSSS_SPLIT)
    if request.method == "POST":
        post_values = request.POST.copy()
        post_values['user'] = request.user.pk
        post_values['added'] = datetime.now().date()
        post_values['is_complete'] = False
        #post_values['expires'] = 0;
        form = TransactionForm(post_values)   
        if form.is_valid():
            transaction = form.save()
            response = escrowhandler.post_handler(request.POST, request);
            if response:
                messages.success(request, 'The Escrow was successfully created.')
        else:
            print form.errors
            messages.error(request, form.errors)
    return render_view(request,'home.html',{'TransactionForm':TransactionForm,
        'escroweremail':settings.ESCROWER_EMAIL})


@login_required
def list_transactions(request):
    '''
    List transactions
    @request  request object
    '''
    if not request.user.is_authenticated:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
    transactions = Transaction.objects.all().filter(user=request.user.pk) 
    return render_view(request,'transactions.html',
        {'transactions':transactions}
        )


@login_required
def list_transaction(request,name):
    '''
    List transactions
    @request  request object
    @name string transaction hashed name
    '''
    id = int(name)^0xABCDEFAB
    transactions = get_object_or_404(Transaction.objects.filter(id=id),id=id)
    return render_view(request,'transaction.html',
        {'transaction':transactions},
        )

@login_required
def add_complaint(request):
    '''
    Add Complaint
    @request request object()
    '''
    #transactions = Transaction.objects.values_list('id', flat=True).filter(user=request.user.pk)
    transactions = Transaction.objects.all().filter(user=request.user.pk) 
    print transactions 
    return render_view(request,'complaint.html',
        {'transactions':transactions},
        )
