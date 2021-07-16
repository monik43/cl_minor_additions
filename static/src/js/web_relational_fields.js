odoo.define('cl_minor_additions.confirm_stage_change', function (require) {
    "use strict";

    var relational_fields = require('web.relational_fields');

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _rpc = require('web.rpc');
    var _t = core._t;

    relational_fields.FieldStatus.include({
        /**
         * Called when on status stage is clicked -> sets the field value.
         * @private
         * @param {MouseEvent} e
         */
        _onClickStage: function (e) {
            var self = this;
            var target = $(e.currentTarget).data("value");
            _rpc.query({
                model: 'helpdesk.stage',
                method: 'js_template_handler',
                args: [target]
            }).then(function (data) {
                if (data != false) {
                    Dialog.confirm(this, _t("La etapa a la  que estás intentando cambiar tiene una plantilla de mail. Estás segurx de que quieres cambiar a esa etapa?"), {
                        confirm_callback: function () {
                            self._setValue(target);
                        },
                    });
                } else {
                    self._setValue(target);
                }
            });
        },
    });
});