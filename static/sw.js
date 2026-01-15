self.addEventListener("push", event => {
  const data = event.data.text();

  event.waitUntil(
    self.registration.showNotification("Push Test", {
      body: data,
      icon: "/static/icon.png"
    })
  );
});
