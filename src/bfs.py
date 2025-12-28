from manim import *


class BFSQueueVisualization(Scene):
    """
    Breadth-First Search with explicit queue, matching styles/colors of DFS scenes.
    """

    def construct(self):
        # ============================================================
        # Introduction
        # ============================================================
        intro_title = Text("Graph Theory – Breadth-First Search", font_size=48)
        self.play(FadeIn(intro_title, shift=UP * 0.5), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(intro_title, shift=UP * 0.5), run_time=0.8)

        # ============================================================
        # BFS Algorithm Steps (separate slide)
        # ============================================================
        bfs_algo_title = Text("BFS Algorithm", font_size=40)
        bfs_algo_text = VGroup(
            MathTex(r"\text{1. Start at a source vertex (enqueue).}", font_size=24),
            MathTex(r"\text{2. Mark current vertex as visited.}", font_size=24),
            MathTex(r"\text{3. Enqueue all unvisited neighbors.}", font_size=24),
            MathTex(r"\text{4. Dequeue next vertex and repeat.}", font_size=24),
            MathTex(r"\text{5. Continue until queue is empty.}", font_size=24),
            MathTex(r"\text{6. BFS explores level by level (breadth-first).}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        algo_block = VGroup(bfs_algo_title, bfs_algo_text).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        algo_block.move_to(ORIGIN)
        self.play(Write(bfs_algo_title), run_time=1.2)
        self.play(Write(bfs_algo_text), run_time=3.75)
        self.wait(1)
        self.play(FadeOut(algo_block), run_time=1.0)

        # Graph setup (same as DFS)
        vertices = [0, 1, 2, 3, 4, 5, 6]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 6)]

        layout = {
            0: UP * 2.2,
            1: LEFT * 2.0 + UP * 0.8,
            2: RIGHT * 2.0 + UP * 0.8,
            3: LEFT * 3.0 + DOWN * 0.8,
            4: LEFT * 0.4 + DOWN * 1.2,
            5: RIGHT * 3.0 + DOWN * 0.8,
            6: DOWN * 2.2,
        }

        vertex_style = {
            "radius": 0.22,
            "fill_color": WHITE,
            "stroke_color": WHITE,
            "stroke_width": 2,
        }
        edge_width = 3
        edge_style = {
            "stroke_color": WHITE,
            "stroke_width": edge_width,
        }

        graph = Graph(
            vertices,
            edges,
            layout=layout,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )

        # Node labels
        node_labels = VGroup()
        for v in vertices:
            lbl = MathTex(str(v), font_size=20, color=BLACK)
            lbl.move_to(graph.vertices[v].get_center())
            node_labels.add(lbl)

        title = MathTex(r"\text{Breadth-First Search (Queue)}", font_size=28).to_edge(UP, buff=0.3)
        self.play(Create(graph), Write(node_labels), run_time=1.1)
        self.wait(0.5)
        self.play(Write(title), run_time=0.75)
        self.wait(0.5)

        # Queue UI
        queue_label = MathTex(r"\text{Queue}", font_size=22)
        queue_label.to_edge(LEFT, buff=0.4).shift(UP * 1.6)

        queue_container = Rectangle(
            width=3.2,
            height=1.4,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_opacity=0.05,
            fill_color=BLUE,
        )
        queue_container.next_to(queue_label, DOWN, buff=0.25)
        queue_container.align_to(queue_label, LEFT)

        queue_inner = Rectangle(
            width=3.0,
            height=1.2,
            stroke_color=BLUE,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        queue_inner.move_to(queue_container.get_center())

        self.play(Write(queue_label), Create(queue_container), Create(queue_inner), run_time=0.9)
        self.wait(0.5)

        visited_label = MathTex(r"\text{Visited:}", font_size=18)
        visited_label.next_to(queue_container, DOWN, buff=0.3)
        visited_label.align_to(queue_label, LEFT)
        self.play(Write(visited_label), run_time=0.25)
        self.wait(0.5)
        
        # Distance table (similar style to Dijkstra, on the right)
        dist_label = MathTex(r"\text{Distances}", font_size=18)
        dist_label.next_to(graph, RIGHT, buff=1.0).shift(UP * 1.0)
        dist_container = Rectangle(
            width=2.2,
            height=3.2,
            stroke_color=BLUE,
            stroke_width=2,
            fill_opacity=0.05,
            fill_color=BLUE,
        )
        dist_container.next_to(dist_label, DOWN, buff=0.2)
        dist_container.align_to(dist_label, LEFT)
        dist_inner = Rectangle(
            width=2.0,
            height=3.0,
            stroke_color=BLUE,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        dist_inner.move_to(dist_container.get_center())
        self.play(
            Write(dist_label),
            Create(dist_container),
            Create(dist_inner),
            run_time=0.5,
        )

        distances = {v: float("inf") for v in vertices}
        dist_items = VGroup()
        dist_entries = {}
        for i, v in enumerate(vertices):
            node_text = MathTex(rf"d[{v}]", font_size=18, color=WHITE)
            dist_text = MathTex(r"\infty", font_size=18, color=WHITE)
            entry_group = VGroup(node_text, dist_text).arrange(RIGHT, buff=0.25)
            if i == 0:
                entry_group.next_to(dist_container.get_top(), DOWN, buff=0.25)
                entry_group.align_to(dist_container, LEFT).shift(RIGHT * 0.2)
            else:
                entry_group.next_to(dist_items[-1], DOWN, buff=0.2)
                entry_group.align_to(dist_items[-1], LEFT)
            dist_items.add(entry_group)
            dist_entries[v] = dist_text
            self.add(entry_group)
        self.play(FadeIn(dist_items), run_time=0.4)

        visited_items = VGroup()
        queue_items = []
        traversal_order = []
        in_queue = set()
        visited = set()
        move_label = [None]
        tree_edges = []
        current_node_indicator = None  # Visual indicator for current node

        # Helper: show edge wave + move text
        def show_move(parent, child):
            if parent is None:
                return
            edge_key = (min(parent, child), max(parent, child))
            if edge_key in graph.edges:
                wave = graph.edges[edge_key].copy().set_stroke(BLUE, width=edge_width + 2)
                self.play(
                    ShowPassingFlash(wave, time_width=0.9, run_time=0.7, rate_func=linear),
                )
            if move_label[0] is not None:
                self.play(FadeOut(move_label[0], run_time=0.2))
            lbl = MathTex(rf"{parent} \rightarrow {child}", font_size=22, color=WHITE)
            lbl.to_edge(DOWN, buff=0.6)
            move_label[0] = lbl
            self.play(FadeIn(lbl, shift=UP * 0.1), run_time=0.5, rate_func=smooth)

        # Helper: reposition queue items (front on the left)
        def layout_queue():
            x_start = queue_inner.get_left()[0] + 0.3
            y_mid = queue_inner.get_center()[1]
            for i, item in enumerate(queue_items):
                target = np.array([x_start + i * 0.75, y_mid, 0])
                if len(queue_items) > 0:
                    self.play(item.animate.move_to(target), run_time=0.1, rate_func=smooth)

        # Enqueue helper
        def enqueue(node):
            if node in visited or node in in_queue:
                return
            box = Rectangle(
                width=0.7,
                height=0.6,
                stroke_color=BLUE,
                stroke_width=1.5,
                fill_color=BLUE,
                fill_opacity=0.3,
            )
            txt = MathTex(str(node), font_size=16, color=WHITE)
            txt.move_to(box.get_center())
            group = VGroup(box, txt)
            # place temporarily at right then layout
            group.move_to(queue_inner.get_right() + LEFT * 0.3)
            queue_items.append(group)
            self.add(group)
            self.play(FadeIn(group, shift=DOWN * 0.1), run_time=0.15, rate_func=smooth)
            self.wait(0.5)
            layout_queue()
            # queue color on node
            self.play(
                graph.vertices[node].animate.set_fill("#5FA8FF"),
                node_labels[node].animate.set_color(WHITE),
                run_time=0.3,
                rate_func=smooth,
            )
            in_queue.add(node)

        # Dequeue helper
        def dequeue():
            if not queue_items:
                return None
            item = queue_items.pop(0)
            self.play(FadeOut(item, shift=LEFT * 0.2), run_time=0.15, rate_func=smooth)
            layout_queue()
            return item

        # Build adjacency list
        adj = {v: [] for v in vertices}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        for v in adj:
            adj[v].sort()

        # Start BFS
        start = 0
        enqueue(start)
        # Update distance for source node
        distances[start] = 0
        old_dist_start = dist_entries[start]
        new_dist_start = MathTex("0", font_size=18, color=WHITE)
        new_dist_start.move_to(old_dist_start.get_center())
        self.play(Transform(old_dist_start, new_dist_start), run_time=0.25)
        dist_entries[start] = new_dist_start

        queue = [(start, None)]

        while queue:
            # Short pause before entering new node and erasing it from queue
            self.wait(0.5)
            node, parent = queue.pop(0)
            dequeue()
            in_queue.discard(node)

            if node in visited:
                continue

            visited.add(node)
            traversal_order.append(node)
            show_move(parent, node)
            
            # Remove previous indicator if exists
            if current_node_indicator is not None:
                self.remove(current_node_indicator)
            
            # Create and add current node indicator (dot)
            current_node_indicator = Dot(radius=0.12, color=RED)
            current_node_indicator.move_to(graph.vertices[node].get_center())
            self.add(current_node_indicator)
            
            self.play(
                graph.vertices[node].animate.set_fill("#FFD54F"),
                node_labels[node].animate.set_color(BLACK),
                FadeIn(current_node_indicator, scale=0.5),
                run_time=0.5,
                rate_func=smooth,
            )
            self.wait(0.5)

            # Add to visited list and finalize color
            visited_item = MathTex(str(node), font_size=16, color=BLUE)
            if len(visited_items) == 0:
                visited_item.next_to(visited_label, DOWN, buff=0.2)
                visited_item.align_to(visited_label, LEFT).shift(RIGHT * 0.3)
            else:
                visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
                visited_item.align_to(visited_items[-1], DOWN)
            visited_items.add(visited_item)
            self.add(visited_item)

            self.play(
                FadeIn(visited_item, scale=0.9),
                graph.vertices[node].animate.set_fill("#34C759"),
                node_labels[node].animate.set_color(WHITE),
                FadeOut(current_node_indicator),
                run_time=0.425,
                rate_func=smooth,
            )
            # Remove indicator after node is fully visited
            if current_node_indicator is not None:
                self.remove(current_node_indicator)
                current_node_indicator = None
            self.wait(0.5)

            # Enqueue neighbors and record tree edges (and update their distances)
            for nbr in adj[node]:
                if nbr not in visited and nbr not in in_queue:
                    queue.append((nbr, node))
                    tree_edges.append((min(node, nbr), max(node, nbr)))
                    # distance of neighbor = distance of current + 1
                    if distances[nbr] == float("inf"):
                        distances[nbr] = distances[node] + 1
                        old_dt = dist_entries[nbr]
                        new_dt = MathTex(str(int(distances[nbr])), font_size=18, color=WHITE)
                        new_dt.move_to(old_dt.get_center())
                        self.play(Transform(old_dt, new_dt), run_time=0.2)
                        dist_entries[nbr] = new_dt
                    enqueue(nbr)

        self.wait(1)
        
        # Fade out move label before showing summary
        if move_label[0] is not None:
            self.play(FadeOut(move_label[0]), run_time=0.5)
            move_label[0] = None  # Clear reference to prevent double fade
        
        # Remove current node indicator if still exists
        if current_node_indicator is not None:
            self.remove(current_node_indicator)

        summary = VGroup(
            MathTex(r"\text{Traversal Order:}", font_size=18),
            MathTex(r" \to ".join(str(v) for v in traversal_order), font_size=16, color=WHITE),
        ).arrange(DOWN, buff=0.2)
        summary.to_edge(DOWN, buff=0.3)  # Position lower at bottom
        self.play(Write(summary), run_time=1.2)
        self.wait(1)

        # Keep original graph; move it left and build spanning tree on the right edge-by-edge
        fade_anims = [
            FadeOut(queue_label),
            FadeOut(queue_container),
            FadeOut(queue_inner),
            FadeOut(visited_label),
            FadeOut(visited_items),
            FadeOut(dist_label),
            FadeOut(dist_container),
            FadeOut(dist_inner),
            FadeOut(dist_items),
            FadeOut(summary),
            FadeOut(title),
        ]
        if queue_items:
            fade_anims.append(FadeOut(VGroup(*queue_items)))
        if move_label[0]:
            fade_anims.append(FadeOut(move_label[0]))
        self.play(*fade_anims)

        shift_vec = LEFT * 3
        self.play(
            graph.animate.shift(shift_vec).scale(0.7),
            node_labels.animate.shift(shift_vec).scale(0.7),
            run_time=1.2,
            rate_func=smooth,
        )

        tree_graph = Graph(
            vertices,
            [],
            layout=layout,
            vertex_config=vertex_style,
            edge_config={**edge_style, "tip_length": 0.25},
            edge_type=Arrow,
        ).shift(RIGHT * 3).scale(0.7)
        tree_labels = VGroup()
        for v in vertices:
            lbl = MathTex(str(v), font_size=20, color=BLACK)
            lbl.move_to(tree_graph.vertices[v].get_center())
            tree_labels.add(lbl)
        for edge in tree_graph.edges.values():
            edge.set_opacity(0)

        base_title = MathTex(r"\text{Original Graph}", font_size=26).next_to(graph, UP, buff=0.25)
        tree_title = MathTex(r"\text{BFS Spanning Tree}", font_size=26).next_to(tree_graph, UP, buff=0.25)

        self.play(Create(tree_graph), Write(tree_labels), Write(base_title), Write(tree_title), run_time=1.0, rate_func=smooth)

        for e in tree_edges:
            if e not in graph.edges:
                continue
            wave = graph.edges[e].copy().set_stroke(BLUE, width=edge_width + 2)
            tree_graph.add_edges(e, edge_config={"stroke_color": edge_style["stroke_color"], "stroke_width": edge_width, "tip_length": 0.25}, edge_type=Arrow)
            new_edge = tree_graph.edges[e]
            new_edge.set_opacity(0)
            # Ensure tip is also hidden if it exists as a separate component
            for submob in new_edge.submobjects:
                submob.set_opacity(0)

            anims = [
                ShowPassingFlash(wave, time_width=0.9, run_time=0.6, rate_func=linear),
                new_edge.animate.set_opacity(1),
            ]
            # Animate all submobjects (including tip) to visible
            for submob in new_edge.submobjects:
                anims.append(submob.animate.set_opacity(1))

            self.play(*anims, run_time=0.7, rate_func=smooth)

        self.wait(1)
        self.play(
            FadeOut(tree_graph),
            FadeOut(tree_labels),
            FadeOut(base_title),
            FadeOut(tree_title),
            FadeOut(graph),
            FadeOut(node_labels),
            run_time=1.0,
        )

        # ============================================================
        # Bipartite spotlight + extra BFS demos
        # ============================================================
        # 1) Show the bipartite graph from main.py
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
        bi_graph = Graph(
            vertices_bi,
            all_bi_pairs,
            layout=layout_bi,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        title_bi = Text("Bipartite Graph", font_size=36).to_edge(UP)
        self.play(Create(bi_graph), Write(title_bi), run_time=1.2)
        self.wait(0.6)
        # Color parts to emphasize bipartition (even vs odd distance levels)
        COLOR_EVEN = "#4ECDC4"
        COLOR_ODD = "#FF9F1C"
        self.play(
            *[bi_graph.vertices[v].animate.set_fill(COLOR_EVEN) for v in left_part],
            *[bi_graph.vertices[v].animate.set_fill(COLOR_ODD) for v in right_part],
            run_time=0.8,
        )
        self.play(
            FadeOut(bi_graph),
            FadeOut(title_bi),
            run_time=0.8
        )

        # Add tom.png image
        try:
            tom_img = ImageMobject("assets/tom.png")
            tom_img.scale(1.5)
            tom_img.move_to(ORIGIN)
            self.play(FadeIn(tom_img), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(tom_img), run_time=1.0)
        except:
            # If image not found, show a placeholder text
            tom_text = Text("🖼️ TOM 🖼️", font_size=64, color=YELLOW)
            self.play(FadeIn(tom_text), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(tom_text), run_time=1.0)

        # Helper to rerun a compact BFS with the same queue animation style
        # Optionally color vertices by distance parity and/or explain non-bipartiteness.
        def run_queue_bfs(
            title_text,
            vertices_local,
            edges_local,
            layout_local,
            start_vertex=None,
            show_bipartite_coloring=False,
            explain_non_bipartite=False,
            show_layers=False,
        ):
            graph_local = Graph(
                vertices_local,
                edges_local,
                layout=layout_local,
                vertex_config=vertex_style,
                edge_config=edge_style,
            )
            labels_local = VGroup()
            label_map_local = {}
            for v in vertices_local:
                lbl = MathTex(str(v), font_size=20, color=BLACK)
                lbl.move_to(graph_local.vertices[v].get_center())
                labels_local.add(lbl)
                label_map_local[v] = lbl

            title_local = MathTex(title_text, font_size=26).to_edge(UP, buff=0.35)
            self.play(Create(graph_local), Write(labels_local), Write(title_local), run_time=1.0)
            self.wait(0.4)

            # Queue UI
            queue_label = MathTex(r"\text{Queue}", font_size=20)
            queue_label.to_edge(LEFT, buff=0.4).shift(UP * 1.6)
            queue_container = Rectangle(
                width=3.0,
                height=1.4,
                stroke_color=BLUE,
                stroke_width=2.0,
                fill_opacity=0.05,
                fill_color=BLUE,
            )
            queue_container.next_to(queue_label, DOWN, buff=0.25)
            queue_container.align_to(queue_label, LEFT)
            queue_inner = Rectangle(
                width=2.8,
                height=1.2,
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.3,
            )
            queue_inner.move_to(queue_container.get_center())
            visited_label = MathTex(r"\text{Visited:}", font_size=16)
            visited_label.next_to(queue_container, DOWN, buff=0.3)
            visited_label.align_to(queue_label, LEFT)
            self.play(
                Write(queue_label),
                Create(queue_container),
                Create(queue_inner),
                Write(visited_label),
                run_time=0.8,
            )

            visited_items_local = VGroup()
            queue_items_local = []
            traversal_local = []
            in_queue_local = set()
            visited_local = set()
            dist_local = {}
            move_label_local = [None]
            current_indicator = None

            # Distance table for this BFS run (right side)
            dist_label = MathTex(r"\text{Distances}", font_size=16)
            dist_label.next_to(graph_local, RIGHT, buff=0.9).shift(UP * 0.9)
            dist_container = Rectangle(
                width=2.0,
                height=2.8,
                stroke_color=BLUE,
                stroke_width=2,
                fill_opacity=0.05,
                fill_color=BLUE,
            )
            dist_container.next_to(dist_label, DOWN, buff=0.2)
            dist_container.align_to(dist_label, LEFT)
            dist_inner = Rectangle(
                width=1.8,
                height=2.6,
                stroke_color=BLUE,
                stroke_width=1,
                stroke_opacity=0.3,
            )
            dist_inner.move_to(dist_container.get_center())
            self.play(
                Write(dist_label),
                Create(dist_container),
                Create(dist_inner),
                run_time=0.7,
            )

            dist_items = VGroup()
            dist_entries = {}
            for i, v in enumerate(vertices_local):
                node_text = MathTex(rf"d[{v}]", font_size=14, color=WHITE)
                dist_text = MathTex(r"\infty", font_size=14, color=WHITE)
                entry_group = VGroup(node_text, dist_text).arrange(RIGHT, buff=0.2)
                if i == 0:
                    entry_group.next_to(dist_container.get_top(), DOWN, buff=0.2)
                    entry_group.align_to(dist_container, LEFT).shift(RIGHT * 0.15)
                else:
                    entry_group.next_to(dist_items[-1], DOWN, buff=0.15)
                    entry_group.align_to(dist_items[-1], LEFT)
                dist_items.add(entry_group)
                dist_entries[v] = dist_text
                self.add(entry_group)
            self.play(FadeIn(dist_items), run_time=0.6)

            def show_move(parent, child):
                if parent is None:
                    return
                edge_key = (min(parent, child), max(parent, child))
                if edge_key in graph_local.edges:
                    wave = graph_local.edges[edge_key].copy().set_stroke(BLUE, width=edge_width + 2)
                    self.play(
                        ShowPassingFlash(wave, time_width=0.7, run_time=0.4, rate_func=linear),
                    )
                if move_label_local[0] is not None:
                    self.play(FadeOut(move_label_local[0], run_time=0.15))
                lbl = MathTex(rf"{parent} \rightarrow {child}", font_size=20, color=WHITE)
                lbl.to_edge(DOWN, buff=0.6)
                move_label_local[0] = lbl
                self.play(FadeIn(lbl, shift=UP * 0.08), run_time=0.25, rate_func=smooth)

            def layout_queue():
                x_start = queue_inner.get_left()[0] + 0.3
                y_mid = queue_inner.get_center()[1]
                for i, item in enumerate(queue_items_local):
                    target = np.array([x_start + i * 0.7, y_mid, 0])
                    self.play(item.animate.move_to(target), run_time=0.15, rate_func=smooth)

            def enqueue(node):
                if node in visited_local or node in in_queue_local:
                    return
                box = Rectangle(
                    width=0.65,
                    height=0.55,
                    stroke_color=BLUE,
                    stroke_width=1.5,
                    fill_color=BLUE,
                    fill_opacity=0.3,
                )
                txt = MathTex(str(node), font_size=16, color=WHITE)
                txt.move_to(box.get_center())
                group = VGroup(box, txt)
                group.move_to(queue_inner.get_right() + LEFT * 0.3)
                queue_items_local.append(group)
                self.add(group)
                self.play(FadeIn(group, shift=DOWN * 0.08), run_time=0.2, rate_func=smooth)
                layout_queue()
                self.play(
                    graph_local.vertices[node].animate.set_fill("#5FA8FF"),
                    label_map_local[node].animate.set_color(WHITE),
                    run_time=0.2,
                    rate_func=smooth,
                )
                in_queue_local.add(node)

            def dequeue():
                if not queue_items_local:
                    return None
                item = queue_items_local.pop(0)
                self.play(FadeOut(item, shift=LEFT * 0.2), run_time=0.2, rate_func=smooth)
                layout_queue()
                return item

            # adjacency
            adj_local = {v: [] for v in vertices_local}
            for u, v in edges_local:
                adj_local[u].append(v)
                adj_local[v].append(u)
            for v in adj_local:
                adj_local[v].sort()

            start = start_vertex if start_vertex is not None else vertices_local[0]
            enqueue(start)
            dist_local[start] = 0
            # Update distance table for source
            old_dt = dist_entries[start]
            new_dt = MathTex("0", font_size=14, color=WHITE)
            new_dt.move_to(old_dt.get_center())
            self.play(Transform(old_dt, new_dt), run_time=0.4)
            dist_entries[start] = new_dt
            queue_work = [(start, None)]

            while queue_work:
                self.wait(0.25)
                node, parent = queue_work.pop(0)
                dequeue()
                in_queue_local.discard(node)
                if node in visited_local:
                    continue
                visited_local.add(node)
                traversal_local.append(node)
                show_move(parent, node)

                if current_indicator is not None:
                    self.remove(current_indicator)
                current_indicator = Dot(radius=0.12, color=RED)
                current_indicator.move_to(graph_local.vertices[node].get_center())
                self.add(current_indicator)
                self.play(
                    graph_local.vertices[node].animate.set_fill("#FFD54F"),
                    label_map_local[node].animate.set_color(BLACK),
                    FadeIn(current_indicator, scale=0.5),
                    run_time=0.4,
                    rate_func=smooth,
                )
                self.wait(0.15)

                visited_item = MathTex(str(node), font_size=16, color=BLUE)
                if len(visited_items_local) == 0:
                    visited_item.next_to(visited_label, DOWN, buff=0.2)
                    visited_item.align_to(visited_label, LEFT).shift(RIGHT * 0.3)
                else:
                    visited_item.next_to(visited_items_local[-1], RIGHT, buff=0.25)
                    visited_item.align_to(visited_items_local[-1], DOWN)
                visited_items_local.add(visited_item)
                self.add(visited_item)

                self.play(
                    FadeIn(visited_item, scale=0.9),
                    graph_local.vertices[node].animate.set_fill("#34C759"),
                    label_map_local[node].animate.set_color(WHITE),
                    FadeOut(current_indicator),
                    run_time=0.35,
                    rate_func=smooth,
                )
                if current_indicator is not None:
                    self.remove(current_indicator)
                    current_indicator = None
                self.wait(0.1)

                for nbr in adj_local[node]:
                    if nbr not in visited_local and nbr not in in_queue_local:
                        queue_work.append((nbr, node))
                        # distance level for neighbor is parent level + 1
                        dist_local[nbr] = dist_local.get(node, 0) + 1
                        # update distance table entry
                        old_dt = dist_entries[nbr]
                        new_dt = MathTex(str(int(dist_local[nbr])), font_size=14, color=WHITE)
                        new_dt.move_to(old_dt.get_center())
                        self.play(Transform(old_dt, new_dt), run_time=0.3)
                        dist_entries[nbr] = new_dt
                        enqueue(nbr)

            # After BFS, optionally show bipartite coloring by distance parity
            if show_bipartite_coloring:
                COLOR_EVEN = "#4ECDC4"
                COLOR_ODD = "#FF9F1C"
                self.play(
                    *[
                        graph_local.vertices[v].animate.set_fill(
                            COLOR_EVEN if dist_local.get(v, 0) % 2 == 0 else COLOR_ODD
                        )
                        for v in vertices_local
                    ],
                    run_time=0.8,
                )

            # Optionally highlight an odd cycle witness: edge between same-parity vertices
            if explain_non_bipartite:
                bad_edges = []
                for u, v in edges_local:
                    if dist_local.get(u, 0) % 2 == dist_local.get(v, 0) % 2:
                        bad_edges.append((u, v))
                if bad_edges:
                    self.play(
                        *[
                            graph_local.edges[e].animate.set_stroke(RED, width=edge_width + 1)
                            for e in bad_edges
                        ],
                        run_time=0.6,
                    )
                    odd_cycle_text = MathTex(
                        r"\text{Edge between same-colored vertices }"
                        r"\Rightarrow \text{ graph has an odd cycle (not bipartite)}",
                        font_size=22,
                    )
                    odd_cycle_text.to_edge(DOWN, buff=0.6)
                    self.play(Write(odd_cycle_text), run_time=0.8)

            self.wait(0.3)
            if move_label_local[0] is not None:
                self.play(FadeOut(move_label_local[0]), run_time=0.2)

            traversal_summary = VGroup(
                MathTex(r"\text{Traversal Order:}", font_size=16),
                MathTex(r" \to ".join(str(v) for v in traversal_local), font_size=16, color=WHITE),
            ).arrange(DOWN, buff=0.15)
            traversal_summary.to_edge(DOWN, buff=0.3)
            self.play(Write(traversal_summary), run_time=0.6)
            self.wait(0.35)

            if explain_non_bipartite and 'odd_cycle_text' in locals():
                self.play(FadeOut(odd_cycle_text), run_time=0.6)

            # If layer view requested, first clear queue/dist UI, then lay out levels
            if show_layers:
                self.play(
                    FadeOut(queue_label),
                    FadeOut(queue_container),
                    FadeOut(queue_inner),
                    FadeOut(visited_label),
                    FadeOut(visited_items_local),
                    FadeOut(dist_label),
                    FadeOut(dist_container),
                    FadeOut(dist_inner),
                    FadeOut(dist_items),
                    FadeOut(traversal_summary),
                    run_time=0.8,
                )

                layers = {}
                for v, d in dist_local.items():
                    layers.setdefault(int(d), []).append(v)

                if layers:
                    sorted_levels = sorted(layers.keys())
                    y_top = 2.3  # numeric y for top row
                    y_step = 1.1  # tighter rows
                    x_step = 1.8
                    COLOR_EVEN = "#4ECDC4"
                    COLOR_ODD = "#FF9F1C"

                    label_targets = {}
                    color_targets = []
                    layer_rows = VGroup()
                    # Light grid frame
                    grid_height = y_step * max(1, (len(sorted_levels) - 1)) + 1.0
                    grid_width = 8.0
                    grid_box = Rectangle(
                        width=grid_width,
                        height=grid_height,
                        stroke_color=GRAY,
                        stroke_opacity=0.4,
                        fill_opacity=0.02,
                        fill_color=WHITE,
                    )
                    grid_box.move_to(np.array([0, y_top - grid_height / 2 + 0.2, 0]))
                    grid_lines = VGroup()
                    for i in range(len(sorted_levels)):
                        y_val = y_top - i * y_step
                        line = DashedLine(
                            np.array([-grid_width / 2, y_val, 0]),
                            np.array([grid_width / 2, y_val, 0]),
                            dash_length=0.15,
                            color=GRAY,
                            stroke_opacity=0.35,
                        )
                        grid_lines.add(line)
                    self.play(FadeIn(grid_box), FadeIn(grid_lines), run_time=0.6)
                    layer_caption = Text("BFS Layers (distance from source)", font_size=22)
                    layer_caption.next_to(grid_box, UP, buff=0.2)
                    self.play(Write(layer_caption), run_time=0.6)

                    for i, level in enumerate(sorted_levels):
                        verts = layers[level]
                        y_val = y_top - i * y_step
                        verts_sorted = sorted(verts)
                        total_width = x_step * (len(verts_sorted) - 1) if len(verts_sorted) > 1 else 0
                        for j, v in enumerate(verts_sorted):
                            x_val = -total_width / 2 + j * x_step
                            target_pos = np.array([x_val, y_val, 0])
                            label_targets[v] = target_pos
                            color_targets.append(
                                (v, COLOR_EVEN if level % 2 == 0 else COLOR_ODD)
                            )

                        row_tex = MathTex(
                            rf"{level} : " + ", ".join(str(v) for v in verts_sorted),
                            font_size=18,
                        )
                        row_tex.move_to(np.array([grid_box.get_left()[0] - 0.4, y_val, 0]))
                        layer_rows.add(row_tex)

                    # Build a new graph laid out on the grid, then transform to it so edges move too
                    new_layout = {v: pos for v, pos in label_targets.items()}
                    new_graph = Graph(
                        vertices_local,
                        edges_local,
                        layout=new_layout,
                        vertex_config=vertex_style,
                        edge_config=edge_style,
                    )
                    # Match current colors/styles so transform looks smooth (no flash / reset)
                    for v in vertices_local:
                        new_graph.vertices[v].set_fill(
                            graph_local.vertices[v].get_fill_color(),
                            opacity=graph_local.vertices[v].get_fill_opacity(),
                        )
                        new_graph.vertices[v].set_stroke(
                            graph_local.vertices[v].get_stroke_color(),
                            width=graph_local.vertices[v].get_stroke_width(),
                            opacity=graph_local.vertices[v].get_stroke_opacity(),
                        )
                    for e_key, edge_mob in graph_local.edges.items():
                        if e_key in new_graph.edges:
                            new_edge = new_graph.edges[e_key]
                            new_edge.set_stroke(
                                edge_mob.get_stroke_color(),
                                width=edge_mob.get_stroke_width(),
                                opacity=edge_mob.get_stroke_opacity(),
                            )

                    label_moves = [label_map_local[v].animate.move_to(pos) for v, pos in label_targets.items()]

                    self.play(
                        Transform(graph_local, new_graph),
                        *label_moves,
                        run_time=1.0,
                        rate_func=smooth,
                    )

                    if color_targets:
                        self.play(
                            *[
                                graph_local.vertices[v].animate.set_fill(color)
                                for v, color in color_targets
                            ],
                            run_time=0.8,
                            rate_func=smooth,
                        )

                    if len(layer_rows) > 0:
                        self.play(Write(layer_rows), run_time=0.8)
                    self.wait(0.8)

                    self.play(
                        FadeOut(layer_caption),
                        FadeOut(grid_lines),
                        FadeOut(grid_box),
                        FadeOut(layer_rows),
                        FadeOut(title_local),
                        FadeOut(graph_local),
                        FadeOut(labels_local),
                        run_time=0.8,
                    )
                else:
                    self.play(
                        FadeOut(title_local),
                        FadeOut(graph_local),
                        FadeOut(labels_local),
                        run_time=0.8,
                    )
            else:
                self.play(
                    FadeOut(queue_label),
                    FadeOut(queue_container),
                    FadeOut(queue_inner),
                    FadeOut(visited_label),
                    FadeOut(visited_items_local),
                    FadeOut(dist_label),
                    FadeOut(dist_container),
                    FadeOut(dist_inner),
                    FadeOut(dist_items),
                    FadeOut(traversal_summary),
                    FadeOut(title_local),
                    FadeOut(graph_local),
                    FadeOut(labels_local),
                    run_time=0.8,
                )
            return traversal_local

        # 2) BFS on the new 8-node graph
        custom_vertices = list(range(8))
        custom_edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (2, 7),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
        ]
        layout_custom = {
            0: LEFT * 4 + UP * 1.8,
            1: LEFT * 2.5 + UP * 1.8,
            2: LEFT * 1.0 + UP * 1.0,
            3: RIGHT * 0.8 + UP * 1.6,
            4: RIGHT * 2.4 + UP * 1.0,
            5: RIGHT * 3.6 + DOWN * 0.4,
            6: RIGHT * 2.0 + DOWN * 1.4,
            7: LEFT * 0.6 + DOWN * 0.4,
        }
        run_queue_bfs(
            r"\text{BFS on custom graph}",
            custom_vertices,
            custom_edges,
            layout_custom,
            start_vertex=0,
            show_bipartite_coloring=True,
            show_layers=True,
        )

        # 3) Run BFS on a non-bipartite triangle (odd cycle) and show why it fails 2-coloring
        triangle_vertices = [1, 2, 3]
        triangle_edges = [(1, 2), (2, 3), (1, 3)]
        layout_triangle = {
            1: LEFT * 2 + DOWN * 0.5,
            2: RIGHT * 2 + DOWN * 0.5,
            3: UP * 1.8,
        }
        run_queue_bfs(
            r"\text{BFS on triangle (odd cycle)}",
            triangle_vertices,
            triangle_edges,
            layout_triangle,
            start_vertex=1,
            show_bipartite_coloring=True,
            explain_non_bipartite=True,
        )

        # ============================================================
        # Summary
        # ============================================================
        summary_title = Text("Summary", font_size=48)
        self.play(FadeIn(summary_title, shift=UP * 0.5), run_time=1.0)
        self.wait(1)
        self.play(summary_title.animate.to_edge(UP), run_time=0.8)

        summary_points = VGroup(
            MathTex(r"\text{BFS: Explores level by level using a queue}", font_size=26),
            MathTex(r"\text{Finds shortest paths in unweighted graphs}", font_size=26),
            MathTex(r"\text{Ideal for level-order exploration and connectivity}", font_size=26),
            MathTex(r"\text{Visits all vertices at distance } k \text{ before } k+1", font_size=26),
            MathTex(r"\text{Bipartite: nodes split into two parts, no odd cycles}", font_size=26),
            MathTex(r"\text{Time complexity: } O(V + E)", font_size=26),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.6)
        self.play(Write(summary_points), run_time=2.5)
        self.wait(1)

        self.play(
            FadeOut(summary_title), FadeOut(summary_points),
            run_time=1.0
        )
        self.wait(1)
