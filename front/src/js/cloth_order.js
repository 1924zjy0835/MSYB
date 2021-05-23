// 商品详情
function ClothOrder() {

}

ClothOrder.prototype.listenZFEvent = function () {
    var buyBtn = $("#buy-btn");
    buyBtn.click(function (event) {
        event.preventDefault();
        var goodsname = $("input[name='goodsname']").val();
        var istype = $("input[name='istype']:checked").val();
        var notify = $("input[name='notify_url']").val();
        var orderid = $("input[name='orderid']").val();
        var price = $("input[name='price']").val();
        var return_url = $("input[name='return_url']").val();

        msybajax.post({
            'url': '/cloth/order/key/',
            'data': {
                'goodsname': goodsname,
                'istype': istype,
                'notify_url': notify,
                'orderid': orderid,
                'price': price,
                'return_url': return_url
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    var key = result['data']['key'];
                    var keyInput = $("input[name='key']");
                    keyInput.val(key);
                    $("#pay-form").submit();
                }
            }
        });

        msybajax.post({
            'url': '/notify/url/',
            'data': {
                'istype': istype,
                'orderid': orderid,

            },
        });
    });
};

ClothOrder.prototype.listenIsNotBuyEvent = function () {
    var self = this;
    var buyBtn = $("#buy-btn");

    buyBtn.click(function () {
        var div = $(this).parent();
        var buyer = div.attr("data-auth");
        var status = div.attr("data-id");

        setTimeout(function () {
            window.location.reload();
        }, 8000);

        setTimeout(function () {
            msybajax.post({
                'url': '/profile/view/',
                'data': {
                    'buyer': buyer,
                    'status': status
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        window.messageBox.showSuccess("恭喜您支付成功啦~");
                    }
                }
            });
        }, 10000);

    })
};


ClothOrder.prototype.run = function () {
    var self = this;
    self.listenZFEvent();
    // self.listenIsNotBuyEvent();
};

$(function () {
    var clothorder = new ClothOrder();
    clothorder.run();
});