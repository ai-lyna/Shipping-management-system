import { openAddModal } from "../components/AddModal.js";
import { saveLogic } from "../components/Save.js";

export function favorisLogic({ infoModalEl, infoModal, modalBody, saveBtn, csrfToken }) {
  let currentName = null;

  const cards = document.querySelectorAll(".fav-card");

  cards.forEach(card => {
    card.addEventListener("click", async () => {
      currentName = card.dataset.cardName;

      saveBtn.classList.remove("d-none");
      saveBtn.classList.add("d-inline-flex");

      await openAddModal({
        infoModalEl,
        infoModal,
        modalBody,
        name: currentName
      });
    });
  });

  // attach ONCE
  saveLogic({
    infoModalEl,
    infoModal,
    modalBody,
    saveBtn,
    csrfToken,
    getName: () => currentName
  });
}

favorisLogic();