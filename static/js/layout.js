require('bootstrap/dist/css/bootstrap.css')
require('../css/bootstrap4/utilities.css')
require('../css/global.css')

require('font-awesome/css/font-awesome.css')
global.$ = global.jQuery = require('jquery')
require('bootstrap');

(function ($) {
  $.fn.serializeJSON = function () {
    var serializeObj = {}
    var array = this.serializeArray()
    $(array).each(function () {
      if (serializeObj[this.name]) {
        if ($.isArray(serializeObj[this.name])) {
          serializeObj[this.name].push(this.value)
        } else {
          serializeObj[this.name] = [serializeObj[this.name], this.value]
        }
      } else {
        serializeObj[this.name] = this.value
      }
    })
    return serializeObj
  }
})(jQuery)

var joinMessageForm = $('#joinMessageModal form')
var joinMessageModal = $('#joinMessageModal')
joinMessageModal.find('button[type=\'submit\']').click(function (e) {
  e.preventDefault()
  $.ajax({
    type: 'PUT',
    url: joinMessageForm.attr('action'),
    data: JSON.stringify(joinMessageForm.serializeJSON()),
    success: function (data) {
      joinMessageModal.modal('hide')
      joinMessageForm[0].reset()
    },
    error: function (jqXHR) {
      if (jqXHR.status == 400) {
        console.log($.parseJSON(jqXHR.responseText))
        alert($.parseJSON(jqXHR.responseText)['error'])
      } else {
        alert(
          'Oops, it seems that something went wrong, please try again later.')
      }
    },
    dataType: 'json',
    contentType: 'application/json; charset=utf-8',
  })
})
