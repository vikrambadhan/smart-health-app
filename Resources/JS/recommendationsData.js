const userId = userid = window.localStorage.getItem('userid');

createOrder();

async function createOrder() {
        console.log("reached address fields")
        const response = await fetch("https://xxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/userrecommendationdata?userId=" + userId, {
            method: "GET",
            headers: { "Content-Type": "application/json" }
        });
        const { body } = await response.json();
        console.log("Received body");
        console.log(JSON.stringify(body));
        // console.log("Recommended Json :")
        // console.log(body.recommendationJson[0])
        // console.log(body.recommendationJson[1])

        if (JSON.stringify(body) === "\"No Data Found\""){
                console.log("Object is Empty")
                alert("The user currently doesn't have any nutrition information. You will be redirected to the profile page to fill out this data")
                let url = "https://mealdeliveryapp.s3.amazonaws.com/Resources/HTML/profile.html"
                window.location.replace(url);
        }else {
                console.log("Object is Not Empty")
                for(let i = 0; i< body.recommendationJson.length; i++){
                        let j=i+1;
                        let MealelementId = "meal-"+ j
                        let CallelementId = "cal-"+ j
                        let mealElement = document.getElementById(MealelementId)
                        let calElement = document.getElementById(CallelementId)
                        mealElement.innerText = body.recommendationJson[i];
                        calElement.innerText = "Calories : " + body.recommendedcalories[i]
                        calElement.style.fontWeight = 'bold';
                }

                let element = document.getElementById("loading")
                element.remove()
        }


}

function proceedToBilling(button){
        let url = "https://mealdeliveryapp.s3.amazonaws.com/Resources/HTML/pricing.html?mealid=" + (getRandomInt(13)+1)
        window.location.replace(url);
}

function getRandomInt(max) {
        return Math.floor(Math.random() * max);
}
