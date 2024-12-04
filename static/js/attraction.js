document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;
    const url = '/api' + path;
    fetch(url)
        .then(response => response.json())
        .then(res => {
            if (res.error) {
                let container = document.querySelector('.grid-attraction');
                container.innerHTML = "";
                return;
            }
            appendInfo(res.data);

            const morningRadio = document.getElementById('morning');
            const afternoonRadio = document.getElementById('afternoon');


            morningRadio.addEventListener('change', updatePrice);
            afternoonRadio.addEventListener('change', updatePrice);

            updatePrice();

            function updatePrice() {
                if (morningRadio.checked) {
                    priceResult = 2000;
                } else if (afternoonRadio.checked) {
                    priceResult = 2500;
                }
                document.getElementById('amount').textContent = '新台幣 ' + priceResult + ' 元';
            }
        })
        .catch(error => {
            console.error('Error fetching item', error);
        });

});



function appendInfo(result) {
    const imgCounter = document.getElementById('imgCounter');
    const imgContainer = document.querySelector('.attr-img');
    const imgElement = document.createElement('img');
    imgElement.id = 'imgContainer';
    imgContainer.appendChild(imgElement);

    const images = result.images;
    const imgArray = new ImageCarousel(images);

    images.forEach((image, index) => {
        const imgCount = document.createElement('input');
        imgCount.type = 'radio';
        imgCount.id = `img-${index}`;
        imgCount.name = 'imgCounter';
        imgCounter.appendChild(imgCount);
    });
    imgElement.id = 'imgContainer';
    imgArray.updateSelection('imgContainer', 'imgCounter');

    document.getElementById('nextBtnId').addEventListener('click', () => imgArray.next('imgContainer', 'imgCounter'));
    document.getElementById('preBtnId').addEventListener('click', () => imgArray.pre('imgContainer', 'imgCounter'));

    let nameContainer = document.querySelector('.name');
    nameContainer.textContent = result.name;
    nameContainer.className = "header3";

    let catmrtContainer = document.querySelector('.category-mrt');
    catmrtContainer.textContent = result.category + ' at ' + result.mrt;

    let desContainer = document.querySelector('.description');
    desContainer.textContent = result.description;

    let addContainer = document.querySelector('.address');
    addContainer.textContent = result.address;

    let transContainer = document.querySelector('.transport');
    transContainer.textContent = result.transport;
}

class ImageCarousel {
    constructor(images) {
        this.images = images;
        this.i = 0;
    }

    updateSelection(imgId, imgCounterId) {
        const img = document.getElementById(imgId);

        img.src = this.images[this.i];

        const radios = document.getElementsByName('imgCounter');
        for (let j = 0; j < radios.length; j++) {
            radios[j].checked = (j === this.i);
        }

    }
    next(imgId, imgCounterId) {
        this.i = (this.i + 1) % this.images.length;
        this.updateSelection(imgId, imgCounterId);
    }
    pre(imgId, imgCounterId) {
        this.i = (this.i - 1 + this.images.length) % this.images.length;
        this.updateSelection(imgId, imgCounterId);
    }
}

function triggerDatePicker() {
    const dateInput = document.getElementById('appt');
    dateInput.showPicker ? dateInput.showPicker() : dateInput.click();
}


document.querySelector('#profileBooking').addEventListener('click', async () => {
const isValidToken = await verifyUserToken('/api/user/auth');
    if (!isValidToken) {
        displaySigninModal();
    } else {
        document.getElementById('bookingForm').dispatchEvent(new Event('submit'));
    }
});

document.getElementById('bookingForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const bookingForm = event.target;

    const amtElement = bookingForm.querySelector('#amount').textContent;
    const amtNum = parseInt(amtElement.match(/\d+/)[0],10);

    const path = window.location.pathname;
    const attrNum = parseInt(path.match(/\d+/)[0],10);

    const bookingData = {
        date: bookingForm.querySelector('#appt').value,
        time: bookingForm.querySelector('input[name="timing"]:checked').value,
        price: amtNum,
        attractionId: attrNum,
    };

    const jsonString = JSON.stringify(bookingData);


    try {
        const url = '/api/booking';
        const token = localStorage.getItem('authToken');
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization':`Bearer ${token}`,
            },
            body: jsonString
        });


        if (response.ok) {
            const data = await response.json();
            console.log('Book successful');
            window.location.href = "/booking";
        } else {
            const data = await response.json();
            console.error('Book error:', data['message']);
        }

    } catch (error) {
        console.error('Fetch error:', error);
    }
});


