/*
	Author:			Hristofor Lukanov
	Description:	AJAX Interface
	========================================

	Example:
	----------------------------------------

	Ajax.setHeader( 'a', '1' );
	Ajax.setHeaders( { 'b': 1, 'c': 2 } );
	Ajax.setHeaders( {'b': null} ); // Remove header

	var Request = Ajax.GET( 'url' );
	var Request = Ajax.POST( 'url' );

	var Request = Ajax.POST( 'url', {
		'data': { 'a': 1, 'b': 2, 'c': 3 },
		'onload': function ( response ) {
			// response.text
			// response.xml
		},
		'onerror': function ( status, error ) { },
		'onfinish': function () { },
		'onstart': function () { },
		'headers': {
			'a': 'a value',
			'b': 'b value'
		},
		'form': 'form1', // name / ID
		'async': true
	} );

	Request.abort();
*/
var Ajax=function(){var m=["Microsoft.XMLHTTP","MSXML2.XMLHTTP","MSXML2.XMLHTTP.3.0"],o=m.length,k=null,q=null,r=function(){r=q?function(){return new k(q)}:function(){return new k};return r()},h=function(b,c){return Object.prototype.hasOwnProperty.call(b,c)},s=function(b){return"object"===typeof b&&b instanceof j},j=function(){},p={"Content-type":"application/x-www-form-urlencoded"},t=function(b,c){var a;if(0<c.keys.length){a=c.keys.shift();if(!h(b,a)||!s(b[a])||""==a)""==a&&(a=j.nextIndex(b)),b[a]=new j;j.push.call(b,a,t(b[a],c));return b}return encodeURIComponent(c.value)},u=function(b,c){var a,e="";for(a in b)h(b,a)&&("string"===typeof b[a]?e+=c.keys+(1<c.level?"%5B"+a+"%5D":a)+"="+b[a]+"&":s(b[a])&&(e+=u(b[a],{keys:c.keys+(0<c.level?"%5B"+a+"%5D":a),level:c.level+1})));return e},v=function(b,c,a){var e={onfinish:null,onstart:null,onerror:null,onload:null,async:!0},l=new j,f=r(),n={},i="",k,m,g,d,o=function(a,b,c){var d=b.length,e;if("undefined"===typeof l[a]||!s(l[a]))l[a]=new j;for(e=0;e<d;e++)b[e]=b[e].substring(1);j.push.call(l,a,t(l[a],{value:c.value,keys:b,c:a}))};for(d in p)h(p,d)&&(n[d]=p[d]);a||(a={});for(d in a)h(a,d)&&h(e,d)&&(e[d]=a[d]);"boolean"!==typeof e.async&&(e.async=!0);"function"!==typeof e.onfinish&&(e.onfinish=null);"function"!==typeof e.onerror&&(e.onerror=null);"function"!==typeof e.onstart&&(e.onstart=null);"function"!==typeof e.onload&&(e.onload=null);"object"!==typeof a.data&&(a.data={});"object"!==typeof a.headers&&(a.headers={});if(h(a,"headers"))for(d in a.headers)n[d]=a.headers[d];h(a,"form")&&(h(document.forms,a.form)?g=document.forms[a.form]:document.getElementById(a.form)&&(g=document.getElementById(a.form)));if(g){g=g.elements;i=g.length;for(d=0;d<i;d++)("checkbox"===g[d].type||"radio"===g[d].type)&&!g[d].checked||""==g[d].name||((k=g[d].name.match(/^([^\[]+)(?:\[.*?\])+.*?$/))?o(k[1],g[d].name.match(/\[([^\]]*)(?=\])/g),g[d]):l[g[d].name]=encodeURIComponent(g[d].value))}i=u(l,{keys:"",level:0});if(h(a,"data"))for(d in a.data)h(a.data,d)&&(i+=encodeURIComponent(d)+"="+encodeURIComponent(a.data[d])+"&");0<i.length&&"&"==i.charAt(i.length-1)&&(i=i.substring(0,i.length-1));"GET"==b&&0<i.length&&(c+=(-1<c.indexOf("?")?"&":"?")+i);f.onreadystatechange=function(){if(4==f.readyState||"complete"==f.readyState)200!=f.status||f.getResponseHeader("Error")?(m=f.getResponseHeader("Error")?decodeURIComponent(f.getResponseHeader("Error")):f.statusText,e.onerror&&e.onerror.call(f,f.status,decodeURIComponent(m))):h(a,"onload")&&a.onload.call(f,{text:f.responseText,xml:f.responseXML}),e.onfinish&&e.onfinish.call(f)};e.onstart&&e.onstart.call(f);f.open(b,c,e.async);for(d in n)h(n,d)&&"string"===typeof n[d]&&f.setRequestHeader(d,n[d]);f.send(i);return f};j.push=function(b,c){if(""===b)this[j.nextIndex(this)]=c;else return this[b]=c,this[b]};j.nextIndex=function(b){var c,a=-1;for(c in b)h(b,c)&&/^\d+$/.test(c)&&1*c>a&&(a=1*c);return a+1};if("undefined"!==typeof XMLHttpRequest)k=XMLHttpRequest;else for(k=ActiveXObject;o--;)try{new k(m[o]);q=m[o];break}catch(w){}return{POST:function(b,c){return v("POST",b,c)},GET:function(b,c){return v("GET",b,c)},setHeader:function(b,c){p[b]=c},setHeaders:function(b){for(var c in b)h(b,c)&&(p[c]=b[c])}}}();