/** @odoo-module **/
import {WebsiteSale} from "@website_sale/js/website_sale";
import {debounce} from "@web/core/utils/timing";

WebsiteSale.include({
    /**
     * @constructor
     */
    init: function () {
        this._super.apply(this, arguments);
        this._onChangeState = debounce(this._onChangeState.bind(this), 500);
    },

    /**
     * Extended to hide municipalities when the region changes
     * and avoid the slight delay. Afterward, _onChangeState is called again
     * to synchronize municipalities as soon as the states/provinces are
     * obtained.
     *
     * @private
     */
    _changeCountry: function () {
        let data = {
            municipalities: []
        }
        this._expandDataStates(data);
        this._super.apply(this, arguments);
        this._onChangeState(this);
    },

    _onChangeState: function (ev) {
        return this._super.apply(this, arguments).then(() => {
            const country = $("select[name='country_id']");

            const selectedOption = country.find('option:selected');
            const countryCode = selectedOption.attr('code');
            const mode = country.attr('mode');

            const state = $("select[name='state_id']");

            if (state.val() === '' || countryCode !== 'CU') {
                let data = {
                    municipalities: []
                }
                return this._expandDataStates(data);
            }

            return this.rpc("/shop/l10n_cu/state_infos/" + parseInt(state.val()), {
                mode: mode
            }).then((data) => {
                return this._expandDataStates(data);
            })

        });
    },

    _expandDataStates(data) {
        // populate states and display
        let selectMunicipalities = $("select[name='res_municipality_id']");
        // dont reload state at first loading (done in qweb)
        if (selectMunicipalities.data('init') === 0 || selectMunicipalities.find('option').length === 1) {
            if (data.municipalities.length || data.municipality_required) {
                selectMunicipalities.html('');
                data.municipalities.forEach((x) => {
                    let opt = $('<option>').text(x[1])
                        .attr('value', x[0])
                        .attr('data-code', x[2]);
                    selectMunicipalities.append(opt);
                });
                selectMunicipalities.parent('div').show();
            } else {
                selectMunicipalities.val('').parent('div').hide();
            }
            selectMunicipalities.data('init', 0);
        } else {
            selectMunicipalities.data('init', 0);
        }
    }
});
