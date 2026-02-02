import { openAddModal } from "../components/AddModal.js";
import { saveLogic } from "../components/Save.js";

export function favorisLogic() {
    const infoModalEl = document.getElementById("infoModal");
    if (!infoModalEl) return;

    const infoModal = new bootstrap.Modal(infoModalEl);
    const modalBody = infoModalEl.querySelector(".modal-body");
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    const cards = document.querySelectorAll(".fav-card");

    cards.forEach(card => {
        card.addEventListener("click", async () => {
            const name = card.dataset.cardName;

            await openAddModal({
                infoModalEl,
                infoModal,
                modalBody,
                name: name
            });

            const activeSaveBtn = infoModalEl.querySelector("#saveBtn");

            if (activeSaveBtn) {
                saveLogic({ 
                    infoModalEl, 
                    infoModal, 
                    modalBody, 
                    saveBtn: activeSaveBtn,
                    name, 
                    csrfToken 
                });
            } else {
                console.error("Save button still not found after openAddModal!");
            }
        });
    });
}

favorisLogic();