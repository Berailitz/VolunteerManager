function del_hours(hour_id){
            $.post('opp.my.php?manage_type='+get_query_string('manage_type')+'&m=del_hour&item=hour&opp_id='+$('input[name=opp_id]').val(), {hour_id:hour_id}, function(data) {
                try{
                    var ret=$.evalJSON(data);
                    if(ret.code==0){
                        console.log(hour_id);
                    }else{
                        C.alert.alert({content:ret.msg});
                    }
                }catch(e){alert(e.message+data);}
            });
}

uids = [27018758 ,27014374 ,27030001 ,27011563 ,27060126 ,27018802 ,27193722 ,5102666 ,31210199 ,27025394 ,27035012 ,27033707 ,27142227 ,27042661 ,27023251 ,27183649 ,27287112 ,27246613 ,27193819 ,27139981];
for (var i = uids.length - 1; i >= 0; i--) {
    del_hours(uids[i]);
}