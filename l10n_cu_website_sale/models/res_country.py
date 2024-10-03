from odoo import api, fields, models, _


class ResCountry(models.Model):
    _inherit = 'res.country'

    city_required = fields.Boolean(default=True)
    municipality_required = fields.Boolean(default=False)

