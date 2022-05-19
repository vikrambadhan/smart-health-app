      // This is a public sample test API key.
      // Don’t submit any personally identifiable information in requests made with this key.
      // Sign in to see your own test API key embedded in code samples.
const stripe = Stripe("......bcLZXimm.......");

let elements;

initialize();

// Fetches a payment intent and captures the client secret
async function initialize() {
  const response = await fetch("https://fjnmcs782f.execute-api.us-east-1.amazonaws.com/dev/getpaymentinent", {
    method: "GET",
    headers: { "Content-Type": "application/json" }
  });
  const { clientSecret } = await response.json();
  // console.log("Received response");
  // console.log(clientSecret);

  const appearance = {
    theme: 'stripe',
  };
  elements = stripe.elements({ appearance, clientSecret });

  // console.log("Got elements");
  // console.log(elements);
  document
      .querySelector("#payment-form")
      .addEventListener("submit", handleSubmit);

  const paymentElement = elements.create("payment");
  paymentElement.mount("#payment-element");
}

async function handleSubmit(e) {
  e.preventDefault();
  setLoading(true);

  const orderId = new URLSearchParams(window.location.search).get(
      "orderId"
  );

  let url = "http://localhost:63342/smart-health-app/Resources/HTML/paymentConfirmation.html?orderId=" + orderId

  const { error } = await stripe.confirmPayment({
    elements,
    confirmParams: {
      // Make sure to change this to your payment completion page
      return_url: url,
    },
  });

  // This point will only be reached if there is an immediate error when
  // confirming the payment. Otherwise, your customer will be redirected to
  // your `return_url`. For some payment methods like iDEAL, your customer will
  // be redirected to an intermediate site first to authorize the payment, then
  // redirected to the `return_url`.
  if (error.type === "card_error" || error.type === "validation_error") {
    showMessage(error.message);
  } else {
    showMessage("An unexpected error occured.");
  }

  setLoading(false);
}


// ------- UI helpers -------

function showMessage(messageText) {
  const messageContainer = document.querySelector("#payment-message");

  messageContainer.classList.remove("hidden");
  messageContainer.textContent = messageText;

  setTimeout(function () {
    messageContainer.classList.add("hidden");
    messageText.textContent = "";
  }, 4000);
}

// Show a spinner on payment submission
function setLoading(isLoading) {
  if (isLoading) {
    // Disable the button and show a spinner
    document.querySelector("#submit").disabled = true;
    document.querySelector("#spinner").classList.remove("hidden");
    document.querySelector("#button-text").classList.add("hidden");
  } else {
    document.querySelector("#submit").disabled = false;
    document.querySelector("#spinner").classList.add("hidden");
    document.querySelector("#button-text").classList.remove("hidden");
  }
}
