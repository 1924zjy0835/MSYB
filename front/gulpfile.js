const gulp = require("gulp");
const cssnano = require("gulp-cssnano");
const uglify = require("gulp-uglify");
const rename = require("gulp-rename");
const cache = require("gulp-cache");
// const concat = require("gulp-concat");
const imagemin = require("gulp-imagemin");
const sass = require("gulp-sass");
//创建服务器
const bs = require("browser-sync").create();
const util = require("gulp-util");
const sourcemaps = require("gulp-sourcemaps");

// 初始化浏览器
gulp.task("bs", function () {
   bs.init({
       "server": {
           'baseDir': "./"
       }});
});

// 定义路径变量
const path = {
    "css": "./src/css/",
    "js": "./src/js/",
    "html": "./src/templates/",
    "images": "./src/images/",
    "css_dist": "./dist/css/",
    "js_dist": "./dist/js/",
    "images_dist": "./dist/images/"
};

// 定义一个处理css的任务
gulp.task("css", function () {
    gulp.src(path.css + "*.scss")
        .pipe(sass().on("error", sass.logError))
        .pipe(cssnano())
        .pipe(rename({"suffix": ".min"}))
        .pipe(gulp.dest(path.css_dist))
        // 自动刷新浏览器
        .pipe(bs.stream());
});

// 定义一个处理js的任务
gulp.task("js", function () {
    gulp.src(path.js + "*.js")
        .pipe(sourcemaps.init())
        .pipe(uglify())
        .pipe(rename({"suffix": ".min"}))
        .pipe(sourcemaps.write())
        .pipe(gulp.dest(path.js_dist))
        .pipe(bs.stream());
});

// 定义一个处理html的任务
gulp.task("html", function () {
    //检测到html源文件发生改变了，就重新加载html
    gulp.src(path.html + "*.html")
        .pipe(bs.stream())
});

// 定义一个处理图片的任务
gulp.task("images", function () {
    gulp.src(path.images + "*.*")
        .pipe(cache(imagemin()))
        .pipe(rename({"suffix": ".min"}))
        .pipe(gulp.dest(path.images_dist))
        .pipe(bs.stream());
});

// 定义一个监听任务
gulp.task("watch", function () {
    gulp.watch(path.css + "*.scss", ['css']);
    gulp.watch(path.js + "*.js", ["js"]);
    gulp.watch(path.html + "*.html", ["html"]);
    gulp.watch(path.images + "*.*", ["images"]);
});

// 定义一个默认任务
// gulp.task("default", ['bs', 'watch']);
gulp.task("default", ['watch']);