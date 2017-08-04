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
  stretchH: 'all',
});

function search() {
  let student_id = $('#student-id-box')[0].value;
  let legal_name = $('#legal-name-box')[0].value;
  if (student_id && !$.isNumeric(student_id)) {
    showToast('ERROR: 学号不为整数');
    return;
  }
  $.getJSON("https://own.ohhere.xyz/volunteers", {
    'student_id': student_id,
    'legal_name': legal_name,
  }, function (rawResponse) {
    console.log(rawResponse['data']);
    tableLines.splice(0, tableLines.length);
    if (rawResponse['data'].length == 0) {
      tableLines = [[]];
      $('#student-id-box')[0].focus();
      showToast('ERROR: 查无此人');
    } else {
      $.each(infoList, function (infoIndex, infoName) {
        $('#' + infoName.replace('_', '-') + '-box').parent().addClass('is-dirty');
        $('#' + infoName.replace('_', '-') + '-box')[0].value = rawResponse['data']['info'][infoName];
      });
      $.each(rawResponse['data']['records'], function (line_index, raw_line) {
        tableLines[line_index] = raw_line;
        // console.log(tableLines[line_index]);
      });
      htmlTable.selectCell(0, 0);
    }
    htmlTable.loadData(tableLines);
    htmlTable.render();
  });
}

function loadData(page, length) {
  $.getJSON("https://own.ohhere.xyz/volunteers", {
    'page': page,
    'length': length
  }, function (rawResponse) {
    console.log(rawResponse);
    tableLines.splice(0, tableLines.length);
    $.each(rawResponse['data'], function (lineIndex, rawLine) {
      tableLines[lineIndex] = rawLine;
      // console.log(line);
    });
    htmlTable.render();
    htmlTable.selectCell(0, 0);
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
}

function showToast(messageText) {
  $('#snackbar')[0].MaterialSnackbar.showSnackbar(
    {
      message: messageText,
    }
  );
}

// loadData(1, 20);

htmlTable.loadData([[]]);