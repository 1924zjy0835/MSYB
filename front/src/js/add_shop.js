function Shop() {

}

Shop.prototype.run = function () {
    var self = this;
    self.listenAddShopEvent();
    self.listenEditShopEvent();
    self.listenDeleteShopEvent();
};

// 监听添加分类功能
Shop.prototype.listenAddShopEvent = function () {
    var self = this;
    var addshopBtn = $("#add-shop-btn");
    addshopBtn.click(function () {
        // 显示一个弹出框
        msybalert.alertOneInput({
            "title": "请填写店铺信息",
            "placeholder": "请输入您要添加的店铺名",
            "confirmCallback": function (inputValue) {
                msybajax.post({
                    'url': '/cms/add/shop/',
                    'data': {
                        'name': inputValue,
                    },
                    'success': function (result) {
                        if (result["code"] === 200){
                            console.log(result);
                            window.location.reload();
                        }else {
                            msybalert.close();
                            console.log(result['message']);
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
};

// 监听编辑分类功能
Shop.prototype.listenEditShopEvent = function () {
    var self = this;
    var shopeditBtn = $(".shop-edit-btn");
    shopeditBtn.click(function () {
        // currentBtn为当前的这个编辑按钮
        var currentBtn = $(this);
        // 通过当前按钮的父级的父级元素，获取我们要的tr，因为我们在tr上绑定了这个服装分类的pk和服装分类名
        var tr = currentBtn.parent().parent();
        var pk = tr.attr("data-id");
        var name = tr.attr("data-name");

        msybalert.alertOneInput({
            "title": "编辑店铺名称",
            "placeholder": "请编辑您的新店铺名",
            "value": name,
            "confirmCallback" : function (inputValue) {
                msybajax.post({
                    "url": "/cms/edit/shop/",
                    "data": {
                        "pk": pk,
                        "name": inputValue
                    },
                    "success": function (result) {
                        if (result['code'] === 200) {
                            window.location.reload();
                        }else {
                            msybalert.close();
                            window.messageBox.showError(result['message']);
                        }
                    }
                });
            }
        });
    });
};

//监听删除分类功能
Shop.prototype.listenDeleteShopEvent = function () {
    var self = this;
    var shopdeleteBtn = $(".shop-delete-btn");
    shopdeleteBtn.click(function () {
        // currentBtn代表的是当前的删除按钮
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr("data-id");

        msybalert.alertConfirm({
           "title": "确定要删除该店铺吗？",
           "confirmCallback": function () {
               msybajax.post({
                   'url': '/cms/delete/shop/',
                   'data': {
                       'pk': pk,
                   },
                   'success': function (result) {
                       if (result['code'] === 200) {
                           window.location.reload();
                       }
                   },
               });
           },
        });
    });
};

$(function () {
    var shop =  new Shop();
    shop.run();
});