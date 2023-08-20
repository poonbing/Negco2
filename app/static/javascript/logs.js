const searchInput = document.getElementById("table-search-logs");
const table = document.getElementById("logs-table");
const checkboxes = table.querySelectorAll('input[type="checkbox"]');
const checkboxAll = document.getElementById("checkbox-all");

searchInput.addEventListener("input", function (e) {
  const searchString = e.target.value.toLowerCase();
  const rows = table
    .getElementsByTagName("tbody")[0]
    .getElementsByTagName("tr");

  for (let row of rows) {
    const timestamp = row
      .getElementsByTagName("th")[0]
      .innerText.toLowerCase();
    const source = row.getElementsByTagName("td")[0].innerText.toLowerCase();
    const logged_user = row.getElementsByTagName("td")[1].innerText.toLowerCase();
    const address = row.getElementsByTagName("td")[2].innerText.toLowerCase();
    const category = row.getElementsByTagName("td")[2].innerText.toLowerCase();
    const text = row.getElementsByTagName("td")[2].innerText.toLowerCase();



    if (
      timestamp.includes(searchString) ||
      source.includes(searchString) ||
      logged_user.includes(searchString) ||
      address.includes(searchString) ||
      category.includes(searchString) ||
      text.includes(searchString) 
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

fetch("/get_logs_data")
  .then((response) => response.json())
  .then((data) => {
    const tbody = table.querySelector("tbody");
    table.classList.remove("shadow");
    table.classList.remove("animate-pulse");
    tbody.textContent = "";
    const logs = data;

    logs.forEach((log) => {
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
      checkboxInput.id = `checkbox-table-${log.id}`;
      checkboxInput.type = "checkbox";
      checkboxInput.className =
        "w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 dark:focus:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600";
      const checkboxLabel = document.createElement("label");
      checkboxLabel.setAttribute("for", `checkbox-table-${log.id}`);
      checkboxLabel.className = "sr-only";
      checkboxDiv.appendChild(checkboxInput);
      checkboxDiv.appendChild(checkboxLabel);
      checkboxCell.appendChild(checkboxDiv);
      row.appendChild(checkboxCell);

      // Create timestamp cell
      const timestampCell = document.createElement("th");
      timestampCell.setAttribute("scope", "row");
      timestampCell.className =
        "px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white";
      timestampCell.textContent = log.timestamp;
      row.appendChild(timestampCell);


      // Create source cell
      const loggedUserCell = document.createElement("td");
      loggedUserCell.className = "px-6 py-4";
      loggedUserCell.textContent = log.logged_user;
      row.appendChild(loggedUserCell);

      // Create address cell
      const addressCell = document.createElement("td");
      addressCell.className = "px-6 py-4";
      addressCell.textContent = log.address;
      row.appendChild(addressCell);

      // Create Category Cell
      const categoryCell = document.createElement("td");
      categoryCell.className = "px-6 py-4";
      categoryCell.textContent = log.category;
      row.appendChild(categoryCell);

      // Create text cell
      const textCell = document.createElement("td");
      textCell.className = "px-6 py-4";
      textCell.textContent = log.text;
      row.appendChild(textCell);


      // Create action cell
      const actionCell = document.createElement("td");
      const editLink = document.createElement("a");
      editLink.href = `/${log.id}/settings`;
      editLink.className =
        "font-medium text-blue-600 dark:text-blue-500 hover:underline px-3";
      editLink.textContent = "Edit";
      const deleteLink = document.createElement("a");
      deleteLink.href = `/delete/${log.id}`;
      deleteLink.className =
        "font-medium text-red-600 dark:text-red-500 hover:underline px-3";
      deleteLink.textContent = "Delete";
      deleteLink.onclick = function () {
        return confirm("Are you sure you want to delete this log?");
      };
      actionCell.appendChild(editLink);
      actionCell.appendChild(deleteLink);
      row.appendChild(actionCell);

      // Append the row to the table body
      tbody.appendChild(row);
    });
  });