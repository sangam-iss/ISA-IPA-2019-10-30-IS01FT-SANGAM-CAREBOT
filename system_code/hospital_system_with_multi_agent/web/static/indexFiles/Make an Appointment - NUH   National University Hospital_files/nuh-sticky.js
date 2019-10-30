$(window).on("load", function () {
    if ($(window).width() > 992) {
        // for large screens
            var siteindexcontainer_height = $(".siteindex-container").height();
            var copyrightcontainer_height = $(".copyright-container").height();
            var hospitallogocontainer_height = $(".hospital-logo-container").height();
            var extra = 70;
            var totalHeight = siteindexcontainer_height + copyrightcontainer_height + hospitallogocontainer_height + extra;
            $("#StickWhileScrollPage").sticky({ topSpacing: 125, bottomSpacing: totalHeight, responsiveWidth: true });
    } else {
        // for small screens
        $("#StickWhileScrollPage").unstick();
    }

	$(window).on('resize', function () {
	    var win = $(this);
	    if (win.width() > 992) {
	        // for large screens
	            var siteindexcontainer_height = $(".siteindex-container").height();
	            var copyrightcontainer_height = $(".copyright-container").height();
	            var hospitallogocontainer_height = $(".hospital-logo-container").height();
	            var extra = 70;
	            var totalHeight = siteindexcontainer_height + copyrightcontainer_height + hospitallogocontainer_height + extra;
	            $("#StickWhileScrollPage").sticky({ topSpacing: 125, bottomSpacing: totalHeight, responsiveWidth: true });
	    } else {
	        // for small screens
	        $("#StickWhileScrollPage").unstick();
	    }
	});

});
