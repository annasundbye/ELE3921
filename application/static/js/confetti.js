document.addEventListener("DOMContentLoaded", () => {
  const duration = 3 * 1000;
  const animationEnd = Date.now() + duration;

  (function frame() {
    confetti({
      particleCount: 3,
      angle: 60,
      spread: 55,
      origin: { x: 0 },
    });
    confetti({
      particleCount: 3,
      angle: 120,
      spread: 55,
      origin: { x: 1 },
    });

    if (Date.now() < animationEnd) {
      requestAnimationFrame(frame);
    }
  })();
});
