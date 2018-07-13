function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$("#form-avatar").submit(function() {

    $(this).ajaxSubmit({
        url: '/user/mprofile/',
        type: 'PUT',
        dataType: 'json',
        success: function (data) {
            if (data.code == '200') {
                $('.menu-content').show();
                $('#user-avatar').attr('src', data.url)
            }
        },
        error: function (data) {
            alert(data)
        }

    });
    return false;
});

$("#form-name").submit(function() {
    $('.error-msg').hide()

    $(this).ajaxSubmit({
        url: '/user/mprofile/',
        type: 'PUT',
        dataType: 'json',
        success: function (data) {
            if (data.code == '200') {
                $('.popup_con').show()
            }
            else{
                $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>用户名已存在，请重新设置')
                $('.error-msg').show()
            }
        },
        error: function (data) {
            alert(data)
        }

    });
    return false;
});