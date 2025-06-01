document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const quantity = document.getElementById("quantity");
  const customQuantity = document.getElementById("custom-quantity");
  const finalQuantity = document.getElementById("final-quantity");
  const toppingElements = document.querySelectorAll(".topping-option");
  const extraToppingsInput = document.getElementById("extra-toppings");
  const drinkElements = document.querySelectorAll(".drink-option");
  const drinkIdInput = document.getElementById("drink-id");
  const sizeSelect = document.getElementById("select-pizza-size");

  // State
  const selectedToppings = new Set();
  const sizeMultipliers = {
    small: 1.0,
    medium: 1.25,
    large: 1.5,
  };

  //  Quantity Logic
  function syncFinalQuantity() {
    finalQuantity.value = quantity.innerText;
  }

  quantity.addEventListener("click", () => {
    customQuantity.value = quantity.innerText;
    quantity.classList.add("hidden");
    customQuantity.classList.remove("hidden");
    customQuantity.focus();
  });

  customQuantity.addEventListener("change", () => {
    const newVal = parseInt(customQuantity.value);
    if (!isNaN(newVal) && newVal >= 0) {
      quantity.innerText = newVal;
    }
    customQuantity.classList.add("hidden");
    quantity.classList.remove("hidden");
    syncFinalQuantity();
  });

  document.getElementById("sub").addEventListener("click", () => {
    const currentQuantity = parseInt(quantity.innerText);
    quantity.innerText = Math.max(currentQuantity - 1, 0);
    syncFinalQuantity();
  });

  document.getElementById("add").addEventListener("click", () => {
    const currentQuantity = parseInt(quantity.innerText);
    quantity.innerText = currentQuantity + 1;
    syncFinalQuantity();
  });

  //  Toppings Logic
  toppingElements.forEach((el) => {
    el.addEventListener("click", () => {
      const toppingId = el.dataset.id;
      const addedCell = el.querySelector("td:last-child");

      if (selectedToppings.has(toppingId)) {
        selectedToppings.delete(toppingId);
        el.classList.remove("selected");
        if (addedCell) addedCell.textContent = "";
      } else {
        selectedToppings.add(toppingId);
        el.classList.add("selected");
        if (addedCell) addedCell.textContent = "✅";
      }

      extraToppingsInput.value = Array.from(selectedToppings).join(",");
    });
  });

  //  Drink Logic
  drinkElements.forEach((el) => {
    el.addEventListener("click", () => {
      const drinkId = el.dataset.id;
      drinkIdInput.value = drinkId;
    });
  });

  //  Size-based Topping Price Update
  function updateToppingPrices() {
    const selectedSize = sizeSelect.value;
    const multiplier = sizeMultipliers[selectedSize] || 1.0;

    toppingElements.forEach((el) => {
      const basePrice = parseFloat(el.dataset.price);
      const priceCell = el.querySelector(".topping-price");
      const newPrice = (basePrice * multiplier).toFixed(2);
      if (priceCell) {
        priceCell.textContent = `${newPrice},-`;
      }
    });
  }

  if (sizeSelect) {
    sizeSelect.addEventListener("change", updateToppingPrices);
    updateToppingPrices(); // Initial run
  }
});
