$("#tet").click(function(){
  var html = '';
  $("#search").html('查询中');
  $("#notify").html('实时查询时间较长，请耐心等待，查询完毕上面文字会变为"查询结果"');
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
	$("#search").html('查询结果');
	 $("#notify").html('')
    $("#result").html(html);
	
  });
});
