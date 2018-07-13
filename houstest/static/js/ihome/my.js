function logout() {
    $.get("/user/logout/", function(data){
        if (data.code=='200') {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){
    $.get('/user/user/',function (data) {
        if(data.code == '200'){
            $('#user-name').html(data.user.name);
            $('#user-mobile').html(data.user.phone);
            $('#user-avatar').attr('src',data.user.avatar)
        }
    })

})