require('./bootstrap.js')
require('../css/global.css')

require('bootstrap-validator')
global.Cookies = require('js-cookie')

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

var ageVerificationModal = $('#ageVerificationModal')
var ageVerify = Cookies.get('age_verified')

// 年龄未被验证且页面非酒精内容页面
if (ageVerify == undefined &&
  window.location.pathname.indexOf('privacy-policy') == -1) {
  // 使点击外部区域不会关闭modal
  ageVerificationModal.modal({backdrop: 'static', keyboard: false})
  ageVerificationModal.modal('show')
}

ageVerificationModal.find('button[data-dismiss=\'modal\']').click(function () {
  if (ageVerificationModal.find('input[type=\'checkbox\']').prop('checked')) {
    Cookies.set('age_verified', true, {expires: 30})
  } else {
    Cookies.set('age_verified', true)
  }
})

ageVerificationModal.find('button:first').click(function () {
  window.location.href = 'about:blank'
  window.close()
})

