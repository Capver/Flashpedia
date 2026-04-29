# Flashpedia

> **Note on Development:** This project was developed entirely from scratch without the use of AI coding assistants (LLMs). It serves as a foundational demonstration of my understanding of core programming syntax, relational databases, state management, and web architecture.

#### Video Demo: [Watch on YouTube](https://youtu.be/yNDL3Ts6V1w)

## Architectural Overview
_Flashpedia_ is a specialized CRUD (Create, Read, Update, Delete) web application engineered for structured active recall. While many existing flashcard applications force users to adopt complex folder structures or naming conventions, Flashpedia eliminates friction by organizing data strictly around **Course** and **Lecture** parameters. This creates a streamlined, highly targeted studying environment.

The application is built on a lightweight architecture utilizing **Python (Flask)** for backend routing, **SQLite3** for relational data storage, and **Jinja2** with **Bootstrap** for dynamic frontend rendering.

## Technical Stack
* **Backend:** Python, Flask
* **Database:** SQLite3
* **Frontend:** HTML5, CSS3, JavaScript (DOM manipulation), Bootstrap 4, Jinja2
* **Concepts:** CRUD Operations, Session/Cookie Management, Relational Database Filtering

## Core System Components

### 1. Data Ingestion Pipeline (`/`)
The landing page serves as the primary data entry point, allowing users to immediately begin inputting flashcard data (Course, Lecture, Front, Back) without friction. 
* **State Management:** Instead of forcing account creation, the system generates and assigns a unique tracking cookie (lasting up to 2 years) upon the user's first visit. This handles user session tracking for all subsequent SQL queries while lowering the barrier to entry.

### 2. Data Retrieval & Filtering (`/view`)
This route handles the dynamic querying of user-specific data. 
* **Logic:** It queries the SQLite database to extract distinct courses and lectures associated with the user's cookie, populating frontend filter dropdowns. 
* **Data Mutation:** Users can isolate specific lecture sets and perform Update (`/modify`) or Delete (`/delete`) operations, supported by asynchronous JavaScript alerts for UI feedback.

### 3. Active Recall Engine (`/study`)
The core utility of the application. Users select a specific course/lecture node to study.
* **Querying:** A helper function (`get_flashcards`) retrieves the requested subset of data from the database, randomizes the order via SQL (`ORDER BY RANDOM()`), and ensures no duplicates are shown in a single session.
* **Frontend Interaction:** JavaScript is utilized to manage the UI state, allowing users to toggle between the **Front** (Question) and **Back** (Answer) of the cards seamlessly without requiring page reloads.

## How to Run Locally

To run this project on your local machine, follow these steps:

1. **Clone the repository:**
```git clone [https://github.com/Capver/Flashpedia.git](https://github.com/Capver/Flashpedia.git)
cd Flashpedia```
2. **Set up a virtual environment:**
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate
3. **Install dependencies**
pip install Flask
4. **Run the application**
flask run
5. **Access the web app:**
Open your browser and navigate to http://127.0.0.1:5000/

Developed as the final project for Harvard's CS50x.
