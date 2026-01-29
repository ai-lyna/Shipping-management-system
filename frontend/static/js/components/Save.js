export function saveLogic({ infoModalEl, modalBody, saveBtn, name, csrfToken }) {
  saveBtn.addEventListener("click", async () => {
    const mode = infoModalEl.dataset.mode;
    const id = infoModalEl.dataset.id;

    const dataToSend = {};
    const formElements = modalBody.querySelectorAll("input, select, textarea");

    formElements.forEach(element => {
      if (element.type === 'radio') {
        if (element.checked) dataToSend[element.name] = element.value === 'true';
      } else if (element.type === 'checkbox') {
        dataToSend[element.name] = element.checked;
      } else {
        dataToSend[element.name] = element.value;
      }
    });

    try {
      let url = mode === "edit" ? `/${name}/${id}/edit/` : `/${name}/create/`;

      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": csrfToken  
        },
        body: JSON.stringify(dataToSend)
      });

      if (!response.ok) throw new Error(`${mode === "edit" ? "Update" : "Create"} failed`);

      const data = await response.json();
      console.log("Saved successfully:", data);

      infoModalEl.hide();

    } catch (err) {
      console.error(err);
      alert(err.message);
    }
  });
}
