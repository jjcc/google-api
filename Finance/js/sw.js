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
	if(img.includes("/etf"))
	{
		var sloc = img.indexOf("/etf");
		var fileName = img.substr(sloc + 1);
		var components = fileName.split("_")
		console.log(fileName);
		var new_file = [components[0],components[1],"111.png"].join("_")
		img = img.replace(fileName,new_file);
	}
	$("img#currentimg")[0].src = img;
	
	var comp;
	var file = codeid + "_componentsx.json";
	$.getJSON("compj/" + file, function(json) {
		$("#swlist").children().remove();
		comp = json;
		names = comp.stock_name;
		codes = comp.stock_code;
		changepcts = comp.changepercent;
		for (i in names) { 
			//console.log("name:" + names[i]);
			var name = names[i];
			var code = codes[i];
			var changepct = changepcts[i];
			var code_link = "0." +  code;
			if (code.startsWith('6'))
				code_link = "1." + code;
			var whole_link = external_prefix + code_link;
			var bgcolor = lut(changepct);
			$("#swlist").append("<div class='ml-2'><a href='" + whole_link +
				"' target='_blank' style='background-color:"+ bgcolor + ";color:black'>" + name +"</a></div>");
		}
		console.log(lut(3.5));
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


function lut(  pctg ){
	var list = {9:"#FE0000",8:"#FF1919",7:"#FF3333",6:"#FF4D4D",
		5:"#FF6666",4:"#FF7F7F",3:"#FF9999",2:"#FFB2B2",
		1:"#FFCCCC",0:"#FFE5E5"};
	var list_g = {9:"#00FE00",8:"#19FF19",7:"#33FF33",6:"#4DFF4D",
		5:"#66FF66", 4:"#7FFF7F",3:"#99FF99",2:"#B2FFB2",
		1:"#CCFFCC",0:"#E5FFE5"};
	if(pctg>10)
		pctg = 9.99;
	var grade =  Math.floor( pctg + 0.5 );
	if (pctg >= 0) {
		return list[grade];
	}
	else {
		//var grade =  Math.floor( pctg - 0.5 );
		return list_g[grade];
	}
}
