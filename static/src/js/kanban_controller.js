odoo.define(
  "cl_minor_additions.confirm_kanban_stage_change",
  function (require) {
    "use strict";

    var kanban_controller = require("web.KanbanController");

    var core = require("web.core");
    var Dialog = require("web.Dialog");
    var _rpc = require("web.rpc");

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

        if (
          (column.relation == "helpdesk.stage") &
          (column.modelName == "helpdesk.ticket")
        ) {
          _rpc
            .query({
              model: "helpdesk.stage",
              method: "js_template_handler",
              args: [column.id],
            })
            .then(function (data) {
              if (data[0] != false) {
                  if (data[1] == 'Asignado'){
                    _rpc
                  .query({
                    model: "helpdesk.ticket",
                    method: "js_stage_handler",
                    args: [column.id],
                  })
                  .then(function (data2) {
                    console.log("test")
                    console.log(record)
                    /*
                    if (data2 == false) {
                      Dialog.confirm(
                        this,
                        _t(
                          "No se ha registrado el número de serie en la base de datos. Antes de cambiar el estado, registre el nº de serie."
                        ),
                        {
                          confirm_callback: function () {
                            console.log();
                          },
                        }
                      );
                    }*/
                  });
                  } else {
                    Dialog.confirm(
                        this,
                        _t(
                          "La etapa a la  que estás intentando cambiar tiene una plantilla de mail. Estás segurx de que quieres cambiar a esa etapa?"
                        ),
                        {
                          confirm_callback: function () {
                            self
                              .alive(
                                self.model.moveRecord(
                                  record.db_id,
                                  column.db_id,
                                  self.handle
                                )
                              )
                              .then(function (column_db_ids) {
                                return self
                                  ._resequenceRecords(column.db_id, event.data.ids)
                                  .then(function () {
                                    _.each(column_db_ids, function (db_id) {
                                      var data = self.model.get(db_id);
                                      self.renderer.updateColumn(db_id, data);
                                    });
                                  });
                              })
                              .fail(self.reload.bind(self));
                          },
                        }
                      );
                  }
                
              } else {
                self
                  .alive(
                    self.model.moveRecord(
                      record.db_id,
                      column.db_id,
                      self.handle
                    )
                  )
                  .then(function (column_db_ids) {
                    return self
                      ._resequenceRecords(column.db_id, event.data.ids)
                      .then(function () {
                        _.each(column_db_ids, function (db_id) {
                          var data = self.model.get(db_id);
                          self.renderer.updateColumn(db_id, data);
                        });
                      });
                  })
                  .fail(self.reload.bind(self));
              }
            });
        } else {
          self
            .alive(
              self.model.moveRecord(record.db_id, column.db_id, self.handle)
            )
            .then(function (column_db_ids) {
              return self
                ._resequenceRecords(column.db_id, event.data.ids)
                .then(function () {
                  _.each(column_db_ids, function (db_id) {
                    var data = self.model.get(db_id);
                    self.renderer.updateColumn(db_id, data);
                  });
                });
            })
            .fail(self.reload.bind(self));
        }
      },
    });
  }
);
