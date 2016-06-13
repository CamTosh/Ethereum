function color_label() {


	$('.hashvalue').each(function(i, n) {

	   if($(n).text() >= 26000000) $('.hash').css('background-color', '#68b665');
	   else if($(n).text() >= 19000000) $('.hash').css('background-color', '#fdca41');
	   else $('.hash').css('background-color', '#db5959');

	});

	$('.gain').css('background-color', '#68b665');

	$('.fanvalue').each(function(i, n) {

	   if($(n).text() >= 100) $('.fan').css('background-color', '#db5959');
	   else if($(n).text() >= 70) $('.fan').css('background-color', '#fdca41');
	   else $('.fan').css('background-color', '#68b665');

	});


	$('.loadvalue').each(function(i, n) {

	   if($(n).text() >= 90) $('.load').css('background-color', '#68b665');
	   else if($(n).text() >= 80) $('.load').css('background-color', '#fdca41');
	   else $('.load').css('background-color', '#db5959');

	});

	
	$('.clockvalue').each(function(i, n) {

	   if($(n).text() >= 950) $('.clock').css('background-color', '#68b665');
	   else $('.clock').css('background-color', '#db5959');

	});


	$('.memvalue').each(function(i, n) {

	   if($(n).text() >= 1250) $('.memory').css('background-color', '#db5959');
	   else $('.memory').css('background-color', '#68b665');

	});


	$('.heatvalue').each(function(i, n) {

	   if($(n).text() > 90) $('.heat').css('background-color', '#db5959');
	   else if($(n).text() >= 80) $('.heat').css('background-color', '#fdca41');
	   else $('.heat').css('background-color', '#68b665');

	});		

	console.log("color set");
}
function repeatMe(){
	$.ajax({
		url: '', // Url de l'api
		dataType: 'json',
		cache: false,
		timeout: 1000,
		success: function(data) {

			//color_label();

		  	r = data;
		  	mem = r.CurrentMem / r.MaxMem * 100
		  	clock = r.CurrentClock / r.MaxClock * 100
			//$("uptime").text(r.Uptime);
		    $("#serv_name").text(r.Name);
		    $("#serv_ip").text(r.Ip);
		    $("#serv_fan").text(r.FanSpeed);
			$("#serv_load").text(r.Load);
			$("#serv_clock").text(clock.toFixed(2));
			$("#serv_mem").text(mem.toFixed(2));
			$("#serv_maxclock").text(r.MaxClock);
			$("#serv_maxmem").text(r.MaxMem);
			$("#serv_heat").text(r.Heat );
			/*
			$("hashvalue").text(r.Hash);
			s = r.Balance /1000000000000000000;
			$("gainvalue").text(s.toFixed(5));
			$("eurvalue").text(r.Euro );
			*/
		},

	});
}

setInterval(repeatMe, 2000);