
// Code taken and adapted from the CI tutorial for Boutiqu Ado

// Get keys
var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);
//create a variable using our stripe public key.
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();
var card = elements.create('card');

// style elements from stripe JS modified to match site design/bootstrap
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};


// var card = elements.create('card', {
//     style: style
// });

// mount into the card div in checkout.html
card.mount('#card-element', {style:style});