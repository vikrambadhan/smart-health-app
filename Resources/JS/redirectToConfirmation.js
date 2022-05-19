const stripe = Stripe("XXXXXXXXXXXXXX");

const orderId = new URLSearchParams(window.location.search).get(
    "orderId"
);

checkStatus();

const myTimeout = setTimeout(redirectToConfirmation, 1500);

// Fetches the payment intent status after payment submission
async function checkStatus() {
    const clientSecret = new URLSearchParams(window.location.search).get(
        "payment_intent_client_secret"
    );

    if (!clientSecret) {
        return;
    }

    const { paymentIntent } = await stripe.retrievePaymentIntent(clientSecret);

    switch (paymentIntent.status) {
        case "succeeded":
            console.log("Payment succeeded for order Id :");
            console.log(orderId);
            postPayment(orderId);

            break;
        case "processing":
            console.log("Your payment is processing.");
            break;
        case "requires_payment_method":
            console.log("Your payment was not successful, please try again.");
            break;
        default:
            console.log("Something went wrong.");
            break;
    }
}

function postPayment(orderId) {
    // const items = { mealId: "10", orderDate: "2022-05-11 15:00:00", userId: "11" };
     fetch("https://xxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/postpayment", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
        ,body: JSON.stringify({ "orderId" : orderId}),
    });
}

function redirectToConfirmation(){
//TODO : Placeholder url for now. REPLACE THIS WITH ORDER CONFIRMATION PAGE
    let url = "https://mealdeliveryapp.s3.amazonaws.com/Resources/HTML/orderConfirmation.html?orderId=" + orderId
    window.location.replace(url);
}
