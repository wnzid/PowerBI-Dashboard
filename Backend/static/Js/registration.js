document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('registrationForm');
  const pwdInput = document.getElementById('password');
  const toggleBtn = document.querySelector('.toggle-password');

  if (toggleBtn) {
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

  form.addEventListener('submit', (e) => {
    const email = document.getElementById('email').value.trim();
    const password = pwdInput.value.trim();
    const role = document.getElementById('role').value;

    if (!email || !password) {
      e.preventDefault();
      alert('Please fill in all fields.');
      return;
    }

    const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailRegex.test(email)) {
      e.preventDefault();
      alert('Please enter a valid email address.');
      return;
    }

    if (password.length < 12) {
      e.preventDefault();
      alert('Password must be at least 12 characters long.');
      return;
    }

    if (!role) {
      e.preventDefault();
      alert('Please select a role to register.');
      return;
    }
  });
});
