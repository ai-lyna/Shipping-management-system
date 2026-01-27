export function btnLogic() {
  const actionBar = document.getElementById("actionBar");
  const viewBtn = document.getElementById("viewBtn");
  const editBtn = document.getElementById("editBtn"); 
  const addBtn = document.getElementById("addBtn");
  const deleteBtn = document.getElementById("deleteBtn");
  const saveBtn = document.getElementById("savebtn");
  const table = document.querySelector("table[data-name]");
  const name = table.dataset.name;

  const infoModalEl = document.getElementById("infoModal");
  const infoModal = new bootstrap.Modal(infoModalEl);
  const modalBody = infoModalEl.querySelector(".modal-body");


  function updateActionBar() {
    const currentCheckboxes = document.querySelectorAll('.row-checkbox');
    const checked = Array.from(currentCheckboxes).filter(cb => cb.checked);
    
    if (checked.length > 0) {
      actionBar.classList.remove('d-none');
      actionBar.classList.add('d-flex');
      viewBtn.disabled = checked.length !== 1;
      editBtn.disabled = checked.length !== 1;
    } else {
      actionBar.classList.remove('d-flex');
      actionBar.classList.add('d-none');
    }
  }

  document.addEventListener("change", function (e) {
        if (e.target.classList.contains("row-checkbox")) {
            updateActionBar();
        }
  });


  function openEditModal(id) {
    infoModalEl.dataset.mode = "edit";
    infoModal.show();
    history.pushState({ modal: "edit", id }, "", `/${name}/${id}/edit/`);
  }

  function openViewModal(id) {
    infoModal.show();
    history.pushState({ modal: "view", id }, "", `/${name}/${id}/`);
  }

  function openAddModal() {
    infoModalEl.dataset.mode = "create";
    infoModal.show();
    history.replaceState(null, "", `/${name}/`);
  }


  
  viewBtn.addEventListener("click", async () => {
    const checked = document.querySelectorAll('.row-checkbox:checked');
    if (checked.length !== 1) return;
    const id = checked[0].dataset.id;

    try {
      const response = await fetch(`/${name}/${id}`);
      if (!response.ok) throw new Error("Data not found");
      const data = await response.json();

      modalBody.innerHTML = "";
      for (let key in data) {
        const div = document.createElement("div");
        div.classList.add("mb-4");

        const label = document.createElement("h6");
        label.textContent = key.charAt(0).toUpperCase() + key.slice(1);

        const value = document.createElement("p");
        value.textContent = data[key];

        div.appendChild(label);
        div.appendChild(value);
        modalBody.appendChild(div);
      }

      openViewModal(id);
    } catch (err) {
      console.error(err);
    }
  });




  editBtn.addEventListener("click", async () => {
    const checked = document.querySelectorAll('.row-checkbox:checked');
    if (checked.length !== 1) return;
    const id = checked[0].dataset.id;

    try {
      const response = await fetch(`/${name}/${id}`);
      if (!response.ok) throw new Error("Data not found");
      const data = await response.json();

      infoModalEl.dataset.id = id;

      modalBody.innerHTML = "";
      saveBtn.classList.remove("d-none");
      saveBtn.classList.add("d-inline-flex");

      for (let key in data) {
        if (key === "id" || key === "date_creation") continue;
        
        const div = document.createElement("div");
        div.classList.add("mb-2", "gap-4");

        const label = document.createElement("h6");
        label.classList.add("mb-2");
        label.textContent = key.charAt(0).toUpperCase() + key.slice(1);

        const input = document.createElement("input");
        input.type = "text";
        input.classList.add("form-control");
        input.value = data[key];
        input.name = key;

        div.appendChild(label);
        div.appendChild(input);
        modalBody.appendChild(div);
      }

      openEditModal(id);
    } catch (err) {
      console.error(err);
    }
  });



  
addBtn.addEventListener("click", async () => {
  try {

    saveBtn.classList.remove("d-none");
    saveBtn.classList.add("d-inline-flex");


    const response = await fetch(`/${name}/info/`);
    if (!response.ok) throw new Error("Data not found");
    const fields = await response.json();
    console.log("Données reçues de Django:", fields);

    const typeMap = {
      string: "text",
      number: "number",
      email: "email",
      boolean: "boolean"
    };

    modalBody.innerHTML = ""; 

    for (let key in fields) {
      const div = document.createElement("div");
      div.classList.add("mb-3");

      const label = document.createElement("h6");
      label.textContent = key.replace(/_/g, ' ').charAt(0).toUpperCase() + key.replace(/_/g, ' ').slice(1);
      div.appendChild(label);

      if (fields[key] === "boolean") {
        const radioContainer = document.createElement("div");
        radioContainer.classList.add("d-flex", "gap-3", "mt-2");

        radioContainer.innerHTML = `
            <div class="form-check">
                <input class="form-check-input" type="radio" name="${key}" value="true" id="${key}_yes" checked>
                <label class="form-check-label" for="${key}_yes">Oui</label>
            </div>
            <div class="form-check">
                <input class="form-check-input" type="radio" name="${key}" value="false" id="${key}_no">
                <label class="form-check-label" for="${key}_no">Non</label>
            </div>
        `;
        div.appendChild(radioContainer);
        
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
        }

      else {
        const input = document.createElement("input");
        input.type = typeMap[fields[key]] || "text";
        input.classList.add("form-control");
        input.name = key;
        div.appendChild(input);
      }

      modalBody.appendChild(div);
    }

    openAddModal();

  } catch (err) {
    console.error("Erreur lors de l'ajout:", err);
  }
});




saveBtn.addEventListener("click", async () => {
  const mode = infoModalEl.dataset.mode;
  const id = infoModalEl.dataset.id;

  const dataToSend = {};
  let fieldTypes = {};
  
  const formElements = modalBody.querySelectorAll("input, select, textarea");
  
  formElements.forEach(element => {
  if (element.type === 'radio') {
    if (element.checked) dataToSend[element.name] = element.value === 'true';
  } else if (element.type === 'checkbox') {
    dataToSend[element.name] = element.checked;
  } else {
    if (element.name === "numBureau") {
      dataToSend[element.name] = element.value
        .split(',')
        .map(v => v.trim())
        .filter(v => v !== "")
        .map(Number);
    } else {
      dataToSend[element.name] = element.value;
    }
  }
});
  
  const responseInfo = await fetch(`/${name}/info/`);
  if (responseInfo.ok) {
    const fieldTypes = await responseInfo.json();
    
    for (let key in dataToSend) {
      if (fieldTypes[key] === "number" && dataToSend[key] !== "") {
        dataToSend[key] = Number(dataToSend[key]);
      } else if (fieldTypes[key] === "boolean" && typeof dataToSend[key] === "string") {
        dataToSend[key] = Boolean(dataToSend[key]);
      }
    }
  }

  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  try {
    let url = "";
    let method = "POST";
    
    if (mode === "edit") {
      url = `/${name}/${id}/edit/`;
    } else if (mode === "create") {
      url = `/${name}/create/`;
    }

    const response = await fetch(url, {
      method: method,
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken
      },
      body: JSON.stringify(dataToSend)
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `${mode === "edit" ? "Update" : "Create"} failed`);
    }

    const data = await response.json();
    
    if (mode === "edit") {
     
      const row = document.querySelector(`.row-checkbox[data-id="${id}"]`)?.closest("tr");
      if (row) {
       
        const headers = Array.from(table.querySelectorAll('th')).map(th => {
          return th.textContent.trim().toLowerCase().replace(/\s+/g, '_');
        });
        
    
        for (let i = 0; i < headers.length; i++) {
          const fieldName = headers[i];
          if (fieldName === 'id') {
          
            row.cells[i].innerHTML = `
              <input class="form-check-input row-checkbox" type="checkbox" data-id="${data.id}">
              <label class="form-check-label">${data.id}</label>
            `;
          } else if (data[fieldName] !== undefined) {

            if (fieldTypes && fieldTypes[fieldName] === "boolean") {
              const badgeClass = data[fieldName] ? "badge-success" : "badge-failure";
              const badgeText = data[fieldName] ? "Oui" : "Non";
              row.cells[i].innerHTML = `<span class="badge ${badgeClass}">${badgeText}</span>`;
            } else {
              row.cells[i].textContent = data[fieldName];
            }
          }
        }
      }
    } else if (mode === "create") {
      console.log("Created successfully:", data);
      
    }

    infoModal.hide();
    
  } catch (err) {
    console.error(err);
    alert(err.message || `${mode === "edit" ? "Update" : "Create"} failed`);
  }
});


 infoModalEl.addEventListener("hidden.bs.modal", () => {
    history.replaceState(null, "", `/${name}/`);
     window.location.reload();
  });

  

  deleteBtn.addEventListener("click", async () => {
    const checked = Array.from(document.querySelectorAll('.row-checkbox:checked'));
    if (checked.length === 0) return;

    const ids = checked.map(cb => cb.dataset.id);

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
      const response = await fetch(`/${name}/delete/`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken
        },
        body: JSON.stringify({ ids })
      });

      if (!response.ok) throw new Error("Delete failed");

      checked.forEach(cb => cb.closest('tr').remove());
      
      actionBar.classList.add('d-none');
      actionBar.classList.remove('d-flex');

    } catch (err) {
      console.error(err);
      alert("Delete failed");
    }
  });
 
};


