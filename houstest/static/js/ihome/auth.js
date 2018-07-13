function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$.get('/user/auths/', function (da) {
    if (da.code == '200') {
        $('#real-name').val(da.id_name)
        $('#id-card').val(da.id_card)
        $('.btn-success').hide()
    }
});

$('#form-auth').submit(function () {

    $.ajax({
        url: '/user/auths/',
        type: 'put',
        dataType: 'json',
        data: {
            id_name: $('#real-name').val(),
            id_card: $('#id-card').val()
        },
        success: function (da) {
            if (da.code == '200') {
                $('.btn-success').hide()
                $('.error-msg').hide()
            }
            else {
                $('.error-msg').show()
            }
        },
        error: function (a) {
            alert(a)
        }
    })
    return false;
})