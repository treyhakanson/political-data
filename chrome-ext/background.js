chrome.runtime.onMessage.addListener(function(request, sender, callback) {
  if (request.action == "xhttp") {
    $.ajax({
        type: request.method,
        url: request.url,
        data: request.data,
        success: function(response){
            callback(response);
        },
        error: function(error){
           callback();
        }
     });

    return true; // prevents the callback from being called too early on return
  }
});