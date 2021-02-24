$(document).ready(function(){
    var url = window.location.href
    var args = url.split('/events')[1]
    var download_url = '/download/events'+ 
                args
    $("#download-btn").attr('href',download_url)
    var download_ips_url = '/download/ip/events'+ 
                args
    $("#download-ip-btn").attr('href',download_ips_url)
})
