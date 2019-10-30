// FUNCTION - *** Print log message ***
function LogMessage(message) {
    var isShow = true;
    if (isShow) {
        console.log(message);
    }
}

// Make the height of all selected elements exactly equal - requires jquery.matchHeight-min.js
function MatchHeight() {
    $('.match-height').matchHeight();	// requires jquery.matchHeight-min.js
    $('.match-height2').matchHeight();	// requires jquery.matchHeight-min.js
    $('.match-height3').matchHeight();	// requires jquery.matchHeight-min.js
    $('.match-height4').matchHeight();	// requires jquery.matchHeight-min.js
    $('.match-height5').matchHeight();	// requires jquery.matchHeight-min.js
    $('.match-height6').matchHeight();	// requires jquery.matchHeight-min.js
    $('.match-height7').matchHeight();	// requires jquery.matchHeight-min.js
}

// Scroll back to the top of the page smoothly 
function BackToTop() {
    // Hide #back-top first
    $("#back-top").hide();
    // Fade in #back-top
    $(window).scroll(function () {

        if ($(this).scrollTop() > 100) {
            $("#back-top").fadeIn();
        } else {
            $("#back-top").fadeOut();
        }
    });
    $("#s4-workspace").scroll(function () {


        if ($(this).scrollTop() > 100) {
            $("#back-top").fadeIn();
        } else {
            $("#back-top").fadeOut();
        }
    });


    // Scroll body to 0px on click
    $("#back-top a").click(function () {
        $("body,html,#s4-workspace").animate({
            scrollTop: 0
        }, 800);
        return false;
    });
}

// Smooth Page Scroll - for Anchor Tags
function EnablePageScrollForAnchorTags() {
    $('.AnchorTagGroup a[href*="#"]:not([href="#"])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {

                // $('html, body').animate({
                //	 scrollTop: (target.offset().top - 152)	// scrollTop: target.offset().top
                // }, 800);

                //alert($(window).width() + "	 " + ($(window).width()+17));
                var currentWidth = $(window).width() + 17;
                if (currentWidth > 924) {
                    $('html, body').animate({
                        scrollTop: (target.offset().top - 152)	// scrollTop: target.offset().top
                    }, 800);
                } else {
                    $('html, body').animate({
                        scrollTop: target.offset().top
                    }, 800);
                }

                return false;
            }
        }
    });
}

// Anchor Tags (Reposition anchor tags after the link is redirected) --- ... pages
$(document).ready(function () {
    var elements = $("body").find(".AnchorTagPoint");
    if (elements.length > 0) {
        clearTimeout($.data(this, 'resizeTimer'));
        $.data(this, 'resizeTimer', setTimeout(function () {
            var currentURLHash = location.hash;
            var target = $(currentURLHash);
            // LogMessage(target);
            if (target.length) {

                // $('html, body').animate({
                //	 scrollTop: (target.offset().top - 152)	// scrollTop: target.offset().top
                // }, 20);

                //alert($(window).width() + "	 " + ($(window).width()+17));
                var currentWidth = $(window).width() + 17;
                if (currentWidth > 924) {
                    $('html, body').animate({
                        scrollTop: (target.offset().top - 152)	// scrollTop: target.offset().top
                    }, 800);
                } else {
                    $('html, body').animate({
                        scrollTop: target.offset().top
                    }, 800);
                }

                return false;
            }
        }, 500));
    }
});


$(document).ready(function () {
    /** main navigation **/
    $('.navmenubox .navbar-header button:first').click(function (e) {
        if ($('.navmenubox .navbar-header button:first').attr('aria-expanded') == 'true') {
            $('.navmenubox .navbar-header button:first i').removeClass("fa-bars").addClass("fa-times");
            $('.navmenubox .navbar-header button:last').attr('aria-expanded', 'false');
            $('.navmenubox .navbar-header button:last i').removeClass("fa-times fa-lg").addClass("fa-bars");

            $(".navmenubox .navbar-collapse.searchnavbar").removeClass("show");
            $(".navmenubox .navbar-collapse.menunavbar").addClass("show");
        } else {
            $('.navmenubox .navbar-header button:first i').removeClass('fa-bars').addClass('fa-times fa-lg');
            $('.navmenubox .navbar-header button:last').attr('aria-expanded', 'false');
            $('.navmenubox .navbar-header button:last i').removeClass("fa-bars").addClass("fa-times");

            $(".navmenubox .navbar-collapse.searchnavbar").removeClass("show");
            $(".navmenubox .navbar-collapse.menunavbar").removeClass("show");
        }
    });
});


// Hover On Box
$(document).ready(function () {
    var boxes = $(".box:not(.disableslide)");
    boxes.each(function () {
        $(this).mouseenter(function () {
            $(this).find(".caption").stop().animate({ height: "100%" });
        });

        $(this).mouseleave(function () {
            $(this).find(".caption").stop().animate({ height: "55px" }, function () {
            });
        });
    });
});


/* Requires two js files: (1) slick.min.js & (2) jquery.fitvids.min.js */
$(document).ready(function () {
	/* The below example uses Slick Carousel, however this can be extended into any type of carousel, provided it lets you
	 * bind events when the slide changes. This will only work if all framed videos have the JS API parameters enabled. */

    // Bind our event here, it gets the current slide and pauses the video before each slide changes.
    $(".slick").on("beforeChange", function (event, slick) {
        var currentSlide, slideType, player, command;

        // Find the current slide element and decide which player API we need to use.
        currentSlide = $(slick.$slider).find(".slick-current");

        // Determine which type of slide this, via a class on the slide container.
        // This reads the second class, you could change this to get a data attribute or something similar if you don't want to use classes.
        slideType = currentSlide.attr("class").split(" ")[1];

        // Get the iframe inside this slide.
        player = currentSlide.find("iframe").get(0);

        if (slideType == "vimeo") {
            command = {
                "method": "pause",
                "value": "true"
            };
        } else if (slideType == "youtube") {
            command = {
                "event": "command",
                "func": "pauseVideo"
            };
        } else {
            command = {
                "event": "command",
                "func": "pauseVideo"
            };
        }

        // Check if the player exists.
        if (player != undefined) {
            // Post our command to the iframe.
            player.contentWindow.postMessage(JSON.stringify(command), "*");
        }
    });

    // Run the fitVids jQuery plugin to ensure the iframes stay within the item.
    $('.slick .item').fitVids();
    // $('.carousel-container .video').fitVids();

    // Start the slider
    $('.slider').slick({
        slidesToShow: 1,
        slidesToScroll: 1,
        arrows: false,
        fade: true,
        // adaptiveHeight: true,
        asNavFor: '.slider-nav'
    });
    $('.slider-nav').slick({
        slidesToShow: 3,
        slidesToScroll: 1,
        asNavFor: '.slider',
        dots: true,
        // centerMode: true,
        focusOnSelect: true
    });
});




$(document).ready(function () {

    // open first accordion
    $("#accordion .panel:first-child .panel-title a").removeClass("collapsed");
    $("#accordion .panel:first-child .panel-collapse").addClass("show");
    $("#accordion .panel:first-child .panel-collapse").css("height", "");
    $(window).on('resize', function () {

        $("#accordion .panel:first-child .panel-collapse").removeClass("in");
    });
    if ($(window).width() > 991) {
        // for large screens
        $(".mobile-collapsed-default .panel-title a").removeClass("collapsed");

        $(".mobile-collapsed-default .panel-collapse").addClass("show");
        $(".mobile-collapsed-default .panel-collapse").css("height", "");
    } else {
        // for small screens
        $(".mobile-collapsed-default .panel-title a").removeClass("collapsed");
        $(".mobile-collapsed-default .panel-collapse").addClass("show");

    }
});

$(document).ready(function () {
    /* ======================= Font Size Adjuster ======================= */
    var affectedElements = $(".landing-content, .landing-content p, .landing-content h2, .landing-content h3, .landing-content h4, .landing-content h5, .landing-content a, .landing-content li, .landing-content span, .landing-content b, .landing-content i, .landing-content th, .landing-content td, .landing-content button, .landing-content label");
    var isTextZoomTriggered = false;
    var textZoomLevel = 0;

    affectedElements.each(function () {
        // Store the original size in a data attribute so size can be reset
        $(this).data("original-size", $(this).css("font-size"));
    });

    $("#btn-increase").click(function () {
        if (!isTextZoomTriggered) {
            SetOriginalFontSize(affectedElements);
            isTextZoomTriggered = true;
        }
        if (textZoomLevel < 2) {
            ChangeFontSize(2);
            MatchHeight();
            textZoomLevel++;
        }
        MatchHeight();	// Fired twice
    });
    $("#btn-decrease").click(function () {
        if (!isTextZoomTriggered) {
            SetOriginalFontSize(affectedElements);
            isTextZoomTriggered = true;
        }
        if (textZoomLevel > -2) {
            ChangeFontSize(-2);
            MatchHeight();
            textZoomLevel--;
        }
        MatchHeight();	// Fired twice
    });
    $("#btn-original").click(function () {
        SetOriginalFontSize(affectedElements);
        MatchHeight();
        textZoomLevel = 0;
        MatchHeight();
    });

    function ChangeFontSize(direction) {
        affectedElements.each(function () {
            // $(this).css("font-size", parseInt($(this).css("font-size"))+direction);

            if ($(this).closest(".skipfontresize").length === 0) {
                $(this).css("font-size", parseInt($(this).css("font-size")) + direction);
            }
        });
    }
    function SetOriginalFontSize(items) {
        items.each(function () {
            $(this).css("font-size", $(this).data("original-size"));
        });
    }
    /* ================================================================== */
});


$(document).ready(function () {
    MatchHeight(); // Make the height of all selected elements exactly equal - requires jquery.matchHeight-min.js

    BackToTop();	// Scroll back to the top of the page smoothly

    EnablePageScrollForAnchorTags();	// Smooth Page Scroll - for Anchor Tags

    initializeMasterPage();
});
function printpg() {
    window.print();
}

$(window).resize(function () {
    try { mob_nicescroll(); } catch (errC) { }
});

$(document).ready(function () {
    $(window).bind('orientationchange', function () { try { mob_nicescroll(); } catch (errC) { } });    
    try { mob_nicescroll(); } catch (errC) { }

    $(".panel-heading h4").click(function () {
        try { mob_nicescroll(); } catch (errC) { }
    });
});

function mob_nicescroll() {
    $(document).ready(function () {
        try {
            $('.landing-content table').each(function () {
                if (!$(this).parent().is('div.rd-mob-tablewrap')) { // if not already wrapped
                    var bTableVisible = $(this).is(':visible');
                    var bTableNested = $(this).closest('.landing-content table table').length;
                    if ((bTableVisible) && (bTableNested == 0)) { // visible and non-nested table 
                        var viewportSizeContent = $('.landing-content').width();
                        if ($(this).width() > viewportSizeContent) {
                            $(this).wrapAll('<div class="rd-mob-tablewrap" />');
                            try { var eNice = $(this).parent().niceScroll({ touchbehavior: true, emulatetouch: true, cursorcolor: "#dddddd", cursoropacitymax: 0.3, cursorwidth: 8, autohidemode: false }); } catch (errC) { }
                        }
                    }
                }
            });
        } catch (errC) { }
    });
}




/* homepage useful content widget */
$(document).ready(function () {
	$('.usefulinfo-container #usefulinfotab a').on('mouseup', function() {
		setTimeout(function() {
		    $('.match-height').matchHeight();
		}, 50);
	});
});


/* forms requirement treatment */
$(document).ready(function () {
	// hide non-mandatory id fields
	try { $(".form-horizontal label[for='nric']").closest("div.form-group").wrap("<div class='formgroup-hidden' style='height:0; overflow:hidden; display:none !important;'></div>"); } catch(errC) {}
	try { $(".form-horizontal label[for='passportNo']").closest("div.form-group").wrap("<div class='formgroup-hidden' style='height:0; overflow:hidden; display:none !important;'></div>"); } catch(errC) {}
	try { $(".form-pharmacy label[for*='txtPatientNRIC']").closest("div.form-group").wrap("<div class='formgroup-hidden' style='height:0; overflow:hidden; display:none !important;'></div>"); } catch(errC) {}
});	


/* brand top bar */
$(document).ready(function () {
 try { $('div.navmenubox.navbar').prepend('<div class="corpbrand-topbar"><div class="corpbrand-topbar3"><div class="corpbrand-topbar2"><div class="corpbrand-topbar1">&nbsp;</div></div></div></div>'); } catch(errC) {}
}); 
/* favicon */
$(document).ready(function () { try { $('#favicon').attr("href","/style library/nuh/images/favicon.ico"); } catch(errC) {} }); 
$(document).ready(function () { try { $('link[rel="shortcut icon"]').attr("href","/style library/nuh/images/favicon.ico"); } catch(errC) {} }); 