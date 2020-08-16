var hidebyself = false;
var external_prefix = "http://quote.eastmoney.com/unify/r/";

function mo(elm){
	//if (hidebyself == true)
	//	return;
	codeid = elm.parentElement.id	
	var x = elm.parentElement.offsetLeft + 20;
	var y = elm.parentElement.offsetTop + 40;
	$('#popup').css({
		position: 'absolute',
		left: x,
		top: y,
	})
	$("#popup").show();
	img = elm.src;
	$("img#currentimg")[0].src = img;
	
	var comp;
	var file = codeid + "_components.json";
	$.getJSON("compj/" + file, function(json) {
		$("#swlist").children().remove();
		comp = json;
		names = comp.stock_name;
		codes = comp.stock_code;
		for (i in names) { 
			//console.log("name:" + names[i]);
			var name = names[i];
			var code = codes[i];
			var code_link = "0." +  code;
			if (code.startsWith('6'))
				code_link = "1." + code;
			var whole_link = external_prefix + code_link;
			$("#swlist").append("<div class='ml-2'><a href='"+ whole_link + "' target='_blank' >" + name +"</a></div>");
		}
		
	});
	console.log("mo called, code id:" + codeid);
	
	
}

function hide_popup(){
	$("#popup").hide();
	console.log("hide popup called");
}

function mout(){
	hidebyself = false; //reset
	console.log("mout called");
}

$("#popup").mouseleave(function() {
	hidebyself = true;
	$("#popup").hide();
	console.log("click self called");
});

$(".sector img").mouseover( function(){
	mo(this);
});
