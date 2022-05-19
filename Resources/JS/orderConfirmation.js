const orderId = new URLSearchParams(window.location.search).get(
    "orderId"
);

getOrder();

async function getOrder() {
    const response = await fetch("https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/getorder?orderId=" + orderId, {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    // console.log("Response Received : ")
    // const BigResponse = await response.json();
    // console.log(BigResponse);
    const { orderInfo, mealInfo } = await response.json();
    // console.log("Received orderInfo");
    // console.log(orderInfo);
    // console.log("Received MealInfo");
    // console.log(mealInfo);
    // console.log("Meal ID :  ");
    // console.log(orderInfo[0].orderId);
    // console.log("Meal Date :  ");
    // console.log(orderInfo[0].orderDate);
    // console.log("Meal Price :  ");
    // console.log(orderInfo[0].orderAmount);

    // console.log("Meal Frequency :  ");
    // console.log(orderInfo[0].frequency);

    setElementText(orderInfo, mealInfo);
    let element = document.getElementById("loading")
    element.remove()
}


function setElementText(orderInfo, mealInfo){
    let mealName = document.getElementById("mealName");
    mealName.innerText = mealInfo[0].mealname;

    let mealDescription = document.getElementById("mealDescription");
    mealDescription.innerText = mealInfo[0].mealdesc;

    let mealPrice = document.getElementById("mealPrice");
    mealPrice.innerText = mealInfo[0].mealprice;

    let orderDate = document.getElementById("orderDate");
    orderDate.innerText = orderInfo[0].orderDate;

    let mealFrequency = document.getElementById("mealFrequency");
    mealFrequency.innerText = orderInfo[0].frequency;

}
