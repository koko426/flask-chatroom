var socket = io.connect('http://' + document.domain + ':' + location.port);

function Mybtn() {
    var user_id = document.getElementById('user_id').innerText;
    var msg = $("#textarea").val();
    if (msg == '') {
        return
    }
    socket.emit('send_message', {data: msg, 'send_id': user_id})
    //    清空输入栏
    $("#textarea").val('');
}

function myfunc(username) {
    socket.emit('newLogin', username, function (e) {
        window.location.href = '/'
    });
}


function logoutfunc(user_id) {
    socket.emit('newLogout', user_id, function (e) {
        window.location.href = '/login/'
    });
}

socket.on('newLogout_return', function (username) {
    var li = document.getElementsByClassName(username);
    for (var i = 0; i < li.length; i++) {
        li[i].remove();
    }
})

/*
socket.on('disconnect', function (msg) {
    document.getElementById('gbo').innerText = msg
})

socket.on('connect', function (msg) {
    console.log("111111111111111111111111")
    document.getElementById('gbo').innerText = msg
})
*/

socket.on('newLogin_return', function (data) {
    $(".chat03_content ul").append("<li id='" + data.username + "'>\n" +
        "                                    <label class=\"online\">\n" +
        "                                    </label>\n" +
        "                                    <a href=\"javascript:;\">\n" +
        "                                        <img src=\"static/img/user_head/" + data.imgname + "\"></a><a href=\"javascript:;\" class=\"chat03_name\">" + data.username + "</a>\n" +
        "                                </li>")
});

//消息回复
socket.on('recive_msg', function (res) {
    var g = res['msg'];

    var send_name = res['username']
    var web_name = $("#current_user").val();

    function h() {
        -1 != g.indexOf("*#emo_") && (g = g.replace("*#", "<img src='static/img/").replace("#*", ".gif'/>"), h())
    }

    h();
    var msgBox = $('.chat01_content');
    if (send_name == web_name) {
        msgBox.append("<div class=\"message clearfix\"><div class=\"wrap-text\">" + "<img class='wg' src='static/img/wg.png' style='width: 15px;height: 15px' alt='👑'>" +
            "<h5 class=\"clearfix\">" + res['username'] + "</h5><div class=\"goodman\" style='font-weight: bold;'>" + g + "</div></div><div class=\"wrap-ri\">" +
            "<div clsss=\"clearfix\"><span>" + res['create_time'] + "</span>" +
            "</div></div><div style=\"clear:both;\"></div></div>");
    } else {
        msgBox.append("<div class=\"message clearfix\"><div class=\"wrap-text\">" +
            "<h5 class=\"clearfix\">" + res['username'] + "</h5><div><span style=\"font-size: 16px\">" + g + "</span></div></div><div class=\"wrap-ri\">" +
            "<div clsss=\"clearfix\"><span>" + res['create_time'] + "</span>" +
            "</div></div><div style=\"clear:both;\"></div></div>");
    }


    $(".chat01_content").scrollTop(msgBox[0].scrollHeight + 220)
});
