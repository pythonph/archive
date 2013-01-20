(function() {
  var Conference, ScheduleView, root,
    __hasProp = {}.hasOwnProperty,
    __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

  root = typeof exports !== "undefined" && exports !== null ? exports : window;

  Conference = (function(_super) {

    __extends(Conference, _super);

    function Conference() {
      return Conference.__super__.constructor.apply(this, arguments);
    }

    Conference.prototype.defaults = {
      startDate: null,
      endDate: null,
      startTime: null,
      duration: null,
      dateRange: null,
      dateRangeIterator: null
    };

    Conference.prototype.initialize = function() {
      var intervalEnd;
      this.set('dateRange', moment().range(this.get('startDate'), this.get('endDate')));
      intervalEnd = this.get('startDate').clone().add('days', 1);
      return this.set('dateRangeIterator', moment().range(this.get('startDate'), intervalEnd));
    };

    return Conference;

  })(Backbone.Model);

  ScheduleView = (function(_super) {

    __extends(ScheduleView, _super);

    function ScheduleView() {
      return ScheduleView.__super__.constructor.apply(this, arguments);
    }

    ScheduleView.prototype.template = '#schedule-template';

    ScheduleView.prototype.initialize = function() {
      return this.template = Handlebars.compile($(this.template).html());
    };

    ScheduleView.prototype.render = function() {
      var context;
      context = this.model.toJSON();
      context.dates = [];
      context.hours = [];
      context.dateRange.by(context.dateRangeIterator, function(moment) {
        return context.dates.push(moment.format('DD MMM YYYY'));
      });
      _.each(_.range(0, context.startTime.hours()), function(hour) {
        var formattedHour;
        formattedHour = context.startTime.clone().add('hours', hour).format('hh:mm A');
        return context.hours.push(formattedHour);
      });
      return $(this.el).html(this.template(context));
    };

    return ScheduleView;

  })(Backbone.View);

  root.Schedule = {
    start: function() {
      var conference, scheduleView;
      conference = new Conference({
        startDate: moment("2013-06-01"),
        endDate: moment("2013-06-03"),
        startTime: moment([null, null, null, 9, 0]),
        duration: moment.duration(8, 'hours')
      });
      scheduleView = new ScheduleView({
        model: conference
      });
      scheduleView.render();
      return $('#schedule-proposals').append(scheduleView.el);
    }
  };

}).call(this);
