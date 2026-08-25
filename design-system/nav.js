(function () {
  const nav = document.querySelector(".topnav");
  const links = nav && nav.querySelector(".topnav-links");
  if (!nav || !links) return;

  document.documentElement.classList.add("has-nav-js");

  if (!links.id) links.id = "topnav-links";

  const toggle = document.createElement("button");
  toggle.type = "button";
  toggle.className = "topnav-toggle";
  toggle.setAttribute("aria-expanded", "false");
  toggle.setAttribute("aria-controls", links.id);
  toggle.setAttribute("aria-label", "Open menu");
  toggle.innerHTML =
    '<span class="topnav-toggle-icon" aria-hidden="true">' +
    "<span></span><span></span><span></span>" +
    "</span>";

  const divider = nav.querySelector(".topnav-divider");
  nav.insertBefore(toggle, divider || links);

  function setOpen(open) {
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  }

  function isMobileNav() {
    return window.matchMedia("(max-width: 720px)").matches;
  }

  toggle.addEventListener("click", function () {
    setOpen(!nav.classList.contains("is-open"));
  });

  links.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      if (isMobileNav()) setOpen(false);
    });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && nav.classList.contains("is-open")) {
      setOpen(false);
      toggle.focus();
    }
  });

  document.addEventListener("click", function (event) {
    if (!nav.classList.contains("is-open")) return;
    if (!nav.contains(event.target)) setOpen(false);
  });

  window.matchMedia("(max-width: 720px)").addEventListener("change", function (event) {
    if (!event.matches) setOpen(false);
  });
})();
