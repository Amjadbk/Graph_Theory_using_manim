from manim import *
import numpy as np

class DFSVisualization(Scene):
    def construct(self):
        # ============================================================
        # Unified Introduction
        # ============================================================
        intro_title = Text("Graph Theory – Depth-First Search (DFS)", font_size=48)
        self.play(FadeIn(intro_title, shift=UP * 0.5), run_time=0.75)
        self.wait(0.5)
        self.play(FadeOut(intro_title, shift=UP * 0.5), run_time=0.4)

        # ============================================================
        # Recursive DFS Section
        # ============================================================
        # Graph setup - bigger scale, matching main.py colors
        vertices = [0, 1, 2, 3, 4, 5, 6]
        edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 6)]
        
        # Custom layout - balanced spacing
        layout = {
            0: UP * 2.2,
            1: LEFT * 2.0 + UP * 0.8,
            2: RIGHT * 2.0 + UP * 0.8,
            3: LEFT * 3.0 + DOWN * 0.8,
            4: LEFT * 0.4 + DOWN * 1.2,
            5: RIGHT * 3.0 + DOWN * 0.8,
            6: DOWN * 2.2,
        }
        
        # Palette & timing tuned to match dijk.py
        EDGE_COLOR = WHITE
        EDGE_HIGHLIGHT = "#FF6B6B"  # vibrant red highlight
        NODE_ACTIVE = "#FFD54F"     # warm gold
        NODE_VISITED = "#34C759"    # rich green
        WAVE_COLOR = BLUE
        T_NODE = 0.5
        T_EDGE = 0.425
        T_PUSH = 0.35
        T_POP = 0.3
        T_VISITED = 0.425
        T_MOVE_LABEL = 0.25
        T_WAVE = 0.35

        # Match main.py vertex style
        vertex_style = {
            "radius": 0.22,
            "fill_color": WHITE,
            "stroke_color": WHITE,
            "stroke_width": 2,
        }
        
        # Match main.py edge style
        edge_width = 3
        edge_style = {
            "stroke_color": EDGE_COLOR,
            "stroke_width": edge_width,
        }
        
        # Create graph
        graph = Graph(
            vertices,
            edges,
            layout=layout,
            vertex_config=vertex_style,
            edge_config=edge_style,
        )
        
        # Add labels to nodes - matching main.py style (MathTex)
        node_labels = VGroup()
        for v in vertices:
            label = MathTex(str(v), font_size=20, color=BLACK)
            label.move_to(graph.vertices[v].get_center())
            node_labels.add(label)
        
        # ============================================================
        # DFS Algorithm Steps
        # ============================================================
        dfs_algo_title = Text("DFS Algorithm", font_size=40).to_edge(UP)
        self.play(Write(dfs_algo_title), run_time=0.6)
        
        dfs_algo_text = VGroup(
            MathTex(r"\text{1. Start at a source vertex (push to stack).}", font_size=24),
            MathTex(r"\text{2. Mark current vertex as visited.}", font_size=24),
            MathTex(r"\text{3. Explore unvisited neighbors (push to stack).}", font_size=24),
            MathTex(r"\text{4. When no unvisited neighbors, backtrack (pop from stack).}", font_size=24),
            MathTex(r"\text{5. Repeat until stack is empty.}", font_size=24),
            MathTex(r"\text{6. DFS explores as deep as possible before backtracking.}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        dfs_algo_text.next_to(dfs_algo_title, DOWN, buff=0.4)
        self.play(Write(dfs_algo_text), run_time=1.875)
        self.wait(0.5)
        
        self.play(
            FadeOut(dfs_algo_title), FadeOut(dfs_algo_text),
            run_time=0.6
        )
        
        # Title - smaller
        title = MathTex(r"\text{Depth-First Search (DFS) with Stack}", font_size=28).to_edge(UP, buff=0.3)
        self.play(Create(graph), Write(node_labels), run_time=1.1)
        self.wait(0.5)
        self.play(Write(title), run_time=0.75)
        self.wait(0.5)
        
        # Stack visualization setup - professional design
        stack_label = MathTex(r"\text{Call Stack}", font_size=22)
        stack_label.to_edge(LEFT, buff=0.4).shift(UP * 1.8)
        
        # Professional stack container with border and background
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
        
        # Add a subtle inner border for professional look
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
            run_time=0.9
        )
        self.wait(0.5)
        
        # Visited set visualization - smaller
        visited_label = MathTex(r"\text{Visited:}", font_size=18)
        visited_label.next_to(stack_container, DOWN, buff=0.3)
        visited_label.align_to(stack_label, LEFT)
        
        self.play(Write(visited_label), run_time=0.25)
        self.wait(0.5)
        
        # DFS implementation
        visited = set()
        stack_items = VGroup()
        visited_items = VGroup()
        traversal_order = []  # Track the order nodes were visited
        move_label = [None]  # holder for showing "u -> v"
        tree_edges = []
        current_node_indicator = None  # Visual indicator for current node
        stack_node_map = {}  # Map stack items to node numbers for red dot tracking

        # Helper: show edge wave + move text
        def show_move(parent, child):
            if parent is None:
                return
            edge_key = (min(parent, child), max(parent, child))
            if edge_key in graph.edges:
                wave = graph.edges[edge_key].copy().set_stroke(WAVE_COLOR, width=edge_width + 2)
                self.play(
                    ShowPassingFlash(wave, time_width=0.9, run_time=T_WAVE, rate_func=linear),
                )
            # update move label
            if move_label[0] is not None:
                self.play(FadeOut(move_label[0], run_time=0.1))
            lbl = MathTex(rf"{parent} \rightarrow {child}", font_size=24, color=WHITE)
            lbl.to_edge(DOWN, buff=0.45)
            move_label[0] = lbl
            self.play(FadeIn(lbl, shift=UP * 0.08), run_time=T_MOVE_LABEL, rate_func=smooth)
        
        def dfs_animation(node, parent=None, depth=0):
            """Recursive DFS with visual stack representation"""
            nonlocal current_node_indicator
            if node in visited:
                return
            
            # Wait 5 seconds before entering new node
            self.wait(0.5)
            
            # Mark as visited
            visited.add(node)
            traversal_order.append(node)  # Track traversal order
            
            # Add to stack (push) - professional styling
            stack_item = Rectangle(
                width=1.9,
                height=0.4,
                stroke_color=BLUE,
                stroke_width=1.5,
                fill_color=BLUE,
                fill_opacity=0.3,
            )
            stack_text = MathTex(rf"\text{{DFS}}({node})", font_size=16, color=WHITE)
            stack_text.move_to(stack_item.get_center())
            stack_item_group = VGroup(stack_item, stack_text)
            
            # Position stack items from bottom to top
            if len(stack_items) == 0:
                stack_item_group.next_to(stack_container.get_bottom(), UP, buff=0.15)
                stack_item_group.align_to(stack_container, LEFT).shift(RIGHT * 0.15)
            else:
                stack_item_group.next_to(stack_items[-1], UP, buff=0.08)
                stack_item_group.align_to(stack_items[-1], LEFT)
            
            stack_items.add(stack_item_group)
            self.add(stack_item_group)
            # Store mapping for red dot tracking
            stack_node_map[stack_item_group] = node
            
            # Animate stack push - smoother, professional
            # Update red dot to show top of stack (current node)
            if current_node_indicator is not None:
                self.remove(current_node_indicator)
            
            # Create and add current node indicator (red dot) on top of stack
            current_node_indicator = Dot(radius=0.12, color=RED)
            current_node_indicator.move_to(graph.vertices[node].get_center())
            self.add(current_node_indicator)
            
            self.play(
                FadeIn(stack_item_group, shift=DOWN * 0.15),
                FadeIn(current_node_indicator, scale=0.5),
                run_time=T_PUSH,
                rate_func=smooth
            )
            self.wait(0.5)
            
            # Highlight current node - matching main.py (YELLOW)
            self.play(
                graph.vertices[node].animate.set_fill(NODE_ACTIVE),
                node_labels[node].animate.set_color(BLACK),
                run_time=T_NODE,
                rate_func=smooth
            )
            
            # Highlight edge from parent if exists - matching main.py (RED for highlights)
            if parent is not None:
                edge_key = (min(parent, node), max(parent, node))
                if edge_key in graph.edges:
                    show_move(parent, node)
                    self.play(
                        graph.edges[edge_key].animate.set_stroke(
                            color=EDGE_HIGHLIGHT,
                            width=edge_width + 1.5
                        ),
                        run_time=T_EDGE,
                        rate_func=smooth
                    )
                    self.wait(0.5)
            
            self.wait(0.5)
            
            # Add to visited set visualization - matching main.py style
            visited_item = MathTex(str(node), font_size=16, color=BLUE)
            if len(visited_items) == 0:
                visited_item.next_to(visited_label, DOWN, buff=0.2)
                visited_item.align_to(visited_label, LEFT).shift(RIGHT * 0.3)
            else:
                visited_item.next_to(visited_items[-1], RIGHT, buff=0.3)
                visited_item.align_to(visited_items[-1], DOWN)
            
            visited_items.add(visited_item)
            self.add(visited_item)
            
            # Node fully visited: color it green and keep the label visible
            self.play(
                FadeIn(visited_item, scale=0.9),
                graph.vertices[node].animate.set_fill(NODE_VISITED),
                node_labels[node].animate.set_color(WHITE),
                run_time=T_VISITED,
                rate_func=smooth
            )
            
            self.wait(0.5)
            
            # Explore neighbors
            neighbors = []
            for edge in edges:
                if edge[0] == node and edge[1] not in visited:
                    neighbors.append(edge[1])
                elif edge[1] == node and edge[0] not in visited:
                    neighbors.append(edge[0])
            
            # Sort neighbors for consistent traversal
            # Special case: at node 1, visit 4 before 3 to get correct spanning tree edge (1,4) instead of (4,6)
            if node == 1 and 3 in neighbors and 4 in neighbors:
                neighbors = [4, 3] + [n for n in neighbors if n not in [3, 4]]
            else:
                neighbors.sort()
            
            for neighbor in neighbors:
                # Double-check neighbor is still unvisited (may have been visited in recursive call)
                if neighbor not in visited:
                    # Keep parent->child direction for arrow orientation
                    tree_edges.append((node, neighbor))
                    # Recursive call visualization
                    dfs_animation(neighbor, node, depth + 1)
            
            # Pop from stack (return from recursive call) - smoother
            if len(stack_items) > 0:
                item_to_remove = stack_items[-1]
                stack_items.remove(item_to_remove)
                # Remove from map
                if item_to_remove in stack_node_map:
                    del stack_node_map[item_to_remove]
                
                self.play(
                    FadeOut(item_to_remove, shift=UP * 0.2),
                    run_time=T_POP,
                    rate_func=smooth
                )
                self.remove(item_to_remove)
                self.wait(0.5)
                
                # Update red dot to show new top of stack (if stack not empty)
                if current_node_indicator is not None:
                    self.remove(current_node_indicator)
                    current_node_indicator = None
                
                # If stack still has items, show red dot on the new top
                if len(stack_items) > 0:
                    # Get node number from the top stack item using our map
                    top_stack_item = stack_items[-1]
                    if top_stack_item in stack_node_map:
                        top_node = stack_node_map[top_stack_item]
                        current_node_indicator = Dot(radius=0.12, color=RED)
                        current_node_indicator.move_to(graph.vertices[top_node].get_center())
                        self.add(current_node_indicator)
                        self.play(FadeIn(current_node_indicator, scale=0.5), run_time=0.15)
                
                # Restore edge color if returning - matching main.py (WHITE)
                if parent is not None:
                    edge_key = (min(parent, node), max(parent, node))
                    if edge_key in graph.edges:
                        self.play(
                            graph.edges[edge_key].animate.set_stroke(
                                color=WHITE,
                                width=edge_width
                            ),
                            run_time=0.2,
                            rate_func=smooth
                        )
                        self.wait(0.5)
        
        # Run DFS
        dfs_animation(0)
        
        self.wait(0.5)
        
        # Fade out move label before showing summary
        if move_label[0] is not None:
            self.play(FadeOut(move_label[0]), run_time=0.25)
            move_label[0] = None  # Clear reference to prevent double fade
        self.wait(0.5)
        
        # Summary - positioned at middle bottom of slide
        summary = VGroup(
            MathTex(r"\text{Traversal Order:}", font_size=18),
            MathTex(r" \to ".join([str(v) for v in traversal_order]), font_size=16, color=WHITE)
        ).arrange(DOWN, buff=0.2)
        summary.to_edge(DOWN, buff=0.3)  # Position lower at bottom
        
        self.play(Write(summary), run_time=0.6)
        self.wait(0.5)

        # Keep the original graph; move it left and build spanning tree on the right
        fade_anims = [
            FadeOut(stack_label),
            FadeOut(stack_container),
            FadeOut(stack_inner),
            FadeOut(visited_label),
            FadeOut(visited_items),
            FadeOut(stack_items),
            FadeOut(summary),
            FadeOut(title),
        ]
        if move_label[0] is not None:
            fade_anims.append(FadeOut(move_label[0]))
        self.play(*fade_anims)

        shift_vec = LEFT * 3
        self.play(
            graph.animate.shift(shift_vec).scale(0.7),
            node_labels.animate.shift(shift_vec).scale(0.7),
            run_time=0.4,
            rate_func=smooth,
        )

        tree_graph = DiGraph(
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
        tree_title = MathTex(r"\text{DFS Spanning Tree}", font_size=26).next_to(tree_graph, UP, buff=0.25)

        self.play(Create(tree_graph), Write(tree_labels), Write(base_title), Write(tree_title), run_time=0.75, rate_func=smooth)
        self.wait(0.5)

        # Transfer spanning-tree edges with effects
        for e in tree_edges:
            edge_key = (min(e[0], e[1]), max(e[0], e[1]))
            if edge_key not in graph.edges:
                continue
            wave = graph.edges[edge_key].copy().set_stroke(WAVE_COLOR, width=edge_width + 2)
            tree_graph.add_edges(
                e,
                edge_config={
                    "stroke_color": EDGE_COLOR,
                    "stroke_width": edge_width,
                    "tip_length": 0.25,
                },
                edge_type=Arrow,
            )
            new_edge = tree_graph.edges[e]
            # Hide full Arrow (line + head) until animation
            new_edge.set_opacity(0)
            # Ensure tip is also hidden if it exists as a separate component
            for submob in new_edge.submobjects:
                submob.set_opacity(0)

            anims = [
                ShowPassingFlash(wave, time_width=0.9, run_time=0.35, rate_func=linear),
                new_edge.animate.set_opacity(1),
            ]
            # Animate all submobjects (including tip) to visible
            for submob in new_edge.submobjects:
                anims.append(submob.animate.set_opacity(1))

            self.play(*anims, run_time=0.425, rate_func=smooth)
            self.wait(0.5)
        
        self.wait(0.5)
        self.play(
            FadeOut(tree_graph),
            FadeOut(tree_labels),
            FadeOut(base_title),
            FadeOut(tree_title),
            FadeOut(graph),
            FadeOut(node_labels),
            run_time=0.5,
        )

        self.wait(0.5)

        # ============================================================
        # Batman Sticker Slide
        # ============================================================
        # Load batman image (user should place batman.jpg in project folder)
        # If image doesn't exist, it will show an error, but we'll handle it gracefully
        try:
            batman_img = ImageMobject("assets/batman.jpg")
            batman_img.scale(1.5)
            batman_img.move_to(ORIGIN)
            self.play(FadeIn(batman_img), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(batman_img), run_time=1.0)
        except:
            # If image not found, show a placeholder text
            batman_text = Text("🦇 BATMAN 🦇", font_size=64, color=YELLOW)
            self.play(FadeIn(batman_text), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(batman_text), run_time=1.0)

        # ============================================================
        # Iterative DFS Section
        # ============================================================
        # Iterative DFS Algorithm Steps (separate slide)
        iter_dfs_algo_title = Text("Iterative DFS Algorithm", font_size=40).to_edge(UP)
        iter_dfs_algo_text = VGroup(
            MathTex(r"\text{1. Start at source vertex (push to stack).}", font_size=24),
            MathTex(r"\text{2. While stack is not empty:}", font_size=24),
            MathTex(r"\text{   - Pop vertex from stack.}", font_size=24),
            MathTex(r"\text{   - If not visited, mark as visited.}", font_size=24),
            MathTex(r"\text{   - Push all unvisited neighbors to stack.}", font_size=24),
            MathTex(r"\text{3. Continue until stack is empty.}", font_size=24),
            MathTex(r"\text{4. Uses explicit stack instead of recursion.}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        iter_dfs_algo_text.next_to(iter_dfs_algo_title, DOWN, buff=0.4)
        self.play(Write(iter_dfs_algo_title), run_time=1.2)
        self.play(Write(iter_dfs_algo_text), run_time=4.0)
        self.wait(1)
        self.play(
            FadeOut(iter_dfs_algo_title),
            FadeOut(iter_dfs_algo_text),
            run_time=1.0,
        )

        # Graph setup (same palette/scale as dfs.py)
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

        # Title
        title = MathTex(r"\text{DFS (Iterative Stack)}", font_size=28).to_edge(UP, buff=0.3)
        self.play(Create(graph), Write(node_labels), run_time=2.2)
        self.wait(1)
        self.play(Write(title), run_time=1.5)
        self.wait(1)

        # Stack UI (professional look)
        stack_label = MathTex(r"\text{Call Stack}", font_size=22)
        stack_label.to_edge(LEFT, buff=0.4).shift(UP * 1.8)

        stack_container = Rectangle(
            width=2.2,
            height=3.2,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_opacity=0.05,
            fill_color=BLUE,
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

        self.play(Write(stack_label), Create(stack_container), Create(stack_inner), run_time=2.5)
        self.wait(1)

        # Visited list
        visited_label = MathTex(r"\text{Visited:}", font_size=18)
        visited_label.next_to(stack_container, DOWN, buff=0.3)
        visited_label.align_to(stack_label, LEFT)
        self.play(Write(visited_label), run_time=0.5)
        self.wait(1)

        # Palette & timing harmonized with dijk.py
        EDGE_COLOR = WHITE
        EDGE_HIGHLIGHT = "#FF6B6B"
        NODE_ACTIVE = "#FFD54F"
        NODE_VISITED = "#34C759"
        NODE_QUEUED = "#5FA8FF"
        WAVE_COLOR = BLUE
        T_NODE = 1.0
        T_VISITED = 0.85
        T_WAVE = 0.7
        T_PUSH = 0.6
        T_POP = 0.6
        T_EDGE = 0.85
        T_MOVE_LABEL = 0.5

        visited_items = VGroup()
        stack_items = VGroup()
        traversal_order = []
        in_stack = set()
        tree_edges = []
        move_label = [None]  # holder for "u -> v"
        current_node_indicator = None  # Red dot to show current node

        # Helper: show edge wave + move text
        def show_move(parent, child):
            if parent is None:
                return
            edge_key = (min(parent, child), max(parent, child))
            if edge_key in graph.edges:
                wave = graph.edges[edge_key].copy().set_stroke(WAVE_COLOR, width=edge_width + 2)
                self.play(
                    ShowPassingFlash(wave, time_width=0.9, run_time=T_WAVE, rate_func=linear),
                )
            if move_label[0] is not None:
                self.play(FadeOut(move_label[0], run_time=0.2))
            lbl = MathTex(rf"{parent} \rightarrow {child}", font_size=24, color=WHITE)
            lbl.to_edge(DOWN, buff=0.45)
            move_label[0] = lbl
            self.play(FadeIn(lbl, shift=UP * 0.08), run_time=T_MOVE_LABEL, rate_func=smooth)

        # Helper to push onto visual stack
        def push_stack(text, node_id=None, animate=True):
            # Skip if already visited or already scheduled
            if node_id is not None:
                if node_id in visited or node_id in in_stack:
                    return
            item_box = Rectangle(
                width=1.9,
                height=0.4,
                stroke_color=BLUE,
                stroke_width=1.5,
                fill_color=BLUE,
                fill_opacity=0.3,
            )
            item_txt = MathTex(text, font_size=16, color=WHITE)
            item_txt.move_to(item_box.get_center())
            group = VGroup(item_box, item_txt)

            # Position group at final location first
            if len(stack_items) == 0:
                group.next_to(stack_container.get_bottom(), UP, buff=0.15)
                group.align_to(stack_container, LEFT).shift(RIGHT * 0.15)
            else:
                group.next_to(stack_items[-1], UP, buff=0.08)
                group.align_to(stack_items[-1], LEFT)

            # Store target position and transform for smooth entrance
            target_pos = group.get_center()
            target_scale = 1.0
            
            # Start from below, smaller, and transparent
            group.move_to(target_pos + DOWN * 0.3)
            group.scale(0.75)
            group.set_opacity(0)
            
            stack_items.add(group)
            self.add(group)
            
            # Smooth appearance animation: move up, scale up, fade in
            if animate:
                self.play(
                    group.animate.move_to(target_pos).scale(1/0.75).set_opacity(1),
                    run_time=0.5,
                    rate_func=smooth,
                )
            else:
                # For batch animation, just set final state
                group.move_to(target_pos)
                group.scale(1/0.75)
                group.set_opacity(1)

            # If a node is associated and not yet visited, give it a subtle queued color
            if node_id is not None and node_id not in visited:
                color_anim = AnimationGroup(
                    graph.vertices[node_id].animate.set_fill("#4A90E2"),
                    node_labels[node_id].animate.set_color(WHITE),
                    run_time=0.3,
                    rate_func=smooth,
                )
                in_stack.add(node_id)
            else:
                color_anim = None

            return None, color_anim

        # Helper to pop from visual stack
        def pop_stack(node_id=None):
            if len(stack_items) == 0:
                return None
            grp = stack_items[-1]
            stack_items.remove(grp)
            # Smooth pop animation: scale down and fade out while moving up
            self.play(
                grp.animate.scale(0.7).set_opacity(0).shift(UP * 0.4),
                run_time=0.4,
                rate_func=smooth,
            )
            self.remove(grp)
            if node_id is not None:
                in_stack.discard(node_id)
            return grp

        # Build adjacency list
        adj = {v: [] for v in vertices}
        for u, v in edges:
            adj[u].append(v)
            adj[v].append(u)
        for v in adj:
            adj[v].sort()

        visited = set()
        stack = [(0, None)]  # (node, parent)
        in_stack.add(0)

        # Initial stack push
        push_stack("DFS(0)", node_id=0)

        while stack:
            # Wait 5 seconds before entering new node and erasing it from stack
            self.wait(1)
            node, parent = stack.pop()
            pop_stack(node_id=node)

            if node in visited:
                continue

            # Visit node
            visited.add(node)
            in_stack.discard(node)
            traversal_order.append(node)
            show_move(parent, node)
            
            # Keep red dot on the node we are actively exploring
            if current_node_indicator is not None:
                self.remove(current_node_indicator)
            current_node_indicator = Dot(radius=0.12, color=RED, fill_opacity=1.0)
            current_node_indicator.move_to(graph.vertices[node].get_center())
            self.add(current_node_indicator)
            self.play(FadeIn(current_node_indicator, scale=0.5), run_time=0.2)

            self.play(
                graph.vertices[node].animate.set_fill("#FFD54F"),
                node_labels[node].animate.set_color(BLACK),
                run_time=T_NODE,
                rate_func=smooth,
            )
            self.wait(1)

            # Edge highlight
            if parent is not None:
                edge_key = (min(parent, node), max(parent, node))
                if edge_key in graph.edges:
                    self.play(
                        graph.edges[edge_key].animate.set_stroke(color="#FF6B6B", width=edge_width + 1.5),
                        run_time=T_EDGE,
                        rate_func=smooth,
                    )

            # Mark visited (final color green)
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
                run_time=T_VISITED,
                rate_func=smooth,
            )
            self.wait(1)

            # Push neighbors (reverse order so smallest processed first) if not visited and not already stacked
            batch_anims = []
            neighbors_to_push = []
            stack_start_len = len(stack_items)
            
            for nbr in reversed(adj[node]):
                if nbr not in visited and nbr not in in_stack:
                    stack.append((nbr, node))
                    tree_edges.append((min(node, nbr), max(node, nbr)))
                    neighbors_to_push.append(nbr)
            
            # Push all neighbors (they're already positioned but invisible)
            for nbr in neighbors_to_push:
                _, color_anim = push_stack(f"DFS({nbr})", node_id=nbr, animate=False)
                if color_anim:
                    batch_anims.append(color_anim)
            
            # Animate all newly added stack items appearing with staggered timing
            if neighbors_to_push:
                # Get the groups that were just added (from stack_start_len to end)
                new_stack_groups = []
                for i in range(stack_start_len, len(stack_items)):
                    new_stack_groups.append(stack_items[i])
                
                for grp in new_stack_groups:
                    target_pos = grp.get_center()
                    # Reset to start position for animation
                    grp.move_to(target_pos + DOWN * 0.3)
                    grp.scale(0.75)
                    grp.set_opacity(0)
                    batch_anims.append(
                        grp.animate.move_to(target_pos).scale(1/0.75).set_opacity(1)
                    )
            
            if batch_anims:
                self.play(
                    AnimationGroup(*batch_anims, lag_ratio=0.12),
                    run_time=0.7,
                    rate_func=smooth,
                )

            # After processing neighbors, if we colored queued nodes and never visit them (already visited), ensure label readable
            for nbr in adj[node]:
                if nbr in visited:
                    # keep their final colors/labels intact
                    continue
        
        # Clean up any remaining indicator
        if current_node_indicator is not None:
            self.remove(current_node_indicator)
            current_node_indicator = None

        self.wait(1)
        
        # Fade out move label before showing summary
        if move_label[0] is not None:
            self.play(FadeOut(move_label[0]), run_time=0.5)
            move_label[0] = None  # Clear reference to prevent double fade
        
        summary = VGroup(
            MathTex(r"\text{Traversal Order:}", font_size=18),
            MathTex(r" \to ".join(str(v) for v in traversal_order), font_size=16, color=WHITE),
        ).arrange(DOWN, buff=0.2)
        summary.to_edge(DOWN, buff=0.3)  # Position lower at bottom
        self.play(Write(summary), run_time=1.2)
        self.wait(1)

        # Slide: keep original graph, move it left, build spanning tree on the right edge-by-edge
        fade_anims = [
            FadeOut(stack_label),
            FadeOut(stack_container),
            FadeOut(stack_inner),
            FadeOut(visited_label),
            FadeOut(visited_items),
            FadeOut(stack_items),
            FadeOut(summary),
            FadeOut(title),
        ]
        if move_label[0] is not None:
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
        tree_title = MathTex(r"\text{DFS Spanning Tree}", font_size=26).next_to(tree_graph, UP, buff=0.25)

        self.play(Create(tree_graph), Write(tree_labels), Write(base_title), Write(tree_title), run_time=1.5, rate_func=smooth)

        for e in tree_edges:
            if e not in graph.edges:
                continue
            wave = graph.edges[e].copy().set_stroke(WAVE_COLOR, width=edge_width + 2)
            tree_graph.add_edges(e, edge_config={"stroke_color": EDGE_COLOR, "stroke_width": edge_width, "tip_length": 0.25}, edge_type=Arrow)
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

        self.wait(1)

        # ============================================================
        # Unified Summary
        # ============================================================
        summary_title = Text("Summary", font_size=48)
        self.play(FadeIn(summary_title, shift=UP * 0.5), run_time=1.0)
        self.wait(1)
        self.play(summary_title.animate.to_edge(UP), run_time=0.8)

        summary_points = VGroup(
            MathTex(r"\text{DFS: Explores as far as possible before backtracking}", font_size=26),
            MathTex(r"\text{Recursive DFS: Uses function call stack}", font_size=26),
            MathTex(r"\text{Iterative DFS: Uses explicit stack instead of recursion}", font_size=26),
            MathTex(r"\text{Iterative DFS avoids recursion depth limits}", font_size=26),
            MathTex(r"\text{Great for deep exploration (paths, components)}", font_size=26),
            MathTex(r"\text{Useful for cycle detection, topological sorts}", font_size=26),
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
