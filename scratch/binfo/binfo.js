#!/usr/bin/env phantomjs

var page = require('webpage').create(),
    system = require('system'),
    action = null,
    q = null;

var fs = require('fs');

//--------------------------------------------------------

if (system.args.length === 1) {
  console.log('Usage: binfo.js <some Query>');
  phantom.exit(1);
} else {
  q = system.args[1];
}

var genename = q; 

//--------------------------------------------------------

start = function () {
    console.log('ACTION: start');

    page.evaluate( function( ) {

    } )

    fs.write(genename + '.html', page.content, 'w');

    phantom.exit(); 
}

work = function () {
    if(action == null) {
        action = start;
    }

    action.call();
}

injectJQuery = function (callback) {
    page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", callback);
}

page.onLoadFinished = function(status) {
    if(status == 'success') {
        injectJQuery( work );

    } else {
        console.log('Connection failed.');
        phantom.exit();

    }   
}

page.onConsoleMessage = function(msg) { 
    console.log('PAGE: ' + msg);
};

page.onResourceReceived = function (response) {
  if(response.stage == "end")
    console.log('Response (#' + response.id + ', status ' + response.status + '"): ' + response.url);
}

page.onUrlChanged = function (url) {
    console.log("URL: " + url);
}

page.open('http://www.binfo.ncku.edu.tw/cgi-bin/gf.pl?genename=' + genename);

