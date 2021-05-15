function RotateModel() {
    var self = this;
    this.index = 0;
    this.modelWidth = 240;
    this.modelfitting = $(".model-fitting");
    this.modelUl = $("#model-ul");
    this.liList = this.modelUl.children("li");
    this.modelCount = this.liList.length;
}

//运动函数
RotateModel.prototype.animate = function() {
    var self = this;
    self.modelUl.css({"left": -self.modelWidth * self.index});
    // var index = self.index;
    // if(index === 0){
    //     index = self.modelCount - 1;
    // }else if(index === self.modelCount){
    //     index = 0;
    // }else {
    //     index = self.index - 1;
    // }
};

// 人体模型的运动
RotateModel.prototype.loop = function () {
    var self = this;
    this.timer = setInterval(function () {
        // 动态获取模型的个数
        if (self.index >= self.modelCount) {
            self.modelUl.css({"left":0});
            self.index = 1;
        } else {
            self.index++;
        }
        self.animate()
    }, 2000);
};


// 动态获取人体模型图的个数
RotateModel.prototype.initModel = function () {
    var self = this;

    var firstModel = self.liList.eq(0).clone();

    // 将复制的第一张和最后一张banner添加至轮播图的最后和最前面
    self.modelUl.append(firstModel);

    self.modelUl.css({"width": (self.modelCount + 1) * self.modelWidth});
};

// 监听模型旋转事件
// RotateModel.prototype.listenRotateModelEvent = function() {
//     var self = this;
//     var fittingModel = $("#fitting-model");
//
//     fittingModel.click(function () {
//         if (self.index === self.modelCount + 1) {
//             self.modelUl.css({"left": -self.modelWidth});
//             self.index = 2;
//         } else {
//             self.index++;
//         }
//         self.animate();
//         console.log("running..............");
//         console.log(self.modelCount);
//     });
// };

RotateModel.prototype.listenRun = function () {
    var self = this;
    // 设置一个定时器

    setInterval(function () {
        // 如果轮播的次数已经大于模型的个数了就设置index为0
        if (self.index >= self.modelCount) {
            self.index = 0;
        // 否者的话，就置index每次加1
        } else {
            self.index++;
        }
        self.modelUl.css({"left": -self.modelWidth*self.index});
    }, 1000);
};

RotateModel.prototype.run = function () {
    var self = this;
    self.loop();
    self.initModel();
    self.listenRun();
    // self.listenRotateModelEvent();
};

// 在网页加载完毕之后，人体模型图就可以运动起来了
$(function () {
    var rotateModel = new RotateModel();
    rotateModel.run();
});