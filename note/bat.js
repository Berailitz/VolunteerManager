function import_hour(IDType, ProjectID, JobID) {
    $.post('opp.my.php?manage_type=0&m=import_hour&item=hour&opp_id=' + str(ProjectID), { 'content': BatText, 'vol_type': IDType, 'opp_id': ProjectID, 'job_id': JobID }, function(data) {
        var ret = $.evalJSON(data);
        if (ret.code == 0) {
            // $('#vols').html(data);
            var h1 = '<table class="table1">';
            var h2 = '<table class="table1 m10">';
            h1 += '<tr><th>状态</th><th>志愿者ID</th><th>项目ID</th><th>时长</th></tr>';
            h2 += '<tr><th>状态</th><th>志愿者ID</th><th>项目ID</th><th>时长</th></tr>';
            for (var i = 0; i < ret.data.length; i++) {
                var a = ret.data[i];
                h1 += '<tr>';
                h1 += '<td><font color=green>' + a.msg + '</font></td>';
                h1 += '<td>' + a.vol_id + '</td>';
                h1 += '<td>' + a.opp_id + '</td>';
                h1 += '<td>' + a.hour_num + '</td>';
                h1 += '</tr>';
            }
            for (var i = 0; i < ret.failed.length; i++) {
                var a = ret.failed[i];
                h2 += '<tr>';
                h2 += '<td><font color=red>' + a.msg + '</font></td>';
                h2 += '<td>' + a.vol_id + '</td>';
                h2 += '<td>' + a.opp_id + '</td>';
                h2 += '<td>' + a.hour_num + '</td>';
                h2 += '</tr>';
            }
            h1 += '</table>';
            h2 += '</table>';
            $('#vols').html(h1 + h2);
        } else {
            // C.alert.alert({ content: ret.msg });
        }
    });
}
