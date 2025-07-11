If useful to your research, we would appreciate a citation:<br>
**Su Y., Iyela P.M., Zhu J., et al.**  
*A Voronoi-based Gaussian smoothing algorithm for efficiently generating RVEs of multi-phase composites with graded aggregates and random pores*.  
Materials & Design 244, 113159 (2024).  
DOI: [10.1016/j.matdes.2024.113159](https://doi.org/10.1016/j.matdes.2024.113159)
Feel free to utilize this code. 
If any questions, please email us (suyutai@nwpu.edu.cn). <br>


# 3D-multi-phase-meso-scale-modelling-of-concrete
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  <!-- 可选：添加License徽章 -->
## Keywords:
Abaqus; Python script; Mayavi; three-dimensional (3D) meso-scale model; multi-phase material
## Features
- ✅ **Multi-phase modeling**:
  - Graded aggregates generation
  - Interfacial Transition Zones (ITZ) modeling
  - Mortar matrix construction
  - Random pore distribution

- ⚡ **ABAQUS integration**:
  - Automatic `.inp` file generation
  - Pre-defined element sets (`*ELSET`)
  - Pixel-to-element mapping preserved

## File Structure
├── 📄 main.py # main algorithm<br>
├── 📄 plot_utils.py # visualization<br>
├── 📄 inp_writer.py # ABAQUS INP file output<br>
├── 📂 inpfiles/ # INP files generations<br>
└── 📄 README.md<br>

## Packages requirements
Packages, including numpy, scipy, and mayavi are needed.
Inp files with ordered element numbers in Abaqus should also be prepared first. <br>

## Usage
1. Configure parameters in `main.py`.
2. Run generation.
3. Outputs will be saved in inpfiles/

## Some results
Mesostructure of our model: <br>
![image](https://user-images.githubusercontent.com/116877222/221400622-1f44794d-f6b7-474f-8b96-abc23ccf35f2.png)<br>
Generation time for 1,000,000 elements:<br>
![image](https://user-images.githubusercontent.com/116877222/221400646-3b096761-83ba-49ca-a6a2-b2f1bf4e5da8.png)<br>
