# CS50W CAPSTONE PROJECT


This project was created for completing CS50W HarvardX course. It is a delivery website, that allows customers to order any food of their choice from a restaurant that creates an account on this website, and adds its menu on it. This website covers the customer and the restaurant sides: On one side the customer can add an item to the cart, order it, and also add  restaurants to "favorite"; on the other side, the restaurant can add an item on its menu, remove it and accept or decline orders.

* My project satisfies all the requirements mentioned, it is distinct from all the other projects I did for this course, and even though the old CS50W Pizza project is also a delivery app, this current one is completely different because unlike the latter, any restaurant can easily sign up, and add items to its menu, and allows anyone to order from it. It is also fully mobile-responsive.  
### What is contained in my files
---
* Inside the delivery app folder, there are several python files: 
    + <code>views.py</code> where all the views function are available.
    + <code>models.py</code> where we can see all four models created for this project: User, Restaurant, Food and Order.
    + <code>urls.py</code> where we can see all urls of this project.
* The  <code>templates/delivery</code> includes all the HTML files, and all of them extend from <code>layout.html</code>.
* The <code>static/delivery</code> include two files: 
    + <code>styles.css</code> which is the CSS of all the HTML files that I used, used in addition to the bootstrap implementation on my HTML files.
    + <code>script.js</code> is the javascript files that is required for some HTML files.

I decided to use one <code>.css</code> file and one <code>.js</code> file for the whole project, because they ended up not having many lines. This is why in <code>styles.css</code>, there are some classes that are  designed and not available on some HTML templates, and in <code>script.js</code>, several <code>try/catch</code> where the <code>catch</code> is empty, it is just not to get errors when the <code>querySelector</code> item is not available on a certain page that still uses this javascript code.

### How to run my application
Download the code, with the terminal <code>cd</code> into it, and type <code>python3 <span>manage.py</span> runserver</code> and you should be good.
