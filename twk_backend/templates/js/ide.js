var BASE_URL = localStorageGetItem("baseUrl") || "{{ judge0_api_url }}";
var SUBMISSION_CHECK_TIMEOUT = 10; // in ms
var WAIT = localStorageGetItem("wait") || false;
var sourceEditor, inputEditor, outputEditor;
var $insertTemplateBtn, $navBtn, $selectTaskBtn, $selectLanguageBtn, $runBtn, $submitBtn, $saveBtn, $chatBtn, $vimCheckBox;
var $statusLine, $emptyIndicator;
var judge = 0; 

function getIdFromURI() {
  return location.search.substr(1).trim();
}

function updateEmptyIndicator() {
  if (outputEditor.getValue() == "") {
    $emptyIndicator.html("empty");
  } else {
    $emptyIndicator.html("");
  }
}

function handleError(jqXHR, textStatus, errorThrown) {
  outputEditor.setValue(JSON.stringify(jqXHR, null, 4));
  $statusLine.html(`${jqXHR.statusText} (${jqXHR.status})`);
}

function handleRunError(jqXHR, textStatus, errorThrown) {
  handleError(jqXHR, textStatus, errorThrown);
  $runBtn.button("reset");
  updateEmptyIndicator();

}
function handleSubmitError(jqXHR, textStatus, errorThrown) {
  handleError(jqXHR, textStatus, errorThrown);
  $submitBtn.button("reset");
  updateEmptyIndicator();
}

function handleSubmit(data){
  // var status = data.status;
  var stdout = decodeURIComponent(escape(atob(data.stdout || "")));
  var stderr = decodeURIComponent(escape(atob(data.stderr || "")));

  var message = decodeURIComponent(escape(atob(data.message || "")));
  var time = (data.time === null ? "-" : data.time + "s");
  var memory = (data.memory === null ? "-" : data.memory + "KB");

  $statusLine.html(`${status.description}, ${time}, ${memory}`);

  // if (status.id == 6) {
  //   stdout = compile_output;
  // } else if (status.id == 13) {
  //   stdout = message;
  // } else if (status.id != 3 && stderr != "") { // If status is not "Accepted", merge stdout and stderr
  //   stdout += (stdout == "" ? "" : "\n") + stderr;
  // }

  outputEditor.setValue(stdout);

  updateEmptyIndicator();
  $submitBtn.button("reset");
}

function handleResult(data) {
  var status = data.status;
  var stdout = decodeURIComponent(escape(atob(data.stdout || "")));
  var stderr = decodeURIComponent(escape(atob(data.stderr || "")));
  var compile_output = decodeURIComponent(escape(atob(data.compile_output || "")));
  var message = decodeURIComponent(escape(atob(data.message || "")));
  var time = (data.time === null ? "-" : data.time + "s");
  var memory = (data.memory === null ? "-" : data.memory + "KB");

  $statusLine.html(`${status.description}, ${time}, ${memory}`);

  if (status.id == 6) {
    stdout = compile_output;
  } else if (status.id == 13) {
    stdout = message;
  } else if (status.id != 3 && stderr != "") { // If status is not "Accepted", merge stdout and stderr
    stdout += (stdout == "" ? "" : "\n") + stderr;
  }

  outputEditor.setValue(stdout);

  updateEmptyIndicator();
  $runBtn.button("reset");
}

function toggleVim() {
  var keyMap = vimCheckBox.checked ? "vim" : "default";
  localStorageSetItem("keyMap", keyMap);
  sourceEditor.setOption("keyMap", keyMap);
  focusAndSetCursorAtTheEnd();
}

function navBar() {
  if(document.getElementById("mySidenav").style.width == "0") {
    openNav();
  } else {
    closeNav();
  }
}

function openNav() {
  document.getElementById("mySidenav").style.width = "250px";

}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";

}

function send_message(user, id) {
  console.log("1231312312312421412421");
  var data = {
    user: user,
    msg: `The home work is in {{twk_url}}/templates/ide.html#${id}` 
  }
  
  $.ajax({
    url: `{{twk_url}}/send_msg/`,
    type: "POST",
    async: true,
    headers: {
      "Accept": "application/json"
    },
    data: JSON.stringify(data),
    success: function(data, textStatus, jqXHR) {
      console.log(data);
    }
  });
}

function run() {
  if (sourceEditor.getValue().trim() == "") {
    alert("Source code can't be empty.");
    return;
  } else {
    $runBtn.button("loading");
  }

  var sourceValue = btoa(unescape(encodeURIComponent(sourceEditor.getValue())));
  var inputValue = btoa(unescape(encodeURIComponent(inputEditor.getValue())));
  var languageId = $selectLanguageBtn.val();
  var data = {
    source_code: sourceValue,
    language_id: languageId,
    stdin: inputValue
  };

  $.ajax({
    url: BASE_URL + `/submissions?base64_encoded=true&wait=${WAIT}`,
    type: "POST",
    async: true,
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function (data, textStatus, jqXHR) {
      console.log(`Your submission token is: ${data.token}`);
      if (WAIT == true) {
        handleResult(data);
      } else {
        setTimeout(fetchSubmission.bind(null, data.token), SUBMISSION_CHECK_TIMEOUT);
      }
    },
    error: handleRunError
  });
}

function revise(id, console, error_text) {
  
  var id = id;
  var console = console;
  var error_text= error_text;
  var data = {
    id: id,
    console:console,
    error_text:error_text,
  }
  $.ajax({
    url:`{{twk_url}}/revise_hw/`,
    type: "POST",
    async: true,
    data:JSON.stringify(data),
    
    success: function(data, textStatus, jqXHR) {
      console.log("success");
    },
    error:handleRunError
  });

}


function submit() {
  if (sourceEditor.getValue().trim() == "") {
    alert("Source code can't be empty.");
    return;
  } else {
    $submitBtn.button("loading");
  }
  console.log($selectTaskBtn.val());
  var sourceValue = btoa(unescape(encodeURIComponent(sourceEditor.getValue())));
  var languageId = $selectLanguageBtn.val();
  var assignmentId = $selectTaskBtn.val();
  var data = {
    source_code: sourceValue,
    language_id: languageId,  
    assignment_id: assignmentId
    
  };

  $.ajax({
    url:`{{twk_url}}/submit_hw/`,
    type: "POST",
    async: true,
    headers: {
      "Accept":"application/json",
    //  'X-CSRFToken': $('meta[name="token"]').attr('ontent')
    },
    data: data,
    success: function(data, textStatus, jqXHR) {
      send_message('hsunyuan', data.homework_id);
      console.log(`Your submission token is: ${data.description}`);
      alert(`${data.description}`); 
      //outputEditor.setValue(`id : ${data.id} \ndescription : ${data.description}` );
      $submitBtn.button("reset");
    },
    error:handleError
  });
}

function fetchSubmit(submission_token) {
  $.ajax({
    url:"{{twk_url}}/submissions/" + submission_token + "?base64_encoded=true",
    type: "GET",
    async: true,
    success: function (data, textStatus, jqXHR) {
      if (data.status.id <= 2) { // In Queue or Processing
        setTimeout(fetchSubmit.bind(null, submission_token), SUBMISSION_CHECK_TIMEOUT);
        return;
      }
      handleResult(data);
    },
    error: handleRunError
  });
}


function fetchSubmission(submission_token) {
  $.ajax({
    url: BASE_URL + "/submissions/" + submission_token + "?base64_encoded=true",
    type: "GET",
    async: true,
    success: function (data, textStatus, jqXHR) {
      if (data.status.id <= 2) { // In Queue or Processing
        setTimeout(fetchSubmission.bind(null, submission_token), SUBMISSION_CHECK_TIMEOUT);
        return;
      }
      handleResult(data);
    },
    error: handleRunError
  });
}

function save() {
  var content = JSON.stringify({
    source_code: btoa(unescape(encodeURIComponent(sourceEditor.getValue()))),
    stdin: btoa(unescape(encodeURIComponent(inputEditor.getValue()))),
    language_id: $selectLanguageBtn.val(),
        // task_id:$selectTaskBtn.val()
  });
  var filename = $selectTaskBtn.val();
  var data = {
    content: content,
    filename: filename
  };

  $saveBtn.button("loading");
  $.ajax({
    url: "{{ twk_url }}/save_hw/",
    type: "POST",
    async: true,
    headers: {
      "Accept":"application/json"
    },
    data: data,
    success: function (data, textStatus, jqXHR) {
      $saveBtn.button("reset");
      if (getIdFromURI() != data["long"]) {
        window.history.replaceState(null, null, location.origin + location.pathname + "?" + data["long"]);
      }
    },
    error: function (jqXHR, textStatus, errorThrown) {
      handleError(jqXHR, textStatus, errorThrown);
      $saveBtn.button("reset");
    }
  });
}

function get_code(id) {
  
  console.log("call get_code api with id" + id)
  $.ajax({
    url: `{{twk_url}}/get_code/${id}`,
    type: "GET",
    async:true,
    success: function (data, textStatus, jqXHR) {
      sourceEditor.setValue(decodeURIComponent(escape(atob(data["source_code"] || ""))));
      inputEditor.setValue("");
      $selectLanguageBtn[0].value = data["language_id"];
      // $selectTaskBtn[0].value = data["task_id"];
      setEditorMode();
      focusAndSetCursorAtTheEnd();
      sourceEditor.readOnly = true;
    },
    error: function (jqXHR, textStatus, errorThrown) {
      sourceEditor.setValue("Code not found!");
    }
  });
}


function loadSavedSource() {
  $.ajax({
    url: "{{ twk_url }}/load_hw/",
    type: "POST",
    headers: {
      "Accept":"application/json"
    },
    data:{'filename':$selectTaskBtn.val()},
    success: function (data, textStatus, jqXHR) {
      sourceEditor.setValue(decodeURIComponent(escape(atob(data["source_code"] || ""))));
      inputEditor.setValue(decodeURIComponent(escape(atob(data["stdin"] || ""))));
      $selectLanguageBtn[0].value = data["language_id"];
      // $selectTaskBtn[0].value = data["task_id"];
      setEditorMode();
      focusAndSetCursorAtTheEnd();
    },
    error: function (jqXHR, textStatus, errorThrown) {
      // alert("Code not found!");
      window.history.replaceState(null, null, location.origin + location.pathname);
      //loadRandomLanguage();
      insertTemplate();
    }
  });
}

function setEditorMode() {
  sourceEditor.setOption("mode", $selectLanguageBtn.find(":selected").attr("mode"));
}

function focusAndSetCursorAtTheEnd() {
  sourceEditor.focus();
  sourceEditor.setCursor(sourceEditor.lineCount(), 0);
}

function insertTemplate() {
  var value = parseInt($selectLanguageBtn.val());
  sourceEditor.setValue(sources[value]);
  focusAndSetCursorAtTheEnd();
  sourceEditor.markClean();
}

function loadRandomLanguage() {
  var randomChildIndex = Math.floor(Math.random() * $selectLanguageBtn[0].length);
  $selectLanguageBtn[0][randomChildIndex].selected = true;
  setEditorMode();
  insertTemplate();
}

function loadCLanguage() {
  var gcc_7_2_0_Index = 3;
  $selectLanguageBtn[0][gcc_7_2_0_Index].selected = true;
  setEditorMode();
  insertTemplate();
}

function initializeElements() {
  $selectLanguageBtn = $("#selectLanguageBtn");
  $selectTaskBtn = $("#selectTaskBtn");
  $insertTemplateBtn = $("#insertTemplateBtn");
  $runBtn = $("#runBtn");
  $submitBtn = $("#submitBtn");
  $saveBtn = $("#saveBtn");
  $chatBtn = $('#chatBtn');
  $navBtn = $('#navBtn');
  $vimCheckBox = $("#vimCheckBox");
  $emptyIndicator = $("#emptyIndicator");
  $statusLine = $("#statusLine");
  $loadBtn = $('#loadBtn');
}

function localStorageSetItem(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch (ignorable) {}
}

function localStorageGetItem(key) {
  try {
    return localStorage.getItem(key);
  } catch (ignorable) {
    return null;
  }
}

$(document).ready(function () {
  console.log("Hey, TWKIDE is based on judge0 ide, an open-sourced: https://github.com/ 0/ide. Have fun!");

  initializeElements();

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  });


  if(location.hash.length > 1 && !isNaN(location.hash.slice(1))) {
    judge = 1;
    console.log("aaa");
    get_code(location.hash.slice(1));
   
  } else {
    judge = 0;
  }

  if(judge === 0) {
    console.log("not judge"+judge);
    document.getElementById("judging").style.visibility = "hidden";
  sourceEditor = CodeMirror(document.getElementById("sourceEditor"), {
    lineNumbers: true,
    indentUnit: 4,
    indentWithTabs: true,
    showCursorWhenSelecting: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    keyMap: localStorageGetItem("keyMap") || "default",
    extraKeys: {
      "Tab": function (cm) {
        var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
        cm.replaceSelection(spaces);
      }
    }
  });
} else {
  HashHandler();
  console.log("judging");
  document.getElementById("judging").style.visibility = "visible";
  sourceEditor = CodeMirror(document.getElementById("sourceEditor"), {
    readOnly:true,
    lineNumbers: true,
    indentUnit: 4,
    indentWithTabs: true,
    showCursorWhenSelecting: true,
    matchBrackets: true,
    autoCloseBrackets: true,
    keyMap: localStorageGetItem("keyMap") || "default",
    extraKeys: {
      "Tab": function (cm) {
        var spaces = Array(cm.getOption("indentUnit") + 1).join(" ");
        cm.replaceSelection(spaces);
      }
    }
  });
}

  inputEditor = CodeMirror(document.getElementById("inputEditor"), {
    lineNumbers: true,
    mode: "plain"
  });
  outputEditor = CodeMirror(document.getElementById("outputEditor"), {
    readOnly: true,
    mode: "plain"
  });

  $vimCheckBox.prop("checked", localStorageGetItem("keyMap") == "vim").change();

//  if (getIdFromURI()) {
//    loadSavedSource();
//  } else {
    //loadRandomLanguage();
    loadCLanguage();

    
//  }
  // send_message();
  
  $(".trigger_popup_fricc").click(function(){
    $('.hover_bkgr_fricc').show();
 });
//  $('.hover_bkgr_fricc').click(function(){
//      $('.hover_bkgr_fricc').hide();
//  });
 $('.popupCloseButton').click(function(){
     $('.hover_bkgr_fricc').hide();
 });

  



// Alert some text if there has been changes to the anchor part
function HashHandler() {
  console.log(location.hash.slice(1));
  if(judge == 1) {
    get_code(location.hash.slice(1));
    $("#chatBtn").css("display", "none");
    $("#loadBtn").css("display", "none");
    $("#saveBtn").css("display", "none");
    $("#submitBtn").css("display", "none");
    $("#downloadSourceBtn").css("display", "none");
    $(".toggle").css("display", "none");
    $("#true").css("display", "inline-flex");
    $("#false").css("display", "inline-flex");
  }
  


}

window.addEventListener("hashchange", HashHandler, false);

  
$("#true").click(function (e) {
  revise(id = location.hash.slice(1), console="True",error_text="");
  window.location = "{{ twk_url }}";
  window.alert("submit success");
});

$("#false").click(function (e) {
  revise(id = location.hash.slice(1), console="False",error_text=inputEditor.getValue());
  window.location = "{{ twk_url }}";
  window.alert("submit success");
});



  $selectLanguageBtn.change(function (e) {
    if (sourceEditor.isClean()) {
      loadSavedSource();
    }
    setEditorMode();
  });

  $selectTaskBtn.change(function (e) {

      loadSavedSource();


    setEditorMode();
  })

  $insertTemplateBtn.click(function (e) {
    if (!sourceEditor.isClean() && confirm("Are you sure? Your current changes will be lost.")) {
      setEditorMode();
      insertTemplate();
    }
  });

  $("body").keydown(function (e) {
    var keyCode = e.keyCode || e.which;
    if (keyCode == 120) { // F9
      e.preventDefault();
      run();
    } else if (keyCode == 119) { // F8
      e.preventDefault();
      var url = prompt("Enter URL of Judge0 API:", BASE_URL).trim();
      if (url != "") {
        BASE_URL = url;
        localStorageSetItem("baseUrl", BASE_URL);
      }
    } else if (keyCode == 118) { // F7
      e.preventDefault();
      WAIT = !WAIT;
      localStorageSetItem("wait", WAIT);
      alert(`Submission wait is ${WAIT ? "ON. Enjoy" : "OFF"}.`);
    } else if ((event.ctrlKey || event.metaKey) && keyCode == 83) { // Ctrl+S
      e.preventDefault();
      save();
    } else if ((event.ctrlKey || event.metaKey) && keyCode == 13) { // Ctrl+Enter
      e.preventDefault();
      submit();
    }
  });


  function show_frame() {
    if (document.getElementById("myiframe").style.display == "block")
      document.getElementById("myiframe").style.display = "none"
    else {
      document.getElementById("myiframe").style.display = "block"
    }
  }
  $chatBtn.click(function (e) {
    show_frame();
  })

  $('#navBtn').mouseenter(openNav);

  $('#mySidenav').mouseleave(navBar);

  $loadBtn.click(function(e){
    loadSavedSource();
  });

  $runBtn.click(function(e) {
    run();
  });


  $submitBtn.click(function(e) {
    submit();
  });

  CodeMirror.commands.save = function () {
    save();
  };
  $saveBtn.click(function (e) {
    save();
  });

  $vimCheckBox.change(function () {
    toggleVim();
  });

  $("#downloadSourceBtn").click(function (e) {
    var value = parseInt($selectLanguageBtn.val());
    download(sourceEditor.getValue(), fileNames[value], "text/plain");
  });

  $("#downloadInputBtn").click(function (e) {
    download(inputEditor.getValue(), "input.txt", "text/plain");
  });

  $("#downloadOutputBtn").click(function (e) {
    download(outputEditor.getValue(), "output.txt", "text/plain");
  });
});

// Template Sources
var bashSource = "echo \"hello, world\"\n";

var basicSource = "PRINT \"hello, world\"\n";

var cSource = "\
#include <stdio.h>\n\
\n\
int main(void) {\n\
    printf(\"hello, world\\n\");\n\
    return 0;\n\
}\n";

var cppSource = "\
#include <iostream>\n\
\n\
int main() {\n\
    std::cout << \"hello, world\" << std::endl;\n\
    return 0;\n\
}\n";

var csharpSource = "\
public class Hello {\n\
    public static void Main() {\n\
        System.Console.WriteLine(\"hello, world\");\n\
    }\n\
}\n";

var clojureSource = "(println \"hello, world\")\n";

var crystalSource = "puts \"hello, world\"\n";

var elixirSource = "IO.puts \"hello, world\"\n";

var erlangSource = "\
main(_) ->\n\
    io:fwrite(\"hello, world\\n\").\n";

var goSource = "\
package main\n\
\n\
import \"fmt\"\n\
\n\
func main() {\n\
    fmt.Println(\"hello, world\")\n\
}\n";

var haskellSource = "main = putStrLn \"hello, world\"\n";

var insectSource = "\
2 min + 30 s\n\
40 kg * 9.8 m/s^2 * 150 cm\n\
sin(30°)\n";

var javaSource = "\
public class Main {\n\
    public static void main(String[] args) {\n\
        System.out.println(\"hello, world\");\n\
    }\n\
}\n";

var javaScriptSource = "console.log(\"hello, world\");\n";

var ocamlSource = "print_endline \"hello, world\";;\n";

var octaveSource = "printf(\"hello, world\\n\");\n";

var pascalSource = "\
program Hello;\n\
begin\n\
    writeln ('hello, world')\n\
end.\n";

var pythonSource = "print(\"hello, world\")\n";

var rubySource = "puts \"hello, world\"\n";

var rustSource = "\
fn main() {\n\
    println!(\"hello, world\");\n\
}\n"

var textSource = "hello, world\n";

var sources = {
  1: bashSource,
  2: bashSource,
  3: basicSource,
  4: cSource,
  5: cSource,
  6: cSource,
  7: cSource,
  8: cSource,
  9: cSource,
  10: cppSource,
  11: cppSource,
  12: cppSource,
  13: cppSource,
  14: cppSource,
  15: cppSource,
  16: csharpSource,
  17: csharpSource,
  18: clojureSource,
  19: crystalSource,
  20: elixirSource,
  21: erlangSource,
  22: goSource,
  23: haskellSource,
  24: haskellSource,
  25: insectSource,
  26: javaSource,
  27: javaSource,
  28: javaSource,
  29: javaScriptSource,
  30: javaScriptSource,
  31: ocamlSource,
  32: octaveSource,
  33: pascalSource,
  34: pythonSource,
  35: pythonSource,
  36: pythonSource,
  37: pythonSource,
  38: rubySource,
  39: rubySource,
  40: rubySource,
  41: rubySource,
  42: rustSource,
  43: textSource
};

var fileNames = {
  1: "script.sh",
  2: "script.sh",
  3: "main.bas",
  4: "main.c",
  5: "main.c",
  6: "main.c",
  7: "main.c",
  8: "main.c",
  9: "main.c",
  10: "main.cpp",
  11: "main.cpp",
  12: "main.cpp",
  13: "main.cpp",
  14: "main.cpp",
  15: "main.cpp",
  16: "Main.cs",
  17: "Main.cs",
  18: "main.clj",
  19: "main.cr",
  20: "main.exs",
  21: "main.erl",
  22: "main.go",
  23: "main.hs",
  24: "main.hs",
  25: "main.ins",
  26: "Main.java",
  27: "Main.java",
  28: "Main.java",
  29: "main.js",
  30: "main.js",
  31: "main.ml",
  32: "file.m",
  33: "main.pas",
  34: "main.py",
  35: "main.py",
  36: "main.py",
  37: "main.py",
  38: "main.rb",
  39: "main.rb",
  40: "main.rb",
  41: "main.rb",
  42: "main.rs",
  43: "source.txt"
};
