let page = 0;
let keyword = "";
let isLoading = false;
let initialLoadCompleted = false;
let hasNextPage = false;
let observer;

document.addEventListener('DOMContentLoaded', function () {
    if (!initialLoadCompleted) {
        hasNextPage = true;
        loadData();
        initialLoadCompleted = true;
    }
    getMrt();
    observeLastElement();
});

let callback = function(entries){
    entries.forEach(entry => {
        if (entry.isIntersecting && !isLoading && initialLoadCompleted && hasNextPage) {
            page++;
            isLoading = true;
            loadData();
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

function loadData() {
    if (!hasNextPage) return;

    const url = `/api/attractions?page=${page}&keyword=${keyword}`
    fetch(url)
        .then(response => response.json())
        .then(res => {
            isLoading = false;

            if (res.error) {
                let container = document.querySelector('.grid-attraction');
                return container.innerHTML = "找不到資料！！";
            }
            
            appendAttractions(res.data);

            updateScrollTrigger(res.nextPage);
            console.log('下一頁:',res.nextPage);

        })
        .catch(error => {
            isLoading = false;
            console.error('Error fetching item', error);
        });
}

function appendAttractions(attractions) {
    attractions.forEach(attraction => {
        appendAttraction(attraction);
    });
}

function updateScrollTrigger(nextPage) {
    let oldTrigger = document.querySelector('.scroll-trigger');
    if(oldTrigger){
        oldTrigger.remove();
    }

    if (nextPage !== null){
        let newTrigger = document.createElement('div');
        newTrigger.className = 'scroll-trigger';
        let container = document.querySelector('.grid-attraction');
        container.appendChild(newTrigger);
        hasNextPage = true;
        observeLastElement();
    } else {
        hasNextPage = false;
        if (observer) {
            observer.disconnect();
        }
    }
}

function appendAttraction(result){
    let parentDiv = document.createElement('div');
    parentDiv.className = "attraction-group";

    let topDiv = document.createElement('div');
    topDiv.className = "attraction-top";

    let attractionA = document.createElement('a');
    attractionA.href= 'attraction/'+result.id;

    let attractionImg = document.createElement('img');
    attractionImg.src = result.images[0];
    attractionImg.className = "attraction-img";
    topDiv.appendChild(attractionImg);

    let attractionName = document.createElement('div');
    attractionName.textContent = result.name;
    attractionName.className = "attraction-name";
    topDiv.appendChild(attractionName);

    attractionA.appendChild(topDiv);
    parentDiv.appendChild(attractionA);

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
    const url = 'api/mrts';
    fetch(url)
        .then(response => response.json())
        .then(res => {
            if (!res.error) {
                let mrts = res.data;
                for (let mrt of mrts) {
                    if (mrt !== 'mrt-not-exist') {
                        appendMrt(mrt);
                    }
                }
            }
        })
        .catch(e => {
            console.error('getMrt Error:', e);
        });
}


function appendMrt(mrt) {
    let mrtDiv = document.createElement('div');
    mrtDiv.textContent = mrt;
    mrtDiv.className = 'mrt-item';
    mrtDiv.addEventListener('click', function () {
        inputMrt(this);
        searchAttraction();
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
        page = 0;
        let container = document.querySelector('.grid-attraction')
        container.innerHTML = '';
        hasNextPage = true;
        loadData();
        observeLastElement();
    }
    catch (error) {
        console.error("searchAttraction Error: ", error);
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

    } catch (error) {
        console.error("inputMrt Error", error);
    }
}


function clearDefaultText(input) {
    if (input.value == "輸入景點名稱查詢") {
        input.value = "";
    }
}

function rightShift() {
    let selectDiv = document.getElementById('mrt-list');
    selectDiv.scrollLeft += 60;
}

function leftShift() {
    let selectDiv = document.getElementById('mrt-list');
    selectDiv.scrollLeft -= 60;
}