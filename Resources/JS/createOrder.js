// Already defined in getMealInfo
// const mealId = new URLSearchParams(window.location.search).get(
//     "mealId"
// );

async function createOrder() {
    const price = document.getElementById("mealPrice").innerHTML
    const frequency = document.getElementById("mealFrequency").innerHTML

    if(validateFields()){
        console.log("reached address fields")
        userid = window.localStorage.getItem('userid');
        // const items = { mealId: "10", orderDate: "2022-05-11 15:00:00", userId: "11" };
        const response = await fetch("https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/createorder", {
            method: "POST",
            headers: { "Content-Type": "application/json" }
            ,body: JSON.stringify({ "mealId": mealId , "userId": userid, "orderAmount" : price, "frequency": frequency,
            'street' : document.getElementById("streetAddress").value,
            'city' : document.getElementById("city").value,
            'state' : document.getElementById("state").value,
            'country' : document.getElementById("country").value,
            'zip' : document.getElementById("zip").value
            }),
        });
        const { orderId } = await response.json();
        console.log("Received orderId");
        console.log(orderId);
        let url = "https://mealdeliveryapp.s3.amazonaws.com/Resources/HTML/checkout.html?orderId=" + orderId

        window.location.replace(url);
    }
    else{
        alert("All the shipping fields are required")
    }
}

function validateFields(){
    const streetAddress = document.getElementById("streetAddress").value
    const city = document.getElementById("city").value
    const state = document.getElementById("state").value
    const country = document.getElementById("country").value
    const zip = document.getElementById("zip").value
    // console.log("Values are as follows : ")
    // console.log(streetAddress)
    // console.log(city)
    // console.log(state)
    // console.log(country)
    // console.log(zip)
    return !(streetAddress === '' || city === '' || state === '' || country === '' || zip === '');
}
