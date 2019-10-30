$(document).ready(function() {

  // Lightbox with extended functionality zoom (requires jquery.fancybox.js)
  $(".fancybox-button").fancybox({
    prevEffect: 'fade',
    nextEffect: 'fade',
    closeBtn: true,
    closeClick: false,
    helpers: {
      title: { type: 'inside' },
      buttons: {
        position: 'top',
        tpl:  '<div id="fancybox-buttons"><ul style="width:74px;height:32px;">' +
          '<li><a class="btnPrev" title="Previous" href="javascript:;" style="display:none;"></a></li>' +
          '<li><a class="btnPlay" title="Start slideshow" href="javascript:;" style="display:none;"></a></li>' +
          '<li><a class="btnNext" title="Next" href="javascript:;" style="display:none;"></a></li>' +
          '<li><a class="btnToggle" title="Toggle size" href="javascript:;"></a></li>' +
          '<li><a class="btnClose" title="Close" href="javascript:;"></a></li>' +
          '</ul></div>'
      }
    }
  });
  
});