
function ClosetClothes() {

}

// 监听将服装加入储衣间的事件
ClosetClothes.prototype.listenClosetClothEvent = function () {
    var self = this;
    var addClosetBtn = $(".add-closet-btn");

    addClosetBtn.click(function () {
        var thumbnail = $(this).parent().parent().siblings().children().attr('data-name');
        var title = $(this).parent().siblings().attr('data-name');

        msybajax.post({
            'url': '/closet/room/',
            'data': {
                'title': title,
                'thumbnail': thumbnail,
            },
            'success': function (result) {
                if (result['code'] === 200){
                    setTimeout(function () {
                        window.messageBox.showSuccess("恭喜您~加入储衣间成功啦~");
                        window.location.reload();
                    },500);
                }
            }
        });
    });
};


// 监听选择这件衣服的事件


// 监听提取衣服模型
ClosetClothes.prototype.listenGrabCutEvent = function() {
    var self = this;


};

// 监听删除这件衣服
ClosetClothes.prototype.listenDropClosetClothEvent = function () {
    var self = this;
    var deleteClothBtn = $('.delete-cloth');
    deleteClothBtn.click(function () {
        var img_url = $(this).parent().parent().attr("data-name");
        console.log(img_url);

        msybajax.post({
            'url': '/drop/closet/cloth/',
            'data': {
                'img_url': img_url,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    window.messageBox.showSuccess("删除服装成功~3秒后自动刷新哦");
                    setTimeout(function () {
                        window.location.reload();
                    }, 3000);
                }
            }
        });
    });
};

ClosetClothes.prototype.run =  function() {
    var self = this;
    self.listenClosetClothEvent();
    self.listenDropClosetClothEvent();
    self.listenGrabCutEvent();
};

$(function () {
    var closetclothes = new ClosetClothes();
    closetclothes.run();
});