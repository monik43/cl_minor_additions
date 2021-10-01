odoo.define("cl_minor_additions.created_by_user", function (require) {
  "use strict";
  var core = require("web.core");
  var ajax = require("web.ajax");
  var qweb = core.qweb;
  ajax.loadXML("/cl_minor_additions/static/src/xml/activity_items_extend_created_by.xml", qweb);
});
