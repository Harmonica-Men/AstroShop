# Agile

# Table Of Contents

- Agile [KanBan](https://github.com/users/Harmonica-Men/projects/12)

- Table Of Contents
    - [Benefits of agile development](#benefits-of-agile-development)
    - [MoSCoW](#moscow)   
    - [Milestones](#milestones)
    - [User Stories and Epics](#user-stories-and-epics)
    - [Story Points](#story-points)
    - [Interactions & Milestones](#iterations-and-milestones)
    - [Kanban Board](#kanban-board)
    - [User Stories](#user-stories)
    - [List Of Epics](#list-of-epics)
  - [UX Table Of Contents](#the-ux-table-of-contents)
    - [Welcome and Introduction](#1-welcome-and-introduction)
    - [Product Page](#2-product-page)
    - [Nav-bar](#3-nav-bar)
    - [Sign-Up Process](#4-sign-up-process)
    - [Product Details](#5-product-details)
    - [The Shopping Cart](#6-the-shopping-cart)
    - [Check Out](#7-check-out)
    - [Payment](#8-payment)
    - [Email Confirmation](#9-email-confirmation-and-redirect-to-merchant)
    - [Review and follow up orders](#10-review-and-follow-up-orders)


## Benefits of agile development

As mentioned in the introduction there was a learning curve associated with using agile development for the first time, however there was a received number of benefits associated as well. These benefits include:

 1. Having a plan in place. It was easier to know which task I was working on and found myself getting less distracted as I was carrying out the work associated with the project.
 2. Having a dedicated timeframe for issues to be done. This helped me stay on track in terms of timeframe for the project.
 3. Initial overall planning of the project. As a lot of thought went into the user stories I was able to have a better picture of the overall project before starting the work. This sped up production and definitely felt more organised.
 4. Easily see the benefits of collaboration. As I was working on this project on my own it was easy to see how the use of agile would benefit collaboration if multiple people where working on a project together. Especially with the Kanban board, being able to see what is being worked on and the status of the work and also being able to assign this work to individual developers.

## MoSCoW

Having created the user stories, I used **MoSCoW prioritisation** to ensure that the most important requirements were addressed first. MoSCoW is a useful technique for managing project scope and ensuring that critical tasks are prioritised, while also providing flexibility in the development process. Here's how I applied the MoSCoW method:

- **Must-Have**: Critical requirements that are essential for project success.
- **Should-Have**: Important requirements that significantly add value.
- **Could-Have**: Desirable features that provide additional benefits.
- **Won't-Have**: Features explicitly excluded from the project scope.

This method is beneficial as it allows for clear communication about what will be delivered in each iteration. It ensures that essential features are prioritised, while also managing expectations by clearly defining what will not be included. By using MoSCoW prioritisation, I was able to focus on delivering the highest value to users and stakeholders first, while still maintaining the flexibility to address lower-priority features later in the project.

[Table Of Contents](#table-of-contents)

## Milestones 

The project was divided into three milestones, each containing the corresponding epics and user stories: [Milestone in Projects](https://github.com/Harmonica-Men/AstroShop/milestones)
<br>

1. [Setting Up The Project @ Bear minimums](https://github.com/Harmonica-Men/AstroShop/issues/18)
- Task: The goal is to set up the project at its bare minimum.
  - EPIC 0 (Repository and Deploy Early)

2. [Basic Astro Shop Functionality](https://github.com/Harmonica-Men/AstroShop/milestone/3)
- Task: Implement basic Astro Shop functionality including models, views, and templates.
  - EPIC 1 (Viewing and Navigation)
  - EPIC 2 (Registration and User Accounts) 
  - EPIC 3 (Sorting and Searching)  
  - EPIC 4 (Pruchasing and checkout)

3. [Testing and Validation](https://github.com/Harmonica-Men/AstroShop/milestone/2)
- Task: test & validate
  - EPIC 5 (Testing and Validations) 

## User Stories and Epics

Astro Shop is designed for individuals passionate about astronomy and related subjects/objects.  

During the project planning phase, I carefully analyzed and defined the functional requirements for the platform. I considered the website's primary goals, the needs of its target audience, and the features that would deliver the most value to users. From this foundation, I crafted user stories to outline the required functionalities.  

These user stories were documented as issues on GitHub. Any requirement that was too extensive to fit into a single user story was categorized as an Epic, with related user stories grouped under it. This method ensured that large tasks could be broken down into smaller, more manageable components.  

Each user story included:  
- **Title** - A concise description summarizing the user story.  
- **Description** - Structured as: *As a **[role]**, I can **[capability]** so that **[received benefit]***.  
- **Acceptance Criteria** - Specific conditions that must be met for the feature to be accepted by the user.  
- **Unit Tasks** - A detailed breakdown of tasks required to complete the user story.  
- **MoSCoW Label** - Prioritization of tasks using the MoSCoW method (Must have, Should have, Could have, Won’t have).  

Additionally, the following fields were tracked:  
- **Assignee** - The team member responsible for completing the user story.  
- **Milestone** - The associated Epic or project milestone.  

An Agile methodology was used to organize and execute the project. This was implemented via the GitHub Project Board, which helped manage milestones, epics, user stories, and tasks effectively. Each user story was labeled with a MoSCoW prioritization to ensure clarity and focus throughout the development process.

### Story Points

In this project, story points were used to estimate the relative complexity of each user story, enabling efficient time management and iteration planning. Each story was assigned a point value of 1, 2, 3, 5, 8, 13, or 21 based on the Fibonacci sequence, which provides a non-linear scale to account for increasing uncertainty with more complex tasks. By analysing the tasks and acceptance criteria for each story, I determined its difficulty relative to others, ensuring a realistic assessment of workload. This method facilitated the prediction of solo velocity for each iteration, aiding in the planning of future development cycles and prioritisation of features.

### Iterations and Milestones

To organise and manage progress, I divided the project into 7 weekly iterations, each represented by a milestone in GitHub. 

- Story Point Allocation: User stories were prioritised and assigned story points to estimate effort. The total story points were divided evenly across the 7 iterations.
- Adding to Iterations: At the start of each iteration, user stories were added until their total story points matched the planned weekly workload.
- Adjustments: Incomplete tasks at the end of an iteration were moved back to the backlog (or no-status) for refinement and included in the next iteration.

This approach ensured steady progress throughout the project while allowing flexibility to adjust as needed.

### Kanban Board

To manage and track the progress of user stories during the project, I created a Kanban Board board. The board was divided into four columns: **Epics**, **To Do**, **In Progress**, and **Done**.

- Epics: This column contained overarching goals that grouped related user stories together.
- To Do: At the start of each iteration, user stories to be completed were moved here.
- In Progress: As work began on a user story, it was moved to this column.
- Done: Completed user stories were moved to this column to indicate they were finished.

This setup provided a clear and simple way to track the status of tasks throughout the project, ensuring that progress was organised and transparent.

**Github Kanboard During Development**

You can view the [Astro Shop Kanban Board](https://github.com/users/Harmonica-Men/projects/12) for a detailed overview of the project's progress and task management.

### User stories 

A user story is an explanation of a software feature written from the perspective of the end user. Its purpose is to articulate how a software feature will provide value to the customer. User stories were created with the help of GitHub issues. Each user story contains:
* Title - Short description of the user story. 
* Description - As a **role** i can **capability** so that **received benefit**.
* Acceptance criteria - A set of conditions that a feature must meet to be accepted by the user. 
* Unit tasks - A break down of each task needed to complete user story. 
* A MoSCoW label - To prioritise tasks. 
* Assignee -  Who the user store is assigned too. 
* Milestone - Which epic this user store is associated with.

Below is an example of how the user stories where structured for this project.

[Table Of Contents](#table-of-contents)

### List of Epics

- [EPIC 0: Repository and Deploy Early](https://github.com/Harmonica-Men/AstroShop/issues/18)
- [EPIC 1: Viewing and Navigation](https://github.com/users/Harmonica-Men/projects/12?pane=issue&itemId=90498491&issue=Harmonica-Men%7CAstroShop%7C22)
- [EPIC 2: Registration and User Accounts](https://github.com/users/Harmonica-Men/projects/12?pane=issue&itemId=90498621&issue=Harmonica-Men%7CAstroShop%7C23)
- [EPIC 3: Sorting and Searching](https://github.com/users/Harmonica-Men/projects/12?pane=issue&itemId=90498654&issue=Harmonica-Men%7CAstroShop%7C24)
- [EPIC 4: Purchasing and checkout](https://github.com/users/Harmonica-Men/projects/12?pane=issue&itemId=90498707&issue=Harmonica-Men%7CAstroShop%7C25#:~:text=EPIC%204-,Purchasing%20and%20checkout,-%2325)
- [EPIC 5: Testing and Validations](https://github.com/Harmonica-Men/AstroShop/issues/40)

User Stories with their id: <br>
#### EPIC 0
- As a software developer, I can set up the VS Code IDE on my local machine, so that I can efficiently develop and debug my projects. [#31](https://github.com/Harmonica-Men/AstroShop/issues/31)
- As a software developer, I want to set up a GitHub repository for our new project, so that the team can collaborate on the codebase efficiently and maintain version control. [#30](https://github.com/Harmonica-Men/AstroShop/issues/30)
- As a software developer, I can to create a working Django app, so that I can build and deploy a web application efficiently. [#32](https://github.com/Harmonica-Men/AstroShop/issues/32)
- As a software developer, I want to deploy our application to Heroku, so that it is accessible to users and can be tested in a live environment. [#33](https://github.com/Harmonica-Men/AstroShop/issues/33)
- As a software developer, I want to set up a GitHub repository for our new project, so that the team can collaborate on the codebase efficiently and maintain version control.[#34](https://github.com/Harmonica-Men/AstroShop/issues/34)

#### EPIC 1
- As a shopper, I can view specific categories of products so that I quickly find the items I'm interested in and make informed purchasing decisions.[#3](https://github.com/Harmonica-Men/AstroShop/issues/3)
- As a shopper, I want to be able to view individual product details so that I can identify the price, description, product rating, product image, and available sizes.[#4](https://github.com/Harmonica-Men/AstroShop/issues/4)
- As a shopper I can be able to quickly identify deals, clearance items, and special offers so that I take advantage of special savings on products I’d like to purchase.[#5](https://github.com/Harmonica-Men/AstroShop/issues/5)
- As a shopper, I want to easily view the total of my purchases at any time, so that I can avoid spending too much.[#28](https://github.com/Harmonica-Men/AstroShop/issues/28)

#### EPIC 2
- As a Site User I can easily register for an account so that I can have a personal account and view my profile.[#35](https://github.com/Harmonica-Men/AstroShop/issues/35)
- As a Site User I can easily log in or log out so that I can access my personal account information.[#36](https://github.com/Harmonica-Men/AstroShop/issues/36)
- As a Site User I can easily recover my password in case I forget it so that I can recover my personal account.[#37](https://github.com/Harmonica-Men/AstroShop/issues/37)
- As a Site User I can receive an email confirmation after registering so that I can verify that my account registration was successful.[#38](https://github.com/Harmonica-Men/AstroShop/issues/38)
- As a Site User I can have a personalized user profile so that I can view my personal order history, order confirmations, and save my payment information.[#39](https://github.com/Harmonica-Men/AstroShop/issues/39)

#### EPIC 3
- As a shopper, I can sort the list of available products so that I can easily identify the best-rated, best-priced, and categorically sorted products.[#12](https://github.com/Harmonica-Men/AstroShop/issues/12)
- As a shopper, I can sort a specific category of products so that I can find the best-priced or best-rated product in that category or sort the products by their names.[#13](https://github.com/Harmonica-Men/AstroShop/issues/13)
- As a Site User I can easily recover my password in case I forget it so that I can recover my personal account.[#37](https://github.com/Harmonica-Men/AstroShop/issues/37)
- As a shopper, I can search for a product by name or description so that I can find a specific product I’d like to purchase.[#15](https://github.com/Harmonica-Men/AstroShop/issues/15)
- As a shopper, I can easily see what I’ve searched for and the number of results so that I can quickly decide whether the product I want is available.[#16](https://github.com/Harmonica-Men/AstroShop/issues/16)

#### EPIC 4
- As a shopper I can be able to view the total of my purchases at any time easily so that I void spending too much.[#6](https://github.com/Harmonica-Men/AstroShop/issues/6)

#### EPIC 5
- As a software developer, I want to write unit tests and integration tests for critical functionality, So that I can ensure the reliability and correctness of the application and catch issues early in the development cycle.[#38](https://github.com/Harmonica-Men/AstroShare-Blog/issues/38)
- As a software developer I want to set up continuous integration (CI) So that I can automate tests and streamline manual testing processes to improve software quality and reduce the time spent on manual checks. [#39](https://github.com/Harmonica-Men/AstroShare-Blog/issues/39)


[Table Of Contents](#table-of-contents)

## User Stories Table of Contents
1. [Welcome and Introduction](#welcome-and-introduction)
2. [Sign-Up Process](#sign-up-process)
3. [Navigation and Exploration](#navigation-and-exploration)
4. [Creating and Sharing Content](#creating-and-sharing-content)
5. [Interaction and Collaboration](#interaction-and-collaboration)
6. [Profile and Community Building](#profile-and-community-building)
7. [Ease of Use and Accessibility](#ease-of-use-and-accessibility)
8. [Continuous Engagement](#continuous-engagement)

### Welcome and Introduction
**As a user:**
- I want to see a visually appealing landing page with a space theme and a welcoming headline.
- I want to read a brief introduction about the shop and its features.
- I want to have prominent "Sign Up" and "Log In" buttons to easily join or access the shop.
- I want to actual status of the shopping cart items across the site. 

### Sign-Up Process  
**As a shopper:**  
- I want to click on "Sign Up" and fill out a simple form with my Username, Email, Password, and Confirm Password.  
- I want the option to sign up using my social media accounts (Twitter, Facebook, etc.).  
- I want to access my purchase history and order details after signing up.  
- I want to access my shopping cart at any give time to checkout.  

### Navigation and Exploration  
**As a shopper:**  
- I want an easy-to-navigate menu with options like **Home**, **Shop**, **Categories**, **My Cart**, **Orders**, **My Profile** and **Log Out**.  
- I want to browse a shop feed showcasing featured products, sales, specials, and recommendations based on my preferences.  
- I want each product listing to display the product image, name, price, a brief description, and action buttons like **Add to Cart** and **View Details**.  

### Shopping and Checkout  
**As a shopper:**  
- I want to search for products using a search bar with filters for price range, categories, ratings, and availability.  
- I want to view detailed product pages with multiple images and detailed descriptions.  
- I want to add products to my cart and adjust quantities directly in the cart.  
- I want a seamless checkout process with options to:  
  - Enter my shipping and billing details.  
  - Choose a payment method (credit card, PayPal, etc.).      
  - Review my order summary before confirming the purchase.  

### Interaction and Engagement  
**As a shopper:**  
- I want to share products with my friends through social media or email.  
- I want to receive notifications for price drops, new arrivals, order status updates, and exclusive deals.  

### Profile and Account Management  
**As a shopper:**  
- I want to manage my profile, including my shipping address, payment methods, and personal information.  
- I want to view my order history, including order details, status, and tracking information for shipped items.  
- I want to manage my subscriptions for newsletters, deals, and promotional updates.  

### Ease of Use and Accessibility  
**As a shopper:**  
- I want the webshop to be fully responsive, working seamlessly on desktop, tablet, and mobile devices.  
- I want fast loading times and smooth transitions between pages.  
- I want a high contrast mode and text resizing options for better accessibility if I am visually impaired.  
- I want a keyboard-navigable interface and screen reader compatibility.  
- I want an easily accessible help section with FAQs, return policy information, and a contact support option for direct assistance. (index)

### Continuous Engagement  
**As a shopper:**  
- I want personalized product recommendations based on my browsing and purchasing behavior.  
- I want regular email updates with exclusive offers, product highlights, and sales events.  
- I want to participate in seasonal sales, promotional contests, and loyalty programs to earn rewards.  
- I want to receive reminders about items left in my cart or wishlist.  

## The UX Table Of Contents
 
### 1. Welcome and Introduction
**User opens the Astro Shop:**

- **Landing Page:**
  - On the home page ther is a banner that include all links to the categories product pages.
  - On the home page there is no nav-bar but only "Shop Now" button to navigate to the Astro Shop.
  - The background image is of the physical store.
  - Subscribtion section for newsletter sign up.
  - The Footer contain all legal and fiscal information of the store whit the social media links.
  
- **Call to Action:**
  - "Shop Now" button leads you the astro-shop products page.  
  - Fill in the subscription and a confirmation mail will be sent.
  - Subscription is no registration to the "Astro Shop".

### 2. Product page 
- **User clicks on "Shop Now":**
  - All registered users can a purchase of anything on the shop.
  - All selected items are located in the shopping cart.
  - At any give time the shopping cart can be checked out to the payment methode 

- **Call to Action:**
  - All non-autheticad users can access the shop, but can not buy. (no guest mode)
  - All autheticad users can access the shop, they can make purchases.

[Table Of Contents](#table-of-contents)

### 3. Nav-bar 
- **User clicks access to Navigation Bar"**
  - The users can see any time the status of there shopping cart.
  - The users can access if logged in there creditials.
  - The users can easy search trougout the shop.
  - Categories lists feature to display products per category.
  - Content of the categories.
  - "Astro Shop" button on the left redirect always the home page.
  - "All Products" button give sorting out products by price and product category.
  - "Product Category" button give user the possiblity to select a certain product category.

- **Call to Action**
  - The users can easy login or logout.
  - The users can update and/or manipulate there profile.    
  - The users can search for certain key words to access and find products.
  - Display all products relevant to the category.
  - Show all categories and there content in Product Category.
  - Subpage of the shop is the product page of the Astro Shop.
  - Mainpage of the shop is the homepage of the Astro Shop.

### 4. Sign-Up Process
**User clicks on "Register":**

- **Sign-Up Form:**
  - On the product page there is on the right upper corner a "My Account" button that open pull down menu where you select "Register"
  - Simple form requesting essential information: Username, Email, Password, and Confirm Password.
  - The a redirect to fill User Information & Shipping Information (optional)

- **Account Setup:**
  - After signing up, there is the possibility to complete their profile "My Account" button:
    - Update 'My Profile' information
    - Update 'My Shipping' information
    - Update 'My Payment' information 

### 5. Product Details 
**User clicks on "Add Post":**

- **Add To Cart:**
  - View your chosen product in details
    - Select "Category" if needed to view all products of current category 
    - option to select quantity.
    - Add To Cart button to put the item(s) in to shopping cart.

[Table Of Contents](#table-of-contents)

### 6. The Shopping Cart 
**Customer verify the cart:**

- **Overview**
  - The customer has a overall prespective of his schopping cart.
  - The overall totals of each product item and the grand total.
  

- **Update The Cart**
  - If nessariy the items in the cart can be deleted form shopping cart.
  - The quantity of cart can be adjusted

### 7. Check Out
**The customer can check**

- **Order Summary:**
  - The user can see all there items in the schopping cart and if needed can be changed on "Update Cart" button. 
  - The overall totals of each product item and grand total.
  
- **Shipping Information**
  - Shipping address is not always the same as the customer address of resident therefor must be checked again.
  
  **Make The Order**
  - This is the fase where order is made official but that does not mean the deal is closed.
  - A email is sent to the customer to confirm that there was a transaction that verify the order.

### 8. Payment
**Client is redirected to PayPal**

- PayPal offers a variety of options for secure online transactions:

  - **PayPal Balance**: Pay directly using funds stored in your PayPal account.
  - **Linked Bank Account**: Payments are debited from your connected bank account.
  - **Credit/Debit Card**: Use cards linked to your PayPal account for secure payments.
  - **PayPal Credit**: A credit line for eligible users, allowing flexible payment terms.
  - **Pay in 4**: Split the purchase into four interest-free installments.
  - **Guest Checkout**: Make payments without creating a PayPal account using a card.
  - **PayPal Business Payments**: For merchants, supports invoicing, subscription payments, and POS systems.

  These methods ensure secure and flexible payment experiences.

### 9. Email Confirmation and Redirect to Merchant
**After a Successful PayPal Payment:**

1. **Payment Confirmation**:  
   PayPal sends a confirmation to both the buyer and the merchant, typically via email. This includes transaction details, such as the amount, payer's information, and a unique transaction ID.

2. **Merchant Notification**:  
   The merchant’s system receives an Instant Payment Notification (IPN) or Webhook, confirming the payment status.

3. **Order Processing**:  
   The merchant begins processing the order, such as shipping the purchased item or granting access to digital products.

4. **Transaction Logging**:  
   The payment is recorded in both PayPal and the merchant’s order management system for future reference.

5. **Email Confirmation**:     
   An email has been sent to confirm that the payment was received by PayPal and the transaction succeeded.

**After an Unsuccessful PayPal Payment:**

1. **Payment Denied Notification**:  
   PayPal informs the buyer of the failure, typically citing reasons such as insufficient funds, incorrect card details, or declined authorization.

2. **Merchant Notification**:  
   The merchant may also receive a failed payment notification or see a "payment failed" status in their system.

3. **Retry Option**:  
   The buyer is usually prompted to correct any issues (e.g., updating card information) and try the payment again.

4. **Order on Hold**:  
   The merchant's system may put the order on hold or cancel it until payment is successfully completed.

5. **No Funds Deduction**:  
   In the case of failure, no funds are deducted from the buyer’s PayPal account or linked payment method.

### 10. Review and follow up orders 
  - A "My Orders" page in a webshop typically serves as a centralized hub where users can view and manage their previous orders. 

[Table Of Contents](#table-of-contents)

