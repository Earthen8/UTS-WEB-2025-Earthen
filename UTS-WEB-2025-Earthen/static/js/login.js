// Nama: Earthen Krisdian Setya
// NIM: 23502410009
// Prodi: DBT24

const togglePassword = document.getElementById("togglePassword");
const passwordInput = document.querySelector('input[type="password"]');

if (togglePassword && passwordInput) {
  togglePassword.addEventListener("click", function () {
    const type =
      passwordInput.getAttribute("type") === "password" ? "text" : "password";
    passwordInput.setAttribute("type", type);

    this.classList.toggle("bi-eye-fill");
    this.classList.toggle("bi-eye-slash-fill");
  });
}

document.querySelectorAll(".form-control").forEach((input) => {
  input.addEventListener("focus", function () {
    this.parentElement.style.transform = "scale(1.02)";
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
    '<span class="spinner-border spinner-border-sm me-2"></span>Logging in...';
  submitBtn.disabled = true;
});

document.querySelectorAll(".alert").forEach((alert) => {
  setTimeout(() => {
    const bsAlert = new bootstrap.Alert(alert);
    bsAlert.close();
  }, 5000);
});