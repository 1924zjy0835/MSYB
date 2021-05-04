/**
 * @Description: msybajax.js
 * @Author: 孤烟逐云zjy
 * @Date: 2021/4/22 10:09
 * @SoftWare: PyCharm
 * @CSDN: https://blog.csdn.net/zjy123078_zjy
 * @博客园: https://www.cnblogs.com/guyan-2020/
 */

function getcookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var msybajax = {
    'get': function (args) {
        args['method'] = 'get';
        this.ajax(args);
    },
    'post': function (args) {
        args['method'] = 'post';
        this._ajaxSetup();
        this.ajax(args);
    },
    'ajax': function (args) {
        var success = args['success'];
        // 重写post中的success
        args['success'] = function (result) {
            if (result['code'] === 200) {
                // 如果用户在使用ajax.post提交数据时写了success方法，就是用用户自定义的success
                if (success) {
                    // 直接将返回的结果传递给success
                    success(result);
                    // window.location.reload();
                }
            } else {
                // message可能是字典或者是字符串
                var messageObject = result['message'];
                // 如果是字符串的话就直接展示错误就可以
                if (typeof messageObject == 'string' || messageObject.constructor === String) {
                    window.messageBox.showError(messageObject)
                } else {
                    // {"password":['密码最大长度不能超过20为！','xxx'],"telephone":['xx','x']}
                    for (var key in messageObject) {
                        // messages为根据key取出的所有的value的列表
                        var messages = messageObject[key];
                        // message为列表中的第一个错误信息
                        var message = messages[0];
                        window.messageBox.showError(message);
                    }
                }
            }
            if (success) {
                success(result);
            }
        };
        args['fail'] = function (error) {
            console.log(error);
            window.messageBox.showError('服务器内部错误！');
        };
        $.ajax(args);
    },
    '_ajaxSetup':

        function () {
            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!/^(GET|HEAD|OPTIONS|TRACE)$/.test(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", getcookie('csrftoken'));
                    }
                }
            });
        }
};