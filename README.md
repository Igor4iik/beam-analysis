# beam-analysis
Python tool for simple beam analysis using strength of materials methods.

## Overview
A code to analyze beam deflection using strength of materials methods. It automatically calculates support reactions based on external forces.
You can calculate:
- the center of gravity of the beam section;
- the second moment of area;
- the maximum deflection.
And visualize the section, applied forces, beam deformation, and internal force and bending moment diagrams.

## Assumptions
- Bernoulli-Navier hypothesis.
- The beam stays in the elastic regime.
- The beam must be statically determinate (isostatic).
- The material is homogeneous, isotropic, and continuous.

## Inputs
- Geometry of the beam section (mm) and beam length (m).
- Young's modulus of the material (Pa).
- External forces, except support reactions (N).

## Outputs
- Coordinates of the centroid.
- Second moment of area of the section.
- Maximum deflection.
- Beam deflection/deformation diagram.
- Normal force, shear force, and bending moment diagrams.

## Example

- The cross-section is composed of rectangular sub-sections  [[0,0,60,20],[20,20,40,60],[0,60,60,80]]
```
# Les éléments rectangulaires élémentaires composant la surface en mm
# Rect = [[x1,y1,x2,y2],[x1,y1,x2,y2]]
Rect = [[0,0,60,20],[20,20,40,60],[0,60,60,80]]
```
<img width="298" height="260" alt="изображение" src="https://github.com/user-attachments/assets/7427609c-a89c-4b47-8be5-e58b0135c9a2" />

- Young's modulus E = 200e9 Pa (steel)

- Length of L = 10 m

- 2 vertical forces: 100N at 3 m and -150 N at 7 m <br>
  No horizontal forces
```
# La position des efforts extérieurs en newton sauf celle des supports
# F = [[force 1, position 1], [force 2, position 2], ...]
Fy = [[100.0, 3.0], [-150.0, 7.0]]
Fx = []
```
- 2 supports: pin at 0m and a roller at 10 m <br>
`Pos_supp = [[0,'pin'], [10,'roller']]` <br>

<img width="960" height="720" alt="forces" src="https://github.com/user-attachments/assets/d7d5696c-2517-43de-8c17-51b4cf6c29e6" />

<img width="960" height="720" alt="diagrams" src="https://github.com/user-attachments/assets/2c428ba6-e4d8-4a1c-9eac-04bbdb6d2783" />


## Limitations 
We assume that the section is constant.

## Requirements 
Matplotlib (visualization) <br>
NumPy (array management and linear algebra) <br>
SciPy (numerical integration) <br>

## Context
I was inspired by my strength of materials class so I decided to build a free, open-source tool to visualize all essential information.
