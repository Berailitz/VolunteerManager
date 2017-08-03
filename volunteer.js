var column_names = ['志愿者编号', '志愿北京用户名', '学号', '姓名', '手机号', '邮箱', '性别', '年龄', '累计时长', '备注'];
column_names = column_names.concat(['email', 'gender', 'age', 'volunteer_time', 'note'])
var table_lines = Array();
var container = document.getElementById('example');
var hot = new Handsontable(container, {
  colHeaders: column_names,
  columns: [
    {data: 'volunteer_id'},
    {data: 'username'}, 
    {data: 'student_id'},
    {data: 'legal_name'},
    {data: 'phone'},
    {data: 'email'},
    {data: 'gender'},
    {data: 'age'},
    {data: 'volunteer_time'},
    {data: 'note'},
  ],
  rowHeaders: true,
  data: table_lines,
  contextMenu: true
});

function load_data(page, length) {
  $.getJSON("https://own.ohhere.xyz/volunteers",{
    'page': page,
    'length': length
  }, function(raw_lines) {
      console.log(raw_lines);
      table_lines.splice(0, table_lines.length);
      $.each(raw_lines['data'], function(line_index, raw_line) {
        table_lines[line_index] = JSON.parse(raw_line);
        // console.log(line);
      });
      hot.render();
    });
}

function append_row(line_count) {
  hot.alter('insert_row', hot.countRows(), line_count);
}

function submit_line(line_index) {
  var submit_data = $.post("https://own.ohhere.xyz/volunteers", {
    'data': JSON.stringify(table_lines[line_index])
  }, function (submit_response, textStatus, jqXHR) {
    console.log(submit_response);
  });
}

load_data(1, 20);