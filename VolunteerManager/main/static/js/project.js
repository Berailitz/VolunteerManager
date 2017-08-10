'use strict;'

const COLUMN_NAMES = ['记录ID', '姓名', '学号', '工作项目', '工作日期', '时长', '记录备注', '录入人', '录入时间'];
let tableLines = [];
let container = $('#volunteer-table')[0];
let infoList = ['job_start', 'job_end', 'director', 'location', 'note'];
let jobNameDict = {};
let projectNameList = [];
let htmlTable = new Handsontable(container, {
  colHeaders: COLUMN_NAMES,
  columns: [
    { data: 'record_id' },
    { data: 'legal_name' },
    { data: 'student_id' },
    { data: 'job_name' },
    { data: 'job_date' },
    { data: 'working_time' },
    { data: 'record_note' },
    { data: 'operator_name' },
    { data: 'operation_date' },
  ],
  columnSorting: true,
  contextMenu: true,
  colWidths: [70, 120, 90, 120, 100, 70, 120, 80, 140],
  data: tableLines,
  manualColumnResize: true,
  readOnly: true,
  rowHeaders: true,
  sortIndicator: true,
  stretchH: 'all',
});

function iniConf() {
  getRelationship.then(setProjectNameMenu);
}

function setProjectNameMenu() {
  projectNameList = relationshipDict["project_name_dict"];
  $.each(projectNameList,
  (project_name, project_id) => $('#project-name-menu').append(`<li class="mdl-menu__item" tabindex="-1" data-project-index="project-${project_id + 1}">${project_name}</li>`));
   getmdlSelect.init('.getmdl-select');
}

function setJobNameMenu(project_name) {
  let job_names = project_name == '所有志愿项目' ? [] : Object.keys(relationshipDict['project_id_dict'][String(project_name_to_id(project_name))]['job_name_dict']);
  // console.log(project_name);
  $('#job-name-menu').empty();
  $('#job-name-menu').append(`<li class="mdl-menu__item" data-job-index="job-0">所有岗位</li>`);
  $('#job-name-input')[0].value = '所有岗位';
  $.each(job_names, (job_index, job_name) => $('#job-name-menu').append(`<li class="mdl-menu__item"  data-job-index="job-${job_index + 1}">${job_name}</li>`));
   getmdlSelect.init('.getmdl-select');
}

function search() {
  let project_name = $('#project-name-input')[0].value;
  let job_name = $('#job-name-input')[0].value;
  let payload = {'query_type': 'all', 'token': Cookies.get('token')};
  resetTable();
  if (project_name != '所有志愿项目') {
      payload['project_id'] = project_name_to_id(project_name);
  }
  if (job_name != '所有岗位') {
      payload['job_id'] = job_name_to_id(payload['project_id'], job_name);
  }
  $.getJSON("/api/records", payload, function (RawData) {
    setToken(RawData['token']);
    if (RawData['status']) {
      showToast(`ERROR: 查询失败: ${RawData['data']['msg']}`);
    } else {
      let count = RawData['data']['records'].length;
      tableLines.splice(0, count);
      // $.each(infoList, function (infoIndex, infoName) {
      //   $('#' + infoName.replace('_', '-') + '-box').parent().addClass('is-dirty');
      //   $('#' + infoName.replace('_', '-') + '-box')[0].value = RawData['data']['info'][infoName];
      // });
      if (count) {
        $.each(RawData['data']['records'], function (line_index, raw_line) {
          tableLines[line_index] = decodeLine(raw_line);
          // console.log(tableLines[line_index]);
        });
        htmlTable.selectCell(0, 0);
      } else {
        showToast('ERROR: 查无记录');
      }
      htmlTable.loadData(tableLines);
      htmlTable.render();
    }
  });
  showToast('查询中', 800);
}

function resetTable() {
  tableLines = [[]];
  htmlTable.loadData(tableLines);
  htmlTable.render();
  htmlTable.selectCell(0, 0);
//   $.each(infoList, function (infoIndex, infoName) {
//     $('#' + infoName.replace('_', '-') + '-box').parent().removeClass('is-dirty');
//     $('#' + infoName.replace('_', '-') + '-box')[0].value = '';
//   })
//   $('#student-id-box')[0].value = '';
//   $('#legal-name-box')[0].value = '';
//   $('#student-id-box')[0].focus();
}

iniConf();
htmlTable.loadData([[]]);