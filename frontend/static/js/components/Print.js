export function printLogic({ name }) {

  const printBtn = document.getElementById("printBtn");

  printBtn.addEventListener("click", async () => {
    const checked = document.querySelectorAll('.row-checkbox:checked');
    if (checked.length !== 1) {
      alert("selectionner une seule ligne pour imprimer");
      return;
    }

    const id = checked[0].dataset.id;

    try {
      const response = await fetch(`/${name}/${id}`);
      if (!response.ok) throw new Error("Data not found");
      const data = await response.json();


      const printWindow = window.open('', '_blank');
      
      let content = `<html><head><title>Impression ${name}</title>`;

      content += `
        <style>
          body { font-family: 'Inter', sans-serif; padding: 40px; }
          h1 { color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }
          .field { margin-bottom: 20px; }
          .label { font-weight: bold; font-size: 14px; color: #666; text-transform: uppercase; }
          .value { font-size: 18px; margin-top: 5px; color: #000; }
          @media print { .no-print { display: none; } }
        </style>
      </head><body>`;

      content += `<h1>Détails - ${name.charAt(0).toUpperCase() + name.slice(1)} #${id}</h1>`;

      for (let key in data) {
        const label = key.replaceAll('_', ' ').charAt(0).toUpperCase() + key.slice(1);
        content += `
          <div class="field">
            <div class="label">${label}</div>
            <div class="value">${data[key]}</div>
          </div>`;
      }

      content += `</body></html>`;

      printWindow.document.write(content);
      printWindow.document.close();
      

      printWindow.focus();
      setTimeout(() => {
        printWindow.print();
        printWindow.close();
      }, 500);

    } catch (err) {
      console.error("Print failed:", err);
    }
  });
}