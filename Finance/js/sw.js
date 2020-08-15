var hidebyself = false;
function mo(elm){
	//if (hidebyself == true)
	//	return;
	codeid = elm.parentElement.id	
	var x = elm.parentElement.offsetLeft + 60;
	var y = elm.parentElement.offsetTop + 80;
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
		for (i in names) { 
			//console.log("name:" + names[i]);
			var name = names[i];
			$("#swlist").append("<div class='ml-2'>" + name +"</div>");
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
