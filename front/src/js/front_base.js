//
function Sleep(time) {
    return new Promise((resolve => setTimeout(resolve,time)));
}


// 用来处理登录与注册页面
function Auth() {
    var self = this;
    self.maskWrapper = $(".mask-wrapper");
    self.ScrollWrapper = $(".scroll-wrapper");
    self.signinGroup = $(".signin-group");
    self.signupGroup = $(".signup-group");
}

// 定义监听登录，注册页面的显示事件
Auth.prototype.ShowEvent = function () {
    var self = this;
    self.maskWrapper.show();

    $(".close-btn").click(function () {
        $(".mask-wrapper").hide();
    });
};

// 定义监听登录，注册页面的隐藏事件
Auth.prototype.HideEvent = function () {
    var self = this;
    self.maskWrapper.hide();
};

// 监听登录注册按钮的点击事件
Auth.prototype.listenShowHideClickEvent = function () {
    var self = this;
    var signinBtn = $(".Signin-btn");
    var signupBtn = $(".Signup-btn");

    signinBtn.click(function () {
        self.ShowEvent();
        $(".scroll-wrapper").css({"left": 0}, 500);
    });

    signupBtn.click(function () {
        self.ShowEvent();
        $(".scroll-wrapper").css({"left": -400}, 500);
    });
};

// 监听登录注册页面的切换事件
Auth.prototype.listenSwitchEvent = function () {
    var self = this;
    var switch01Btn = $(".switch01-btn");
    var switch02Btn = $(".switch02-btn");
    switch01Btn.click(function () {
        self.ScrollWrapper.animate({"left": -400}, 500);
    });
    // swith02请登录，被点击之后就会将scroll-wrapper的left置为0；
    switch02Btn.click(function () {
        self.ScrollWrapper.animate({"left": 0}, 500);
    });
};

// 监听登录事件
Auth.prototype.listenSigninEvent = function () {
    var self = this;
    var telephoneInput = self.signinGroup.find("input[name='telephone']");
    var passwordInput = self.signinGroup.find("input[name='password']");
    var rememberInput = self.signinGroup.find("input[name='remember']");

    var signinSubmit = self.signinGroup.find(".submit-btn");
    signinSubmit.click(function () {
        var telephone = telephoneInput.val();
        var password = passwordInput.val();
        var remember = rememberInput.prop("checked");

        // 在Django中采用post请求提交数据，会做一层csrf校验，所以在使用ajaxpost提交数据的时候需要做一些手脚
        //在ajax中怎么解决csrf攻击的问题
        msybajax.post({
            'url': '/account/login/',
            'data': {
                'telephone': telephone,
                'password': password,
                'remember': remember ? 1 : 0,
            },
            'success': function (result) {
                //    result['code']=200 or 400; so category;
                if (result['code'] === 200) {
                    // 如果是200的话就关闭登录页面，并且刷新窗口
                    self.HideEvent();
                    window.location.reload();
                } else {
                    var messageObject = result['message'];
                    if (typeof messageObject == "string" || messageObject.constructor == String) {
                        window.messageBox.showError(messageObject);
                    } else {
                        for (var key in messageObject) {
                            var messages = messageObject[key];
                            var message = messages[0];
                            window.messageBox.showError(message);
                        }
                    }
                }
            },
            'fail': function (error) {
                console.log(error);
                // window.messageBox.showError(error);
            },
        });
    });
};

// 监听注册事件
Auth.prototype.listenSignupEvent = function () {
    var self = this;
    var signupSubmitBtn = self.signupGroup.find(".submit-btn");
    signupSubmitBtn.click(function () {
        var telephoneInput = self.signupGroup.find("input[name='telephone']");
        var usernameInput = self.signupGroup.find("input[name='username']");
        var passwordInput1 = self.signupGroup.find("input[name='password1']");
        var passwordInput2 = self.signupGroup.find("input[name='password2']");
        var img_captchaInput = self.signupGroup.find("input[name='img_captcha']");

        var telephone = telephoneInput.val();
        var username = usernameInput.val();
        var password1 = passwordInput1.val();
        var password2 = passwordInput2.val();
        var img_captcha = img_captchaInput.val();

        msybajax.post({
            'url': '/account/register/',
            'data': {
                'telephone': telephone,
                'username': username,
                'password1': password1,
                'password2': password2,
                'img_captcha': img_captcha
            },
            'success': function (result) {
                if (result['code'] === 200){
                    window.messageBox.showSuccess("恭喜您注册成功啦~2秒后会自动登录哦");
                    setTimeout(function () {
                       window.location.reload();
                    },3000);
                }
            }
        })
    });
};

// 监听图形验证码的切换事件
Auth.prototype.listenCaptchaClickEvent = function () {
    var imgCaptcha = $(".img_captcha");
    // var imgCaptcha = $(".img_captcha");
    imgCaptcha.click(function () {
        // Math.random()函数会产生一个随机的0-1的小数，就会重新请求一次url
        imgCaptcha.attr("src", "/account/img/captcha/" + "?random=" + Math.random())
    });
};


Auth.prototype.run = function () {
    // var self = this;
    this.listenShowHideClickEvent();
    this.listenSwitchEvent();
    this.listenSigninEvent();
    this.listenCaptchaClickEvent();
    this.listenSignupEvent();
};


// 用来处理导航条
function FrontBase() {
    var self = this;
    self.AuthBox = $(".auth-box");
    self.userMoreBox = $(".user-more-box");

}

FrontBase.prototype.listenAuthBoxHoverEvent = function () {
    var self = this;
    self.AuthBox.hover(function () {
        self.userMoreBox.show();
    }, function () {
        self.userMoreBox.hide();
    });
};

// 监听导航条函数的入口
FrontBase.prototype.run = function () {
    var self = this;
    self.listenAuthBoxHoverEvent();
};

$(function () {
    var auth = new Auth();
    auth.run();
});

$(function () {
    var frontBase = new FrontBase();
    frontBase.run();
});