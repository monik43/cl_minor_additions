odoo.define("cl_minor_additions.created_by_user", function (require) {
  "use strict";
  var mail_activity = require("mail.Activity");
  var AbstractField = require("web.AbstractField");
  var AbstractActivityField = require("mail.AbstractActivityField");
  var BasicModel = require("web.BasicModel");
  var core = require("web.core");
  var field_registry = require("web.field_registry");
  var time = require("web.time");
  var utils = require("mail.utils");

  var QWeb = core.qweb;
  var _t = core._t;

  mail_activity.AbstractActivityField.include({
    className: "o_mail_activity",
    events: {
      "click .o_activity_edit": "_onEditActivity",
      "click .o_activity_unlink": "_onUnlinkActivity",
      "click .o_activity_done": "_onMarkActivityDone",
    },
    specialData: "_fetchSpecialActivity",

    // inherited
    init: function () {
      this._super.apply(this, arguments);
      this.activities = this.record.specialData[this.name];
    },
    _render: function () {
      _.each(this.activities, function (activity) {
        if (activity.note) {
          activity.note = utils.parse_and_transform(
            activity.note,
            utils.add_link
          );
        }
      });
      var activities = setDelayLabel(this.activities);
      if (activities.length) {
        var nbActivities = _.countBy(activities, "state");
        this.$el.html(
          QWeb.render("activity_items", {
            activities: activities,
            nbPlannedActivities: nbActivities.planned,
            nbTodayActivities: nbActivities.today,
            nbOverdueActivities: nbActivities.overdue,
            date_format: time.getLangDateFormat(),
            datetime_format: time.getLangDatetimeFormat(),
          })
        );
      } else {
        this.$el.empty();
      }
    },
    _reset: function (record) {
      this._super.apply(this, arguments);
      this.activities = this.record.specialData[this.name];
      // the mail widgets being persistent, one need to update the res_id on reset
      this.res_id = record.res_id;
    },

    // public
    scheduleActivity: function (previous_activity_type_id) {
      var callback = this._reload.bind(this, { activity: true, thread: true });
      return this._scheduleActivity(false, previous_activity_type_id, callback);
    },
    // private
    _reload: function (fieldsToReload) {
      this.trigger_up("reload_mail_fields", fieldsToReload);
    },

    /** Binds a focusout handler on a bootstrap popover
     *  Useful to do some operations on the popover's HTML,
     *  like keeping the user's input for the feedback
     *  @param {JQuery} $popover_el: the element on which
     *    the popover() method has been called
     */
    _bindPopoverFocusout: function ($popover_el) {
      var self = this;
      // Retrieve the actual popover's HTML
      var $popover = $popover_el.data("bs.popover").tip();
      var activity_id = $popover_el.data("activity-id");
      $popover.off("focusout");
      $popover.focusout(function (e) {
        // outside click of popover hides the popover
        // e.relatedTarget is the element receiving the focus
        self.feedbackValue[activity_id] = $popover
          .find("#activity_feedback")
          .val()
          .trim();
        if (
          !$popover.is(e.relatedTarget) &&
          !$popover.find(e.relatedTarget).length
        ) {
          $popover_el.popover("hide");
        }
      });
    },

    // handlers
    _onEditActivity: function (event, options) {
      event.preventDefault();
      var self = this;
      var activity_id = $(event.currentTarget).data("activity-id");
      var action = _.defaults(options || {}, {
        type: "ir.actions.act_window",
        res_model: "mail.activity",
        view_mode: "form",
        view_type: "form",
        views: [[false, "form"]],
        target: "new",
        context: {
          default_res_id: this.res_id,
          default_res_model: this.model,
        },
        res_id: activity_id,
      });
      return this.do_action(action, {
        on_close: function () {
          self._reload({ activity: true, thread: true });
        },
      });
    },
    _onUnlinkActivity: function (event, options) {
      event.preventDefault();
      var activity_id = $(event.currentTarget).data("activity-id");
      options = _.defaults(options || {}, {
        model: "mail.activity",
        args: [[activity_id]],
      });
      return this._rpc({
        model: options.model,
        method: "unlink",
        args: options.args,
      }).then(this._reload.bind(this, { activity: true }));
    },

    _onMarkActivityDone: function (event) {
      event.preventDefault();
      var self = this;
      this.feedbackValue = this.feedbackValue || {};
      var $popover_el = $(event.currentTarget);
      var activity_id = $popover_el.data("activity-id");
      var previous_activity_type_id = $popover_el.data(
        "previous-activity-type-id"
      );
      if (!$popover_el.data("bs.popover")) {
        this.feedbackValue[activity_id] = "";
        $popover_el
          .popover({
            title: _t("Feedback"),
            html: "true",
            trigger: "click",
            content: function () {
              var $popover = $(
                QWeb.render("mail.activity_feedback_form", {
                  previous_activity_type_id: previous_activity_type_id,
                })
              );
              $popover
                .find("#activity_feedback")
                .val(self.feedbackValue[activity_id]);
              $popover.on(
                "click",
                ".o_activity_popover_done_next",
                function () {
                  var feedback = _.escape(
                    $popover.find("#activity_feedback").val()
                  );
                  var previous_activity_type_id =
                    $popover_el.data("previous-activity-type-id") || false;
                  self
                    ._markActivityDone(activity_id, feedback)
                    .then(
                      self.scheduleActivity.bind(
                        self,
                        previous_activity_type_id
                      )
                    );
                }
              );
              $popover.on("click", ".o_activity_popover_done", function () {
                var feedback = _.escape(
                  $popover.find("#activity_feedback").val()
                );
                self
                  ._markActivityDone(activity_id, feedback)
                  .then(
                    self._reload.bind(self, { activity: true, thread: true })
                  );
              });
              $popover.on("click", ".o_activity_popover_discard", function () {
                $popover_el.popover("hide");
              });
              return $popover;
            },
          })
          .on("show.bs.popover", function (e) {
            var $popover = $(this).data("bs.popover").tip();
            $popover.addClass("o_mail_activity_feedback").attr("tabindex", 0);
            $(".o_mail_activity_feedback.popover")
              .not(e.target)
              .popover("hide");
          })
          .on("shown.bs.popover", function () {
            var $popover = $(this).data("bs.popover").tip();
            $popover.find("#activity_feedback").focus();
            self._bindPopoverFocusout($(this));
          })
          .popover("show");
      }
    },
  });
});
