document.addEventListener('DOMContentLoaded', () => {
  const pwdInput = document.getElementById('password');
  const toggleBtn = document.querySelector('.toggle-password');
  const form = document.querySelector('.login-form');
  const loginBtn = document.getElementById('loginBtn');
  const spinner = document.getElementById('loginSpinner');

  if (pwdInput && toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      if (pwdInput.type === 'password') {
        pwdInput.type = 'text';
        toggleBtn.textContent = 'Hide';
      } else {
        pwdInput.type = 'password';
        toggleBtn.textContent = 'Show';
      }
    });
  }

  if (form && loginBtn && spinner) {
    form.addEventListener('submit', () => {
      loginBtn.disabled = true;
      spinner.classList.remove('d-none');
    });
  }
});
