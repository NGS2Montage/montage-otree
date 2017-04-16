
  var extremeX=450;
  var moveTo=0;

  var results = [];

  var containerScale;
  var figureScale;
  var backgroundScale;

  var whichFigureIsMoving = null;
  var offsetX = 0;
    
  var absoluteOffsetX;
  var minX;
  var maxX;

  var figureScaleRadius = 100; 
  var backgroundScaleRadius = 150; 


  function globalX(elem) {
    var l = elem.offsetLeft;
    while (elem = elem.offsetParent)
      l += elem.offsetLeft;
    return l;
  }  

  function setPositionX(elem, pixels) {
    if (elem.style.pixelLeft==undefined)
      elem.style.left = pixels + "px"; // Firefox
    else 
      elem.style.pixelLeft = pixels; // Others
  }
  
  function addEvent(evnt, elem, func) {
    if (elem.addEventListener)  // W3C DOM
      elem.addEventListener(evnt, func, false);
    else if (elem.attachEvent) // IE DOM
      elem.attachEvent("on"+evnt, function(a){a.currentTarget=elem;func(a);});
    else // Not much to do
      elem["on"+evnt] = func;
  }  

  function overlappingArea(centerSmall, centerBig) {
    var R = figureScaleRadius;
    var r = backgroundScaleRadius;
    var d = centerBig - centerSmall;
    var t1 = (d*d+r*r-R*R)/(2*d*r);
    var t2 = (d*d+R*R-r*r)/(2*d*R);
    var t3 = (-d+r+R)*(d+r-R)*(d-r+R)*(d+r+R);
    var area = r*r*Math.acos(t1) + R*R*Math.acos(t2) - Math.sqrt(t3)/2;
    return area;
  }

  function myMouseMove(e) {
    e.touches = [{clientX: e.clientX, clientY: e.clientY}];
    return myTouchMove(e);    
  }

  function myTouchMove(e) {
    if (whichFigureIsMoving != null) { 

      var positionX = e.touches[0].clientX;

      if (positionX < minX + offsetX)
        positionX = minX + offsetX;
      else if (positionX > maxX + offsetX)
        positionX = maxX + offsetX;

      setPositionX(whichFigureIsMoving, positionX - offsetX - absoluteOffsetX);

      calculateResults();

    }    
    return false;
  }

  function myMouseUp(e) {
    if (whichFigureIsMoving != null)
    whichFigureIsMoving = null;
    document.onmouseup = null;
    document.onmousemove = null;
    document.ontouchup = null;
    document.ontouchmove = null;
  }


  function myMouseDown(e) {
    if (e.offsetX == undefined)
      offsetX = e.layerX;
    else
      offsetX = e.offsetX;

    whichFigureIsMoving = e.currentTarget;

    absoluteOffsetX = globalX(containerScale); 
    minX = globalX(containerScale);
    maxX = minX + extremeX;
    
    addEvent('mouseup', document, myMouseUp);
    addEvent('mousemove', document, myMouseMove);
    addEvent('touchend', document, myMouseUp);
    addEvent('touchmove', document, myTouchMove);

    // So touchstart would work in Android browser
    if (navigator.userAgent.match(/Android/i) )
        e.preventDefault();
    // Prevent cursor to change (as if we where selecting text)
    return false;
  }

function calculateResults() {
      // Calculate overlapping
      var figureScaleCenter = globalX(whichFigureIsMoving) + figureScaleRadius;
      var backgroundScaleCenter = globalX(backgroundScale) + backgroundScaleRadius;
      var displacement;

      // Calcular porcentaje
      var percentage = 0;
      if (backgroundScaleCenter - figureScaleCenter > figureScaleRadius +  backgroundScaleRadius)
        percentage = 0;
      else if (backgroundScaleCenter - backgroundScaleRadius < figureScaleCenter - figureScaleRadius)
        percentage = 100;
      else {
        var area = overlappingArea(figureScaleCenter, backgroundScaleCenter);
        percentage = Math.round((area * 100)/(Math.PI*figureScaleRadius*figureScaleRadius));
      }
      
      if (whichFigureIsMoving.style.pixelLeft == undefined)
        // Firefox
        displacement = Math.round((parseInt(whichFigureIsMoving.style.left) - 200) / 2);
      else 
        // Others
        displacement = Math.round((whichFigureIsMoving.style.pixelLeft - 200) / 2); 

      results[whichFigureIsMoving.myScale][0].value = displacement;
      results[whichFigureIsMoving.myScale][1].value = percentage; 
}


  function setPositionForward(myScaleTo) {
    moveTo=20;
    setPositionTo(myScaleTo)
  }

  function setPositionRewind(myScaleTo) {
    moveTo=-20;
    setPositionTo(myScaleTo)
  }

  function setPositionPlay(myScaleTo) {
    moveTo=2;
    setPositionTo(myScaleTo)
  }

  function setPositionReverse(myScaleTo) {
    moveTo=-2;
    setPositionTo(myScaleTo)
  }

  function setPositionTo(myScaleTo) {
    var positionX = 0;
    figureScale = document.getElementById('mySlider'+myScaleTo);
    whichFigureIsMoving = figureScale;

    if (figureScale.style.pixelLeft==undefined)
      positionX = parseInt(figureScale.style.left); // Firefox
    else 
      positionX = figureScale.style.pixelLeft; // Others

    positionX = positionX + moveTo;

    if (positionX < 0)
      positionX = 0;
    else if (positionX > extremeX)
      positionX = extremeX;

    if (figureScale.style.pixelLeft==undefined)
      figureScale.style.left = positionX + "px"; // Firefox
    else 
      figureScale.style.pixelLeft = positionX; // Others

    calculateResults();

    myMouseUp(figureScale);

  }


function difi(myScale, myGroup, mySelf, myColor, myDistance, myVisible) {
  if (typeof(myScale)=="undefined") myScale="Scale";
  if (typeof(myGroup)=="undefined") myGroup="Group";
  if (typeof(mySelf)=="undefined") mySelf="Me";
  if (typeof(myColor)=="undefined") myColor="grey";
  if (typeof(myDistance)=="undefined") myDistance="-50";
  if (typeof(myVisible)=="undefined") myVisible="true";
  myColor = myColor.toLowerCase();
  myDistance = parseInt(myDistance);
  if (myDistance>125) myDistance=125;
  if (myDistance<-100) myDistance=-100;


  var urlMe = '/static/images/me.png';
  
  // Change png for a gif to fix IE6 transparency issues
  if (/\bMSIE 6/.test(navigator.userAgent) && !window.opera) urlMe = '/static/images/me.gif';

  var urlThem = '/static/images/them_' + myColor + '.png';

  document.write('<div style="width:730px;height:380px;padding:15px;border:1px solid black">'+

  '<div id="myContainer'+myScale+'" style="width:700px;height:350px;font-family:Arial;font-weight:bold;font-size:16px;">' +

  '<div id="myControl'+myScale+'" style="width:700px;height:50px;left:0px;top:0px;border:0px;position:relative;">' +
  '<table width="700px" height="50px" border="0" cellspacing="0" cellpadding="0"><tr>' +
  '<td valign="top" align="right" width="100px"><image src="/static/images/go_rewind.png" width="100" height="30" border="0" style="cursor:pointer" onClick=setPositionRewind("'+myScale+'")></td>' +
  '<td valign="top" align="right" width="100px"><image src="/static/images/go_reverse.png" width="100" height="30" border="0" style="cursor:pointer" onClick=setPositionReverse("'+myScale+'")></td>' +
  '<td valign="top" align="right" width="100px"><image src="/static/images/go_play.png" width="100" height="30" border="0" style="cursor:pointer" onClick=setPositionPlay("'+myScale+'")></td>' +
  '<td valign="top" align="left" width="100px"><image src="/static/images/go_forward.png" width="100" height="30" border="0" style="cursor:pointer" onClick=setPositionForward("'+myScale+'")></td>' +
  '<td valign="middle" align="center" width="300px">'+myGroup+'</td>' +
  '</tr></table></div>' +

  '<div id="mySlider'+myScale+'" name="mySlider'+myScale+'" style="width:200px;height:200px; ' +
  '     left:' + (200+(2*myDistance)) + 'px;top:50px;float:left;position:relative;z-index:92; text-align:center;cursor:move;">' +

  '   <table width="200px" height="200px" border="0" cellspacing="0" cellpadding="0" ' +
  '          background="'+urlMe+'" ' + 
  '          onmousedown="if (event.preventDefault) event.preventDefault()"' +
  '          ontouchmove="if (event.preventDefault) event.preventDefault()">' +
  '   <tr><td valign="middle" align="center">'+mySelf+'</td></tr></table>' +
  '</div>' +

  '<div id="myDestination'+myScale+'" name="myDestination'+myScale+'" ' +
  '        style="width:300px;height:300px;' +
  '               left:200px;top:0px;float:left;position:relative;z-index:91;">' +
  '<table width="300px" height="300px" border="0" cellspacing="0" cellpadding="0">' +
  '<tr><td valign="middle" align="center" width="300px" height="300px"><img src="'+urlThem+'"/></td></tr>' +
  '</table>' +
  '</div>' +

  '</div></div>');


  figureScale = document.getElementById('mySlider'+myScale);
  figureScale['myScale'] = myScale;

  containerScale = document.getElementById('myContainer'+myScale);
  backgroundScale = document.getElementById('myDestination'+myScale);

  if (myVisible == "false") document.getElementById('distance' + myScale).style.visibility = 'hidden';
  document.getElementById('distance' + myScale).readOnly = true;

  if (myVisible == "false") document.getElementById('overlap' + myScale).style.visibility = 'hidden';
  document.getElementById('overlap' + myScale).readOnly = true;

  results[myScale] = [ document.getElementById('distance' + myScale), 
                       document.getElementById('overlap' + myScale) ];


  // Prevent selecting text in IE
  document.onselectstart = function() { return false; }

  addEvent('mousedown', figureScale, myMouseDown);
  addEvent('touchstart', figureScale, myMouseDown);

}

