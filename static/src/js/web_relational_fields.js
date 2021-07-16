odoo.define('cl_minor_additions.confirm_stage_change', function (require) {
    "use strict";

    //require the module to modify:
    var relational_fields = require('web.relational_fields');

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _rpc = require('web.rpc');
    var _t = core._t;

    //override the method:
    relational_fields.FieldStatus.include({
            /**
             * Called when on status stage is clicked -> sets the field value.
             * @private
             * @param {MouseEvent} e
             */
            _onClickStage: function (e) {
                var self = this;
                console.log(self);
                console.log(self.record);
                console.log(self.record.data);
                console.log(self.record.data.stage_id);
                console.log("id stage: ", self.record.data.stage_id.data.id);
                console.log("---");
                console.log(self._rpc({
                    model: 'helpdesk.stage',
                    method: 'get_template_id',
                    args:[self.record.data.stage_id.data.id]
                }));
                

            Dialog.confirm(this, _t("You sure mate?"), {
                confirm_callback: function () {
                    self._setValue($(e.currentTarget).data("value"));
                },
            });

        },
    });
});