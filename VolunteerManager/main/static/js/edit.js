'use strict;'

let infoList = ['legal_name', 'student_id', 'working_time', 'project_name', 'job_name', 'job_date', 'note'];

function search() {
  let record_id = $('#record-id-box')[0].value;
  if (record_id && !$.isNumeric(record_id)) {
    showToast('ERROR: 记录不为整数');
    $('#student-id-box')[0].focus();
    return;
  }
  $.getJSON("/api/records", {
    'record_id': record_id,
    'query_type': 'one',
    'token': Cookies.get('token')
  }, function (rawResponse) {
    if (rawResponse['status']) {
      showToast(`ERROR: 查询失败: ${rawResponse['data']['msg']}`);
    } else {
      setToken(rawResponse['token']);
      rawRecord = rawResponse['data']['records'][0]
      console.log(rawRecord);
      rawRecord = decodeLine(rawRecord);
      $.each(infoList, function (infoIndex, infoName) {
        $('#' + infoName.replace('_', '-') + '-box').parent().addClass('is-dirty');
        $('#' + infoName.replace('_', '-') + '-box')[0].value = rawRecord[infoName] ? rawRecord[infoName] : '';
      });
    }
  });
  showToast('查询中', 800);
}
