export function deleteLogic({ deleteBtn, name }) {

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

      const actionBar = document.getElementById("actionBar");
      actionBar.classList.add('d-none');
      actionBar.classList.remove('d-flex');

    } catch (err) {
      console.error("Delete failed:", err);
      alert("Delete failed");
    }
  });
}
