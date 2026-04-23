from flask import Flask, render_template, request, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import matplotlib.pyplot as plt
from problems import daily_plan, daily_questions

app = Flask(__name__)
app.secret_key = "supersecretkey"

# DATABASE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# LOGIN
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# ================= MODELS =================

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class Progress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    day = db.Column(db.Integer)
    topic = db.Column(db.String(200))
    problems_done = db.Column(db.Integer)
    accuracy = db.Column(db.Integer)
    weak_area = db.Column(db.String(200))
    status = db.Column(db.String(50))


# CREATE DB
with app.app_context():
    db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ================= AUTH =================

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user_exists = User.query.filter_by(username=username).first()
        if user_exists:
            flash("User already exists!")
            return redirect("/register")

        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created! Please login.")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid username or password!")
            return redirect("/login")

        login_user(user)
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


# ================= MAIN =================

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    user_data = Progress.query.filter_by(user_id=current_user.id).all()

    if request.method == "POST":
        problems_done = int(request.form["problems"])
        accuracy = int(request.form["accuracy"])

        entry = Progress(
            user_id=current_user.id,
            day=int(request.form["day"]),
            topic=request.form["topic"],
            problems_done=problems_done,
            accuracy=accuracy,
            weak_area=request.form["weak"],
            status="⚠️ Low" if problems_done < 10 else "✅ Good"
        )

        db.session.add(entry)
        db.session.commit()
        return redirect("/")

    day = len(user_data) + 1
    plan = daily_plan.get(day, "DSA Practice")
    questions = daily_questions.get(day, [])

    total_days = len(user_data)
    avg_accuracy = round(sum(d.accuracy for d in user_data) / total_days, 2) if user_data else 0
    progress = int((total_days / 90) * 100)

    return render_template(
        "index.html",
        data=user_data,
        day=day,
        plan=plan,
        questions=questions,
        total_days=total_days,
        avg_accuracy=avg_accuracy,
        progress=progress
    )


@app.route("/graph")
@login_required
def graph():

    user_data = Progress.query.filter_by(user_id=current_user.id).all()

    days = [d.day for d in user_data]
    accuracy = [d.accuracy for d in user_data]

    plt.figure()
    plt.plot(days, accuracy, marker="o")
    plt.xlabel("Day")
    plt.ylabel("Accuracy")
    plt.title("Progress Graph")
    plt.grid(True)
    plt.savefig("static/graph.png")
    plt.close()

    return render_template("graph.html")


if __name__ == "__main__":
    app.run(debug=True)