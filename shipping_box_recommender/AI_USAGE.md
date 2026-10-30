# AI_USAGE.md

## 1. AI Tools Used

- **ChatGPT (OpenAI):** Used for Django development guidance, understanding errors, debugging, and improving HTML templates and Python code.

## 2. Prompts Given

I used the following prompts during project development:

1. Help me develop an Ecommerce Shipping Box Recommendation System using Django.
2. My customer login page redirects to the warehouse dashboard. How can I fix it?
3. Help me understand Django login redirects and authentication decorators.
4. Help me improve the warehouse dashboard and shipping box recommendation pages.

## 3. Outputs Accepted

I reviewed the AI-generated suggestions and incorporated the parts that were suitable for my project requirements, including:

- Separate authentication logic for customers and packaging staff.
- Redirecting customers to the product list after successful login.
- Redirecting packaging staff to the warehouse dashboard after successful login.
- HTML login forms containing username and password fields.

## 4. Outputs Rejected or Modified

I modified some AI-generated suggestions to match my project requirements:

- Modified the HTML templates and CSS to match the required page design.
- Adjusted redirect destinations to keep customer and packaging staff workflows separate.

## 5. Mistakes Found in AI Assistance

During development, I identified and corrected the following issues in the suggested code:

- The initial customer login URL used Django's `LoginView`. This did not provide the intended custom customer login behavior and could redirect users to a `next` URL instead of the product page.
- An earlier staff account creation configuration redirected users to the staff login page instead of the staff creation page.
- AI-generated code needed to be checked against the existing project structure and requirements before using it.

## 6. How I Verified the Final Code

I used the following checks to verify the application:

### Django Configuration Checks

- Ran `python manage.py check` to check for Django configuration errors.
- Ran `python manage.py makemigrations` to prepare database migrations when model changes were made.
- Ran `python manage.py migrate` to apply database migrations.
- Ran `python manage.py runserver` to start the development server.

### Functional Testing

I checked the following application features:

1. Homepage displays customer and packaging staff options.
2. Customer registration creates a customer account.
3. Customer login accepts valid customer credentials.
4. Successful customer login redirects to the product list.
5. Packaging staff can log in using their separate login page.
6. Successful staff login redirects to the warehouse dashboard.
7. Customers can purchase products and complete orders.
8. Completed customer orders appear on the warehouse dashboard. 
9. Packaging staff can calculate suitable shipping boxes for completed orders.

## 7. Conclusion

ChatGPT was used as an assistance tool during development. I reviewed the suggested code, modified it according to my project requirements, and used Django commands and application testing to check the implementation. I am responsible for the final code submitted in this project.