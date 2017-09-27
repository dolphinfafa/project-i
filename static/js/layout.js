require('bootstrap/dist/css/bootstrap.css')
require('../css/bootstrap4/utilities.css')
require('../css/global.css')

require('font-awesome/css/font-awesome.css')
global.$ = global.jQuery = require('jquery')
require('bootstrap')

var joinMessageForm = $('#joinMessageModal form')
var joinMessageModal = $('#joinMessageModal')
joinMessageModal.find('button[type=\'submit\']').click(function (e) {
  e.preventDefault()
  $.ajax({
    type: 'POST',
    url: joinMessageForm.attr('action'),
    data: joinMessageForm.serialize(),
    success: function (data) {
      joinMessageModal.modal('hide')
      joinMessageForm[0].reset()
    },
    error: function (jqXHR) {
      if (jqXHR.status == 400) {
        console.log($.parseJSON(jqXHR.responseText))
        alert($.parseJSON(jqXHR.responseText)['error'])
      } else {
        alert('Server error, please try again.')
      }
    },
    dataType: 'json',
  })
})
