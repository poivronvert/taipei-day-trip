document.addEventListener('DOMContentLoaded', function(){
    const path = window.location.pathname;
    const url = '/api'+path;
    fetch(url)
        .then(response => response.json())
        .then(res => {
            if (res.error) {
                alert(res.message);
                return;
            }
            appendInfo(res.data);
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

    images.forEach((image, index)=> {
        const imgCount = document.createElement('input');
        imgCount.type = 'radio';
        imgCount.id = `img-${index}`;
        imgCount.name = 'imgCounter';
        imgCounter.appendChild(imgCount);
    });
    imgElement.id = 'imgContainer';
    imgArray.updateSelection('imgContainer','imgCounter');

    document.getElementById('nextBtnId').addEventListener('click',()=> imgArray.next('imgContainer','imgCounter'));
    document.getElementById('preBtnId').addEventListener('click',()=> imgArray.pre('imgContainer','imgCounter'));

    let nameContainer = document.querySelector('.name');
    nameContainer.textContent = result.name;
    nameContainer.className = "header3";

    let catmrtContainer = document.querySelector('.category-mrt');
    catmrtContainer.textContent = result.category+' at '+result.mrt;

    let desContainer = document.querySelector('.description');
    desContainer.textContent = result.description;

    let addContainer = document.querySelector('.address');
    addContainer.textContent = result.address;

    let transContainer = document.querySelector('.transport');
    transContainer.textContent = result.transport;
}

class ImageCarousel {
    constructor(images){
        this.images = images;
        this.i =0;
    }

    updateSelection(imgId, imgCounterId){
        const img = document.getElementById(imgId);

        img.src=this.images[this.i];

        const radios = document.getElementsByTagName('input');
        for (let j=0;j<radios.length;j++){
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

