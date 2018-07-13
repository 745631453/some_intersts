function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {

    $.get('/house/facility/', function (data) {
        var are_html_list = ''
        for (var i = 0; i < data.areas_list.length; i += 1) {
            var are_list = '<option value="' + data.areas_list[i].id + '">' + data.areas_list[i].name + '</option>'
            are_html_list += are_list
        }
        $('#area-id').html(are_html_list)
        var faciltys_html_list = ''
        for (var i = 0; i < data.areas_list.length; i += 1) {
            var faciltys_list = '<li>'
            faciltys_list += '<div class="checkbox">'
            faciltys_list += '<label>'
            faciltys_list += '<input type="checkbox" name="facility" ' +
                'value="' + data.faciltys_list[i].id + '">' + data.faciltys_list[i].name + '</label>'
            faciltys_list += '</div></li>'
            faciltys_html_list += faciltys_list
        }
        $('.house-facility-list').html(faciltys_html_list)
    })


    $("#form-house-info").submit(function () {
        $.post('/house/getnewhouse/', $(this).serialize(), function (data) {
            if (data.code == '200') {
                $('#form-house-info').hide()
                $('#form-house-image').show()
                $('#house-id').val(data.hous_id)
            }
        })
        return false;
    });

    $('#form-house-image').submit(function () {
        $(this).ajaxSubmit({
            url: '/house/newimage/',
            type: 'post',
            dataType: 'json',
            success: function (data) {
                if (data.code == '200') {
                    $('.house-image-cons').append('<img src="' + data.im_url + '">')
                }
            },
            error: function (data) {
                alert(data)
            }
        })
        return false;
    })
})