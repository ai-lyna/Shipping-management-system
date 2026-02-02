export function editLogic({ infoModalEl, infoModal, modalBody, saveBtn, editBtn,name }) {

  function openEditModal(id) {
    infoModalEl.dataset.mode = "edit";
    infoModal.show();
    history.pushState({ modal: "edit", id }, "", `/${name}/${id}/edit/`);
  }

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
      console.error("Edit failed:", err);
    }
  });
}
