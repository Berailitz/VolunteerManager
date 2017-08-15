// 'use strict;'

function login() {
  showToast('登录中', 700);
  $.getJSON('/api/tokens', {
    'username': document.getElementById('username-box').value,
    'password': document.getElementById('password-box').value
  }, function (rawData) {
    if (rawData['status']) {
      showToast('ERROR: 用户名或密码错误');
      document.getElementById('username-box').focus();
    } else {
      showToast('登录成功', 800);
      setToken(rawData['token']);
      window.location.href = '/record';
    }
  })
}