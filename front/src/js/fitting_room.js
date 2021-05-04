function Photoes() {

}

// 监听上传个人照片的事件
Photoes.prototype.listenUploadPhotoesEvent = function () {
    var self = this;
    var uploadBtn = $("#upload-btn");
    uploadBtn.change(function () {
        var file = uploadBtn[0].files[0];
        var formData = new FormData();
        formData.append("file", file);

        msybajax.post({
            'url': '/upload/person/photo/',
            'data': formData,
            // 上传文件还需要上传以下两个参数，如果不上传这两个参数，文件就不能上传成功
            'processData': false, // 告诉Jquery这个文件就不需要再去处理了，因为它是一个文件不是一个普通的字符串
            'contentType': false, // 告诉它不要再去设置类型了，就用这个文件的类型就可以了
            'success': function (result) {
                if (result['code'] === 200) {
                    // var url = result['data']['img_url'];
                    window.messageBox.show("亲~您上传的个人照片已经上传成功~");
                    window.location.reload();
                }else {
                    window.messageBox.showError("不好意思亲~您的照片没有上传成功")
                }
            }
        });
    });
};

// 监听删除个人照片的事件
Photoes.prototype.listenDropPersonalPhotoEvent = function() {
    var self = this;
    var dropBtn = $(".drop-btn");
    dropBtn.click(function () {
        var currentBtn = $(this);
        var img = currentBtn.parent().siblings();
        var img_url = img.attr("data-name");
        msybajax.post({
            'url': '/drop/personal/photo/',
            'data': {
                'img_url': img_url,
            },
            'success': function (result) {
                if(result['code'] === 200) {
                    window.messageBox.showSuccess("删除照片成功~3秒后自动刷新哦~");
                    setTimeout(function () {
                        window.location.reload();
                    },3000);
                }
            }
        });
    });
};


// 监听提取人体3D模型的事件

// 监听保存模型的事件

// 监听删除模型的事件


// 监听使用该模型的事件

Photoes.prototype.run = function () {
    var self = this;
    self.listenUploadPhotoesEvent();
    self.listenDropPersonalPhotoEvent();
};

$(function () {
    var photoes = new Photoes();
    photoes.run();
});