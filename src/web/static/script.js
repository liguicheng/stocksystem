const signInBtn = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUp");
const container = document.querySelector(".container");

signInBtn.addEventListener("click", () => {
	container.classList.remove("right-panel-active");
});

signUpBtn.addEventListener("click", () => {
	container.classList.add("right-panel-active");
});


// $(function() {
//     $.ajax( {
//         url:"../cgi-bin/logout.py",
//         dataType:'html',
//         type: "post",
//         data: {},
//         success: function(data, textStatus){
//             //alert("清除cookie成功");
//         },
//
// 		error: function(){
// 			alert("清除cookie失败！");
//
// 		}
//     });
//
// });


function register() {
	var url="/register_into_db";

	var f = document.form1;
    var name = f.name.value;
    var email   = f.email.value;
    var password   = f.password.value;

	var data = "name=" + name + "&email=" + email + "&password=" + password;

	$.ajax({
		url: url,
		type: "POST",//方法类型
		dataType: "json",//预期服务器返回的数据类型
		data: data,
		success: function (result) {
			if(result['code'] ==="False"){
				alert("注册失败！已经存在该邮箱用户");
			} else {
				alert("注册成功，快去登录吧！");
			}
		},
		error : function() {
			alert("异常！");
		}
	});
}

function login() {
	var url="/login_into_db";

	var f = document.form2;
    var email   = f.email.value;
    var password   = f.password.value;

	var data = "&email=" + email + "&password=" + password;

	//const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();

	$.ajax({
		url: url,
		type: "POST",//方法类型
		dataType: "json",//预期服务器返回的数据类型
		data: data,
		success: function (result) {
			if(result['code'] === "True"){
				//alert(result)
				alert("登录成功！点击确定进入个人主页...");
				window.location.href = "/index";
				var Days = 3;
				var exp = new Date();
				exp.setTime(exp.getTime() + Days*24*60*60*1000);
				document.cookie="name="+result['name'] + ";expires=" + exp.toGMTString();;
				// alert(document.cookie);

			}
			else {
				// 这里要判断用户不存在或者密码错误
				if (result['code'] === "NOT_EXIST") {
					alert("用户未注册，请先注册");
				} else {
					alert("登录失败！密码错误");
				}

			}
		},
		error : function() {
			alert("异常！");
		}
	});

}


