/**
 * Created by parangsaraf on 3/21/17.
 */

function hide_panel(divId, glyphId) {
    if (!document.getElementById(divId)) {
        alert("Given Div Id : " + divId + " Doesn't Exist.");
        return
    }
    if (!document.getElementById(glyphId)) {
        alert("Given glyph Id : " + glyphId + " Doesn't Exist.");
        return
    }
    if (document.getElementById(glyphId).className == 'glyphicon glyphicon-minus') {
        document.getElementById(divId).style.display = 'none';
        document.getElementById(glyphId).className = 'glyphicon glyphicon-plus';
    }
    else {
        document.getElementById(divId).style.display = 'block';
        document.getElementById(glyphId).className = 'glyphicon glyphicon-minus';
    }
}