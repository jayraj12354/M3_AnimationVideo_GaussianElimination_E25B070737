# README – M3 Animation Video: Gaussian Elimination

**Student:** Jayraj Deshmukh (`E25B070737`)  
**Course:** Linear Algebra and Calculus (M3) • Internal Assessment

## Repository Structure

```
M3_AnimationVideo_GaussianElimination_E25B070737/
├── README.md                        ← this file
├── Storyboard.pdf                   ← 6-scene storyboard PDF
├── GaussianElimination_Video.mp4    ← final 1080p 60fps MP4 with voice-over & music
└── Code/
    ├── gaussian_elimination.py      ← Manim animation source (Python)
    ├── generate_music.py            ← soft ambient background track synthesizer
    └── render.sh                    ← one-command render script
```

## How to Render

### Prerequisites
```bash
pip install manim numpy
```
> macOS users may also need: `brew install cairo pango ffmpeg`

### Render (1080p 60fps)
```bash
cd Code
bash render.sh
# OR directly:
manim -qh gaussian_elimination.py GaussianElimination
```
Output video: `Code/media/videos/gaussian_elimination/1080p60/GaussianElimination.mp4`

## Topic
**How Gaussian Elimination Solves a 3×3 Linear System**

Learning objective: *By the end of this video, the viewer will understand how Gaussian Elimination systematically converts a 3×3 augmented matrix to Row Echelon Form and uses back-substitution to find the unique solution.*

## Tools Used & AI Disclosure
- **Manim Community Edition** – programmatic math animation
- **Python 3 + NumPy** – ambient background music synthesis
- **FFmpeg** – audio-video synchronization and mastering
- **Antigravity AI** – script and Manim code drafting assistance *(disclosed)*

## References
- Gilbert Strang, *Introduction to Linear Algebra*, 5th Edition, Wellesley-Cambridge Press
- Manim Community Docs: https://docs.manim.community
