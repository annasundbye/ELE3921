document.addEventListener("DOMContentLoaded", () => {
  const quantityEl = document.getElementById("quantity");
  const sizeMultiplier = {
    small: 1.0,
    medium: 1.1,
    large: 1.2,
    "x-large": 1.3,
  };

  const selectedToppings = new Set();
  let selectedSize = "medium";
  let selectedDrinkId = null;

  let sizeInput = document.querySelector("input#size");
  let toppingsInput = document.querySelector("input#extra-toppings");
  let drinkInput = document.querySelector("input#drink-id");

  document.getElementById("sub").addEventListener("click", () => {
    const qty = Math.max(1, parseInt(quantityEl.innerText) - 1);
    quantityEl.innerText = qty;
  });

  document.getElementById("add").addEventListener("click", () => {
    const qty = parseInt(quantityEl.innerText) + 1;
    quantityEl.innerText = qty;
  });

  function updateToppingPrices() {
    const multiplier = sizeMultiplier[selectedSize];

    document.querySelectorAll("[id^='extra-topping-']").forEach((btn) => {
      const basePrice = parseFloat(btn.dataset.price);
      const newPrice = Math.round(basePrice * multiplier * 100) / 100;
      const pTag = btn.getElementsByClassName("topping-price")[0];

      if (pTag) {
        pTag.innerHTML = `+${newPrice.toFixed(2)},-`;
      }
    });
  }

  // Select Size
  document.querySelectorAll("[id^='size-']").forEach((btn) => {
    btn.addEventListener("click", () => {
      sizeInput.value = btn.dataset.id;

      // Highlight selected
      document.querySelectorAll("[id^='size-']").forEach((b) => {
        b.classList.remove("border-[var(--color-pink)]");
        b.classList.add("border-gray-300");
      });
      btn.classList.add("border-[var(--color-pink)]");
      btn.classList.remove("border-gray-300");

      updateToppingPrices();
    });
  });

  // default size is medium
  const defaultBtn = document.querySelector('[id="size-medium"]');
  if (defaultBtn) {
    defaultBtn.click();
  }

  // Select Toppings
  document.querySelectorAll("[id^='extra-topping-']").forEach((btn) => {
    btn.addEventListener("click", () => {
      const toppingId = btn.dataset.id;

      if (selectedToppings.has(toppingId)) {
        selectedToppings.delete(toppingId);
        btn.classList.remove("border-[var(--color-pink)]");
        btn.classList.add("border-gray-300");
      } else {
        selectedToppings.add(toppingId);
        btn.classList.add("border-[var(--color-pink)]");
        btn.classList.remove("border-gray-300");
      }

      toppingsInput.value = Array.from(selectedToppings).join(",");
      console.log(toppingsInput.value);
    });
  });

  // Select Drink
  document.querySelectorAll("[id^='drink-id-']").forEach((btn) => {
    btn.addEventListener("click", () => {
      selectedDrinkId = btn.dataset.id;
      drinkInput.value = selectedDrinkId;

      // Deselect all others
      document.querySelectorAll("[id^='drink-id-']").forEach((b) => {
        b.classList.remove("border-[var(--color-pink)]", "ring-2");
      });
      btn.classList.add("border-[var(--color-pink)]", "ring-2");
    });
  });
});
