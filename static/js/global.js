require('../css/global.css');

global.Cookies = require('js-cookie');

var $ageVerificationModal = $('#ageVerificationModal');
var ageVerify = Cookies.get('age_verified');

// 年龄未被验证且页面非酒精内容页面
if (ageVerify == undefined &&
  window.location.pathname.indexOf('privacy-policy') == -1) {
  // 使点击外部区域不会关闭modal
  $ageVerificationModal.modal({ backdrop: 'static', keyboard: false });
  $ageVerificationModal.modal('show');
}

$ageVerificationModal.find('button[data-dismiss=\'modal\']').click(function () {
  if ($ageVerificationModal.find('input[type=\'checkbox\']').prop('checked')) {
    Cookies.set('age_verified', true, { expires: 30 });
  } else {
    Cookies.set('age_verified', true);
  }
});

$ageVerificationModal.find('button:first').click(function () {
  window.location.href = 'about:blank';
  window.close();
});
