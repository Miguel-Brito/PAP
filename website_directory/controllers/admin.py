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

import odoo
from odoo import http
from odoo import fields
from odoo.http import request
from odoo.osv.orm import browse_record


logger = logging.getLogger(__name__)


class DirectoryAdminController(http.Controller):

    @http.route('/admin', type='http', auth="user", website=True)
    def index(self, **kw):
        page = 'admin'
        

        
        
        return http.request.render('website_directory.admin')

###################################################################################### listings

    @http.route('/admin/listings', type='http', auth="user", website=True)
    def listings_directory(self, **kwargs):
        
        budgets = request.env['budget'].sudo().search([])
        proposals = request.env['proposal'].sudo().search([('user_id.id','=', request.env.user.id)])
        print '#####################'
        print proposals['state']
        print budgets
        
        print '#####################'
    	  
        return http.request.render('website_directory.listings', {'budgets': budgets, 'proposals': proposals} )    	

###################################################################################### lista propostas

    @http.route('/admin/proposals', type='http', auth="user", website=True)
    def proposals_directory(self, **kw):
        
        proposals = request.env['proposal'].sudo().search([('user_id.id','=', request.env.user.id)])
        
        return http.request.render('website_directory.proposals', {'proposals': proposals})

###################################################################################### adiciona proposta 

    @http.route('/admin/proposals/add', type='http', auth="user", website=True)
    def proposals_directory_add(self, **kw):
        

        return http.request.render('website_directory.proposals_add')
        
###################################################################################### processa nova proposta

    @http.route('/admin/proposals/add/process', type='http', auth="user", website=True)
    def proposals_directory_add_process(self, **kw):
        

        return werkzeug.utils.redirect("/admin/proposals")
        
###################################################################################### edita uma proposta

    @http.route('/admin/proposals/edit/<model("proposal"):proposal>', type='http', auth="user", website=True)
    def proposals_directory_edit(self, proposal, **kwargs):
        if proposal.user_id.id == request.env.user.id:
            partners = request.env['res.partner'].sudo().search([('pro','=', True), ('user_id','=', request.env.user.id)])
            countries = request.env['res.country'].search([])
            return http.request.render('website_directory.proposals_edit', {'proposal': proposal, 'partners': partners, 'countries': countries} )
        else:
            return "ACCESS DENIED"
            
###################################################################################### processa a alteração de uma proposta existente
    @http.route('/admin/proposals/edit/process', type='http', auth="user", website=True)
    def proposals_directory_edit_process(self, **kwargs):

        values = {}
	for field_name, field_value in kwargs.items():
	    values[field_name] = field_value


        existing_record = request.env['proposal'].browse( int(values['user_id'] ) )
        
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
