import { addBtnLogic } from "./Add.js";
import { saveLogic } from "./Save.js";
import { editLogic } from "./Edit.js";
import { deleteLogic } from "./Delete.js";
import { viewLogic } from "./View.js";

export function modalLogic() {
  const table = document.querySelector("table[data-name]");
  if (!table) return;

  const name = table.dataset.name;

  const infoModalEl = document.getElementById("infoModal");
  const infoModal = new bootstrap.Modal(infoModalEl);
  const modalBody = infoModalEl.querySelector(".modal-body");

  const saveBtn = document.getElementById("savebtn");
  const addBtn = document.getElementById("addBtn");
  const editBtn = document.getElementById("editBtn");
  const viewBtn = document.getElementById("viewBtn");
  const deleteBtn = document.getElementById("deleteBtn");

  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]")?.value;


  const actionBar = document.getElementById("actionBar");

  function updateActionBar() {
    const checked = document.querySelectorAll(".row-checkbox:checked");

    if (checked.length > 0) {
      actionBar.classList.remove("d-none");
      actionBar.classList.add("d-flex");

      viewBtn.disabled = checked.length !== 1;
      editBtn.disabled = checked.length !== 1;
    } else {
      actionBar.classList.add("d-none");
      actionBar.classList.remove("d-flex");
    }
  }

  document.addEventListener("change", e => {
    if (e.target.classList.contains("row-checkbox")) {
      updateActionBar();
    }
  });


  addBtnLogic({addBtnId: "addBtn", infoModalEl, infoModal, modalBody, saveBtn, name });

  saveLogic({infoModalEl,infoModal, modalBody, saveBtn, name, csrfToken });

  editLogic({ infoModalEl, infoModal, modalBody, saveBtn, editBtn, name });

  viewLogic({ infoModalEl, infoModal, modalBody, viewBtn, name });

  deleteLogic({ deleteBtn, name });


  infoModalEl.addEventListener("hidden.bs.modal", () => {
    history.replaceState(null, "", `/${name}/`);
    window.location.reload();
  });
}
