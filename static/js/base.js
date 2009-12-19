(function($) {
  var titleColors = ['#d0884c', '#8e4cd0', '#4c70d0', '#4cd0ac', '#2b7e27', '#cbe341', '#c57862', '#c41a1a', '#b2509e'];
  $(function() {
    $('#header').animate({'backgroundColor': '#7ddb6e'}, 2000);
    $('.headerBtn').animate({'borderColor': '#1e2295'}, 2000);
    $('.headerBtn a').hover(function() {
      $(this).animate({'color': '#362f20'}, 500);
      $(this).css("border-style", "dashed");
      }, function() {
      $(this).animate({'color': '#a5905a'}, 500);
      $(this).css("border-style", "solid");
      });
    var titleColorIndex;
    function animateTitle(index) {      
      $('#pageTitle').animate({'color': titleColors[index]}, 1000, function() {
        titleColorIndex = index >= titleColors.length ? 0 : index + 1;
        animateTitle(titleColorIndex);
        });
      }
    setTimeout("animateTitle(0)", 4000);  
    var searchIndex;
    function changeSearch() {
      if (searchIndex >= TAGS.length) searchIndex = 0;
      $('#search').val(TAGS[searchIndex]);
      searchIndex++;
      }
    $('#search').blur(function() {
      searchInterval = setInterval(changeSearch, 2000);
      }).focus(function() {
      clearInterval(searchInterval);
      });
    var searchInterval = setInterval(changeSearch, 2000);  
    });
  })(jQuery);

  
