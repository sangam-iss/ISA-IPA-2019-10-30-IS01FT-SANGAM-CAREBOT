var iWantToSettings = '[' +
    '{ "Pagename":"Make/Change/Cancel an Appointment" , "Icon":"fa fa-calendar" },' +
    '{ "Pagename":"Find a Doctor" , "Icon":"fa fa-user-md"  },' +
    '{ "Pagename":"Find a Condition/Treatment" , "Icon":"fa fa-medkit" },' +
    '{ "Pagename":"Find Directions" , "Icon":"fa fa-map-marker"  },' +
    '{ "Pagename":"Contact NUH" , "Icon":"fa fa-phone" },' +
    '{ "Pagename":"Make Online Payment" , "Icon":"fa fa-dollar"  },' +
    '{ "Pagename":"Search" , "Icon":"fa fa-search"  } ]';
var socialMediaSettings = '[' +
    '{ "LinkName":"Facebook" , "URL":"https://www.facebook.com/NationalUniversityHospital/" , "Hide":"No"},' +
    '{ "LinkName":"LinkedIn" , "URL":"https://www.linkedin.com/company/national-university-hospital" ,"Hide":"No"  },' +
    '{ "LinkName":"Youtube" , "URL":"https://www.youtube.com/user/TheNUH1985" ,"Hide":"No" },' +
    '{ "LinkName":"Instagram" , "URL":"https://www.instagram.com/nuhig/" ,"Hide":"No"  }' +

    ']';
var navRemoveMobileView = '['+
		'{ "LinkName":"Clinical Outcomes" },' +
		'{"LinkName":"Diseases & Conditions"},' +
		'{"LinkName":"Specialties"},'  +
		'{"LinkName":"Overseas Referrals"}'  +
		']';


var searchPageURL = null;

function initializeMasterPage() {
    //Hide Submenus for mobile view
    
     var obj = jQuery.parseJSON(navRemoveMobileView);
      $.each(obj, function (index, jsonObject) {
    	 $("a[title='"+jsonObject.LinkName+"']").siblings("ul").remove();

     });

    UpdateSocialLinks();
    //Site Icon CSS change
    $('ul.navbar-nav li:first').css('display', 'none');
    $("#DeltaSiteLogo > a").attr("class", "navbar-brand");

    //Bredcrumb
    $('ul.breadcrumb').find('a').each(function () {
        $(this).css('color', 'white');

    });
    customizedNavigation();
    loadFooterContent();
    $(window).resize(checkRibbon);
    checkRibbon();

}
function UpdateSocialLinks() {
    var obj = jQuery.parseJSON(socialMediaSettings);
    $.each(obj, function (index, jsonObject) {
        if (jsonObject.LinkName.toLowerCase() === "facebook") {
            if (jsonObject.Hide.toLowerCase() === "no") {
                $("div.socialmedia").find("i.fa-facebook").parents('a').css('display', 'inline');
                $("div.socialmedia").find("i.fa-facebook").parents('a').attr('href', encodeURI(decodeURI(jsonObject.URL)));
            }
            else {
                $("div.socialmedia").find("i.fa-facebook").parents('a').css('display', 'none');

            }

        }
        if (jsonObject.LinkName.toLowerCase() === "linkedin") {
            if (jsonObject.Hide.toLowerCase() === "no") {
                $("div.socialmedia").find("i.fa-linkedin").parents('a').css('display', 'inline');
                $("div.socialmedia").find("i.fa-linkedin").parents('a').attr('href', encodeURI(decodeURI(jsonObject.URL)));
            }
            else {
                $("div.socialmedia").find("i.fa-linkedin").parents('a').css('display', 'none');

            }

        }
        if (jsonObject.LinkName.toLowerCase() === "instagram") {
            if (jsonObject.Hide.toLowerCase() === "no") {
                $("div.socialmedia").find("i.fa-instagram").parents('a').css('display', 'inline');
                $("div.socialmedia").find("i.fa-instagram").parents('a').attr('href', encodeURI(decodeURI(jsonObject.URL)));
            }
            else {
                $("div.socialmedia").find("i.fa-instagram").parents('a').css('display', 'none');

            }

        }
        if (jsonObject.LinkName.toLowerCase() === "youtube") {
            if (jsonObject.Hide.toLowerCase() === "no") {
                $("div.socialmedia").find("i.fa-youtube-square").parents('a').css('display', 'inline');
                $("div.socialmedia").find("i.fa-youtube-square").parents('a').attr('href', encodeURI(decodeURI(jsonObject.URL)));
            }
            else {
                $("div.socialmedia").find("i.fa-youtube-square").parents('a').css('display', 'none');

            }

        }




    });


}
function loadFooterContent() {

    $('.footer').load('/SiteAssets/HTML/Footer/footer.html');

}
function checkRibbon() {
    if ($("#s4-ribbonrow").is(":visible")) {
        $("div.fixed-top").css('position', 'relative');
        $("div.fixed-top").css('z-index', '1000');

    }

}
function customizedNavigation() {

    //Apply custom style for breadcrumb

    var breadcrumbStr = "";
    //Get Root node
    var rootNode = $('a.ms-breadcrumbRootNode');
    if ($(rootNode).length) {
        var nodeName = rootNode[0].innerText;

        breadcrumbStr += "<li><a href='" + encodeURI(decodeURI(rootNode[0].href)) + "'>" + nodeName + "</a></li>";

    }
    //Get Subsequent nodes
    var nodes = $('a.ms-breadcrumbNode');
    if ($(nodes).length) {
        var i = 0;

        $(nodes).each(function () {

            if (i == 0) {
                $("#pageHeading").text($(this)[0].innerText);
                $("ul.navbar-nav > li").find('a[title="' + $(this)[0].innerText + '"]').parent().closest('li').addClass('active');
                nodeName = $(this)[0].innerText;
                breadcrumbStr += "<li>" + nodeName + "</li>";

            }//ESAPI.encoder()
            else {
                nodeName = $(this)[0].innerText;
                breadcrumbStr += "<li><a href='" + encodeURI(decodeURI($(this)[0].href)) + "'>" + nodeName + "</a></li>";
            }

            i++;
        });

    }
    //Get CurruentNode
    var curruentNode = $('span.ms-breadcrumbCurrentNode');
    if ($(curruentNode).length) {


        breadcrumbStr += "<li>" + curruentNode[0].innerText + "</li>";

        if (nodes.length == 0) {

            $("ul.navbar-nav > li").find('a[title="' + curruentNode[0].innerText + '"]').parent().closest('li').addClass('active')
            $("#pageHeading").text(curruentNode[0].innerText);

        }//

    }
    $("ul.breadcrumb").empty();
    $("ul.breadcrumb").append(breadcrumbStr);

    var selectedTabName = "";
    var nav = $(".nav");
    if (nav == null || typeof (nav) == 'undefined') return;
    //Apply Custom CSS to Left Navigation

    $("div.ms-core-listMenu-verticalBox > ul").attr("id", "left-menu");

    $("#left-menu").attr("class", "leftsidenav"); // set the class for <ul> element replacing the system css  

    $('#left-menu').parent().closest('div').attr("class", "").addClass("panel-collapse collapse show");
    $('#left-menu').parent().closest('div').attr("id", "leftnav_accordion_collapse1")

    $('#leftnav_accordion_collapse1').parent().closest('div').attr("id", "leftnav_accordion");
    $('#leftnav_accordion_collapse1').parent().closest('div').addClass("panel-group leftnav_accordion");

    $('#leftnav_accordion').parent().closest('div').attr("id", "StickWhileScrollPage");
    $('#leftnav_accordion').parent().closest('div').css("width", "width: 247.25px");

    $('#StickWhileScrollPage').parent().closest('div').attr("id", "left_collapse1");
    $('#StickWhileScrollPage').parent().closest('div').addClass("panel-collapse collapse show leftside_panelgroup_content d-none d-lg-block");

    $('#left-menu > li').each(function (i) {
        if ($(this).find("a:first").length) //If its link node 
        {

            var headerlinkURL = encodeURI($(this).find("a:first")[0].pathname); //Required if submenu is selected 
            var relativeURL = decodeURI(headerlinkURL);
            if ($(this).children("ul").length) {
                // the clicked on <li> has a <ul> as a direct child
                $(this).addClass('parent');
                $(this).find("span.ms-hidden").remove();


                var subMenus = $(this).children("ul")
                var isSubMenuSelected = false;
                $(subMenus).find('li').each(function () {


                    $(this).find("span.ms-hidden").remove();
                    var subMenuNavElement = $(this).find("a:first");
                    if (subMenuNavElement[0] == null || typeof (subMenuNavElement[0]) == 'undefined') return;

                    var subMenuLinkName = $(subMenuNavElement)[0].innerText;

                    var subMenuURL = encodeURI(decodeURI($(subMenuNavElement)[0].href));

                    $(this).html('<a href="' + subMenuURL + '">' + subMenuLinkName + '</a>');
                    if ($(this).hasClass('selected')) {
                        isSubMenuSelected = true;
                        $(this).addClass('active');

                        //Check For Topnavigation selected as submenus not present in top nav


                        var selectedTopNav = $(".nav").find('a[href="' + relativeURL + '"]');
                        if ($(selectedTopNav).hasClass("navmenu")) {
                            $(selectedTopNav).closest("li").addClass("active");
                        }
                        else {
                            $(selectedTopNav).parent().parent().closest("li").addClass("active");
                        }


                    }


                });
                if ($(this).hasClass('selected')) {
                    $(this).addClass('active');
                }
                else {
                    if (!isSubMenuSelected) //If submenu not selected, submenus not visible
                    {
                        $(subMenus).css('display', 'none');
                        var name = $(this).find("a:first")[0].innerText;
                        $(this).find("a:first").replaceWith(function () {
                            return $('<a href="' + encodeURI(decodeURI(headerlinkURL)) + '">' + name + '</a>');
                        });
                        $(this).removeClass('parent');
                        //$(this).find("a:first").html('<a href="' + headerlinkURL + '">' + name + '</a>');
                    }
                }
            }
            else {
                $(this).find("span.ms-hidden").remove();
                var navElement = $(this).find("a:first");
                if (navElement[0] == null || typeof (navElement[0]) == 'undefined') return;

                var linkName = $(navElement)[0].innerText;
                var linkURL = encodeURI(decodeURI($(navElement)[0].href));
                $(this).html('<a href="' + linkURL + '">' + linkName + '</a>');
                if ($(this).hasClass('selected')) {
                    $(this).addClass('active');
                }
            }
        }


    });
    //Hide Recent From Top Navigation
    $(".nav-link[title='Recent']").each(function () {
        $(this).hide();
    });
    $(".ms-core-listMenu-item:contains('Recent')").parent().hide();

    //I want to settings

    $("ul.navbar-nav > li:last").addClass('iwantto');
    $("li.iwantto a").first().append('<i class="fa fa-angle-down"></i>');


    var obj = jQuery.parseJSON(iWantToSettings);
    $.each(obj, function (index, jsonObject) {

        var object = $("li.iwantto").find('a:contains(' + jsonObject.Pagename + ')');
        if (jsonObject.Pagename.toLowerCase() === "search") {
            $(object).addClass("IWANTTO_SEARCH_MODAL_BOX_LINK");
            searchPageURL = $(object).attr("href");

            $(object).removeAttr("href");
        }
        $(object).prepend("<i class='" + jsonObject.Icon + "'></i>");


    });

    //Add Search Box to left navigation
    var leftSearchNav = $('#left-menu > li').find('a:contains("Search")');
    if ($(leftSearchNav).length) {
        $(leftSearchNav).addClass("IWANTTO_SEARCH_MODAL_BOX_LINK");

        $(leftSearchNav).removeAttr("href");
    }

    $('#modalSearchTextbox').keypress(function (event) {
        if (event.keyCode == 13 || event.which == 13) {
            redirectToSearcPage();

            event.preventDefault();
        }
    });

    SearchModalBoxSetting();
}

// Search Modal Box

function SearchModalBoxSetting() {
    var modalBox = $(".IWANTTO_SEARCH_MODAL_BOX");
    var openBtn = $(".IWANTTO_SEARCH_MODAL_BOX_LINK");
    var closeBtn = $(".IWANTTO_SEARCH_MODAL_BOX .close");

    // open the modal box
    openBtn.click(function (e) {
        modalBox.show();
    });

    // close the modal box
    closeBtn.click(function (e) {
        modalBox.hide();
    });

    // click outside of the modal box to close it
    $(document).on("click", function (e) {
        if (modalBox.is(e.target) && modalBox.has(e.target).length === 0) {
            modalBox.hide();
        }
    });

}



// Search Modal Box

function SearchModalBoxSetting() {
    var modalBox = $(".IWANTTO_SEARCH_MODAL_BOX");
    var openBtn = $(".IWANTTO_SEARCH_MODAL_BOX_LINK");
    var closeBtn = $(".IWANTTO_SEARCH_MODAL_BOX .close");

    // open the modal box
    openBtn.click(function (e) {
        modalBox.show();
    });

    // close the modal box
    closeBtn.click(function (e) {
        modalBox.hide();
    });

    // click outside of the modal box to close it
    $(document).on("click", function (e) {
        if (modalBox.is(e.target) && modalBox.has(e.target).length === 0) {
            modalBox.hide();
        }
    });

}
function redirectToSearcPage() {

    var sbox = document.getElementById('modalSearchTextbox');
    if (sbox.value.toString() > '') {

        window.location.href = searchPageURL + "?q=" + encodeURIComponent(sbox.value.toString());
    }
    return false;
}
