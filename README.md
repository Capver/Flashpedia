# Flashpedia
#### Video Demo:  https://youtu.be/yNDL3Ts6V1w
#### Description:
My final project for CS50x is a web application for making flashcards that I called "Flashpedia". Sometimes I find that the current free web applications for making flashcards are not completely focused on studying. When this happens, the user is forced to start being creative with the way they name their files or their deck. This web application removes these unnecessary tasks since this web application is purely for studying and it bases its flashcards in the "course" and "lecture" that the user wants to study upon making their flashcards.

# Programming languages
For this application, I decided to use Python (because it is the programming language I am the most interested in), Flask and Jinja2 (since they go well with Python and also, I learnt well their basics when doing the last problem of CS50x), SQLite3, some Javascript, and, evidently, HTML and CSS. I also used the help of Copilot and bootstrap.

# Files in use
The functionality of my web application involves the database flashcards.db, the Python file app.py, and 6 html templates.

My database contains 1 table called "flashcards". This table contains the following columns: user, front, back, course, and lecture. These columns are used to store the user that creates a flashcard, along with the information of said flashcard.

My Python file has all the functions needed to make my Flask web application work with HTML. It also declares all the necessary imports and makes a connection with the flashcards.db database.

# "Make" function
The first function is “make”, which is the "/" route and is associated with the file make.html. The purpose of this route is that the user makes their flashcard by inputting the course, lecture, the front of the flashcard (the question or sentence), and the back (the answer). The reason why this is the "/" route and not the "/make" route is that I wanted this to be the landing page and also the default one, since I wanted the user to be able to open the web application and be able to start making flashcards right away (which would be really useful if they were listening to a lecture). This function gets the cookies of the user, which will be used for the rest of the web application whenever an SQL query requires a user. The decision of using cookies instead of login/logout sessions was based on that I wanted to learn how much I can do with cookies and also that I wanted the user to be able to try the webpage without having to make an account (this may change for a commercial web application though).

# "View" function
The second function is “view”, which is the "/view" route and associated with the file view.html. This one is used to view the user's flashcards by filtering them with the courses and lectures provided in the route for making flashcards. The filter options are chosen based on the courses and lectures that the user has flashcards with. This is done by using an SQLite query on app.py that selects for all courses or all lectures that the user may have in their flashcards. Using Jinja2, this information is passed to the template. The user can also delete or modify their flashcards from this route. These actions need a separate function each, and the "modify" function has, in fact, its own template: modify.html. The view template also uses JavaScript to show a green alert underneath the header, saying that the flashcards were modified or deleted successfully. Finally, this template has an alert that appears in the place of the flashcards when there are none available – that is, when either no flashcards have been created or when the filters gave no flashcards.

# "Study" function
The next function is study, which is the "/study" route and associated with the file study.html. Its purpose is to allow the user to pick a course (or course and lecture) they want to study, and they will be able to study by seeing the requested flashcards in random order. This one uses a helper function called "get_flashcards", which retrieves the requested flashcards and make sure they are not repeated in the same study session (i.e, when the user presses "Start Studying", they should not be able to see a flashcard they have already seen after starting). Once the user has gone through all flashcards, they will see an alert and be redirected to the "/study" route. The way this template allows the user to choose their courses and lectures is like that of the view route. Finally, this template uses JavaScript to properly show the flashcards, allowing the user to reveal the back of the flashcards and move on to the next one.

# Conclusion
In conclusion, _Flashpedia_ is a specialized web application designed to streamline the flashcard creation and studying process. It uses several programming languages to provide an user-friendly interface, while also being simple. As always, there is room for improvement in web design. However, this web app has the necessary components to meet its functional goals and become a valuable study tool.
