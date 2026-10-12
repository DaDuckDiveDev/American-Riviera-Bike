/* Header behaviour: mobile menu toggle and the compact "stuck" state on desktop. */
(function () {
  var header = document.getElementById('site-header');
  if (!header) return;
  var toggle = header.querySelector('.sh-toggle');
  var nav = header.querySelector('.sh-nav');

  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    toggle.addEventListener('click', function () {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setOpen(false);
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) setOpen(false);
    });
  }

  /* Two thresholds so the bar does not flicker around the switch point. */
  var stuck = false, ticking = false;
  var update = function () {
    ticking = false;
    var y = window.pageYOffset || document.documentElement.scrollTop;
    if (!stuck && y > 160) { stuck = true; header.classList.add('is-stuck'); }
    else if (stuck && y < 40) { stuck = false; header.classList.remove('is-stuck'); }
  };
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; window.requestAnimationFrame(update); }
  }, { passive: true });
  update();
})();
