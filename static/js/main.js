$("#tet").click(function(){
  var html = '';
  $.post("/testAjax",
  {
    building: $("#buildingSelect").val(),
    mac: $("#macinput").val()
  },
  function(data){
	  //console.log(data.result.length)
	  var i = 0
	  for (jsf in data.result) {
		i = i + 1 
        html += '<li><a href="">'+i+'</a> [<span>'+data.result[i]+'</span>]</li>';
      }
    $("#result").html(html);
  });
});
