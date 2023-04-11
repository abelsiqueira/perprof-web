"""Functions related to plotting."""

import base64
from io import BytesIO

from matplotlib.figure import Figure
from perprof.profile_data import ProfileData


def matplotlib_performance_profile(solvers):
    """Plot the performance profile using matplotlib.

    Args:
        solvers (list[SolverData]): List of solvers

    Returns:
        plot_data: Data converted into a base64 format to use with flask.
    """
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
    return base64.b64encode(output.getbuffer()).decode("ascii")
