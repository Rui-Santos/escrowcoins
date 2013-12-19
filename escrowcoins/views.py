# Create your views here.
from django.template import Template, context, RequestContext
from django.shortcuts import render_to_response,render, get_object_or_404
from django.http import HttpResponseNotFound
import webescrow.escrowhandler as escrowhandler
import settings as settings
import os
from webescrow.forms import TransactionForm
from webescrow.models import *
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from webescrow import mailer


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
        post_values['expires'] = datetime.now().date();
        if not 'encypt_emails' in post_values:
            post_values['encypt_emails'] = False
        form = TransactionForm(post_values)   
        if form.is_valid():
            transaction = form.save()
            #response = escrowhandler.post_handler(post_values, request);
            if post_values['is_sender']:
                email = post_values['buyer']
                role = 'Seller'
            else:
                email = post_values['seller']
                role = 'Buyer'
            escrow_link = settings.BASE_URL+''+transaction.get_unique_url()+'agreeterms'
            """Send an email asking the user to agree terms"""
            response = mailer.agreeTermsEmail(email,role,escrow_link,post_values['helptext'])
            if response:
                messages.success(request, 'The Escrow was successfully created , An email was sent to %s , once they agree to the Escrow terms you will be notified and the escrow will be marked active.'% email)
        else:
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
def transaction_agree_terms(request,name):
    '''
    Agree transaction terms
    @request  request object
    @name string transaction hashed name
    '''
    id = int(name)^0xABCDEFAB
    transaction = get_object_or_404(Transaction.objects.filter(id=id),id=id)
    '''Terms have already been agreed , we relocate'''
    f04 = False
    print transaction
    if transaction.terms_agreed:
        f04 = True
    if transaction.is_sender:
        if transaction.sender == request.user.email:
            f04 = True
    else:
        if transaction.buyer == request.user.email:
            f04 = True 
    if f04:
        return HttpResponseNotFound('<h1>No Page Here</h1>')
    if request.method == "POST":
        post_values = request.POST.copy()
        if post_values['agree_terms']:
            '''user has agreed to terms ,do ahead and create shares'''
            response = escrowhandler.post_handler(post_values, request);
        else:
            '''user has not agreed terms ,figure out what to do'''
            pass
    return render_view(request,'agree_transaction.html',
        {'transaction':transaction},
        )


@login_required
def add_complaint(request):
    '''
    Add Complaint
    @request request object()
    '''
    #transactions = Transaction.objects.values_list('id', flat=True).filter(user=request.user.pk)
    transactions = Transaction.objects.all().filter(user=request.user.pk) 
    return render_view(request,'complaint.html',
        {'transactions':transactions},
        )
