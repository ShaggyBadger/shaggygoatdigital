// Mobile menu: close after choosing a link, on Escape, on an outside tap, and
// when the layout switches back to the desktop nav. The <details> element opens
// and closes on its own without this file.
const menu = document.querySelector(".nav-menu");

if (menu) {
  const toggle = menu.querySelector("summary");

  menu.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
      menu.open = false;
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && menu.open) {
      menu.open = false;
      toggle.focus();
    }
  });

  document.addEventListener("click", (event) => {
    if (menu.open && !menu.contains(event.target)) {
      menu.open = false;
    }
  });

  const desktop = window.matchMedia("(min-width: 901px)");
  desktop.addEventListener("change", (event) => {
    if (event.matches) {
      menu.open = false;
    }
  });
}
