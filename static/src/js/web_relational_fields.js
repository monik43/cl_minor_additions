odoo.define("cl_minor_additions.confirm_stage_change", function (require) {
  "use strict";

  var relational_fields = require("web.relational_fields");

  var core = require("web.core");
  var Dialog = require("web.Dialog");
  var _rpc = require("web.rpc");
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
      if (self.model == "helpdesk.ticket") {
        _rpc
          .query({
            model: "helpdesk.stage",
            method: "js_template_handler",
            args: [target],
          })
          .then(function (data) {
            console.log(data)
            if (data[0] != false) {
              if (data[1] == "Asignado") {
                _rpc
                  .query({
                    model: "helpdesk.ticket",
                    method: "js_stage_handler",
                    args: [self],
                  })
                  .then(function (data2) {
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
                    }
                  });
              } else {
                _rpc
                  .query({
                    model: "helpdesk.stage",
                    method: "js_get_template_sequence",
                    args: [self.value.data.id, target],
                  })
                  .then(function (data3) {
                    self_seq = data3[0]
                    target_seq = data3[1]
                    console.log("current: ", self_seq, "target_seq: ", target_seq)
                  });
                Dialog.confirm(
                  this,
                  _t(
                    "La etapa a la que estás intentando cambiar tiene una plantilla de mail. Estás segurx de que quieres cambiar a esa etapa?"
                  ),
                  {
                    confirm_callback: function () {
                      self._setValue(target);
                    },
                  }
                );
              }
            } else {
              self._setValue(target);
            }
          });
      } else {
        self._setValue(target);
      }
    },
  });
});
