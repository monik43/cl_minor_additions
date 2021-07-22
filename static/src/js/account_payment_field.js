odoo.define('cl_minor_additions.payment', function (require) {
    "use strict";

    var core = require('web.core');
    var field_utils = require('web.field_utils');
    var QWeb = core.qweb;
    var account_payment = require('account.payment');

    account_payment.ShowPaymentLineWidget.include({
        _render: function() {
            var self = this;
            var info = JSON.parse(this.value);
            if (!info) {
                this.$el.html('');
                return;
            }
            _.each(info.content, function (k, v){
                k.index = v;
                k.amount = field_utils.format.float(k.amount, {digits: k.digits});
                if (k.date){
                    k.date = field_utils.format.date(field_utils.parse.date(k.date, {}, {isUTC: true}));
                }
            });
            this.$el.html(QWeb.render('ShowPaymentInfoCl', {
                lines: info.content,
                outstanding: info.outstanding,
                title: info.title
            }));
            _.each(this.$('.js_payment_info'), function (k, v){
                var content = info.content[v];
                var options = {
                    content: function () {
                        var $content = $(QWeb.render('PaymentPopOver', {
                            name: content.name,
                            journal_name: content.journal_name,
                            date: content.date,
                            amount: content.amount,
                            currency: content.currency,
                            position: content.position,
                            payment_id: content.payment_id,
                            move_id: content.move_id,
                            ref: content.ref,
                            account_payment_id: content.account_payment_id,
                            invoice_id: content.invoice_id,
                            invoice_view_id: content.invoice_view_id,
                        }));
                        $content.filter('.js_unreconcile_payment').on('click', self._onRemoveMoveReconcile.bind(self));
                        $content.filter('.js_open_payment').on('click', self._onOpenPayment.bind(self));
                        return $content;
                    },
                    html: true,
                    placement: 'left',
                    title: 'Payment Information',
                    trigger: 'focus',
                    delay: { "show": 0, "hide": 100 },
                };
                $(k).popover(options);
            });
        }
    });
});