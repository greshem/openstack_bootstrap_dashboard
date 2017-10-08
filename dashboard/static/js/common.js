Number.prototype.formatMoney = function(places, symbol, thousand, decimal) {
	places = !isNaN(places = Math.abs(places)) ? places : 2;
	symbol = symbol !== undefined ? symbol : "￥";
	thousand = thousand || ",";
	decimal = decimal || ".";
	var number = this, negative = number < 0 ? "-" : "", i = parseInt(
			number = Math.abs(+number || 0).toFixed(places), 10)
			+ "", j = (j = i.length) > 3 ? j % 3 : 0;
	return symbol
			+ negative
			+ (j ? i.substr(0, j) + thousand : "")
			+ i.substr(j).replace(/(\d{3})(?=\d)/g, "$1" + thousand)
			+ (places ? decimal + Math.abs(number - i).toFixed(places).slice(2)
					: "");
};

function money_formatter(value) {
	return Number(value).formatMoney(4)
}
String.prototype.startwith=function(str){     
  var reg=new RegExp("^"+str);     
  return reg.test(this);        
}  

String.prototype.endwith=function(str){     
  var reg=new RegExp(str+"$");     
  return reg.test(this);        
}
String.prototype.contain=function(str){     
	  var reg=new RegExp(str);     
	  return reg.test(this);        
	}
constant = {
	'account_type' : {
		'normal' : '普通账户',
		'credit' : '信用账户'
	},
	'resource_type' : {
		'instance' : '云服务器(CPU,内存)',
		'ip' : '浮动IP',
		'router' : '路由器',
		'disk' : '云硬盘',
		'bandwidth' : '带宽',
		'snapshot' : '快照',
		'vpn' : 'VPN',
		'cdn' : 'CDN',
		'cpu':'CPU',
		'memory':'内存',
		'cdnflow' : 'CDN',
		'cdnbandwidth' : 'CDN',
		'tunnel' : '通道',
	},
	'payment_type' : {
		'gift' : '赠送',
		'recharge' : '充值'
	},
	'discount_item' : [ 'cpu', 'memory', 'ip', 'bandwidth', 'router', 'disk',
			'snapshot', 'vpn', 'cdn' ]
}

function type_formatter(value) {
	return constant.account_type[value]
}

function getRegionList() {
	values = $.ajax({
		url : constant_root_url+'/center/common/regionlist',
		async : false
	})
	return eval(values.responseText)
}

/**
 * 限制输入框只能输入数字(JQuery插件)
 * 
 * 
 * @example $("#amount").numeral()
 * 
 * @example $("#amount").numeral(4) or $("#amount").numeral({'scale': 4})
 * 
 * @example $(".x-amount").numeral()
 */
$.fn.numeral = function() {
	var args = arguments;
	var json = typeof (args[0]) == "object";
	var scale = json ? args[0].scale : args[1];
	scale = scale || 0;
	var positions = json ? args[0].positions : args[0];
	positions = positions || 1;
	$(this).css("ime-mode", "disabled");
	var keys = new Array(8, 9, 35, 36, 37, 38, 39, 40, 46);
	this.bind("keydown", function(e) {
		e = window.event || e;
		var code = e.which || e.keyCode;
		if (e.shiftKey) {
			return false;
		}
		var idx = Array.indexOf(keys, code);
		if (idx != -1) {
			return true;
		}
		var value = this.value;
		var id=this.id
		if (code == 190 || code == 110) {
			if (scale == 0 || value.indexOf(".") != -1) {
				return false;
			}
			return true;

		} else {
			if ((code >= 48 && code <= 57) || (code >= 96 && code <= 105)) {
				if (value.indexOf(".") == -1) {
					var reg = new RegExp("^[0-9]{0," + (positions - 1) + "}$");
				}
				if (scale > 0 && value.indexOf(".") != -1) {
					var reg = new RegExp("^[0-9]{0," + positions
							+ "}(\.[0-9]{0," + (scale-1) + "})?$");
				}
				var selText = getSelection();
				if (selText != value && !reg.test(value)) {
					var result= JudgeCursor(id,positions);
					if (result=="After")
						return false;
				}
				return true;
			}
			return false;
		}
	});
	this.bind("blur", function() {
		if (this.value.lastIndexOf(".") == (this.value.length - 1)) {
			this.value = this.value.substr(0, this.value.length - 1);
		} else if (isNaN(this.value)) {
			this.value = "";
		} else {
			var value = this.value;
			if (value.indexOf(".") != -1) {
				if (scale > 0) {
					var reg = new RegExp("^[0-9]{0," + positions
							+ "}(\.[0-9]{0," + scale + "})?$");
				}
			} else {
				var reg = new RegExp("^[0-9]{0," + positions + "}$");
			}
			if (!reg.test(value)) {
				this.value = format(value, scale);
			}
		}
		var reg1=new RegExp("^0{1,}([1-9]{1}[0-9]{0,}\.{0,1}[0-9]{0,})$")
		var reg2=new RegExp("^0{1,}(\.{0,1}[0-9]{0,})$")
		if (reg1.test(this.value)) {
			value = this.value.match(reg1)
			value1 = value[1]
			this.value = value1
		}
		if (reg2.test(this.value)){
			value=this.value.match(reg2)
			value1="0"+value[1]
			this.value=value1
		}
	});
	this.bind("paste", function() {
		var s = window.clipboardData.getData('text');
		if (!/\D/.test(s))
			;
		value = s.replace(/^0*/, '');
		return false;
	});
	this.bind("dragenter", function() {
		return false;
	});
	var format = function(value, scale) {
		return Math.round(value * Math.pow(10, scale)) / Math.pow(10, scale);
	}

	var getSelection = function() {
		if (window.getSelection) {
			return window.getSelection();
		}
		if (document.selection) {
			return document.selection.createRange().text;
		}
		return "";
	};

	var JudgeCursor = function(id,positions){
		var CursorPos = 0;
		var reg3=new RegExp("^[0-9]{"+positions+",}\..*$")
		temp=document.getElementById(id)
		if (document.selection) { // IE Support
			temp.focus();
			var Sel = document.selection.createRange();
			Sel.moveStart('character', -temp.value.length);
			CursorPos = Sel.text.length;
		}
		else if(temp.selectionStart || temp.selectionStart == '0') {
			 // Firefox support
			 CursorPos = temp.selectionStart;
		 }
		var commaPosition=temp.value.indexOf(".")
		if ((CursorPos<=commaPosition) && (commaPosition!=-1) && (!reg3.test(temp.value)) )
			return "Before"
		else
			return "After"
	};

	Array.indexOf = function(array, value) {
		for (var i = 0; i < array.length; i++) {
			if (value == array[i]) {
				return i;
			}
		}
		return -1;
	}
};

(function($, h, c) {
	var a = $([]), e = $.resize = $.extend($.resize, {}), i, k = "setTimeout", j = "resize", d = j
			+ "-special-event", b = "delay", f = "throttleWindow";
	e[b] = 250;
	e[f] = true;
	$.event.special[j] = {
		setup : function() {
			if (!e[f] && this[k]) {
				return false
			}
			var l = $(this);
			a = a.add(l);
			$.data(this, d, {
				w : l.width(),
				h : l.height()
			});
			if (a.length === 1) {
				g()
			}
		},
		teardown : function() {
			if (!e[f] && this[k]) {
				return false
			}
			var l = $(this);
			a = a.not(l);
			l.removeData(d);
			if (!a.length) {
				clearTimeout(i)
			}
		},
		add : function(l) {
			if (!e[f] && this[k]) {
				return false
			}
			var n;
			function m(s, o, p) {
				var q = $(this), r = $.data(this, d);
				r.w = o !== c ? o : q.width();
				r.h = p !== c ? p : q.height();
				n.apply(this, arguments)
			}
			if ($.isFunction(l)) {
				n = l;
				return m
			} else {
				n = l.handler;
				l.handler = m
			}
		}
	};
	function g() {
		i = h[k](function() {
			a.each(function() {
				var n = $(this), m = n.width(), l = n.height(), o = $.data(
						this, d);
				if (m !== o.w || l !== o.h) {
					n.trigger(j, [ o.w = m, o.h = l ])
				}
			});
			g()
		}, e[b])
	}
})(jQuery, this);