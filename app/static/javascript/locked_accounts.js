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