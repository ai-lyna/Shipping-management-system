export async function openAddModal({ infoModalEl, infoModal, modalBody, name }) {
  infoModalEl.dataset.mode = "create";
  delete infoModalEl.dataset.id;

  modalBody.innerHTML = "";
  infoModal.show();
  history.replaceState(null, "", `/${name}/`);

  const res = await fetch(`/${name}/info/`);
  if (!res.ok) throw new Error("Data not found");

  const fields = await res.json();
  const typeMap = { string: "text", number: "number", email: "email" };

  for (let key in fields) {
    const div = document.createElement("div");
    div.classList.add("mb-3");

    const label = document.createElement("h6");
    label.textContent = key.replace(/_/g, " ").replace(/^\w/, c => c.toUpperCase());
    div.appendChild(label);

    if (fields[key] === "boolean") {
      div.innerHTML += `
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="${key}" value="true" checked> Oui
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="radio" name="${key}" value="false"> Non
        </div>
      `;
    } else if (fields[key].type === "choice") {
      const select = document.createElement("select");
      select.classList.add("form-select");
      select.name = key;

      fields[key].choices.forEach(opt => {
        const option = document.createElement("option");
        option.value = opt.value;
        option.textContent = opt.label;
        select.appendChild(option);
      });

      div.appendChild(select);
    } else {
      const input = document.createElement("input");
      input.type = typeMap[fields[key]] || "text";
      input.classList.add("form-control");
      input.name = key;
      div.appendChild(input);
    }

    modalBody.appendChild(div);
  }
}
