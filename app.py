from flask import Flask, request, render_template, redirect, url_for, make_response
import sqlite3
import random

app = Flask(__name__)
app.secret_key = "secret"

# Helper function for database connection


def get_db_connection():
    conn = sqlite3.connect("flashcards.db")
    return conn


@app.route("/", methods=["GET", "POST"])
def make():
    if request.method == "GET":
        # Getting the cookies of the user
        user = request.cookies.get("user")

        # If there are no cookies, make them and store them for a long time (2 years)
        if not user:
            user = "user" + str(random.randint(1000, 9999))
            response = make_response(render_template("make.html", user=user))
            response.set_cookie("user", user, max_age=60*60*24*365*2)
            return response

        # Retrieving the courses and lectures for the datalist on make.html
        else:
            with get_db_connection() as conn:
                db = conn.cursor()
                db.execute("SELECT DISTINCT course FROM flashcards WHERE user = ?", (user,))
                # Unpacking each tuple so the datalist works
                courses = [course[0] for course in db.fetchall()]
                db.execute("SELECT DISTINCT lecture FROM flashcards WHERE user = ?", (user,))
                # Unpacking each tuple so the datalist works
                lectures = [lecture[0] for lecture in db.fetchall()]
                return render_template("make.html", courses=courses, lectures=lectures)

    elif request.method == "POST":

        # Storing the flashcard information in the database
        user = request.cookies.get("user")
        course = request.form.get("course")
        lecture = request.form.get("lecture")
        front = request.form.get("front")
        back = request.form.get("back")
        with get_db_connection() as conn:
            db = conn.cursor()
            db.execute("INSERT INTO flashcards (user, course, lecture, front, back) VALUES (?, ?, ?, ?, ?)",
                       (user, course, lecture, front, back))
            conn.commit()
        return redirect("/")


@app.route("/view")
def view():
    if request.method == "GET":
        # Getting the cookies of the user
        user = request.cookies.get("user")
        # Getting the course and lecture values form the form
        course = request.args.get("course")
        lecture = request.args.get("lecture")
        # If the cookie exists, get the flashcards, courses, and lectures for that user
        if user:
            with get_db_connection() as conn:
                db = conn.cursor()
                # Gettig the courses and lectures from the database to use as options for filtering
                db.execute("SELECT DISTINCT course FROM flashcards WHERE user = ?", (user,))
                courses = db.fetchall()
                db.execute("SELECT DISTINCT lecture FROM flashcards WHERE user = ?", (user,))
                lectures = db.fetchall()
            # If the course and lecture are specified, filter the flashcards by them
            if course and lecture:
                db.execute(
                    "SELECT * FROM flashcards WHERE user = ? AND course = ? AND lecture = ?", (user, course, lecture))
            # If only the course is specified, filter the flashcards by it
            elif course:
                db.execute("SELECT * FROM flashcards WHERE user = ? AND course = ?", (user, course))
            # If none were specified, get all the flashcards for that user (default)
            else:
                db.execute("SELECT * FROM flashcards WHERE user = ?", (user,))
            # Get the flashcards from the database
            flashcards = db.fetchall()
            # Render the view template with the flashcards, courses, lectures and, if applicable, message
            message = request.args.get("message")
            message_type = request.args.get("message_type")
            return render_template("view.html", flashcards=flashcards, courses=courses, lectures=lectures, message=message, message_type=message_type)
    else:
        # If there are no cookies, redirect to make.html
        return redirect("/")


@app.route("/delete/<int:flashcard_id>")
def delete(flashcard_id):
    # Delete the flashcard data from the database
    # Thanks to Copilot for the insightful help with the logic of the "delete" and "modify" functions
    with get_db_connection() as conn:
        db = conn.cursor()
        db.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_id,))
        conn.commit()

    # Redirecting to view.html after the flashcard is deleted
    return redirect(url_for('view', message="Flashcard deleted successfully!", message_type="success"))


@app.route("/modify/<int:flashcard_id>", methods=["GET", "POST"])
def modify(flashcard_id):

    if request.method == "GET":
        # Getting the flashcard data from the database
        with get_db_connection() as conn:
            db = conn.cursor()
            db.execute("SELECT * FROM flashcards WHERE id = ?", (flashcard_id,))
            flashcard = db.fetchone()
        # Rendering modify.html with the flashcard data
        return render_template("modify.html", flashcard=flashcard)

    elif request.method == "POST":
        # Getting the updated values from the form
        course = request.form.get("course")
        lecture = request.form.get("lecture")
        front = request.form.get("front")
        back = request.form.get("back")

        # Updating the flashcard in the database
        with get_db_connection() as conn:
            db = conn.cursor()
            db.execute("UPDATE flashcards SET course = ?, lecture = ?, front = ?, back = ? WHERE id = ?",
                       (course, lecture, front, back, flashcard_id))
            conn.commit()

        # Redirecting to view.html after the flashcard is modified
    return redirect(url_for('view', message="Flashcard updated successfully!", message_type="success"))


@app.route("/study", methods=["GET", "POST"])
def study():
    # Getting the cookies of the user
    user = request.cookies.get("user")
    # If there are no cookies, redirect to make.html
    if not user:
        return redirect("/")

    if request.method == "POST":
        # Getting the flashcards from the selected course and lecture
        course = request.form.get("course")
        lecture = request.form.get("lecture")
        flashcards = get_flashcards(user, course, lecture)
        if flashcards:
            # Sending the list of flashcards
            return render_template("study.html", flashcards=flashcards, course=course, lecture=lecture)
        else:
            # If no flashcards found, redirect to study.html
            return redirect("/study")

    elif request.method == "GET":
        # Display the form to choose course and lecture
        with get_db_connection() as conn:
            db = conn.cursor()
            db.execute("SELECT DISTINCT course FROM flashcards WHERE user = ?", (user,))
            courses = db.fetchall()
            db.execute("SELECT DISTINCT lecture FROM flashcards WHERE user = ?", (user,))
            lectures = db.fetchall()
        return render_template("study.html", courses=courses, lectures=lectures)


def get_flashcards(user, course, lecture):
    # Helper function for getting a random flashcard for the selected course and, if applicable, lecture (Thanks to Copilot for helping with the logic)
    with get_db_connection() as conn:
        db = conn.cursor()
        # Checking if there is a lecture on the form and if that lecture option is not "All" (which should not be an option)
        if lecture and lecture != 'All':
            db.execute(
                "SELECT front, back FROM flashcards WHERE user = ? AND course = ? AND lecture = ? ORDER BY RANDOM()", (user, course, lecture))
        # Checking if there is a course on the form and if that course is not "All"
        elif course and course != 'All':
            db.execute(
                "SELECT front, back FROM flashcards WHERE user = ? AND course = ? ORDER BY RANDOM()", (user, course))
        # Checking if the user is retreiving all flashcards for a lecture
        else:
            db.execute("SELECT front, back FROM flashcards WHERE user = ? ORDER BY RANDOM()", (user,))
        # Storing the selected flashcards as a list
        flashcards = [{'front': row[0], 'back': row[1]} for row in db.fetchall()]
    return flashcards
