document.addEventListener('DOMContentLoaded', function() {
    var cont = document.querySelector('.cont');
    var imgBtn = document.querySelector('.img-btn');
    var showSignIn = document.getElementById('showSignIn');
    var showSignUp = document.getElementById('showSignUp');

    function isMobile() {
        return window.innerWidth <= 700;
    }

    // Desktop toggle (animation)
    if (imgBtn) {
        imgBtn.addEventListener('click', function() {
            if (!isMobile()) {
                cont.classList.toggle('s-signup');
            }
        });
    }

    // Mobile toggle
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
        showSignIn.addEventListener('click', function() {
            if (isMobile()) showSignInMobile();
        });
        showSignUp.addEventListener('click', function() {
            if (isMobile()) showSignUpMobile();
        });
    }

    // Set initial state on load
    function setInitialState() {
        if (isMobile()) {
            showSignInMobile();
        } else {
            cont.classList.remove('show-signin', 'show-signup');
            // Don't touch s-signup, let user toggle
        }
    }
    setInitialState();

    // On resize, update state
    window.addEventListener('resize', setInitialState);
});