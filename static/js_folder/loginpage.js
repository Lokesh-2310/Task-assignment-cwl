const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

function showSignup() {
    container.classList.add("right-panel-active");
}

function showLogin() {
    container.classList.remove("right-panel-active");
}

function showError(message) {
    const errorBox = document.getElementById('errorBox');
    errorBox.textContent = message;
    errorBox.classList.add('show');
    setTimeout(() => {
        errorBox.classList.remove('show');
    }, 4000);
}

// ==== LOGIN API CALL =====
async function login() {
    const email = document.getElementById("login_email").value;
    const password = document.getElementById("login_password").value;

    const res = await fetch("http://127.0.0.1:5000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
    });

    const data = await res.json();
    if (data.error){
        showError(data.error);
    }
    // STORE TOKEN IN COOKIES
    if (data.token) {
        // Expires in 1 day
        document.cookie = `jwt_token=${data.token}; path=/; max-age=86400; Secure; SameSite=Lax`;

        console.log("Token Saved in Cookies:", data.token);

        window.location.href = "/home"; // redirect after login
    }
}

// ==== SIGNUP API CALL =====
async function signup() {
    const name = document.getElementById("signup_name").value;
    const email = document.getElementById("signup_email").value;
    const password = document.getElementById("signup_password").value;

    const res = await fetch("http://127.0.0.1:5000/auth/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password })
    });

    const data = await res.json();
    if (data.error){
        showError(data.error);
    }

    if (data.message) showLogin();
}