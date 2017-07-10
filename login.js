// Username = "scsfire"
// EncryptedPassword = r"VsNl91lWRJpjkVCTVL4j/pa2w1Ij+U0JqNHIoWCYiGZy5+246J+1UDIs+aplYoH4DiHVfk+jkzGDijqc6ZLsb8mhrjWOO/CdZ7tD5rn5+Wd6yFgXnRoiaZGAiaAxiPONZuVce11IyOyISchMapiV8b4G8GyREbEg+pcRuhz5Y3Q=")
function login(Username = "", EncryptedPassword = "") {
    var LoginURL = 'http://www.bv2008.cn/app/user/login.php?m=login'
    $.post(LoginURL, {uname: Username, upass: EncryptedPassword}, function(RawLoginResponse) {
        // data = {"code":0,"msg":"登录成功","referer":"http://www.bv2008.cn/app/opp/list.php","id":"uname"}
        var LoginResponseJSON = $.evalJSON(RawLoginResponse);
        if (LoginResponseJSON.code == 0) {
            console.log("Login as " + LoginResponseJSON.id + " : " + LoginResponseJSON.msg);
            return 1;
        } else {
            console.log("Failed to login: " + LoginResponseJSON.msg);
            return 0;
        }
    });
}
