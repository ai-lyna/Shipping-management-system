
export function viewLogic({ infoModalEl, infoModal, modalBody, viewBtn, name }) {

  function openViewModal(id) {
    infoModal.show();
    history.pushState({ modal: "view", id }, "", `/${name}/${id}/`);
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
      console.error("View failed:", err);
    }
  });
}
