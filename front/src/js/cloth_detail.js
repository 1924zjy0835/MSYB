// 商品详情
function ClothDetail() {

}

ClothDetail.prototype.listenClothDetailClickEvent = function () {
    var self = this;
    var clothDetailBtn = $(".cloth-detail");

    clothDetailBtn.click(function () {
        var pk = $(this).parent().parent().parent().parent().attr('data-id');
        msybajax.post({
            'url': '/detail/',
            'data': {
                'pk': pk,
            },
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

ClothDetail.prototype.run = function () {
    var self = this;
    self.listenClothDetailClickEvent();
};

$(function () {
    var clothdetail = new ClothDetail();
    clothdetail.run();
});