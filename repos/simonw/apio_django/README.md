#Project Description 

[*Currently only Django Framework supported*]

Apio helps in monitoring of Applications. You can easily integrate(see setup below) it with your application and instantly start tracking errors and performance metrics.


##Setup

Installation instructions: https://www.youtube.com/watch?v=tpx4mTuv0-0

1. Create an account on [Apio signup](https://apio.in/signup)

2. Register an application on [Apio onboarding](https://apio.in/onboarding)

3. Install Apio-django using pip

`pip install apio-django`

4. Add `apio-django` to your installed Apps in your `settings.py`.

5. Add `apio_django.middleware.ApioMiddleware` to list of Middleware

6. Add `application_key` received after you onboarded your application on step 2 in your `settings.py`

`APIO_D = { "application_key": generated_application_key }`

7. Thats it :) Now on any error you will receive an email on the registered email id and also you can see all the details of your application on the dashboard of [Apio](https://apio.in) 


##Disclaimer
The Apio service is currently in beta testing phase. We don't take any responsbility of continued service or issues that may arise. 

##Contact (any queries)

Email: apio.monitor@gmail.com