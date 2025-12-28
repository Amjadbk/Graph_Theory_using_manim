from manim import *


class HamiltonConcepts(Scene):
    def construct(self):
        edge_width = 3
        vertex_style = {
            "radius": 0.14,
            "fill_color": WHITE,
            "stroke_color": WHITE,
            "stroke_width": 2,
        }
        edge_style = {
            "stroke_color": WHITE,
            "stroke_width": edge_width,
        }

        def animate_path(graph, path_vertices, color=YELLOW, close_cycle=False):
            """Animate a Hamilton path/cycle as a moving dot plus edge highlighting."""
            if len(path_vertices) < 2:
                return

            # Optionally close the cycle by returning to the start
            if close_cycle and path_vertices[0] != path_vertices[-1]:
                path_vertices = list(path_vertices) + [path_vertices[0]]

            dot = Dot(radius=0.12, color=color)
            dot.move_to(graph.vertices[path_vertices[0]].get_center())
            self.add(dot)

            edges_used = []
            for i in range(len(path_vertices) - 1):
                u = path_vertices[i]
                v = path_vertices[i + 1]
                # undirected edges stored as sorted tuples
                key = (u, v) if (u, v) in graph.edges else (v, u)
                if key not in graph.edges:
                    continue
                edges_used.append(key)
                target = graph.vertices[v].get_center()
                self.play(dot.animate.move_to(target), run_time=0.7)

            # highlight edges
            uniq_edges = list(dict.fromkeys(edges_used))
            if uniq_edges:
                self.play(
                    *[
                        graph.edges[e].animate.set_stroke(color=color, width=edge_width + 1)
                        for e in uniq_edges
                    ],
                    run_time=1.5,
                )
                self.wait(1)
                self.play(
                    *[
                        graph.edges[e].animate.set_stroke(WHITE, width=edge_width)
                        for e in uniq_edges
                    ],
                    run_time=1.0,
                )

            self.play(FadeOut(dot), run_time=0.4)

        # Base Hamiltonian graph used in many prompts (hexagon with chords)
        vertices = [1, 2, 3, 4, 5, 6]
        edges = [
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 1),  # 6-cycle
            (1, 4),
            (2, 5),
            (3, 6),  # chords
        ]
        layout = {
            1: LEFT * 3 + UP * 1.5,
            2: LEFT * 1 + UP * 2.2,
            3: RIGHT * 1 + UP * 2.2,
            4: RIGHT * 3 + UP * 1.5,
            5: RIGHT * 2 + DOWN * 1.8,
            6: LEFT * 2 + DOWN * 1.8,
        }

        base_graph = Graph(
            vertices,
            edges,
            layout=layout,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        base_graph.scale(0.95)

        # ============================================================
        # Introduction
        # ============================================================
        intro_title = Text("Graph Theory – Hamiltonian Path and Cycle", font_size=48)
        self.play(FadeIn(intro_title, shift=UP * 0.5), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(intro_title, shift=UP * 0.5), run_time=0.8)

        # ============================================================
        # Prompt 9: Hamilton Path (visits every vertex exactly once)
        # ============================================================
        title = Text("Hamilton Path", font_size=40).to_edge(UP)
        desc = MathTex(
            r"\text{Visits every vertex exactly once,}",
            r"\text{ does not return to the start.}",
            font_size=28,
        ).next_to(title, DOWN, buff=0.3)

        self.play(Create(base_graph), Write(title), run_time=1.5)
        self.play(Write(desc), run_time=1.2)
        self.wait(1)

        ham_path = [1, 2, 3, 4, 5, 6]  # open Hamilton path
        path_label = MathTex(
            r"1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 5 \rightarrow 6",
            font_size=26,
        ).to_corner(DL)
        self.play(Write(path_label), run_time=1.0)
        self.wait(1)

        animate_path(base_graph, ham_path, color=YELLOW, close_cycle=False)
        self.wait(1)

        self.play(FadeOut(desc), FadeOut(path_label), run_time=0.8)

        # ============================================================
        # Prompt 10: Hamilton Cycle
        # ============================================================
        title_cycle = Text("Hamilton Cycle", font_size=40).to_edge(UP)
        desc_cycle = MathTex(
            r"\text{Visits every vertex exactly once}",
            r"\text{ and returns to the start.}",
            font_size=28,
        ).next_to(title_cycle, DOWN, buff=0.3)

        self.play(Transform(title, title_cycle), Write(desc_cycle), run_time=1.5)
        self.wait(1)

        ham_cycle = [1, 2, 3, 4, 5, 6]  # will be closed back to 1
        cycle_label = MathTex(
            r"1 \rightarrow 2 \rightarrow 3 \rightarrow 4 \rightarrow 5 \rightarrow 6 \rightarrow 1",
            font_size=26,
        ).to_corner(DL)
        self.play(Write(cycle_label), run_time=1.0)
        self.wait(1)

        animate_path(base_graph, ham_cycle, color=ORANGE, close_cycle=True)
        self.wait(1)

        self.play(FadeOut(desc_cycle), FadeOut(cycle_label), run_time=0.8)

        # ============================================================
        # Prompt 11: Hamiltonian Graph
        # ============================================================
        title_hg = Text("Hamiltonian Graph", font_size=40).to_edge(UP)
        self.play(Transform(title, title_hg), run_time=1.0)

        hg_text = MathTex(
            r"\text{This graph is Hamiltonian:}",
            r"\text{ it has a Hamilton path and a Hamilton cycle.}",
            font_size=28,
        ).next_to(title_hg, DOWN, buff=0.3)
        self.play(Write(hg_text), run_time=1.0)

        # briefly highlight the Hamilton cycle again
        cycle_edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (1, 6)]
        self.play(
            *[
                base_graph.edges[
                    (u, v) if (u, v) in base_graph.edges else (v, u)
                ].animate.set_stroke(GREEN, width=edge_width + 1)
                for (u, v) in cycle_edges
            ],
            run_time=1.5,
        )
        self.wait(1)
        self.play(
            *[
                base_graph.edges[
                    (u, v) if (u, v) in base_graph.edges else (v, u)
                ].animate.set_stroke(WHITE, width=edge_width)
                for (u, v) in cycle_edges
            ],
            run_time=1.0,
        )
        self.wait(1)

        self.play(FadeOut(base_graph), FadeOut(title), FadeOut(hg_text), run_time=1.0)
        self.wait(1)

        # Add shelby.jpg image before Ore's theorem
        try:
            shelby_img = ImageMobject("assets/shelby.jpg")
            shelby_img.scale(1.5)
            shelby_img.move_to(ORIGIN)
            self.play(FadeIn(shelby_img), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(shelby_img), run_time=1.0)
        except:
            # If image not found, show a placeholder text
            shelby_text = Text("🖼️ SHELBY 🖼️", font_size=64, color=YELLOW)
            self.play(FadeIn(shelby_text), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(shelby_text), run_time=1.0)

        # ============================================================
        # Prompt 12: Ore's Theorem
        # ============================================================
        # Use n = 6, graph satisfying Ore: K6 minus one edge (1,4)
        ore_vertices = [1, 2, 3, 4, 5, 6]
        ore_edges = [
            (1, 2),
            (1, 3),
            (1, 5),
            (1, 6),
            (2, 3),
            (2, 4),
            (2, 5),
            (2, 6),
            (3, 4),
            (3, 5),
            (3, 6),
            (4, 5),
            (4, 6),
            (5, 6),
        ]  # complete graph except missing (1,4)

        ore_layout = {
            1: LEFT * 3 + UP * 1.8,
            2: LEFT * 1 + UP * 2.4,
            3: RIGHT * 1 + UP * 2.4,
            4: RIGHT * 3 + UP * 1.8,
            5: RIGHT * 2 + DOWN * 1.8,
            6: LEFT * 2 + DOWN * 1.8,
        }

        ore_graph = Graph(
            ore_vertices,
            ore_edges,
            layout=ore_layout,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        ore_graph.scale(0.9)

        title_ore = Text("Ore's Theorem", font_size=40).to_edge(UP)
        desc_ore = MathTex(
            r"\text{If for every non-adjacent } u,v: \deg(u)+\deg(v)\ge n,",
            r"\text{ then the graph is Hamiltonian.}",
            font_size=26,
        ).next_to(title_ore, DOWN, buff=0.3)

        self.play(Create(ore_graph), Write(title_ore), run_time=1.5)
        self.play(Write(desc_ore), run_time=1.2)
        self.wait(1)

        # Non-adjacent pair: (1,4)
        u, v = 1, 4
        deg = {x: sum(1 for e in ore_edges if x in e) for x in ore_vertices}
        pair_circle = VGroup(
            ore_graph.vertices[u].copy().set_fill(YELLOW, opacity=0.5),
            ore_graph.vertices[v].copy().set_fill(YELLOW, opacity=0.5),
        )
        self.play(FadeIn(pair_circle, scale=1.2), run_time=0.8)

        ore_text_pair = MathTex(
            rf"\deg({u}) = {deg[u]},\ \deg({v}) = {deg[v]},\ "
            rf"\deg({u}) + \deg({v}) = {deg[u] + deg[v]} \ge n = 6",
            font_size=26,
        ).to_corner(DL)
        self.play(Write(ore_text_pair), run_time=1.0)
        self.wait(1)

        self.play(FadeOut(pair_circle), run_time=0.6)
        self.wait(1)

        self.play(
            FadeOut(ore_graph),
            FadeOut(title_ore),
            FadeOut(desc_ore),
            FadeOut(ore_text_pair),
            run_time=1.0,
        )
        self.wait(1)

        # ============================================================
        # Prompt 13: Dirac’s Theorem
        # ============================================================
        # Graph on n=6 with minimum degree >= n/2 = 3
        dirac_vertices = [1, 2, 3, 4, 5, 6]
        dirac_edges = [
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 3),
            (2, 5),
            (3, 6),
            (4, 5),
            (4, 6),
            (5, 6),
        ]

        dirac_layout = ore_layout  # reuse hex layout
        dirac_graph = Graph(
            dirac_vertices,
            dirac_edges,
            layout=dirac_layout,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        dirac_graph.scale(0.9)

        title_dirac = Text("Dirac's Theorem", font_size=40).to_edge(UP)
        desc_dirac = MathTex(
            r"\text{If every vertex has } \deg(v) \ge \frac{n}{2},",
            r"\text{ then the graph has a Hamiltonian cycle.}",
            font_size=26,
        ).next_to(title_dirac, DOWN, buff=0.3)

        self.play(Create(dirac_graph), Write(title_dirac), run_time=1.5)
        self.play(Write(desc_dirac), run_time=1.2)
        self.wait(1)

        deg_d = {x: sum(1 for e in dirac_edges if x in e) for x in dirac_vertices}
        n = len(dirac_vertices)
        min_deg = min(deg_d.values())

        deg_text_dirac = MathTex(
            rf"n = {n},\ \frac{{n}}{{2}} = {n/2},\ "
            rf"\min_v \deg(v) = {min_deg} \ge \frac{{n}}{{2}}",
            font_size=26,
        ).to_corner(DL)
        self.play(Write(deg_text_dirac), run_time=1.0)
        self.wait(1)

        # highlight all vertices once to show degrees
        for vtx in dirac_vertices:
            incident = [e for e in dirac_edges if vtx in e]
            self.play(
                dirac_graph.vertices[vtx].animate.set_fill(YELLOW),
                *[
                    dirac_graph.edges[e].animate.set_stroke(
                        YELLOW, width=edge_width + 1
                    )
                    for e in incident
                ],
                run_time=0.8,
            )
            self.wait(1)
            self.play(
                dirac_graph.vertices[vtx].animate.set_fill(WHITE),
                *[
                    dirac_graph.edges[e].animate.set_stroke(WHITE, width=edge_width)
                    for e in incident
                ],
                run_time=0.6,
            )

        self.wait(1)

        self.play(
            FadeOut(dirac_graph),
            FadeOut(title_dirac),
            FadeOut(desc_dirac),
            FadeOut(deg_text_dirac),
            run_time=1.0,
        )
        self.wait(1)

        # ============================================================
        # Prompt 14: Algorithm Types (Backtracking vs Heuristics)
        # ============================================================
        title_alg = Text("Algorithm Types for Hamiltonian Cycles", font_size=34).to_edge(
            UP
        )
        self.play(Write(title_alg), run_time=1.2)

        # Two panels side-by-side
        left_box = Rectangle(width=5.5, height=4, color=BLUE_D).shift(LEFT * 3)
        right_box = Rectangle(width=5.5, height=4, color=GREEN_D).shift(RIGHT * 3)
        left_title = Text("Backtracking", font_size=30).next_to(
            left_box.get_top(), DOWN, buff=0.2
        )
        right_title = Text("Heuristics", font_size=30).next_to(
            right_box.get_top(), DOWN, buff=0.2
        )

        self.play(Create(left_box), Create(right_box), run_time=1.0)
        self.play(Write(left_title), Write(right_title), run_time=1.0)

        backtrack_bullets = VGroup(
            Text("Systematically explores", font_size=22),
            Text("Backtracks on dead ends", font_size=22),
            Text("Guarantees correctness", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        backtrack_bullets.next_to(left_title, DOWN, buff=0.3)

        heuristic_bullets = VGroup(
            Text("Greedy / local choices", font_size=22),
            Text("Faster in practice", font_size=22),
            Text("No guarantee of success", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        heuristic_bullets.next_to(right_title, DOWN, buff=0.3)

        self.play(Write(backtrack_bullets), Write(heuristic_bullets), run_time=1.5)
        self.wait(1)

        self.play(
            FadeOut(left_box),
            FadeOut(right_box),
            FadeOut(left_title),
            FadeOut(right_title),
            FadeOut(backtrack_bullets),
            FadeOut(heuristic_bullets),
            FadeOut(title_alg),
            run_time=1.0,
        )
        self.wait(1)

        # ============================================================
        # Prompt 15–18: Backtracking Algorithm Visualization
        # ============================================================
        # Use a small 5-vertex graph for the algorithm demo
        # Graph designed so 1->2->3->4->5 hits a dead end at 5,
        # then backtrack to find 1->2->3->5->4->1
        v_alg = [1, 2, 3, 4, 5]
        e_alg = [
            (1, 2),
            (2, 3),
            (3, 4),  # First path: 1->2->3->4->5 (dead end at 5)
            (4, 5),  # Edge from 4 to 5
            (3, 5),  # Alternative path that works: 1->2->3->5->4->1
            (5, 4),  # Edge from 5 to 4 (for the successful path)
            (4, 1),  # Edge from 4 to 1 (to complete the cycle)
        ]
        lay_alg = {
            1: UP * 2,
            2: LEFT * 2,
            3: ORIGIN,
            4: RIGHT * 2,
            5: DOWN * 2,
        }

        alg_graph = Graph(
            v_alg,
            e_alg,
            layout=lay_alg,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        alg_graph.scale(0.9)

        # ============================================================
        # Backtracking Algorithm Steps (shown BEFORE graph)
        # ============================================================
        backtrack_algo_title = Text("Backtracking Algorithm", font_size=40).to_edge(UP)
        self.play(Write(backtrack_algo_title), run_time=1.2)
        
        backtrack_algo_text = VGroup(
            MathTex(r"\text{1. Start with initial vertex in path.}", font_size=24),
            MathTex(r"\text{2. Try adding an unvisited neighbor to path.}", font_size=24),
            MathTex(r"\text{3. If path includes all vertices and forms cycle: success!}", font_size=24),
            MathTex(r"\text{4. If dead end reached: backtrack (remove last vertex).}", font_size=24),
            MathTex(r"\text{5. Try next unvisited neighbor.}", font_size=24),
            MathTex(r"\text{6. Repeat until cycle found or all possibilities exhausted.}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        backtrack_algo_text.next_to(backtrack_algo_title, DOWN, buff=0.4)
        self.play(Write(backtrack_algo_text), run_time=3.75)
        self.wait(1)
        
        self.play(
            FadeOut(backtrack_algo_title), FadeOut(backtrack_algo_text),
            run_time=1.2
        )

        # Add node labels like in dfs.py
        alg_node_labels = VGroup()
        label_dict = {}  # Map vertex number to label mobject
        for v in v_alg:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(alg_graph.vertices[v].get_center())
            alg_node_labels.add(label)
            label_dict[v] = label

        title_bt = Text("Backtracking for Hamiltonian Cycle", font_size=34).to_edge(UP)
        self.play(Create(alg_graph), Write(alg_node_labels), Write(title_bt), run_time=1.5)
        self.wait(1)

        # Stack visualization setup - matching dfs.py style
        stack_label = MathTex(r"\text{Path Stack}", font_size=22)
        stack_label.to_edge(LEFT, buff=0.4).shift(UP * 1.8)
        
        stack_container = Rectangle(
            width=2.2,
            height=3.2,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_opacity=0.05,
            fill_color=BLUE
        )
        stack_container.next_to(stack_label, DOWN, buff=0.25)
        stack_container.align_to(stack_label, LEFT)
        
        stack_inner = Rectangle(
            width=2.0,
            height=3.0,
            stroke_color=BLUE,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        stack_inner.move_to(stack_container.get_center())
        
        self.play(
            Write(stack_label),
            Create(stack_container),
            Create(stack_inner),
            run_time=1.8
        )
        self.wait(1)

        # Visited set visualization
        visited_label = MathTex(r"\text{Visited:}", font_size=18)
        visited_label.next_to(stack_container, DOWN, buff=0.3)
        visited_label.align_to(stack_label, LEFT)
        
        self.play(Write(visited_label), run_time=0.5)
        self.wait(1)

        # Status text at bottom
        status_text = MathTex(
            r"\text{Status:}", font_size=20
        ).to_edge(DOWN, buff=0.3).shift(LEFT * 2)
        
        self.play(Write(status_text), run_time=0.5)
        self.wait(1)

        # Prompt 15: Initialization
        start_v = 1
        path = [start_v]
        visited_set = {start_v}
        stack_items = VGroup()
        visited_items = VGroup()
        current_path_edges = []

        # Initialize: highlight start vertex
        self.play(
            alg_graph.vertices[start_v].animate.set_fill(YELLOW),
            label_dict[start_v].animate.set_color(BLACK),
            run_time=1.0,
        )
        
        # Add start to stack
        stack_item = Rectangle(
            width=1.9,
            height=0.4,
            stroke_color=BLUE,
            stroke_width=1.5,
            fill_color=BLUE,
            fill_opacity=0.3,
        )
        stack_text = MathTex(str(start_v), font_size=16, color=WHITE)
        stack_text.move_to(stack_item.get_center())
        stack_item_group = VGroup(stack_item, stack_text)
        stack_item_group.next_to(stack_container.get_bottom(), UP, buff=0.15)
        stack_item_group.align_to(stack_container, LEFT).shift(RIGHT * 0.15)
        stack_items.add(stack_item_group)
        self.add(stack_item_group)
        self.play(FadeIn(stack_item_group, shift=DOWN * 0.15), run_time=0.7)
        
        # Add to visited
        visited_item = MathTex(str(start_v), font_size=16, color=BLUE)
        visited_item.next_to(visited_label, DOWN, buff=0.2)
        visited_item.align_to(visited_label, LEFT).shift(RIGHT * 0.3)
        visited_items.add(visited_item)
        self.add(visited_item)
        self.play(FadeIn(visited_item, scale=0.9), run_time=0.5)
        
        self.wait(1)

        # Helper function to get edge key (handle both directions)
        def get_edge_key(u, v):
            key1 = (u, v)
            key2 = (v, u)
            if key1 in alg_graph.edges:
                return key1
            elif key2 in alg_graph.edges:
                return key2
            else:
                # Return canonical form as fallback
                return (min(u, v), max(u, v))

        # Helper function to update status
        # Only show a few key messages to avoid clutter:
        # - "Exploring..."
        # - "Dead end"
        # - "Backtracking..."
        # - "Hamiltonian cycle found"
        def update_status(msg):
            # Decide which short message to show
            if "Exploring" in msg:
                display = "Exploring..."
            elif "Dead end" in msg or "no edge" in msg:
                display = "Dead end"
            elif "Backtracking" in msg:
                display = "Backtracking..."
            # Only treat messages that explicitly say the cycle was found
            elif "Hamiltonian cycle found" in msg or "cycle found" in msg:
                display = "Hamiltonian cycle found"
            else:
                # Ignore less important / verbose messages
                return

            new_status = MathTex(rf"\text{{Status: {display}}}", font_size=20)
            new_status.move_to(status_text.get_center())
            self.play(Transform(status_text, new_status), run_time=0.5)

        # Helper function to push to stack
        def push_to_stack(vertex):
            stack_item = Rectangle(
                width=1.9,
                height=0.4,
                stroke_color=BLUE,
                stroke_width=1.5,
                fill_color=BLUE,
                fill_opacity=0.3,
            )
            stack_text = MathTex(str(vertex), font_size=16, color=WHITE)
            stack_text.move_to(stack_item.get_center())
            stack_item_group = VGroup(stack_item, stack_text)
            if len(stack_items) == 0:
                stack_item_group.next_to(stack_container.get_bottom(), UP, buff=0.15)
                stack_item_group.align_to(stack_container, LEFT).shift(RIGHT * 0.15)
            else:
                stack_item_group.next_to(stack_items[-1], UP, buff=0.08)
                stack_item_group.align_to(stack_items[-1], LEFT)
            stack_items.add(stack_item_group)
            self.add(stack_item_group)
            self.play(FadeIn(stack_item_group, shift=DOWN * 0.15), run_time=0.7)
            return stack_item_group

        # Helper function to pop from stack
        def pop_from_stack():
            if len(stack_items) > 0:
                item_to_remove = stack_items[-1]
                stack_items.remove(item_to_remove)
                self.play(FadeOut(item_to_remove, shift=UP * 0.2), run_time=0.6)
                self.remove(item_to_remove)
                return True
            return False

        # Prompt 16: Backtracking Process
        update_status("Exploring path...")
        self.wait(1)

        # Step 1: Try 1 -> 2
        next_v = 2
        edge_key = get_edge_key(start_v, next_v)
        path.append(next_v)
        visited_set.add(next_v)
        current_path_edges.append(edge_key)
        
        self.play(
            alg_graph.vertices[next_v].animate.set_fill(YELLOW),
            label_dict[next_v].animate.set_color(BLACK),
            alg_graph.edges[edge_key].animate.set_stroke(ORANGE, width=edge_width + 1),
            run_time=1.0,
        )
        push_to_stack(next_v)
        visited_item = MathTex(str(next_v), font_size=16, color=BLUE)
        if len(visited_items) > 0:
            visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
            visited_item.align_to(visited_items[-1], DOWN)
        visited_items.add(visited_item)
        self.add(visited_item)
        self.play(FadeIn(visited_item, scale=0.9), run_time=0.5)
        self.wait(1)

        # Step 2: Try 2 -> 3
        prev_v = next_v
        next_v = 3
        edge_key = get_edge_key(prev_v, next_v)
        path.append(next_v)
        visited_set.add(next_v)
        current_path_edges.append(edge_key)
        
        self.play(
            alg_graph.vertices[next_v].animate.set_fill(YELLOW),
            label_dict[next_v].animate.set_color(BLACK),
            alg_graph.edges[edge_key].animate.set_stroke(ORANGE, width=edge_width + 1),
            run_time=1.0,
        )
        push_to_stack(next_v)
        visited_item = MathTex(str(next_v), font_size=16, color=BLUE)
        visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
        visited_item.align_to(visited_items[-1], DOWN)
        visited_items.add(visited_item)
        self.add(visited_item)
        self.play(FadeIn(visited_item, scale=0.9), run_time=0.5)
        self.wait(1)

        # Step 3: Try 3 -> 4
        prev_v = next_v
        next_v = 4
        edge_key = get_edge_key(prev_v, next_v)
        path.append(next_v)
        visited_set.add(next_v)
        current_path_edges.append(edge_key)
        
        self.play(
            alg_graph.vertices[next_v].animate.set_fill(YELLOW),
            label_dict[next_v].animate.set_color(BLACK),
            alg_graph.edges[edge_key].animate.set_stroke(ORANGE, width=edge_width + 1),
            run_time=1.0,
        )
        push_to_stack(next_v)
        visited_item = MathTex(str(next_v), font_size=16, color=BLUE)
        visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
        visited_item.align_to(visited_items[-1], DOWN)
        visited_items.add(visited_item)
        self.add(visited_item)
        self.play(FadeIn(visited_item, scale=0.9), run_time=0.5)
        self.wait(1)

        # Step 4: Try 4 -> 5 (this will lead to a dead end at 5)
        update_status("At vertex 4: going to vertex 5...")
        self.wait(1)
        
        prev_v = 4
        next_v = 5
        edge_key = get_edge_key(prev_v, next_v)
        path.append(next_v)
        visited_set.add(next_v)
        current_path_edges.append(edge_key)
        
        self.play(
            alg_graph.vertices[next_v].animate.set_fill(YELLOW),
            label_dict[next_v].animate.set_color(BLACK),
            alg_graph.edges[edge_key].animate.set_stroke(ORANGE, width=edge_width + 1),
            run_time=1.0,
        )
        push_to_stack(next_v)
        visited_item = MathTex(str(next_v), font_size=16, color=BLUE)
        visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
        visited_item.align_to(visited_items[-1], DOWN)
        visited_items.add(visited_item)
        self.add(visited_item)
        self.play(FadeIn(visited_item, scale=0.9), run_time=0.5)
        self.wait(1)

        # At vertex 5: Check if we can complete the cycle - DEAD END SCENARIO
        # Path is [1, 2, 3, 4, 5], visited = {1, 2, 3, 4, 5}
        # All vertices are visited, but we need to check if we can return to start
        # In our graph, 5 has edges to: 3 (visited), 4 (visited)
        # There's no edge (5,1) to return to start, so this is a dead end!
        update_status("At vertex 5: checking cycle completion...")
        self.wait(1)
        
        # Check if edge 5->1 exists
        return_edge_key = get_edge_key(5, 1)
        if return_edge_key not in alg_graph.edges:
            update_status("At vertex 5: no edge to start vertex 1! Dead end.")
            self.wait(1)
            
            # Mark vertex 5 as dead end (red)
            self.play(
                alg_graph.vertices[5].animate.set_fill(RED),
                label_dict[5].animate.set_color(WHITE),
                run_time=0.8,
            )
            self.wait(1)
            
            # BACKTRACK: Pop 5 from stack and path
            update_status("Backtracking: removing vertex 5 from path...")
            self.wait(1)
            
            # Remove 5 from visited set
            visited_set.remove(5)
            path.pop()  # Remove 5 from path
            last_edge = current_path_edges.pop()  # Remove edge (4,5)
            
            # Reset edge (4,5) to normal
            edge_to_reset = get_edge_key(4, 5)
            if edge_to_reset in alg_graph.edges:
                self.play(
                    alg_graph.edges[edge_to_reset].animate.set_stroke(WHITE, width=edge_width),
                    run_time=0.6,
                )
            
            # Reset vertex 5 to normal
            self.play(
                alg_graph.vertices[5].animate.set_fill(WHITE),
                label_dict[5].animate.set_color(BLACK),
                run_time=0.6,
            )
            
            # Remove 5 from visited items display
            if len(visited_items) > 0:
                item_to_remove = visited_items[-1]
                visited_items.remove(item_to_remove)
                self.play(FadeOut(item_to_remove), run_time=0.5)
                self.remove(item_to_remove)
            
            # Pop 5 from stack
            pop_from_stack()
            self.wait(1)
            
            # BACKTRACK further: Pop 4 from stack and path
            update_status("Backtracking: removing vertex 4 from path...")
            self.wait(1)
            
            # Remove 4 from visited set
            visited_set.remove(4)
            path.pop()  # Remove 4 from path
            last_edge = current_path_edges.pop()  # Remove edge (3,4)
            
            # Reset edge (3,4) to normal
            edge_to_reset = get_edge_key(3, 4)
            if edge_to_reset in alg_graph.edges:
                self.play(
                    alg_graph.edges[edge_to_reset].animate.set_stroke(WHITE, width=edge_width),
                    run_time=0.6,
                )
            
            # Reset vertex 4 to normal
            self.play(
                alg_graph.vertices[4].animate.set_fill(WHITE),
                label_dict[4].animate.set_color(BLACK),
                run_time=0.6,
            )
            
            # Remove 4 from visited items display
            if len(visited_items) > 0:
                item_to_remove = visited_items[-1]
                visited_items.remove(item_to_remove)
                self.play(FadeOut(item_to_remove), run_time=0.5)
                self.remove(item_to_remove)
            
            # Pop 4 from stack
            pop_from_stack()
            self.wait(1)
            
            # Now at vertex 3: Try alternative path 3 -> 5
            # Backtracking finished, start exploring again
            update_status("Exploring alternative path 3 -> 5...")
            self.wait(1)
            
            # Step: 3 -> 5
            prev_v = 3
            next_v = 5
            edge_key = get_edge_key(prev_v, next_v)
            path.append(next_v)
            visited_set.add(next_v)
            current_path_edges.append(edge_key)
            
            self.play(
                alg_graph.vertices[next_v].animate.set_fill(YELLOW),
                label_dict[next_v].animate.set_color(BLACK),
                alg_graph.edges[edge_key].animate.set_stroke(ORANGE, width=edge_width + 1),
                run_time=1.0,
            )
            push_to_stack(next_v)
            visited_item = MathTex(str(next_v), font_size=16, color=BLUE)
            visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
            visited_item.align_to(visited_items[-1], DOWN)
            visited_items.add(visited_item)
            self.add(visited_item)
            self.play(FadeIn(visited_item, scale=0.9), run_time=0.5)
            self.wait(1)
            
            # Step: 5 -> 4
            update_status("At vertex 5: going to vertex 4...")
            self.wait(1)
            
            prev_v = 5
            next_v = 4
            edge_key = get_edge_key(prev_v, next_v)
            path.append(next_v)
            visited_set.add(next_v)
            current_path_edges.append(edge_key)
            
            self.play(
                alg_graph.vertices[next_v].animate.set_fill(YELLOW),
                label_dict[next_v].animate.set_color(BLACK),
                alg_graph.edges[edge_key].animate.set_stroke(ORANGE, width=edge_width + 1),
                run_time=1.0,
            )
            push_to_stack(next_v)
            visited_item = MathTex(str(next_v), font_size=16, color=BLUE)
            visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
            visited_item.align_to(visited_items[-1], DOWN)
            visited_items.add(visited_item)
            self.add(visited_item)
            self.play(FadeIn(visited_item, scale=0.9), run_time=0.5)
            self.wait(1)
            
            # At vertex 4: Check if we can complete the cycle
            # Path is [1, 2, 3, 5, 4], visited = {1, 2, 3, 4, 5}
            # All vertices visited! Check if edge 4->1 exists
            update_status("At vertex 4: all vertices visited! Checking cycle completion...")
            self.wait(1)
        
        # Verify all vertices are visited
        all_visited = len(visited_set) == len(v_alg)
        path_complete = len(path) == len(v_alg)
        
        status_msg = f"Visited: {len(visited_set)}/{len(v_alg)}, Path length: {len(path)}/{len(v_alg)}"
        update_status(status_msg)
        self.wait(1)
        
        if not all_visited or not path_complete:
            update_status(f"Error: Not all vertices visited! Missing: {set(v_alg) - visited_set}")
            self.wait(1)
            return
        
        # Check if edge 4->1 exists
        return_edge_key = get_edge_key(4, 1)
        if return_edge_key not in alg_graph.edges:
            update_status("Dead end: no edge 4 -> 1. Cannot complete cycle.")
            self.wait(1)
            return
        
        # All conditions met: complete the cycle
        update_status("All conditions met! Edge 4 -> 1 exists. Completing cycle...")
        self.wait(1)
        
        prev_v = 4
        next_v = 1
        edge_key = return_edge_key
        current_path_edges.append(edge_key)
        
        update_status("Hamiltonian cycle found: 1 -> 2 -> 3 -> 5 -> 4 -> 1")
        self.wait(1)
        
        # Highlight the return edge (4->1) prominently
        if edge_key in alg_graph.edges:
            edge_mob = alg_graph.edges[edge_key]
            # Flash the edge to make it visible
            self.play(
                edge_mob.animate.set_stroke(YELLOW, width=edge_width + 3),
                run_time=0.5,
            )
            self.wait(1)
            # Then set it to green
            self.play(
                alg_graph.vertices[next_v].animate.set_fill(GREEN),
                label_dict[next_v].animate.set_color(WHITE),
                edge_mob.animate.set_stroke(GREEN, width=edge_width + 2),
                run_time=1.0,
            )
        else:
            self.play(
                alg_graph.vertices[next_v].animate.set_fill(GREEN),
                label_dict[next_v].animate.set_color(WHITE),
                run_time=1.0,
            )
        self.wait(1)

        # Prompt 18: Hamiltonian Cycle Found
        self.wait(1)

        # Highlight all cycle edges in green
        # Cycle is: 1 -> 2 -> 3 -> 5 -> 4 -> 1
        # Edges: (1,2), (2,3), (3,5), (5,4), (4,1)
        # Build cycle edges explicitly from the path
        final_cycle_edges = []
        # Add all edges from current_path_edges (path edges)
        for e in current_path_edges:
            if isinstance(e, tuple) and len(e) == 2:
                key = get_edge_key(e[0], e[1])
            else:
                key = e
            if key in alg_graph.edges and key not in final_cycle_edges:
                final_cycle_edges.append(key)
        
        # Add the return edge (4,1) to complete the cycle
        return_edge_key_final = get_edge_key(4, 1)
        if return_edge_key_final in alg_graph.edges and return_edge_key_final not in final_cycle_edges:
            final_cycle_edges.append(return_edge_key_final)
        
        # Also explicitly check all edges in the cycle path: 1->2->3->5->4->1
        cycle_path_edges = [
            (1, 2), (2, 3), (3, 5), (5, 4), (4, 1)
        ]
        for u, v in cycle_path_edges:
            edge_k = get_edge_key(u, v)
            if edge_k in alg_graph.edges and edge_k not in final_cycle_edges:
                final_cycle_edges.append(edge_k)
        
        # Also highlight all vertices in the cycle in green
        cycle_vertices = [1, 2, 3, 5, 4]
        vertex_anims = [
            alg_graph.vertices[v].animate.set_fill(GREEN)
            for v in cycle_vertices
        ]
        label_anims = [
            label_dict[v].animate.set_color(WHITE)
            for v in cycle_vertices
        ]
        edge_anims = [
            alg_graph.edges[e].animate.set_stroke(GREEN, width=edge_width + 2)
            for e in final_cycle_edges
        ]
        
        self.play(
            *vertex_anims,
            *label_anims,
            *edge_anims,
            run_time=1.5,
        )
        self.wait(1)

        # Prompt 17: Show final path summary
        # Explicit LaTeX arrows so the text renders cleanly
        # Cycle: 1 -> 2 -> 3 -> 5 -> 4 -> 1
        summary_text = MathTex(
            r"\text{Hamiltonian Cycle: } 1 \to 2 \to 3 \to 5 \to 4 \to 1",
            font_size=24,
            color=GREEN,
        ).next_to(status_text, UP, buff=0.3)
        self.play(Write(summary_text), run_time=1.0)
        self.wait(1)

        self.play(
            FadeOut(alg_graph),
            FadeOut(alg_node_labels),
            FadeOut(title_bt),
            FadeOut(stack_label),
            FadeOut(stack_container),
            FadeOut(stack_inner),
            FadeOut(visited_label),
            FadeOut(visited_items),
            FadeOut(stack_items),
            FadeOut(status_text),
            FadeOut(summary_text),
            run_time=1.0,
        )
        self.wait(1)

        # ============================================================
        # Summary
        # ============================================================
        summary_title = Text("Summary", font_size=48)
        self.play(FadeIn(summary_title, shift=UP * 0.5), run_time=1.0)
        self.wait(1)
        self.play(summary_title.animate.to_edge(UP), run_time=0.8)

        summary_points = VGroup(
            MathTex(r"\text{Hamilton Path: visits every vertex once, different start/end}", font_size=26),
            MathTex(r"\text{Hamilton Cycle: visits every vertex once, returns to start}", font_size=26),
            MathTex(r"\text{Ore's Theorem: } \deg(u) + \deg(v) \geq n \Rightarrow \text{ Hamiltonian}", font_size=26),
            MathTex(r"\text{Dirac's Theorem: } \deg(v) \geq n/2 \Rightarrow \text{ Hamiltonian cycle}", font_size=26),
            MathTex(r"\text{Backtracking: systematic search for Hamiltonian cycles}", font_size=26),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.6)
        self.play(Write(summary_points), run_time=2.5)
        self.wait(1)

        self.play(
            FadeOut(summary_title), FadeOut(summary_points),
            run_time=1.0
        )
        self.wait(1)

        # ============================================================
        # Final Summary (Hamiltonian topics)
        # ============================================================
        summary_title = Text("Summary – Hamiltonian Paths & Cycles", font_size=42)
        self.play(FadeIn(summary_title, shift=UP * 0.5), run_time=1.0)
        self.wait(1)
        self.play(summary_title.animate.to_edge(UP), run_time=0.8)

        summary_points = VGroup(
            MathTex(r"\text{Hamilton path: visits every vertex exactly once.}", font_size=24),
            MathTex(r"\text{Hamilton cycle: Hamilton path that returns to start.}", font_size=24),
            MathTex(r"\text{Ore/Dirac: degree conditions that guarantee cycles.}", font_size=24),
            MathTex(r"\text{Backtracking: systematic search for Hamilton cycles.}", font_size=24),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.6)

        self.play(Write(summary_points), run_time=2.0)
        self.wait(1)

        self.play(FadeOut(summary_title), FadeOut(summary_points), run_time=1.0)
        self.wait(1)

