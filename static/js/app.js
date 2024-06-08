let page = 0;
let keyword = "";
let isLoading = false;
let initialLoadCompleted = false;
let hasNextPage = true;
let observer;

document.addEventListener('DOMContentLoaded', function() {
    if(!initialLoadCompleted){
        getData(page, keyword);
        initialLoadCompleted = true;

    }

    getMrt();
    observeLastElement();
});

let callback = function(entries, observer) {
    entries.forEach(entry => {
        if (entry.isIntersecting && !isLoading && initialLoadCompleted && hasNextPage) {
            page++;
            isLoading = true;
            getData(page, keyword);
        }
    });
};

function observeLastElement() {
    let targetElement = document.querySelector('.scroll-trigger');
    if (targetElement) {
        observer = new IntersectionObserver(callback);
        observer.observe(targetElement);
    }
}

function getData(page, keyword){
    const url = `/api/attractions?page=${page}&keyword=${keyword}`
    fetch(url)
    .then(response => response.json())
    .then(res => {
        isLoading = false; 
        if (res.hasOwnProperty('error')) {
            let errorMessage = document.createElement('div');
            errorMessage.textContent = res.message;
            container.appendChild(errorMessage);
            return;
        }

        let results = res.data;
        results.forEach(result => {
            appendAttraction(result);
        });


        let oldTrigger = document.querySelector('.scroll-trigger');
        if (oldTrigger){
            oldTrigger.remove();
        }

        if (res.nextpage !== null) {
            let newTrigger = document.createElement('div');
            newTrigger.className='scroll-trigger';
            let container = document.querySelector('.grid-attraction');
            container.appendChild(newTrigger);

  
        } else {
            hasNextPage = false;
            observer.disconnect();
        }

        observeLastElement();
    })
    .catch(error => {
        isLoading = false;
        console.error('Error fetching item',error);
    });
}

function appendAttraction(result){

    let parentDiv = document.createElement('div');
    parentDiv.className = "attraction-group";

    let topDiv = document.createElement('div');
    topDiv.className = "attraction-top";
    
    let attractionImg = document.createElement('img');
    attractionImg.src = result.images[0];
    attractionImg.className = "attraction-img";
    topDiv.appendChild(attractionImg);

    let attractionName = document.createElement('div');
    attractionName.textContent = result.name;
    attractionName.className = "attraction-name";
    topDiv.appendChild(attractionName);

    parentDiv.appendChild(topDiv);

    let attractionInfo = document.createElement('div');
    attractionInfo.className = "attraction-info";

    let attractionMrt = document.createElement('div');
    attractionMrt.textContent = result.mrt;
    attractionInfo.appendChild(attractionMrt);

    let attractionCat = document.createElement('div');
    attractionCat.textContent = result.category;
    attractionInfo.appendChild(attractionCat);

    parentDiv.appendChild(attractionInfo);

    let container = document.querySelector('.grid-attraction');
    container.appendChild(parentDiv);
    
}

function getMrt() {
    const url ='api/mrts';
    fetch(url)
    .then(response => response.json())
    .then(res => {
        if (res.hasOwnProperty('error')) {
            let errorMessage = document.createElement('div');
            errorMessage.textContent = res.message;
            let container = document.querySelector('.mrt-list');
            container.appendChild(errorMessage);
        }
        let mrts = res.data;
        for (let mrt of mrts){
            if (mrt !== 'mrt-not-exist'){
                appendMrt(mrt);
            }

        }
    })
    .catch(e => {
        console.error(e);
    });
}


function appendMrt(mrt){
    let mrtDiv = document.createElement('div');
    mrtDiv.textContent = mrt;
    mrtDiv.className = 'mrt-item';
    mrtDiv.addEventListener('click', function() {
        inputMrt(this);
    });

    let container = document.querySelector('.mrt-list');
    container.appendChild(mrtDiv);
}

function searchAttraction() {
    let keywordInput = document.getElementById('attraction-search');
    let newKeyword = keywordInput.value;
    if (newKeyword === keyword || newKeyword === "輸入景點名稱查詢") {
        return;
    }
    try {
        keyword = newKeyword;
        page=0;
        let container = document.querySelector('.grid-attraction')
        container.innerHTML = '';
        getData(page,keyword);
        observeLastElement();
    }
    catch(error){
        console.error(error);
    }
}

function inputMrt(div) {
    try {
        let keyword = div.textContent
        let keywordInput = document.getElementById('attraction-search');
        if (keywordInput.value == "輸入景點名稱查詢") {
            keywordInput.value = "";
        }
        keywordInput.value = keyword;
        
    } catch(error){
        console.error(error);
    }
}


function clearDefaultText(input) {
    if (input.value == "輸入景點名稱查詢") {
        input.value = "";
    }
}
observeLastElement();

function rightShift(){
    let selectDiv = document.getElementById('mrt-list');
    selectDiv.scrollLeft +=60;
}

function leftShift(){
    let selectDiv = document.getElementById('mrt-list');
    selectDiv.scrollLeft -=60;
}