function Clothes() {

}

// 将文件上传至本地服务器
Clothes.prototype.listenUploadFileEvent = function() {
    // 获取的是一个集合
    var thumbnailBtn = $("#thumbnail-btn");
    thumbnailBtn.change(function () {
        // 因此我们需要找到满足条件的第一个文件
        // var file = .files(0);
        var file = thumbnailBtn[0].files[0];
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
                    var thumbnailForm = $("#thumbnail-form");
                    // 为输入框设置值
                    thumbnailForm.val(url);
                }
            }
        });
    });
};

// 将文件上传至七牛云存储
Clothes.prototype.listenUploadFileToQiniu = function() {
    var self = this;
    var thumbnailBtn = $("#thumbnail-btn");
    thumbnailBtn.change(function () {
        var file = this.files[0];
        msybajax.get({
            'url': '/cms/qntoken/',
            'success': function (result) {
                var token = result['data']['token'];
                var filestr = file.name.split(".");
                // 将上传的文件名按照.拆开，此时filestr就是一个列表，接下来我们根据列表的长度选择列表的最后一个就是文件的后缀了
                var key = (new Date()).getTime() + "." + filestr[filestr.length-1];
                var putExtra = {
                    fname: key,
                    params: {},
                    mimeType: ['image/png', 'image/jpeg', 'image/gif'],
                };
                var config = {
                    useCdnDomain: true,
                    retryCount: 3,
                    region: qiniu.region.z2
                    // 这是一个对象
                };
                // 就会根据设定的验证信息生成一个对象
                var observable = qiniu.upload(file, key, token, putExtra, config);
                // observable调用subscribe()函数用来设置上传过程的想听函数，有三个属性next、error、complete
                observable.subscribe({
                    // 在这里就需要去执行这个参数，后期他自己就会执行，将执行的结果放到这里
                    'next': self.handleUploadFileProcess,
                    'error': self.handleUploadFileError,
                    'complete': self.handleUploadFileComplete
                });
            }
        });
    });
};


// 监听文件上传至七牛云的上传过程的函数
Clothes.prototype.handleUploadFileProcess = function(response) {
    // 会返回一个response对象上面会有uploadinfo和total字段，
    // 而total字段上又会有loaded，total，percent三个属性
    var total = response.total;
    var percent = total.percent;
    // 将progress-group绑定在Clothes对象上面，这样就不用每次都使用jq对象从网页中去加载它了
    var progressGroup = $("#progress-group");
    progressGroup.show();
    var progressBar = $(".progress-bar");
    // percent.toFixed(0)代表的是不需要任何的小数点
    var percentText = percent.toFixed(0) + "%";
    progressBar.css({"width": percentText});
    progressBar.text(percentText);
};

// 监听文件上传至七牛云的上传的过程中出现错误的函数
Clothes.prototype.handleUploadFileError = function(error) {
    console.log(error.message);
        // 上传文件完成之后就将进度条隐藏
    var progressGroup = Clothes.progressGroup;
    progressGroup.hide();
};


// 监听文件上传至七牛云完成之后的函数
Clothes.prototype.handleUploadFileComplete = function(response) {
    // 默认的话会上传hash、key,上传文件完成之后就将进度条隐藏
    var progressGroup = Clothes.progressGroup;
    progressGroup.hide();

    // 并且需要将url放在input的输入框中
    var domain = "http://qs93q0n5y.hn-bkt.clouddn.com";
    var filename = response.key;
    var url = domain + "/" + filename;
    var thumbnailInput = $("input[name='thumbnail']");
    thumbnailInput.val(url);
};
// 初始化UEditor
Clothes.prototype.initUEditor = function() {
    window.ue = UE.getEditor("ueditor", {
        // 'initilFrameHeight': 400,
        // 使用ueditor上传图片至qiniu
        'serverUrl': '/ueditor/upload/'
    });
};

Clothes.prototype.listenPublishCloth = function(event) {
    var self = this;
    var submitBtn = $("#submit-btn");
    submitBtn.click(function () {
       var shop = $("select[name='shop']").val();
       var title = $("input[name='title']").val();
       var category = $("select[name='category']").val();
       var price = $("input[name='price']").val();
       var desc = $("input[name='desc']").val();
       var thumbnail = $("input[name='thumbnail']").val();
       // 这样后端得到的值会发生改变
       var content = window.ue.getContent();
       //  var clothContent = window.ue.getContent();
        // var content = base.encode(clothContent);

       msybajax.post({
           'url': '/cms/publish/cloth/',
           'data': {
               'shop': shop,
               'title': title,
               'category': category,
               'price': price,
               'desc': desc,
               'thumbnail': thumbnail,
               'content': content
           },
           'success': function (result) {
               if (result['code'] === 200) {
                   msybalert.alertSuccess('哇哦~您的服装上新成功了诶~', function () {
                       window.location.reload();
                   });
               }
           }
       });
    });
};


Clothes.prototype.run = function () {
    var self = this;
    // 不用将商品的主图上传至本地服务器
    // self.listenUploadFileEvent();
    // 只需要将商品的主图上传至七牛就可以了
    self.listenUploadFileToQiniu();
    // 将商品属性中的图片上传至七牛，不用上传至本地服务器
    self.initUEditor();
    self.listenPublishCloth();
};

$(function () {
    var clothes = new Clothes();
    clothes.run();

    Clothes.progressGroup = $("#progress-group");
});