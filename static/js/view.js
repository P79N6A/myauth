/**
 * Created by admin on 2017/5/4.
 */

function alertWin(title, msg, w, h) {
            var Overlay = BUI.Overlay
            var dialog = new Overlay.Dialog({
                title: title,
                width: w,
                height: h,
            buttons:[],
             bodyContent:"<iframe src='" + msg + "'  width='100%' height='" + (h - 68) + "px' frameborder='0'/>",
                mask: true
            });
            dialog.show();
        };