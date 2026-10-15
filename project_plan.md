# Ctrl + Teach - Project Blueprint (Updated)

## 📌 Phase 1: Foundation (COMPLETED)
- [x] Set up Python virtual environment
- [x] Configure Flask application (`main_application_file.py`)
- [x] Create `.gitignore` and `requirements.txt`

## 📌 Phase 2: Database & Models (COMPLETED)
- [x] Integrate Flask-SQLAlchemy
- [x] Create SQLite database (`app.db`)
- [x] Define Models: `User`, `Subject`, `Course`, `Booking`, `Testimonial`
- [x] Seed database with standard and Foreign Language subjects

## 📌 Phase 3: User Authentication (COMPLETED)
- [x] Implement Flask-Login
- [x] Secure password hashing (Werkzeug)
- [x] Build Registration and Login routes/forms
- [x] Role-based routing (Student vs. Tutor vs. Admin)

## 📌 Phase 4: Core Features (COMPLETED)
- [x] **Tutor Core:** Create courses linked to specific subjects.
- [x] **Student Core:** Browse active courses on the Explore page.
- [x] **Booking System:** Students can schedule sessions with specific tutors.
- [x] **Payment System:** Dummy GCash checkout flow to simulate payment confirmation.
- [x] **Admin Core:** Admin dashboard to view all users and platform activity.

## 📌 Phase 5: UI/UX Overhaul (COMPLETED)
- [x] Implement split-screen designs for Auth pages.
- [x] Add CSS fade-in and hover animations.
- [x] Design dynamic Dashboard UI depending on user role.
- [x] Add competitor features (Verified badges, Trial lesson highlights, Video intro placeholders).
- [x] Refine navigation logic (Smart "Back" buttons based on auth state).

## 📌 Phase 6: Deployment & CD (COMPLETED)
- [x] Create `Procfile` for Gunicorn.
- [x] Push source code to GitHub repository.
- [x] Connect GitHub repository to Railway for Continuous Deployment.

## 🚀 Future Roadmap (Post-Deployment Ideas)
1. **Real Payment Gateway:** Swap the dummy GCash page with Stripe, PayPal, or PayMongo APIs.
2. **Email Notifications:** Send actual email receipts when a booking is confirmed using Flask-Mail.
3. **Video Integration:** Add a field for Tutors to paste their Zoom/Meet links so they appear on the Student's dashboard after booking.
4. **User Profiles:** Allow users to upload profile pictures and write biographies.