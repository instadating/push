self.addEventListener("push", event => {
  let data = "You have a new notification";

  if (event.data) {
    data = event.data.text();
  }

  event.waitUntil(
    self.registration.showNotification("🚀 Push Test", {
      body: data,
      icon: "/static/icon.png",
      badge: "/static/icon.png",   // optional small icon
      requireInteraction: true,     // stays until user interacts
      silent: false,
      tag: "push-test",             // prevents duplicate stacking
      renotify: false,
      actions: []                   // ❌ no unsubscribe button
    })
  );
});

// Handle notification click
self.addEventListener("notificationclick", event => {
  event.notification.close();

  event.waitUntil(
    clients.matchAll({ type: "window", includeUncontrolled: true }).then(clientList => {
      for (const client of clientList) {
        if (client.url === "/" && "focus" in client) {
          return client.focus();
        }
      }
      if (clients.openWindow) {
        return clients.openWindow("/");
      }
    })
  );
});

