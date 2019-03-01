    var dummy = {
        children: []
      };
      var tags = {
          step: {
          attrs: {
            type: ["sql", "python"]
          },
          children: ["from_sqlstr",
              "except_db",
				"to_sqlstr",
				"result_check",
                "result_ok",
                "regcolumn", "reg", "reg2", "funcname",
                "to_sqlstr_header","to_sqlstr_footer","to_sqlstr_join",
              "to_action","child_sqlstr","child_server",

"except_db","para",

              "result_error"
				]
        },
          from_server: dummy, to_server: dummy, delaysecond: dummy, skiphour: dummy, skipday: dummy, success: dummy, tasktype: dummy, onerror: dummy,
          reportname: dummy, mailtitle: dummy, mailto: dummy, themecolor: dummy
          ,phone:dummy,toparty:dummy,agentdid:dummy,totag:dummy,msgtype:dummy
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

