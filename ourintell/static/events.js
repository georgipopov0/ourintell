$(document).ready(function(){
    $("#search_box").on('keypress', function (e) {
        if(e.which === 13){ 

            value = $(this).val();
            // value = value.replace(/\s+/g, '');
            tags = value.split(",")
            console.log(tags)
            for(tag in tags){
                // Add the url arguments for the search
                if(document.location.href.indexOf('?') > -1) {
                    var url = document.location.href+'&'+tags[tag];
                }else{
                    var url = document.location.href+'?'+tags[tag];
                }
            }
            document.location = url;


        }
    });
});

