export async function tableLogic() {

  const table = document.querySelector("table[data-name]");

  const name = table.dataset.name;
  const tablehead = document.getElementById("table-head");
  const tablebody = document.getElementById("table-body");

  try {
    const headers = JSON.parse(document.getElementById("headers").textContent);
    tablehead.innerHTML = `<th>ID</th>`;
    tablehead.setAttribute("scope", "col");

    headers.forEach(field => {
      tablehead.innerHTML += `<th>${field.charAt(0).toUpperCase() + field.slice(1)}</th>`;
    });

    const data = JSON.parse(document.getElementById("data-structure").textContent);

    tablebody.innerHTML = "";

    data.forEach(item => {
      let row = `
        <tr>
          <td>
            <input class="form-check-input row-checkbox" type="checkbox" data-id="${item.id}">
            <label class="form-check-label">${item.id}</label>
          </td>
      `;

    for (const key in item) {
      if (key !== "id") {

        if (key === "disponibilite") {
          const badgeClass = item[key] ? "badge-success" : "badge-failure";
          const badgeText = item[key] ? "Disponible" : "Non Disponible";
          row += `<td><span class="badge ${badgeClass}">${badgeText}</span></td>`;
        
        } else if (key === "resolu") {
          const badgeClass = item[key] ? "badge-success" : "badge-failure";
          const badgeText = item[key] ? "Oui" : "Non";
          row += `<td><span class="badge ${badgeClass}">${badgeText}</span></td>`;

        } else if (key === "statut") {
            let badgeClass = "";
            if (item[key] === "en_cours") badgeClass = "badge-warning";
            else if (item[key] === "resolue") badgeClass = "badge-success";
            else if (item[key] === "annulee") badgeClass = "badge-failure";

            const badgeText = item[key].charAt(0).toUpperCase() + item[key].slice(1);
            row += `<td><span class="badge ${badgeClass}">${badgeText}</span></td>`;
        
        } else {
          row += `<td>${item[key]}</td>`;
        }

      }
    }

      row += `</tr>`;
      tablebody.innerHTML += row;
    });

  } catch (error) {
    console.error("Failed to load table:", error);
  }
}