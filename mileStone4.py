import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from agents import run_workflow

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/workflow")
def workflow():
    return render_template("workflow.html", title="Workflow")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/contact")
def contact():
    return render_template("contact.html", title="Contact")


@app.route("/run-workflow", methods=["POST"])
def run_workflow_api():
    data = request.json

    topic = data.get("topic", "").strip()
    purpose = data.get("purpose", "").strip()

    #  BLOCK empty input
    if not topic or not purpose:
        return jsonify({
            "error": "Topic and Email Purpose are required."
        }), 400

    return jsonify(run_workflow(topic, purpose))


if __name__ == "__main__":
    app.run(debug=True)
