function Category() {

}

Category.prototype.run = function () {
    var self = this;
    self.listenAddCategoryEvent();
    self.listenEditCategoryEvent();
    self.listenDeleteCategoryEvent();
};

// 监听添加分类功能
Category.prototype.listenAddCategoryEvent = function () {
    var self = this;
    var addCategoryBtn = $("#add-category-btn");
    addCategoryBtn.click(function () {
        // 显示一个弹出框
        msybalert.alertOneInput({
            "title": "添加服装分类",
            "placeholder": "请输入您要添加的服装分类",
            "confirmCallback": function (inputValue) {
                msybajax.post({
                    'url': '/cms/add/category/cloth/',
                    'data': {
                        'name': inputValue,
                    },
                    'success': function (result) {
                        if (result["code"] === 200){
                            console.log(result);
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

// 监听编辑分类功能
Category.prototype.listenEditCategoryEvent = function () {
    var self = this;
    var editBtn = $(".edit-btn");
    editBtn.click(function () {
        // currentBtn为当前的这个编辑按钮
        var currentBtn = $(this);
        // 通过当前按钮的父级的父级元素，获取我们要的tr，因为我们在tr上绑定了这个服装分类的pk和服装分类名
        var tr = currentBtn.parent().parent();
        var pk = tr.attr("data-id");
        var name = tr.attr("data-name");

        msybalert.alertOneInput({
            "title": "编辑服装分类",
            "placeholder": "请输入您要编辑的新分类名",
            "value": name,
            "confirmCallback" : function (inputValue) {
                msybajax.post({
                    "url": "/cms/edit/category/cloth/",
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
Category.prototype.listenDeleteCategoryEvent = function () {
    var self = this;
    var deleteBtn = $(".delete-btn");
    deleteBtn.click(function () {
        // currentBtn代表的是当前的删除按钮
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var pk = tr.attr("data-id");
        // var name = tr.attr("data-name")

        msybalert.alertConfirm({
           "title": "确定要删除该服装分类吗？",
            // 'value': name,
           "confirmCallback": function () {
               msybajax.post({
                   'url': '/cms/delete/category/cloth/',
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
    var category =  new Category();
    category.run();
});