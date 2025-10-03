// Nama: Earthen Krisdian Setya
// NIM: 23502410009
// Prodi: DBT24

document.querySelectorAll(".form-control, .form-select").forEach((input) => {
  input.addEventListener("focus", function () {
    this.parentElement.style.transform = "scale(1.01)";
    this.parentElement.style.transition = "transform 0.3s ease";
  });

  input.addEventListener("blur", function () {
    this.parentElement.style.transform = "scale(1)";
  });
});

const form = document.querySelector("form");
form.addEventListener("submit", function (e) {
  const submitBtn = form.querySelector('button[type="submit"]');
  submitBtn.innerHTML =
    '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
  submitBtn.disabled = true;
});