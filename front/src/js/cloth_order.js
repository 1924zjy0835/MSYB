$(function () {
    var buyBtn = $("#buy-btn");
    buyBtn.click(function (event) {
        event.preventDefault();
        var goodsname = $("input[name='goodsname']").val();
        var istype = $("input[name='istype']:checked").val();
        var notify = $("input[name='notify_url']").val();
        var orderid = $("input[name='orderid']").val();
        var price = $("input[name='price']").val();
        var return_url = $("input[name='return_url']").val();

        console.log("=============");
        console.log(goodsname);
        console.log(istype);
        console.log(notify);
        console.log(orderid);
        console.log(price);
        console.log(return_url);

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
                'orderid': orderid
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    setTimeout(function () {
                        msybalert.alertSuccess("支付成功~");
                    },10000);

                    setTimeout(function () {
                        window.location.href="/clothes/profile.html";
                    },12000)
                }
                else {
                    setTimeout(function () {
                        msybalert.alertSuccess("支付成功~");
                    },10000);

                    setTimeout(function () {
                        window.location.href="/clothes/profile.html";
                    },12000)
                }
            }
        });
    });
});