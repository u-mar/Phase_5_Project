(function () {
  document.addEventListener('DOMContentLoaded', function (e) {
    var isIE = /msie|trident|edge/g.test(navigator.userAgent.toLowerCase());
    if (!isIE) {
      // This script should only run in Internet Explorer!
      return;
    }
    var main = document.querySelector("main");
    var banner = Banner(main);
    var popup = Popup();
    popup.show();
  });

  var Banner = function (target) {
    const template = document.createElement("div");
    template.classList.add("ie-banner");
    template.innerHTML = '<div class="ie-banner__container container clearfix"><div class="ie-banner__left"><img width="211" height="102" src="/static/images/ie-logo.png"></div><div class="ie-banner__right"><h2>Internet Explorer is no longer supported</h2><p>Some features of the Climate Action Tracker website might not work correctly, please upgrade your browser for a better experience.</p></div></div>';
    target.insertBefore(template, target.firstChild);
    return template;
  }

  var Popup = function () {
    const popup = document.createElement("div");
    popup.classList.add("ie-popup");
    popup.classList.add("ie-popup--hidden");
    popup.innerHTML = '<button title="Close popup" class="ie-popup__close"><span class="icon icon-icons_24"></span></button><img width="411" height="197" src="/static/images/ie-logo-large.png"><div class="ie-popup__text"><h2>Internet Explorer is no longer supported</h2><p>Some features of the Climate Action Tracker website might not work correctly, please upgrade your browser for a better experience.</p></div>';
    document.body.appendChild(popup);

    popup.querySelector("button").addEventListener("click", function (e) {
      e.preventDefault();
      hide();
    });

    function show() {
      popup.classList.remove("ie-popup--hidden");
    }

    function hide() {
      popup.classList.add("ie-popup--hidden");
    }

    return {
      show: show,
      hide: hide
    }
  };
})();
