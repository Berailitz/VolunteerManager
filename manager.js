var column_names = ['user_id', 'volunteer_id', 'username', 'student_id', 'legal_name', 'phone'];
column_names = column_names.concat(['email', 'gender', 'age', 'volunteer_time', 'note'])

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
  ]
});

function load_data() {
  $.getJSON("https://own.ohhere.xyz/volunteers?length=5", function(res) {
      console.log(res);
      $.each(res, function(vol_index, one_vol) {
        json_one = JSON.parse(one_vol)
        console.log(json_one);
        hot.alter('insert_row', hot.countRows(), 1, json_one);
      })
    });
}

load_data();