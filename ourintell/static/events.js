$(document).ready(function(){
    var url = window.location.href

    // Creates a string containing only the url arguments
    var args = url.split('/events')[1]

    $("#download-btn").attr('href','/download/events' + args)
    $("#download-ip-btn").attr('href','/download/ip/events' + args)
})

