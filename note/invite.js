function MyInvite(ProjectID = 0, JobID = 0, VolunteerIDs = []){
    if(uid.length==0) {
        console.log("No volunteer specifed to be added.")
        return false;
    } else {
        $.post(
            'http://www.bv2008.cn/app/opp/opp.my.php?m=invite&item=recruit&opp_id=' + ProjectID + '&job_id=' + JobID,
            {stype:'local', uid: VolunteerIDs},
            function(RawResponse) {
                try{
                    var ResponseJSON = $.evalJSON(RawResponse);
                    console.log("Succeeded inviting @ " + VolunteerIDs + " " + ResponseJSON.msg)
                }
                catch(e){
                	console.log("Failed to invite @ " + VolunteerIDs + " " + e.message);}
            }
        );
    }
}
