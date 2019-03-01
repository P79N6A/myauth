    var dummy = {
        children: []
      };
      var tags = {
        page: {
          attrs: {
            viewtype: ["table", "line", "bar", "guage", "stack", "map","mix"]
          },
          children: ["connstr",
				"sqlstr",
				"viewtype",
				"width",
				"height",
				"pagesize",
				"chart_title",
				"chart_xtype",
				"chart_maptype",
				"chart_yaxis",
                "chart_ymin",
				"chart_group",
				"chart_datazoom",
				"chart_legendstyle",
				"css",
				"style",
				"table_addin",
                "tableformat",
				"formart",
				"html",
                'edittable_format',
              'tableheader','title','title2','rowstyle','divstyle','insertsql','updatesql','deletesql'
              ,'freezecolumns','columnfarmat','colnames','colmodel'
				]

        },
        debug: dummy,
        ajax: dummy,
        btnname: dummy,
        sqllog: dummy,
        sqlrole: dummy,
        reportview: dummy,
        para: {
          attrs: {
            name: null,
            type: ["string", "date","select","checkbox","radio"]
          },
          children: ["name",
			"type",
			"desc",
			"connstr",
			"sqlstr",
            "format",
			"item_text",
			"item_value",
			"onchange",
			"defaultvalue",
			"width",'hidden_parahtml',
			"style"]
        }, title: dummy, html: dummy
      };

      function completeAfter(cm, pred) {
        var cur = cm.getCursor();
        if (!pred || pred()) setTimeout(function() {
          if (!cm.state.completionActive)
            cm.showHint({completeSingle: false});
        }, 100);
        return CodeMirror.Pass;
      }

      function completeIfAfterLt(cm) {
        return completeAfter(cm, function() {
          var cur = cm.getCursor();
          return cm.getRange(CodeMirror.Pos(cur.line, cur.ch - 1), cur) == "<";
        });
      }

      function completeIfInTag(cm) {
        return completeAfter(cm, function() {
          var tok = cm.getTokenAt(cm.getCursor());
          if (tok.type == "string" && (!/['"]/.test(tok.string.charAt(tok.string.length - 1)) || tok.string.length == 1)) return false;
          var inner = CodeMirror.innerMode(cm.getMode(), tok.state).state;
          return inner.tagName;
        });
      }

      var editor = CodeMirror.fromTextArea(document.getElementById("content"), {
        mode: "xml",
        lineNumbers: true,
        extraKeys: {
          "'<'": completeAfter,
          "'/'": completeIfAfterLt,
          "' '": completeIfInTag,
          "'='": completeIfInTag,
          "Ctrl-Space": "autocomplete"
        },
        hintOptions: {schemaInfo: tags}
      });

