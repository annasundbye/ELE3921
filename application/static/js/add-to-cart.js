document.addEventListener("DOMContentLoaded", () => {
  const quantity = document.getElementById("quantity");
  const customQuantity = document.getElementById("custom-quantity");

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
  });

  document.getElementById("sub").addEventListener("click", () => {
    const currentQuantity = parseInt(quantity.innerText);
    if (currentQuantity <= 0) {
      quantity.innerText = 0;
    } else {
      quantity.innerText = currentQuantity - 1;
    }
  });
  document.getElementById("add").addEventListener("click", () => {
    const currentQuantity = parseInt(quantity.innerText);
    quantity.innerText = currentQuantity + 1;
  });
});
