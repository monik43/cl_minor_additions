odoo.define('cl_minor_additions.confirm_stage_change', function (require) {
    "use strict";
 
    //require the module to modify:
    var helpdesk_dashboard = require('helpdesk.dashboard');
 
    var core = require('web.core');
    var KanbanController = require('web.KanbanController');
    var KanbanModel = require('web.KanbanModel');
    var KanbanRenderer = require('web.KanbanRenderer');
    var KanbanView = require('web.KanbanView');
    var session = require('web.session');
    var view_registry = require('web.view_registry');
    
    var QWeb = core.qweb;
    
    var _t = core._t;
    var _lt = core._lt;

    //override the method:
    helpdesk_dashboard.HelpdeskDashboardRenderer.include({
        events: _.extend({}, KanbanRenderer.prototype.events, {
            'click .o_dashboard_action': '_onDashboardActionClicked',
            'click .o_target_to_set': '_onDashboardTargetClicked',
        }),
        /**
         * @private
         * @param {MouseEvent}
         */
         _onDashboardTargetClicked: function (e) {
            var self = this;
            var $target = $(e.currentTarget);
            var target_name = $target.attr('name');
            var target_value = $target.attr('value');
            console.log(print($target, " ", target_name, " ", target_value))
            var $input = $('<input/>', {type: "text", name: target_name});
            if (target_value) {
                $input.attr('value', target_value);
            }
            $input.on('keyup input', function (e) {
                if (e.which === $.ui.keyCode.ENTER) {
                    self._notifyTargetChange(target_name, $input.val());
                }
            });
            $input.on('blur', function () {
                self._notifyTargetChange(target_name, $input.val());
            });
            $input.replaceAll($target)
                  .focus()
                  .select();
        },
    });
});