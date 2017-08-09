'use strict;'

function showToast(messageText, timeout=2000) {
  $('#snackbar')[0].MaterialSnackbar.showSnackbar(
    {
      'message': messageText,
      'timeout': timeout,
    }
  );
}

function set_token(token) {
  Cookies.set('token', token, {
    expires: 7,
    secure: true
  });
}

function login() {
  showToast('登录中', 700);
  $.getJSON('https://own.ohhere.xyz/api/tokens', {
    'username': document.getElementById('username-box').value,
    'password': document.getElementById('password-box').value
  }, function (rawData) {
    if (rawData['status']) {
      showToast('ERROR: 用户名或密码错误');
      document.getElementById('username-box').focus();
    } else {
      showToast('登录成功', 800);
      set_token(rawData['token']);
      window.location.href = 'https://own.ohhere.xyz/record';
    }
  })
}