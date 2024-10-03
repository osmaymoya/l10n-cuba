# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from odoo.addons.website_sale.controllers.main import WebsiteSale


class L10nCuWebsiteSale(WebsiteSale):

    def _get_country_related_render_values(self, kw, render_values):
        """ Provide the fields related to the country to render the website sale form """

        res = super(L10nCuWebsiteSale, self)._get_country_related_render_values(kw, render_values)
        mode = render_values['mode']
        Partner = request.env['res.partner']
        partner_id = render_values['partner_id']

        if mode and partner_id != -1:
            Partner = Partner.browse(int(render_values['partner_id']))

        res['state_id'] = Partner.state_id
        res['municipalities'] = Partner.state_id.get_website_sale_municipalities(mode=mode[1])

        return res

    def _get_mandatory_fields_billing(self, country_id=False):
        req = super(L10nCuWebsiteSale, self)._get_mandatory_fields_billing(country_id=country_id)
        if country_id:
            country = request.env['res.country'].browse(country_id)
            if country.municipality_required:
                req += ['res_municipality_id']
            if not country.city_required:
                req.remove('city')

        return req

    def _get_mandatory_fields_shipping(self, country_id=False):
        req = super(L10nCuWebsiteSale, self)._get_mandatory_fields_shipping(country_id=country_id)
        if country_id:
            country = request.env['res.country'].browse(country_id)
            if country.municipality_required:
                req += ['res_municipality_id']
            if not country.city_required:
                req.remove('city')

        return req

    @http.route(['/shop/l10n_cu/state_infos/<model("res.country.state"):state>'], type="json", auth="public", methods=["POST"], website=True,)
    def l10n_cu_state_infos(self, state, mode, **kw):

        municipalities = state.get_website_sale_municipalities(mode=mode)

        return {'municipalities': [(c.id, c.name, c.code) for c in municipalities]}
