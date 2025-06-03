document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("hamburger-button");
  const menu = document.getElementById("dropdown-menu");

  button.addEventListener("click", () => {
    menu.classList.toggle("hidden");
  });

  document.addEventListener("click", (e) => {
    if (!button.contains(e.target) && !menu.contains(e.target)) {
      menu.classList.add("hidden");
    }
  });
});
