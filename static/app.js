// Cong thu thap bao gia - tien ich giao dien (khong phu thuoc thu vien ngoai)

document.addEventListener("DOMContentLoaded", function () {
  // 1) Dinh dang so tien co dau cham ngan cach hang nghin khi go
  document.querySelectorAll(".money-input").forEach(function (input) {
    const clean = (v) => v.replace(/[^\d]/g, "");
    const fmt = (v) => {
      const n = clean(v);
      if (!n) return "";
      return Number(n).toLocaleString("vi-VN");
    };
    input.addEventListener("input", function () {
      const pos = input.selectionStart;
      const before = input.value.length;
      input.value = fmt(input.value);
      const after = input.value.length;
      const diff = after - before;
      try { input.setSelectionRange(pos + diff, pos + diff); } catch (e) {}
    });
    // truoc khi submit, gui gia tri thuan so (khong dau cham) qua 1 input an
    const form = input.closest("form");
    if (form) {
      form.addEventListener("submit", function () {
        input.value = clean(input.value);
      });
    }
  });

  // 2) Dropzone: click de chon file + keo-tha
  document.querySelectorAll(".dropzone").forEach(function (zone) {
    const input = zone.querySelector("input[type=file]");
    const labelEl = zone.querySelector(".dz-label");
    if (!input) return;
    zone.addEventListener("click", () => input.click());
    input.addEventListener("change", () => {
      if (input.files && input.files[0] && labelEl) {
        labelEl.textContent = "Đã chọn: " + input.files[0].name;
      }
    });
    ["dragenter", "dragover"].forEach((evt) =>
      zone.addEventListener(evt, (e) => { e.preventDefault(); zone.classList.add("dragover"); })
    );
    ["dragleave", "drop"].forEach((evt) =>
      zone.addEventListener(evt, (e) => { e.preventDefault(); zone.classList.remove("dragover"); })
    );
    zone.addEventListener("drop", (e) => {
      if (e.dataTransfer.files.length) {
        input.files = e.dataTransfer.files;
        if (labelEl) labelEl.textContent = "Đã chọn: " + e.dataTransfer.files[0].name;
      }
    });
  });

  // 3) Tu dong an flash message sau 6 giay
  document.querySelectorAll(".alert[data-autohide]").forEach(function (el) {
    setTimeout(() => { el.style.transition = "opacity .4s"; el.style.opacity = "0"; setTimeout(() => el.remove(), 400); }, 6000);
  });

  // 4) Dem nguoc thoi gian dong cong (neu co phan tu #close-countdown)
  const cd = document.getElementById("close-countdown");
  if (cd && cd.dataset.closeAt) {
    const closeAt = new Date(cd.dataset.closeAt).getTime();
    function tick() {
      const diff = closeAt - Date.now();
      if (diff <= 0) { cd.textContent = "Đã hết hạn"; return; }
      const d = Math.floor(diff / 86400000);
      const h = Math.floor((diff % 86400000) / 3600000);
      const m = Math.floor((diff % 3600000) / 60000);
      cd.textContent = (d > 0 ? d + " ngày " : "") + h + " giờ " + m + " phút nữa";
    }
    tick();
    setInterval(tick, 30000);
  }
});
