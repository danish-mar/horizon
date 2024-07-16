// login.js

// Handle form submission for login
document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('login-form');

    function resetMessage() {
        document.getElementById('ok-login-message').innerText = ' ';
        document.getElementById('error-login-message').innerText = ' ';
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(loginForm);
            const username = formData.get('username');
            const password = formData.get('password');
            let errorAlert = document.getElementById('error-login-message');
            let successAlert = document.getElementById('ok-login-message')


            fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json' // Set Content-Type to JSON
                },
                body: JSON.stringify({ // Stringify the object to JSON
                    username: username,
                    password: password
                })

            })
                .then(response => {
                    resetMessage()
                    successAlert.innerText = "Logging in... "
                    // Get the X-Auth-Token cookie from the response headers
                    const authToken = response.headers.get('X-Auth-Token');
                    if (authToken) {
                        // Set the cookie with the received auth token
                        document.cookie = `X-Auth-Token=${authToken};  SameSite=Strict; path=/`;

                    }
                    return response.json();
                })
                .then(data => {
                    resetMessage()
                    successAlert = ' Welcome back, Redirecting...'
                    if (data.success) {
                        // Successful login, redirect to /account
                        window.location.href = "/account";

                    } else {

                        if (!data.success){
                            console.log(data.message)

                            if(data.server_response_code === 503){
                                alert(data.message)
                                resetMessage()
                                errorAlert.innerText = "Server under Maintenance \n Please try again later~";
                                errorAlert.style.display = 'block';
                            }else{
                                resetMessage()
                                errorAlert.innerText = data.message;
                                errorAlert.style.display = 'block';
                            }
                        }
                        // Failed login, show error message
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    // Handle other errors or network issues
                });
        });
    }
});
