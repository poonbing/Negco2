const copyButton = document.getElementById("copyButton");
const apiValue = document.getElementById("apiValue");

copyButton.addEventListener("click", () => {
  const textToCopy = apiValue.innerText;

  navigator.clipboard
    .writeText(textToCopy)
    .then(() => {
      console.log("Text copied to clipboard:", textToCopy);
    })
    .catch((error) => {
      console.error("Error copying text:", error);
    });
});

document.addEventListener("DOMContentLoaded", function() {
  document.querySelector("form").addEventListener("submit", function(event) {
      const profilePicture = document.getElementById("profile_picture").files[0];
      const firstName = document.getElementById("first_name").value;
      const lastName = document.getElementById("last_name").value;
      const phone = document.getElementById("phone").value;
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;
      const confirmPassword = document.getElementById("confirm_password").value;

      if (profilePicture) {
          const allowedExtensions = /(\.jpg|\.png)$/i;
          if (!allowedExtensions.exec(profilePicture.name)) {
              event.preventDefault();  // prevent form submission
              return alert("Invalid file type for Profile Picture. Only JPG and PNG images are allowed.");
          }
      }

      if (!firstName) {
          event.preventDefault();
          return alert("First Name is required.");
      }

      if (!lastName) {
          event.preventDefault();
          return alert("Last Name is required.");
      }

      if (phone.length < 8 || phone.length > 16) {
          event.preventDefault();
          return alert("Phone number must be between 8 and 16 characters.");
      }

      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
      if (email && !emailPattern.test(email)) {
          event.preventDefault();
          return alert("Invalid email format.");
      }

      if (password || confirmPassword) {
          if (password !== confirmPassword) {
              event.preventDefault();
              return alert("Passwords do not match.");
          }
      }
  });
});