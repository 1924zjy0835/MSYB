/**
 * @Description: example.js.js
 * @Author: 孤烟逐云zjy
 * @Date: 2021/4/12 14:49
 * @SoftWare: PyCharm
 * @CSDN: https://blog.csdn.net/zjy123078_zjy
 * @博客园: https://www.cnblogs.com/guyan-2020/
 */

// JS for content editable trick from Chris Coyier

var h1 = document.querySelector("h1");

h1.addEventListener("input", function() {
  this.setAttribute("data-heading", this.innerText);
});
