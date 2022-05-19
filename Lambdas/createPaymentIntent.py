import json
import stripe


def lambda_handler(event, context):
    stripe.api_key = "##key###"


    # Alternatively, set up a webhook to listen for the payment_intent.succeeded event
    # and attach the PaymentMethod to a new Customer
    customer = stripe.Customer.create()

    try:
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            customer=customer['id'],
            setup_future_usage='off_session',
            amount=690984,
            currency='usd',

            payment_method_types=["card"],
        )
        return {
            'clientSecret': intent["client_secret"]
        }
    except Exception as e:
        print(str(e))

    # response = stripe.PaymentIntent.create(
    #     amount=2000,
    #     currency="usd",
    #     payment_method_types=["card"],
    # )
    # # data_json = json.loads(response);
    # print(response["client_secret"]);

