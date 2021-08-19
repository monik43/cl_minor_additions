odoo.define('cl_minor_additions.confirm_kanban_stage_change', function (require) {
    "use strict";

    var kanban_controller = require('web.KanbanController');

    var Dialog = require('web.Dialog');
    var _rpc = require('web.rpc');

    var BasicController = require('web.BasicController');
    var Context = require('web.Context');
    var core = require('web.core');
    var Domain = require('web.Domain');
    var view_dialogs = require('web.view_dialogs');
    var viewUtils = require('web.viewUtils');

    var _t = core._t;

    kanban_controller.include({
        /**
         * @private
         * @param {OdooEvent} event
         */
        _onAddRecordToColumn: function (event) {
            var self = this;
            var record = event.data.record;
            var column = event.target;
            if (column.relation == "helpdesk.stage" & column.modelName == "helpdesk.ticket") {
                _rpc.query({
                    model: 'helpdesk.stage',
                    method: 'js_template_handler',
                    args: [column.id]
                }).then(function (data) {
                    if (data != false) {
                        Dialog.confirm(this, _t("La etapa a la  que estás intentando cambiar tiene una plantilla de mail. Estás segurx de que quieres cambiar a esa etapa?"), {
                            confirm_callback: function () {
                                this.alive(this.model.moveRecord(record.db_id, column.db_id, this.handle))
                                    .then(function (column_db_ids) {
                                        return self._resequenceRecords(column.db_id, event.data.ids)
                                            .then(function () {
                                                _.each(column_db_ids, function (db_id) {
                                                    var data = self.model.get(db_id);
                                                    self.renderer.updateColumn(db_id, data);
                                                });
                                            });
                                    }).fail(this.reload.bind(this));
                            },
                        });
                    } else {
                        this.alive(this.model.moveRecord(record.db_id, column.db_id, this.handle))
                            .then(function (column_db_ids) {
                                return self._resequenceRecords(column.db_id, event.data.ids)
                                    .then(function () {
                                        _.each(column_db_ids, function (db_id) {
                                            var data = self.model.get(db_id);
                                            self.renderer.updateColumn(db_id, data);
                                        });
                                    });
                            }).fail(this.reload.bind(this));
                    }
                });
            } else {
                this.alive(this.model.moveRecord(record.db_id, column.db_id, this.handle))
                    .then(function (column_db_ids) {
                        return self._resequenceRecords(column.db_id, event.data.ids)
                            .then(function () {
                                _.each(column_db_ids, function (db_id) {
                                    var data = self.model.get(db_id);
                                    self.renderer.updateColumn(db_id, data);
                                });
                            });
                    }).fail(this.reload.bind(this));
            }

        },
    });
});