# coding: utf-8
#!/usr/bin/env python
import datetime
import re


class normalTable(object):
    def __init__(self):        
        self.html_fenye=u'''<span id="tablenav{pagei}" class="tbfoot" >{fenyespan}<span id="currentpage{pagei}"></span>/<span id="totalpages{pagei}"></span>页&nbsp;
                <a href="javascript:sorter{pagei}.move(-1,true)">首页</a>&nbsp;
                <a href="javascript:sorter{pagei}.move(-1)">上一页</a>&nbsp;
                <a href="javascript:sorter{pagei}.move(1)">下一页</a>&nbsp;
                <a href="javascript:sorter{pagei}.move(1,true)">尾页</a>&nbsp;
                <a href="javascript:sorter{pagei}.showall()">全部</a>&nbsp;
                <select id="pagedropdown{pagei}" style="visible:hidden"></select>
            </span>

            '''# <span style=" visibility:hidden; display:none;">
         # <select id="columns{pagei}" onchange="sorter{pagei}.search('query')"></select>
         #            <input type="text" id="query{pagei}" onkeyup="sorter{pagei}.search('query')" />
         #        </span>
        self.html_fenyejs=u'''<script type="text/javascript">
            var sorter{pagei} = new TINY.table.sorter('sorter{pagei}','table{pagei}',{
		    colddid:'columns{pagei}',
		    currentid:'currentpage{pagei}',
		    totalid:'totalpages{pagei}',
		    startingrecid:'startrecord{pagei}',
		    endingrecid:'endrecord{pagei}',
		    totalrecid:'totalrecords{pagei}',
		    hoverid:'selectedrow{pagei}',
		    pageddid:'pagedropdown{pagei}',
		    navid:'tablenav{pagei}',
            headclass:'head',
		    ascclass:'asc',
		    descclass:'desc',
		    evenclass:'evenrow',
		    oddclass:'oddrow',
		    evenselclass:'evenselected',
		    oddselclass:'oddselected',
		    sortdir:0,			
		    '''
        self.html_nofenyejs=u'''<script type="text/javascript">
            var sorter{pagei} = new TINY.table.sorter('sorter{pagei}','table{pagei}',{
            headclass:'head',
		    ascclass:'asc',
		    descclass:'desc',
		    evenclass:'evenrow',
		    oddclass:'oddrow',
		    evenselclass:'evenselected',
		    oddselclass:'oddselected',
		    sortdir:0,			
		    '''  
        #self.html_nofenyejs_blank=u'''<script type="text/javascript">           	
		#    '''  
        pass

    def makeHtmlTable_real(self,pageDetail,spagei,rows,resultinfo,columns,builder,linkname,ht_formartcolumn,isjs,isbootstrap=False):        
        tableheader=pageDetail['tableheader']
        RowStyle=pageDetail['rowstyle']
        rowcounts=len(rows)
        if isjs:
            pagesize=pageDetail['pagesize']
            if rowcounts<=pagesize:
                pagesize=0
        else:
            pagesize=0;

        if RowStyle in( "group","column") and len(columns)>1:
            columns=columns[1:]
        str_timeinfo=""
        #str_timeinfo=u"&nbsp;查询用时%s毫秒"%resultinfo.get('runtimes','-1')
        str_currentsize=""
        if pageDetail['width']=="99%":
            widthstr=""
        else:
            widthstr="width:%s"%pageDetail['width']
        if isbootstrap:
            str_currentsize=u'<span id="startrecord{spagei}"></span>-<span id="endrecord{spagei}"></span>/<span id="totalrecords{spagei}" >{rowcount}</span>'.format(spagei=spagei,rowcount=str(rowcounts))
            builder.append(u'<table id="table%s"  class="table %s" style="%s;%s"><thead>'%(spagei,pageDetail["css"],widthstr,pageDetail["style"]))
            builder.append(u'<tr>')
            for columnname in columns:
                builder.append(u'<th>{name}</th>'.format(name=columnname))#builder.append(u'<th>{name}</th>'.format(name=columnname.decode(self.GBKCHARTS)))
            builder.append(u'</tr>')
        else:


            builder.append(u'''<span  style=" visibility:hidden; display:none;" class="search"><select id="columns{pagei}" onchange="sorter{pagei}.search('query')"></select><input type="text" id="query{pagei}" onkeyup="sorter{pagei}.search('query')" /></span>  '''.replace('{pagei}',spagei))



            builder.append(u'<div class="tableheader" style="%s"><b>%s</b>'%(widthstr,pageDetail['title'].replace("{linkname}",linkname) ))
            if pageDetail['title2']<>'pagesize':
                builder.append(u'&nbsp;%s'%pageDetail['title2'])
            elif isjs:
                builder.append(u'&nbsp;共<span id="totalrecords%s"  class="f_tcolor">%s</span> 条 %s'%(spagei,str(rowcounts),str_timeinfo))
            if isjs and pagesize>0:#str(pagesize),
                builder.append(u',当前 <span id="startrecord%s" class="f_tcolor"></span>-<span id="endrecord%s" class="f_tcolor"></span> 条.'%(spagei,spagei))
                builder.append(self.html_fenye.format(pagei=spagei,fenyespan=str_currentsize))
            builder.append(u'</div>')
            if isjs:
                builder.append(u'<table cellpadding="0" cellspacing="0" border="0" id="table%s" class="geentable%s" style="%s;%s"><thead>'%(spagei,pageDetail["css"],widthstr,pageDetail["style"]))
            else:
                builder.append(u'<table cellpadding="0" cellspacing="0" border="0" id="table%s" class="geentable" style="%s;%s"><thead>'%(spagei,widthstr,pageDetail["style"]))
            
            if len(tableheader)>0:
                builder.append(tableheader)
            else:  
                builder.append(u'<tr>') 
                for columnname in columns:
                    builder.append(u'<th><h3>{name}'.format(name=columnname))#builder.append(u'<th><h3>{name}'.format(name=columnname.decode(self.GBKCHARTS)))
                    builder.append(u'</h3></th>')        
                builder.append(u'</tr>')
        builder.append(u'</thead><tbody>')

        self.get_table_tbody(rows,ht_formartcolumn,builder,RowStyle,isbootstrap,(pagesize>0))
        builder.append(u'</tbody></table>')

        print((isbootstrap,isjs,pagesize,RowStyle))
        if not isbootstrap:         
            if isjs:
                if RowStyle=="group":
                    print("dddd")
                    pass
                elif pagesize>0:
                    print("'''''")
                    builder.append(self.html_fenyejs.replace('{pagei}',spagei))
                    builder.append(u'''paginate:true,size:%s,'''%pagesize)
                    builder.append(pageDetail['table_addin']);
                    builder.append(u'''init:true});</script>''')               
                else:
                    builder.append(self.html_nofenyejs.replace('{pagei}',spagei))
                    builder.append(u'paginate:false,')
                    builder.append(pageDetail['table_addin']);
                    builder.append(u'''init:true});</script>''')

        
    #得到talbe的tbody
    def get_table_tbody(self, rows,ht_formartcolumn,builder,RowStyle="",isbootstrap=False,ispagesize=False):        
        int_rows=0
        lastparentid=""
        for row in rows:
            int_rows=int_rows+1
            if ispagesize:
                builder.append(u'<tr>')
            elif RowStyle not in ("group","column",""):
                builder.append(u'<tr style="%s">'%RowStyle)            
            elif RowStyle  in ("group","column"):
                builder.append(u'<tr')
            else:
                if int_rows%2==0:
                    builder.append(u'<tr>')
                else:
                    builder.append(u'<tr class="oddrow">')                            
            for i_nowcolumn,column in enumerate(row):
                si_nowcolumn=str(i_nowcolumn) 
                cellvalue=self.columnValue(column)                
                if  i_nowcolumn==0 and RowStyle  in ("group","column"):
                    if RowStyle=="group":
                        if "p"==cellvalue:
                            lastparentid=str(int_rows)
                            builder.append(u' class="pp_rent" id="%s">'%(lastparentid))
                        else:
                            builder.append(u' class="pp_child pp_child_%s">'%(lastparentid))                            
                    else:
                        builder.append(u' class="%s">'%(cellvalue))
                    continue
                if ht_formartcolumn.has_key(si_nowcolumn):
                    cellvalue=self.get_formartcolumnstr(ht_formartcolumn[si_nowcolumn],row,i_nowcolumn,isbootstrap)
                    builder.append(cellvalue)
                else:
                    builder.append(u'<td>')
                    builder.append(cellvalue)
                    builder.append(u'</td>')
            builder.append(u'</tr>')
        return 0

    #fz3
    def get_formartcolumnstr(self,formartstr,columns,columni,isbootstrap=False):
        tdstyle=""#预留
        if formartstr in ("percent100","percent0","percentsim100","percentsim0"):
            displayvalue=str(columns[columni])
            columevalue=int(columns[columni])
            if formartstr in ("percent0","percentsim0"):
                columevalue=100-columevalue
            spancss=""
            if columevalue>80:
                spancss="success"
            elif columevalue>60:
                spancss="info"
            elif columevalue>40:
                spancss="warning"
            else:
                spancss="danger"
            if isbootstrap:
                return u'''<td><div class="progress"><span class="progress-bar progress-bar-{spancss} progress-bar-striped" role="progressbar" aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="100" style="width: {value}%">{displayvalue}%</span></div></td>'''.format(spancss=spancss,value=columevalue,displayvalue=displayvalue)
                #return u'''<td><span class="label label-{spancss}">&nbsp;{value}%&nbsp;</span></td>'''.format(spancss=spancss,value=columevalue)
                #return u'''<td><div class="progress"><div class="progress-bar progress-bar-{spancss} progress-bar-striped" role="progressbar" aria-valuenow="{value}" aria-valuemin="0" aria-valuemax="100" style="width: {value}%"><span class="sr-only">{value}%</span></div></div></td>'''.format(spancss=spancss,value=columevalue)
            else:
                if 'percentsim' in formartstr:
                    return u'<td><span class="f_{spancss}"">{displayvalue}%</span></td>'.format(spancss=spancss,value=columevalue,displayvalue=displayvalue)
                else:
                    return u'<td><div class="progress"><span class="{spancss}" style="width: {value}%;"><span>{displayvalue}%</span></span></div></td>'.format(spancss=spancss,value=columevalue,displayvalue=displayvalue)
        elif formartstr=="warningbar":
            columevalue=str(columns[columni])
            columindex=columevalue.find("_")
            if  columindex>0:
                spancss=columevalue[0:columindex]
                columevalue=columevalue[columindex+1:]
                return u'''<td><span class="label label-{spancss}">{value}%</span></td>'''.format(spancss=spancss,value=columevalue)
            else:
                return u'''<td>{value}%/td>'''.format(value=columevalue)
        elif formartstr in ("p0","p1","p2","p3","p4"):
            columevalue=str(columns[columni])
            return "<td>%s</td>"%(columevalue)                              
        else:
            for c in re.compile(r'\{#*\d+\}').findall(formartstr):
                if '#' in c:
                    ic=int(c.replace('#','').replace('{','').replace('}',''))                
                    if ic<=len(self.paraValue_list):                    
                        formartstr=formartstr.replace(c,self.paraValue_list[ic])
                else:
                    ic=int(c.replace('{','').replace('}',''))              
                    if ic<=len(columns):
                        formartstr=formartstr.replace(c,self.columnValue(columns[ic]))
            return "<td>%s</td>"%(formartstr)  

    def columnValue(self,value):
        if isinstance(value,unicode) :
            #print("z")
            return value
        elif id(type) and type(value) in (datetime.datetime, datetime.date):
            #print '1.time2str'
            return self.time2str(value)
            #madmin.mainData().timeself,pageDetail,spagei,rows,resultinfo,columns,builder,linkname,ht_formartcolumn,isjs,2str(value)
        elif type(value) in ('int','long'):
            return str(value)
        elif type(value) ==bytearray:
            #print ''.join(hex(x) for x in value)
 
            #bytearray(value
            try:
                return "0x"+''.join(hex(x) for x in value).replace("0x","").upper()
            except:
                return "0xErr_20"
        elif type(value)==datetime.datetime:
            #print("*")
            return str(value)
        else:
            #print(str(value).replace("\\",""))
            try:
                #binder=[]
                #for i in value:
                #    binder.append(str(i))
                ##print(binder)           
                #return "".join(binder)
                return str(value)+""
            except:
                return "0xErr_10"

    def time2str(self,value):
        if isinstance(value, datetime.datetime):
            try:
                return value.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                return str(value)
        elif isinstance(value, datetime.date):
            try:
                return value.strftime('%Y-%m-%d')
            except ValueError:
                #print '1.str(value)'
                return str(value)
        else:
            #print 'else'
            try:
                #print 'dd'
                return  str(value)
            except:
                return 'is not time serializable'

class verticalTable(object):
    def __init__(self):
        pass
    def makeHtml(self,pageDetail,spagei,rows,resultinfo,columns,builder,linkname,ht_formartcolumn,isjs=False,isbootstrap=False):
        tableheader=pageDetail['tableheader']
        rowcounts=len(rows)
        if rowcounts==0:
            builder.append(u'<div style="marign:10px">该查询结果集返回：<span class="f_red fbold">0 </span>行！</div>')
            return 
        pagesize=pageDetail['pagesize']
        ipagenow_begin=0
        title=pageDetail['title']
        if pageDetail['width']=="99%":
            widthstr=""
        else:
            widthstr="width:%s"%pageDetail['width']
        if(pagesize<1):
            pagesize=1
        if len(tableheader)>0:
            tableheader.replace("<tr","<div").replace("</tr>","</div>").replace("</th>","</th>||")
            columns=tableheader.split('||')[-1]
        builder.append(u'<div class="tableheader" style="%s"><b>%s</b>'%(widthstr,pageDetail['title']))
        builder.append(u'<table cellpadding="1" cellspacing="1" border="0" id="table%s" class="geentable" style="%s;%s">'%(spagei,widthstr,pageDetail["style"]))
        for i_nowcolumn,columnname in enumerate(columns):
            builder.append(u'<tr>')
            builder.append(u'<th><h3>{name}'.format(name=columnname))#builder.append(u'<th><h3>{name}'.format(name=columnname.decode(self.GBKCHARTS)))
            builder.append(u'</h3></th>')
            ipagenow_end=ipagenow_begin+pagesize
            if ipagenow_end>rowcounts:
                ipagenow_end=rowcounts
            for ipagenow in range(ipagenow_begin,ipagenow_end):
                builder.append(u'<td>&nbsp;')
                #if ipagenow%2==0:
                #    builder.append(u'<td>&nbsp;')
                #else:
                #    builder.append(u'<td class="oddrow">')
                #print ("*"*10)
                cellvalue=normalTable().columnValue(rows[ipagenow][i_nowcolumn])
                if ht_formartcolumn.has_key(str(i_nowcolumn)):
                    cellvalue=self.get_formartcolumnstr(ht_formartcolumn[str(i_nowcolumn)],rows[ipagenow],i_nowcolumn,isbootstrap)
                builder.append(cellvalue)
                builder.append(u'</td>')
            builder.append(u'</tr>')
        builder.append(u'</table>')



class editTable(object):
    def __init__(self):
        pass
    def makeHtml(self,pageDetail,spagei,rows,resultinfo,columns,builder,editurl):
        columns_dict=pageDetail['edittable_format']
        rowcounts=len(rows)
        pagesize=pageDetail['pagesize']
        height=pageDetail['height'].replace("px","")
        title=pageDetail['title']
        spagei=""
        if pagesize<2:
            pagesize=10
        if columns_dict.has_key('width'):
            widthstr="width:"+columns_dict['width'].replace("px","")
        else:
            widthstr="autowidth: true"


        if columns_dict.has_key('colnames'):
            columnsstr="[' ', "+columns_dict['colnames']+"]"
        else:
            columnsstr="[' ', '"+"','".join(columns)+"']"

        if columns_dict.has_key('columnfarmat'):
            columnfarmat=columns_dict['columnfarmat']
        else:
            columnfarmat="""{name:'{columnname}',index:'{columnname}', width:150,editable: {editable},editoptions:{size:"20"}}"""


        datalist_formatlist=[]
        columndetail_list=[]


        freezecolumns=int(columns_dict.get('freezecolumns',-1))


        for i_nowcolumn,columnname in enumerate(columns):
            datalist_formatlist.append('{columnname}:"{{{i_nowcolumn}}}"'.format(i_nowcolumn=i_nowcolumn,columnname=columnname))
            if i_nowcolumn<freezecolumns:
                columndetail_list.append(columnfarmat.replace("{columnname}",columnname).replace("{editable}",'false'))
            else:
                columndetail_list.append(columnfarmat.replace("{columnname}",columnname).replace("{editable}",'true'))
        if columns_dict.has_key('colmodel'):
            columndetailstr=columns_dict['colmodel']
        else:
            columndetailstr=",".join(columndetail_list)
        datalist_format="{{"+",".join(datalist_formatlist)+"}}"
        datalist=[]
        for row in rows:
            datalist.append(datalist_format.format(*row))
        dataliststr=",".join(datalist)
        self.get_htmlstr_h(spagei,dataliststr,columnsstr,columndetailstr,pagesize,height,editurl,title,widthstr,builder)
    def get_htmlstr_h(self,spagei,datalist,columns,columndetail,pagesize,height,editurl,title,widthstr,builder):
        builder.append("""
        <div class="main-container">
            <div class="page-content">
                <div class="row">
                    <div class="col-xs-12">
                        <table id="grid-table{spagei}"></table>
                        <div id="grid-pager{spagei}"></div>
                        <!-- PAGE CONTENT ENDS -->
                    </div><!-- /.col -->
                </div><!-- /.row -->
            </div><!-- /.page-content -->
        </div><!-- /.main-content -->
		<script type="text/javascript">
            var grid_data{spagei} =[{datalist}];
			jQuery(function($) {
			    var grid_selector = "#grid-table{spagei}";
			    var pager_selector = "#grid-pager{spagei}";
				jQuery(grid_selector).jqGrid({
					//direction: "rtl",					
				    data: grid_data{spagei},
					datatype: "local",
                    colNames:{columns},
					colModel:[
						{name:'myac',index:'', width:80, fixed:true, sortable:false, resize:false,
							formatter:'actions', 
							formatoptions:{ 
								keys:true,								
								delOptions:{recreateForm: true, beforeShowForm:beforeDeleteCallback},
								//editformbutton:true, editOptions:{recreateForm: true, beforeShowForm:beforeEditCallback}
							}
						},
						{columndetail}
					], """.replace("{spagei}",spagei).replace("{datalist}",datalist).replace("{columns}",columns).replace("{columndetail}",columndetail))
        #
        builder.append("""
                     height: {height},
					viewrecords : true,
					rowNum: {pagesize},
                    editurl: "{editurl}",//nothing is saved
					caption: "{title}",
					pager : pager_selector,
					altRows: true,
					//toppager: true,	
					multiselect: true,
					//multikey: "ctrlKey",
			        multiboxonly: true,			
					loadComplete : function() {
						var table = this;
						setTimeout(function(){
							styleCheckbox(table);
							updateActionIcons(table);
							updatePagerIcons(table);
							enableTooltips(table);
						}, 0);
					},		
					{widthstr}
				});""".replace("{spagei}",spagei).replace("{pagesize}",str(pagesize)).replace("{editurl}",editurl).replace("{title}",title).replace("{height}",height).replace("{widthstr}",widthstr))
        builder.append("""
        
				//enable search/filter toolbar
				//jQuery(grid_selector).jqGrid('filterToolbar',{defaultSearch:true,stringResult:true})
			
				//switch element when editing inline
				function aceSwitch( cellvalue, options, cell ) {
					setTimeout(function(){
						$(cell) .find('input[type=checkbox]')
								.wrap('<label class="inline" />')
							.addClass('ace ace-switch ace-switch-5')
							.after('<span class="lbl"></span>');
					}, 0);
				}
				//enable datepicker
				function pickDate( cellvalue, options, cell ) {
					setTimeout(function(){
						$(cell) .find('input[type=text]')
								.datepicker({format:'yyyy-mm-dd' , autoclose:true}); 
					}, 0);
				}	
			
				//navButtons
				jQuery(grid_selector).jqGrid('navGrid',pager_selector,
					{ 	//navbar options
						edit: true,
						editicon : 'icon-pencil blue',
						add: true,
						addicon : 'icon-plus-sign purple',
						del: true,
						delicon : 'icon-trash red',
						search: true,
						searchicon : 'icon-search orange',
						refresh: true,
						refreshicon : 'icon-refresh green',
						view: true,
						viewicon : 'icon-zoom-in grey',
					},
					{
						//edit record form
						//closeAfterEdit: true,
						recreateForm: true,
						beforeShowForm : function(e) {
							var form = $(e[0]);
							form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />')
							style_edit_form(form);
						}
					},
					{
						//new record form
						closeAfterAdd: true,
						recreateForm: true,
						viewPagerButtons: false,
						beforeShowForm : function(e) {
							var form = $(e[0]);
							form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />')
							style_edit_form(form);
						}
					},
					{
						//delete record form
						recreateForm: true,
						beforeShowForm : function(e) {
							var form = $(e[0]);
							if(form.data('styled')) return false;
							
							form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />')
							style_delete_form(form);
							
							form.data('styled', true);
						},
						onClick : function(e) {
							alert(1);
						}
					},
					{
						//search form
						recreateForm: true,
						afterShowSearch: function(e){
							var form = $(e[0]);
							form.closest('.ui-jqdialog').find('.ui-jqdialog-title').wrap('<div class="widget-header" />')
							style_search_form(form);
						},
						afterRedraw: function(){
							style_search_filters($(this));
						}
						,
						multipleSearch: true,
						/**
						multipleGroup:true,
						showQuery: true
						*/
					},
					{
						//view record form
						recreateForm: true,
						beforeShowForm: function(e){
							var form = $(e[0]);
							form.closest('.ui-jqdialog').find('.ui-jqdialog-title').wrap('<div class="widget-header" />')
						}
					}
				)
				function style_edit_form(form) {
					//enable datepicker on "sdate" field and switches for "stock" field
					form.find('input[name=sdate]').datepicker({format:'yyyy-mm-dd' , autoclose:true})
						.end().find('input[name=stock]')
							  .addClass('ace ace-switch ace-switch-5').wrap('<label class="inline" />').after('<span class="lbl"></span>');
			
					//update buttons classes
					var buttons = form.next().find('.EditButton .fm-button');
					buttons.addClass('btn btn-sm').find('[class*="-icon"]').remove();//ui-icon, s-icon
					buttons.eq(0).addClass('btn-primary').prepend('<i class="icon-ok"></i>');
					buttons.eq(1).prepend('<i class="icon-remove"></i>')
					
					buttons = form.next().find('.navButton a');
					buttons.find('.ui-icon').remove();
					buttons.eq(0).append('<i class="icon-chevron-left"></i>');
					buttons.eq(1).append('<i class="icon-chevron-right"></i>');		
				}
			
				function style_delete_form(form) {
					var buttons = form.next().find('.EditButton .fm-button');
					buttons.addClass('btn btn-sm').find('[class*="-icon"]').remove();//ui-icon, s-icon
					buttons.eq(0).addClass('btn-danger').prepend('<i class="icon-trash"></i>');
					buttons.eq(1).prepend('<i class="icon-remove"></i>')
				}
				
				function style_search_filters(form) {
					form.find('.delete-rule').val('X');
					form.find('.add-rule').addClass('btn btn-xs btn-primary');
					form.find('.add-group').addClass('btn btn-xs btn-success');
					form.find('.delete-group').addClass('btn btn-xs btn-danger');
				}
				function style_search_form(form) {
					var dialog = form.closest('.ui-jqdialog');
					var buttons = dialog.find('.EditTable')
					buttons.find('.EditButton a[id*="_reset"]').addClass('btn btn-sm btn-info').find('.ui-icon').attr('class', 'icon-retweet');
					buttons.find('.EditButton a[id*="_query"]').addClass('btn btn-sm btn-inverse').find('.ui-icon').attr('class', 'icon-comment-alt');
					buttons.find('.EditButton a[id*="_search"]').addClass('btn btn-sm btn-purple').find('.ui-icon').attr('class', 'icon-search');
				}
				
				function beforeDeleteCallback(e) {
					var form = $(e[0]);
					if(form.data('styled')) return false;
					
					form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />')
					style_delete_form(form);
					
					form.data('styled', true);
				}
				
				function beforeEditCallback(e) {
					var form = $(e[0]);
					form.closest('.ui-jqdialog').find('.ui-jqdialog-titlebar').wrapInner('<div class="widget-header" />')
					style_edit_form(form);
				}
				//it causes some flicker when reloading or navigating grid
				//it may be possible to have some custom formatter to do this as the grid is being created to prevent this
				//or go back to default browser checkbox styles for the grid
				function styleCheckbox(table) {
				/**
					$(table).find('input:checkbox').addClass('ace')
					.wrap('<label />')
					.after('<span class="lbl align-top" />')
			
			
					$('.ui-jqgrid-labels th[id*="_cb"]:first-child')
					.find('input.cbox[type=checkbox]').addClass('ace')
					.wrap('<label />').after('<span class="lbl align-top" />');
				*/
				}
				
			
				//unlike navButtons icons, action icons in rows seem to be hard-coded
				//you can change them like this in here if you want
				function updateActionIcons(table) {
					/**
					var replacement = 
					{
						'ui-icon-pencil' : 'icon-pencil blue',
						'ui-icon-trash' : 'icon-trash red',
						'ui-icon-disk' : 'icon-ok green',
						'ui-icon-cancel' : 'icon-remove red'
					};
					$(table).find('.ui-pg-div span.ui-icon').each(function(){
						var icon = $(this);
						var $class = $.trim(icon.attr('class').replace('ui-icon', ''));
						if($class in replacement) icon.attr('class', 'ui-icon '+replacement[$class]);
					})
					*/
				}
				
				//replace icons with FontAwesome icons like above
				function updatePagerIcons(table) {
					var replacement = 
					{
						'ui-icon-seek-first' : 'icon-double-angle-left bigger-140',
						'ui-icon-seek-prev' : 'icon-angle-left bigger-140',
						'ui-icon-seek-next' : 'icon-angle-right bigger-140',
						'ui-icon-seek-end' : 'icon-double-angle-right bigger-140'
					};
					$('.ui-pg-table:not(.navtable) > tbody > tr > .ui-pg-button > .ui-icon').each(function(){
						var icon = $(this);
						var $class = $.trim(icon.attr('class').replace('ui-icon', ''));
						
						if($class in replacement) icon.attr('class', 'ui-icon '+replacement[$class]);
					})
				}
			
				function enableTooltips(table) {
					$('.navtable .ui-pg-button').tooltip({container:'body'});
					$(table).find('.ui-pg-div').tooltip({container:'body'});
				}
			
				//var selr = jQuery(grid_selector).jqGrid('getGridParam','selrow');
			
			
			});
		</script>
        """)
        pass


if __name__ == '__main__':
    pageDetail={'pagesize':10,'height':'350','title':'TEST','edittable_format':{'colnames':"'a','b','c','d','e','f'"},'tableheader':'','width':'900px','style':''}
    spagei=""    
    rows=[(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6),(1,2,3,4,5,6)]
    resultinfo=""
    columns=("a","b","c","d","e","f")
    builder=[]
    editurl="http://www.dboop.com"
    #fx=editTable()
    #fx.makeHtml(pageDetail,spagei,rows,resultinfo,columns,builder,editurl,)
    #pageDetail,spagei,rows,resultinfo,columns,builder,editurl,columns_dict
    fx=verticalTable()
    #pageDetail,spagei,rows,resultinfo,columns,builder,linkname,ht_formartcolumn
    linkname="bjs-dbhotel"
    ht_formartcolumn={}
    fx.makeHtml(pageDetail,spagei,rows,resultinfo,columns,builder,linkname,ht_formartcolumn)
    #print("\n".join(builder))
    fout = open("jq.html",'wb')
    fout.write("""<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<title></title>
		<link href="css/bootstrap.min.css" rel="stylesheet" />
		<link rel="stylesheet" href="css/font-awesome.min.css" />
		<link rel="stylesheet" href="css/jquery-ui-1.10.3.full.min.css" />
		<link rel="stylesheet" href="css/datepicker.css" />
		<link rel="stylesheet" href="css/ui.jqgrid.css" />	
		<link rel="stylesheet" href="css/ace.min.css" />
	</head>
	<body>""")
    fout.write("\r\n".join(builder))
    fout.write("""</body>
</html>
""")

    fout.close()    

