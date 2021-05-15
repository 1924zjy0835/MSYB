// 商品详情
function ClothDetail() {

}

ClothDetail.prototype.listenClothDetailClickEvent = function () {
    var clothDetailBtn = $(".cloth-detail");

    clothDetailBtn.click(function () {
        msybajax.post({
            'url': '/detail/',
            'success': function (result) {
                if (result['code'] === 200) {

                } else {
                    console.log();
                    window.messageBox.showError(result['message']);
                }
            }
        });

    });
};

// 监听将服装加入储衣间的事件
ClothDetail.prototype.listenClosetClothEvent = function () {
    var self = this;
    var addCloset = $(".add-closet");

    addCloset.click(function () {
        var thumbnail = $(this).parent().attr('data-name');
        var title = $(this).attr('data-name');

        console.log(thumbnail);
        console.log(title);

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


ClothDetail.prototype.run = function () {
    var self = this;
    self.listenClothDetailClickEvent();
    self.listenClosetClothEvent();
};

$(function () {
    var clothdetail = new ClothDetail();
    clothdetail.run();
});