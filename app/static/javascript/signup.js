document.addEventListener("DOMContentLoaded", function() {
    document.querySelector("form").addEventListener("submit", function(event) {
        let errorMessages = [];

        // First Name Validation
        const firstName = document.querySelector("[name='first_name']").value;
        if (!firstName || firstName.length < 5 || firstName.length > 49) {
            errorMessages.push("First Name should be between 5 to 49 characters.");
        }

        // Last Name Validation
        const lastName = document.querySelector("[name='last_name']").value;
        if (!lastName || lastName.length < 5 || lastName.length > 49) {
            errorMessages.push("Last Name should be between 5 to 49 characters.");
        }

        // Username Validation
        const username = document.querySelector("[name='username']").value;
        const usernamePattern = /^[a-zA-Z0-9_-]{5,49}$/;
        if (!usernamePattern.test(username)) {
            errorMessages.push("Invalid username format. Only letters, numbers, underscores, and hyphens are allowed.");
        }

        // Email Validation
        const email = document.querySelector("[name='email']").value;
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailPattern.test(email)) {
            errorMessages.push("Invalid email format.");
        }

        // Password Validation
        const password = document.querySelector("[name='password']").value;
        const passwordError = validatePassword(password);
        if (passwordError) {
            errorMessages.push(passwordError);
        }

        // Confirm Password Validation
        const confirmPassword = document.querySelector("[name='confirm_password']").value;
        if (confirmPassword !== password) {
            errorMessages.push("Passwords do not match.");
        }

        // Age Validation
        const age = document.querySelector("[name='age']").value;
        if (isNaN(age) || age < 0 || age > 200) {
            errorMessages.push("Age must be between 0 and 200.");
        }

        // Phone Validation
        const phone = document.querySelector("[name='phone']").value;
        const phonePattern = /^\d{8}$/;
        if (!phonePattern.test(phone)) {
            errorMessages.push("Phone number must be exactly eight digits.");
        }

        // If any error messages were added to the array, prevent submission
        if (errorMessages.length > 0) {
            event.preventDefault();
            alert(errorMessages.join("\n"));
        }

    });
    
    // Password Validation Function (same as provided in the earlier message)
    function validatePassword(password) {
        const lengthError = password.length < 8;
        const digitError = !/\d/.test(password);
        const uppercaseError = !/[A-Z]/.test(password);
        const lowercaseError = !/[a-z]/.test(password);
        const symbolError = !/[ !#$%&'()*+,-./[\]\\^_`{|}~"]/.test(password);
        
        if (lengthError || digitError || uppercaseError || lowercaseError || symbolError) {
            return "Password must be at least 8 characters long and contain at least one digit, one uppercase letter, one lowercase letter, and one symbol.";
        }
        return null;
    }
});