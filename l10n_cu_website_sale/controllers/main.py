# -*- coding: utf-8 -*-
from odoo import http, _
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

    def checkout_form_validate(self, mode, all_form_values, data):
        error, error_message = super(L10nCuWebsiteSale, self).checkout_form_validate(mode, all_form_values, data)

        # country and state validation
        try:
            country_id = data.get("country_id")
            if not country_id.isdigit():
                raise ValueError(_('Country ID must be a valid integer.'))

            country = request.env['res.country'].browse(int(country_id))

            if not country.exists():
                error["country_id"] = 'error'
                error_message.append(_('Invalid Country! Please select a valid country.'))

            state_id = data.get("state_id")

            if state_id and not state_id.isdigit():
                raise ValueError(_('State ID must be a valid integer.'))

            if state_id and int(state_id) not in country.state_ids.ids:
                error["state_id"] = 'error'
                error_message.append(_('Invalid State / Province. Please select a valid State or Province.'))

            if country and not state_id and country.state_required:
                error["state_id"] = 'error'
                error_message.append(_('Some required fields are empty.'))

        except ValueError as e:
            error['common'] = 'Unknown error'
            error_message.append(e.args[0])

        return error, error_message

    def _get_mandatory_fields_shipping(self, country_id=False):
        req = super(L10nCuWebsiteSale, self)._get_mandatory_fields_shipping(country_id=country_id)
        if country_id:
            country = request.env['res.country'].browse(country_id)
            if country.municipality_required:
                req += ['res_municipality_id']
            if not country.city_required:
                req.remove('city')

        return req

    @http.route(['/shop/l10n_cu/state_infos/<model("res.country.state"):state>'], type="json", auth="public", methods=["POST"], website=True, )
    def l10n_cu_state_infos(self, state, mode, **kw):

        municipalities = state.get_website_sale_municipalities(mode=mode)
        municipality_required = state.country_id.municipality_required

        return {
            'municipalities': [(c.id, c.name, c.code) for c in municipalities],
            'municipality_required': municipality_required
        }
