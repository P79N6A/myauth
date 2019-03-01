# -*- coding:utf-8 -*-
#!/usr/bin/env python
from __future__ import unicode_literals


import htmlstr_

class form_():
    def __init__(self):
        self.JSDICT={} #Calendar
        self.Js_header =["""<script src="/static/js/jquery-1.8.1.min.js"></script>""",
                   """<script src="/static/js/bui/bui.js"></script>"""]
        pass


    def make_desc(self,desc,maxlength=20):
        if len(desc)>maxlength:
            desc = '&nbsp;<a href="#" class="icon-question-sign tipsuccess" title="%s"></a>' % (desc,)
        else:
            desc = '<span class="auxiliary-text" >%s</span>' % (desc,)
        return desc

    '''def makecode(self, pagei, pageDetail):
        codetype = pageDetail["codetype"]
        code = pageDetail["code"].replace("{![CDATA[", "<![CDATA[").replace("]]}", "]]>")

        codetext = {"xml": "text/xml", "sql": "text/x-mysql"}.get(codetype, "text/x-mysql")
        spagei = str(pagei)
        builder_html = []
        # builder=[]
        if len(pageDetail["title"]) > 0:
            builder_html.append(u'<div>%s</div>' % pageDetail["title"])
        builder_html.append(
            htmlstr_.html_codejs.replace('{pagei}', spagei).replace('{code}', code).replace('{codetype}', codetext))
        #JSDICT['js_code' + codetype] = True
        shtml = "\n".join(builder_html)  # +"\n".join(builder)
        return shtml'''

    def make_form_head(self,spagei=0,method="post",action=""):
        return """ <form  id="form_%s" class="form-horizontal"  method="%s" action="%s">"""%(spagei,method,action)

    def make_form_foot(self,spagei,btnlist=[{"btntype":"submit","btnclass":"button-primary","id":"btnsave","title":"保存","action":""}]):
        sb_btn=[]
        sb_btn_script=[]
        sb_html = []
        for btn in btnlist:
            btntype = btn.get("type", "submit")
            btnclass=btn.get("btnclass", "button-primary")
            id=btn.get("id", "btnsave")
            title = btn.get("title", "保存")
            action = btn.get("action", "")
            sb_btn.append('<button type="{btntype}" class="button {btnclass}" id="{id}">{title}</button>'.format(
                btntype=btntype,btnclass=btnclass,id=id,title=title
            ))
            if action=="onclick_action":
                sb_btn_script.append("""
                 $('#{id}').on('click',function(){{
        var idField = form.getField('hid_button');
        idField.set('value','{id}');
        form.submit();
      }});
             """.format(id=btn.get("id","")))


        if len(btnlist)>0:
            sb_html.append("""<div class="row form-actions actions-bar">
            <div class="span13 offset3 ">
              %s%s
            </div>
            </div>
            </form>"""%(self.make_hidden("hid_button",""),"\n".join(sb_btn)))
        sb_html.append('<script type="text/javascript">')
        if self.JSDICT.has_key("Calendar"):
            sb_html.append('''var Calendar = BUI.Calendar,
                  Form = BUI.Form;
                  var datepicker = new Calendar.DatePicker({
                    trigger:'.calendar',
                    autoRender : true });
                    ''')
        sb_html.append('''
            BUI.use('common/page'); //页面链接跳转
            BUI.use('bui/form',function (Form) {
              var form = new Form.HForm({
                srcNode : '#form_%s'
              });
              form.render();
              %s
            });
                </script>''' % (spagei, "\n".join(sb_btn_script)))
        return "\n".join(sb_html)

    """def make_form_script(self,spagei=0,formscript=""):
        sb_js=[]
        sb_js.append('<script type="text/javascript">')
        if self.JSDICT.has_key("Calendar"):
            sb_js.append('''var Calendar = BUI.Calendar,
          Form = BUI.Form;
          var datepicker = new Calendar.DatePicker({
            trigger:'.calendar',
            autoRender : true });
            ''')
        sb_js.append('''
    BUI.use('common/page'); //页面链接跳转
    BUI.use('bui/form',function (Form) {
      var form = new Form.HForm({
        srcNode : '#form_%s'
      });
 
      form.render();
      %s
    });
        </script>'''%(spagei,formscript))
        return "\n".join(sb_js)"""

    '''def make_input_dic(self,dic_input):
        shtml=""" <div class="row"><div class="control-group {spanclass}">
            <label class="control-label">{title}：</label>
            <div class="controls">
              <input name="{paraid}" id="{paraid}" type="text" data-tip='{datatip}'  class="{inputclass} control-text"  data-rules="{datarules}">{defaultvalue}</input>{desc}
            </div>
          </div></div>""".format(dic_input)
        return shtml'''



    def make_input(self,paraid,title="",defaultvalue="",spanclass="span8",datatip="",inputclass="",datarules="",desc=""):
        desc = self.make_desc(desc)
        shtml=""" <div class="row"><div class="control-group {spanclass}">
            <label class="control-label">{title}：</label>
            <div class="controls">
              <input name="{paraid}" id="{paraid}" type="text" data-tip='{datatip}'  class="{inputclass} control-text"  data-rules="{datarules}" value="{defaultvalue}"/>&nbsp;{desc}
            </div>
          </div></div>""".format(spanclass=spanclass,title=title,paraid=paraid,datatip=datatip,inputclass=inputclass,datarules=datarules,defaultvalue=defaultvalue,desc=desc)
        return shtml

    def make_textarea(self,paraid,title="",defaultvalue="",spanclass="span8",datatip="input-normal",inputclass="",datarules="",desc=""):
        desc = self.make_desc(desc)
        shtml = """ <div class="row"><div class="control-group {spanclass}">
                    <label class="control-label">{title}：</label>
                     <div class="controls  control-row4">
                     <textarea name="{paraid}" id="{paraid}" class="{inputclass}">{defaultvalue}</textarea>{desc}
                    </div>
                  </div></div>""".format(spanclass=spanclass, title=title, paraid=paraid, datatip=datatip,
                                         inputclass=inputclass, datarules=datarules, defaultvalue=defaultvalue,
                                         desc=desc)
        return shtml

    def makecode_sql(self,paraid,title="",defaultvalue="",spanclass="span8",datatip="input-normal",inputclass="",datarules="",desc=""):
        defaultvalue = defaultvalue.replace("{![CDATA[", "<![CDATA[").replace("]]}", "]]>")
        #codetype = {"xml": "text/xml", "sql": "text/x-mysql"}.get(datarules, "text/x-mysql")
        desc = self.make_desc(desc)
        shtml = u"""
                  <div class="row"><div class="control-group {spanclass}">
                    <label class="control-label">{title}：</label>
                     <div >
                     <textarea name="{paraid}" id="{paraid}"  >{defaultvalue}</textarea>{desc}
                    </div>
                  </div></div>
                  
                     <script type="text/javascript">
        jQuery(function($){{window.editor = CodeMirror.fromTextArea(document.getElementById('{paraid}'), {{
            mode: "text/x-mysql",
            indentWithTabs: true,
            smartIndent: true,
            lineNumbers: true,
            matchBrackets : true,
            autofocus: true,
            extraKeys: {{"Tab": "autocomplete"}},
            hintOptions: {{tables: {{
              usersList: {{name: null, score: null, birthDate: null}},
              countries: {{name: null, population: null, size: null}}
                }} }}
          }});
        	}});
            </script>
                """.format(spanclass=spanclass, title=title, paraid=paraid, datatip=datatip,
                                         inputclass=inputclass, defaultvalue=defaultvalue,
                                         desc=desc,datarules=datarules)
        self.Js_header.append("""<link rel="stylesheet" href="/static/code/css/codemirror.css" />""")
        self.Js_header.append("""<script src="/static/code/js/codemirror.js"> </script>""")
        self.Js_header.append("""<script src="/static/code/js/sql.js"></script>""")
        self.Js_header.append("""<link rel="stylesheet" href="/static/code/css/show-hint.css" />""")
        self.Js_header.append("""<script src="/static/code/js/show-hint.js"> </script>""")
        self.Js_header.append("""<script src="/static/code/js/sql-hint.js"></script>""")
        return shtml


    def make_hidden(self, paraid,  defaultvalue=""):
        shtml = """ <input type="hidden" id="{paraid}" value="{defaultvalue}" name="{paraid}" /> 
""".format(paraid=paraid, defaultvalue=defaultvalue)
        return shtml

    def make_lable(self, title, value=""):
        shtml = """<div class="control-group ">
          <label class="control-label">{title}：</label>
          <div class="controls">
          <span class="control-text">{value}</span>
          </div>
        </div>""".format(title=title, value=value)
        return shtml

    #form_.make_select(self.name,self.title, newvalue,self.style.get("div-class",""), "input-normal", self.style.get("data-tip",""),self.style.get("input-class",""), rowlist)

    def make_select(self,paraid,title="",defaultvalue="",spanclass="span8",inputclass="",onchangestr="",rows=[],desc=""):
        desc = self.make_desc(desc)
        itemlist=[]
        if len(defaultvalue)==0 and len(rows)>0:
            defaultvalue=rows[0][1]
        for row in rows:
            itemlist.append("{text:'%s',value:'%s'}"%row)
        valuestr=','.join(itemlist)
        #valuestr = '''{text:'选项1',value:'a'},{text:'选项2',value:'b'},{text:'选项3',value:'c'}'''
        #onchangestr="""alert(ev.item);"""
        shtml=""" 
<div class="row"><div class="control-group {spanclass}">
            <label class="control-label">{title}：</label>
            <div class="controls">
              <span id="s_{paraid}" class="{inputclass}"><input type="hidden" id="{paraid}" value="{defaultvalue}" name="{paraid}" /></span> &nbsp;{desc}
            </div>
</div></div>
<script type="text/javascript">
    var Select = BUI.Select
    var items = [{valuestr}],
        select = new Select.Select({{  
          render:'#s_{paraid}',
          valueField:'#{paraid}',
          items:items
        }});
    select.render();
    select.on('change', function(ev){{
      {onchangestr}
    }});
  </script>
""".format(spanclass=spanclass,title=title,paraid=paraid,onchangestr=onchangestr,valuestr=valuestr,inputclass=inputclass,defaultvalue=defaultvalue,desc=desc)
        return shtml


    def make_multi_select(self,paraid,title="",defaultvalue="",spanclass="span8",inputclass="",onchangestr="",rows=[],desc=""):
        desc = self.make_desc(desc)
        itemlist=[]
        if len(defaultvalue)==0 and len(rows)>0:
            defaultvalue=rows[0][1]
        for row in rows:
            itemlist.append("{text:'%s',value:'%s'}"%row)
        valuestr=','.join(itemlist)
        #valuestr = '''{text:'选项1',value:'a'},{text:'选项2',value:'b'},{text:'选项3',value:'c'}'''
        #onchangestr="""alert(ev.item);"""
        shtml=""" 
<div class="row"><div class="control-group {spanclass}">
            <label class="control-label">{title}：</label>
            <div class="controls">
              <span id="s_{paraid}" class="{inputclass}"><input type="hidden" id="{paraid}" value="{defaultvalue}" name="{paraid}" /></span> &nbsp;{desc}
            </div>
</div></div>
<script type="text/javascript">
    var Select = BUI.Select
    var items = [{valuestr}],
        select = new Select.Select({{  
          render:'#s_{paraid}',
          valueField:'#{paraid}',
          items:items,
          multipleSelect:true
        }});
    select.render();
    select.on('change', function(ev){{
      {onchangestr}
    }});
  </script>
""".format(spanclass=spanclass,title=title,paraid=paraid,onchangestr=onchangestr,valuestr=valuestr,inputclass=inputclass,defaultvalue=defaultvalue,desc=desc)
        return shtml



    def make_sugget(self,paraid,rowstr,title="",defaultvalue="",spanclass="span8",datatip="",datarules="",desc=""):
        shtml="""
        <div id="%s"></div>
            <script type="text/javascript"> 
            BUI.setDebug(true);     
                var Select = BUI.Select   
                var suggest = new Select.Suggest({
                   render:'#%s',
                   name:'suggest',
                   data:[%s]
                });
                suggest.render();  
              </script>"""%(paraid,paraid,rowstr)
              #(self.make_input(paraid,title,defaultvalue,spanclass,datatip,datarules,desc),paraid,rowstr)
        return shtml
