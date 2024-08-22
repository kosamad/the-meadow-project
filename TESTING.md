<h1 align="center">The Meadow Project-Testing</h1>

![The Meadow Project on different screens]()

[View the live website here - The Meadow Project]()

---
<h2>Contents</h2>







# Introduction

Testing is essential to ensure the website functions correctly, is free from bugs, and allows users to fully utilise all features before its release to the general market. This guarantees a positive user experience (UX) and encourages repeat visits from customers and registered users.

Throughout the development process, I relied on Chrome developer tools to assess page responsiveness across various screen sizes and address any encountered issues. In troubleshooting, I utilised the console to log and monitor JavaScript code, aiding in resolving aspects of the site that did not perform as intended. Additionally, I employed Python development techniques to address backend issues, ensuring seamless functionality across the site. All the test results detailed below are based on the [deployed site]().

---

# Automated Testing

The automated testing implemented in this project complements the manual tests, ensuring that the Python code fulfilled its objectives from the outset. The testing strategy was not aimed at achieving 100% coverage but at supporting and enhancing the manual testing process. To run tests I have used the Django Testing Framework. 

The tests for each app are organized into a tests folder. Note that tests were conducted using the local database, as Heroku does not support automatic testing of its databases. During testing, the Postgres database configuration in settings.py was commented out to facilitate running tests locally.

To run the tests:

* Type "python3 manage.py test" into the terminal.
* To test one app only type "python manage.py test <app name>".
* To understand how comprehensive the test are, generate a coverage report using the command "coverage report".
* To view the coverage report in your web browser, type "coverage html" and open the "index.html" file newly created directory.

During this build, I utilised [Travis](https://www.travis-ci.com/) CI to automatically run tests each time my project was deployed. This ensured I was promptly notified of any test failures caused by new code, allowing me to address issues before they were merged into my main branch. This also meant I did not need to alter my settings.py file to run tests. 

# Manual Testing

The desktop version of the site underwent testing across various browsers and devices to ensure compatibility. Testing included Google Chrome, Mozilla Firefox, and Microsoft Edge on desktop computers. Additionally, Chrome was tested on both Lenovo Tablet and Pixel devices, while Safari was used for mobile testing.

The site was responsive on all browsers and devices (down to  320px as recommended by [Free Code Camp](https://www.freecodecamp.org/news/media-query-css-example-max-and-min-screen-width-for-mobile-responsive-design/))





## Testing User Stories

The site was built from the User Stories documented in the [Readme](README.md#user-stories). The site was tested against each of them and the results are documented below.

1. As a **potential customer**, I want to be able to:

* Immediately understand the purpose of the site and get a sense of its ethos.
    * The site opens with a stunning logo image of vibrant flowers, immediately drawing the user's attention. This is followed by a visually engaging image summary highlighting the main features of the shop. The presence of the navigation bar helps the user understand what the site offers from the very start. The home page gives a summary of the site and its ethos both using words and pictures. 

* Navigate to areas of interest quickly and easily.
    * The clear and intuitive navigation bar at the top of the page allows users to effortlessly explore the different sections of the site. 

* Filter what products I'm looking for.
    * Users can search the shop from the nav bar and can filter products by category on the main shop page.

* Visit the site on all my devices.
    * the site is responsive on all devices and has been designed to work on various screen sizes. 

* Find and understand key information about products including descriptions, costs, and delivery information so I can make an informed purchasing decision.
    * The main shop page clearly lists each product and event by name, along with their prices. Detailed information is available on individual product and event pages, including clear delivery details. Additional information about the site can be found on the About page.

* Understand what the company stands for and see it aligns with my values.
    * Users can navigate to the about page to understnad more about The Meadow Project and learn how they work. This will inform users if the site aligns with their values.

* Pick a delivery date that suits me.
    * Users can pick a delivery/pick up date that is convinent for them. 

* Add a message with my bouquet/plant delivery
    * Users can submit an order with a card message.

* Add a note to my order to say to avoid roses, or yellow flowers.
    * Users can submit an order with a note to the seller.

* Learn about future events I might want to sign up for.
    * Users can browse events in the shop by filtering by the events category. Future events are listed to encourage users to learn more about them and sign up. 

* View where the company is based so I can see if event attendance is possible.
    *  Users can see the contact/address information for The Meadow Project in the footer. They can also see this on the contact page, where a map is rendered to enhance UX. The about page gives more information about the event venue. This information is clearly linked from the event detail pages making it easy for a user to find. 

* Read reviews from other customers to help me make an informed purchasing decision.
    * Reveiws can be left by users with an account for each order. These are rendered to the home page. 

* Sign up for the site's newsletter so I can be informed about new events, products, and rewards.
    * Users are encouraged to sign up for the site at various points, including in the footer, during the checkout process to store their address information, and on the blog page, which offers a link to sign up and be the first to hear about new blog posts.

* Contact the business to ask any questions before making a purchase.
    * Users can use the contact information given in the footer, or can use the contact form on the contact page to get in touch with The Meadow Project. 

* Add products to my basket, so I can make a purchase when I'm ready to and have confidence they have been added succesfully.
    * Products can be easily added to a user's basket directly from their detail pages. The session is stored, making it even more convenient for users, as they can return to the site later and still see their basket with items saved. This allows them to continue browsing the shop and complete their transaction whenever they're ready.

* View my basket and identify how much my order might cost me.
    * Users can access their basekt from the Bag Icon in the navigation bar, allowing them to easily see their items at any time. A toast informs the user of this information when they add a item to their basket. 

* See adverts for part of the site I might not have thought of.
    * This has not been implemented at this time but is flagged as a future development. 

* Follow the companies social media platforms. 
    * Social media links are given in the footer. 

As a **buying customer** , I would also like to be able to:

* Easily input my delivery and card information.
    * The checkout form allows a user to easily input this information.

* Register on the site so I can make further purchases more easily.
    * Users are encouraged to sign up for the site at various points, including in the footer, during the checkout process to store their address information, and on the blog page, which offers a link to sign up and be the first to hear about new blog posts.

* Remove unwanted items from my basket. 
    * Items can be easily removed from the basket by clicking the bin icon next to each product. The ability to adjust the bag is also available from the checkout page giving the user convient ways to ammend their order if they need to. 

* Be able to add more than one person to an event's booking.
    * Users input the attendee names into their booking therefore they can purchace two tickets at once. 

* Recieve an email confirmation of my order once complete.
    * An automatic email is sent to users once they have completed their order. Further to this, Event tickets are also automatically sent out if they have been purchaced. 

As a **registerd user**, I would also like to be able to:

* Sign into my account.
    * Users can sign into their account from the Profile Icon in the navigation bar.

* Find previous oders easily and see a summary.
    * The profile page renders a users order history with a summary of the items purchaced. They can see further details by clicking the order number.

* Contact the business about a specific order.
    * If a user is logged in, the contact form renders a drop down menu of previous orders, listing the number and the date to help the user idenfiy which order they want to contact the site about. This is submitted with the form.

* Update my details.
    * Name and address details can be updated from the profile page. 

* Change my password.
    * This is integrated using Django Allauth. Users can change their password if they need to using a link from the profile page.

* Reset my password if I forget it.
    * This is integrated using Django Allauth and can be accessed from the log in page. 

* Sign out of my account.
    * Users can sign out of their accounts using the drop down option from the Profile Icon in the navigation bar. 

* Add/Edit reviews to products to help others be informed about their purchasing decsions. 
    * At present a user can only add a reveiw to the site and not edit them. This was a purposful decision during the creation of the site. This is to ensure that reveiws don't get changed if a user decides to modify previous content. They can contact the site owners to remove any reveiws they no longer want listed. 

As a **business owner** user, I would like to be able to:

* Add, edit, and delete events on the site quickly and easily.
    * Only superusers can add events, which they can do from their profile page (the management page) or directly from the shop. Superusers also have the ability to edit or delete items, either from their individual detail pages or directly from the shop page via the item's card.

* View an event summary, including who is booked for each event.
    * An email is sent to owners when a user checks out an event. This lists the attendees. 

* Have immediate access to customer information, including those registered to receive our newsletter and discounts.
    * These features haven't been implemented at this time so a customer information interface has not been developed. This is noted as a future development.

* Amend the reward codes the site is accepting.
    * This feature hasn't been implemented at this time. 

* Edit and delete products and their prices.
    * Items can be edited using the form connected to each product. This can be accessed via the shop cards, or via the item detail page. Delete function is accessed from the same places. 

* Delete user reviews (if malicious).
    * Superusers have access to a table which lists all reveiws submitted to the site. They can use this to find and delete malicious reveiws. 

* Track sales data to see which products are most popular and help with stock control.
    * This feature hasn't been implemented at this time.

* Add a blog post to the site.
    * Superusers can add a blog post from the main blog page or using the button in their admin profile. Both buttons take them to the form which allows them to submit a post to the site. 

* Control stock.
     * This feature hasn't been implemented at this time.

* Receive emails from users who contact the business via the contact form(s)
    * The contact form on the site sends an email to The Meadow Project. This can be picked up by team members and easily resolved. 




## Real User Testing

## Mobile and Desktop Test Results

# Validators
