from flask import Blueprint, render_template, request, redirect, session
from models import db, User, Project, Bug, ActivityLog

project = Blueprint("project", __name__)



@project.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    role = session['user_role']
    user_id = session['user_id']

    # ==========================
    # Admin Dashboard
    # ==========================

    total_users = User.query.count()

    total_projects = Project.query.count()

    total_bugs = Bug.query.count()

    open_bugs = Bug.query.filter_by(
        status="Open"
    ).count()

    closed_bugs = Bug.query.filter_by(
        status="Closed"
    ).count()

    activities = ActivityLog.query.order_by(
        ActivityLog.id.desc()
    ).limit(5).all()

    # ==========================
    # Project Manager Dashboard
    # ==========================

    active_projects = Project.query.filter_by(
        status="Active"
    ).count()

    assigned_bugs = Bug.query.filter(
        Bug.assigned_to != None
    ).count()

    pending_bugs = Bug.query.filter_by(
        status="Pending"
    ).count()

    # ==========================
    # Developer Dashboard
    # ==========================

    my_bug_list = Bug.query.filter_by(
        assigned_to=user_id
    ).all()

    my_bugs = len(my_bug_list)

    in_progress = Bug.query.filter_by(
        assigned_to=user_id,
        status="In Progress"
    ).count()

    resolved = Bug.query.filter_by(
        assigned_to=user_id,
        status="Resolved"
    ).count()

    performance = 0

    if my_bugs > 0:
        performance = round((resolved / my_bugs) * 100)

    # ==========================
    # Tester Dashboard (Temporary)
    # ==========================

    # ==========================
    # Tester Dashboard
    # ==========================

    bugs_reported = Bug.query.filter_by(
    created_by=user_id
).count()

    verified_bugs = Bug.query.filter_by(
    created_by=user_id,
    status="Verified"
).count()

    reopened_bugs = Bug.query.filter_by(
    created_by=user_id,
    status="Reopened"
).count()

    return render_template(

        "dashboard.html",

        role=role,
        user_name=session["user_name"],

        # Admin
        total_users=total_users,
        total_projects=total_projects,
        total_bugs=total_bugs,
        open_bugs=open_bugs,
        closed_bugs=closed_bugs,
        activities=activities,

        # Project Manager
        active_projects=active_projects,
        assigned_bugs=assigned_bugs,
        pending_bugs=pending_bugs,

        # Developer
        my_bugs=my_bugs,
        my_bug_list=my_bug_list,
        in_progress=in_progress,
        resolved=resolved,
        performance=performance,

        # Tester
        bugs_reported=bugs_reported,
        verified_bugs=verified_bugs,
        reopened_bugs=reopened_bugs

    )

# ==========================
# Create Project
# ==========================

@project.route("/create_project", methods=["GET", "POST"])
def create_project():

    if "user_id" not in session:
        return redirect("/login")

    if session['user_role'] not in ["Admin", "Project Manager"]:
        return "Access Denied"

    if request.method == "POST":

        project_data = Project(
            project_name=request.form["project_name"],
            description=request.form["description"],
            status=request.form["status"]
        )

        db.session.add(project_data)
        db.session.commit()

        return redirect("/projects")

    return render_template("create_project.html")


# ==========================
# View Projects
# ==========================

@project.route("/projects")
def projects():

    if "user_id" not in session:
        return redirect("/login")

    all_projects = Project.query.all()

    return render_template(
        "projects.html",
        projects=all_projects
    )