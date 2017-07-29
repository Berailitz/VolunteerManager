var column_names = ['user_id', 'volunteer_id', 'username', 'student_id', 'legal_name', 'phone'];
column_names = column_names.concat(['email', 'gender', 'age', 'volunteer_time', 'note'])
var table_lines = Array();
var container = document.getElementById('example');
var hot = new Handsontable(container, {
  colHeaders: column_names,
  columns: [
    {data: 'user_id'},
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
  data: table_lines,
});


function load_data() {
  $.getJSON("https://own.ohhere.xyz/volunteers?length=5", function(raw_lines) {
      console.log(raw_lines);
      $.each(raw_lines, function(line_index, raw_line) {
        table_lines[line_index] = JSON.parse(raw_line)
        // console.log(line);
      });
      hot.render();
    });
}

load_data();