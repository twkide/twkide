var $loginBtn;

 function login() {
    console.log("login");
    window.location.href = "./ide.html";
  // if (sourceEditor.getValue().trim() == "") {
  //   alert("Source code can't be empty.");
  //   return;
  // } else {
  //   $runBtn.button("loading");
  // }

  // var sourceValue = btoa(unescape(encodeURIComponent(sourceEditor.getValue())));
  // var inputValue = btoa(unescape(encodeURIComponent(inputEditor.getValue())));
  // var languageId = $selectLanguageBtn.val();
  // var data = {
  //   source_code: sourceValue,
  //   language_id: languageId,
  //   stdin: inputValue
  // };

  // $.ajax({
  //   url: BASE_URL + `/submissions?base64_encoded=true&wait=${WAIT}`,
  //   type: "POST",
  //   async: true,
  //   contentType: "application/json",
  //   data: JSON.stringify(data),
  //   success: function(data, textStatus, jqXHR) {
  //     console.log(`Your submission token is: ${data.token}`);
  //     if (WAIT == true) {
  //       handleResult(data);
  //     } else {
  //       setTimeout(fetchSubmission.bind(null, data.token), SUBMISSION_CHECK_TIMEOUT);
  //     }
  //   },
  //   error: handleRunError
  // });
}

function initializeElements() {
    $loginBtn = $('#loginBtn');
    
  }

$(document).ready(function() {
    console.log("Hey, TWKIDE is based on judge0 ide, an open-sourced: https://github.com/judge0/ide. Have fun!");
  
    initializeElements();
    if ($loginBtn == undefined) console.log("loginbtn undefined");

    $loginBtn.click(function(e) {
        console.log("click loginbtn");
        login();
      });
    
    
 });

 
