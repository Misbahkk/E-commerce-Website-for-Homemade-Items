// Toggle hamburger menu
document.querySelectorAll('.product-card').forEach((card) => {
    card.addEventListener('click', () => {
      alert('Product added to cart!');
    });
  });
  


// For Filters
document.addEventListener("DOMContentLoaded", function() {
  var filterBtn = document.getElementById('filter-btn');
  var btnTxt = document.getElementById('btn-txt');
  var filterAngle = document.getElementById('filter-angle');
  
  $('#filterbar').collapse(false);
  var count = 0, count2 = 0;
  function changeBtnTxt() {
  $('#filterbar').collapse(true);
  count++;
  if (count % 2 != 0) {
  filterAngle.classList.add("fa-angle-right");
  btnTxt.innerText = "show filters"
  filterBtn.style.backgroundColor = "#36a31b";
  }
  else {
  filterAngle.classList.remove("fa-angle-right")
  btnTxt.innerText = "hide filters"
  filterBtn.style.backgroundColor = "#ff935d";
  }
  
  }
  
  // For Applying Filters
  $('#inner-box').collapse(false);
  $('#inner-box2').collapse(false);
  
  // For changing NavBar-Toggler-Icon
  var icon = document.getElementById('icon');
  
  function chnageIcon() {
  count2++;
  if (count2 % 2 != 0) {
  icon.innerText = "";
  icon.innerHTML = '<span class="far fa-times-circle" style="width:100%"></span>';
  icon.style.paddingTop = "5px";
  icon.style.paddingBottom = "5px";
  icon.style.fontSize = "1.8rem";
  
  
  }
  else {
  icon.innerText = "";
  icon.innerHTML = '<span class="navbar-toggler-icon"></span>';
  icon.style.paddingTop = "5px";
  icon.style.paddingBottom = "5px";
  icon.style.fontSize = "1.2rem";
  }
  }
  
  // Showing tooltip for AVAILABLE COLORS
  $(function () {
  $('[data-tooltip="tooltip"]').tooltip()
  })
  
  // For Range Sliders
  var inputLeft = document.getElementById("input-left");
  var inputRight = document.getElementById("input-right");
  
  var thumbLeft = document.querySelector(".slider > .thumb.left");
  var thumbRight = document.querySelector(".slider > .thumb.right");
  var range = document.querySelector(".slider > .range");
  
  var amountLeft = document.getElementById('amount-left')
  var amountRight = document.getElementById('amount-right')
  
  function setLeftValue() {
  var _this = inputLeft,
  min = parseInt(_this.min),
  max = parseInt(_this.max);
  
  _this.value = Math.min(parseInt(_this.value), parseInt(inputRight.value) - 1);
  
  var percent = ((_this.value - min) / (max - min)) * 100;
  
  thumbLeft.style.left = percent + "%";
  range.style.left = percent + "%";
  amountLeft.innerText = parseInt(percent * 100);
  }
  setLeftValue();
  
  function setRightValue() {
  var _this = inputRight,
  min = parseInt(_this.min),
  max = parseInt(_this.max);
  
  _this.value = Math.max(parseInt(_this.value), parseInt(inputLeft.value) + 1);
  
  var percent = ((_this.value - min) / (max - min)) * 100;
  
  amountRight.innerText = parseInt(percent * 100);
  thumbRight.style.right = (100 - percent) + "%";
  range.style.right = (100 - percent) + "%";
  }
  setRightValue();
  
  inputLeft.addEventListener("input", setLeftValue);
  inputRight.addEventListener("input", setRightValue);
  
  inputLeft.addEventListener("mouseover", function () {
  thumbLeft.classList.add("hover");
  });
  inputLeft.addEventListener("mouseout", function () {
  thumbLeft.classList.remove("hover");
  });
  inputLeft.addEventListener("mousedown", function () {
  thumbLeft.classList.add("active");
  });
  inputLeft.addEventListener("mouseup", function () {
  thumbLeft.classList.remove("active");
  });
  
  inputRight.addEventListener("mouseover", function () {
  thumbRight.classList.add("hover");
  });
  inputRight.addEventListener("mouseout", function () {
  thumbRight.classList.remove("hover");
  });
  inputRight.addEventListener("mousedown", function () {
  thumbRight.classList.add("active");
  });
  inputRight.addEventListener("mouseup", function () {
  thumbRight.classList.remove("active");
  });
  });



  
  function confirmLogout(event) {
    event.preventDefault(); // Prevent the default action of the link

    Swal.fire({
        title: 'Are you sure?',
        text: "You will be logged out!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#FF6F61',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, logout',
        cancelButtonText: 'No, stay'
    }).then((result) => {
        if (result.isConfirmed) {
            // Redirect to the logout URL
            window.location.href = "{% url 'logout' %}";
        }
    });
}


document.querySelectorAll("input").forEach((input) => {
  input.addEventListener("dblclick", () => {
      input.removeAttribute("readonly");
  });
});

// function incrementQuantity(cartItemId) {
//   let quantityInput = document.querySelector(`#quantity-input-${cartItemId}`);
//   quantityInput.value = parseInt(quantityInput.value) + 1;
// }

// function decrementQuantity(cartItemId) {
//   let quantityInput = document.querySelector(`#quantity-input-${cartItemId}`);
//   if (parseInt(quantityInput.value) > 1) {
//       quantityInput.value = parseInt(quantityInput.value) - 1;
//   }
// }


function updateQuantity(cartItemId, change) {
  var quantityInput = $('#quantity-' + cartItemId);
  var newQuantity = parseInt(quantityInput.val()) + change;

  if (newQuantity < 1) {
      alert('Quantity must be greater than 0.');
      return;
  }

  $.ajax({
      url: "{% url 'update_quantity' %}",
      method: "POST",
      data: {
          'cart_item_id': cartItemId,
          'quantity': newQuantity,
          'csrfmiddlewaretoken': '{{ csrf_token }}'
      },
      success: function(response) {
          if (response.status === 'success') {
              quantityInput.val(newQuantity);
              $('#total-price-' + cartItemId).text('$' + response.total_price);
              $('#subtotal').text('$' + response.cart_total_price);
              $('#grandtotal').text('$' + (response.cart_total_price));
          } else {
              alert(response.message);
          }
      },
      error: function() {
          alert('An error occurred while updating the quantity.');
      }
  });
}