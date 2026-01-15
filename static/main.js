const publicKey = "BN6tMU7CgGrHp-BA4UtYTrNs6OxL2kk0P2YHU00dATYPFWtu8MEhufhim-7zcSpKwjVcGl1sLi5g-R6L2E8K9l8";

async function subscribe() {
  if (!("serviceWorker" in navigator)) {
    alert("Service workers not supported");
    return;
  }

  const reg = await navigator.serviceWorker.register("/static/sw.js");

  const sub = await reg.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array(publicKey)
  });

  await fetch("/subscribe", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(sub)
  });

  alert("Subscribed successfully!");
}

function send() {
  fetch("/send");
}

function urlBase64ToUint8Array(base64String) {
  const padding = "=".repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, "+")
    .replace(/_/g, "/");

  const raw = atob(base64);
  return Uint8Array.from([...raw].map(c => c.charCodeAt(0)));
}
