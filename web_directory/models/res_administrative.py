# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from psycopg2 import IntegrityError
from odoo.tools.translate import _

@api.model
def location_name_search(self, name='', args=None, operator='ilike', limit=100):
    if args is None:
        args = []

    records = self.browse()
    if len(name) == 2:
        records = self.search([('code', 'ilike', name)] + args, limit=limit)

    search_domain = [('name', operator, name)]
    if records:
        search_domain.append(('id', 'not in', records.ids))
    records += self.search(search_domain + args, limit=limit)

    # the field 'display_name' calls name_get() to get its value
    return [(record.id, record.display_name) for record in records]


class County(models.Model):
    _name = 'res.county'
    _description = 'County'
    _order = 'name'

    name = fields.Char(string='County Name', required=True, translate=True, help='The full name of the county.')
    code = fields.Char(string='County Code', size=4,
                help='The ISO county code in two chars. \nYou can use this field for quick search.')
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)

    local_ids = fields.One2many('res.county.local', 'county_id', string='Locales')

    _sql_constraints = [
        ('code_uniq', 'unique (code)',
            'The code of the county must be unique !')
    ]

    name_search = location_name_search


class CountyLocales(models.Model):
    _description = "County Local"
    _name = 'res.county.local'
    _order = 'name'

    name = fields.Char(string='Local Name', required=True,
               help='Administrative divisions of a county. E.g. Fed. Local')
    code = fields.Char(string='State Code', size=6, help='The Local code.', required=True)
    country_id = fields.Many2one('res.country', string='Country', required=True)
    state_id = fields.Many2one('res.country.state', string='State', required=True)
    county_id = fields.Many2one('res.county', string='County', required=True)
    
    name_search = location_name_search

    _sql_constraints = [
        ('code_uniq', 'unique (code)',
            'The code of the local must be unique !')
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if self.env.context.get('get_parent_county', False):
            lst = []
            lst.append(self.env.context.get('county_id'))
            counties = self.env['res.county'].browse(lst)
            #while counties.parent_id:
            #    lst.append(counties.parent_id.id)
            #    counties = counties.parent_id
            locales = self.env['res.county.local'].search([('county_id', 'in', lst)])
            return locales.name_get()
        return super(CountyLocales, self).name_search(
            name, args, operator=operator, limit=limit)
