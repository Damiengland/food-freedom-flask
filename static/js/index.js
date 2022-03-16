// Weight loss equation drop panel
$(".down").click(function() {
    if($(".down").hasClass("fa-chevron-down")){
        $(".down").removeClass("fa-chevron-down")
        $(".down").addClass("fa-chevron-up")
    } else {
        $(".down").removeClass("fa-chevron-up")
        $(".down").addClass("fa-chevron-down")
    }
    $(".collapse-info").toggleClass("expand")

})

// Add White BG to navbar after feature image
var path = document.location.pathname;

if (path == "/") {
    $(window).scroll(function() {
        var scroll = $(window).scrollTop();
        var sectionHeight = $("#banner").height();

            if (scroll >= (0.9 * sectionHeight)) {
                $(".navbar").css("background-color", "white");
            } else {
                $(".navbar").css("background-color", "transparent");
            }
    });
} else {
    $(".navbar").css("background-color", "white");
};

// Social icon show tag
$(".instagram").hover(function() {
    $(".instagram .tag").toggleClass("show-tag");
});
$(".facebook").hover(function() {
    $(".facebook .tag").toggleClass("show-tag");
});


// Print Page
function printDiv()
{

  var divToPrint = document.getElementById('print-section');

  var newWin = window.open('','Print-Window');

  newWin.document.open();

  newWin.document.write('<html><body onload="window.print()">'+divToPrint.innerHTML+'</body></html>');

  newWin.document.close();

}