import { openAddModal } from "./AddModal.js";
import { SaveLogic } from "./Save.js";

export function addBtnLogic({ addBtnId, infoModalEl, infoModal, modalBody, saveBtn, name }) {
  const addBtn = document.getElementById(addBtnId);

  addBtn.addEventListener("click", async () => {
    try {
      saveBtn.classList.remove("d-none");
      saveBtn.classList.add("d-inline-flex");

      await openAddModal({ infoModalEl, infoModal, modalBody, name });
      SaveLogic({ saveBtn, infoModal, modalBody, name });
    } catch (err) {
      console.error("Add button error:", err);
    }
  });
}
