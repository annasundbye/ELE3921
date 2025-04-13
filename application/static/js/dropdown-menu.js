document.addEventListener("DOMContentLoaded", () => {
  const hamburgerButton = document.getElementById("hamburger-button");
  const navMenu = document.getElementById("dropdown-menu");

  hamburgerButton.addEventListener("click", () => {
    navMenu.classList.toggle("hidden");
  });
});
