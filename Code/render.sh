#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
# render.sh – One-command render script for the Gaussian
#              Elimination animation video.
# Usage:  bash render.sh
# Output: media/videos/gaussian_elimination/1080p60/GaussianElimination.mp4
# ─────────────────────────────────────────────────────────────

set -euo pipefail
cd "$(dirname "$0")"

echo "▶ Rendering Gaussian Elimination animation (1080p 60fps)…"
manim -qh gaussian_elimination.py GaussianElimination

echo ""
echo "✅ Done! Find your video in:"
echo "   media/videos/gaussian_elimination/1080p60/GaussianElimination.mp4"
