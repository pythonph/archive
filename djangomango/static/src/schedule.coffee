root = (exports ? window)

class Conference extends Backbone.Model
  defaults:
    startDate: null
    endDate: null
    startTime: null         # ie. 00:00 AM/PM
    duration: null          # hours
    dateRange: null
    dateRangeIterator: null

  initialize: ->
    # setup date range
    @set('dateRange', moment().range(@get('startDate'), @get('endDate')))

    # setup date range iterator
    intervalEnd = @get('startDate').clone().add('days', 1)
    @set('dateRangeIterator', moment().range(@get('startDate'), intervalEnd))


class ScheduleView extends Backbone.View
  template: '#schedule-template'

  initialize: ->
    @template = Handlebars.compile($(@template).html())

  render: ->
    context = @model.toJSON()
    context.dates = []
    context.hours = []
    context.dateRange.by context.dateRangeIterator, (moment) ->
      context.dates.push moment.format('DD MMM YYYY')

    _.each _.range(0, context.startTime.hours()), (hour) ->
      formattedHour = context.startTime.clone().add('hours', hour).format('hh:mm A')
      context.hours.push formattedHour

    $(@el).html(@template(context))


root.Schedule =
  start: ->
    conference = new Conference({
      startDate: moment("2013-06-01")
      endDate: moment("2013-06-03")
      startTime: moment([null, null, null, 9, 0]),  # 9AM
      duration: moment.duration(8, 'hours')
    })
    scheduleView = new ScheduleView({model: conference})
    scheduleView.render()
    $('#schedule-proposals').append(scheduleView.el)
