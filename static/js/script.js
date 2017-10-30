var USERMENU_FADE_DURATION = 250,
    LIGHTBOX_FADE_DURATION = 250,
    SCREENS_TRANSLATION_DURATION = 400;

var bricks = null;

var $grid = $('.screens-content');

var showMenu = function(menu){
  animate({
    el: menu,
    opacity: [0, 1],
    easing: 'easeInOutQuad',
    duration: USERMENU_FADE_DURATION,
    begin: function() {
      menu.removeClass('hide');
    }
  });
};

var hideMenu = function(menu){
  animate({
    el: menu,
    opacity: [1, 0],
    easing: 'easeInOutQuad',
    duration: USERMENU_FADE_DURATION,
    complete: function() {
      menu.addClass('hide');
    }
  });
};

var gotoScreen = function(screenId){
  var $lightbox = $('.lightbox');

  if (!$lightbox.is(':visible')) return;

  var $prevActiveScreen = $lightbox.find('.lightbox-screen.active'),
      $nextActiveScreen = $lightbox.find('.lightbox-screen[data-screen-id="' + screenId + '"]');

  if ($nextActiveScreen.length > 0) shiftScreens($prevActiveScreen, $nextActiveScreen);
};

var gotoPrevScreen = function(){
  var $lightbox = $('.lightbox');

  if (!$lightbox.is(':visible')) return;

  var $prevActiveScreen = $lightbox.find('.lightbox-screen.active'),
      $nextActiveScreen = $prevActiveScreen.prev();

  if ($nextActiveScreen.length > 0) shiftScreens($prevActiveScreen, $nextActiveScreen);
};

var gotoNextScreen = function(){
  var $lightbox = $('.lightbox');

  if (!$lightbox.is(':visible')) return;

  var $prevActiveScreen = $lightbox.find('.lightbox-screen.active'),
      $nextActiveScreen = $prevActiveScreen.next();

  if ($nextActiveScreen.length > 0) shiftScreens($prevActiveScreen, $nextActiveScreen);
};

var closeLightbox = function(){
  var $lightbox = $('.lightbox');

  if (!$lightbox.is(':visible')) return;

  animate({
    el: $lightbox,
    opacity: [1, 0],
    easing: 'easeInOutQuad',
    duration: LIGHTBOX_FADE_DURATION,
    complete: function() {
      $lightbox.addClass('hide');
    }
  });

  var loc = window.location.href.replace(/#.*/, '');
  history.replaceState('', document.title, loc);

  $('body').removeClass('locked');
};

var showLightbox = function(activeScreenId){
  var $lightbox         = $('.lightbox'),
      $prevActiveScreen = $lightbox.find('.lightbox-screen.active'),
      $nextActiveScreen = $lightbox.find('.lightbox-screen[data-screen-id="' + activeScreenId + '"]');

  if ($lightbox.length == 0 || $nextActiveScreen.length == 0) return;

  $('body').addClass('locked');

  animate({
    el: $lightbox,
    opacity: [0, 1],
    easing: 'easeInOutQuad',
    duration: LIGHTBOX_FADE_DURATION,
    begin: function(){
      $lightbox.removeClass('hide');

      var lightboxHeight = $lightbox.height();

      $lightbox.find('.lightbox-screen').each(function(){
        var $figure   = $(this),
            $img      = $figure.find('> img'),
            $caption  = $figure.find('> figcaption'),
            height  = Math.min(lightboxHeight, $img.data('height'));

        $img.height(height);
        $img.width($img.data('width') * (height / $img.data('height')));
      });

      shiftScreens($prevActiveScreen, $nextActiveScreen, { animate: false });
    }
  });
};

var shiftScreens = function($prev, $next, opts){
  var $strip    = $('.lightbox-strip'),
      $controls = $('.lightbox-control-prev, .lightbox-control-next'),
      transX    = (-1 * $next.position().left) + ($(window).width() / 2) - ($next.width() / 2);

  $controls.hide();

  $prev.removeClass('active');
  $next.addClass('active');

  if (typeof opts !== 'undefined' && opts.animate === false) {
    $strip.css('transform', 'translateX(' + transX + 'px)');
    positionControls($next);
  } else {
    animate({
      el: $strip,
      translateX: [$strip.data('current-trans-x'), transX],
      easing: 'easeOutSine',
      duration: SCREENS_TRANSLATION_DURATION,
      complete: function() {
        positionControls($next);
      }
    });
  }

  var loc = window.location.href.replace(/#.*/, '') + '#' + $next.data('screen-id');
  history.replaceState('', document.title, loc);

  $strip.data('current-trans-x', transX);
};

var positionControls = function($scr){
  var topOffset = $scr.position().top + $scr.find('> img').height() / 2,
      sideOffset = ($(window).width() - $scr.width()) / 2 - 66;

  $('.lightbox-control-prev')
    .css({
      top: topOffset,
      left: "40px"
    })
    .show();

  $('.lightbox-control-next')
    .css({
      top: topOffset,
      right: "40px"
    })
    .show();
};


var hidePopup = function(){
  $('.overlay .popup a.close').on('click', function(){
    $('.overlay').hide();
  });
}

var screensInit = function(){
  $(document)
    .keyup(function(e){
      switch(e.which){
        case 27:
          closeLightbox();
          break;
        case 37:
          gotoPrevScreen();
          break;
        case 39:
          gotoNextScreen();
          break;
      }
    })
    .on('focus', '#search_input', function(){
      showMenu($('#search_menu'));
    })
    .on('blur', '#search_input', function(){
      hideMenu($('#search_menu'));
    })
    .on('mouseenter', '#user_menu_handle', function(){
      showMenu($('#user_menu'));
    })
    .on('mouseleave', '#user_menu', function(){
      hideMenu($('#user_menu'));
    })
    .on('click', '[data-toggle="lightbox"]', function(e){
      e.preventDefault();
      showLightbox($(this).parents('.screen').data('screen-id'));
    })
    .on('click', '.lightbox-control-close', closeLightbox)
    .on('click', '.lightbox-control-prev', gotoPrevScreen)
    .on('click', '.lightbox-control-next', gotoNextScreen)
    .on('click', '.lightbox-screen', function(){
      gotoScreen($(this).data('screen-id'));
    });

  if (location.hash) {
    var screenId = location.hash.substring(location.hash.indexOf('#') + 1);

    showLightbox(screenId);
  }
}

$(window).on("scroll", function() {
  var scrollHeight = $(document).height();
  var scrollPosition = $(window).height() + $(window).scrollTop();
  if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
      // when scroll to bottom of the page
      $(".popup").css("bottom", "-666px");
  }else{
    $(".popup").css("bottom", "30px" );
  }
});

$(document)
  .on('ready', function(){

    screensInit();
    $grid.masonry({
      // options...
      itemSelector: '.screen',
      columnWidth: 250,
      fitWidth: true,
      gutter: 20,
      transitionDuration: 0
    });


    hidePopup();

    // hide #back-top first
  	$("#back-top").hide();

  	// fade in #back-top
  	$(function () {
  		$(window).scroll(function () {
  			if ($(this).scrollTop() > 100) {
  				$('#back-top').fadeIn();
  			} else {
  				$('#back-top').fadeOut();
  			}
  		});

  		// scroll body to 0px on click
  		$('#back-top a').click(function () {
  			$('body,html').animate({
  				scrollTop: 0
  			}, 400);
  			return false;
  		});
  	});
  });

$grid.on('DOMNodeInserted', function(e){$grid.masonry( 'appended', $(".screen:not([style])"))});
$('select').niceSelect();

(function (grid) {

    var objStr = {};
    var allFilters = document.querySelectorAll(".filter");
    var allCheckedRadio = document.querySelectorAll('.filter input:checked');

    //init active checkboxes

    for (var i=0; i<= allCheckedRadio.length-1; i++) {
        allCheckedRadio[i].parentNode.classList.toggle("checked" + allCheckedRadio[i].name);
    }

    // Set event listenters to all filters group
    for (var i = 0; i <= allFilters.length - 1; i++) {
        allFilters[i].addEventListener("click", function (e) {

            var target = e && e.target || event.srcElement;
            if (target.tagName === 'INPUT') {

                var label = document.querySelectorAll(".checked" + target.name);
                target.parentNode.classList.toggle("checked" + target.name);
                for (var i = label.length - 1; i >= 0; i--) {
                    if (label[i] !== target.parentNode)
                        label[i].classList.remove("checked" + target.name);
                }

                if (target.parentNode.classList.contains("checked" + target.name)) {
                    objStr[target.name] = target.value;
                    AJAX(objStr);
                }
                else {
                    delete objStr[target.name];
                    target.checked = false;
                    AJAX(objStr);
                }
            } else {
                return
            }

        });
    }

    function AJAX(objStr) {
        var str = '';
        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
                document.querySelector("#screenshots").innerHTML = xmlhttp.responseText;
                $grid.masonry();
                window.history.pushState('', '', window.location.pathname+'?'+str);
            } else if(xmlhttp.readyState === 4 && xmlhttp.status !== 200) {
                alert('Sorry some trouble in server.')
            }
        };
        var counter = 0;
        for (key in objStr) {
            if (counter > 0) {
                str += '&' + key + '=' + objStr[key];
            } else {
                str += key + '=' + objStr[key];
                counter++;
            }

        }

        console.log(str);
        xmlhttp.open('GET', window.location.pathname+'?'+str, true);
        xmlhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xmlhttp.send();
    }
})($grid);