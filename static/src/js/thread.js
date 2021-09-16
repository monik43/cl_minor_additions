odoo.define("cl_minor_additions.change_update_date", function (require) {
  "use strict";

  var chatThread = require("mail.ChatThread");

  chatThread.include({
    update_timestamps: function () {
      /*
            var isAtBottom = this.is_at_bottom();
            this.$('.o_mail_timestamp').each(function() {
                var date = $(this).data('date');
                $(this).html(time_from_now(date));
            });
            if (isAtBottom && !this.is_at_bottom()) {
                this.scroll_to();
            }
      */
    },
  });
});
