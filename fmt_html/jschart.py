# -*- coding: utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
import htmlstr_
class chart():
    pub_chart_js = []  # 图表的js
    pub_dic_jsvara={}
    def __int__(self):
        pass


    def make_static_chart(self,rows, columns, spagei=0, page={}):
        pageDetail={}
        pageDetail['viewtype'] = page.get('viewtype', 'line')
        #pageDetail['pagesize'] = int(page.get('pagesize', '0'))
        #pageDetail['table_addin'] = page.get('table_addin', '')
        #pageDetail['format'] = (page.get('format', ''))
        #pageDetail['html'] = page.get('html', '')
        pageDetail['width'] = page.get('width', '99%')
        pageDetail['style'] = page.get('style', '')
        #pageDetail['ajax'] = page.get('ajax', '')
        pageDetail['chart_yaxis'] = page.get('chart_yaxis', '')
        pageDetail['chart_ymin'] = page.get('chart_ymin', 'false')
        pageDetail['height'] = page.get('height', '400px')
        pageDetail['title'] = page.get('title', '')
        pageDetail['chart_tooltip'] = page.get('chart_tooltip', 'false')
        pageDetail['chart_xtype'] = page.get('chart_xtype', 'category')
        pageDetail['chart_title'] = page.get('chart_title', '')
        pageDetail['chart_radius'] = page.get('chart_radius', '50%')
        pageDetail['chart_center_x'] = page.get('chart_center_x', "50%")
        pageDetail['chart_center_y'] = page.get('chart_center_y', "50%")
        pageDetail['chart_theme'] = page.get('chart_theme', '')
        pageDetail['chart_maptype'] = page.get('chart_maptype', 'china')
        pageDetail['chart_datazoom'] = page.get('chart_datazoom', '')
        pageDetail['chart_group'] = page.get('chart_group', '')
        pageDetail['chart_addin'] = page.get('chart_addin', '')  # grid:{ x:20,x2:10,y2:30 },
        pageDetail['css'] = page.get('css', '')
        pageDetail['chart_legendstyle'] = page.get('chart_legendstyle', "x:'left',borderWidth:1,padding:10")  #
        pageDetail['chart_itemstyle'] = self.get_diccontent_bydic(page, 'chart_itemstyle')

        css_file = []
        html_footer = ""
        builder_html=[]
        builder_html.append(u'<div id="chart%s" class="%s" style="margin-left:5px;padding-top:5px;height:%s;width:%s;%s"></div>' % (
            spagei, pageDetail.get("css",""), pageDetail.get("height",600), pageDetail["width"], pageDetail["style"]))
        self.get_chart_option_real(pageDetail, spagei,rows,columns)

        htmlstr = "\n".join(builder_html) +'<script type="text/javascript">'+ "\n".join(self.pub_chart_js )+'</script>'
        js_file=['<script src="/static/js/echarts.min.js"></script>']
        return htmlstr, js_file, css_file, html_footer




    def get_chart_option_real(self, pageDetail, spagei, rows, columns, linkname=""):
        charttype = pageDetail["viewtype"]
        columncount = len(columns)
        if len(rows) == 0 or columncount < 2:
            # return (u'<div style="height:%s;width:%s;%s">图表数据不足，无法展现(至少需要1行数据)</div>'%(pageDetail["height"],pageDetail["width"],pageDetail["style"]))
            return 0
        if pageDetail["chart_theme"] == "":
            self.pub_chart_js.append(u"var myChart%s = echarts.init(document.getElementById('chart%s'));" % (spagei, spagei))
        else:
            self.pub_chart_js.append(u"""%s
            var myChart%s = echarts.init(document.getElementById('chart%s'),%s);""" % (
            htmlstr_.html_chart_theme[pageDetail["chart_theme"]], spagei, spagei, pageDetail["chart_theme"]))
        self.pub_chart_js.append(u"var option%s =" % spagei)
        self.pub_chart_js.append(u"{animation : false,")
        self.pub_chart_js.append(pageDetail['chart_title'].replace("{linkname}", linkname))

        rowsValue = map(list, zip(*rows))

        columnValues, columnValues__display = self.get_realColumValues(columns, columncount)
        if charttype in ('gauge') or pageDetail["chart_tooltip"] == "false":
            self.pub_chart_js.append(htmlstr_.html_chart_toolbox['none'])
        elif charttype in ('line', 'bar', 'mutibar'):
            self.pub_chart_js.append(htmlstr_.html_chart_toolbox['normal'])
        else:
            self.pub_chart_js.append(htmlstr_.html_chart_toolbox['simple'])
        self.pub_chart_js.append(pageDetail["chart_addin"]);
        self.pub_chart_js.append('calculable : true,')
        # 1.简单的饼图，仪表板，直接替换
        if charttype in ('pie', 'gauge'):
            pievalue = []
            # rowsValue=map(list,zip(*rows))
            if len(columnValues__display) > 1:
                for pie_i in range(0, len(columnValues__display)):
                    # builder.append("data:%s"%optionname)
                    pievalue.append(
                        u"{value:%s, name:'%s'}" % (str(rowsValue[pie_i + 1][0]), columnValues__display[pie_i]))
                    if pie_i < len(columnValues__display) - 1:
                        pievalue.append(u",")
            else:
                for pie_i in range(0, len(rowsValue[0])):
                    # builder.append("data:%s"%optionname)
                    pievalue.append(u"{value:%s, name:'" % str(rowsValue[1][pie_i]))
                    pievalue.append(rowsValue[0][pie_i])
                    if pie_i < len(rowsValue[0]) - 1:
                        pievalue.append(u"'},")
                    else:
                        pievalue.append(u"'}")
                        # optionname=u'chart_%s_%s'%(spagei,str(pie_i+1))
            # builder_html.append(u"var %s=[%s];"%(optionname,"".join(pievalue)))
            # builder.append(htmlstr_.html_chart_simple[charttype].replace('{wokofo_value_name}',optionname))
            self.pub_chart_js.append(
                htmlstr_.html_chart_simple[charttype].replace('{wokofo_radius}', pageDetail["chart_radius"]).replace(
                    '{wokofo_center_x}', pageDetail["chart_center_x"]).replace('{wokofo_center_y}',
                                                                               pageDetail["chart_center_y"]).replace(
                    '{wokofo_value_name}', "".join(pievalue)))
        # 复杂的图型（一般都有多列，需要循环列数COLUMNCOUNT）
        elif charttype == "radar":
            # self.pub_chart_js.append("legend: {x : 'right',y:'bottom',data:['%s']},"%"','".join(columnValues__display))
            builder_polar = []
            for ri in rowsValue[0]:
                builder_polar.append("{text : '%s', max  : 100}" % self.columnValue(ri))
            self.pub_chart_js.append("polar : [{indicator : [%s],radius : 130}]," % (",".join(builder_polar)))
            builder_yvalue = []
            for i in range(1, columncount):
                builder_yvalue.append("{value : [%s],name : '%s'}" % (
                self.get_series_datalist_s(rowsValue[i]), columnValues__display[i - 1]))
            self.pub_chart_js.append(
                "series : [{type: 'radar',itemStyle: {normal: { areaStyle: {type: 'default'} } },data : [%s]}]" % ','.join(
                    builder_yvalue))
        else:
            if charttype == 'map':
                self.pub_chart_js.append(
                    u"mapType: '%s',itemStyle:{normal:{label:{show:true}},emphasis:{label:{show:true}}}," % pageDetail[
                        "chart_maptype"])
                # print rowsValue

                self.pub_chart_js.append(
                    u"dataRange: {min: 0,max: %s,text:['高','低'],calculable : true}," % str(max(rowsValue[1])))
            else:
                if pageDetail['chart_datazoom'] <> '':
                    self.pub_chart_js.append(htmlstr_.html_chart_dataZoom % pageDetail['chart_datazoom'])
                self.pub_chart_js.append(u"tooltip: {show: true,trigger: 'axis'},")
                if "show:false" not in pageDetail['chart_legendstyle']:
                    self.pub_chart_js.append(u"legend: {data: ['%s'],%s}," % (
                    "','".join(columnValues__display), pageDetail['chart_legendstyle']))
                if pageDetail["chart_group"] == "":
                    self.pub_chart_js.append(u"xAxis: [{type: '%s',data: ['%s'] }]," % (
                    pageDetail['chart_xtype'], "','".join(str(ri) for ri in rowsValue[0])))
                else:
                    axisData_key = pageDetail["chart_group"]
                    if not self.pub_dic_jsvara.has_key(axisData_key):
                        self.pub_dic_jsvara[axisData_key] = (
                        u"['%s']" % ("','".join(self.columnValue(ri) for ri in rowsValue[0])), ["myChart%s" % spagei])
                        # self.dic_chartbind[axisData_key]=['myChart%s'%spagei]
                    else:
                        if spagei not in self.pub_dic_jsvara[axisData_key][1]:
                            self.pub_dic_jsvara[axisData_key][1].append("myChart%s" % spagei)
                            # else:
                            # self.dic_chartbind[axisData_key].append('myChart%s'%spagei)
                    self.pub_chart_js.append(htmlstr_.html_char_xbind % (pageDetail['chart_xtype'], axisData_key))
                self.pub_chart_js.append(
                    u"yAxis : [%s]," % self.get_yalix(pageDetail['chart_yaxis'], pageDetail['chart_ymin']))
            self.pub_chart_js.append("series: [")
            for i in range(1, columncount):
                self.pub_chart_js.append(" {")
                if charttype == 'map':
                    # 处理name,charttype
                    self.pub_chart_js.append(u"name:'%s',type:'map'," % columnValues[i - 1])
                    self.pub_chart_js.append(
                        u"mapType: '%s',itemStyle:{normal:{label:{show:true}},emphasis:{label:{show:true}}}," %
                        pageDetail["chart_maptype"])
                    # 处理数值
                    self.pub_chart_js.append(
                        self.get_series_datadic(rowsValue[i], rowsValue[0]))  # 数值列 data[{value:,name:},]
                else:
                    # 处理name,charttype
                    self.pub_chart_js.append(self.get_series_type(charttype, columnValues[i - 1],
                                                                  pageDetail["chart_itemstyle"].get(str(i), ''),
                                                                  str(len(rowsValue[0]))))
                    # 处理数值
                    self.pub_chart_js.append(self.get_series_datalist(rowsValue[i]))  # 数值列 data[value,]
                if i < columncount - 1:
                    self.pub_chart_js.append(" },")
                else:
                    self.pub_chart_js.append(" }")
            self.pub_chart_js.append("]")
            # linesend
        self.pub_chart_js.append("};")
        self.pub_chart_js.append(u" myChart%s.setOption(option%s,true);" % (spagei, spagei))

        # for (xkeys,xvalues) in self.dic_chartbind.items():
        #    xvalues2 = list(set(xvalues))
        #    for chartn in xvalues2:
        #        chartnstr=("{m1}.connect([,{m2},]);".format(m1=chartn,m2=",".join(xvalues2))).replace(","+chartn+",","").replace("([,","([").replace(",])","])")
        #        builder.append(chartnstr)

        # return 0


        # 生成series(1)



    def get_realColumValues(self, columns, columncount):
        columnValues = []
        columnValues__display = []
        for i in range(1, columncount):
            cvalue = str(columns[i]).decode('utf8')  # 20141016修改,可能用问题
            columnValues.append(cvalue)
            if "__" in cvalue:
                columnValues__display.append(cvalue[0:cvalue.index('__')])
            else:
                columnValues__display.append(cvalue)
        return columnValues, columnValues__display

    def get_series_datadic(self, rowsValue, rowsValue0):
        pievalue2 = []
        for pie_i in range(0, len(rowsValue)):
            pievalue2.append(u"{value:%s, name:'" % str(rowsValue[pie_i]))
            pievalue2.append(rowsValue0[pie_i])
            if pie_i < len(rowsValue0) - 1:
                pievalue2.append(u"'},")
            else:
                pievalue2.append(u"'}")
        return ("data:[%s]" % "".join(pievalue2))
        # 生成series(2)

    def get_series_datalist(self, rowsValue):
        return ("data:[%s]" % (",".join(str(ri) for ri in rowsValue)))

    def get_series_datalist_s(self, rowsValue):
        return (",".join(str(ri) for ri in rowsValue))

    # 生成type()
    def get_series_type(self, charttype, columnValue, chart_itemstyle, max_x):
        yalix_str = ''
        chart_itemstyle_str = self.get_html_chart_item_detail(chart_itemstyle, max_x)

        linestyle = ''
        if charttype == "mix" and '__' in columnValue:
            yalix = columnValue.split('__')
            columnValue = yalix[0]
            if len(yalix) > 1:
                yalix_str = "yAxisIndex:%s," % yalix[1]
            if len(yalix) > 2:
                charttype = yalix[2]
            else:
                charttype = "line"

            if len(yalix) > 3:
                linestylestr = yalix[3].split('_')
                #
                linestyle = " itemStyle: {normal: {lineStyle: {color:'%s',width:%s,type:'%s'}}}," % (
                linestylestr[0], linestylestr[1], linestylestr[2])
                # linestyle=''
        if charttype == 'stack':
            return "name:'%s',type:'line'%s,%s smooth:true%s,stack: 'all',symbol: 'none',%s" % (
            columnValue, chart_itemstyle_str, yalix_str, htmlstr_.html_chart_item_detail.get('stack'), linestyle)
        elif charttype == 'mutistack':
            return "name:'%s',type:'line'%s,%s smooth:true%s,stack: '%s',symbol: 'none',%s" % (
            columnValue, chart_itemstyle_str, yalix_str, htmlstr_.html_chart_item_detail.get('stack'), columnValue[0:1],
            linestyle)
        elif charttype == 'nostack':
            return "name:'%s',type:'line'%s,%s smooth:true%s,symbol: 'none',%s" % (
            columnValue, chart_itemstyle_str, yalix_str, htmlstr_.html_chart_item_detail.get('stack'), linestyle)
        elif charttype == 'mutibar':
            return "name:'%s',type:'bar',stack: 'all'%s,%s" % (columnValue, chart_itemstyle_str, yalix_str)
        else:
            return "name:'%s',symbol: 'none',type:'%s'%s,%s%s" % (
            columnValue, charttype, chart_itemstyle_str, yalix_str, linestyle)

    def get_html_chart_item_detail(self, itemstr, max_x):
        if len(itemstr) == 0:
            return ""

        resultstr = ""

        itemlist = itemstr.split(",")
        for item in itemlist:
            if ":" in item:
                itemsplits = item.split(':')
                funname = itemsplits[0]
                funvalue = (itemsplits[1].split('|'))
                if funname == 'markline':
                    if funvalue[0] in ('average', 'min', 'max'):
                        resultstr += htmlstr_.html_chart_item_detail.get('marklinesimple').format(*funvalue)
                    else:
                        resultstr += htmlstr_.html_chart_item_detail.get('markline').format(*funvalue, max_x=max_x)
                else:
                    resultstr += (htmlstr_.html_chart_item_detail.get(funname).format(*funvalue))
            else:
                resultstr += htmlstr_.html_chart_item_detail.get(item)
        return resultstr

    # 得到y轴格式
    def get_yalix(self, chart_yaxis, ymin):
        if chart_yaxis == '':
            return u"{type : 'value',splitArea : {show : true},scale:%s}" % str(ymin)
        else:
            builder = []
            yalixs = chart_yaxis.split(',')
            for yi, yalix in enumerate(yalixs):
                yalix_s = yalix.split(':')
                builder.append(u"{name : '%s',type : 'value'" % yalix_s[0])
                if len(yalix_s) > 1:
                    if yalix_s[1] == "-1":
                        builder.append(u",axisLabel : {formatter: function(v){return - v;}}")
                    else:
                        builder.append(u",axisLabel : {formatter: '{value}%s'}" % yalix_s[1])
                if yi == len(yalixs) - 1:
                    builder.append(u",scale:%s}" % str(ymin));
                else:
                    builder.append(u",scale:%s}," % str(ymin));
            return "".join(builder)


    def get_diccontent_bydic(self,page,keyvalue):
        dic_temp={}
        if page.has_key(keyvalue) and page[keyvalue].has_key('column'):
            tempkeys=page[keyvalue]['column']
            if isinstance(tempkeys, list):
                for itemstyle in tempkeys:
                    dic_temp[itemstyle['@id']]=itemstyle['#text']
            elif isinstance(tempkeys, dict):
                dic_temp[tempkeys['@id']]=tempkeys['#text']
        return dic_temp


if __name__ == "__main__":
    charts = chart()
    rows=[('11:00',1,2),('11:30',3,4),('12:00',5,6),('12:30',2,1)]
    columns=('addtime','Today__1__bar','LastWeek__1__line')
    echart_format={}
    htmlstr, js_file, css_file, html_footer = charts.make_static_chart(rows, columns, 0, echart_format)
    print (htmlstr)