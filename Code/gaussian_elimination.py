"""
Gaussian Elimination – M3 Animation Video
Topic: How Gaussian Elimination Solves a 3x3 Linear System
Tool : Manim (Community Edition) — pure Text/Vector rendering (no LaTeX required)

Run with:
    manim -pqh gaussian_elimination.py GaussianElimination
"""

from manim import *

# ── Global colour palette ────────────────────────────────────────────────────
BG      = "#000000"   # pure premium black background
GOLD    = "#F0C040"
TEAL    = "#00C4B4"
PINK    = "#FF6B8A"
LGREEN  = "#7ED957"
WHITE   = "#FFFFFF"
LTGRAY  = "#CCCCCC"
ROW_COL = [TEAL, GOLD, PINK]   # consistent colours for equations / rows 1, 2, 3
OP_COL  = LGREEN               # row-operation label colour


# ── Shared matrix builder (no external LaTeX required) ───────────────────────
def _build_matrix_grid(rows, font_size, col_spacing, row_spacing, pivots, zeros,
                       aug_col_gap=0.0, bracket_pad=0.26, tick=0.16, bold_highlights=False):
    """Build matrix entries and square brackets; return (l_bracket, entries, r_bracket)."""
    if not rows or not rows[0]:
        raise ValueError("Matrix must be non-empty")

    pivots = pivots or set()
    zeros = zeros or set()

    entries = VGroup()
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            color = WHITE
            weight = NORMAL
            if (r_idx, c_idx) in pivots:
                color = GOLD
                weight = BOLD if bold_highlights else NORMAL
            elif (r_idx, c_idx) in zeros:
                color = LGREEN
                weight = BOLD if bold_highlights else NORMAL

            t = Text(str(val), font_size=font_size, color=color, weight=weight)
            x_offset = c_idx * col_spacing + (aug_col_gap if c_idx == len(row) - 1 else 0.0)
            y_offset = -r_idx * row_spacing
            t.move_to([x_offset, y_offset, 0])
            entries.add(t)

    entries.move_to(ORIGIN)
    top_y = entries.get_top()[1] + 0.18
    bot_y = entries.get_bottom()[1] - 0.18
    left_x = entries.get_left()[0] - bracket_pad
    right_x = entries.get_right()[0] + bracket_pad

    l_bracket = VGroup(
        Line([left_x + tick, top_y, 0], [left_x, top_y, 0], color=WHITE, stroke_width=2.8),
        Line([left_x, top_y, 0], [left_x, bot_y, 0], color=WHITE, stroke_width=2.8),
        Line([left_x, bot_y, 0], [left_x + tick, bot_y, 0], color=WHITE, stroke_width=2.8),
    )
    r_bracket = VGroup(
        Line([right_x - tick, top_y, 0], [right_x, top_y, 0], color=WHITE, stroke_width=2.8),
        Line([right_x, top_y, 0], [right_x, bot_y, 0], color=WHITE, stroke_width=2.8),
        Line([right_x, bot_y, 0], [right_x - tick, bot_y, 0], color=WHITE, stroke_width=2.8),
    )
    return l_bracket, entries, r_bracket, top_y, bot_y


def make_aug_matrix(rows, font_size=30, col_spacing=1.05, row_spacing=0.65,
                    pivots=None, zeros=None):
    """Build an augmented 3x4 matrix VGroup with square brackets and vertical bar."""
    if any(len(r) != 4 for r in rows):
        raise ValueError("Augmented matrix expects 4 columns per row")

    l_bracket, entries, r_bracket, top_y, bot_y = _build_matrix_grid(
        rows, font_size, col_spacing, row_spacing, pivots, zeros,
        aug_col_gap=0.35, bracket_pad=0.28, tick=0.18, bold_highlights=True,
    )
    bar_x = (entries[2].get_center()[0] + entries[3].get_center()[0]) / 2
    divider = Line([bar_x, top_y, 0], [bar_x, bot_y, 0], color=LTGRAY, stroke_width=2.2)
    return VGroup(l_bracket, entries, divider, r_bracket)


def make_3x3_pattern(rows, font_size=34, col_spacing=0.85, row_spacing=0.65,
                     pivots=None, zeros=None):
    """Build a 3x3 matrix VGroup with square brackets (no divider)."""
    l_bracket, entries, r_bracket, _, _ = _build_matrix_grid(
        rows, font_size, col_spacing, row_spacing, pivots, zeros,
        aug_col_gap=0.0, bracket_pad=0.26, tick=0.16, bold_highlights=False,
    )
    return VGroup(l_bracket, entries, r_bracket)


# ════════════════════════════════════════════════════════════════════════════
#  SCENE 0 – Opening Frame (Title, Concept, Student Name & ID) (~14.3 s)
# ════════════════════════════════════════════════════════════════════════════
class Scene0_Opening(Scene):
    def construct(self):
        self.camera.background_color = BG

        course = Text(
            "LINEAR ALGEBRA AND CALCULUS (M3)  •  INTERNAL ASSESSMENT",
            font_size=22, color=TEAL, weight=BOLD
        ).to_edge(UP, buff=1.1)

        title = Text("Gaussian Elimination", font_size=56, color=GOLD, weight=BOLD)
        subtitle = Text(
            "Solving a 3 × 3 System of Linear Equations Visually",
            font_size=30, color=WHITE
        ).next_to(title, DOWN, buff=0.35)

        divider = Line(LEFT * 4, RIGHT * 4, color=TEAL, stroke_width=2).next_to(
            subtitle, DOWN, buff=0.55
        )

        student = Text(
            "Student Name: Jayraj Deshmukh    |    Student ID: E25B070737",
            font_size=26, color=LTGRAY
        ).next_to(divider, DOWN, buff=0.55)

        self.play(FadeIn(course, shift=DOWN * 0.2), run_time=0.8)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle, shift=UP * 0.2), Create(divider), run_time=0.9)
        self.play(FadeIn(student), run_time=0.8)
        self.wait(9.8)
        self.play(FadeOut(VGroup(course, title, subtitle, divider, student)), run_time=0.8)


# ════════════════════════════════════════════════════════════════════════════
#  SCENE 1 – Hook / Context (~35.9 s)
# ════════════════════════════════════════════════════════════════════════════
class Scene1_Hook(Scene):
    def construct(self):
        self.camera.background_color = BG

        question = Text(
            "How do you solve THREE equations\nwith THREE unknowns — systematically?",
            font_size=38, color=WHITE, line_spacing=1.4
        ).to_edge(UP, buff=0.8)

        self.play(Write(question), run_time=2.5)
        self.wait(2.5)

        label = Text(
            "Real-world systems: electrical circuits, economics, 3-D graphics…",
            font_size=26, color=LTGRAY
        ).next_to(question, DOWN, buff=0.5)
        self.play(FadeIn(label, shift=UP * 0.2), run_time=1.0)
        self.wait(8.5)

        eq1 = Text(" 2x +  y −  z =   8", font_size=38, color=ROW_COL[0])
        eq2 = Text("−3x −  y + 2z = −11", font_size=38, color=ROW_COL[1])
        eq3 = Text("−2x +  y + 2z =  −3", font_size=38, color=ROW_COL[2])
        eqs = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.42, aligned_edge=LEFT).move_to(DOWN * 0.35)

        for eq in eqs:
            self.play(FadeIn(eq, shift=RIGHT * 0.4), run_time=1.0)
            self.wait(3.0)

        hint = Text("Enter: Gaussian Elimination →", font_size=32, color=GOLD, weight=BOLD)
        hint.next_to(eqs, DOWN, buff=0.75)
        self.play(Write(hint), run_time=1.4)
        self.wait(7.2)

        self.play(FadeOut(VGroup(question, label, eqs, hint)), run_time=0.8)


# ════════════════════════════════════════════════════════════════════════════
#  SCENE 2 – Concept Introduction (~44.6 s)
# ════════════════════════════════════════════════════════════════════════════
class Scene2_ConceptIntro(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("What is Gaussian Elimination?", font_size=42, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.2)

        obj = Text(
            "Goal: Convert Ax = b into Row Echelon Form, then use Back-Substitution.",
            font_size=25, color=TEAL
        ).next_to(title, DOWN, buff=0.35)
        self.play(FadeIn(obj), run_time=1.0)
        self.wait(3.8)

        bullets = VGroup(
            Text("• A systematic algorithm for solving linear systems  Ax = b", font_size=26, color=WHITE),
            Text("• Uses the augmented matrix  [A | b]  to track all coefficients", font_size=26, color=WHITE),
            Text("• Applies three Elementary Row Operations that preserve solutions", font_size=26, color=WHITE),
            Text("• Reduces to Row Echelon Form (REF), then solves bottom-up", font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(obj, DOWN, buff=0.45)

        for idx, line in enumerate(bullets):
            self.play(FadeIn(line, shift=RIGHT * 0.3), run_time=1.0)
            self.wait(1.5 if idx == 3 else 2.5)

        ops_title = Text("Three Elementary Row Operations", font_size=27, color=TEAL, weight=BOLD)
        op1 = VGroup(
            Text("Rᵢ ↔ Rⱼ", color=LGREEN, font_size=26, weight=BOLD),
            Text("   – Swap two rows", font_size=25, color=WHITE),
        ).arrange(RIGHT, buff=0.15)
        op2 = VGroup(
            Text("k·Rᵢ → Rᵢ  (k ≠ 0)", color=LGREEN, font_size=26, weight=BOLD),
            Text("   – Scale a row", font_size=25, color=WHITE),
        ).arrange(RIGHT, buff=0.15)
        op3 = VGroup(
            Text("Rᵢ + k·Rⱼ → Rᵢ", color=LGREEN, font_size=26, weight=BOLD),
            Text("   – Add a multiple of one row to another", font_size=25, color=WHITE),
        ).arrange(RIGHT, buff=0.15)

        rows = VGroup(op1, op2, op3).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        box_group = VGroup(ops_title, rows).arrange(DOWN, buff=0.26).to_edge(DOWN, buff=0.45)
        box = SurroundingRectangle(box_group, color=TEAL, corner_radius=0.15, buff=0.25)

        self.play(FadeIn(ops_title), Create(box), run_time=1.0)
        for r in rows:
            self.play(FadeIn(r, shift=RIGHT * 0.2), run_time=0.9)
            self.wait(3.2)

        self.wait(11.5)
        self.play(FadeOut(VGroup(title, obj, bullets, box_group, box)), run_time=0.8)


# ════════════════════════════════════════════════════════════════════════════
#  SCENE 3 – Visual Intuition (~28.3 s)
# ════════════════════════════════════════════════════════════════════════════
class Scene3_VisualIntuition(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Visual Intuition: Staircase (Row Echelon) Form",
                     font_size=38, color=GOLD, weight=BOLD).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)

        before_lbl = Text("General (dense) matrix", font_size=24, color=LTGRAY)
        before_mat = make_3x3_pattern([
            ["•", "•", "•"],
            ["•", "•", "•"],
            ["•", "•", "•"],
        ])
        before_grp = VGroup(before_lbl, before_mat).arrange(DOWN, buff=0.28)

        after_lbl = Text("Row Echelon Form (goal)", font_size=24, color=TEAL)
        after_mat = make_3x3_pattern(
            [
                ["■", "•", "•"],
                ["0", "■", "•"],
                ["0", "0", "■"],
            ],
            pivots={(0, 0), (1, 1), (2, 2)},
            zeros={(1, 0), (2, 0), (2, 1)},
        )
        after_grp = VGroup(after_lbl, after_mat).arrange(DOWN, buff=0.28)

        arrow = Arrow(LEFT * 0.5, RIGHT * 0.5, color=LGREEN, buff=0.1)
        row = VGroup(before_grp, arrow, after_grp).arrange(RIGHT, buff=0.65).next_to(title, DOWN, buff=0.5)

        self.play(FadeIn(before_grp), run_time=0.8)
        self.wait(1.5)
        self.play(GrowArrow(arrow), FadeIn(after_grp), run_time=1.2)
        self.wait(3.5)

        note = Text(
            "Each elimination step forces a zero below the pivot (■),\n"
            "creating a 'staircase' of zeros in the lower triangle.",
            font_size=24, color=WHITE, line_spacing=1.35
        ).next_to(row, DOWN, buff=0.45)
        self.play(FadeIn(note), run_time=1.0)
        self.wait(6.0)

        geo_title = Text(
            "Geometric Picture: Equations as Planes Intersecting at One Point",
            font_size=24, color=TEAL
        ).next_to(note, DOWN, buff=0.4)

        plane = NumberPlane(
            x_range=[-3, 3, 1], y_range=[-2, 2, 1],
            x_length=4.5, y_length=2.2,
            background_line_style={"stroke_opacity": 0.25}
        ).next_to(geo_title, DOWN, buff=0.22)

        l1 = plane.plot(lambda x: 0.6 * x + 0.4, x_range=[-3, 2.6], color=ROW_COL[0])
        l2 = plane.plot(lambda x: -0.8 * x + 1.1, x_range=[-1.1, 3], color=ROW_COL[1])
        pt = Dot(plane.c2p(0.5, 0.7), color=LGREEN, radius=0.09)
        pt_lbl = Text("Unique Solution", font_size=19, color=LGREEN).next_to(pt, UP + RIGHT, buff=0.1)

        self.play(FadeIn(geo_title), Create(plane), run_time=1.2)
        self.play(Create(l1), Create(l2), run_time=1.2)
        self.play(FadeIn(pt, scale=1.5), FadeIn(pt_lbl), run_time=0.8)
        self.wait(9.3)

        self.play(FadeOut(VGroup(title, row, note, geo_title, plane, l1, l2, pt, pt_lbl)), run_time=0.8)


# ════════════════════════════════════════════════════════════════════════════
#  SCENE 4 – Worked Example (~67.7 s)
# ════════════════════════════════════════════════════════════════════════════
class Scene4_WorkedExample(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Worked Example: 3 × 3 System", font_size=40, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.45)
        self.play(Write(title), run_time=1.0)

        # Left side: Original system + Augmented matrix
        sys_lbl = Text("Original system:", font_size=24, color=LTGRAY).next_to(
            title, DOWN, buff=0.35
        ).to_edge(LEFT, buff=0.7)

        sys_eqs = VGroup(
            Text(" 2x +  y −  z =   8", font_size=27, color=ROW_COL[0]),
            Text("−3x −  y + 2z = −11", font_size=27, color=ROW_COL[1]),
            Text("−2x +  y + 2z =  −3", font_size=27, color=ROW_COL[2]),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(sys_lbl, DOWN, buff=0.2).to_edge(LEFT, buff=0.85)

        self.play(FadeIn(sys_lbl), FadeIn(sys_eqs), run_time=1.0)
        self.wait(2.0)

        aug_lbl = Text("Augmented matrix  [A | b]:", font_size=24, color=LTGRAY).next_to(
            sys_eqs, DOWN, buff=0.38
        ).to_edge(LEFT, buff=0.7)

        aug0 = make_aug_matrix(
            [
                ["2", "1", "−1", "8"],
                ["−3", "−1", "2", "−11"],
                ["−2", "1", "2", "−3"],
            ],
            pivots={(0, 0)},
        ).next_to(aug_lbl, DOWN, buff=0.3).to_edge(LEFT, buff=0.85)

        self.play(FadeIn(aug_lbl), FadeIn(aug0), run_time=1.2)
        self.wait(3.8)

        # Right side: Step-by-step operations & intermediate arithmetic
        right_x = 2.6

        # ── STEP 1 ── (17.0 s)
        step1_hdr = Text("Step 1: Eliminate −3 below pivot 2", font_size=24, color=GOLD).move_to([right_x, 1.85, 0])
        op1_tex = Text("R₂ ← R₂ + (3/2) R₁", font_size=27, color=OP_COL, weight=BOLD).next_to(
            step1_hdr, DOWN, buff=0.18
        )
        calc1 = Text(
            "[−3, −1, 2 | −11] + (3/2)[2, 1, −1 | 8] = [0, ½, ½ | 1]",
            font_size=19, color=LTGRAY
        ).next_to(op1_tex, DOWN, buff=0.16)

        aug1 = make_aug_matrix(
            [
                ["2", "1", "−1", "8"],
                ["0", "½", "½", "1"],
                ["−2", "1", "2", "−3"],
            ],
            pivots={(0, 0)},
            zeros={(1, 0)},
        ).move_to(aug0.get_center())

        self.play(FadeIn(step1_hdr), Write(op1_tex), run_time=1.2)
        self.wait(4.0)
        self.play(FadeIn(calc1), run_time=1.2)
        self.wait(3.5)
        self.play(ReplacementTransform(aug0, aug1), run_time=1.4)
        self.wait(5.7)

        # ── STEP 2 ── (15.0 s)
        step2_hdr = Text("Step 2: Eliminate −2 below pivot 2", font_size=24, color=GOLD).next_to(
            calc1, DOWN, buff=0.36
        )
        op2_tex = Text("R₃ ← R₃ + R₁", font_size=27, color=OP_COL, weight=BOLD).next_to(
            step2_hdr, DOWN, buff=0.18
        )
        calc2 = Text(
            "[−2, 1, 2 | −3] + [2, 1, −1 | 8] = [0, 2, 1 | 5]",
            font_size=19, color=LTGRAY
        ).next_to(op2_tex, DOWN, buff=0.16)

        aug2 = make_aug_matrix(
            [
                ["2", "1", "−1", "8"],
                ["0", "½", "½", "1"],
                ["0", "2", "1", "5"],
            ],
            pivots={(0, 0), (1, 1)},
            zeros={(1, 0), (2, 0)},
        ).move_to(aug1.get_center())

        self.play(FadeIn(step2_hdr), Write(op2_tex), run_time=1.2)
        self.wait(3.5)
        self.play(FadeIn(calc2), run_time=1.2)
        self.wait(3.0)
        self.play(ReplacementTransform(aug1, aug2), run_time=1.4)
        self.wait(4.7)

        # ── STEP 3 ── (26.7 s including fadeout)
        step3_hdr = Text("Step 3: Eliminate 2 below pivot ½", font_size=24, color=GOLD).next_to(
            calc2, DOWN, buff=0.36
        )
        op3_tex = Text("R₃ ← R₃ − 4 R₂", font_size=27, color=OP_COL, weight=BOLD).next_to(
            step3_hdr, DOWN, buff=0.18
        )
        calc3 = Text(
            "[0, 2, 1 | 5] − 4[0, ½, ½ | 1] = [0, 0, −1 | 1]",
            font_size=19, color=LTGRAY
        ).next_to(op3_tex, DOWN, buff=0.16)

        aug3 = make_aug_matrix(
            [
                ["2", "1", "−1", "8"],
                ["0", "½", "½", "1"],
                ["0", "0", "−1", "1"],
            ],
            pivots={(0, 0), (1, 1), (2, 2)},
            zeros={(1, 0), (2, 0), (2, 1)},
        ).move_to(aug2.get_center())

        ref_note = Text("Row Echelon Form!", font_size=25, color=LGREEN, weight=BOLD).next_to(
            aug3, DOWN, buff=0.3
        )

        self.play(FadeIn(step3_hdr), Write(op3_tex), run_time=1.2)
        self.wait(6.0)
        self.play(FadeIn(calc3), run_time=1.2)
        self.wait(4.5)
        self.play(ReplacementTransform(aug2, aug3), run_time=1.4)
        self.play(FadeIn(ref_note), run_time=0.8)
        self.wait(10.8)

        self.play(
            FadeOut(VGroup(
                title, sys_lbl, sys_eqs, aug_lbl, aug3, ref_note,
                step1_hdr, op1_tex, calc1,
                step2_hdr, op2_tex, calc2,
                step3_hdr, op3_tex, calc3,
            )),
            run_time=0.8,
        )


# ════════════════════════════════════════════════════════════════════════════
#  SCENE 5 – Interpretation: Back-Substitution → Solution (~53.0 s)
# ════════════════════════════════════════════════════════════════════════════
class Scene5_Interpretation(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Back-Substitution: Reading the Solution", font_size=40, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=1.0)

        ref_lbl = Text("Row Echelon Form:", font_size=26, color=LTGRAY)
        ref_mat = make_aug_matrix(
            [
                ["2", "1", "−1", "8"],
                ["0", "½", "½", "1"],
                ["0", "0", "−1", "1"],
            ],
            pivots={(0, 0), (1, 1), (2, 2)},
            zeros={(1, 0), (2, 0), (2, 1)},
        )
        grp = VGroup(ref_lbl, ref_mat).arrange(DOWN, buff=0.3).to_edge(LEFT, buff=0.8).shift(UP * 0.55)
        self.play(FadeIn(grp), run_time=1.0)
        self.wait(3.0)

        bs_title = Text("Back-Substitution (Bottom → Top):", font_size=27, color=TEAL, weight=BOLD)
        z_eq = Text("−z = 1   ⇒   z = −1", font_size=28, color=ROW_COL[2])
        y_eq = Text("½y + ½(−1) = 1   ⇒   y = 3", font_size=28, color=ROW_COL[1])
        x_eq = Text("2x + 3 − (−1) = 8   ⇒   x = 2", font_size=28, color=ROW_COL[0])

        bs_grp = VGroup(bs_title, z_eq, y_eq, x_eq).arrange(DOWN, buff=0.36, aligned_edge=LEFT)
        bs_grp.to_edge(RIGHT, buff=0.7).shift(UP * 0.55)

        self.play(FadeIn(bs_title), run_time=0.8)
        self.play(FadeIn(z_eq, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(4.5)
        self.play(FadeIn(y_eq, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(8.8)
        self.play(FadeIn(x_eq, shift=RIGHT * 0.3), run_time=1.2)
        self.wait(8.8)

        sol_txt = Text("x = 2,   y = 3,   z = −1", font_size=36, color=LGREEN, weight=BOLD)
        sol_box = SurroundingRectangle(sol_txt, color=LGREEN, corner_radius=0.12, buff=0.22)
        sol = VGroup(sol_txt, sol_box).to_edge(DOWN, buff=1.35)
        self.play(Write(sol_txt), Create(sol_box), run_time=1.2)
        self.wait(2.5)

        verify = Text(
            "Verify: 2(2)+3−(−1)=8 ✔   −3(2)−3+2(−1)=−11 ✔   −2(2)+3+2(−1)=−3 ✔",
            font_size=22, color=GOLD
        ).next_to(sol, DOWN, buff=0.32)
        self.play(FadeIn(verify), run_time=1.0)
        self.wait(6.5)

        geo = Text(
            "Geometrically: (2, 3, −1) is the unique point where all three planes intersect.",
            font_size=24, color=LTGRAY
        ).next_to(verify, DOWN, buff=0.28)
        self.play(FadeIn(geo), run_time=1.0)
        self.wait(8.5)

        self.play(FadeOut(VGroup(title, grp, bs_grp, sol, verify, geo)), run_time=0.8)


# ════════════════════════════════════════════════════════════════════════════
#  SCENE 6 – Summary & Credits (~18.1 s)
# ════════════════════════════════════════════════════════════════════════════
class Scene6_Summary(Scene):
    def construct(self):
        self.camera.background_color = BG

        title = Text("Summary & Credits", font_size=44, color=GOLD, weight=BOLD)
        title.to_edge(UP, buff=0.55)
        self.play(Write(title), run_time=1.0)

        takeaways = VGroup(
            Text("1. Gaussian Elimination converts [A | b] into Row Echelon Form (REF)", font_size=26, color=WHITE),
            Text("2. Swap, Scale, and Row-Add operations preserve the solution set", font_size=26, color=WHITE),
            Text("3. Back-substitution reads off (x, y, z) = (2, 3, −1) from bottom up", font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(title, DOWN, buff=0.55)

        for item in takeaways:
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=0.9)
            self.wait(2.2)

        credits_title = Text("Credits & AI Disclosure", font_size=28, color=TEAL, weight=BOLD)
        credits_body = Text(
            "Author: Jayraj Deshmukh (E25B070737)  •  M3 Internal Assessment\n"
            "Animation: Manim Community Edition (Python)\n"
            "Reference: Gilbert Strang, 'Introduction to Linear Algebra', 5th ed.\n"
            "AI Disclosure: Script and Manim code drafting assisted by Antigravity AI.\n"
            "Background Music: Original Soft Ambient Pad (Synthesized, Royalty-Free)",
            font_size=21, color=LTGRAY, line_spacing=1.45
        )
        credits_grp = VGroup(credits_title, credits_body).arrange(DOWN, buff=0.25)
        credits_grp.to_edge(DOWN, buff=0.55)

        self.play(FadeIn(credits_grp), run_time=1.0)
        self.wait(5.8)

        self.play(FadeOut(VGroup(title, takeaways, credits_grp)), run_time=1.0)


# ════════════════════════════════════════════════════════════════════════════
#  MASTER SCENE – runs all scenes sequentially
# ════════════════════════════════════════════════════════════════════════════
class GaussianElimination(Scene):
    """
    Master scene: chains Opening + all 6 scenes.
    Render with:
        manim -pqh gaussian_elimination.py GaussianElimination
    """

    def construct(self):
        subscenes = [
            Scene0_Opening,
            Scene1_Hook,
            Scene2_ConceptIntro,
            Scene3_VisualIntuition,
            Scene4_WorkedExample,
            Scene5_Interpretation,
            Scene6_Summary,
        ]
        for SceneClass in subscenes:
            SceneClass.construct(self)
