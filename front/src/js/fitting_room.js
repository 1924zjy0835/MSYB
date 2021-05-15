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
Photoes.prototype.listenExtractModelEvent = function() {
    var self = this;
    var extractBtn = $(".extract-btn");
    extractBtn.click(function () {
        var thumbnail = $(this).attr("data-name");
        // var srcInput = extractBtn.parent().siblings().attr("src");
        // 将当前上传的人物照片的位置更改为人体的三维模型照片
        $('#img_url').attr('src', thumbnail);
        // document.getElementById('img_url').src = "thumbnail";
        console.log(thumbnail);
    });
};

// 监听保存模型的事件，单击保存模型的时候，监听其点击事件，将其保存到数据库中
Photoes.prototype.listenSaveModelEvent = function() {
    var self = this;
    var thumbnail = $(".extract-btn").attr("data-name");

    var saveModelBtn = $(".save-btn");
    saveModelBtn.click(function () {
        msybajax.post({
        "url": "/people/model/",
        "data": {
            "thumbnail": thumbnail,
        },
        'success': function (result) {
            if (result['code'] === 200) {
                console.log(thumbnail);
                window.messageBox.showSuccess("哇哦~已经成功保存人体模型了哦~")
            }
        }
    });
    });
};
// 监听删除模型的事件
Photoes.prototype.listenDeleteModelEvent = function() {
    var self =this;
    var deleteModelBtn = $(".delete-btn");
    deleteModelBtn.click(function () {
        var thumbnail = $(this).attr("data-name");
        console.log(thumbnail);
        msybajax.post({
            'url': '/delete/model/',
            'data': {
                'thumbnail':thumbnail,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.showSuccess("恭喜您~人体模型删除成功了哦~")
                    setTimeout(function () {
                        window.location.reload();
                    }, 3000);
                }else{
                    window.messageBox.showError("不好意思~人体模型没有删除成功哦~")
                }
            }
        });
    });
};


// 监听使用该模型的事件

Photoes.prototype.run = function () {
    var self = this;
    self.listenUploadPhotoesEvent();
    self.listenDropPersonalPhotoEvent();
    self.listenExtractModelEvent();
    self.listenSaveModelEvent();
    self.listenDeleteModelEvent();
};

$(function () {
    var photoes = new Photoes();
    photoes.run();
});