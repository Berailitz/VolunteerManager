'use strict;'

let editHandle = (function () {
  let infoList = ['legal_name', 'student_id', 'working_time', 'project_name', 'job_name', 'working_date', 'note', 'operator_name', 'operation_time'];
  let record_id;
  
  let encodeLine = function (rawLine) {
    rawLine['project_id'] = project_name_to_id(rawLine['project_name']);
    rawLine['job_id'] = job_name_to_id(rawLine['project_id'], rawLine['job_name']);
    return rawLine;
  }
  
  let setProjectNameMenu = function () {
    projectNameList = relationshipDict["project_name_dict"];
    $.each(projectNameList,
    (project_name, project_id) => $('#project-name-menu').append(`<li class="mdl-menu__item" tabindex="-1" data-project-index="project-${project_id + 1}">${project_name}</li>`));
     getmdlSelect.init('.getmdl-select');
  }
  
  let setJobNameMenu = function () {
    project_name = $('#project-name-input')[0].value
    if (project_name) {
      let job_names = Object.keys(relationshipDict['project_id_dict'][String(project_name_to_id(project_name))]['job_name_dict']);
      // console.log(project_name);
      $('#job-name-menu').empty();
      $('#job-name-input')[0].value = job_names[0];
      $.each(job_names, (job_index, job_name) => $('#job-name-menu').append(`<li class="mdl-menu__item"  data-job-index="job-${job_index + 1}">${job_name}</li>`));
    } else {
      $('#job-name-menu').empty();
      $('#job-name-input')[0].value = '';
    }
    getmdlSelect.init('.getmdl-select');
  }
  
  let showLegalName = function (params) {
    $.getJSON('/api/volunteers', {
      'token': Cookies.get('token'),
      'query_type': 'one',
      'student_id': $('#student-id-input')[0].value
    }, function (raeData) {
      setToken(raeData['token']);
      if (raeData['status']) {
        $('#legal-name-input')[0].value = '';
        showToast(`ERROR: 查无此人: ${raeData['data']['msg']}`);
      } else {
        $('#legal-name-input')[0].value = raeData['data']['info']['legal_name'];
      }
    });
  }
  
  let search_record = function () {
    record_id = $('#record-id-input')[0].value;
    if (record_id && !$.isNumeric(record_id)) {
      showToast('ERROR: 记录ID不为整数');
      $('#record-id-input')[0].focus();
      return;
    }
    $.each(infoList, function (infoIndex, infoName) {
      $('#' + infoName.replace('_', '-') + '-input').parent().removeClass('is-dirty');
      $('#' + infoName.replace('_', '-') + '-input')[0].value = '';
    });
    $.getJSON("/api/records", {
      'record_id': record_id,
      'query_type': 'one',
      'token': Cookies.get('token')
    }, function (raeData) {
      setToken(raeData['token']);
      if (raeData['status']) {
        showToast(`ERROR: 查询失败: ${raeData['data']['msg']}`);
      } else {
        rawRecord = raeData['data']['records'][0]
        console.log(rawRecord);
        rawRecord = decodeLine(rawRecord);
        $.each(infoList, function (infoIndex, infoName) {
          $('#' + infoName.replace('_', '-') + '-input').parent().addClass('is-dirty');
          $('#' + infoName.replace('_', '-') + '-input')[0].value = rawRecord[infoName] ? rawRecord[infoName] : '';
        });
      }
      setJobNameMenu();
    });
    showToast('查询中', 800);
  }
  
  let update_record = function () {
    let currentRecord = new Object();
    $.each(infoList, function (infoIndex, infoName) {
      currentValue = $('#' + infoName.replace('_', '-') + '-input')[0].value;
      if (currentValue) {
        currentRecord[infoName] = currentValue;
      }
    });
    currentRecord['record_id'] = record_id;
    currentRecord = encodeLine(currentRecord);
    $.post('/api/records', {
      'token': Cookies.get('token'),
      'query_type': 'one',
      'data': JSON.stringify(currentRecord)
    }, function (rawData) {
      setToken(rawData['token']);
      if (rawData['status']) {
        showToast(`ERROR: 提交失败: ${rawData['data']['msg']}`);
      } else {
        showToast('修改成功');
        $('#record-id-input')[0].focus();
      }
    })
  }
  
  let delete_record = function () {
    $.ajax({
      url: '/api/records',
      type: 'DELETE',
      data: {'token': Cookies.get('token'), 'data': JSON.stringify({'record_id': record_id})},
      success: function (rawData) {
        setToken(rawData['token']);
        if (rawData['status']) {
          showToast(`ERROR #${record_id}删除失败: ${rawData['data']['msg']}`);
        } else {
          showToast(`#${record_id}删除成功`);
          $.each(infoList, function (infoIndex, infoName) {
            $('#' + infoName.replace('_', '-') + '-input').parent().removeClass('is-dirty');
            $('#' + infoName.replace('_', '-') + '-input')[0].value = '';
          });
        }
      }
    });
  }
  
  let iniConf = function () {
    getRelationship.then(setProjectNameMenu);
  }
  
  iniConf();
});
