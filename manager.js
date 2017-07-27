var data = [
  ["", "Ford", "Volvo", "Toyota", "Honda"],
  ["2016", 10, 11, 12, 13],
  ["2017", 20, 11, 14, 13],
  ["2018", 30, 15, 12, 13]
];

var container = document.getElementById('example');
var hot = new Handsontable(container, {
  rowHeaders: true,
  colHeaders: true,
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
  $.ajax(
    {
      url: "https://own.ohhere.xyz/volunteers?length=1",
      type: "GET",
      dataType: "json",
      async: true,
      success: function (res) {
        console.log(res)
        json = JSON.parse(res)
        hot.loadData(json);
      }
    }
  )
}

load_data();