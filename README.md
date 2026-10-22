# beam-analysis
Python code for calculating stresses and strains in simple beams using strength of materials methods.

## Overview
A code to analyze beam deflection using strength of materials methods. It automatically calculates support reactions based on external forces.
You can calculate:
- the center of gravity of the beam section;
- the second moment of area;
- the maximum deflection.
You can visualize the section, applied forces, beam deformation, and internal force and bending moment diagrams.

## Assumptions
- Bernoulli-Navier hypothesis.
- The beam stays in the elastic regime.
- The beam must be statically determinate (isostatic).
- The material is homogeneous, isotropic, and continuous.

## Inputs
Geometry of the beam section (mm) and beam length (m).
Young's modulus of the material (Pa).
External forces, except support reactions (N).

## Outputs
Coordinates of the centroid.
Second moment of area of the section.
Maximum deflection.
Beam deflection/deformation diagram.
Normal force, shear force, and bending moment diagrams.

## Limitations 
We assume that the section is constant.

## Requirements
Matplotlib (visualization)
NumPy (array management and linear algebra)
SciPy (numerical integration)

## Context
I was inspired by my strength of materials class so I decided to build a free, open-source tool to visualize all essential information.
