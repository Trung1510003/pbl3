loginForm = document.querySelector('.login-container');
regForm = document.querySelector('.register-container');

document.getElementById("login-btn-reg").addEventListener("click", function(e){
    loginForm.style.display = 'block';
    regForm.style.display = 'none';
});

document.getElementById("register-btn").addEventListener("click", function(e){
    loginForm.style.display = 'none';
    regForm.style.display = 'block';
});

document.getElementById("register-btn-reg").addEventListener("click", function(e){
    const email = document.getElementById('regemail').value;
    const username = document.getElementById('regusername').value;
    const password = document.getElementById('regpassword').value;
    const cfpassword = document.getElementById('regcfpassword').value;

    if (password != cfpassword)
    {
        alert('Password does not match')
        return;
    }

    fetch("/regCheck", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            email : email,
            username: username,
            password: password
        })
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.status === "ok") {
            alert('Register successfully');
            window.location.href = "/login"; 
        } else if (data.status === "not-yet") {
            alert('username already exists!');
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });

});


document.getElementById("login-btn").addEventListener("click", function(event) {

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    fetch("/loginCheck", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    })
    .then(response => response.json()) 
    .then(data => {
        if (data.status === "ok") {
            window.location.href = "/chat"; 
        } else if (data.status === "not-yet") {
            document.getElementById("errorMessage").style.display = "block";
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});
