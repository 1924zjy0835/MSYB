function AddModel() {

}

// 将模特上传至本地服务器
AddModel.prototype.listenUploadFileEvent = function() {
    // 获取的是一个集合
    var modelThumbnailBtn = $("#model-thumbnail-btn");
    modelThumbnailBtn.change(function () {
        // 因此我们需要找到满足条件的第一个文件
        // var file = .files(0);
        var file = modelThumbnailBtn[0].files[0];
        // 需要将文件存储在FormData中
        var formdata = new FormData();
        // 上传至本地服务器的接口是通过file
        formdata.append('file',file);
        msybajax.post({
            'url': '/cms/upload/file/',
            'data': formdata,
            // 上传文件还需要上传以下两个参数，如果不上传这两个参数，文件就不能上传成功
            'processData': false, // 告诉Jquery这个文件就不需要再去处理了，因为它是一个文件不是一个普通的字符串
            'contentType':false, // 告诉它不要再去设置类型了，就用这个文件的类型就可以了
            'success': function (result) {
                if (result['code'] === 200){
                    var url = result['data']['url'];
                    // 获取输入框
                    var thumbnailForm = $("#model-thumbnail-form");
                    // 为输入框设置值
                    thumbnailForm.val(url);
                }
            }
        });
    });
};


AddModel.prototype.listenPublishModel = function(event) {
    var self = this;
    var submitBtn = $("#submit-btn");
    submitBtn.click(function () {
       var thumbnail = $("input[name='thumbnail']").val();
       // 这样后端得到的值会发生改变

       msybajax.post({
           'url': '/cms/add/model/',
           'data': {
               'thumbnail': thumbnail
           },
           'success': function (result) {
               if (result['code'] === 200) {
                   msybalert.alertSuccess('哇哦~您的模特上传成功了诶~', function () {
                       window.location.reload();
                   });
               }
           }
       });
    });
};


AddModel.prototype.run = function () {
    var self = this;
    self.listenUploadFileEvent();
    self.listenPublishModel();
};

$(function () {
    var addModel = new AddModel();
    addModel.run();
});