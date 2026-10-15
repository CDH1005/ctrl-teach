# Ctrl + Teach 🎓

An online tutoring platform that connects students with expert tutors across various subjects, including core academics, advanced technical fields, and foreign languages.

## 🌟 Current Features

### User Roles & Authentication
*   **Three Tier System:** Dedicated accounts for Students, Tutors, and Admins.
*   **Secure Access:** Password hashing and session management using Flask-Login.
*   **Personalized Dashboards:** Unique dashboard views based on the user's role.

### For Students
*   **Browse & Filter:** Explore a dynamic catalog of available courses and verified tutors.
*   **Booking System:** Select dates and times for 1-on-1 tutoring sessions.
*   **Payment Simulation:** Integrated dummy GCash payment gateway for secure transaction simulation.
*   **Session Tracking:** View upcoming and past booked sessions directly from the dashboard.

### For Tutors
*   **Course Creation:** Easily publish new course offerings with custom descriptions and hourly rates.
*   **Subject Categorization:** Tag courses with specific subjects (e.g., Japanese, Calculus, Verilog Digital Logic).
*   **Active Roster:** Keep track of active course listings and manage offerings.

### For Administrators
*   **Platform Oversight:** Admin control panel to monitor all registered users and platform-wide bookings.

### UI / UX
*   **Modern Design:** Fully responsive frontend built with Bootstrap 5.
*   **Dynamic Animations:** CSS hover effects, fade-ins, and smooth transitions.
*   **Social Proof:** Integrated testimonial carousel and verified tutor badges.

## 🛠️ Tech Stack
*   **Backend:** Python, Flask
*   **Database:** SQLite, Flask-SQLAlchemy
*   **Frontend:** HTML5, CSS3, Bootstrap 5, Jinja2 Templates
*   **Deployment:** Railway (via GitHub)

## 🚀 How to Run Locally

1. Clone the repository:
   `git clone <your-repo-link>`
   `cd ctrl-teach`
2. Create and activate a virtual environment:
   `python -m venv venv`
   `venv\Scripts\activate`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Run the application:
   `python main_application_file.py`
5. Open `http://127.0.0.1:5000` in your web browser.