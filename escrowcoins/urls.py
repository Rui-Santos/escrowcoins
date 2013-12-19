from django.conf.urls import patterns, include, url
from escrowcoins.views import landing_page, list_transactions, list_transaction, add_complaint, transaction_agree_terms
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
#custom forms
from accounts import forms

urlpatterns = patterns('',
                      url(r'^$',landing_page),
                      url(r'^transactions$',list_transactions),
                      url(r'^transaction/(\w+)/$', list_transaction, name='transaction'),
                      url(r'^transaction/(\w+)/agreeterms', transaction_agree_terms, name='agreeterms'),
                      url(r'^complaint$',add_complaint),
                      #(r'^accounts/signup/$','userena.views.signup',{'signup_form':forms.SignupFormExtra}),
                      (r'^accounts/', include('userena.urls')),
                       # Examples:
                       # url(r'^$', 'escrowcoins.views.home', name='home'),
                       # url(r'^escrowcoins/',
                       # include('escrowcoins.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/',
                       # include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_ROOT, 'show_indexes':True}
                        ),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
                        {'document_root': settings.MEDIA_ROOT, 
                        'show_indexes':True}
                        ),
                       )