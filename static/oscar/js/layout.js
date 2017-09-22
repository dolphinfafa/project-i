require('../css/styles.css')
require('./bootstrap-datetimepicker/bootstrap-datetimepicker.css')
require('../css/datetimepicker.css')
require('font-awesome/css/font-awesome.css')

global.$ = global.jQuery = require('jquery')
var bootstrap = require('./bootstrap3.js')
global.oscar = require('./oscar/ui.js')
require('./bootstrap-datetimepicker/bootstrap-datetimepicker.js')
require('./bootstrap-datetimepicker/locales/bootstrap-datetimepicker.all.js')

$(function () {
    oscar.init()
  }
)

