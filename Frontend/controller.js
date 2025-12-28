$(document).ready(function () {
  // Display Speak Message
  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
    $(".siri-message li:first").text(message);
    $(".siri-message").textillate("start");
  }

   eel.expose(ShowHood);
  function ShowHood() {
    $("#Oval").attr("hidden", false);
    $("#SiriWave").attr("hidden", true);
  }
})
$(document).ready(function () {
    $("#micBtn").click(function () {
        eel.takeAllCommands()();
    });
    $("#sendBtn").click(function () {
        let msg = $("#userInput").val();
        eel.takeAllCommands(msg);
        $("#userInput").val('');
    });
    eel.expose(DisplayMessage);
    function DisplayMessage(msg) {
        $("#chatbox").append(`<div class="bot-msg">${msg}</div>`);
    }
    eel.expose(senderText);
    function senderText(msg) {
        $("#chatbox").append(`<div class="user-msg">${msg}</div>`);
    }
});