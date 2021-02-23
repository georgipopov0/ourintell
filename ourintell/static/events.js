$(document).ready(function(){
    var url = window.location.href
    var args = url.split('/events')[1]
    var test = '/download/events'+ 
                args
    $("#download-btn").attr('href',test)
})
