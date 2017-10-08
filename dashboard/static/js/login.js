var init={
	verifyCode:'',
	loadinfo:function(obj){

	},
	createCode:function(obj){
		code = "";   
	 	var codeLength = 4;//验证码的长度    
	 	var random = new Array(0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R',  
	     'S','T','U','V','W','X','Y','Z');//随机数  
	 	for(var i = 0; i < codeLength; i++) {//循环操作  
	    	var index = Math.floor(Math.random()*36);//取得随机数的索引（0~35）  
	        code += random[index];//根据索引取得随机数加到code上  
	    }  
	    init.verifyCode = code;//把code值赋给验证码  
	    $('#createcode').val(code);
	},
	login:function(){
		if($('#username').val()==''||$('#username').val()==undefined){
			$('.login-name').find('p').text('请输入用户名！').show();
			return false;
		}
		else{
			$('.login-name').find('p').hide();
		}
		if($('#password').val()==''||$('#password').val()==undefined){
			$('.login-psw').find('p').text('请输入密码！').show();
			return false;
		}
		else{
			$('.login-psw').find('p').hide();
		}
		if($('#verifycode').val()==''||$('#verifycode').val()==undefined){
			$('.login-verify').find('p').text('请输入验证码！').show();
			init.createCode();
			return false;
		}
		else if($('#verifycode').val().length !=4){
			$('.login-verify').find('p').text('请输入4位验证码！').show();
			init.createCode();
			return false;
		}
		else{
			if($('#verifycode').val().toUpperCase()!=init.verifyCode){
				$('.login-verify').find('p').text('验证码输入错误！').show();
				init.createCode();
				return false;
			}
			else{
				$('.login-verify').find('p').hide();
			}
			
		}
		$.ajax({
	    	url:"",
	    	type:"post",
	    	data:{'username':$('#username').val(),'password':$('#password').val()},
	    	dataType:"json"
	   	}).done(function(data){
	   		
		}).fail(function(data){
			
		}).always(function(){
				
		});

	}
}
$(function(){
	init.createCode();
	$('#createcode').click(function(){
		init.createCode();
	});
	$('.main-button').click(function(){
		init.login();
	})
	
});