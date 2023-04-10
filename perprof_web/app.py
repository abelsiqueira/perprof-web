"""Main file."""

import base64
import logging
import os
from io import BytesIO

from flask import Flask, redirect, render_template, request, url_for
from matplotlib.figure import Figure
from perprof.profile_data import ProfileData
from perprof.solver_data import SolverData, read_table
from werkzeug.utils import secure_filename

# Define folder to save uploaded files to process further
UPLOAD_FOLDER = os.path.join("uploads")

# Define allowed files (for this example I want only csv file)
ALLOWED_EXTENSIONS = {"csv", "table"}

app = Flask(__name__)
# Configure upload file path flask
app.config["UPLOAD_FOLDER"] = os.path.join(os.path.dirname(__file__), UPLOAD_FOLDER)

# Define secret key to enable session
app.secret_key = "This is your secret key to utilize session in Flask"

solvers = []


@app.route("/")
def home():
    """Home."""
    return render_template(
        "index.html",
        solvers=solvers,
    )


@app.route("/solvers", methods=("POST", "GET"))
def show_solvers():
    """Main page for solvers."""
    if request.method == "POST":
        # upload file flask
        uploaded_file = request.files["uploaded-file"]
        filename = secure_filename(uploaded_file.filename)
        savepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        uploaded_file.save(savepath)

        ext = filename.split(".")[-1]
        if ext == "csv":
            solvers.append(
                SolverData(
                    f"Unnamed solver {len(solvers) + 1}",
                    savepath,
                )
            )
        elif ext == "table":
            solvers.append(read_table(savepath))
        else:
            # TODO: Treat correctly using Flask
            raise ValueError(f"Bad {filename}. Unexpected extension {ext}.")

    fig = Figure()
    axis = fig.subplots()

    if len(solvers) >= 2:
        profile_data = ProfileData(*solvers)
        for i, solver in enumerate(solvers):
            axis.plot(
                profile_data.breakpoints,
                profile_data.cumulative[:, i],
                label=solver.algname,
            )

        axis.set_xscale("log")
        axis.set_xlim(profile_data.breakpoints.min(), profile_data.breakpoints.max())
        axis.set_ylim(-0.02, 1.04)
        axis.legend()

    output = BytesIO()
    fig.savefig(output, format="png")

    data = base64.b64encode(output.getbuffer()).decode("ascii")

    return render_template(
        "solvers.html",
        plot_data=data,
        solvers=solvers,
    )


@app.route("/solvers/<int:solver_id>")
def show_solver(solver_id):
    """Details of a solver."""
    return render_template(
        "solver.html",
        solvers=solvers,
        solver=solvers[solver_id],
    )


@app.route("/update/solver/<int:solver_id>", methods=["POST"])
def update_solver(solver_id):
    """Delete or update a solver."""
    logging.warning(request.form)
    action = request.form.get("action")

    if action == "delete":
        solvers.pop(solver_id)
    elif action == "edit":
        new_algname = request.form.get("algname")
        if len(new_algname.strip()) == 0:
            return "Solver name must be non-null"
        if new_algname != solvers[solver_id].algname:
            solvers[solver_id].algname = new_algname

    return redirect(url_for("show_solvers"))
