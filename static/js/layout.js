require('./bootstrap.js')
require('./global.js')

require('bootstrap-validator')

;
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
var joinMessageSubmitButton = joinMessageModal.find('button[type=\'submit\']')
joinMessageSubmitButton.click(function (e) {
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

var invalidFields = {}

// 如果表单验证通过 则移除disabled属性
joinMessageForm.on('valid.bs.validator', function (e) {
  delete invalidFields[e.relatedTarget.name]
  if ($.isEmptyObject(invalidFields)) {
    joinMessageSubmitButton.removeAttr('disabled')
  }
})

// 如果表单验证失败 则disable submit button
joinMessageForm.on('invalid.bs.validator', function (e) {
  invalidFields[e.relatedTarget.name] = true
  joinMessageSubmitButton.attr('disabled', 'disabled')
})

