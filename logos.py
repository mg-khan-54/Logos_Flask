from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__, instance_relative_config=True)

with open("config.json", "r") as f:
    params = json.load(f)["params"]

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/logos"
db = SQLAlchemy(app)


class Logos(db.Model):
    __tablename__ = 'company_logo'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    img = db.Column(db.String(250), unique=True, nullable=False)


@app.route("/")
@app.route("/<string:page>", methods=["GET"])
def index(page=None):
    search = request.args.get("search")
    if search:
        data = Logos.query.filter(Logos.name.ilike(f"%{search}%")).all()
    else:
        data = Logos.query.filter_by().all()
    return render_template("index.html", params=params, posts=data, page=page)


if __name__ == '__main__':
    app.run(debug=True, port=8002)
