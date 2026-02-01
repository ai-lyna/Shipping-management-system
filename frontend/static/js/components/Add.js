import { openAddModal } from "./AddModal.js";

export function addBtnLogic({ addBtnId, infoModalEl, infoModal, modalBody, saveBtn, name }) {
  const addBtn = document.getElementById(addBtnId);

  addBtn.addEventListener("click", async () => {
    try {
      await openAddModal({ infoModalEl, infoModal, modalBody, name });
    } catch (err) {
      console.error("Add button error:", err);
    }
  });
}
