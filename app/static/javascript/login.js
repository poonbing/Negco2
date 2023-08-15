// login.js
    const passwordToggle = document.querySelector(".js-password-toggle");
    const showIcon = document.querySelector(".js-show-icon");
    const hideIcon = document.querySelector(".js-hide-icon");
  
    passwordToggle.addEventListener("change", function () {
      const password = document.querySelector(".js-password");
  
      if (password.type === "password") {
        password.type = "text";
        showIcon.classList.add("hidden");
        hideIcon.classList.remove("hidden");
      } else {
        password.type = "password";
        showIcon.classList.remove("hidden");
        hideIcon.classList.add("hidden");
      }
  
      password.focus();
    });
