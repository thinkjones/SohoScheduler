# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin


handler500 = 'about.views.errorpage'

urlpatterns = patterns('',

        ## Patterns in order of use
        (r'^newentitywizard/$', 'entity.wizards.loadNewEntityWizard'),
        (r'^newentitywizard/jsonrequests/$', 'entity.wizards.jsonrequests'),
        (r'^newentitywizard/gotonewapplication/$', 'entity.wizards.gotonewapplication'),
	(r'^application/(?P<entity_id>\d+)/$', 'dashboard.views.index'),
	(r'^application/switch/(?P<entity_id>\d+)/$', 'dashboard.views.change_entity'),

        (r'^application/(?P<entity_id>\d+)/appointment/$', 'appointment.views.index'),
        (r'^application/(?P<entity_id>\d+)/appointment/jsonrequests/$', 'appointment.views.jsonrequests'),

	(r'^application/(?P<entity_id>\d+)/crm/$', 'crm.views.index'),
        (r'^application/(?P<entity_id>\d+)/crm/new/$', 'crm.views.new'),

        (r'^application/docpost/$', 'entity.views.docpost'),
        (r'^application/formpost/$', 'entity.views.formpost'),
        (r'^application/docdesignpost/$', 'entity.views.docdesignpost'),

	(r'^application/(?P<entity_id>\d+)/crm/jsonrequests/$', 'crm.views.jsonrequests'),

	(r'^application/(?P<entity_id>\d+)/crm/view/(?P<crm_id>\d+)/$', 'crm.views.viewinfo'),
	(r'^application/(?P<entity_id>\d+)/crm/edit/(?P<crm_id>\d+)/$', 'crm.views.edit'),

	(r'^application/(?P<entity_id>\d+)/settings/$', 'designer.views.index'),

        ### Admin URLS
	(r'^sohoadmin/cron/(?P<cronjob>[a-zA-Z0-9_.-]+)/$', 'sohoadmin.cron.views.cronjobs'),
	(r'^sohoadmin/$', 'sohoadmin.views.index'),

        (r'^about/feedback/(?P<entity_id>\d+)/$', 'about.views.feedback'),
        (r'^about/contactus/$', 'about.views.jsoncontactus'),

        (r'^application/(?P<entity_id>\d+)/crm/wizard/synchwithgoogle/$', 'crm.wizards.loadSyncWithGoogleWizard'),
        (r'^application/(?P<entity_id>\d+)/crm/wizard/synchwithgoogle/jsonrequests/$', 'crm.wizards.jsonrequests'),

        (r'^application/(?P<entity_id>\d+)/settings/$', 'designer.views.index_permissions'),
	(r'^application/(?P<entity_id>\d+)/settings/invitedusers/$', 'designer.views.index_permissions_invitedusers'),
	(r'^application/(?P<entity_id>\d+)/settings/currentusers/$', 'designer.views.index_permissions_currentusers'),
        (r'^application/jsonrequests/$', 'entity.views.jsonrequests'),


        (r'^application/(?P<entity_id>\d+)/$', 'entity.views.index2'),

        (r'^application/(?P<entity_id>\d+)/designer/wizards/publishtemplate/$', 'designer.wizards.publishTemplateWizard'),
	(r'^application/(?P<entity_id>\d+)/designer/wizards/jsonrequests/$', 'designer.wizards.jsonrequests'),


        (r'^application/(?P<entity_id>\d+)/designer/updatedsettings/$', 'designer.views.updatedsettings'),
        (r'^application/(?P<entity_id>\d+)/designer/byformtype/(?P<form_type_id>\d+)/$', 'designer.views.designByType'),

	(r'^application/(?P<entity_id>\d+)/appointment/new/$', 'appointment.views.new'),
	(r'^application/(?P<entity_id>\d+)/appointment/edit/(?P<appointment_id>\d+)/$', 'appointment.views.edit'),
	(r'^application/(?P<entity_id>\d+)/appointment/view/(?P<appointment_id>\d+)/$', 'appointment.views.view'),
	(r'^application/(?P<entity_id>\d+)/appointment/delete/(?P<appointment_id>\d+)/$', 'appointment.views.delete'),
        (r'^application/(?P<entity_id>\d+)/appointment/design/$', 'designer.views.designAppointment'),
	(r'^application/(?P<entity_id>\d+)/crm/design/$', 'designer.views.designCRM'),

        (r'^application/(?P<entity_id>\d+)/sohoformbuilder/jsonrequests/$', 'sohoformbuilder.views.jsonrequests'),
        (r'^application/(?P<entity_id>\d+)/crm/jsonselect/$', 'crm.views.jsonselect'),

        (r'^sohoadmin/downloadusers/$', 'sohoadmin.views.downloadusers'),
        (r'^sohoadmin/changetemplaterating/(?P<entity_id>\d+)/(?P<newratingval>\d+)/$', 'sohoadmin.views.changetemplaterating'),








) 
