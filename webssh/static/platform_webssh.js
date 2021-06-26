function get_term_size() {
    var init_width = 9;
    var init_height = 17;

    var windows_width = $(window).width();
    var windows_height = $(window).height();

    return {
        cols: Math.floor(windows_width / init_width),
        rows: Math.floor(windows_height / init_height),
    }
}

$(function() {
    var param = window.location.search;
    var pwd = new RegExp("(^|&)" + "password" + "=([^&]*)(&|$)");
    var plt_pwd = param.substr(1).match(pwd)[2];
    var name = new RegExp("(^|&)" + "username" + "=([^&]*)(&|$)");
    var plt_name = param.substr(1).match(name)[2];
    var host = new RegExp("(^|&)" + "hostname" + "=([^&]*)(&|$)");
    var plt_host = param.substr(1).match(host)[2];
    var cmd = new RegExp("(^|&)" + "cmd" + "=([^&]*)(&|$)");
    var plt_cmd = param.substr(1).match(cmd)[2];
    console.log(plt_cmd)
    if(plt_cmd!==''){
        var connect_info = 'host=' + plt_host + '&port=22&user=' + plt_name + '&auth=pwd&password=' + plt_pwd + '&cmd=' + plt_cmd;
    }else{
        var connect_info = 'host=' + plt_host + '&port=22&user=' + plt_name + '&auth=pwd&password=' + plt_pwd;
    }
    
    console.log(connect_info);
    var cols = get_term_size().cols;
    var rows = get_term_size().rows;
    var term = new Terminal(
        {
            cols: cols,
            rows: rows,
            useStyle: true,
            cursorBlink: true
        }
        ),
        protocol = (location.protocol === 'https:') ? 'wss://' : 'ws://',
        socketURL = protocol + location.hostname + ((location.port) ? (':' + location.port) : '') +
            '/webssh/?' + connect_info + '&width=' + cols + '&height=' + rows;

    var sock;
    sock = new WebSocket(socketURL);

    // 打开 websocket 连接, 打开 web 终端
    sock.addEventListener('open', function () {
        $('#form').addClass('hide');
        $('#django-webssh-terminal').removeClass('hide');
        term.open(document.getElementById('terminal'));
    });

    // 读取服务器端发送的数据并写入 web 终端
    sock.addEventListener('message', function (recv) {
        var data = JSON.parse(recv.data);
        var message = data.message;
        var status = data.status;
        if (status === 0) {
            term.write(message)
        } else {
            window.location.reload()
        }
    });

    /*
    * status 为 0 时, 将用户输入的数据通过 websocket 传递给后台, data 为传递的数据, 忽略 cols 和 rows 参数
    * status 为 1 时, resize pty ssh 终端大小, cols 为每行显示的最大字数, rows 为每列显示的最大字数, 忽略 data 参数
    */
    var message = {'status': 0, 'data': null, 'cols': null, 'rows': null};

    // 向服务器端发送数据
    term.onData(function (data) {
        message['status'] = 0;
        message['data'] = data;
        var send_data = JSON.stringify(message);
        sock.send(send_data)
    });

    // 监听浏览器窗口, 根据浏览器窗口大小修改终端大小
    $(window).resize(function () {
        var cols = get_term_size().cols;
        var rows = get_term_size().rows;
        message['status'] = 1;
        message['cols'] = cols;
        message['rows'] = rows;
        var send_data = JSON.stringify(message);
        sock.send(send_data);
        term.resize(cols, rows)
    })

})

