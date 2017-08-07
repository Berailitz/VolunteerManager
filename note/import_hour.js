function import_hour(){
    try{
        
        var vol_type=$('input[@name="vol_type"][checked]').val();
        var opp_id=$('#import_hour').find('#opp_id').val();
        var job_id=$('#import_hour').find('#job_id').val();
        C.alert.opacty({content:'<div style="margin-top:10px">数据导入中，请稍候......</div>'});
        $.post('opp.my.php?manage_type='+get_query_string('manage_type')+'&m=import_hour&item=hour&opp_id='+opp_id, {content:$('#content').val(),vol_type:vol_type,opp_id:opp_id,job_id:job_id}, function(data) {
            try{
                C.alert.opacty_close();
                var ret=$.evalJSON(data);
                if(ret.code==0){
                    C.alert.alert({content:ret.msg});
                    $('#vols').html(data);
                    var h1='<table class="table1">';
                    var h2='<table class="table1 m10">';
                    h1+='<tr><th>状态</th><th>志愿者ID</th><th>项目ID</th><th>时长</th></tr>';
                    h2+='<tr><th>状态</th><th>志愿者ID</th><th>项目ID</th><th>时长</th></tr>';
                    for(var i=0;i<ret.data.length;i++){
                        var a=ret.data[i];
                        h1+='<tr>';
                        h1+='<td><font color=green>'+a.msg+'</font></td>';
                        h1+='<td>'+a.vol_id+'</td>';
                        h1+='<td>'+a.opp_id+'</td>';
                        h1+='<td>'+a.hour_num+'</td>';
                        h1+='</tr>';
                    }
                    for(var i=0;i<ret.failed.length;i++){
                        var a=ret.failed[i];
                        h2+='<tr>';
                        h2+='<td><font color=red>'+a.msg+'</font></td>';
                        h2+='<td>'+a.vol_id+'</td>';
                        h2+='<td>'+a.opp_id+'</td>';
                        h2+='<td>'+a.hour_num+'</td>';
                        h2+='</tr>';
                    }
                    h1+='</table>';
                    h2+='</table>';
                    $('#vols').html(h1+h2);
                }else{
                    C.alert.alert({content:ret.msg});
                }
            }catch(e){alert(e.message+data);}
        });
    }catch(e){alert(e.message+'\r\n'+data);}
}