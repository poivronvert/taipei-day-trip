async function fetchData(url){
    const token = localStorage.getItem('authToken');
    try {
        const response = await fetch(url, {
            headers:{
                'Authorization': `Bearer ${token}`
            }
        });

        return response.json();

    } catch (error) {
        console.error('Error fetching data', error);
        throw error;
    }
}

document.addEventListener('DOMContentLoaded', async()=> {
    const url = '/api/booking';
    let token = localStorage.getItem('authToken'.split('.'));
    let info = token[1];
    let user = JSON.parse(decodeURIComponent(window.atob(info)));

    try {
        const bookingData = await fetchData(url);

        const welcomeName = document.getElementById('welcomeName');

        const existedData = document.getElementById('optionExist');
        const nullData = document.getElementById('optionNone');

        welcomeName.innerHTML = '您好，'+ user['name'] + '待預定的行程如下：'

        if (bookingData.data==null) {
            nullData.style.display = 'block';
            existedData.style.display = 'none';
            nullData.innerHTML = "目前沒有任何待預訂的行程";
        }
        


    }
    catch (error){
        console.log('伺服器內部錯誤')

    }
});

