const mealId = new URLSearchParams(window.location.search).get(
    "mealId"
);

const price = new URLSearchParams(window.location.search).get(
    "price"
);
const frequency = new URLSearchParams(window.location.search).get(
    "frequency"
);


getMealInfo();

async function getMealInfo() {
    const response = await fetch("https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/getmealdata?mealId=" + mealId, {
        method: "GET",
        headers: { "Content-Type": "application/json" }
    });
    const { mealInfo } = await response.json();

    console.log("Received meal info: ");
    console.log(mealInfo);
    console.log("Meal ID :  ");
    console.log(mealInfo[0].meal_id);
    console.log("Meal Description :  ");
    console.log(mealInfo[0].mealdesc);
    console.log("Meal Name :  ");
    console.log(mealInfo[0].mealname);
    console.log("Meal mealPrice :  ");
    console.log(mealInfo[0].mealprice);
    setElementText(mealInfo);

    let element = document.getElementById("loading")
    element.remove()

}

function setElementText(mealInfo){
    let mealName = document.getElementById("mealName");
    mealName.innerText = mealInfo[0].category;

    let mealDescription = document.getElementById("mealDescription");
    mealDescription.innerText = mealInfo[0].mealdesc;

    let mealPrice = document.getElementById("mealPrice");
    mealPrice.innerText = price;

    let mealFrequency = document.getElementById("mealFrequency");
    mealFrequency.innerText = frequency;
}
