'use strict;'

let allJobNameList = {'': []};
let jobNameList = [];
const COLUMN_NAMES = ['学号', '姓名', '时长', '志愿项目', '工作项目', '活动日期', '备注', '录入状态'];
let container = $('#record-table')[0];
let tableLines = Array();
let htmlTable = new Handsontable(container, {
  colHeaders: COLUMN_NAMES,
  columns: [
    {
      data: 'student_id',
    },
    {
      data: 'legal_name',
    },
    {
      data: 'working_time',
      type: 'numeric',
    },
    {
      data: 'project_name',
      type: 'dropdown',
      source: function (query, process) {
        process(Object.keys(relationshipDict['project_name_dict']));
      },
    },
    {
      data: 'job_name',
      type: 'dropdown',
      source: function (query, process) {
        process(jobNameList);
      },
    },
    {
      data: 'job_date',
      type: 'date',
      dateFormat: 'YYYY-MM-DD',
    },
    {
      data: 'record_note',
    },
    {
      data: 'record_status',
      readOnly: true,
    },
  ],
  columnSorting: true,
  colWidths: [100, 120, 60, 200, 120, 100, 120, 120],
  contextMenu: true,
  data: tableLines,
  manualColumnResize: true,
  renderAllRows: true,
  rowHeaders: true,
  sortIndicator: true,
  stretchH: 'all',
  afterChange: function (changes, source) {
    let rowCount = this.countRows();
    // console.log(rowCount);
    if (rowCount >= 2 && checkEmpty(this.getDataAtRow(rowCount - 2))) {
      deleteRow(1);
    };
    if (!checkEmpty(this.getDataAtRow(rowCount - 1))) {
      appendRow(1);
    };
  },
  afterSelection: function (up, left, down, right, preventScrolling) {
    // console.log(up, left, down, right, preventScrolling);
    if (left == right && up == down && right == 4) {
      let currentProjectName = tableLines[up]['project_name'];
      // console.log(allJobNameList[currentProjectName]);
      jobNameList = Object.keys(relationshipDict['project_id_dict'][String(project_name_to_id(currentProjectName))]['job_name_dict']);
      // console.log(jobNameList);
    }
  },
});

class RecordLine {
  constructor(student_id='', legal_name='', working_time='', project_name='', job_name='', job_date='', record_note='', record_status='') {
    this.student_id = student_id;
    this.legal_name = legal_name;
    this.working_time = working_time;
    this.project_name = project_name;
    this.job_name = job_name;
    this.job_date = job_date;
    this.record_note = record_note;
    this.record_status = record_status;
  }
}

function appendRow(rowCount, afterIndex) {
  // htmlTable.alter('insert_row', afterIndex ? afterIndex : htmlTable.countRows(), rowCount);
  tableLines.push(new RecordLine());
  htmlTable.loadData(tableLines);
}

function checkEmpty(LineData) {
  let isLineEmpty = true;
  let exception_index = 'record_status' in LineData ? 'record_status' : 7;
  $.each(LineData, function (index, value) {
    // console.log(index, value);
    if (value && index != exception_index) {
      isLineEmpty = false;
    }
  });
  // console.log('isLineEmpty: ' + isLineEmpty)
  return isLineEmpty;
}

function checkFull(LineData) {
  let isLineFull = true;
  let exception_index = 'record_status' in LineData ? 'record_status' : 7;
  $.each(LineData, function (index, value) {
    // console.log(index, value);
    if (!value && index != exception_index) {
      isLineFull = false;
    }
  });
  // console.log('isLineEmpty: ' + isLineEmpty)
  return isLineFull;
}

function deleteRow(rowCount = 1, afterIndex = htmlTable.countRows() - 1) {
  tableLines.splice(afterIndex, rowCount);
  htmlTable.loadData(tableLines);
}

function encodeLine(rawLine) {
  rawLine['project_id'] = project_name_to_id(rawLine['project_name']);
  rawLine['job_id'] = job_name_to_id(rawLine['project_id'], rawLine['job_name']);
  return rawLine;
}

function getTestRecordline() {
  return new RecordLine('2012110649', "徐盈盈", 1, "a", "a", "2017-08-16", "aa", "");
}

function loadOnlineData(page, length) {
  $.getJSON("/api/records",{
    'page': page,
    'length': length,
    'query_type': 'page',
    'token': Cookies.get('token')
  }, function(rawResponse) {
      // console.log(rawResponse);
      set_token(rawResponse['token']);
      tableLines.splice(0, tableLines.length);
      $.each(rawResponse['data'], function(LineIndex, rawLine) {
        rawLine.record_status = '已录入';
        tableLines[LineIndex] = rawLine
        console.log(rawLine);
      });
      htmlTable.loadData(tableLines);
      htmlTable.render();
      appendRow(1);
    });
}

function resetCurcor() {
  htmlTable.selectCell(0, 0);
}

function resetTable() {
  tableLines = [new RecordLine()];
  htmlTable.loadData(tableLines);
  resetCurcor()
}

function submitAll() {
  showToast('正在录入', 700);
  $.each(tableLines, function (LineIndex, LineData) {
    // console.log(LineData['record_status'] == '未录入' && !checkEmpty(LineData));
    if (LineData['record_status'] != '已录入' && !checkEmpty(LineData)) {
      if (!checkFull(LineData)) {
        showToast(`ERROR: #${LineIndex + 1} 需补充信息`, 800);
        LineData['record_status'] = '需补充信息';
      } else {
        LineData['record_status'] = '正在录入';
        htmlTable.loadData(tableLines);
        $.post("/api/records", {
          'data': JSON.stringify(encodeLine(LineData)),
          'token': Cookies.get('token')
        }, function (SubmitResponse, TextStatus, jqXHR) {
          // console.log(SubmitResponse['data']);
          set_token(SubmitResponse['token']);
          LineData['record_status'] = SubmitResponse['data']['msg'];
        });
      };
    };
  });
  htmlTable.loadData(tableLines);
  resetCurcor();
}

function tranferToItem(lineList) {
  return new RecordLine(...lineList);
}

appendRow(1);
tableLines[0] = getTestRecordline();
resetCurcor()