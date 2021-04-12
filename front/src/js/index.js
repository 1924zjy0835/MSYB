// 函数Banner()用来定义banner的属性
function Banner() {
    this.index = 1;
    this.bannerWidth = 1300;
    this.bannerGroup = $("#banner-group");
    this.pageControl = $(".page-control");
    this.leftArrow = $(".left-arrow");
    this.rightArrow = $(".right-arrow");
    this.bannerUl = $("#banner-ul");
    this.liList = this.bannerUl.children("li");
    this.bannerCount = this.liList.length;
    this.headerList = $(".nav");
    this.listTab = $(".list-tab");
}

//运动函数
Banner.prototype.animate = function() {
    var self = this;
    self.bannerUl.animate({"left": -self.bannerWidth * self.index}, 500);
    var index = self.index;
    if(index === 0){
        index = self.bannerCount - 1;
    }else if(index === self.bannerCount + 1 ){
        index = 0;
    }else {
        index = self.index - 1;
    }
    // 但是每次点击小点点的时候，小点点会被选中，而其他的兄弟节点的选中状态就会被移除掉；
    self.pageControl.children("li").eq(index).addClass("active").siblings().removeClass("active");
};

// 监听箭头的点击事件
Banner.prototype.ListenArrowClick = function () {
    var self = this;
    self.leftArrow.click(function () {
        //这里可以是会用三个等号也可以使用两个等号
        if (self.index === 0) {
            self.bannerUl.css({"left": -self.bannerWidth * self.bannerCount});
            self.index = self.bannerCount - 1;
        } else {
            self.index--;
        }
        self.animate();
        // 但是这里就不用再使用每个图片的停留时间就是2000毫秒了，该函数没有这个功能
    });

    self.rightArrow.click(function () {
        if (self.index === self.bannerCount + 1) {
            self.bannerUl.css({"left": -self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate();
    });
};

// 监听箭头是否展示
Banner.prototype.listenArrowShow = function (isShow) {
    var self = this;
    if (isShow) {
        self.leftArrow.show();
        self.rightArrow.show();
    } else {
        self.leftArrow.hide();
        self.rightArrow.hide();
    }
};

// 鼠标控制轮播图的轮播
Banner.prototype.listenBannerHover = function () {
    var self = this;
    self.bannerGroup.hover(function () {
        // 第一个函数用来表示鼠标移动到轮播图上面的时候的动作
        clearInterval(self.timer);
        self.listenArrowShow(true);
    }, function () {
        // 第二个函数用来表示鼠标从轮播图上一下来的时候的动作
        self.loop();
        self.listenArrowShow(false);
    });
};

// 轮播图的轮播
Banner.prototype.loop = function () {
    var self = this;
    this.timer = setInterval(function () {
        // 动态获取轮播图的个数
        if (self.index >= self.bannerCount + 1) {
            self.bannerUl.css({"left":-self.bannerWidth});
            self.index = 2;
        } else {
            self.index++;
        }
        self.animate()
    }, 2000);
};

// 动态生成小点点
Banner.prototype.AddPageControl = function () {
    var self = this;
    for (var i = 0; i < self.bannerCount; i++) {
        // 创建一个li标签
        var circle = $("<li></li>");
        self.pageControl.append(circle);
        // 此处只能用三个等号，判断是否相等
        if (i === 0) {
            circle.addClass("active");
        }
    }
    self.pageControl.css({"width":self.bannerCount*15+self.bannerCount*24+self.bannerCount*2});
};

// 监听小点点被点击的事件
Banner.prototype.listenPageControl = function() {
      var self = this;
      // each()函数中可以传递两个参数，一个就是当前的索引，另一个就是当前的这个小点点本身
    // 此处的index为传递进来的点击的小点点对应的index
      self.pageControl.children("li").each(function (index,obj) {
          // 首先将当前的这个对象包装成jquery对象,就是当前的这个小点点
          $(obj).click(function () {
              self.index = index + 1;
              self.animate();
              // $(obj).addClass("active").siblings().removeClass("active")
          });
      });
};

// 动态获取轮播图的个数
Banner.prototype.initBanner = function () {
    var self = this;

    var firstBanner = self.liList.eq(0).clone();
    var lastBanner = self.liList.eq(self.bannerCount - 1).clone();

    // 将复制的第一张和最后一张banner添加至轮播图的最后和最前面
    self.bannerUl.append(firstBanner);
    self.bannerUl.prepend(lastBanner);

    self.bannerUl.css({"width": (self.bannerCount + 2) * self.bannerWidth, "left": -self.bannerWidth});
};

// 监听导航栏一选项的选中状态
Banner.prototype.listenHeaderClick = function() {
    var self = this;
    self.headerList.children("li").each(function (index, obj) {
        $(obj).click(function () {
            $(obj).addClass("active").siblings().removeClass("active");
        }) ;
    });
};

// 监听导航栏二选项的选中状态
Banner.prototype.listenListClick = function() {
    var self = this;
    self.listTab.children("li").each(function (index, obj) {
        $(obj).click(function () {
            $(obj).addClass("active").siblings().removeClass("active");
        });
    });
};

// 定义Banner对象的run方法，如果想要轮播图动起来的话，就可以调用banner()方法
Banner.prototype.run = function () {
    this.loop();
    this.listenBannerHover();
    this.ListenArrowClick();
    this.AddPageControl();
    this.initBanner();
    this.listenPageControl();
    this.listenHeaderClick();
    this.listenListClick();
};

// 但是，轮播图动起来之前的，就需要将网页中所有元素加载完毕之后方可运动
$(function () {
    var banner = new Banner();
    banner.run();
});

