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
	var url="../cgi-bin/register.py";

	var f = document.form1;
    var name = f.name.value;
    var email   = f.email.value;
    var password   = f.password.value;

	var data = "name=" + name + "&email=" + email + "&password=" + password;

	$.ajax({
		url: url,
		type: "POST",//方法类型
		dataType: "html",//预期服务器返回的数据类型
		// data:{
		// 	'name': name,
		// 	'email': email,
		// 	'password': password
		// },
		data: data,
		success: function (result) {
			if(result.trim().toLowerCase() == "false"){
				alert("注册失败！已经存在该邮箱用户");
			}
			else {
				alert("注册成功，快去登录吧！");
			}
		},
		error : function() {
			alert("异常！");
		}
	});
}

function login() {
	var url="../cgi-bin/login.py";

	var f = document.form2;
    var email   = f.email.value;
    var password   = f.password.value;

	var data = "&email=" + email + "&password=" + password;

	//const getCookie = (name) => document.cookie.match(`[;\s+]?${name}=([^;]*)`)?.pop();

	$.ajax({
		url: url,
		type: "POST",//方法类型
		dataType: "html",//预期服务器返回的数据类型
		data: data,
		success: function (result) {
			if(result.trim().toLowerCase() == "true"){
				//alert(result)
				alert("登录成功！点击确定进入个人主页...");
				//这里href跳转到个人主页，获取信息填充，名字，头像
				// ajax内如何跳转页面，并把数据传过去
				// "b.html?name="+name+"&age="+age;
				// window.location.href = "../user/index.html?email=" + "1098668564@qq.com";

				//document.cookie="email="+email;
				window.location.href = "../user/index.html?" + btoa(encodeURIComponent("email=" + email));

			}
			else {
				// 这里要判断用户不存在或者密码错误
				if (result.trim() == "NOT_EXIST") {
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


