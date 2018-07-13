function addshop(goods_id) {

    csrf = $('input[name="csrfmiddlewaretoken"]').val()
    $.ajax({
        url: '/ind/add/',
        type: 'post',
        headers: {'X-CSRFToken': csrf},
        data: {'goods_id': goods_id},
        dataType: 'json',
        success: function (msg) {
            $('#num' + goods_id).html(msg.c_num);
            $('#all123').html('总价' + msg.allnum)
        },
        error: function () {
            alert('失败');
        }
    })
}

function delshop(goods_id) {

    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ind/del/',
        type: 'post',
        data: {'goods_id': goods_id},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        success: function (msg) {
            $('#num' + goods_id).html(msg.c_num);
        },
        error: function () {
            alert('失败');
        }
    })
}

function changecheck(goods_id) {
    csrf = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        url: '/ind/changecheck/',
        type: 'post',
        data: {'goods_id': goods_id},
        headers: {'X-CSRFToken': csrf},
        dataType: 'json',
        success: function (msg) {
            if (msg.changecheck) {
                s = '<span onclick="changecheck(' + goods_id + ')">√</span>'
            }
            else {
                s = '<span onclick="changecheck(' + goods_id + ')">x</span>'
            }
            $('#nume' + goods_id).html(s)
        },
        error: function () {
            alert('选择失败')
        }
    })
}
