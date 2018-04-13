# -*- coding: utf-8 -*-

from odoo import api, fields, models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

class WorkTypeWebDirectory(models.Model):

    _name = "worktype"
    _description = "Budget Work Type"
    
    name = fields.Char(string="Name")
    interest_category_id = fields.Many2one('res.partner.category')
    description = fields.Text(string="Description")

		
class BudgetWebDirectory(models.Model):

    _name = "budget"
    _description = "Budgets"
    
    partner_id = fields.Many2one('res.partner', string="Partner Budgets")
    name = fields.Char(
        'Number', default=lambda self: self.env['ir.sequence'].next_by_code('budget.code.serial'),
        required=True, readonly=True, help="Unique Process/Serial Number")
    work_type = fields.Many2one('worktype', string="Budget work type")
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', string="State", domain="[('country_id', '=', country_id)]")
    city = fields.Char(string="City")
    description = fields.Text(string="Description")
    min_price = fields.Float(string="Minimum Price")
    max_price = fields.Float(string="Maximum Price")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done') ],
                             'State', readonly=True,
                             default=lambda *a: 'draft')
    @api.one
    def confirm_in_progress(self):
        self.state = 'confirmed'
        
    @api.one
    def confirm_to_draft(self):
        self.state = 'draft'        
        

class ProposalWebDirectory(models.Model):

    _name = "proposal"
    _description = "Budgets Proposals"

    budget_id = fields.Many2one('budget', domain="[('state','=','confirmed')]", string="Budgets Proposals")
    partner_id = fields.Many2one('res.partner', domain="[('pro','=',True)]" ,string="Partner Budgets")
    description = fields.Text(string="Description")
    exp_start_date = fields.Date(string="Expected start date")
    exp_duration = fields.Integer(string="Expected duration")
    time_type = fields.Selection([('hours', 'Hours'), ('days', 'Days'), ('months', 'Months')], 'State',default=lambda *a: 'days')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
                             'State', readonly=True,
                             default=lambda *a: 'draft')

    @api.one
    def confirm_in_progress(self):
        self.state = 'confirmed'
        

    @api.one
    def accept_prop(self):
        self.state = 'accepted'
        self.budget_id.state = 'done'
        
        for prop in self.env['proposal'].search([('budget_id','=',int(self.budget_id))]):
            if prop.id != self.id:
            	prop.state = 'rejected'
            		
    
    @api.one
    def confirm_to_draft(self):
        self.state = 'draft'

 
 
 
class ServiceWebDirectory(models.Model):

    _name = "service"
    _description = "Services"
    
    proposal_id = fields.Many2one('proposal',string="Proposal")
    client_id = fields.Integer(string="client_id", compute="_get_client") 
    pro_id = fields.Integer(string="pro_id", compute="_get_pro")
    work_type_id = fields.Integer(string="work_type_id", compute="_get_work_type")
    review_text = fields.Text(string="Message")
    review_star = fields.Float(size=8, string="Rating")
    state = fields.Selection([('scheduled', 'Scheduled'), ('in_execution', 'In Execution'), ('done', 'Done')],
                             'State', readonly=True,
                             default=lambda *a: 'scheduled')
    
    
    #@api.one
    def get_client(self):
        self.client_id = proposal_id.budget_id.partner_id
        
    def get_pro(self):
        self.pro_id = proposal_id.partner_id   
        
    def get_work_type(self):
        self.work_type = proposal_id.budget_id.work_type.id              
         	
           

    
	