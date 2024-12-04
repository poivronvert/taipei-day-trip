const TAPPAY_SDK_ID = process.env.TAPPAY_SDK_ID
const TAPPAY_APP_ID = process.env.TAPPAY_APP_ID

const fields = [
    { name: 'number', placeholder: '**** **** **** ****' },
    { name: 'expirationDate', placeholder: 'MM / YY' },
    { name: 'ccv', placeholder: 'CVV' },
  ].reduce((acc, field) => {
    acc[field.name] = {
      element: `#${field.name}`,
      placeholder: field.placeholder,
    };
    return acc;
  }, {});

TPDirect.setupSDK(TAPPAY_SDK_ID, TAPPAY_APP_ID, "sandbox")

TPDirect.card.setup({
    fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style focus state
        ':focus': {
            'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6, 
        endIndex: 11
    }
})


const submitButton = document.querySelector('.confirm-block__btn');

// call TPDirect.card.getPrime when user submit form to get tappay prime
submitButton.addEventListener("click",() => {
    // 是否正確填寫聯絡資訊
    const contactName = document.getElementById("contact-name").value;
    const contactEmail = document.getElementById("contact-email").value;
    const contactPhone = document.getElementById("contact-phone").value;

    if (!contactName || !contactEmail || !contactPhone) {
      alert("請填寫所有聯絡資訊");
      return;
    }

    if (!validateEmail(contactEmail)) {
      alert("請輸入有效的電子郵件");
      return;
    }

    if (!validatePhone(contactPhone)) {
      alert("請輸入有效的手機號碼");
      return;
    }
    
    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // 確認是否可以 getPrime
    if (tappayStatus.canGetPrime === false) {
        alert("信用卡付款資訊尚未填寫或填寫有誤")
        return
    }

    // Get prime
    TPDirect.card.getPrime((result) => {
        if (result.status !== 0) {
            alert('get prime error' + result.msg)
            return
        }
        const token = localStorage.getItem("token");
        const bookingData = JSON.parse(localStorage.getItem("bookingData"));
        const attractionData = bookingData.attraction;
        const orderData = {
            "prime": result.card.prime,
            "order": {
                "price": bookingData.price,
                "trip": {
                    "attraction": {
                        "id": attractionData.id,
                        "name": attractionData.name,
                        "address": attractionData.address,
                        "image": attractionData.image
                    },
                    "date": bookingData.date,
                    "time": bookingData.time,
                },
                "contact": {
                    "name": contactName,
                    "email": contactEmail,
                    "phone": contactPhone
                }
            }
        };
        fetch("/api/orders",{
            method:"POST",
            headers:{
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            body:JSON.stringify(orderData)
        })
        .then(reponse => {return reponse.json()})
        .then(result => {
            const orderNumber = result.data.number;
            const redirectUrl = `/thankyou?number=${orderNumber}`;
            window.location.href = redirectUrl;
        })
    })
})


function validateEmail(email) {
    const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return emailPattern.test(email);
  }

  function validatePhone(phone) {
    const phonePattern = /^09\d{8}$/;
    return phonePattern.test(phone);
  }