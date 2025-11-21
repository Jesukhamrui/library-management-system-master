// Make <li> clickable when it contains an <a> and add keyboard support
(function($){
  $(function(){
    // Delegate click: if clicked on li (but not on a clickable control), navigate to first anchor
    $(document).on('click', 'ul.interactive li', function(e){
      // ignore clicks on actual anchors, buttons, inputs
      var $target = $(e.target);
      if ($target.is('a') || $target.closest('a').length) return;
      if ($target.is('button') || $target.is('input') || $target.is('label')) return;

      var $a = $(this).find('a').first();
      if ($a.length) {
        var href = $a.attr('href');
        if (href && href !== '#') {
          window.location.href = href;
        }
      }
    });

    // Keyboard accessibility: Enter or Space on focused li
    $(document).on('keydown', 'ul.interactive li', function(e){
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        $(this).trigger('click');
      }
    });

    // Make li elements focusable
    $('ul.interactive li').attr('tabindex', '0');
  });
})(jQuery);
