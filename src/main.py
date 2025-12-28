from manim import *
import itertools
import random

class GraphSequence(Scene):
    def construct(self):
        random.seed(1)  # for reproducibility
        
        # ============================================================
        # Introduction
        # ============================================================
        intro_title = Text("Graph Theory – Traversals, Types, and Matrices", font_size=48)
        self.play(FadeIn(intro_title, shift=UP * 0.5), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(intro_title, shift=UP * 0.5), run_time=1.2)

        # ============================================================
        # Dark Image
        # ============================================================
        try:
            dark_img = ImageMobject("assets/dark.jpg")
            dark_img.scale(2.0)
            dark_img.move_to(ORIGIN)
            self.play(FadeIn(dark_img), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(dark_img), run_time=1.0)
        except:
            # If image not found, skip
            pass

        # ============================================================
        # Node and Edge Introduction
        # ============================================================
        # Create a simple node and edge to introduce the concepts
        intro_node = Dot(radius=0.15, color=WHITE, fill_opacity=1.0)
        intro_node.move_to(LEFT * 2 + UP * 1)
        
        intro_node2 = Dot(radius=0.15, color=WHITE, fill_opacity=1.0)
        intro_node2.move_to(RIGHT * 2 + UP * 1)
        
        intro_edge = Line(
            intro_node.get_center(),
            intro_node2.get_center(),
            stroke_color=WHITE,
            stroke_width=3
        )
        
        node_label = Text("Node", font_size=32, color=YELLOW)
        node_label.next_to(intro_node, DOWN, buff=0.5)
        
        edge_label = Text("Edge", font_size=32, color=YELLOW)
        edge_label.next_to(intro_edge, DOWN, buff=0.5)
        
        self.play(
            FadeIn(intro_node),
            FadeIn(intro_node2),
            run_time=1.0
        )
        self.play(Write(node_label), run_time=0.8)
        self.wait(0.5)
        
        self.play(Create(intro_edge), run_time=1.0)
        self.play(Write(edge_label), run_time=0.8)
        self.wait(1)
        
        self.play(
            FadeOut(intro_node),
            FadeOut(intro_node2),
            FadeOut(intro_edge),
            FadeOut(node_label),
            FadeOut(edge_label),
            run_time=1.0
        )
        self.wait(0.5)

        # Shared styles
        edge_width = 3
        vertex_style = {
            "radius": 0.12,
            "fill_color": WHITE,
            "stroke_color": WHITE,
            "stroke_width": 2,
        }
        edge_style = {
            "stroke_color": WHITE,
            "stroke_width": edge_width,
        }

        # ============================================================
        # Traversal helper
        # ============================================================
        def animate_traversal(graph, vertex_sequence, color=YELLOW, dot_radius=0.12):
            if not vertex_sequence or len(vertex_sequence) < 2:
                return
            dot = Dot(radius=dot_radius, color=color)
            dot.move_to(graph.vertices[vertex_sequence[0]].get_center())
            self.add(dot)
            used_edges = []
            for i in range(len(vertex_sequence) - 1):
                u, v = vertex_sequence[i], vertex_sequence[i + 1]
                if (u, v) in graph.edges:
                    edge_key = (u, v)
                elif (v, u) in graph.edges:
                    edge_key = (v, u)
                else:
                    continue
                used_edges.append(edge_key)
                self.play(dot.animate.move_to(graph.vertices[v].get_center()), run_time=0.7)
            unique_used_edges = list(dict.fromkeys(used_edges))
            if unique_used_edges:
                self.play(
                    LaggedStart(
                        *[
                            graph.edges[e].animate.set_stroke(color=color, width=edge_width + 1)
                            for e in unique_used_edges
                        ],
                        lag_ratio=0.1,
                        run_time=2.0,
                    )
                )
                self.wait(1)
                self.play(
                    *[graph.edges[e].animate.set_stroke(WHITE, width=edge_width) for e in unique_used_edges],
                    run_time=1.2,
                )
            self.play(FadeOut(dot), run_time=0.4)

        # ============================================================
        # Edge-addition helper
        # ============================================================
        # Helper: smooth edge addition (used everywhere)
        def smooth_add_edges(
            graph,
            new_edges,
            edge_width,
            color=BLUE,
            lag_ratio=0.12,
            run_time=5.0,
        ):
            """
            Add edges to a Graph and animate them smoothly:
            - start thin, transparent
            - fade in and thicken
            Returns the list of edge mobjects.
            """
            if not new_edges:
                return []

            graph.add_edges(
                *new_edges,
                edge_config={
                    "stroke_color": color,
                    "stroke_width": 1,
                }
            )
            edge_mobs = [graph.edges[e] for e in new_edges]
            for edge in edge_mobs:
                edge.set_stroke(color=color, width=1, opacity=0)

            self.play(
                LaggedStart(
                    *[
                        edge.animate.set_stroke(
                            color=color,
                            width=edge_width + 0.5,
                            opacity=1.0
                        )
                        for edge in edge_mobs
                    ],
                    lag_ratio=lag_ratio,
                    run_time=run_time,
                )
            )
            return edge_mobs

        # =========================================
        # TRAVERSALS (from gi.py)
        # =========================================
        # Degree example
        vertices_deg1 = [1, 2, 3, 4]
        edges_deg1 = [(1, 2), (2, 3), (3, 4), (1, 4), (2, 4)]
        layout_deg1 = {
            1: LEFT * 2.5 + UP * 1.5,
            2: RIGHT * 0.5 + UP * 1.5,
            3: RIGHT * 2.5 + DOWN * 1.5,
            4: LEFT * 0.5 + DOWN * 1.5,
        }
        deg1_graph = Graph(vertices_deg1, edges_deg1, layout=layout_deg1, vertex_config=vertex_style, edge_config=edge_style)
        deg1_labels = VGroup()
        for v in vertices_deg1:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(deg1_graph.vertices[v].get_center())
            deg1_labels.add(label)
        title_degree = Text("Node Degree", font_size=42).to_edge(UP)
        desc_degree = MathTex(
            r"\text{The degree of a vertex is the number of edges}",
            r"\text{ incident to it.}",
            font_size=26,
        ).next_to(title_degree, DOWN, buff=0.3)
        self.play(Create(deg1_graph), Write(title_degree), run_time=1.5)
        self.play(Write(deg1_labels), run_time=0.8)
        self.play(Write(desc_degree), run_time=1.2)
        self.wait(1)

        degrees1 = {v: sum(1 for e in edges_deg1 if v in e) for v in vertices_deg1}
        placeholder_labels = VGroup()
        for v in vertices_deg1:
            label = MathTex(f"deg({v}) = ?", font_size=28)
            placeholder_labels.add(label)
        placeholder_labels.arrange(RIGHT, buff=0.8)
        placeholder_labels.next_to(deg1_graph, DOWN, buff=0.8)
        actual_labels1 = VGroup()
        for i, v in enumerate(vertices_deg1):
            incident_edges = [e for e in edges_deg1 if v in e]
            edge_anims = [deg1_graph.edges[e].animate.set_stroke(YELLOW, width=edge_width + 1) for e in incident_edges]
            self.play(deg1_graph.vertices[v].animate.set_fill(YELLOW), *edge_anims, run_time=1.0)
            self.wait(1)
            label = MathTex(f"deg({v}) = {degrees1[v]}", font_size=28)
            label.move_to(placeholder_labels[i].get_center())
            actual_labels1.add(label)
            self.play(Write(label), run_time=0.8)
            self.play(
                deg1_graph.vertices[v].animate.set_fill(WHITE),
                *[deg1_graph.edges[e].animate.set_stroke(WHITE, width=edge_width) for e in incident_edges],
                run_time=0.8,
            )
            self.wait(1)
        self.wait(1)
        formula1 = MathTex(r"\sum_{v \in V} \deg(v) = 2|E|", font_size=32).next_to(actual_labels1, DOWN, buff=0.6)
        num_edges_deg = len(edges_deg1)
        formula1_example = MathTex(
            rf"2 + 3 + 2 + 3 = 2 \times {num_edges_deg} = {2 * num_edges_deg}", font_size=28
        ).next_to(formula1, DOWN, buff=0.3)
        self.play(Write(formula1), run_time=1.2)
        self.wait(1)
        self.play(Write(formula1_example), run_time=1.2)
        self.wait(1)
        self.play(
            FadeOut(deg1_graph),
            FadeOut(deg1_labels),
            FadeOut(title_degree),
            FadeOut(desc_degree),
            FadeOut(actual_labels1),
            FadeOut(formula1),
            FadeOut(formula1_example),
            run_time=1.0,
        )
        self.wait(1)

        # Walk
        vertices_walk = [1, 2, 3, 4]
        edges_walk = edges_deg1
        walk_graph = Graph(vertices_walk, edges_walk, layout=layout_deg1, vertex_config=vertex_style, edge_config=edge_style)
        walk_labels = VGroup()
        for v in vertices_walk:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(walk_graph.vertices[v].get_center())
            walk_labels.add(label)
        title_walk = Text("Walk", font_size=42).to_edge(UP)
        desc_walk = MathTex(
            r"\text{Vertices may repeat. Edges may repeat.}", r"\text{ (Closed or Open)}", font_size=28
        ).next_to(title_walk, DOWN, buff=0.3)
        self.play(Create(walk_graph), Write(title_walk), run_time=1.5)
        self.play(Write(walk_labels), run_time=0.8)
        self.play(Write(desc_walk), run_time=1.2)
        self.wait(1)
        walk_sequence = [1, 2, 3, 2, 4, 1, 4]
        walk_label = MathTex(
            r"1 \rightarrow 2 \rightarrow 3 \rightarrow 2 \rightarrow 4 \rightarrow 1 \rightarrow 4", font_size=24
        ).to_corner(DL)
        self.play(Write(walk_label), run_time=1.0)
        self.wait(1)
        animate_traversal(walk_graph, walk_sequence, color=YELLOW)
        self.wait(1)
        self.play(FadeOut(walk_graph), FadeOut(walk_labels), FadeOut(title_walk), FadeOut(desc_walk), FadeOut(walk_label), run_time=1.0)
        self.wait(1)

        # Trail
        vertices_trail = [1, 2, 3, 4, 5]
        edges_trail = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 3), (3, 5)]
        layout_trail = {
            1: LEFT * 3 + UP * 1.2,
            2: LEFT * 1.5 + UP * 1.8,
            3: RIGHT * 0.5 + UP * 1.2,
            4: RIGHT * 2 + UP * 0.3,
            5: RIGHT * 0.5 + DOWN * 1.2,
        }
        trail_graph = Graph(vertices_trail, edges_trail, layout=layout_trail, vertex_config=vertex_style, edge_config=edge_style)
        trail_graph.scale(0.9)
        trail_labels = VGroup()
        for v in vertices_trail:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(trail_graph.vertices[v].get_center())
            trail_labels.add(label)
        title_trail = Text("Trail", font_size=42).to_edge(UP)
        desc_trail = MathTex(r"\text{A walk with no repeated edges.}", font_size=28).next_to(title_trail, DOWN, buff=0.3)
        self.play(Create(trail_graph), Write(title_trail), run_time=1.5)
        self.play(Write(trail_labels), run_time=0.8)
        self.play(Write(desc_trail), run_time=1.2)
        self.wait(1)
        trail_sequence = [1, 2, 3, 4, 5, 3, 1]
        trail_label = MathTex(
            r"1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 5 \rightarrow 3 \rightarrow 1", font_size=22
        ).to_corner(DL)
        self.play(Write(trail_label), run_time=1.0)
        self.wait(1)
        animate_traversal(trail_graph, trail_sequence, color=GREEN)
        self.wait(1)
        self.play(FadeOut(trail_graph), FadeOut(trail_labels), FadeOut(title_trail), FadeOut(desc_trail), FadeOut(trail_label), run_time=1.0)
        self.wait(1)

        # Circuit
        vertices_circuit = [1, 2, 3, 4, 5]
        edges_circuit = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (3, 5)]
        layout_circuit = {
            1: LEFT * 2.5 + UP * 1.5,
            2: RIGHT * 0.5 + UP * 1.8,
            3: RIGHT * 2.5 + UP * 0.5,
            4: RIGHT * 2.5 + DOWN * 1.5,
            5: LEFT * 0.5 + DOWN * 1.5,
        }
        circuit_graph = Graph(
            vertices_circuit, edges_circuit, layout=layout_circuit, vertex_config=vertex_style, edge_config=edge_style
        )
        circuit_graph.scale(0.9)
        circuit_labels = VGroup()
        for v in vertices_circuit:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(circuit_graph.vertices[v].get_center())
            circuit_labels.add(label)
        title_circuit = Text("Circuit", font_size=42).to_edge(UP)
        desc_circuit = MathTex(
            r"\text{A closed trail. No repeated edges,}", r"\text{ but vertices may repeat.}", font_size=28
        ).next_to(title_circuit, DOWN, buff=0.3)
        self.play(Create(circuit_graph), Write(title_circuit), run_time=1.5)
        self.play(Write(circuit_labels), run_time=0.8)
        self.play(Write(desc_circuit), run_time=1.2)
        self.wait(1)
        circuit_sequence = [1, 2, 3, 4, 5, 3, 1]
        circuit_label = MathTex(
            r"1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 5 \rightarrow 3 \rightarrow 1", font_size=22
        ).to_corner(DL)
        self.play(Write(circuit_label), run_time=1.0)
        self.wait(1)
        animate_traversal(circuit_graph, circuit_sequence, color=BLUE)
        self.wait(1)
        start_vertex_c = circuit_graph.vertices[circuit_sequence[0]]
        self.play(start_vertex_c.animate.set_fill(RED), run_time=0.8)
        self.wait(1)
        self.play(start_vertex_c.animate.set_fill(WHITE), run_time=0.8)
        self.play(FadeOut(circuit_graph), FadeOut(circuit_labels), FadeOut(title_circuit), FadeOut(desc_circuit), FadeOut(circuit_label), run_time=1.0)
        self.wait(1)

        # Path
        vertices_path = [1, 2, 3, 4, 5, 6]
        edges_path = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (2, 5), (3, 6)]
        layout_path = {
            1: LEFT * 3 + UP * 1.5,
            2: LEFT * 1.5 + UP * 1.8,
            3: RIGHT * 0.3 + UP * 1.5,
            4: RIGHT * 2 + UP * 0.8,
            5: RIGHT * 0.3 + DOWN * 0.8,
            6: RIGHT * 2 + DOWN * 1.5,
        }
        path_graph = Graph(vertices_path, edges_path, layout=layout_path, vertex_config=vertex_style, edge_config=edge_style)
        path_graph.scale(0.85)
        path_labels = VGroup()
        for v in vertices_path:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(path_graph.vertices[v].get_center())
            path_labels.add(label)
        title_path = Text("Path", font_size=42).to_edge(UP)
        desc_path = MathTex(r"\text{An open trail with no repeated vertices.}", font_size=28).next_to(
            title_path, DOWN, buff=0.3
        )
        self.play(Create(path_graph), Write(title_path), run_time=1.5)
        self.play(Write(path_labels), run_time=0.8)
        self.play(Write(desc_path), run_time=1.2)
        self.wait(1)
        path_sequence = [1, 2, 3, 4, 5, 6]
        path_label = MathTex(r"1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 5 \rightarrow 6", font_size=24).to_corner(
            DL
        )
        self.play(Write(path_label), run_time=1.0)
        self.wait(1)
        animate_traversal(path_graph, path_sequence, color=ORANGE)
        self.wait(1)
        start_v = path_graph.vertices[path_sequence[0]]
        end_v = path_graph.vertices[path_sequence[-1]]
        self.play(start_v.animate.set_fill(GREEN), end_v.animate.set_fill(RED), run_time=1.0)
        self.wait(1)
        self.play(start_v.animate.set_fill(WHITE), end_v.animate.set_fill(WHITE), run_time=0.8)
        self.play(FadeOut(path_graph), FadeOut(path_labels), FadeOut(title_path), FadeOut(desc_path), FadeOut(path_label), run_time=1.0)
        self.wait(1)

        # Cycle
        vertices_cycle = [1, 2, 3, 4, 5]
        edges_cycle = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1), (1, 3), (2, 4)]
        layout_cycle = {
            1: LEFT * 2.5 + UP * 1.5,
            2: RIGHT * 0.5 + UP * 1.8,
            3: RIGHT * 2.5 + UP * 0.5,
            4: RIGHT * 2.5 + DOWN * 1.5,
            5: LEFT * 0.5 + DOWN * 1.5,
        }
        cycle_graph = Graph(vertices_cycle, edges_cycle, layout=layout_cycle, vertex_config=vertex_style, edge_config=edge_style)
        cycle_graph.scale(0.9)
        cycle_labels = VGroup()
        for v in vertices_cycle:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(cycle_graph.vertices[v].get_center())
            cycle_labels.add(label)
        title_cycle = Text("Cycle", font_size=42).to_edge(UP)
        desc_cycle = MathTex(
            r"\text{A closed path. No repeated vertices}", r"\text{ except start/end vertex.}", font_size=28
        ).next_to(title_cycle, DOWN, buff=0.3)
        self.play(Create(cycle_graph), Write(title_cycle), run_time=1.5)
        self.play(Write(cycle_labels), run_time=0.8)
        self.play(Write(desc_cycle), run_time=1.2)
        self.wait(1)
        cycle_sequence = [1, 2, 3, 4, 5, 1]
        cycle_label = MathTex(
            r"1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 5 \rightarrow 1", font_size=24
        ).to_corner(DL)
        self.play(Write(cycle_label), run_time=1.0)
        self.wait(1)
        animate_traversal(cycle_graph, cycle_sequence, color=PURPLE)
        self.wait(1)
        start_end_vertex = cycle_graph.vertices[cycle_sequence[0]]
        self.play(start_end_vertex.animate.set_fill(YELLOW).set_stroke(YELLOW, width=3), run_time=1.0)
        self.wait(1)
        self.play(start_end_vertex.animate.set_fill(WHITE).set_stroke(WHITE, width=2), run_time=0.8)
        self.wait(1)
        self.play(
            FadeOut(cycle_graph),
            FadeOut(cycle_labels),
            FadeOut(title_cycle),
            FadeOut(desc_cycle),
            FadeOut(cycle_label),
            run_time=0.8,
        )
        self.wait(0.5)

        # =========================================
        # PART 1: RANDOM GRAPH → COMPLETE GRAPH
        # =========================================

        n = 7
        vertices = list(range(n))

        # Base: cycle graph + a few chords
        cycle_edges = [(i, (i + 1) % n) for i in range(n)]
        all_pairs = list(itertools.combinations(vertices, 2))
        remaining_pairs = [
            e for e in all_pairs
            if e not in cycle_edges and (e[1], e[0]) not in cycle_edges
        ]
        extra_edges = [e for e in remaining_pairs if random.random() < 0.2]
        random_edges = cycle_edges + extra_edges

        graph = Graph(
            vertices,
            random_edges,
            layout="circular",
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        graph.scale(1.3)
        
        graph_labels = VGroup()
        for v in vertices:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(graph.vertices[v].get_center())
            graph_labels.add(label)

        title = Text("Random Graph", font_size=40).to_edge(UP)
        self.play(Create(graph), Write(title), run_time=1.5)
        self.play(Write(graph_labels), run_time=0.8)
        self.wait(1.0)

        num_edges_random = len(random_edges)
        stats = MathTex(
            rf"n = {n}",
            r",\quad",
            rf"|E| = {num_edges_random}",
            font_size=36
        ).to_corner(DL)
        self.play(Write(stats))
        self.wait(1.0)

        # --- Transform to complete graph ---
        complete_edges = all_pairs
        new_edges = [e for e in complete_edges if e not in random_edges]

        _ = smooth_add_edges(
            graph, new_edges, edge_width,
            color=BLUE, lag_ratio=0.12, run_time=5.0
        )

        # Recolor all edges to uniform white
        self.play(
            *[
                edge.animate.set_stroke(WHITE, width=edge_width)
                for edge in graph.edges.values()
            ],
            run_time=3.0
        )

        num_edges_complete = len(complete_edges)
        stats_complete = MathTex(
            rf"n = {n}",
            r",\quad",
            rf"|E| = {num_edges_complete} = \frac{{n(n-1)}}{{2}}",
            font_size=36
        ).to_corner(DL)

        title_complete = Text("Complete Graph", font_size=40).to_edge(UP)
        self.play(
            Transform(title, title_complete),
            Transform(stats, stats_complete),
        )
        self.wait(1.0)

        # Highlight one vertex's degree (n−1)
        highlight_vertex = 0
        incident_edges = [e for e in complete_edges if highlight_vertex in e]

        self.play(
            graph.vertices[highlight_vertex].animate.set_fill(YELLOW),
            *[
                graph.edges[e].animate.set_stroke(RED, width=edge_width + 1)
                for e in incident_edges
            ],
            run_time=3.0
        )

        degree_text = MathTex(
            rf"\text{{Vertex }} {highlight_vertex} \text{{ has }} n-1 = {n-1} \text{{ edges}}",
            font_size=32
        ).next_to(stats, UP, buff=0.4)

        self.play(Write(degree_text))
        self.wait(1.0)

        # Restore complete graph style
        self.play(
            graph.vertices[highlight_vertex].animate.set_fill(WHITE),
            *[
                graph.edges[e].animate.set_stroke(WHITE, width=edge_width)
                for e in incident_edges
            ],
            run_time=3.0
        )
        self.play(FadeOut(degree_text), run_time=0.8)
        self.wait(1.0)

        # =========================================
        # PART 2: BIPARTITE → COMPLETE BIPARTITE
        # =========================================

        self.play(
            FadeOut(graph),
            FadeOut(graph_labels),
            FadeOut(stats),   # transformed stats
            FadeOut(title),   # transformed title
            run_time=1.0
        )
        self.wait(1.0)

        left_part = ["A_1", "A_2", "A_3"]
        right_part = ["B_1", "B_2", "B_3", "B_4"]
        vertices_bi = left_part + right_part

        layout_bi = {}
        y_step = 1.3
        for i, v in enumerate(left_part):
            layout_bi[v] = LEFT * 3 + UP * (y_step * (len(left_part) - 1) / 2 - y_step * i)
        for j, v in enumerate(right_part):
            layout_bi[v] = RIGHT * 3 + UP * (y_step * (len(right_part) - 1) / 2 - y_step * j)

        all_bi_pairs = [(u, v) for u in left_part for v in right_part]
        bi_edges = [e for e in all_bi_pairs if random.random() < 0.45]
        if not bi_edges:
            bi_edges.append(all_bi_pairs[0])

        bi_graph = Graph(
            vertices_bi,
            bi_edges,
            layout=layout_bi,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        
        bi_labels = VGroup()
        for v in vertices_bi:
            label = MathTex(v, font_size=18, color=BLACK)
            label.move_to(bi_graph.vertices[v].get_center())
            bi_labels.add(label)

        title_bi = Text("Bipartite Graph", font_size=40).to_edge(UP)
        self.play(Create(bi_graph), Write(title_bi), run_time=1.5)
        self.play(Write(bi_labels), run_time=0.8)
        self.wait(1.0)

        m = len(left_part)
        k = len(right_part)
        total_nodes_bi = len(vertices_bi)
        num_edges_bi = len(bi_edges)

        stats_bi = MathTex(
            rf"m = {m},\ n = {k}",
            r",\quad",
            rf"|V| = {total_nodes_bi}",
            r",\quad",
            rf"|E| = {num_edges_bi}",
            font_size=34
        ).to_corner(DL)
        self.play(Write(stats_bi))
        self.wait(1.0)

        # Complete bipartite
        complete_bi_edges = all_bi_pairs
        new_edges_bi = [e for e in complete_bi_edges if e not in bi_edges]

        _ = smooth_add_edges(
            bi_graph, new_edges_bi, edge_width,
            color=BLUE, lag_ratio=0.12, run_time=5.0
        )

        self.play(
            *[
                edge.animate.set_stroke(WHITE, width=edge_width)
                for edge in bi_graph.edges.values()
            ],
            run_time=3.0
        )

        num_edges_complete_bi = len(complete_bi_edges)
        stats_bi_complete = MathTex(
            rf"m = {m},\ n = {k}",
            r",\quad",
            rf"|V| = {total_nodes_bi}",
            r",\quad",
            rf"|E| = {num_edges_complete_bi} = m \cdot n",
            font_size=34
        ).to_corner(DL)

        title_bi_complete = Text("Complete Bipartite Graph", font_size=40).to_edge(UP)
        self.play(
            Transform(title_bi, title_bi_complete),
            Transform(stats_bi, stats_bi_complete),
        )
        self.wait(1.0)

        # Highlight one node in complete bipartite graph
        highlight_vertex_bi = "A_1"
        incident_edges_bi = [e for e in complete_bi_edges if highlight_vertex_bi in e]

        self.play(
            bi_graph.vertices[highlight_vertex_bi].animate.set_fill(YELLOW),
            *[
                bi_graph.edges[e].animate.set_stroke(RED, width=edge_width + 1)
                for e in incident_edges_bi
            ],
            run_time=1.5
        )

        degree_bi_text = MathTex(
            rf"\text{{Vertex }} A_1 \text{{ has }} n = {k} \text{{ edges}}",
            font_size=32
        ).next_to(stats_bi, UP, buff=0.4)

        self.play(Write(degree_bi_text))
        self.wait(1.0)

        self.play(
            bi_graph.vertices[highlight_vertex_bi].animate.set_fill(WHITE),
            *[
                bi_graph.edges[e].animate.set_stroke(WHITE, width=edge_width)
                for e in incident_edges_bi
            ],
            run_time=3.0
        )
        self.play(FadeOut(degree_bi_text), run_time=0.8)
        self.wait(1.0)

        # Erase bipartite graph & its texts
        self.play(
            FadeOut(bi_graph),
            FadeOut(bi_labels),
            FadeOut(stats_bi),
            FadeOut(title_bi),
            run_time=1.0
        )
        self.wait(1.0)

        # =========================================
        # PART 3: CONNECTED → DISCONNECTED
        # =========================================

        vertices_c = list(range(7))
        edges_c = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6)]
        conn_graph = Graph(
            vertices_c,
            edges_c,
            layout="circular",
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        conn_graph.scale(1.3)
        
        conn_labels = VGroup()
        for v in vertices_c:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(conn_graph.vertices[v].get_center())
            conn_labels.add(label)

        title_conn = Text("Connected Graph", font_size=40).to_edge(UP)
        self.play(Create(conn_graph), Write(title_conn), run_time=1.5)
        self.play(Write(conn_labels), run_time=0.8)
        self.wait(1.0)

        stats_conn = MathTex(
            rf"n = {len(vertices_c)}",
            r",\quad",
            rf"|E| = {len(edges_c)}",
            font_size=34
        ).to_corner(DL)
        self.play(Write(stats_conn))
        self.wait(1.0)

                # Make it disconnected: visually remove a "bridge" edge
        bridge_edge = (2, 3)
        bridge_mob = conn_graph.edges[bridge_edge]

        title_disc = Text("Disconnected Graph", font_size=40).to_edge(UP)
        stats_disc = MathTex(
            rf"n = {len(vertices_c)}",
            r",\quad",
            rf"|E| = {len(edges_c)-1}",
            r",\quad",
            r"\text{graph is disconnected}",
            font_size=32
        ).to_corner(DL)

        # Highlight the bridge first
        self.play(
            bridge_mob.animate.set_stroke(color=RED, width=edge_width + 1),
            run_time=2.0
        )

        # Then make it invisible (instead of a separate FadeOut)
        self.play(
            bridge_mob.animate.set_stroke(opacity=0),
            run_time=3.0
        )

        self.play(
            Transform(title_conn, title_disc),
            Transform(stats_conn, stats_disc),
        )
        self.wait(1.0)

        self.play(
            FadeOut(conn_graph),
            FadeOut(conn_labels),
            FadeOut(title_conn),
            FadeOut(stats_conn),
            run_time=1.0
        )
        self.wait(1.0)

        # =========================================
        # PART 4: DIRECTED → STRONGLY CONNECTED
        # =========================================

        vertices_d = [0, 1, 2, 3]
        dir_edges = [(0, 1), (1, 2), (2, 3)]  # not strongly connected

        # Use Graph with Arrow edges (arrowheads on existing edges)
        digraph = Graph(
            vertices_d,
            dir_edges,
            layout="circular",
            vertex_config=vertex_style,
            edge_config={
                "stroke_color": WHITE,
                "stroke_width": edge_width,
            },
            edge_type=Arrow,  # <-- ensures arrowheads
        )
        digraph.scale(1.3)
        
        digraph_labels = VGroup()
        for v in vertices_d:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(digraph.vertices[v].get_center())
            digraph_labels.add(label)

        title_dir = Text("Directed Graph", font_size=40).to_edge(UP)
        self.play(Create(digraph), Write(title_dir), run_time=1.5)
        self.play(Write(digraph_labels), run_time=0.8)
        self.wait(1.0)

        stats_dir = MathTex(
            rf"n = {len(vertices_d)}",
            r",\quad",
            rf"|E| = {len(dir_edges)}",
            r",\quad",
            r"\text{not strongly connected}",
            font_size=32
        ).to_corner(DL)
        self.play(Write(stats_dir))
        self.wait(1.0)

        # --- Make it strongly connected (NOT complete) ---
        # Add just the edge 3 -> 0 to form the directed cycle 0→1→2→3→0
        new_dir_edges = [(3, 0)]

        # Use the same smooth effect for adding edges
        smooth_add_edges(
            digraph,
            new_dir_edges,
            edge_width,
            color=BLUE,
            lag_ratio=0.12,
            run_time=4.0,
        )

        # Ensure arrowhead is visible on the new edge explicitly
        for e in new_dir_edges:
            edge = digraph.edges[e]
            if hasattr(edge, "add_tip"):
                edge.add_tip()

        # Unify style (all arrows white and same width)
        self.play(
            *[
                edge.animate.set_stroke(WHITE, width=edge_width)
                for edge in digraph.edges.values()
            ],
            run_time=3.0
        )

        stats_dir_sc = MathTex(
            rf"n = {len(vertices_d)}",
            r",\quad",
            rf"|E| = {len(dir_edges) + len(new_dir_edges)} = 4",
            r",\quad",
            r"\text{strongly connected}",
            font_size=32
        ).to_corner(DL)

        title_dir_sc = Text("Strongly Connected Directed Graph", font_size=34).to_edge(UP)

        self.play(
            Transform(title_dir, title_dir_sc),
            Transform(stats_dir, stats_dir_sc),
        )
        self.wait(1.0)

        # 1) FIX TEXT OVERLAP: remove stats before showing the definition
        self.play(FadeOut(stats_dir), run_time=0.8)

        # 2) Show definition with smooth effect, at the bottom
        definition = MathTex(
            r"\text{Strongly connected: for every } u,v,",
            r"\text{ there is a directed path from } u \text{ to } v.",
            font_size=30,
        ).to_edge(DOWN)

        self.play(FadeIn(definition, shift=UP), run_time=1.5)
        self.wait(1.0)
        
        # Clear directed strongly-connected graph before regular example
        self.play(
            FadeOut(digraph),
            FadeOut(digraph_labels),
            FadeOut(title_dir),
            FadeOut(definition),
            run_time=1.0,
        )
        self.wait(0.5)

        # =========================================
        # REGULAR GRAPH (k-regular)
        # =========================================
        vertices_reg = list(range(6))
        edges_reg = [
            (0, 1), (0, 2), (0, 5),
            (1, 2), (1, 3),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 2)
        ]  # mixture forming roughly 3-regular except slight variance; adjust to 3-regular below
        # Adjust to true 3-regular on 6 nodes: use prism graph edges
        vertices_reg = list(range(6))
        edges_reg = [
            (0,1),(1,2),(2,0),  # top triangle
            (3,4),(4,5),(5,3),  # bottom triangle
            (0,3),(1,4),(2,5)   # verticals
        ]  # each vertex degree 3
        layout_reg = {
            0: LEFT * 2 + UP * 1.4,
            1: ORIGIN + UP * 1.8,
            2: RIGHT * 2 + UP * 1.4,
            3: LEFT * 2 + DOWN * 1.4,
            4: ORIGIN + DOWN * 1.8,
            5: RIGHT * 2 + DOWN * 1.4,
        }
        reg_graph = Graph(
            vertices_reg,
            edges_reg,
            layout=layout_reg,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        reg_graph.scale(1.1)
        
        reg_labels = VGroup()
        for v in vertices_reg:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(reg_graph.vertices[v].get_center())
            reg_labels.add(label)
        
        title_reg = Text("Regular Graph (3-regular)", font_size=40).to_edge(UP)
        self.play(Create(reg_graph), Write(title_reg), run_time=1.5)
        self.play(Write(reg_labels), run_time=0.8)
        self.wait(1.0)

        # Show degrees (all should be 3)
        deg_reg = {v: 3 for v in vertices_reg}
        deg_labels_reg = VGroup()
        for v in vertices_reg:
            lbl = MathTex(rf"\deg({v}) = 3", font_size=20, color=GREEN)
            lbl.next_to(reg_graph.vertices[v], UP, buff=0.25)
            deg_labels_reg.add(lbl)
        self.play(Write(deg_labels_reg), run_time=1.2)
        self.wait(1.0)

        reg_note = MathTex(r"\text{k-regular: all vertices have the same degree (here }k=3\text{)}", font_size=26)
        reg_note.to_edge(DOWN, buff=0.7)
        self.play(Write(reg_note), run_time=1.2)
        self.wait(1.0)

        self.play(
            FadeOut(reg_graph),
            FadeOut(reg_labels),
            FadeOut(title_reg),
            FadeOut(deg_labels_reg),
            FadeOut(reg_note),
            run_time=1.0,
        )
        self.wait(0.8)


        # =========================================
        # PART 5: INCIDENCE & ADJACENCY MATRICES
        # =========================================

        # Note: digraph, title_dir, and definition were already faded out before regular graph
        self.wait(1.0)

        # ---- Graph for matrices (undirected) ----
        vertices_m = [1, 2, 3, 4]
        # edges must use canonical ordering (u < v) to match Graph's keys
        edges_m = [(1, 2), (2, 3), (3, 4), (1, 4), (2, 4)]

        layout_m = {
            1: LEFT * 3 + UP * 1.5,
            2: LEFT * 1 + UP * 1.5,
            3: LEFT * 1 + DOWN * 1.5,
            4: LEFT * 3 + DOWN * 1.5,
        }

        matrix_graph = Graph(
            vertices_m,
            edges_m,
            layout=layout_m,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        matrix_graph.scale(1.1)

        title_mat = Text("Incidence Matrix", font_size=36).to_edge(UP)
        
        # Add node labels to the graph
        node_labels_matrix = VGroup()
        for v in vertices_m:
            label = MathTex(f"v_{v}", font_size=24, color=BLACK)
            label.move_to(matrix_graph.vertices[v].get_center())
            node_labels_matrix.add(label)
        
        # Add edge labels to the graph (e1, e2, etc.)
        edge_labels_matrix = VGroup()
        for j, e in enumerate(edges_m):
            # Get the midpoint of the edge
            edge_mob = matrix_graph.edges[e]
            midpoint = edge_mob.get_center()
            # Position label slightly offset from the edge
            label = MathTex(f"e_{j+1}", font_size=20, color=YELLOW)
            # Position label perpendicular to edge, slightly away
            if e == (1, 2):
                label.move_to(midpoint + UP * 0.3)
            elif e == (2, 3):
                label.move_to(midpoint + RIGHT * 0.3)
            elif e == (3, 4):
                label.move_to(midpoint + DOWN * 0.3)
            elif e == (1, 4):
                label.move_to(midpoint + LEFT * 0.3)
            elif e == (2, 4):
                label.move_to(midpoint + DOWN * 0.2 + LEFT * 0.2)
            edge_labels_matrix.add(label)
        
        self.play(Create(matrix_graph), Write(title_mat), run_time=1.5)
        self.play(Write(node_labels_matrix), run_time=1.0)
        self.play(Write(edge_labels_matrix), run_time=1.0)
        self.wait(1.0)

        # -----------------------------------------
        # 5A. Incidence Matrix
        # -----------------------------------------

        # Build incidence matrix: rows = vertices, cols = edges
        incidence_data = []
        for v in vertices_m:
            row = []
            for e in edges_m:
                row.append(1 if v in e else 0)
            incidence_data.append(row)

        # Slightly larger matrix
        inc_matrix = IntegerMatrix(
            incidence_data,
            h_buff=0.6,
            v_buff=0.6,
        )
        inc_matrix.scale(1.1)
        inc_matrix.next_to(matrix_graph, RIGHT, buff=1.5)

        # Row labels: vertices (Y-axis) with extra shift to avoid '[' overlap
        row_labels_inc = VGroup()
        for i, v in enumerate(vertices_m):
            lbl = MathTex(f"v_{v}", font_size=32)
            lbl.next_to(inc_matrix.get_rows()[i], LEFT, buff=0.45)
            lbl.shift(LEFT * 0.35)  # extra push to clear the bracket
            row_labels_inc.add(lbl)

        # Column labels: edges e_1,... (X-axis) – short, to avoid clutter
        col_labels_inc = VGroup()
        for j, e in enumerate(edges_m):
            lbl = MathTex(rf"e_{j+1}", font_size=30)
            lbl.next_to(inc_matrix.get_columns()[j], UP, buff=0.35)
            col_labels_inc.add(lbl)

        # Legend for which edge is which (so column labels stay short)
        edge_legend_items = VGroup()
        for j, e in enumerate(edges_m):
            leg = MathTex(
                rf"e_{j+1} = ({e[0]}, {e[1]})",
                font_size=26
            )
            edge_legend_items.add(leg)
        edge_legend = VGroup(*edge_legend_items).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        edge_legend.next_to(matrix_graph, DOWN, buff=0.6)

        inc_title = MathTex(
            r"I(G) \in \{0,1\}^{|V|\times|E|}",
            font_size=32
        ).next_to(inc_matrix, DOWN, buff=0.4)

        self.play(
            Write(inc_matrix),
            Write(row_labels_inc),
            Write(col_labels_inc),
            FadeIn(edge_legend, shift=UP),
            FadeIn(inc_title, shift=UP),
            run_time=2.0
        )
        self.wait(1.0)

        # Map entries (i,j) → mobjects for highlighting
        inc_entries = []
        entries_group = inc_matrix.get_entries()
        num_rows_inc = len(vertices_m)
        num_cols_inc = len(edges_m)
        for i in range(num_rows_inc):
            row_entries = []
            for j in range(num_cols_inc):
                idx = i * num_cols_inc + j
                row_entries.append(entries_group[idx])
            inc_entries.append(row_entries)

        # Highlight each 1 in the incidence matrix with:
        # - the vertex
        # - the edge
        # - the row label (vertex label, Y-axis)
        # - the column label (edge label, X-axis)
        for i, v in enumerate(vertices_m):
            for j, e in enumerate(edges_m):
                if incidence_data[i][j] == 1:
                    cell = inc_entries[i][j]
                    vertex_mob = matrix_graph.vertices[v]
                    edge_mob = matrix_graph.edges[e]
                    row_label = row_labels_inc[i]
                    col_label = col_labels_inc[j]

                    # Find corresponding edge label
                    edge_label_idx = edges_m.index(e)
                    edge_label_mob = edge_labels_matrix[edge_label_idx] if edge_label_idx < len(edge_labels_matrix) else None
                    
                    anims = [
                        cell.animate.set_color(RED),
                        row_label.animate.set_color(RED),
                        col_label.animate.set_color(RED),
                        vertex_mob.animate.set_fill(RED),
                        edge_mob.animate.set_stroke(RED, width=edge_width + 1),
                    ]
                    if edge_label_mob:
                        anims.append(edge_label_mob.animate.set_color(RED))
                    
                    self.play(*anims, run_time=1.2)
                    
                    anims_reset = [
                        cell.animate.set_color(WHITE),
                        row_label.animate.set_color(WHITE),
                        col_label.animate.set_color(WHITE),
                        vertex_mob.animate.set_fill(WHITE),
                        edge_mob.animate.set_stroke(WHITE, width=edge_width),
                    ]
                    if edge_label_mob:
                        anims_reset.append(edge_label_mob.animate.set_color(YELLOW))
                    
                    self.play(*anims_reset, run_time=0.8)

        self.wait(1.0)

        # -----------------------------------------
        # 5B. Adjacency Matrix
        # -----------------------------------------

        # Fade out incidence matrix and labels, change title to Adjacency Matrix
        title_adj = Text("Adjacency Matrix", font_size=36).to_edge(UP)
        self.play(
            FadeOut(inc_matrix),
            FadeOut(row_labels_inc),
            FadeOut(col_labels_inc),
            FadeOut(edge_legend),
            FadeOut(inc_title),
            FadeOut(edge_labels_matrix),  # Remove edge labels for adjacency matrix
            Transform(title_mat, title_adj),
            run_time=1.0
        )
        # Keep node labels for adjacency matrix
        self.wait(1.0)

        # Build adjacency matrix A(G)
        n_m = len(vertices_m)
        adjacency_data = []
        # helper to check edge presence (undirected)
        existing_edges = set((min(u, v), max(u, v)) for (u, v) in edges_m)

        for i, u in enumerate(vertices_m):
            row = []
            for j, v in enumerate(vertices_m):
                if i == j:
                    row.append(0)  # no loops
                else:
                    key = (min(u, v), max(u, v))
                    row.append(1 if key in existing_edges else 0)
            adjacency_data.append(row)

        # Slightly larger adjacency matrix
        adj_matrix = IntegerMatrix(
            adjacency_data,
            h_buff=0.6,
            v_buff=0.6,
        )
        adj_matrix.scale(1.1)
        adj_matrix.next_to(matrix_graph, RIGHT, buff=1.5)

        # Row & column labels: vertices (X and Y axes)
        row_labels_adj = VGroup()
        col_labels_adj = VGroup()

        for i, v in enumerate(vertices_m):
            r_lbl = MathTex(f"v_{v}", font_size=32)
            r_lbl.next_to(adj_matrix.get_rows()[i], LEFT, buff=0.45)
            r_lbl.shift(LEFT * 0.35)  # avoid '[' overlap
            row_labels_adj.add(r_lbl)

        for j, v in enumerate(vertices_m):
            c_lbl = MathTex(f"v_{v}", font_size=32)
            c_lbl.next_to(adj_matrix.get_columns()[j], UP, buff=0.35)
            col_labels_adj.add(c_lbl)

        adj_title = MathTex(
            r"A(G) \in \{0,1\}^{|V|\times|V|}",
            font_size=32
        ).next_to(adj_matrix, DOWN, buff=0.4)

        self.play(
            Write(adj_matrix),
            Write(row_labels_adj),
            Write(col_labels_adj),
            FadeIn(adj_title, shift=UP),
            run_time=2.0
        )
        self.wait(1.0)

        # --- Explanation under the adjacency matrix (stays during highlighting) ---
        adj_explanation = MathTex(
            r"A_{ij} = 1 \iff \{v_i, v_j\} \in E(G)",
            font_size=30
        )
        adj_explanation.next_to(adj_title, DOWN, buff=0.3)

        self.play(Write(adj_explanation), run_time=3.0)

        # Map adjacency entries for highlighting
        adj_entries = []
        entries_group_adj = adj_matrix.get_entries()
        num_rows_adj = n_m
        num_cols_adj = n_m
        for i in range(num_rows_adj):
            row_entries = []
            for j in range(num_cols_adj):
                idx = i * num_cols_adj + j
                row_entries.append(entries_group_adj[idx])
            adj_entries.append(row_entries)

        # Highlight each 1 = edge between v_i and v_j, with:
        # - cell A_ij
        # - row label (v_i)
        # - column label (v_j)
        # - both vertices in the graph
        # - corresponding edge in the graph
        for i, u in enumerate(vertices_m):
            for j, v in enumerate(vertices_m):
                if adjacency_data[i][j] == 1:
                    cell = adj_entries[i][j]

                    key = (min(u, v), max(u, v))
                    edge_mob = matrix_graph.edges[key]
                    vertex_u = matrix_graph.vertices[u]
                    vertex_v = matrix_graph.vertices[v]
                    row_label = row_labels_adj[i]
                    col_label = col_labels_adj[j]

                    # Find corresponding node labels
                    node_label_u = node_labels_matrix[vertices_m.index(u)] if u in vertices_m else None
                    node_label_v = node_labels_matrix[vertices_m.index(v)] if v in vertices_m else None
                    
                    anims = [
                        cell.animate.set_color(RED),
                        row_label.animate.set_color(RED),
                        col_label.animate.set_color(RED),
                        vertex_u.animate.set_fill(RED),
                        vertex_v.animate.set_fill(RED),
                        edge_mob.animate.set_stroke(RED, width=edge_width + 1),
                    ]
                    if node_label_u:
                        anims.append(node_label_u.animate.set_color(RED))
                    if node_label_v:
                        anims.append(node_label_v.animate.set_color(RED))
                    
                    self.play(*anims, run_time=1.2)
                    
                    anims_reset = [
                        cell.animate.set_color(WHITE),
                        row_label.animate.set_color(WHITE),
                        col_label.animate.set_color(WHITE),
                        vertex_u.animate.set_fill(WHITE),
                        vertex_v.animate.set_fill(WHITE),
                        edge_mob.animate.set_stroke(WHITE, width=edge_width),
                    ]
                    if node_label_u:
                        anims_reset.append(node_label_u.animate.set_color(BLACK))
                    if node_label_v:
                        anims_reset.append(node_label_v.animate.set_color(BLACK))
                    
                    self.play(*anims_reset, run_time=0.8)

        self.wait(1.0)
        
        # ============================================================
        # Edge List and Adjacency List + Subgraph
        # ============================================================
        # Fade out adjacency matrix elements, keep graph and node labels
        self.play(
            FadeOut(adj_matrix),
            FadeOut(row_labels_adj),
            FadeOut(col_labels_adj),
            FadeOut(adj_title),
            FadeOut(adj_explanation),
            run_time=1.0
        )
        self.wait(1)
        
        # Show edge list and adjacency list for the current graph (matrix_graph)
        list_title = Text("Edge List & Adjacency List", font_size=36).to_edge(UP)
        self.play(Transform(title_mat, list_title), run_time=1.2)
        self.wait(1)
        
        # Update node labels to show numbers instead of v_1, v_2, etc.
        # Remove old labels and add new ones
        self.play(FadeOut(node_labels_matrix), run_time=0.5)
        node_labels = VGroup()
        for v in vertices_m:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(matrix_graph.vertices[v].get_center())
            node_labels.add(label)
        self.play(Write(node_labels), run_time=1.5)
        self.wait(1)

        # Edge list text - positioned to the right of the graph
        edge_list_str = ", ".join([f"({u},{v})" for (u, v) in edges_m])
        edge_list_tex = MathTex(
            rf"\text{{Edge list: }} {edge_list_str}",
            font_size=24,
        )
        # Position to the right of the graph, at the top
        edge_list_tex.next_to(matrix_graph, RIGHT, buff=1.0).shift(UP * 1.5)
        self.play(Write(edge_list_tex), run_time=1.5)

        # Build adjacency list from edges_m
        adj_list = {v: [] for v in vertices_m}
        for (u, v) in edges_m:
            adj_list[u].append(v)
            adj_list[v].append(u)
        for v in adj_list:
            adj_list[v] = sorted(adj_list[v])

        adj_list_rows = VGroup()
        for i, v in enumerate(vertices_m):
            neighbors_str = ", ".join(str(n) for n in adj_list[v]) if adj_list[v] else "-"
            row_tex = MathTex(
                rf"\text{{Adj}}({v}) : " + neighbors_str,
                font_size=22,
            )
            if i == 0:
                # Position below edge list, aligned to the right
                row_tex.next_to(edge_list_tex, DOWN, buff=0.4).align_to(edge_list_tex, LEFT)
            else:
                row_tex.next_to(adj_list_rows[-1], DOWN, buff=0.25).align_to(adj_list_rows[-1], LEFT)
            adj_list_rows.add(row_tex)

        self.play(Write(adj_list_rows), run_time=2.0)
        self.wait(1)

        # Clear textual lists, keep the graph and labels
        self.play(FadeOut(edge_list_tex), FadeOut(adj_list_rows), run_time=1.0)
        self.wait(1)

        # Highlight a subgraph to define the concept
        sub_vertices = [1, 2, 4]
        sub_edges = [
            e for e in edges_m if (e[0] in sub_vertices and e[1] in sub_vertices)
        ]

        # Dim non-subgraph vertices slightly
        self.play(
            *[
                matrix_graph.vertices[v].animate.set_fill(GRAY if v not in sub_vertices else WHITE)
                for v in vertices_m
            ],
            run_time=1.0,
        )

        # Emphasize subgraph vertices and edges
        self.play(
            *[
                matrix_graph.vertices[v].animate.set_fill(YELLOW)
                for v in sub_vertices
            ],
            *[
                matrix_graph.edges[e].animate.set_stroke(GREEN, width=edge_width + 1)
                for e in sub_edges
            ],
            run_time=1.5,
        )
        subgraph_label = MathTex(
            r"\text{Colored part is a subgraph of the original graph}",
            font_size=26,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(subgraph_label), run_time=1.5)
        self.wait(1)
        
        # ============================================================
        # Summary
        # ============================================================
        # Clear final scene elements (adjacency matrix elements already faded out earlier)
        self.play(
            FadeOut(matrix_graph),
            FadeOut(node_labels),
            FadeOut(title_mat),
            FadeOut(subgraph_label),
            run_time=1.5
        )
        self.wait(1)
        
        summary_title = Text("Summary", font_size=48)
        self.play(FadeIn(summary_title, shift=UP * 0.5), run_time=1.5)
        self.wait(1)
        self.play(summary_title.animate.to_edge(UP), run_time=1.2)
        
        summary_points = VGroup(
            MathTex(r"\text{Walk / Trail / Circuit / Path / Cycle: traversal basics}", font_size=26),
            MathTex(r"\text{Complete Graph: all vertices connected } (|E| = \frac{n(n-1)}{2})", font_size=26),
            MathTex(r"\text{Complete Bipartite: all cross-edges between partitions } (|E| = m \cdot n)", font_size=26),
            MathTex(r"\text{Connected vs Disconnected: path exists between all pairs}", font_size=26),
            MathTex(r"\text{Strongly Connected: directed paths between all pairs}", font_size=26),
            MathTex(r"\text{Incidence Matrix: rows = vertices, columns = edges}", font_size=26),
            MathTex(r"\text{Adjacency Matrix: } A_{ij} = 1 \text{ if edge exists between } v_i \text{ and } v_j", font_size=26),
            MathTex(r"\text{Edge list and adjacency list encode the same graph in list form}", font_size=26),
            MathTex(r"\text{Subgraph: a graph formed from a subset of vertices and edges}", font_size=26),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.6)
        self.play(Write(summary_points), run_time=4.5)
        self.wait(1)
        
        self.play(
            FadeOut(summary_title), FadeOut(summary_points),
            run_time=1.5
        )
        self.wait(1)
