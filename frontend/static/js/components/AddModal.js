export async function openAddModal({ infoModalEl, infoModal, modalBody, name }) {
    infoModalEl.dataset.mode = "create";
    delete infoModalEl.dataset.id;

    // --- 1. SET THE TITLE ---
    const modalTitle = infoModalEl.querySelector(".modal-title");
    if (modalTitle) {
        modalTitle.textContent = `${name}`;
    }

    // --- 2. PREPARE THE BODY ---
    modalBody.innerHTML = "";
    infoModal.show();
    history.replaceState(null, "", `/${name}/`);

    // --- 3. FETCH DATA ---
    const res = await fetch(`/${name}/info/`);
    if (!res.ok) throw new Error("Data not found");

    const fields = await res.json();
    const typeMap = { string: "text", number: "number", email: "email" };

    // --- 4. RENDER FIELDS ---
    for (let key in fields) {
        const div = document.createElement("div");
        div.classList.add("mb-3");

        const label = document.createElement("h6");
        label.textContent = key.replaceAll('_', ' ');
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


    let footer = infoModalEl.querySelector(".modal-footer");
    if (!footer) {
        footer = document.createElement("div");
        footer.classList.add("modal-footer");
        infoModalEl.querySelector(".modal-content").appendChild(footer);
    }


    let saveBtn = footer.querySelector("#saveBtn");
    if (!saveBtn) {
        saveBtn = document.createElement("button");
        saveBtn.id = "saveBtn";
        saveBtn.type = "button";
        saveBtn.className = "btn btn-primary";
        saveBtn.textContent = "Save";
        footer.appendChild(saveBtn);
    }
}