console.log(document.URL)

var ln = $('#left-nav').children();
var rn = $('#right-nav').children();

function changeActive() {
    ln.each(function() {
        $(this).attr('class','active');
    });
    console.log(ln);
    rn.each(function() {
        $(this).attr('class','active');
    });
    console.log(rn);
    $(this).attr('class','active nav-link');
    console.log(this);
}

$(window).bind('beforeunload', function(){
    ln.on('click',changeActive());
    rn.on('click',changeActive());
});