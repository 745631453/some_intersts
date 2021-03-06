function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var imageCodeId = "";

function generateUUID() {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

function generateImageCode() {
}

// function sendSMSCode() {
//     $(".phonecode-a").removeAttr("onclick");
//     var mobile = $("#mobile").val();
//     if (!mobile) {
//         $("#mobile-err span").html("请填写正确的手机号！");
//         $("#mobile-err").show();
//         $(".phonecode-a").attr("onclick", "sendSMSCode();");
//         return;
//     }
//     var imageCode = $("#imagecode").val();
//     if (!imageCode) {
//         $("#image-code-err span").html("请填写验证码！");
//         $("#image-code-err").show();
//         $(".phonecode-a").attr("onclick", "sendSMSCode();");
//         return;
//     }
//     $.get("/api/smscode", {mobile:mobile, code:imageCode, codeId:imageCodeId},
//         function(data){
//             if (0 != data.errno) {
//                 $("#image-code-err span").html(data.errmsg);
//                 $("#image-code-err").show();
//                 if (2 == data.errno || 3 == data.errno) {
//                     generateImageCode();
//                 }
//                 $(".phonecode-a").attr("onclick", "sendSMSCode();");
//             }
//             else {
//                 var $time = $(".phonecode-a");
//                 var duration = 60;
//                 var intervalid = setInterval(function(){
//                     $time.html(duration + "秒");
//                     if(duration === 1){
//                         clearInterval(intervalid);
//                         $time.html('获取验证码');
//                         $(".phonecode-a").attr("onclick", "sendSMSCode();");
//                     }
//                     duration = duration - 1;
//                 }, 1000, 60);
//             }
//     }, 'json');
// }

$(document).ready(function () {
        $(".form-register").submit(function () {

            mobile = $("#mobile").val();
            passwd = $("#password").val();
            passwd2 = $("#password2").val();

            $.ajax({
                url: '/user/register/',
                type: 'POST',
                dataType: 'json',
                data: {'mobile': mobile, 'password': passwd, 'password2': passwd2},
                success: function (date) {
                    if (date.code == '200') {
                        location.href = "/user/login/";
                    }
                },
                error: function (date) {
                    alert(date)
                }

            })
        });
        return false;
})