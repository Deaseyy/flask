

//弹出
function ErroAlert(e) {
    var index = layer.alert(e, { icon: 5, time: 2000, offset: 't', closeBtn: 0, title: '错误信息', btn: [], anim: 2, shade: 0 });
    layer.style(index, {
        color: '#777'
    }); 
}

//Ajax 错误返回处理
function AjaxErro(e) {
    if (e.Status == "Erro") {
        switch (e.Erro) {
            case "500":
                top.location.href = '/Erro/Erro500';
                break;
            case "100001":
                ErroAlert("错误 : 错误代码 '10001'");
                break;
            default:
                ErroAlert(e.Erro);
        }
    } else {
        layer.msg("未知错误！");
    }
}


//生成验证码
var code = "";
function createCode(e) {
    code = "";
    var codeLength = 4;
    var selectChar = new Array(1, 2, 3, 4, 5, 6, 7, 8, 9, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z');
    for (var i = 0; i < codeLength; i++) {
        var charIndex = Math.floor(Math.random() * 60);
        code += selectChar[charIndex];
    }
    if (code.length != codeLength) {
        createCode(e);
    }
	if(canGetCookie == 1){
    	setCookie(e, code, 60 * 60 * 60, '/');
	}else{
		return code;
	}
}

