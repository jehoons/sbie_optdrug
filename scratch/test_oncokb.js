#!/usr/bin/env phantomjs

var page = require('webpage').create(),
    system = require('system'),
    action = null,
    q = null;

var fs = require('fs')

//--------------------------------------------------------

// if (system.args.length === 1) {
//   console.log('Usage: google.js <some Query>');
//   phantom.exit(1);
// } else {
//   q = system.args[1];
// }

//--------------------------------------------------------

start = function () {
    console.log('ACTION: start');

    // page.evaluate( function( ) {    
    //     $('input[class="form-control ng-pristine ng-valid ng-empty ng-touched"]').val( 'APC' );
    //     button = $('button[class="btn btn-default"]')
    //     button.click(); 
    //     waitforload = true;
    // });

    // page.evaluate( function( ) {} )

    // fs.write('login.html', page.content, 'w');
    page.render('view_1.png');

    action = view_after_login;

    // phantom.exit(); 
}

view_after_login = function () {

    console.log('ACTION: view_after_login');
    page.render('view_2.png');

    phantom.exit();

}

//--------------------------------------------------------

work = function () {
    if(action == null) action = start;

    // console.log( "URL: " + page.url );
    // page.render('1.png')

    action.call();
}

injectJQuery = function (callback) {
    //  console.log('injecting JQuery');
    page.includeJs("http://ajax.googleapis.com/ajax/libs/jquery/1.6.1/jquery.min.js", callback);
}

page.onLoadFinished = function(status) {
//  console.log('Status: ' + status);
if(status == 'success') {
    // console.log('Connection success!');
    injectJQuery( work );

    // phantom.exit(); 
} else {
    console.log('Connection failed.');
    phantom.exit();
    }
}

page.onConsoleMessage = function(msg){ 
    console.log('PAGE: ' + msg);
};

page.onResourceReceived = function (response) {
  if(response.stage == "end")
    console.log('Response (#' + response.id + ', status ' + response.status + '"): ' + response.url);
}

page.onUrlChanged = function (url) {
    console.log("URL: " + url);
}

//--------------------------------------------------------

// page.open('http://oncokb.org/#/gene/CTNNB1');
page.open('http://oncokb.org/#/gene/APC');
