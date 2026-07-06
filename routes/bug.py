from flask import Blueprint, render_template, request, redirect, session
from models import db, User, Bug, BugHistory

import joblib

# ==========================
# Load ML Models
# ==========================

severity_model = joblib.load("ml/severity_model.pkl")

severity_vectorizer = joblib.load("ml/tfidf.pkl")

resolution_model = joblib.load("ml/resolution_classifier.pkl")

resolution_vectorizer = joblib.load("ml/resolution_tfidf.pkl")

bug = Blueprint("bug", __name__)


# ==========================
# Predict Bug
# ==========================

def predict_bug(description):

    severity_input = severity_vectorizer.transform(
        [description]
    )

    predicted_severity = severity_model.predict(
        severity_input
    )[0]

    resolution_input = resolution_vectorizer.transform(
        [description]
    )

    predicted_resolution = resolution_model.predict(
        resolution_input
    )[0]

    return predicted_severity, predicted_resolution


# ==========================
# Create Bug
# ==========================

@bug.route("/create_bug", methods=["GET", "POST"])
def create_bug():

    if "user_id" not in session:
        return redirect("/login")
    
    if session["user_role"] not in ["Admin", "Project Manager", "Tester"]:
        return "Access Denied"

    if request.method == "POST":
        
    # ==========================
    # Machine Learning Prediction
        description = request.form["description"]
        predicted_severity, predicted_resolution = predict_bug(description)
    # ==========================

        new_bug = Bug(
            bug_title=request.form["bug_title"],
            description=description,
            priority=request.form["priority"],
            severity=predicted_severity,
            predicted_resolution=predicted_resolution,
            status=request.form["status"],
            assigned_to=int(request.form['assigned_to']),
            created_by=session["user_id"],
        )

        db.session.add(new_bug)
        db.session.commit()

        return redirect("/bugs")

    developers = User.query.filter_by(role="Developer").all()

    return render_template(
        "create_bug.html",
        developers=developers
    )


# ==========================
# View Bugs
# ==========================

@bug.route("/bugs")
def bugs():

    if "user_id" not in session:
        return redirect("/login")

    all_bugs = Bug.query.all()

    return render_template(
        "bugs.html",
        bugs=all_bugs
    )


@bug.route("/update_bug/<int:id>", methods=["GET", "POST"])
def update_bug(id):

    if "user_id" not in session:
        return redirect("/login")

    selected_bug = Bug.query.get_or_404(id)

    print("Bug Assigned To :", selected_bug.assigned_to)
    print("Logged User ID  :", session["user_id"])

    # Developer can update only their assigned bugs
    if session["user_role"] == "Developer":

        if int(selected_bug.assigned_to) != int(session["user_id"]):
            return "Access Denied"

    # ----------------------------
    # Update Status
    # ----------------------------
    if request.method == "POST":

        old_status = selected_bug.status
        selected_bug.status = request.form["status"]

        history = BugHistory(
            bug_id=selected_bug.id,
            old_status=old_status,
            new_status=selected_bug.status,
            updated_by=session["user_name"]
        )

        db.session.add(history)
        db.session.commit()

        print("Bug Updated Successfully")

        if session["user_role"] == "Developer":
            return redirect("/dashboard")

        return redirect("/bugs")

    # ----------------------------
    # Show Update Page
    # ----------------------------
    return render_template(
        "update_bug.html",
        bug=selected_bug
    )
# ==========================
# Bug History
# ==========================

@bug.route("/bug_history")
def bug_history():

    if "user_id" not in session:
        return redirect("/login")

    history = BugHistory.query.all()

    return render_template(
        "bug_history.html",
        history=history
    )
    
# ==========================
# My Reported Bugs
# ==========================

@bug.route("/reported_bugs")
def reported_bugs():

    if "user_id" not in session:
        return redirect("/login")

    if session["user_role"] != "Tester":
        return "Access Denied"

    my_reports = Bug.query.filter_by(
        created_by=session["user_id"]
    ).all()

    return render_template(
        "reported_bugs.html",
        bugs=my_reports
    )


# ==========================
# Verify Bug
# ==========================

@bug.route("/verify_bug/<int:id>")
def verify_bug(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["user_role"] != "Tester":
        return "Access Denied"

    bug = Bug.query.get_or_404(id)

    # Tester can verify only his own bugs
    if bug.created_by != session["user_id"]:
        return "Access Denied"

    if bug.status != "Resolved":
        return "Only Resolved bugs can be verified."

    old_status = bug.status
    bug.status = "Verified"

    history = BugHistory(
        bug_id=bug.id,
        old_status=old_status,
        new_status="Verified",
        updated_by=session["user_name"]
    )

    db.session.add(history)
    db.session.commit()

    return redirect("/reported_bugs")


# ==========================
# Reopen Bug
# ==========================

@bug.route("/reopen_bug/<int:id>")
def reopen_bug(id):

    if "user_id" not in session:
        return redirect("/login")

    if session["user_role"] != "Tester":
        return "Access Denied"

    bug = Bug.query.get_or_404(id)

    # Tester can reopen only his own bugs
    if bug.created_by != session["user_id"]:
        return "Access Denied"

    if bug.status not in ["Verified", "Closed"]:
        return "Only Verified or Closed bugs can be reopened."

    old_status = bug.status
    bug.status = "Reopened"

    history = BugHistory(
        bug_id=bug.id,
        old_status=old_status,
        new_status="Reopened",
        updated_by=session["user_name"]
    )

    db.session.add(history)
    db.session.commit()

    return redirect("/reported_bugs")