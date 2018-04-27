# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import datetime
from dateutil.relativedelta import relativedelta
from itertools import islice
import json
import xml.etree.ElementTree as ET
import logging
import re
import urllib2
import base64
import werkzeug.utils
import werkzeug.wrappers
import urlparse

import odoo
from odoo import http
from odoo import fields
from odoo.http import request
from odoo.osv.orm import browse_record


logger = logging.getLogger(__name__)


class DirectoryAdminController(http.Controller):

    @http.route('/admin', type='http', auth="user", website=True)
    def index(self, **kwargs):
        page = 'admin'
        

        
        
        return http.request.render('website_directory.admin')

#####################################################################################

    @http.route('/admin/account', type='http', auth="user", website=True)
    def account_user(self, **kwargs):
        page = 'account'
        partner = request.env.user.partner_id
        countries = request.env['res.country'].search([])
        states = request.env['res.country.state'].search([])
        	
        
        
        return http.request.render('website_directory.account', {'partner' : partner, 'countries' : countries, 'states' : states})  

#####################################################################################

    @http.route('/admin/account/edit', type='http', auth="user", website=True)
    def account_user_edit(self, **kwargs):
        page = 'account'
        

        return http.request.render('website_directory.account_user_edit')        
              
########################################### acabar #########################################
        
    @http.route('/admin/account/process', type='http', auth="user", website=True)
    def account_directory_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value

        
        
        existing_record = request.env['res.partner'].search([('user_id','=', request.env.user.id)])
        

        if existing_record.user_id.id == request.env.user.id:
            updated_listing = existing_record.sudo().write({
            'name': values['name'], 
            'email': values['email'],
            'category_id': values['category_id'],
            'max_price': values['max_price'],
            'county_id': values['county_id'],
            'city': values['city'],
            'state_id': values['state_id'],
            'description': values['description'],
            'state': values['budget_state']
            
            })

            #Redirect them to thier account page
            return werkzeug.utils.redirect("/admin/account")
        else:
            return "Permission Denied"     



        return werkzeug.utils.redirect("/admin/mylistings")






###################################################################################### listings

    @http.route('/admin/listings', type='http', auth="user", website=True)
    def listings_directory(self, **kwargs):
        
        budgets = request.env['budget_request'].sudo().search([])
        proposals = request.env['proposal'].sudo().search([('user_id.id','=', request.env.user.id)])
        user = request.env.user
    	  
        return http.request.render('website_directory.listings', {'budgets': budgets, 'proposals': proposals, 'user' : user} ) 
        
        
###################################################################################### MY listings

    @http.route('/admin/mylistings', type='http', auth="user", website=True)
    def mylistings_directory(self, **kwargs):
        
        
        
        budgets = request.env['budget_request'].sudo().search([('user_id.id','=', request.env.user.id)])
        proposals = request.env['proposal'].sudo().search([('client_id.id','=', request.env.user.partner_id.id)])
        print budgets
        print proposals

        return http.request.render('website_directory.mylistings', {'budgets': budgets, 'proposals': proposals} )    	
   	
###################################################################################### listings Add

    @http.route('/admin/listings/add', type='http', auth="user", website=True)
    def listings_directory_add(self, **kwargs):

        work_types = request.env['worktype'].sudo().search([])
        categs = request.env['res.partner.category'].sudo().search([])
        
        counties = request.env['res.county'].sudo().search([])
        county_locals = request.env['res.county.local'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
    	  
        return http.request.render('website_directory.listings_add', {'work_types': work_types, 'categs': categs, 'counties': counties, 'county_locals': county_locals, 'states' : states} )        	
   	
###################################################################################### listings Add

    @http.route('/admin/listings/add/process', type='http', auth="user", website=True)
    def listings_directory_add_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value

        insert_values = {'user_id': request.env.user.id, 'partner_id': request.env.user.partner_id.id} 
        
        if 'accepting_date' in values: insert_values['accepting_date'] = "2018-05-31"#values['start_date']
        #if 'xxxx' in values: insert_values['client_id'] = values['xxxx']
        if 'work_type' in values: insert_values['work_type'] = values['work_type']
        if 'category_id' in values: insert_values['category_id'] = values['category_id']
        if 'max_price' in values: insert_values['max_price'] = values['max_price']
        if 'county_id' in values: insert_values['county_id'] = values['county_id']
        if 'city' in values: insert_values['city'] = values['city']
        if 'state_id' in values: insert_values['state_id'] = values['state_id']
        if 'xxxx' in values: insert_values['state'] = values['xxxx']
        if 'description' in values: insert_values['description'] = values['description']
        
        new_budget_request = request.env['budget_request'].sudo().create(insert_values)
    	  
        return werkzeug.utils.redirect("/admin/mylistings")
















        
###################################################################################### edita um pedido orçamento

    @http.route('/admin/listings/edit/<model("budget_request"):listing>', type='http', auth="user", website=True)
    def listings_directory_edit(self, listing, **kwargs):
        if listing.user_id.id == request.env.user.id:
        	
            work_types = request.env['worktype'].sudo().search([])
            categs = request.env['res.partner.category'].sudo().search([])
        
            counties = request.env['res.county'].sudo().search([])
            county_locals = request.env['res.county.local'].sudo().search([])
            states = request.env['res.country.state'].sudo().search([])
            
            

            user_id = listing.user_id
            state = listing.state
            
            
            
            
            print categs
            print listing

            return http.request.render('website_directory.listings_edit', {'listing': listing, 'work_types': work_types, 'categs': categs, 'counties': counties, 'county_locals': county_locals, 'states' : states} )
        else:
            return "ACCESS DENIED"
            
###################################################################################### processa a alteração de pedido orçamento existente
    @http.route('/admin/listings/edit/process', type='http', auth="user", website=True)
    def listings_directory_edit_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value

        print values.keys()
        
        existing_record = request.env['budget_request'].search([('name','=', values['budget_name'])])
        

        if existing_record.user_id.id == request.env.user.id:
            updated_listing = existing_record.sudo().write({
            'accepting_date': values['accepting_date'], 
            'work_type': values['work_type'],
            'category_id': values['category_id'],
            'max_price': values['max_price'],
            'county_id': values['county_id'],
            'city': values['city'],
            'state_id': values['state_id'],
            'description': values['description'],
            'state': values['budget_state']
            
            })

            #Redirect them to thier account page
            return werkzeug.utils.redirect("/admin/mylistings")
        else:
            return "Permission Denied"     























         	
###################################################################################### lista propostas

        
    @http.route('/admin/proposals', type='http', auth="user", website=True)
    def proposals_directory(self, **kwargs):
        
        proposals = request.env['proposal'].sudo().search([('user_id.id','=', request.env.user.id)])
            	
        return http.request.render('website_directory.proposals', {'proposals': proposals})

###################################################################################### adiciona proposta 

    @http.route('/admin/proposals/add', type='http', auth="user", website=True)
    def proposals_directory_add(self, **kwargs):
        print 'dasdasdasdasdasdasdasdasdasd'
        url = urlparse.urlparse(http.request.httprequest.full_path)
        query = dict(urlparse.parse_qs(url.query))
        if query:
            budget_request_id = query['budget_request_id'][0]
            budget_request_name = query['budget_request_name'][0]
            return http.request.render('website_directory.proposals_add', {'budget_request_id' : budget_request_id, 'budget_request_name' : budget_request_name})
        
        
        else:
            budgets = request.env['budget_request'].sudo().search([('user_id','!=', request.env.user.id)])
            return http.request.render('website_directory.proposals_add', {'budgets' : budgets})
        
        



        
        


        
###################################################################################### processa nova proposta

    @http.route('/admin/proposals/add/process', type='http', auth="user", website=True)
    def proposals_directory_add_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value

        insert_values = {'user_id': request.env.user.id, 'partner_id': request.env.user.partner_id.id} 
        
        if 'budget' in values: insert_values['budget_request_id'] = values['budget']
        #if 'xxxx' in values: insert_values['client_id'] = values['xxxx']
        if 'description' in values: insert_values['description'] = values['description']
        if 'start_date' in values: insert_values['exp_start_date'] = "2018-05-31"#values['start_date']
        if 'exp_duration' in values: insert_values['exp_duration'] = values['exp_duration']
        if 'time_type' in values: insert_values['time_type'] = values['time_type']
        if 'xxxx' in values: insert_values['state'] = values['xxxx']
        if 'price' in values: insert_values['price'] = values['price']
        
        #Fix exp_start_date than uncoment 
        
        #if values['time_type'] == 'hours':
        #    exp_end_date = fields.Datetime.from_string(self.exp_start_date) +  relativedelta(hours=self.exp_duration)
        #elif values['time_type'] == 'days':
        #    exp_end_date = fields.Datetime.from_string(self.exp_start_date) +  relativedelta(days=self.exp_duration)   
        #elif values['time_type'] == 'months':
        #    exp_end_date = fields.Datetime.from_string(self.exp_start_date) +  relativedelta(months=self.exp_duration)
        #insert_values['exp_end_date'] = exp_end_date
        
        
        new_proposal = request.env['proposal'].sudo().create(insert_values)

        return werkzeug.utils.redirect("/admin/proposals")
        
###################################################################################### edita uma proposta

    @http.route('/admin/proposals/edit/<model("proposal"):proposal>', type='http', auth="user", website=True)
    def proposals_directory_edit(self, proposal, **kwargs):
        if proposal.user_id.id == request.env.user.id:
        	
            #partners = request.env['res.partner'].sudo().search([('pro','=', True), ('user_id','=', request.env.user.id)])

            work_types = request.env['worktype'].sudo().search([])

            budgets = request.env['budget_request'].sudo().search([])
            
            return http.request.render('website_directory.proposals_edit', {'proposal': proposal, 'work_types': work_types, 'budgets' : budgets})
        else:
            return "ACCESS DENIED"
            
###################################################################################### processa a alteração de uma proposta existente
    @http.route('/admin/proposals/edit/process', type='http', auth="user", website=True)
    def proposals_directory_edit_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value


        existing_record = request.env['proposal'].browse( int(values['user_id.id'] ) )
        
        if existing_record.user_id.id == request.env.user.id:
            updated_listing = existing_record.sudo().write({
            'name': values['name'], 
            'contact_id': values['partner'],
            'network_country': values['country']
            })

            #Redirect them to thier account page
            return werkzeug.utils.redirect("/admin/proposals")
        else:
            return "Permission Denied"     
            
       
       



































     
            
#################            
#            
#     Editar a partir daqui       
#
#
###################################################################################### lista propostas

        
    @http.route('/admin/services', type='http', auth="user", website=True)
    def services_directory(self, **kwargs):
        
        services = request.env['service'].sudo().search([('user_id.id','=', request.env.user.id)])
            	
        return http.request.render('website_directory.services', {'services': services})

###################################################################################### adiciona proposta 

    @http.route('/admin/services/add', type='http', auth="user", website=True)
    def services_directory_add(self, **kwargs):
    	   
        proposals = request.env['proposal'].sudo().search([])
        budget_requests = request.env['budget_request'].sudo().search([])# ('state','!=', 'draft')
        work_types = request.env['worktype'].sudo().search([])
        clients = request.env['res.partner'].sudo().search([('pro','=', False)])
        pros = request.env['res.partner'].sudo().search([('pro','=', True)])
        
        return http.request.render('website_directory.services_add', {'work_types': work_types, 'proposals': proposals, 'budget_requests': budget_requests, 'clients': clients, 'pros': pros })


        
        
###################################################################################### processa nova proposta

    @http.route('/admin/services/add/process', type='http', auth="user", website=True)
    def services_directory_add_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value

        insert_values = {'user_id': request.env.user.id} 

        if 'proposal_id' in values: insert_values['proposal_id'] = values['proposal_id']
        if 'budget_request_id' in values: insert_values['budget_request_id'] = values['budget_request_id']
        if 'pro_id' in values: insert_values['pro_id'] = values['pro_id']
        if 'client_id' in values: insert_values['client_id'] = values['client_id']
        if 'work_type_id' in values: insert_values['work_type_id'] = values['work_type_id']
        if 'price' in values: insert_values['price'] = values['price']
        if 'exp_end_date' in values: insert_values['exp_end_date'] = '2018-09-12' #values['budget'] 
        if 'description' in values: insert_values['description'] = values['description']
        
        new_service = request.env['service'].sudo().create(insert_values)

        return werkzeug.utils.redirect("/admin/services")
        
###################################################################################### edita uma proposta

    @http.route('/admin/services/edit/<model("service"):service>', type='http', auth="user", website=True)
    def services_directory_edit(self, service, **kwargs):
        if service.user_id.id == request.env.user.id:



        	
            work_types = request.env['worktype'].sudo().search([])
            proposals = request.env['proposal'].sudo().search([])
            budget_requests = request.env['budget_request'].sudo().search([])# ('state','!=', 'draft')
            clients = request.env['res.partner'].sudo().search([('pro','=', False)])
            pros = request.env['res.partner'].sudo().search([('pro','=', True)])


            return http.request.render('website_directory.services_edit', {'service': service, 'work_types': work_types, 'proposals': proposals, 'budget_requests': budget_requests, 'clients': clients, 'pros' : pros} )
        else:
            return "ACCESS DENIED"


            
###################################################################################### processa a alteração de uma proposta existente
    @http.route('/admin/services/edit/process', type='http', auth="user", website=True)
    def services_directory_edit_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value
        #quando form de ediçao estiver este browse nao pode ser assim usar name em vez de user id

        existing_record = request.env['service'].browse( int(values['user_id.id'] ) )
        
        if existing_record.user_id.id == request.env.user.id:
            updated_listing = existing_record.sudo().write({
            'name': values['name'], 
            'contact_id': values['partner'],
            'network_country': values['country']
            })

            #Redirect them to thier account page
            return werkzeug.utils.redirect("/admin/services")
        else:
            return "Permission Denied" 