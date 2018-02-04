'use strict;'

function download_code() {
  $.getJSON(
    '/api/code', {
      'token': Cookies.get('token'),
      'project_id': $('#project-id-input')[0].value,
      'job_id': $('#job-id-input')[0].value
    },
    function(rawData) {
      console.log(rawData);
      setToken(rawData['token']);
      if (rawData['status']) {
        showToast(`ERROR: 下载失败: ${rawData['data']['msg']}`);
      } else {
        showToast('下载中');
        document.location.href = rawData['data']['download_url'];
      }
    }
  );
}

function generate_code() {
  $.ajax({
    url: '/api/code',
    type: 'PUT',
    data: {
      'token': Cookies.get('token'),
      'project_id': $('#project-id-input')[0].value,
      'job_id': $('#job-id-input')[0].value,
      'code_amount': $('#code-amount-input')[0].value,
      'code_hour': $('#code-hour-input')[0].value,
      'code_note': $('#code-note-input')[0].value
    },
    success: function(rawData) {
      console.log(rawData);
      setToken(rawData['token']);
      if (rawData['status']) {
        showToast(`ERROR: 操作失败: ${rawData['data']['msg']}`);
      } else {
        showToast('生成成功');
        download_code();
      }
    }
  });
}