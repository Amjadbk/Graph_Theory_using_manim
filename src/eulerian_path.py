"""
Eulerian Paths and Circuits Visualization

This module provides animated visualizations of Eulerian paths and circuits,
including Hierholzer's and Fleury's algorithms for finding Eulerian trails.

The visualization includes:
- Euler path vs. Euler circuit concepts
- Degree conditions for Eulerian graphs
- Hierholzer's algorithm step-by-step
- Fleury's algorithm demonstration
- Multiple example graphs
"""

from manim import *
from collections import defaultdict


class EulerianPaths(Scene):
    """
    Visualizes Eulerian paths, circuits, and algorithms for finding them.

    An Eulerian path uses every edge exactly once, while an Eulerian circuit
    is an Eulerian path that returns to the starting vertex. This scene
    demonstrates the conditions and algorithms for finding such paths.
    """

    def construct(self):
        # ============================================================
        # Configuration: Visual Styles and Constants
        # ============================================================
        EDGE_COLOR = WHITE
        EDGE_HIGHLIGHT = YELLOW
        NODE_COLOR = WHITE
        NODE_ACTIVE = YELLOW
        NODE_SPECIAL = RED
        CIRCUIT_COLOR = GREEN
        STACK_COLOR = BLUE
        EDGE_WIDTH = 3

        vertex_style = {
            "radius": 0.18,
            "fill_color": NODE_COLOR,
            "stroke_color": WHITE,
            "stroke_width": 2,
        }
        edge_style = {
            "stroke_color": EDGE_COLOR,
            "stroke_width": EDGE_WIDTH,
        }

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------
        def make_graph(vertices, edges, layout, directed=False):
            """
            Create a graph with consistent styling and vertex ID labels
            that ALWAYS stay centered on the node.
            """
            g = Graph(
                vertices,
                edges,
                layout=layout,
                vertex_config=vertex_style,
                edge_config=edge_style,
                edge_type=Arrow if directed else Line,
            )

            labels = VGroup()
            for v in vertices:
                lbl = MathTex(str(v), font_size=20, color=BLACK)
                # Always keep node-ID label at the center of its vertex
                lbl.add_updater(lambda m, v=v, g=g: m.move_to(g.vertices[v].get_center()))
                labels.add(lbl)

            return g, labels

        def make_degree_labels(graph, vertices, deg_dict, direction_map, color_map=None, buff=0.4, font_size=20):
            """
            Degree labels anchored relative to each vertex (UP/DOWN/LEFT/RIGHT/diagonal),
            staying correct even if the graph moves/shifts.
            """
            deg_labels = VGroup()
            for v in vertices:
                d_lbl = MathTex(rf"\deg({v})={deg_dict[v]}", font_size=font_size)

                if color_map is not None:
                    d_lbl.set_color(color_map(v, deg_dict[v]))

                direction = direction_map.get(v, UP)

                # Keep the label attached to the node with the same relative direction
                d_lbl.add_updater(
                    lambda m, v=v, g=graph, direction=direction, buff=buff:
                        m.next_to(g.vertices[v], direction, buff=buff)
                )
                deg_labels.add(d_lbl)

            return deg_labels

        def highlight_path(graph, labels, seq, color=EDGE_HIGHLIGHT, close_cycle=False, run_time_per_edge=0.9):
            if close_cycle and seq[0] != seq[-1]:
                seq = list(seq) + [seq[0]]

            dot = Dot(radius=0.12, color=color)
            dot.move_to(graph.vertices[seq[0]].get_center())
            self.add(dot)

            used_edges = []
            for u, v in zip(seq[:-1], seq[1:]):
                key = (u, v) if (u, v) in graph.edges else (v, u)
                used_edges.append(key)
                edge_mob = graph.edges[key]
                self.play(
                    dot.animate.move_to(graph.vertices[v].get_center()),
                    edge_mob.animate.set_stroke(color=color, width=EDGE_WIDTH + 1),
                    run_time=run_time_per_edge,
                )

            self.wait(1)
            self.play(
                *[graph.edges[e].animate.set_stroke(EDGE_COLOR, width=EDGE_WIDTH) for e in set(used_edges)],
                dot.animate.set_opacity(0),
                run_time=0.9,
            )
            self.remove(dot)

        def get_edge_key(u, v, graph):
            return (u, v) if (u, v) in graph.edges else (v, u)

        # ============================================================
        # Section 1: Introduction
        # ============================================================
        title = Text("Graph Theory – Eulerian Path and Circuit", font_size=48)
        self.play(FadeIn(title, shift=UP * 0.5), run_time=2.25)
        self.wait(1)
        self.play(FadeOut(title, shift=UP * 0.5), run_time=1.2)

        # ============================================================
        # Section 2: Euler Path
        # ============================================================
        path_title = Text("Euler Path", font_size=40).to_edge(UP)
        self.play(Write(path_title), run_time=1.2)

        def_euler_path = MathTex(
            r"\text{Euler path: uses every edge exactly once,}",
            r"\\ \text{starts and ends at different vertices.}",
            font_size=30,
        ).next_to(path_title, DOWN, buff=0.5)
        self.play(Write(def_euler_path), run_time=1.8)

        verts_p = [1, 2, 3, 4]
        edges_p = [(1, 2), (2, 3), (3, 4), (2, 4)]
        layout_p = {
            1: LEFT * 3 + UP * 0.5,
            2: LEFT * 1,
            3: RIGHT * 1,
            4: RIGHT * 3 + 0.5 * UP,
        }
        g_path, lbl_path = make_graph(verts_p, edges_p, layout_p, directed=False)
        self.play(Create(g_path), Write(lbl_path), run_time=2.25)
        self.wait(1)

        deg_p = {v: sum(1 for e in edges_p if v in e) for v in verts_p}
        deg_labels_p = make_degree_labels(
            g_path,
            verts_p,
            deg_p,
            direction_map={
                1: UP,
                2: DOWN,
                3: UP,
                4: UP,
            },
            color_map=lambda v, d: RED if d % 2 == 1 else GREEN,
            buff=0.4,
            font_size=20,
        )
        self.play(Write(deg_labels_p), run_time=1.5)
        self.wait(1)

        condition_text = MathTex(
            r"\text{Exactly 2 odd degrees } \Rightarrow \text{ Euler path exists}",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN, buff=0.7)
        self.play(Write(condition_text), run_time=1.2)
        self.wait(1)

        ex_path = MathTex(
            r"\text{Example Euler path: } 1 \to 2 \to 3 \to 4 \to 2",
            font_size=26,
        ).move_to(condition_text.get_center())
        self.play(Transform(condition_text, ex_path), run_time=1.2)
        self.wait(1)

        highlight_path(g_path, lbl_path, [1, 2, 3, 4, 2], color=EDGE_HIGHLIGHT, run_time_per_edge=0.75)

        self.play(FadeOut(deg_labels_p), run_time=0.75)
        self.play(
            FadeOut(path_title), FadeOut(def_euler_path), FadeOut(condition_text),
            FadeOut(g_path), FadeOut(lbl_path),
            run_time=1.2
        )

        # ============================================================
        # Section 3: Euler Circuit
        # ============================================================
        circuit_title = Text("Euler Circuit", font_size=40).to_edge(UP)
        self.play(Write(circuit_title), run_time=1.2)

        def_euler_circuit = MathTex(
            r"\text{Euler circuit: uses every edge exactly once,}",
            r"\\ \text{starts and ends at the same vertex.}",
            font_size=30,
        ).next_to(circuit_title, DOWN, buff=0.5)
        self.play(Write(def_euler_circuit), run_time=1.8)

        verts_c = [1, 2, 3, 4]
        edges_c = [(1, 2), (2, 3), (3, 4), (4, 1)]
        layout_c = {
            1: LEFT * 2 + UP * 1.2,
            2: RIGHT * 2 + UP * 1.2,
            3: RIGHT * 2 + DOWN * 1.2,
            4: LEFT * 2 + DOWN * 1.2,
        }
        g_cyc, lbl_cyc = make_graph(verts_c, edges_c, layout_c, directed=False)
        self.play(Create(g_cyc), Write(lbl_cyc), run_time=1.8)
        self.wait(1)

        deg_c = {v: sum(1 for e in edges_c if v in e) for v in verts_c}
        deg_labels_c = make_degree_labels(
            g_cyc,
            verts_c,
            deg_c,
            direction_map={
                1: UP,
                2: UP,
                3: DOWN,
                4: DOWN,
            },
            color_map=lambda v, d: GREEN,
            buff=0.4,
            font_size=20,
        )
        self.play(Write(deg_labels_c), run_time=1.5)
        self.wait(1)

        condition_text_c = MathTex(
            r"\text{All vertices have even degree } \Rightarrow \text{ Euler circuit exists}",
            font_size=24,
            color=GREEN,
        ).to_edge(DOWN, buff=0.7)
        self.play(Write(condition_text_c), run_time=1.2)
        self.wait(1)

        ex_cyc = MathTex(
            r"\text{Example Euler circuit: } 1 \to 2 \to 3 \to 4 \to 1",
            font_size=26,
        ).move_to(condition_text_c.get_center())
        self.play(Transform(condition_text_c, ex_cyc), run_time=1.2)
        self.wait(1)

        highlight_path(g_cyc, lbl_cyc, [1, 2, 3, 4, 1], color=CIRCUIT_COLOR, run_time_per_edge=0.75)

        self.play(FadeOut(deg_labels_c), run_time=0.75)
        self.play(
            FadeOut(circuit_title), FadeOut(def_euler_circuit), FadeOut(condition_text_c),
            FadeOut(g_cyc), FadeOut(lbl_cyc),
            run_time=1.2
        )

        # Add batman.jpg image
        try:
            batman_img = ImageMobject("assets/batman.jpg")
            batman_img.scale(1.5)
            batman_img.move_to(ORIGIN)
            self.play(FadeIn(batman_img), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(batman_img), run_time=1.0)
        except:
            batman_text = Text("🦇 BATMAN 🦇", font_size=64, color=YELLOW)
            self.play(FadeIn(batman_text), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(batman_text), run_time=1.0)

        # ============================================================
        # Section 4: Eulerian Conditions
        # ============================================================
        cond_title = Text("Euler Conditions", font_size=40).to_edge(UP)
        self.play(Write(cond_title), run_time=1.2)

        cond1_text = MathTex(
            r"\text{All vertices have even degree } \Rightarrow \text{ Euler circuit}",
            font_size=28,
        ).next_to(cond_title, DOWN, buff=0.4)
        self.play(Write(cond1_text), run_time=1.5)

        verts_even = [1, 2, 3, 4]
        edges_even = [(1, 2), (2, 3), (3, 4), (4, 1)]
        layout_even = {
            1: LEFT * 2 + UP * 1.2,
            2: RIGHT * 2 + UP * 1.2,
            3: RIGHT * 2 + DOWN * 1.2,
            4: LEFT * 2 + DOWN * 1.2,
        }
        g_even, lbl_even = make_graph(verts_even, edges_even, layout_even, False)
        g_even.shift(DOWN * 0.5)
        self.play(Create(g_even), Write(lbl_even), run_time=1.8)

        deg_even = {v: sum(1 for e in edges_even if v in e) for v in verts_even}

        # REQUESTED CHANGE:
        # Place top degrees to LEFT of node 1 and RIGHT of node 2
        deg_labels_even = make_degree_labels(
            g_even,
            verts_even,
            deg_even,
            direction_map={
                1: LEFT,   # left of node 1
                2: RIGHT,  # right of node 2
                3: DOWN,
                4: DOWN,
            },
            color_map=lambda v, d: GREEN,
            buff=0.35,
            font_size=20,
        )
        self.play(Write(deg_labels_even), run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(g_even), FadeOut(lbl_even), FadeOut(deg_labels_even),
            FadeOut(cond1_text),
            run_time=1.2
        )

        cond2_text = MathTex(
            r"\text{Exactly two vertices have odd degree } \Rightarrow \text{ Euler path}",
            font_size=28,
        ).next_to(cond_title, DOWN, buff=0.4)
        self.play(Write(cond2_text), run_time=1.5)

        verts_odd = [1, 2, 3, 4]
        edges_odd = [(1, 2), (2, 3), (3, 4), (4, 1), (2, 4)]
        layout_odd = {
            1: LEFT * 2.5 + UP * 0.5,
            2: ORIGIN + UP * 1.5,
            3: RIGHT * 2.5 + UP * 0.5,
            4: ORIGIN + DOWN * 1.5,
        }
        g_odd, lbl_odd = make_graph(verts_odd, edges_odd, layout_odd, False)
        g_odd.shift(DOWN * 0.5)
        self.play(Create(g_odd), Write(lbl_odd), run_time=1.8)

        deg_odd = {v: sum(1 for e in edges_odd if v in e) for v in verts_odd}
        odd_verts = [v for v, d in deg_odd.items() if d % 2 == 1]

        deg_labels_odd = make_degree_labels(
            g_odd,
            verts_odd,
            deg_odd,
            direction_map={
                1: UP + LEFT,
                2: UP,
                3: UP + RIGHT,
                4: DOWN,
            },
            color_map=lambda v, d: RED if d % 2 == 1 else GREEN,
            buff=0.4,
            font_size=20,
        )
        self.play(Write(deg_labels_odd), run_time=1.5)
        self.wait(1)

        self.play(
            *[g_odd.vertices[v].animate.set_fill(NODE_SPECIAL) for v in odd_verts],
            run_time=1.2
        )
        self.wait(1)

        self.play(
            FadeOut(cond_title), FadeOut(cond2_text), FadeOut(g_odd),
            FadeOut(lbl_odd), FadeOut(deg_labels_odd),
            run_time=1.2
        )

        # Add dog.png image
        try:
            dog_img = ImageMobject("assets/dog.png")
            dog_img.scale(1.5)
            dog_img.move_to(ORIGIN)
            self.play(FadeIn(dog_img), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(dog_img), run_time=1.0)
        except:
            dog_text = Text("🐕 DOG 🐕", font_size=64, color=YELLOW)
            self.play(FadeIn(dog_text), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(dog_text), run_time=1.0)

        # ============================================================
        # Degree Progression (Adding Edges)
        # ============================================================
        prog_title = Text("Degree Progression Example", font_size=40).to_edge(UP)
        self.play(Write(prog_title), run_time=1.2)

        verts_prog = [1, 2, 3, 4]
        edges_prog_start = [(1, 2), (3, 4)]
        layout_prog = {
            1: LEFT * 1.5 + UP * 1.2,
            2: RIGHT * 1.5 + UP * 1.2,
            3: RIGHT * 1.5 + DOWN * 1.2,
            4: LEFT * 1.5 + DOWN * 1.2,
        }

        g_prog, lbl_prog = make_graph(verts_prog, edges_prog_start, layout_prog, False)
        g_prog.shift(DOWN * 0.2)
        self.play(Create(g_prog), Write(lbl_prog), run_time=1.8)

        deg_prog = {v: sum(1 for e in edges_prog_start if v in e) for v in verts_prog}
        deg_labels_prog = make_degree_labels(
            g_prog,
            verts_prog,
            deg_prog,
            direction_map={1: UP, 2: UP, 3: DOWN, 4: DOWN},
            color_map=lambda v, d: RED,
            buff=0.4,
            font_size=20,
        )
        self.play(Write(deg_labels_prog), run_time=1.5)

        state_text1 = MathTex(
            r"\text{Initial: All 4 vertices have odd degree (no Euler path/circuit)}",
            font_size=22,
            color=RED,
        ).to_edge(DOWN, buff=0.7)
        self.play(Write(state_text1), run_time=1.5)
        self.wait(1)

        new_edge1 = (2, 3)
        g_prog.add_edges(new_edge1, edge_config=edge_style)
        self.play(Create(g_prog.edges[get_edge_key(2, 3, g_prog)]), run_time=1.2)

        edges_prog_step2 = edges_prog_start + [new_edge1]
        deg_prog_step2 = {v: sum(1 for e in edges_prog_step2 if v in e) for v in verts_prog}

        new_deg_labels = make_degree_labels(
            g_prog,
            verts_prog,
            deg_prog_step2,
            direction_map={1: UP, 2: UP, 3: DOWN, 4: DOWN},
            color_map=lambda v, d: RED if d % 2 == 1 else GREEN,
            buff=0.4,
            font_size=20,
        )
        self.play(Transform(deg_labels_prog, new_deg_labels), run_time=1.5)

        state_text2 = MathTex(
            r"\text{After adding edge (2,3): Exactly 2 odd degrees } \Rightarrow \text{ Euler path exists}",
            font_size=22,
            color=YELLOW,
        ).move_to(state_text1.get_center())
        self.play(Transform(state_text1, state_text2), run_time=1.5)
        self.wait(1)

        new_edge2 = (1, 4)
        g_prog.add_edges(new_edge2, edge_config=edge_style)
        self.play(Create(g_prog.edges[get_edge_key(1, 4, g_prog)]), run_time=1.2)

        edges_prog_step3 = edges_prog_step2 + [new_edge2]
        deg_prog_step3 = {v: sum(1 for e in edges_prog_step3 if v in e) for v in verts_prog}

        new_deg_labels3 = make_degree_labels(
            g_prog,
            verts_prog,
            deg_prog_step3,
            direction_map={1: UP, 2: UP, 3: DOWN, 4: DOWN},
            color_map=lambda v, d: GREEN,
            buff=0.4,
            font_size=20,
        )
        self.play(Transform(deg_labels_prog, new_deg_labels3), run_time=1.5)

        state_text3 = MathTex(
            r"\text{After adding edge (1,4): All vertices have even degree } \Rightarrow \text{ Euler circuit exists}",
            font_size=22,
            color=GREEN,
        ).move_to(state_text1.get_center())
        self.play(Transform(state_text1, state_text3), run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(prog_title), FadeOut(g_prog), FadeOut(lbl_prog),
            FadeOut(deg_labels_prog), FadeOut(state_text1),
            run_time=1.2
        )

        # ============================================================
        # Section 6: Hierholzer's Algorithm (text only)
        # ============================================================
        hierholzer_title = Text("Hierholzer's Algorithm", font_size=40).to_edge(UP)
        self.play(Write(hierholzer_title), run_time=1.2)

        algo_text = VGroup(
            MathTex(r"\text{1. Start with empty stack and empty path/trail.}", font_size=24),
            MathTex(r"\text{   Choose start vertex (even degree: any, odd: one of two).}", font_size=24),
            MathTex(r"\text{2. If current vertex has no neighbors:}", font_size=24),
            MathTex(r"\text{   - Add it to path, pop from stack, set as current.}", font_size=24),
            MathTex(r"\text{3. Otherwise (has neighbors):}", font_size=24),
            MathTex(r"\text{   - Push vertex to stack, pick neighbor, remove edge, move.}", font_size=24),
            MathTex(r"\text{4. Repeat until no neighbors and stack is empty.}", font_size=24),
            MathTex(r"\text{5. Path/trail is in reverse order (end to start).}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        algo_text.next_to(hierholzer_title, DOWN, buff=0.4)
        self.play(Write(algo_text), run_time=3.75)
        self.wait(1)

        self.play(FadeOut(hierholzer_title), FadeOut(algo_text), run_time=1.2)

        # ============================================================
        # Section 7: Hierholzer Example
        # ============================================================
        example_title = Text("Hierholzer Example", font_size=40).to_edge(UP)
        self.play(Write(example_title), run_time=1.2)

        verts_h = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        edges_h = [
            (1, 2), (1, 6), (1, 8), (1, 9),
            (2, 3), (2, 4), (2, 8),
            (3, 4),
            (5, 8),
            (6, 9),
            (7, 8),
        ]
        layout_h = {
            1: UP * 2.0,
            2: LEFT * 2.5 + UP * 0.8,
            3: LEFT * 2.5 + DOWN * 0.6,
            4: LEFT * 0.8 + DOWN * 1.6,
            5: RIGHT * 1.6 + DOWN * 1.8,
            6: RIGHT * 2.8 + UP * 0.8,
            7: RIGHT * 3.2 + DOWN * 0.8,
            8: RIGHT * 1.4 + ORIGIN,
            9: ORIGIN + UP * 0.8,
        }
        g_h, lbl_h = make_graph(verts_h, edges_h, layout_h, False)
        g_h.shift(DOWN * 0.3)
        self.play(Create(g_h), Write(lbl_h), run_time=1.8)
        self.wait(1)

        stack_label = Text("Stack:", font_size=22, color=STACK_COLOR).to_edge(LEFT, buff=0.8).shift(UP * 0.8)
        stack_container = Rectangle(width=1.2, height=4.0, color=STACK_COLOR, stroke_width=2)
        stack_container.next_to(stack_label, RIGHT, buff=0.2)
        stack_bottom = stack_container.get_bottom()[1]
        self.add(stack_label, stack_container)

        path_label = Text("Path:", font_size=22, color=GREEN).to_edge(LEFT, buff=0.8).shift(DOWN * 2.0)
        path_text = MathTex("", font_size=14, color=GREEN).next_to(path_label, RIGHT, buff=0.2)
        self.add(path_label, path_text)

        stack_vertices = []
        stack_visual_items = VGroup()
        path = []

        current_vertex = 5
        remaining_edges = {(min(u, v), max(u, v)) for u, v in edges_h}

        status_text = MathTex(
            r"\text{Start: Choose an odd-degree vertex, here } 5",
            font_size=20,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.8)
        self.play(Write(status_text), run_time=1.2)

        self.play(g_h.vertices[current_vertex].animate.set_fill(NODE_ACTIVE), run_time=0.75)

        current_node_indicator = Dot(radius=0.12, color=RED)
        current_node_indicator.move_to(g_h.vertices[current_vertex].get_center())
        self.add(current_node_indicator)
        self.wait(1)

        while True:
            neighbors = []
            for edge in list(remaining_edges):
                u, v = edge
                if u == current_vertex:
                    neighbors.append(v)
                elif v == current_vertex:
                    neighbors.append(u)

            if len(neighbors) == 0:
                path.append(current_vertex)

                path_str = r" \to ".join([str(v) for v in path])
                new_path_text = MathTex(path_str, font_size=14, color=GREEN).next_to(path_label, RIGHT, buff=0.2)
                new_path_text.scale(0.8)
                self.play(
                    Transform(path_text, new_path_text),
                    g_h.vertices[current_vertex].animate.set_fill(CIRCUIT_COLOR),
                    run_time=0.9
                )

                if len(stack_vertices) == 0:
                    break

                old_vertex = current_vertex
                current_vertex = stack_vertices.pop()

                if len(stack_visual_items) > 0:
                    items_list = list(stack_visual_items)
                    if len(items_list) > 0:
                        item_to_remove = items_list[-1]
                        self.play(FadeOut(item_to_remove), run_time=0.6)
                        stack_visual_items.remove(item_to_remove)

                        for i, item in enumerate(stack_visual_items):
                            item_y = stack_bottom + 0.3 + i * 0.4
                            self.play(item.animate.move_to([stack_container.get_center()[0], item_y, 0]), run_time=0.3)

                new_status = MathTex(
                    rf"\text{{No neighbors: add {old_vertex} to path, pop {current_vertex} from stack}}",
                    font_size=20,
                    color=YELLOW,
                ).move_to(status_text.get_center())

                self.play(
                    Transform(status_text, new_status),
                    g_h.vertices[current_vertex].animate.set_fill(NODE_ACTIVE),
                    current_node_indicator.animate.move_to(g_h.vertices[current_vertex].get_center()),
                    run_time=0.9
                )
                self.wait(1)

            else:
                stack_vertices.append(current_vertex)
                stack_item = Text(str(current_vertex), font_size=18, color=STACK_COLOR)

                item_y = stack_bottom + 0.3 + (len(stack_vertices) - 1) * 0.4
                stack_item.move_to([stack_container.get_center()[0], item_y, 0])
                stack_visual_items.add(stack_item)
                self.play(FadeIn(stack_item), run_time=0.6)

                next_vertex = neighbors[0]
                edge_tuple = (min(current_vertex, next_vertex), max(current_vertex, next_vertex))
                remaining_edges.discard(edge_tuple)
                edge_key = get_edge_key(current_vertex, next_vertex, g_h)

                new_status = MathTex(
                    rf"\text{{Push {current_vertex} to stack, move to {next_vertex}, remove edge}}",
                    font_size=20,
                    color=YELLOW,
                ).move_to(status_text.get_center())

                self.play(
                    Transform(status_text, new_status),
                    g_h.vertices[current_vertex].animate.set_fill(NODE_COLOR),
                    g_h.vertices[next_vertex].animate.set_fill(NODE_ACTIVE),
                    g_h.edges[edge_key].animate.set_stroke(opacity=0.3, width=EDGE_WIDTH),
                    current_node_indicator.animate.move_to(g_h.vertices[next_vertex].get_center()),
                    run_time=1.2
                )

                current_vertex = next_vertex
                self.wait(1)

        final_path = list(reversed(path))

        self.play(
            FadeOut(example_title), FadeOut(g_h), FadeOut(lbl_h),
            FadeOut(stack_label), FadeOut(stack_container),
            FadeOut(stack_visual_items), FadeOut(status_text),
            run_time=1.2
        )

        try:
            self.remove(current_node_indicator)
        except Exception:
            pass

        original_path_str = r" \to ".join([str(v) for v in path])
        path_label_top = Text("Path:", font_size=22, color=GREEN).move_to(UP * 1.2 + LEFT * 2.0)
        original_path_text = MathTex(original_path_str, font_size=18, color=GREEN)
        original_path_text.next_to(path_label_top, RIGHT, buff=0.2)

        self.play(
            path_label.animate.move_to(path_label_top.get_center()),
            path_text.animate.move_to(original_path_text.get_center()).scale(1 / 0.8),
            run_time=1.0
        )
        self.wait(0.5)

        final_path_str = r" \to ".join([str(v) for v in final_path])
        euler_trail_label = MathTex(r"\text{Euler Path:}", font_size=22, color=CIRCUIT_COLOR).move_to(DOWN * 0.3 + LEFT * 2.0)
        final_path_text = MathTex(final_path_str, font_size=22, color=CIRCUIT_COLOR)
        final_path_text.next_to(euler_trail_label, RIGHT, buff=0.2)

        self.play(Write(euler_trail_label), Write(final_path_text), run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(path_label), FadeOut(path_text),
            FadeOut(euler_trail_label), FadeOut(final_path_text),
            run_time=1.2
        )

        # ============================================================
        # Cut Edge (Bridge)
        # ============================================================
        bridge_title = Text("Cut Edge (Bridge)", font_size=40).to_edge(UP)
        self.play(Write(bridge_title), run_time=1.2)

        bridge_def = MathTex(
            r"\text{A cut edge (bridge) is an edge whose removal}",
            r"\\ \text{disconnects the graph.}",
            font_size=28,
        ).next_to(bridge_title, DOWN, buff=0.5)
        self.play(Write(bridge_def), run_time=1.5)

        verts_bridge = [1, 2, 3, 4, 5]
        edges_bridge = [(1, 2), (2, 3), (3, 1), (4, 5), (2, 4)]
        layout_bridge = {
            1: LEFT * 2.5 + UP * 1.0,
            2: ORIGIN + UP * 1.5,
            3: LEFT * 2.5 + DOWN * 1.0,
            4: RIGHT * 2.5 + UP * 1.0,
            5: RIGHT * 2.5 + DOWN * 1.0,
        }
        g_bridge, lbl_bridge = make_graph(verts_bridge, edges_bridge, layout_bridge, False)
        g_bridge.shift(DOWN * 0.3)
        self.play(Create(g_bridge), Write(lbl_bridge), run_time=1.8)
        self.wait(1)

        bridge_edge_key = get_edge_key(2, 4, g_bridge)
        self.play(g_bridge.edges[bridge_edge_key].animate.set_stroke(color=RED, width=EDGE_WIDTH + 2), run_time=1.2)

        bridge_label = Text("BRIDGE", font_size=20, color=RED)
        bridge_label.next_to(g_bridge.edges[bridge_edge_key], UP, buff=0.2)
        self.play(Write(bridge_label), run_time=0.9)
        self.wait(1)

        bridge_edge_mob = g_bridge.edges[bridge_edge_key]
        self.play(FadeOut(bridge_edge_mob), FadeOut(bridge_label), run_time=1.2)

        comp1_text = Text("Component 1", font_size=20, color=BLUE).next_to(g_bridge.vertices[1], LEFT, buff=0.5)
        comp2_text = Text("Component 2", font_size=20, color=GREEN).next_to(g_bridge.vertices[4], RIGHT, buff=0.5)
        self.play(Write(comp1_text), Write(comp2_text), run_time=1.2)
        self.wait(1)

        self.play(
            FadeOut(bridge_title), FadeOut(bridge_def),
            FadeOut(lbl_bridge), FadeOut(comp1_text), FadeOut(comp2_text),
            run_time=1.2
        )
        self.play(
            *[FadeOut(g_bridge.vertices[v]) for v in verts_bridge],
            *[FadeOut(g_bridge.edges[e]) for e in g_bridge.edges if e != bridge_edge_key],
            run_time=1.2
        )

        # ============================================================
        # Fleury's Algorithm
        # ============================================================
        fleury_title = Text("Fleury's Algorithm", font_size=40).to_edge(UP)
        self.play(Write(fleury_title), run_time=1.2)

        fleury_text = VGroup(
            MathTex(r"\text{1. Start at a vertex with odd degree (if exists),}", font_size=26),
            MathTex(r"\text{   otherwise start anywhere.}", font_size=26),
            MathTex(r"\text{2. Choose an edge to traverse:}", font_size=26),
            MathTex(r"\text{   - Avoid bridges unless no other choice.}", font_size=26),
            MathTex(r"\text{3. Remove the edge and move to next vertex.}", font_size=26),
            MathTex(r"\text{4. Repeat until all edges are used.}", font_size=26),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        fleury_text.next_to(fleury_title, DOWN, buff=0.4)
        self.play(Write(fleury_text), run_time=3.0)
        self.wait(1)

        key_point = MathTex(
            r"\text{Key: Avoid bridges when possible!}",
            font_size=28,
            color=YELLOW,
        ).to_edge(DOWN, buff=0.8)
        self.play(Write(key_point), run_time=1.5)
        self.wait(1)

        self.play(FadeOut(fleury_title), FadeOut(fleury_text), FadeOut(key_point), run_time=1.2)

        # ============================================================
        # Euler Path Example (Fleury)
        # ============================================================
        example2_title = Text("Euler Path Example", font_size=40).to_edge(UP)
        self.play(Write(example2_title), run_time=1.2)

        verts_ex = [1, 2, 3, 4, 5]
        edges_ex = [(1, 2), (2, 3), (1, 3), (1, 4), (4, 5)]
        layout_ex = {
            1: LEFT * 3 + UP * 0.5,
            2: LEFT * 1.3 + DOWN * 0.8,
            3: LEFT * 1.0 + UP * 1.8,
            4: RIGHT * 1.5 + DOWN * 0.2,
            5: RIGHT * 3.0 + DOWN * 0.2,
        }
        g_ex, lbl_ex = make_graph(verts_ex, edges_ex, layout_ex, False)
        g_ex.shift(UP * 0.3)
        self.play(Create(g_ex), Write(lbl_ex), run_time=1.8)

        start_text = MathTex("", font_size=24, color=YELLOW).to_edge(DOWN, buff=0.8)
        self.add(start_text)

        start_vertex = 1
        self.play(g_ex.vertices[start_vertex].animate.set_fill(NODE_ACTIVE), run_time=0.75)

        current_node_indicator_f = Dot(radius=0.12, color=RED)
        current_node_indicator_f.move_to(g_ex.vertices[start_vertex].get_center())
        self.add(current_node_indicator_f)
        self.wait(1)

        path_ex = [1, 2, 3, 1, 4, 5]
        used_edges_ex = set()
        step_texts = []

        for i in range(len(path_ex) - 1):
            u, v = path_ex[i], path_ex[i + 1]
            key = get_edge_key(u, v, g_ex)

            if key not in used_edges_ex:
                used_edges_ex.add(key)

                if step_texts:
                    self.play(FadeOut(step_texts[-1]), run_time=0.45)

                step_text = MathTex(
                    rf"\text{{Step {i+1}: }} {u} \to {v}",
                    font_size=22,
                    color=YELLOW,
                ).to_edge(DOWN, buff=0.5)
                step_texts.append(step_text)
                self.play(Write(step_text), run_time=0.6)

                self.play(current_node_indicator_f.animate.move_to(g_ex.vertices[u].get_center()), run_time=0.3)

                self.play(
                    g_ex.edges[key].animate.set_stroke(color=YELLOW, width=EDGE_WIDTH + 1),
                    g_ex.vertices[u].animate.set_fill(NODE_COLOR),
                    g_ex.vertices[v].animate.set_fill(NODE_ACTIVE),
                    current_node_indicator_f.animate.move_to(g_ex.vertices[v].get_center()),
                    run_time=0.9,
                )

                self.play(
                    g_ex.edges[key].animate.set_stroke(opacity=0.3, width=EDGE_WIDTH),
                    run_time=0.45,
                )

        final_path_text = MathTex(
            r"\text{Euler Path (Fleury): } 1 \to 2 \to 3 \to 1 \to 4 \to 5",
            font_size=22,
            color=GREEN,
        ).to_edge(DOWN, buff=0.4)

        if step_texts:
            self.play(FadeOut(step_texts[-1]), run_time=0.45)

        self.play(Write(final_path_text), run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(example2_title), FadeOut(g_ex), FadeOut(lbl_ex),
            FadeOut(start_text), FadeOut(final_path_text),
            FadeOut(current_node_indicator_f),
            run_time=1.2
        )

        # ============================================================
        # Final Summary
        # ============================================================
        summary_title = Text("Summary", font_size=48)
        self.play(FadeIn(summary_title, shift=UP * 0.5), run_time=1.5)
        self.wait(1)
        self.play(summary_title.animate.to_edge(UP), run_time=1.2)

        summary_points = VGroup(
            MathTex(r"\text{Euler Path: uses every edge once, different start/end}", font_size=26),
            MathTex(r"\text{Euler Circuit: uses every edge once, same start/end}", font_size=26),
            MathTex(r"\text{Condition: All even degrees } \Rightarrow \text{ circuit}", font_size=26),
            MathTex(r"\text{Condition: Exactly 2 odd degrees } \Rightarrow \text{ path}", font_size=26),
            MathTex(r"\text{Algorithms: Hierholzer's and Fleury's}", font_size=26),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.6)
        self.play(Write(summary_points), run_time=3.75)
        self.wait(1)

        self.play(FadeOut(summary_title), FadeOut(summary_points), run_time=1.5)
        self.wait(1)
