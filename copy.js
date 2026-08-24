function copyCode(sourceId, btn) {
  const text = document.getElementById(sourceId).value;
  navigator.clipboard.writeText(text).then(() => {
    const original = btn.textContent;
    btn.textContent = "Copied!";
    setTimeout(() => { btn.textContent = original; }, 1500);
  }).catch(() => {
    const original = btn.textContent;
    btn.textContent = "Couldn't copy — select & copy manually";
    setTimeout(() => { btn.textContent = original; }, 2500);
  });
}

function downloadCode(sourceId, filename) {
  const text = document.getElementById(sourceId).value;
  const blob = new Blob([text], { type: "text/x-python" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
