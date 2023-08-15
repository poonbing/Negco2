const searchInput = document.getElementById("table-search-users");
const table = document.getElementById("users-table");
const checkboxes = table.querySelectorAll('input[type="checkbox"]');
const checkboxAll = document.getElementById("checkbox-all");

searchInput.addEventListener("input", function (e) {
  const searchString = e.target.value.toLowerCase();
  const rows = table
    .getElementsByTagName("tbody")[0]
    .getElementsByTagName("tr");

  for (let row of rows) {
    const username = row
      .getElementsByTagName("th")[0]
      .innerText.toLowerCase();
    const name = row.getElementsByTagName("td")[0].innerText.toLowerCase();
    const role = row.getElementsByTagName("td")[1].innerText.toLowerCase();
    const email = row.getElementsByTagName("td")[2].innerText.toLowerCase();

    if (
      username.includes(searchString) ||
      name.includes(searchString) ||
      role.includes(searchString) ||
      email.includes(searchString)
    ) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  }
});

checkboxAll.addEventListener("change", function (e) {
  const isChecked = e.target.checked;

  for (let checkbox of checkboxes) {
    checkbox.checked = isChecked;
  }
});

fetch("/get_users_data")
  .then((response) => response.json())
  .then((data) => {
    const tbody = table.querySelector("tbody");
    table.classList.remove("shadow");
    table.classList.remove("animate-pulse");
    tbody.textContent = "";
    const users = data;

    users.forEach((user) => {
      const row = document.createElement("tr");
      row.classList.add(
        "bg-white",
        "border-b",
        "dark:bg-gray-800",
        "dark:border-gray-700",
        "hover:bg-gray-50",
        "dark:hover:bg-gray-600"
      );

      // Create checkbox cell
      const checkboxCell = document.createElement("td");
      checkboxCell.className = "w-4 p-4";
      const checkboxDiv = document.createElement("div");
      checkboxDiv.className = "flex items-center";
      const checkboxInput = document.createElement("input");
      checkboxInput.id = `checkbox-table-${user.id}`;
      checkboxInput.type = "checkbox";
      checkboxInput.className =
        "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600";
      const checkboxLabel = document.createElement("label");
      checkboxLabel.setAttribute("for", `checkbox-table-${user.id}`);
      checkboxLabel.className = "sr-only";
      checkboxDiv.appendChild(checkboxInput);
      checkboxDiv.appendChild(checkboxLabel);
      checkboxCell.appendChild(checkboxDiv);
      row.appendChild(checkboxCell);

      // Create username cell
      const usernameCell = document.createElement("th");
      usernameCell.setAttribute("scope", "row");
      usernameCell.className =
        "px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white";
      usernameCell.textContent = user.username;
      row.appendChild(usernameCell);

      // Create name cell
      const nameCell = document.createElement("td");
      nameCell.className = "px-6 py-4";
      nameCell.textContent = `${user.first_name} ${user.last_name}`;
      row.appendChild(nameCell);

      // Create role cell
      const roleCell = document.createElement("td");
      roleCell.className = "px-6 py-4";
      roleCell.textContent = user.role;
      row.appendChild(roleCell);

      // Create email cell
      const emailCell = document.createElement("td");
      emailCell.className = "px-6 py-4";
      emailCell.textContent = user.email;
      row.appendChild(emailCell);

      // Create action cell
      const actionCell = document.createElement("td");
      const editLink = document.createElement("a");
      editLink.href = `/${user.id}/settings`;
      editLink.className =
        "font-medium text-blue-600 dark:text-blue-500 hover:underline px-3";
      editLink.textContent = "Edit";
      const deleteLink = document.createElement("a");
      deleteLink.href = `/delete/${user.id}`;
      deleteLink.className =
        "font-medium text-red-600 dark:text-red-500 hover:underline px-3";
      deleteLink.textContent = "Delete";
      deleteLink.onclick = function () {
        return confirm("Are you sure you want to delete this user?");
      };
      actionCell.appendChild(editLink);
      actionCell.appendChild(deleteLink);
      row.appendChild(actionCell);

      // Append the row to the table body
      tbody.appendChild(row);
    });
  });