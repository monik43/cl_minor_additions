odoo.define('cl_minor_additions.confirm_stage_change', function (require) {
    "use strict";
 
    //require the module to modify:
    var relational_fields = require('web.relational_fields');
 
    var core = require('web.core');
    var Dialog = require('web.Dialog');
 
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
            console.log(self.data)
            Dialog.confirm(this, _t("You sure mate?"), {
                confirm_callback: function () {
                    self._setValue($(e.currentTarget).data("value"));
                },
            });
 
        },
    });
});