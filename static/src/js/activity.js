odoo.define("cl_minor_additions.newtemplate", function (require) {
  "use strict";
  var mail_activity = require("mail.Activity");
  //var AbstractField = require("web.AbstractField");
  //var BasicModel = require("web.BasicModel");
  var core = require("web.core");
  //var field_registry = require("web.field_registry");
  var time = require("web.time");
  var utils = require("mail.utils");

  var QWeb = core.qweb;
  var _t = core._t;

  mail_activity.AbstractActivityField.include({
    _render: function () {
      console.log("test")
    },
  });
});
