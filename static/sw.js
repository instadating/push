self.addEventListener("push", event => {
  let data = "You have a new notification";

  if (event.data) {
    data = event.data.text();
  }

  event.waitUntil(
    self.registration.showNotification("🚨 Flask Push Alert", {
      body: data,

      // 🔰 MAIN LOGO (shows on notification)
      icon: "/static/icon.png",

      // 🔹 SMALL STATUS BAR LOGO (Android / Chrome)
      badge: "/static/badge.png",

      // 🖼️ BIG IMAGE (optional – looks premium)
      image: "/static/banner.png",

      requireInteraction: true,
      silent: false,
      tag: "flask-push",
      renotify: false
    })
  );
});

// Click handler
self.addEventListener("notificationclick", event => {
  event.notification.close();

  event.waitUntil(
    clients.openWindow("/")
  );
});
