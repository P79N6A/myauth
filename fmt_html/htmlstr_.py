# -*- coding: utf-8 -*-
#!/usr/bin/env python


html_chart_simple = {'pie': u'''tooltip : {
        trigger: 'item',
        formatter: "{b} : {c} ({d}%)"
    },
    calculable : false,
    series : [
        { type:'pie',radius : '{wokofo_radius}',center: ['{wokofo_center_x}','{wokofo_center_y}'],
         data:[{wokofo_value_name}]
        }
    ]''', 'gauge': u'''
    series : [
        {
            type:'gauge',
            axisLine: {          
                lineStyle: {     
                    color: [[0.2, '#ff4500'],[0.8, '#48b'],[1, '#228b22']], 
                    width: 8
                }
            },
            detail : {formatter:'{value}%'},
            data:[{wokofo_value_name}]
        }
    ]
    '''}

# '家人','朋友'
# {name: '家人'},{name:'朋友'}
# {category:0, name: '乔布斯', value : 10},{category:1, name: '丽萨-乔布斯',value : 2}
# {source : 1, target : 0, weight : 1},{source : 2, target : 0, weight : 2}
html_chart_force = '''tooltip : {
        trigger: 'item',
        formatter: '{a} : {b}'
    },
    legend: {
        x: 'left',
        data:[%s]
    },
    series : [
        {
            type:'force',
            categories : [%s],
            itemStyle: {normal: {label: {show: true,textStyle: {color: '#800080'}},nodeStyle : { brushType : 'both',strokeColor : 'rgba(255,215,0,0.4)',lineWidth : 1}},              },
            minRadius : 15,
            maxRadius : 25,
            density : 0.05,
            attractiveness: 1.2,
            linkSymbol: 'arrow',
            draggable: true,
            nodes:[%s],
            links : [%s]
        }
    ]'''

html_chart_toolbox = {
    'normal': u'''toolbox: {
        show : true,
        feature : {dataView : {show: true, readOnly: true},        
            magicType : {show: true, type: ['line', 'bar']},           
            saveAsImage : {show: true}
        }
    },
    '''
    , 'simple': u'''toolbox: {
        show : true,
        feature : {dataView : {show: true, readOnly: true},
            saveAsImage : {show: true}
        }
    },
    '''
    , 'none': ''}

# html_ajax=u"""
#      function mainAjax() {
#    jQuery.ajax({
#      type: "Get", url: "view.html?report_action=ajax&report_ptname=%s&date=" + new Date().getTime(), dataType:"json",
#       success: function (json) {
#                         jQuery.each(json, function (i, obj) {
#                          jQuery("#"+obj.id).html(obj.value);
#                          jQuery("#titlesms").html((new Date()).format("yyyy-MM-dd hh:mm:ss"))
#               },
#       error:function(XMLResponse){
#        jQuery("#titlesms").html(XMLResponse.responseText);},
#               });
#        };
# Date.prototype.format = function (format) {
#            var o = {
#                "M+": this.getMonth() + 1, //month
#                "d+": this.getDate(),    //day
#                "h+": this.getHours(),   //hour
#                "m+": this.getMinutes(), //minute
#                "s+": this.getSeconds(), //second
#                "q+": Math.floor((this.getMonth() + 3) / 3), //quarter
#                "S": this.getMilliseconds() //millisecond
#            }
#            if (/(y+)/.test(format)) format = format.replace(RegExp.$1,
#              (this.getFullYear() + "").substr(4 - RegExp.$1.length));
#            for (var k in o) if (new RegExp("(" + k + ")").test(format))
#                format = format.replace(RegExp.$1,
#                  RegExp.$1.length == 1 ? o[k] :
#                    ("00" + o[k]).substr(("" + o[k]).length));
#            return format;
#        };
# setInterval("mainAjax()", %s);
# """

#

html_ajax = {"id": u"""  
      function mainAjax() {
    jQuery.ajax({type: "Get", url: "view.html?report_action=ajax&report_ptname=%s&date=" + new Date().getTime(), dataType:"json",
        success: function (json) {jQuery.each(json, function (i, obj) {jQuery("#"+obj.id).html(obj.value);});
        }             
        })
	  };
 setInterval("mainAjax();", %s);
 mainAjax();
""",
             "div": u"""  
      function mainAjax() {
    jQuery.ajax({type: "Get", url: "view.html?report_action=ajax&report_ptname=%s&date=" + new Date().getTime(), dataType:"json",
        success: function (json) {jQuery.each(json, function (i, obj) {	
        if(obj.id.indexOf("style") > 0 )
			{
                objid="#"+obj.id.replace("style","");
				$(objid).removeClass().addClass(obj.value); 
			}
            else if(obj.id.indexOf("value") > 0 )
			{   jQuery("#"+obj.id).html(obj.value); 	             
                //jQuery("#"+obj.id).value(obj.value); 			
			}
            else if(obj.id.indexOf("_chartline_") > 0 )
			{
				$("#"+obj.id).sparkline(obj.value.split(','),{
					type: "line",
					height:'95px',
					width:'120px',
                    chartRangeMin:0,
					lineColor :'rgba(0, 0, 0, 0.15)',
					fillColor  :'rgba(0, 0, 0, 0.15)'
					});		
			}
            else if(obj.id.indexOf("_chartbar_") > 0 )
			{
				$("#"+obj.id).sparkline(obj.value.split(','),{
					type: "bar",
					height:'95px',
					width:'120px',
                    chartRangeMin:0,
					barColor:'rgba(0, 0, 0, 0.15)'
					});		
			}
			else
			{
                jQuery("#"+obj.id).html(obj.value); 				
			}; });
        }             
        })
	  };
 setInterval("mainAjax();", %s);
""",
             "sparkline": u"""  
      function mainAjax() {
    jQuery.ajax({type: "Get", url: "view.html?report_action=ajax&report_ptname=%s&date=" + new Date().getTime(), dataType:"json",
        success: function (json) {jQuery.each(json, function (i, obj) {	if(obj.id.indexOf("_chartline_") > 0 )
			{
				$("#"+obj.id).sparkline(obj.value.split(','),{
					type: "line",
					height:'95px',
					width:'120px',
                    chartRangeMin:0,
					lineColor :'rgba(0, 0, 0, 0.15)',
					fillColor  :'rgba(0, 0, 0, 0.15)'
					});		
			}
            else if(obj.id.indexOf("_chartbar_") > 0 )
			{
				$("#"+obj.id).sparkline(obj.value.split(','),{
					type: "bar",
					height:'95px',
					width:'120px',
                    chartRangeMin:0,
					barColor:'rgba(0, 0, 0, 0.15)'
					});		
			}
			else
			{jQuery("#"+obj.id).html(obj.value); 				
			}; });
        }             
        })
	  };
 setInterval("mainAjax();", %s);
"""
             }

html_ajax_chart = u"""
     function mainJson{pagei}() {
     url="%s&pagei={pagei}&date=" + new Date().getTime();
        $.getScript(url);
    };
 setInterval("mainJson{pagei}()", %s);
"""

html_ajax_simple = """function mainAjax() {
  document.getElementById("sbutton").click();
  };setInterval("mainAjax()", %s);
    """

html_ajax_all = """
  function mainAjaxall() {
    url="%s&date=" + new Date().getTime();
    $.getScript(url);
    };setInterval("mainAjaxall()", %s);"""

html_js = {
    'js_serverlist': u'''<script type="text/javascript" src="/static/js/serverlist.js"></script>   ''',
    'js_clusterlist': u'''<script type="text/javascript" src="/static/js/cluster.js"></script><script type="text/javascript" src="/cluster.js"></script>   ''',
    'js_selectlist': u'''<script type="text/javascript" src="/static/js/cluster-short.js"></script>''',
    'js_codesql': u'''<link rel="stylesheet" href="/static/code/css/codemirror.css" /><script src="/static/code/js/codemirror.js"></script><script src="/static/code/js/sql.js"></script>''',

    'js_codexml': u'''<link rel="stylesheet" href="/static/code/css/codemirror.css" /><link rel="stylesheet" href="/static/code/css/codemirror-h.css" /><script src="/static/code/js/codemirror.js"></script><script src="/static/code/js/xml.js"></script>''',
    'js_datetimepicker': u'''  <script type="text/javascript" src="/static/js/date-time/jquery.datetimepicker.js"></script>  ''',
    'body_spark': ''' <script src="/static/js/jquery.knob.js" type="text/javascript"></script>
    <script src="/static/js/jquery.sparkline.min.js" type="text/javascript"></script>
    <script src="/static/js/boot_chart.js" type="text/javascript"></script>''',
    'js_head_d3': '''<script src="/static/js/d3.v3.min.js"></script>''',
    'js_head_d3zoom': '''<script src="/static/js/d3.js"></script><script src="/static/js/d3.layout.js"></script>'''
}
# <script>
#     var ie = navigator.appName == "Microsoft Internet Explorer" ? true : false;
#     function $(objID) {
#         return document.getElementById(objID);
#     }
# </script>


# y轴
html_chart_yalix = '''{type : 'value',name : '%s',axisLabel : {formatter: '{value} %s'}}'''

html_chart_theme = {
    'green': '''var green={color:['#408829','#68a54a','#a9cba2','#86b379','#397b29','#8abb6f','#759c6a','#bfd3b7'],title:{textStyle:{color:'#408829'}},dataRange:{color:['#1f610a','#97b58d']},toolbox:{color:['#408829','#408829','#408829','#408829']},tooltip:{backgroundColor:'rgba(0,0,0,0.5)',axisPointer:{type:'line',lineStyle:{color:'#408829',type:'dashed'},crossStyle:{color:'#408829'},shadowStyle:{color:'rgba(200,200,200,0.3)'}}},dataZoom:{dataBackgroundColor:'#eee',fillerColor:'rgba(64,136,41,0.2)',handleColor:'#408829'},grid:{borderWidth:0},categoryAxis:{axisLine:{lineStyle:{color:'#408829'}},splitLine:{lineStyle:{color:['#eee']}}},valueAxis:{axisLine:{lineStyle:{color:'#408829'}},splitArea:{show:true,areaStyle:{color:['rgba(250,250,250,0.1)','rgba(200,200,200,0.1)']}},splitLine:{lineStyle:{color:['#eee']}}},timeline:{lineStyle:{color:'#408829'},controlStyle:{normal:{color:'#408829'},emphasis:{color:'#408829'}}},k:{itemStyle:{normal:{color:'#68a54a',color0:'#a9cba2',lineStyle:{width:1,color:'#408829',color0:'#86b379'}}}},map:{itemStyle:{normal:{areaStyle:{color:'#ddd'},label:{textStyle:{color:'#c12e34'}}},emphasis:{areaStyle:{color:'#99d2dd'},label:{textStyle:{color:'#c12e34'}}}}},force:{itemStyle:{normal:{linkStyle:{strokeColor:'#408829'}}}},chord:{padding:4,itemStyle:{normal:{lineStyle:{width:1,color:'rgba(128, 128, 128, 0.5)'},chordStyle:{lineStyle:{width:1,color:'rgba(128, 128, 128, 0.5)'}}},emphasis:{lineStyle:{width:1,color:'rgba(128, 128, 128, 0.5)'},chordStyle:{lineStyle:{width:1,color:'rgba(128, 128, 128, 0.5)'}}}}},gauge:{startAngle:225,endAngle:-45,axisLine:{show:true,lineStyle:{color:[[0.2,'#86b379'],[0.8,'#68a54a'],[1,'#408829']],width:8}},axisTick:{splitNumber:10,length:12,lineStyle:{color:'auto'}},axisLabel:{textStyle:{color:'auto'}},splitLine:{length:18,lineStyle:{color:'auto'}},pointer:{length:'90%',color:'auto'},title:{textStyle:{color:'#333'}},detail:{textStyle:{color:'auto'}}},}'''}

# 预设的ITEM选项
html_chart_item_detail = {
    'markline': ''',markLine : {{data : [[{{name: 'base line', value: {0}, xAxis: -1, yAxis: {0} }},{{name: '', xAxis: {max_x}, yAxis: {0} }}]]}}'''
    , 'marklinesimple': u''',markLine : {{data : [{{type : '{0}', name : '{0}'}}]}}'''
    , 'itemstyle': ''',itemStyle: {{normal: {{color: '{0}',lineStyle: {{width: {1},type: '{2}'}}}}}}'''
    , 'stack': ''',itemStyle: {normal: {areaStyle: {type: 'default'}}}'''
    }

html_chart_dataZoom = '''    dataZoom : {
        show : true,
        realtime: true,
        start : %s,
        end : 100
    },'''

html_char_xbind = """xAxis : [
        {
            type : '%s',
            boundaryGap : true,
            axisTick: {onGap:false},
            splitLine: {show:false},
            data : axisData_%s
        }
    ],"""

d3_chart_js = {
    "tree_text": """
var width_{pagei} = {width},
height_{pagei} = {height};
var tree_{pagei} = d3.layout.tree()
	.size([height_{pagei}, width_{pagei}-200])
	.separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });
var diagonal_{pagei} = d3.svg.diagonal()
	.projection(function(d) { return [d.y, d.x]; });
var svg_{pagei} = d3.select("#d3_{pagei}").append("svg")
	.attr("width", width_{pagei})
	.attr("height", height_{pagei})
	.append("g")
	.attr("transform", "translate(40,0)");
d3.json("{url}", function(error, root) {
	var nodes = tree_{pagei}.nodes(root);
	var links = tree_{pagei}.links(nodes);	
	console.log(nodes);
	console.log(links);	
	var link = svg_{pagei}.selectAll(".d3_tree_link")
	  .data(links)
	  .enter()
	  .append("path")
	  .attr("class", "d3_tree_link")
	  .attr("d", diagonal_{pagei});	
	var node = svg_{pagei}.selectAll(".d3_tree_node")
	  .data(nodes)
	  .enter()
	  .append("g")
	  .attr("class", "d3_tree_node")
	  .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; })	
	node.append("circle")
	  .attr("r", 4.5);	
	node.append("text")
	  .attr("dx", function(d) { return d.children ? -8 : 8; })
	  .attr("dy", 3)
	  .style("text-anchor", function(d) { return d.children ? "end" : "start"; })
	  .text(function(d) { return d.name; });
	});
"""

    , "tree_rect": """
var width_{pagei} = {width},
height_{pagei} = {height};
    color = d3.scale.category20();

var svg_{pagei} = d3.select("#d3_{pagei}").append("svg")
			.attr("width", width_{pagei})
			.attr("height", height_{pagei})
			.append("g");

var partition_{pagei} = d3.layout.partition()
				.sort(null)
				.size([width_{pagei},height_{pagei}])
				.value(function(d) { return 1; });


d3.json("{url}", function(error, root) {

	if(error)
		console.log(error);
	console.log(root);

	var nodes = partition_{pagei}.nodes(root);
	var links = partition_{pagei}.nodes(nodes);

	console.log(nodes);

	var rects = svg_{pagei}.selectAll("g")
				  .data(nodes)
				  .enter().append("g");

	rects.append("rect")
		.attr("x", function(d) { return d.x; })  
		.attr("y", function(d) { return d.y; })  
		.attr("width", function(d) { return d.dx; })  
		.attr("height", function(d) { return d.dy; })  
		.style("stroke", "#fff")
		.style("fill", function(d) { return color((d.children ? d : d.parent).name); })
		.on("mouseover",function(d){
			d3.select(this)
				.style("fill","yellow");
		})
		.on("mouseout",function(d){
			d3.select(this)
				.transition()
				.duration(200)
				.style("fill", function(d) { 
					return color((d.children ? d : d.parent).name); 
				});
		});

	rects.append("text")  
		.attr("class","d3_tree_node_text")
		.attr("transform",function(d,i){
			return "translate(" + (d.x+20) + "," + (d.y+20) + ")";
		}) 
		.text(function(d,i) {
			return d.name;	
		});

});""", "tree_quad": """

var margin_{pagei} = {top: 0, right: 10, bottom: 10, left: 0},
    width_{pagei} = {width} - margin_{pagei}.left - margin_{pagei}.right,
    height_{pagei} = {height} - margin_{pagei}.top - margin_{pagei}.bottom;

var color_{pagei} = d3.scale.category20c();

var treemap_{pagei} = d3.layout.treemap()
    .size([width_{pagei}, height_{pagei}])
    .sticky(true)
    .value(function(d) { return d.size; });

var div_{pagei} = d3.select("#d3_{pagei}").append("div")
    .style("position", "relative")
    .style("width", (width_{pagei} + margin_{pagei}.left + margin_{pagei}.right) + "px")
    .style("height", (height_{pagei} + margin_{pagei}.top + margin_{pagei}.bottom) + "px")
    .style("left", margin_{pagei}.left + "px")
    .style("top", margin_{pagei}.top + "px");
d3.json("{url}", function(error, root) {
  var node = div_{pagei}.datum(root).selectAll(".d3_treemap_node")
      .data(treemap_{pagei}.nodes)
    .enter().append("div")
      .attr("class", "d3_treemap_node")
      .call(position)
      .style("background", function(d) { return d.children ? color_{pagei}(d.name) : null; })
      .text(function(d) { return d.children ? null : d.name; });
});

function position() {
  this.style("left", function(d) { return d.x + "px"; })
      .style("top", function(d) { return d.y + "px"; })
      .style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
      .style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; });
}

"""
    , "tree_quadzoom":
        """
        var w = {width} - 20,
            h = {height} - 20,
            x = d3.scale.linear().range([0, w]),
            y = d3.scale.linear().range([0, h]),
            color_{pagei} = d3.scale.category20c(),
            root,
            node;
        
        var treemap_{pagei} = d3.layout.treemap()
            .round(false)
            .size([w, h])
            .sticky(true)
            .value(function(d) { return d.size; });
        
        var svg = d3.select("#d3_{pagei}").append("div")
            .attr("class", "chart")
            .style("width", w + "px")
            .style("height", h + "px")
          .append("svg:svg")
            .attr("width", w)
            .attr("height", h)
          .append("svg:g")
            .attr("transform", "translate(.5,.5)");
        d3.json("{url}", function(data) {
          node = root = data;
        
          var nodes = treemap_{pagei}.nodes(root)
              .filter(function(d) { return !d.children; });
        
          var cell = svg.selectAll("g")
              .data(nodes)
            .enter().append("svg:g")
              .attr("class", "cell")
              .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
              .on("click", function(d) { return zoom(node == d.parent ? root : d.parent); });
        
          cell.append("svg:rect")
              .attr("width", function(d) { return d.dx - 1; })
              .attr("height", function(d) { return d.dy - 1; })
              .style("fill", function(d) { return color_{pagei}(d.parent.name); });
        
          cell.append("svg:text")
              .attr("x", function(d) { return d.dx / 2; })
              .attr("y", function(d) { return d.dy / 2; })
              .attr("dy", ".35em")
              .attr("text-anchor", "middle")
              .text(function(d) { return d.name; })
              .style("opacity", function(d) { d.w = this.getComputedTextLength(); return d.dx > d.w ? 1 : 0; });
        
          d3.select(window).on("click", function() { zoom(root); });
        
        
        });
        
        function size(d) {
          return d.size;
        }
        
        function count(d) {
          return 1;
        }
        
        function zoom(d) {
          var kx = w / d.dx, ky = h / d.dy;
          x.domain([d.x, d.x + d.dx]);
          y.domain([d.y, d.y + d.dy]);
        
          var t = svg.selectAll("g.cell").transition()
              .duration(d3.event.altKey ? 7500 : 750)
              .attr("transform", function(d) { return "translate(" + x(d.x) + "," + y(d.y) + ")"; });
        
          t.select("rect")
              .attr("width", function(d) { return kx * d.dx - 1; })
              .attr("height", function(d) { return ky * d.dy - 1; })
        
          t.select("text")
              .attr("x", function(d) { return kx * d.dx / 2; })
              .attr("y", function(d) { return ky * d.dy / 2; })
              .style("opacity", function(d) { return kx * d.dx > d.w ? 1 : 0; });
        
          node = d;
          d3.event.stopPropagation();
        }"""
}



