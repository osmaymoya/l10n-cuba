import inspect

from odoo import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _ignore_methods_name_list(self):
        """
        Returns a list of method names where, when calling _formatting_address_fields,
        the `municipality_name` will not be added to avoid errors.
        This method is useful for understanding which specific functions are excluded from the formatting process,
        allowing better control over data handling in situations where the inclusion of `municipality_name`
        would cause problems.

        :return: List of method names to be ignored
        :rtype: list
        """

        return ['_prepare_display_address']

    def _formatting_address_fields(self):
        """Returns the list of address fields usable to format addresses."""
        fields_values = super(ResPartner, self)._formatting_address_fields()
        caller = inspect.stack()[1].function

        if caller not in self._ignore_methods_name_list():
            fields_values += ['municipality_name']

        return fields_values

    def _display_address_depends(self):
        """
        :return: field dependencies of method _display_address()
        """
        # remove 'municipality_name' to prevent api.depends error
        fields_values = super(ResPartner, self)._display_address_depends()
        fields_values.remove('municipality_name')
        return fields_values

    def _prepare_display_address(self, without_company=False):
        """
        get the information that will be injected into the display format
        get the address format
        :param without_company:
        :return:
        """

        address_format, args = super(ResPartner, self)._prepare_display_address(without_company=without_company)
        args['municipality_name'] = self.res_municipality_id.name or ''
        return address_format, args
