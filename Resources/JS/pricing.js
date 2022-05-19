const mealId = new URLSearchParams(window.location.search).get(
    "mealid"
);

function proceedToBilling(button){
    console.log("the meal id is : ")
    console.log(mealId)
    console.log("the price of the button is is : ")
    console.log(button.getAttribute('price'));

    console.log("the frequency of the button is is : ")
    console.log(button.getAttribute('frequency'));

    let price = button.getAttribute('price');
    let frequency = button.getAttribute('frequency');


    let url = "https://xxxxxxxxxx.s3.amazonaws.com/Resources/HTML/billinginfo.html?mealId="
        + mealId + "&frequency=" + frequency + "&price=" + price
    window.location.replace(url);
}
