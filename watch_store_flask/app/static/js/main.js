// WatchStore Client Interaction Scripts
document.addEventListener("DOMContentLoaded", function () {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".alert.alert-dismissible");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      try {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      } catch (e) {
        // ignore
      }
    }, 5000);
  });

  // Quantity spinners
  const qtyInputs = document.querySelectorAll(".quantity-input");
  qtyInputs.forEach(function (input) {
    input.addEventListener("change", function () {
      if (parseInt(this.value, 10) < 1) {
        this.value = 1;
      }
    });
  });
});

