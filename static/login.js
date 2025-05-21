function toggleForm(formType) {
  const loginBox = document.getElementById('login-box');
  const registerBox = document.getElementById('register-box');
  const loginBtn = document.getElementById('login-btn');
  const registerBtn = document.getElementById('register-btn');

  if (formType === 'login') {
    loginBox.classList.remove('hidden');
    registerBox.classList.add('hidden');
    loginBtn.classList.add('active');
    registerBtn.classList.remove('active');
  } else {
    loginBox.classList.add('hidden');
    registerBox.classList.remove('hidden');
    loginBtn.classList.remove('active');
    registerBtn.classList.add('active');
  }
}
  document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
      const alerts = document.querySelectorAll('.fixed > div');
      alerts.forEach(alert => alert.style.display = 'none');
    }, 4000);
  });

