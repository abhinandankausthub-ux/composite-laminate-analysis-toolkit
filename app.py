import streamlit as st
import numpy as np

from modules.material_database import get_all_materials
from modules.stacking_parser import parse_stacking_sequence
from modules.abd_matrix import compute_ABD
from modules.ply_stress import compute_laminate_response
from modules.failure_criteria import (
    tsai_hill_failure,
    maximum_stress_failure,
    tsai_wu_failure
)
from modules.progressive_failure import progressive_failure

from plots.laminate_plots import plot_laminate_stack, plot_stress_through_thickness
from reports.report_generator import generate_report
from modules.laminate_optimizer import optimize_laminate



# -------------------------------------------------
# Page Setup
# -------------------------------------------------

st.set_page_config(page_title="Composite Laminate Toolkit", layout="wide")

st.title("Composite Laminate Analysis Toolkit")
st.write("Classical Lamination Theory (CLT) based laminate analysis tool.")


# -------------------------------------------------
# Material Selection
# -------------------------------------------------

materials = get_all_materials()

material_name = st.selectbox(
    "Select Material",
    list(materials.keys())
)

material = materials[material_name]


# -------------------------------------------------
# Laminate Definition
# -------------------------------------------------

st.subheader("Laminate Definition")

stack_input = st.text_input(
    "Stacking Sequence",
    "[0/45/-45/90]s"
)

ply_thickness = st.number_input(
    "Ply Thickness",
    value=0.125,
    step=0.001,
    format="%.3f"
)


# -------------------------------------------------
# Loads
# -------------------------------------------------

st.subheader("Applied Loads")

col1, col2 = st.columns(2)

with col1:
    Nx = st.number_input("Nx", value=1000.0)
    Ny = st.number_input("Ny", value=0.0)
    Nxy = st.number_input("Nxy", value=0.0)

with col2:
    Mx = st.number_input("Mx", value=0.0)
    My = st.number_input("My", value=0.0)
    Mxy = st.number_input("Mxy", value=0.0)

loads = [Nx, Ny, Nxy, Mx, My, Mxy]


# -------------------------------------------------
# Run Analysis
# -------------------------------------------------

if st.button("Run Analysis"):

    try:

        stack = parse_stacking_sequence(stack_input)

        A, B, D = compute_ABD(material, stack, ply_thickness)

        results = compute_laminate_response(
            material,
            stack,
            ply_thickness,
            loads
        )

        st.session_state["stack"] = stack
        st.session_state["A"] = A
        st.session_state["B"] = B
        st.session_state["D"] = D
        st.session_state["loads"] = loads
        st.session_state["results"] = results

        st.success("Analysis completed successfully")

    except Exception as e:

        st.error(f"Error: {e}")


# -------------------------------------------------
# Display Results
# -------------------------------------------------

if "results" in st.session_state:

    stack = st.session_state["stack"]
    A = st.session_state["A"]
    B = st.session_state["B"]
    D = st.session_state["D"]
    results = st.session_state["results"]


    # -------------------------------------------------
    # ABD Matrices
    # -------------------------------------------------

    st.subheader("ABD Matrices")

    colA, colB, colC = st.columns(3)

    with colA:
        st.write("A Matrix")
        st.write(A)

    with colB:
        st.write("B Matrix")
        st.write(B)

    with colC:
        st.write("D Matrix")
        st.write(D)


    # -------------------------------------------------
    # Failure Analysis
    # -------------------------------------------------

    st.subheader("Ply Failure Analysis")

    failure_data = []

    for ply in results:

        stress = ply["stress"]

        FI_hill = tsai_hill_failure(stress, material)
        FI_max = maximum_stress_failure(stress, material)
        FI_wu = tsai_wu_failure(stress, material)

        failure_data.append({
            "Ply": ply["ply"],
            "Angle": ply["angle"],
            "Max Stress": FI_max,
            "Tsai-Hill": FI_hill,
            "Tsai-Wu": FI_wu
        })

    st.table(failure_data)


    # -------------------------------------------------
    # Visualization
    # -------------------------------------------------

    st.subheader("Laminate Visualization")

    col1, col2 = st.columns(2)

    with col1:
        fig1 = plot_laminate_stack(stack, ply_thickness)
        st.pyplot(fig1)

    with col2:
        fig2 = plot_stress_through_thickness(results)
        st.pyplot(fig2)


    # -------------------------------------------------
    # Progressive Failure Simulation
    # -------------------------------------------------

    st.subheader("Progressive Ply Failure Simulation")

    if st.button("Run Progressive Failure"):

        failure_sequence = progressive_failure(
            material,
            stack,
            ply_thickness,
            loads
        )

        st.write("Failure Sequence")
        st.table(failure_sequence)


    # -------------------------------------------------
    # Laminate Optimizer
    # -------------------------------------------------

    st.subheader("Laminate Design Optimizer")

    if st.button("Run Laminate Optimizer"):

        best_stack, best_fi = optimize_laminate(
            material,
            ply_thickness,
            loads
        )

        st.write("Optimal Stacking Sequence")
        st.write(best_stack)

        st.write("Maximum Failure Index")
        st.write(best_fi)


    # -------------------------------------------------
    # Engineering Report
    # -------------------------------------------------

    st.subheader("Engineering Report")

    if st.button("Generate PDF Report"):

        generate_report(
            material_name,
            stack,
            st.session_state["loads"],
            A,
            B,
            D
        )

        st.success("Report generated successfully: laminate_report.pdf")