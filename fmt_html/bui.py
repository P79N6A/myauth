# -*- coding:utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals
from collections import OrderedDict


html_tips_title="""
   <script type="text/javascript">
    BUI.use('bui/tooltip',function (Tooltip) {
      var tips_title = new Tooltip.Tips({
        tip : {
          trigger : '.tipsuccess', //出现此样式的元素显示tip
          alignType : 'top', //默认方向
          elCls : 'tips tips-success',
          alignType : 'right',
        offset : 10, 
          titleTpl : '<span class="x-icon x-icon-small x-icon-success"><i class="icon icon-white icon-volume-up"></i></span><div class="tips-content">{title}</div>',
        }
      });
      tips_title.render();
         });
    </script>
"""

def make_smalltips(mess,tip="info"):
    tipdic={"warning":"bell","success":"ok","info":"info"}
    return """<div class="tips tips-small  tips-{tip}">
        <span class="x-icon x-icon-small x-icon-{tip}"><i class="icon icon-white icon-{icon}"></i></span>
        <div class="tips-content">{mess}</div>
      </div> 
    """.format(mess=mess,tip=tip,icon=tipdic.get(tip,tip))


def make_stepbar(listbar=[],curindex=0):
    sb_html=[]
    if curindex<0:
        curindex=abs(curindex) #标红等处理留着
    bar_count=len(listbar)
    sb_html.append('<div class="flow-steps"><ol class="num%s unstyled">'%(bar_count,))
    for i_index,bartitle in enumerate(listbar):
        sb_style=[]
        if i_index==0:
            sb_style.append("first")
        if i_index<curindex:
            if i_index==curindex-1:
                sb_style.append("current-prev")
            else:
                sb_style.append("done")
        if i_index<=curindex:
            sb_style.append("current")
        if i_index == bar_count-1:
            sb_style.append("last")
        sb_html.append('<li class="%s"> %s. %s</li>'%(" ".join(sb_style),(i_index+1),bartitle))
    sb_html.append('</ol></div>')
    return "\n".join(sb_html)


def make_static_tree(rows, columns, div_id, format_dic={}):
    height = format_dic.get("height", "450")
    js_file = ["""<script src="/static/js/jquery-1.8.1.min.js"></script>""",
               """<script src="/static/js/bui/bui.js"></script>""", """<script src="/static/js/view.js"></script>"""]
    css_file = []
    html_footer = ""
    if len(columns) > 1:
        columns = columns[1:]
    if format_dic.has_key("columns"):
        columnstr = format_dic["columns"]
    else:
        sb_columnstr = []
        for column in columns:
            sb_columnstr.append("{title: '%s', dataIndex: '%s'}" % (column, column))
        columnstr = ",".join(sb_columnstr)
    primarykeytype = format_dic.get("primarykey", "key1==key2:primary")
    sb_datastr = []
    od = OrderedDict()
    for row in rows:
        # dic={"1"}
        if primarykeytype == "key1==key2:primary":
            pid = row[0]
            nid = row[1]
            if pid == nid:
                # add newparent
                if od.has_key(pid):  # child
                    od[pid][0] = row[1:]
                else:
                    od[pid] = (row[1:], [])
            else:
                if od.has_key(pid):
                    od[pid][1].append(row[1:])
                else:
                    od[pid] = (row[1:], row[1:])
        elif primarykeytype == "key1 not exists :primary":
            pid = row[0]
            if od.has_key(pid):
                od[pid][1].append(row[1:])
            else:
                od[pid] = (row[1:], [])
    for keyid in od.keys():
        row = od[keyid][0]
        childlist = od[keyid][1]
        rowstr = get_columnstr(row, columns, childlist)
        sb_datastr.append("{%s}" % (rowstr,))

    datastr = ",".join(sb_datastr)
    bui_static_tree_template = """
        <div id="page_{div_id}"></div>
        <script type="text/javascript">
      BUI.use('bui/tree',function (Tree) {{
      var data = [{data}];
      var tree = new Tree.TreeList({{
        render : '#page_{div_id}',
        nodes : data
         {tree_style}
      }});
      tree.render();
      tree.on('itemclick',function(ev){{
        var item = ev.item;
        {onchangestr}
      }});
    }});
    </script>
           """
    htmlstr = bui_static_tree_template.format(div_id=div_id, data=datastr,onchangestr=format_dic.get("onchangestr", ""), tree_style=format_dic.get("tree_style", ""))
    return htmlstr, js_file, css_file, html_footer

def make_static_treegrid(rows,columns,div_id,format_dic={}):
    # sb_html=""
    height = format_dic.get("height", "450")
    js_file = ["""<script src="/static/js/jquery-1.8.1.min.js"></script>""",
               """<script src="/static/js/bui/bui.js"></script>""", """<script src="/static/js/view.js"></script>"""]
    css_file = []
    html_footer = ""

    if len(columns)>1:
        columns=columns[1:]
    if format_dic.has_key("columns"):
        columnstr = format_dic["columns"]
    else:
        sb_columnstr = []
        for column in columns:
            sb_columnstr.append("{title: '%s', dataIndex: '%s'}" % (column, column))
        columnstr = ",".join(sb_columnstr)

    primarykeytype=format_dic.get("primarykey", "key1==key2:primary")
    sb_datastr = []
    od = OrderedDict()
    for row in rows:
        #dic={"1"}
        if primarykeytype=="key1==key2:primary":
            pid=row[0]
            nid=row[1]
            if pid==nid:
                #add newparent
                if od.has_key(pid):#child
                    od[pid][0] = row[1:]
                else:
                    od[pid]=(row[1:],[])
            else:
                if od.has_key(pid):
                    od[pid][1].append(row[1:])
                else:
                    od[pid]=(row[1:],row[1:])
        elif primarykeytype=="key1 not exists :primary":
            pid = row[0]
            if od.has_key(pid):
                od[pid][1].append(row[1:])
            else:
                od[pid] = (row[1:], [])

    for keyid in od.keys():
        row=od[keyid][0]
        childlist=od[keyid][1]
        rowstr=get_columnstr(row, columns,childlist)
        sb_datastr.append("{%s}" % (rowstr,))

    datastr = ",".join(sb_datastr)
    bui_static_tree_template = """
        <div id="page_{div_id}"></div>
        <script type="text/javascript">
        BUI.use(['bui/extensions/treegrid'],function (TreeGrid) {{
      var data = [{data}];
     
      var tree = new TreeGrid({{
        render : '#page_{div_id}',
        nodes : data,
        columns : [{columns}]
         {tree_style}
      }});
      tree.render();
    }});
    </script>
           """
    htmlstr = bui_static_tree_template.format(div_id=div_id, columns=columnstr, data=datastr,tree_style=format_dic.get("tree_style", "")
                                              )
    return htmlstr, js_file, css_file, html_footer


def get_columnstr(row,columns,childlist=[]):
    sb_row = []
    for columni, column in enumerate(columns):
        sb_row.append("%s:'%s'" % (column, row[columni]))
    if len(childlist)>0:
        #(childlist)
        sb_childstr=[]
        for child_row in childlist:
            sb_childstr.append("{%s}" % (get_columnstr(child_row,columns),))
        sb_row.append("children: [%s]"%(",".join(sb_childstr),))
    return ",".join(sb_row)


def make_static_grid(rows,columns,div_id=0,format_dic={}):
    #sb_html=""
    js_file=["""<script src="/static/js/jquery-1.8.1.min.js"></script>""","""<script src="/static/js/bui/bui.js"></script>""","""<script src="/static/js/view.js"></script>"""]
    css_file=[]
    html_footer=""


    if format_dic.has_key("columns"):
        #print(format_dic["columns"])
        columnstr=format_dic["columns"]
    else:
        sb_columnstr=[]
        for column in columns:
            sb_columnstr.append("{title: '%s', dataIndex: '%s'}"%(column,column))
        columnstr=",".join(sb_columnstr)
    sb_datastr=[]
    for row in rows:
        sb_row=[]
        for columni, column in enumerate(columns):
            sb_row.append("%s:'%s'"%(column,row[columni]))
        sb_datastr.append("{%s}"%(",".join(sb_row),))
    datastr = ",".join(sb_datastr)
    bui_static_grid_template = """
    <div id="page_{div_id}"></div>
        <script type="text/javascript">
                var Grid = BUI.Grid,
                Format=BUI.Grid.Format,
                Data = BUI.Data;
                var Grid = Grid,
              Store = Data.Store,
              Format=Grid.Format,
              columns = [{columns}],
               data=[{data}]
               {bui_style};

            var store = new Store({{
                data : data,
                autoLoad:true
                {store_style}
              }}),
              grid = new Grid.Grid({{
              render:'#page_{div_id}',
              columns : columns,

              store : store
              {grid_style}
            }});

            grid.render();
        </script>"""
    htmlstr=bui_static_grid_template.format(div_id=div_id,columns=columnstr,data=datastr,bui_style=format_dic.get("bui_style",""),store_style=format_dic.get("store_style",""),grid_style=format_dic.get("grid_style",""))
    return htmlstr,js_file,css_file,html_footer



def get_render_bar(percentlist=(30,60,80),hzstr=""):
    #statlist=("success","info","warning","important")
    #renerstr=[""]
    #for keyi,key in enumerate(percentlist):
    #    if keyi==0:
    #        renerstr.append("""
    if len(percentlist)<3:
        percentlist = (30, 60, 80)
    if percentlist[0]>percentlist[1]:
        formatchar = ">"
    else:
        formatchar = "<"
    renerstr="""
    ,renderer : function (value) {
        if(value {formatchar} %s){
                  return '<span class="label label-success">'+value+'{hzstr}</span>'
                }
        else if(value {formatchar} %s){
                  return '<span class="label label-info">'+value+'{hzstr}</span>'
                } 
        else if(value {formatchar} %s){
                  return '<span class="label label-warning ">'+value+'{hzstr}</span>'
                } 
        else {
                return '<span class="label label-important ">'+value+'{hzstr}</span>'
                }
     }     """%percentlist
    renerstr=renerstr.replace("{formatchar}",formatchar).replace("{hzstr}",hzstr)
    return renerstr


def get_render_text_alertwin(title,url,width=640,height=460,idstr="id"):
    onclickstr="""onclick = "alertWin(\\'{title}\\',\\'{url}'+record['{id}']+'\\',{width},{height});" """.format(
        title=title,url=url,width=width,height=height,id=idstr
    )

    renerstr="""
    ,renderer : function (value,record) {
    return '<a href="#" {onclickstr}><span class="letter-text"> '+value+'</span></a>'
     }     """

    return renerstr.replace("{onclickstr}",onclickstr)

def get_render_bar_alertwin(title,url,width=640,height=460,idstr="id",percentlist=(30,60,80)):
    #'cpu使用率','cpu_use',640,480,'id'
    #statlist=("success","info","warning","important")
    #renerstr=[""]
    #for keyi,key in enumerate(percentlist):
    #    if keyi==0:
    #        renerstr.append("""
    onclickstr="""onclick = "alertWin(\\'{title}\\',\\'{url}'+record['{id}']+'\\',{width},{height});" """.format(
        title=title,url=url,width=width,height=height,id=idstr
    )

    renerstr="""
    ,renderer : function (value,record) {
        if(value < %s){
                  return '<a href="#" {onclickstr}><span class="label label-success w60"  > '+value+'</span></a>'
                }
        else if(value < %s){
                  return '<a href="#" {onclickstr}><span class="label label-info w60">'+value+'</span></a>'
                } 
        else if(value < %s){
                  return '<a href="#" {onclickstr}><span class="label label-warning w60">'+value+'</span></a>'
                } 
        else {
                return '<a href="#" {onclickstr}><span class="label label-important w60">'+value+'</span></a>'
                }
     }     """%percentlist

    return renerstr.replace("{onclickstr}",onclickstr)