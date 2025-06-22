document.addEventListener('DOMContentLoaded', function () {
  var cont = document.querySelector('.cont');
  var imgBtn = document.querySelector('.img-btn');
  var showSignIn = document.getElementById('showSignIn');
  var showSignUp = document.getElementById('showSignUp');

  function isMobile() {
    return window.innerWidth <= 700;
  }

  // Toggle animation for desktop
  if (imgBtn) {
    imgBtn.addEventListener('click', function () {
      if (!isMobile()) {
        cont.classList.toggle('s-signup');
      }
    });
  }

  // Mobile toggle logic
  function showSignInMobile() {
    cont.classList.add('show-signin');
    cont.classList.remove('show-signup');
    cont.classList.remove('s-signup');
  }

  function showSignUpMobile() {
    cont.classList.add('show-signup');
    cont.classList.remove('show-signin');
    cont.classList.remove('s-signup');
  }

  if (showSignIn && showSignUp && cont) {
    showSignIn.addEventListener('click', function () {
      if (isMobile()) showSignInMobile();
    });

    showSignUp.addEventListener('click', function () {
      if (isMobile()) showSignUpMobile();
    });
  }

  // Initial state
  function setInitialState() {
    if (isMobile()) {
      showSignUpMobile();
    } else {
      cont.classList.remove('show-signin', 'show-signup');
    }
  }

  setInitialState();

  // Update on resize
  let previousIsMobile = isMobile();
  window.addEventListener('resize', function () {
    const currentIsMobile = isMobile();
    if (currentIsMobile !== previousIsMobile) {
      if (!currentIsMobile) {
        cont.classList.remove('show-signin', 'show-signup');
      } else {
        showSignInMobile();
      }
      previousIsMobile = currentIsMobile;
    }
  });
});

window.addHobbyField = function(containerId) {
  const container = document.getElementById(containerId);

  const wrapper = document.createElement('div');
  wrapper.className = 'hobby-input-wrapper';

  const input = document.createElement('input');
  input.type = 'text';
  input.name = 'hobbies[]';
  input.placeholder = 'Enter a hobby';
  input.style.marginTop = '5px';

  const removeBtn = document.createElement('button');
  removeBtn.type = 'button';
  removeBtn.className = 'remove-hobby-btn';
  removeBtn.innerHTML = '×';
  removeBtn.onclick = function() {
    container.removeChild(wrapper);
  };

  wrapper.appendChild(input);
  wrapper.appendChild(removeBtn);
  container.appendChild(wrapper);
};
