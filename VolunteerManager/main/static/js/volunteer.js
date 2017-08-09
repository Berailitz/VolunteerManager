'use strict;'

let COLUMN_NAMES = ['记录ID', '志愿项目', '工作项目', '工作日期', '时长', '记录备注', '录入人', '录入时间'];
let tableLines = [];
let container = $('#volunteer-table')[0];
let infoList = ['volunteer_id', 'gender', 'volunteer_time', 'phone', 'email', 'note'];
let htmlTable = new Handsontable(container, {
  colHeaders: COLUMN_NAMES,
  columns: [
    { data: 'record_id' },
    { data: 'project_name' },
    { data: 'job_name' },
    { data: 'job_date' },
    { data: 'working_time' },
    { data: 'record_note' },
    { data: 'operator_name' },
    { data: 'operation_date' },
  ],
  columnSorting: true,
  contextMenu: true,
  colWidths: [80, 200, 120, 100, 70, 120, 80, 140],
  data: tableLines,
  manualColumnResize: true,
  readOnly: true,
  rowHeaders: true,
  sortIndicator: true,
  // stretchH: 'all'
});

function search() {
  let student_id = $('#student-id-box')[0].value;
  let legal_name = $('#legal-name-box')[0].value;
  resetTable();
  if (student_id && !$.isNumeric(student_id)) {
    showToast('ERROR: 学号不为整数');
    $('#student-id-box')[0].focus();
    return;
  }
  $.getJSON("/api/volunteers", {
    'student_id': student_id,
    'legal_name': legal_name,
    'query_type': 'one',
    'token': Cookies.get('token')
  }, function (rawResponse) {
    if (rawResponse['status']) {
      showToast(`ERROR: 查询失败: ${rawResponse['data']['msg']}`);
    } else {
      console.log(rawResponse['data']);
      setToken(rawResponse['token']);
      tableLines.splice(0, tableLines.length);
      if (rawResponse['status'] == 1) {
        tableLines = [[]];
        $('#student-id-box')[0].focus();
        showToast('ERROR: 查无此人', 800);
      } else {
        $.each(infoList, function (infoIndex, infoName) {
          $('#' + infoName.replace('_', '-') + '-box').parent().addClass('is-dirty');
          $('#' + infoName.replace('_', '-') + '-box')[0].value = rawResponse['data']['info'][infoName];
        });
        $.getJSON('/api/records', {
          'user_id': rawResponse['data']['info']['user_id'],
          'query_type': 'all',
          'token': Cookies.get('token')
        }, function (rawResponse) {
          if (rawResponse['status']) {
            showToast(`ERROR: 查询失败: ${rawResponse['data']['msg']}`);
          } else {
            console.log(rawResponse['data']['records']);
            setToken(rawResponse['token']);
            if (rawResponse['data']['records'].length == 0) {
              showToast('ERROR: 查无记录', 800);
              $('#student-id-box')[0].focus();
              return;
            }
            $.each(rawResponse['data']['records'], function (line_index, raw_line) {
              tableLines[line_index] = decodeLine(raw_line);
              // console.log(tableLines[line_index]);
            });
          }
        });
        htmlTable.render();
        htmlTable.selectCell(0, 0);
      }
    }
  });
  showToast('查询中', 800);
}

function loadData(page, length) {
  $.getJSON("/api/volunteers", {
    'page': page,
    'length': length,
    'query_type': 'page',
    'token': Cookies.get('token')
  }, function (rawResponse) {
    if (rawResponse['status']) {
      showToast(`ERROR: 查询失败: ${rawResponse['data']['msg']}`);
    } else {
      console.log(rawResponse);
      setToken(rawResponse['token']);
      tableLines.splice(0, tableLines.length);
      $.each(rawResponse['data'], function (lineIndex, rawLine) {
        tableLines[lineIndex] = rawLine;
        // console.log(line);
      });
      htmlTable.render();
      htmlTable.selectCell(0, 0);
    }
  });
}

function resetTable() {
  tableLines = [[]];
  htmlTable.loadData(tableLines);
  htmlTable.render();
  htmlTable.selectCell(0, 0);
  $.each(infoList, function (infoIndex, infoName) {
    $('#' + infoName.replace('_', '-') + '-box').parent().removeClass('is-dirty');
    $('#' + infoName.replace('_', '-') + '-box')[0].value = '';
  })
  // $('#student-id-box')[0].value = '';
  // $('#legal-name-box')[0].value = '';
}

// loadData(1, 20);

htmlTable.loadData([[]]);