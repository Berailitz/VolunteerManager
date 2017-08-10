'use strict;'

let infoList = ['legal_name', 'student_id', 'working_time', 'project_name', 'job_name', 'job_date', 'note', 'operator_name', 'operation_date'];

function encodeLine(rawLine) {
  rawLine['project_id'] = project_name_to_id(rawLine['project_name']);
  rawLine['job_id'] = job_name_to_id(rawLine['project_id'], rawLine['job_name']);
  return rawLine;
}

function setProjectNameMenu() {
  projectNameList = relationshipDict["project_name_dict"];
  $.each(projectNameList,
  (project_name, project_id) => $('#project-name-menu').append(`<li class="mdl-menu__item" tabindex="-1" data-project-index="project-${project_id + 1}">${project_name}</li>`));
   getmdlSelect.init('.getmdl-select');
}

function setJobNameMenu(project_name) {
  let job_names = relationshipDict['project_id_dict'][String(project_name_to_id(project_name))]['job_id_dict'];
  // console.log(project_name);
  $('#job-name-menu').empty();
  $('#job-name-input')[0].value = job_names[0];
  $.each(job_names, (job_index, job_name) => $('#job-name-menu').append(`<li class="mdl-menu__item"  data-job-index="job-${job_index + 1}">${job_name}</li>`));
   getmdlSelect.init('.getmdl-select');
}

function search() {
  let record_id = $('#record-id-input')[0].value;
  if (record_id && !$.isNumeric(record_id)) {
    showToast('ERROR: 记录ID不为整数');
    $('#record-id-input')[0].focus();
    return;
  }
  $.getJSON("/api/records", {
    'record_id': record_id,
    'query_type': 'one',
    'token': Cookies.get('token')
  }, function (rawResponse) {
    setToken(rawResponse['token']);
    if (rawResponse['status']) {
      showToast(`ERROR: 查询失败: ${rawResponse['data']['msg']}`);
    } else {
      rawRecord = rawResponse['data']['records'][0]
      console.log(rawRecord);
      rawRecord = decodeLine(rawRecord);
      $.each(infoList, function (infoIndex, infoName) {
        $('#' + infoName.replace('_', '-') + '-input').parent().addClass('is-dirty');
        $('#' + infoName.replace('_', '-') + '-input')[0].value = rawRecord[infoName] ? rawRecord[infoName] : '';
      });
    }
  });
  showToast('查询中', 800);
}

function update() {
  let currentRecord = new Object();
  $.each(infoList, function (infoIndex, infoName) {
    currentValue = $('#' + infoName.replace('_', '-') + '-input')[0].value;
    if (currentValue) {
      currentRecord[infoName] = currentValue;
    }
  });
  currentRecord = encodeLine(currentRecord);
  $.post('/api/records', {
    'token': Cookies.get('token'),
    'data': JSON.stringify(currentRecord)
  }, function (rawData) {
    setToken(rawResponse['token']);
    if (rawResponse['status']) {
      showToast(`ERROR: 提交失败: ${rawResponse['data']['msg']}`);
    } else {
      showToast('修改成功');
      $('#record-id-input')[0].focus();
    }
  })
}

function iniConf() {
  getRelationship.then(setProjectNameMenu);
}

iniConf();