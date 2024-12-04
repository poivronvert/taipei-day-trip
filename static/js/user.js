async function verifyUserToken() {
    const token = localStorage.getItem('authToken');
    if (token) {
        const url = '/api/user/auth';

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            const data = await response.json();
            if (data.data) {
                return true;
            }
        } catch (error) {
            console.error('Error verifying token:', error);
            return false;
        }
    }
}

function displaySigninModal() {
    const signinModal = document.getElementById('signinModal');
    const signupModal = document.getElementById('signupModal');
    signinModal.style.display = 'block';
    signupModal.style.display = 'none';
    overlayPage();
}

function displaySignupModal() {
    const signinModal = document.getElementById('signinModal');
    const signupModal = document.getElementById('signupModal');
    signinModal.style.display = 'none';
    signupModal.style.display = 'block';
    overlayPage();
}

function overlayPage() {
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'block';
    document.body.classList.add('modal-active');
}

document.addEventListener("DOMContentLoaded", async () => {
    const navbarSignin = document.getElementById('navbarSignin');
    const navbarSignout = document.getElementById('navbarSignout');

    const isValidToken = await verifyUserToken();

    if (isValidToken) {
        navbarSignin.style.display = 'none';
        navbarSignout.style.display = 'block';
    } else {
        navbarSignin.style.display = 'block';
        navbarSignout.style.display = 'none';
    }
});

document.getElementById('navbarSignin').addEventListener('click', displaySigninModal);
document.getElementById('switchSignin').addEventListener('click', displaySigninModal);
document.getElementById('switchSignup').addEventListener('click', displaySignupModal);

document.querySelectorAll('.closeBtn').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => {
        const signinModal = document.getElementById('signinModal');
        const signupModal = document.getElementById('signupModal');
        const overlay = document.getElementById('overlay');

        signinModal.style.display = 'none';
        signupModal.style.display = 'none';
        overlay.style.display = 'none';
        document.body.classList.remove('modal-active');
    });
});

document.getElementById("signupForm").addEventListener('submit', async (event) => {
    event.preventDefault();
    const signupForm = event.target;

    const signupData = {
        name: signupForm.querySelector('#signupName').value,
        email: signupForm.querySelector('#signupEmail').value,
        password: signupForm.querySelector('#signupPassword').value
    };

    const jsonString = JSON.stringify(signupData);
    

    try {
        const url = '/api/user';
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: jsonString
        });

        let container = document.getElementById('msgSignup');

        if (response.ok) {
            const data = await response.json();
            console.log('Signup successful');
            container.style.display = "block";
            container.innerHTML = '註冊成功，請重新登入(跳轉登入頁面...)';
            setTimeout(()=>{displaySigninModal()},1000);
        } else {
            const error = await response.json();
            container.style.display = "block";
            container.innerHTML = error.message;
        }

    } catch (error) {
        console.error('Fetch error:', error);
        container.style.display = "block";
        container.innerHTML='註冊失敗，請稍後再試。';
    }
});





document.getElementById('signinForm').addEventListener('submit', async (event) => {
    event.preventDefault(); //防止瀏覽器刷新並直接提交表單

    const signinForm = event.target;

    const signinData = {
        email: signinForm.querySelector('#signinEmail').value,
        password: signinForm.querySelector('#signinPassword').value
    };

    const jsonString = JSON.stringify(signinData);


    try {
        const url = "/api/user/auth";
        
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type':'application/json'
            },
            body: jsonString
        });
        if (response.ok) {
            const data = await response.json();
            console.log('Login successful');
            const token = data.token;
            localStorage.setItem('authToken', token);

            window.location.reload();

        } else {
            const data = await response.json();
            console.error('Login failed');
            const errorMsg =data.message;
            let container = document.getElementById('msgSignin');
            container.style.display = "block";
            container.innerHTML = errorMsg;
        }

    } catch (error) {
        console.error('Fetch error:', error);
    }
});

document.getElementById('navbarSignout').addEventListener('click', () => {

    if (localStorage.key('authToken')) {
        localStorage.removeItem('authToken');
        alert('登出成功');

    } else {
        alert('無效操作，請重新登入');
    }

    window.location.reload();
});

document.getElementById('navbarBooking').addEventListener('click', async () => {
    const isValidToken = await verifyUserToken();

    if (!isValidToken) {
        displaySigninModal();
    }
});


