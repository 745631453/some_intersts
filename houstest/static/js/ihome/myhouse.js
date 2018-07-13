$(document).ready(function () {
    $(".auth-warn").show();
    $("#houses-list").hide();
    $.get('/house/auth_myhouse/', function (data) {
        if (data.code == '200') {
            $("#houses-list").show();
            $('.auth-warn').hide();
            var house_list_html = '';
            for (var i = 0; i < data.house_list.length; i += 1) {
                var house_html = '<li>';
                house_html += '<a href="/house/detail/?id=' + data.house_list[i].id + '">';
                house_html += '<div class="house-title">';
                house_html += '<h3>房屋ID:' + data.house_list[i].id + ' —— ' + data.house_list[i].title + '</h3>'
                house_html += '</div>';
                house_html += '<div class="house-content"><img src="' + data.house_list[i].image + '">';
                house_html += '<div class="house-text"><ul><li>位于：' + data.house_list[i].area + '</li>' +
                    '<li>价格：￥' + data.house_list[i].price + '/晚</li>' +
                    '<li>发布时间：' + data.house_list[i].create_time + '</li>'
                house_html += '</ul></div></div></a>';
                house_html += '</li>';
                house_list_html += house_html
            }
            $('#houses-list').append(house_list_html)
        }
    })
})