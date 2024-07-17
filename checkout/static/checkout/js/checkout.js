document.addEventListener('DOMContentLoaded', function () {

    // Delivery method input selector, when the user clicks the button it triggers the function to show/hide delivery details 
    const deliveryMethodInputs = document.querySelectorAll(
        'input[name="delivery_method"], #delivery_method_wrapper select');
    deliveryMethodInputs.forEach(input => {
        input.addEventListener('change', toggleDeliveryDetails);
    });

    toggleDeliveryDetails();

    //Delivery method for Products
    // listens for a change on the select radio box for delivery
    const deliveryMethodSelect = document.querySelector('#delivery_method_wrapper select');
    if (deliveryMethodSelect) {
        deliveryMethodSelect.addEventListener('change', function () {
            toggleDeliveryDetails();
        });
    }
});

// Displays the delivery information if delivery was selected.
function toggleDeliveryDetails() {
    const deliveryDetails = document.querySelector('.delivery-details');
    const shopDetails = document.querySelector('.shop-details');
    const deliveryMethod = document.querySelector('input[name="delivery_method"]:checked') || document
        .querySelector('#delivery_method_wrapper select');

    if (deliveryMethod && deliveryMethod.value === 'delivery') {
        deliveryDetails.style.display = 'block';
        shopDetails.style.display = 'none';
    } else if (deliveryMethod && deliveryMethod.value === 'pickup') {
        deliveryDetails.style.display = 'none';
        shopDetails.style.display = 'block';
    } else {
        deliveryDetails.style.display = 'none';
        shopDetails.style.display = 'none';
    }
}



// Functions to show/hide the different form parts. step = current step user is on.    
// Validate fields for the current step by getting the form elements required.
// Alert if a field is missing. 

let orderType = "{{ order_type }}";

// Function to validate fields and show next step
function validateAndShowNextStep(currentStep) {
    const orderType = "{{ order_type }}";

    if (currentStep === 1) {
        const fullName = document.getElementById('id_full_name').value.trim();
        const email = document.getElementById('id_email').value.trim();

        if (!fullName || !email) {
            alert('Please fill out all fields required by Customer Details');
            return;
        }
    } else if (currentStep === 2) {
        const phoneNumber = document.getElementById('id_phone_number').value.trim();
        const streetAddress1 = document.getElementById('id_street_address1').value.trim();
        const townOrCity = document.getElementById('id_town_or_city').value.trim();
        const county = document.getElementById('id_county').value.trim();
        const postcode = document.getElementById('id_postcode').value.trim();

        if (!phoneNumber || !streetAddress1 || !townOrCity || !county || !postcode) {
            alert('Please fill out all fields required by Customer Address');
            return;
        }
    } else if (currentStep === 3) {
        if (orderType === 'product') {
            const deliveryDate = document.getElementById('id_delivery_date').value.trim();
            const deliveryMethod = document.querySelector('input[name="delivery_method"]:checked');
            if (!deliveryMethod || !deliveryDate) {
                alert('Please select a delivery method and date.');
                return;
            }

            if (deliveryMethod.value === 'delivery') {
                const deliveryDate = document.getElementById('id_delivery_date').value.trim();
                const deliveryName = document.getElementById('id_delivery_name').value.trim();
                const deliveryStreetAddress1 = document.getElementById('id_delivery_street_address1').value
                    .trim();
                const deliveryTownOrCity = document.getElementById('id_delivery_town_or_city').value.trim();
                const deliveryCounty = document.getElementById('id_delivery_county').value.trim();
                const deliveryPostcode = document.getElementById('id_delivery_postcode').value.trim();

                if (!deliveryDate || !deliveryName || !deliveryStreetAddress1 ||
                    !deliveryTownOrCity || !deliveryCounty || !deliveryPostcode) {
                    alert('Please fill out all required Delivery Information.');
                    return;
                }
            }
        }
    }

    // If form is valid hide current step and display next step.    
    document.getElementById(`step-${currentStep}`).style.display = 'none';
    document.getElementById(`step-${currentStep + 1}`).style.display = 'block';
}

// hide's the next step from view when the user goes back and shows the step they are on. 
function showPreviousStep(step) {
    document.getElementById(`step-${step + 1}`).style.display = 'none';
    document.getElementById(`step-${step}`).style.display = 'block';
}