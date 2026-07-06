from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# =========================
# USER
# =========================

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    
reported_bugs = db.relationship(
    "Bug",
    foreign_keys="Bug.created_by",
    backref="reporter",
    lazy=True
)


# =========================
# PROJECT
# =========================

class Project(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(50))



# =========================
# BUG
# =========================

class Bug(db.Model):
    __tablename__ = "bug"

    id = db.Column(db.Integer, primary_key=True)

    bug_title = db.Column(db.String(200), nullable=False)

    description = db.Column(db.Text)

    priority = db.Column(db.String(20))

    # Predicted Severity by ML
    severity = db.Column(db.String(20))

    # Predicted Resolution Time by ML
    predicted_resolution = db.Column(db.String(50))

    status = db.Column(db.String(20))

    # Assigned Developer
    assigned_to = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    # Tester who reported the bug
    created_by = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )

    created_date = db.Column(db.Date)

    # Relationship to Developer
    developer = db.relationship(
        "User",
        foreign_keys=[assigned_to]
    )

    # Relationship to Tester
    reporter = db.relationship(
        "User",
        foreign_keys=[created_by]
    )

# =========================
# BUG HISTORY
# =========================

class BugHistory(db.Model):
    __tablename__ = "bug_history"

    id = db.Column(db.Integer, primary_key=True)

    bug_id = db.Column(db.Integer)

    old_status = db.Column(db.String(20))
    new_status = db.Column(db.String(20))

    updated_by = db.Column(db.String(100))
    updated_date = db.Column(db.Date)


# =========================
# PREDICTION
# =========================

class Prediction(db.Model):
    __tablename__ = "prediction"

    id = db.Column(db.Integer, primary_key=True)

    bug_id = db.Column(db.Integer)

    predicted_severity = db.Column(db.String(20))
    predicted_resolution_days = db.Column(db.Integer)

    model_accuracy = db.Column(db.Float)


# =========================
# COMMENT
# =========================

class Comment(db.Model):
    __tablename__ = "comment"

    id = db.Column(db.Integer, primary_key=True)

    bug_id = db.Column(db.Integer)

    user_name = db.Column(db.String(100))

    comment = db.Column(db.Text)

    comment_date = db.Column(db.Date)


# =========================
# ATTACHMENT
# =========================

class Attachment(db.Model):
    __tablename__ = "attachment"

    id = db.Column(db.Integer, primary_key=True)

    bug_id = db.Column(db.Integer)

    file_name = db.Column(db.String(255))
    file_path = db.Column(db.String(255))

    upload_date = db.Column(db.Date)


# =========================
# PROJECT MEMBER
# =========================

class ProjectMember(db.Model):
    __tablename__ = "project_member"

    id = db.Column(db.Integer, primary_key=True)

    project_id = db.Column(db.Integer)

    user_id = db.Column(db.Integer)


# =========================
# NOTIFICATION
# =========================

class Notification(db.Model):
    __tablename__ = "notification"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    message = db.Column(db.Text)

    status = db.Column(db.String(20))

    created_date = db.Column(db.Date)


# =========================
# ACTIVITY LOG
# =========================

class ActivityLog(db.Model):
    __tablename__ = "activity_log"

    id = db.Column(db.Integer, primary_key=True)

    user_name = db.Column(db.String(100))

    activity = db.Column(db.Text)

    activity_date = db.Column(db.Date)


# =========================
# ML DATASET
# =========================

class MLDataset(db.Model):
    __tablename__ = "ml_dataset"

    id = db.Column(db.Integer, primary_key=True)

    bug_id = db.Column(db.Integer)

    actual_severity = db.Column(db.String(20))

    actual_resolution_days = db.Column(db.Integer)


# =========================
# MODEL PERFORMANCE
# =========================

class ModelPerformance(db.Model):
    __tablename__ = "model_performance"

    id = db.Column(db.Integer, primary_key=True)

    model_name = db.Column(db.String(100))

    accuracy = db.Column(db.Float)
    precision = db.Column(db.Float)
    recall = db.Column(db.Float)
    f1_score = db.Column(db.Float)


# =========================
# DEVELOPER PERFORMANCE
# =========================

class DeveloperPerformance(db.Model):
    __tablename__ = "developer_performance"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    bugs_assigned = db.Column(db.Integer)
    bugs_resolved = db.Column(db.Integer)

    average_resolution_days = db.Column(db.Float)