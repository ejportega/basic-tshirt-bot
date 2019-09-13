function submit_message(message) {
    console.log(message)
    $.post( "/send_message", {message: message}, handle_response);

    function handle_response(data) {
      // append the bot repsonse to the div
      $('.chat-container').append(`
            <div class="chat-message bot-message">
                <div class="chat-image">
                    <img src="https://imgur.com/3pgjFvq.png" />
                </div>
                <b>Bot: </b>
                ${data.message}
            </div>
      `)
      // remove the loading indicator
      $( "#loading" ).remove();
    }
    // auto scroll
    $(".chat-container").stop().animate({ scrollTop: $(".chat-container")[0].scrollHeight}, 1000);
}

$('#target').on('submit', function(e){
    e.preventDefault();
    const input_message = $('#input_message').val()
    // return if the user does not enter any text
    if (!input_message) {
      return
    }

    $('.chat-container').append(`
        <div class="chat-message human-message">
            <div class="chat-image">
                <img src="https://imgur.com/Fcos3Vt.png" />
            </div>
            <b>You: </b>
            ${input_message}
        </div>
    `)

    // loading 
    $('.chat-container').append(`
        <div class="chat-message bot-message" id="loading">
            <b>...</b>
        </div>
    `)

    // clear the text input 
    $('#input_message').val('')

    // send the message
    submit_message(input_message)
});
