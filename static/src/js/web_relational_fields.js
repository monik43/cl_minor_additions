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
                var fdata;
                _rpc.query({
                    model: 'helpdesk.stage',
                    method: 'js_template_handler',
                    args:[$(e.currentTarget).data("value")]
                }).then(function (data){
                    fdata = data;
                    console.log("a", data);
                    console.log("b", fdata);
                });

                setTimeout(function(){console.log("c", fdata);},1000);
        },
    });
});