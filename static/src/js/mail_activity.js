odoo.define("cl_minor_additions.created_by_user", function(require){
    "use strict";
    var mail_activity = require('mail.Activity');

    mail_activity.AbstractActivityField.include({
        _render: function () {
            _.each(this.activities, function (activity) {
                if (activity.note) {
                    activity.note = utils.parse_and_transform(activity.note, utils.add_link);
                }
            });
            var activities = setDelayLabel(this.activities);
            if (activities.length) {
                var nbActivities = _.countBy(activities, 'state');
                this.$el.html(QWeb.render('create_uid_activity_items_ext', {
                    activities: activities,
                    nbPlannedActivities: nbActivities.planned,
                    nbTodayActivities: nbActivities.today,
                    nbOverdueActivities: nbActivities.overdue,
                    date_format: time.getLangDateFormat(),
                    datetime_format: time.getLangDatetimeFormat(),
                }));
            } else {
                this.$el.empty();
            }
        },
    })
})