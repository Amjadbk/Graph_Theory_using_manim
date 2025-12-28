"""
Dijkstra's Algorithm Visualization

This module provides animated visualizations of Dijkstra's shortest path algorithm,
demonstrating how to find the shortest paths from a source vertex to all other
vertices in a weighted graph.

The visualization includes:
- Priority queue explanation and visualization
- Step-by-step distance updates
- Path reconstruction
- Multiple example graphs
"""

from manim import *
import numpy as np
import heapq


class DijkstraVisualization(Scene):
    """
    Visualizes Dijkstra's algorithm for finding shortest paths in weighted graphs.
    
    Dijkstra's algorithm uses a priority queue to systematically explore vertices
    in order of increasing distance from the source, guaranteeing shortest paths
    for non-negative edge weights.
    """
    
    def run_dijkstra_example(self, vertices, edges, edge_weights, layout, example_num):
        """
        Run a complete Dijkstra's algorithm visualization for a given graph.
        
        Args:
            vertices: List of vertex identifiers
            edges: List of (u, v) tuples representing edges
            edge_weights: Dictionary mapping edges to their weights
            layout: Dictionary mapping vertices to their (x, y) positions
            example_num: Example number for title display
        """
        
        # ============================================================
        # Configuration: Visual Styles and Animation Timing
        # Define colors, styles, and timing constants for smooth animations
        # ============================================================
        EDGE_COLOR = WHITE
        EDGE_HIGHLIGHT = "#FF6B6B"  # vibrant red highlight
        NODE_ACTIVE = "#FFD54F"     # warm gold
        NODE_VISITED = "#34C759"    # rich green
        WAVE_COLOR = BLUE
        T_NODE = 1.0
        T_EDGE = 0.85
        T_RELAX = 1.0
        T_VISITED = 0.85
        T_MOVE_LABEL = 0.5
        T_WAVE = 0.7
        T_DIST_UPDATE = 0.85

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
        
        # Add edge weight labels with background to avoid overlapping edges
        weight_labels = VGroup()
        for edge in edges:
            u, v = edge
            weight = edge_weights[edge]
            # Position weight label at midpoint of edge, offset perpendicularly
            edge_mid = (graph.vertices[u].get_center() + graph.vertices[v].get_center()) / 2
            # Calculate perpendicular direction to offset label
            edge_dir = graph.vertices[v].get_center() - graph.vertices[u].get_center()
            edge_dir_norm = np.linalg.norm(edge_dir)
            if edge_dir_norm > 0:
                perp = np.array([-edge_dir[1], edge_dir[0], 0]) / edge_dir_norm * 0.3
            else:
                perp = UP * 0.3
            weight_label = MathTex(str(weight), font_size=18, color=YELLOW)
            weight_label.move_to(edge_mid + perp)
            # Add background rectangle to make weight visible
            bg = BackgroundRectangle(weight_label, color=BLACK, fill_opacity=0.7, buff=0.05)
            weight_group = VGroup(bg, weight_label)
            weight_labels.add(weight_group)
        
        # Title
        title = MathTex(rf"\text{{Dijkstra's Algorithm - Example {example_num}}}", font_size=28).to_edge(UP, buff=0.3)
        # Graph stays in center (no shift needed)
        self.play(Create(graph), Write(node_labels), Write(weight_labels), run_time=2.2)
        self.wait(1)
        self.play(Write(title), run_time=1.5)
        self.wait(1)
        
        # Distance table visualization setup - bigger, on the left
        dist_label = MathTex(r"\text{Distances}", font_size=18)
        dist_label.to_edge(LEFT, buff=0.3).shift(UP * 1.8)
        
        # Bigger distance table container
        dist_container = Rectangle(
            width=2.2,
            height=3.2,
            stroke_color=BLUE,
            stroke_width=2,
            fill_opacity=0.05,
            fill_color=BLUE
        )
        dist_container.next_to(dist_label, DOWN, buff=0.2)
        dist_container.align_to(dist_label, LEFT)
        
        # Add a subtle inner border
        dist_inner = Rectangle(
            width=2.0,
            height=3.0,
            stroke_color=BLUE,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        dist_inner.move_to(dist_container.get_center())
        
        # Priority Queue UI on the right (matching BFS queue style)
        pq_label = MathTex(r"\text{Priority Queue}", font_size=22)
        pq_label.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)

        pq_container = Rectangle(
            width=1.8,
            height=3.2,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_opacity=0.05,
            fill_color=BLUE,
        )
        pq_container.next_to(pq_label, DOWN, buff=0.25)
        pq_container.align_to(pq_label, LEFT)

        pq_inner = Rectangle(
            width=1.6,
            height=3.0,
            stroke_color=BLUE,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        pq_inner.move_to(pq_container.get_center())
        
        self.play(
            Write(dist_label),
            Create(dist_container),
            Create(dist_inner),
            Write(pq_label),
            Create(pq_container),
            Create(pq_inner),
            run_time=1.8
        )
        self.wait(1)
        
        # Initialize distance table entries
        distances = {v: float('inf') for v in vertices}
        distances[0] = 0  # Source node
        
        dist_entries = {}  # Store visual elements for each distance entry
        all_dist_text_objects = []  # Track ALL distance text objects ever created (including transformed ones)
        dist_items = VGroup()
        
        # Create initial distance entries (bigger font to fit rectangle)
        for i, v in enumerate(vertices):
            node_text = MathTex(rf"d[{v}]", font_size=22, color=WHITE)
            dist_text = MathTex(r"\infty", font_size=22, color=WHITE) if distances[v] == float('inf') else MathTex(str(distances[v]), font_size=22, color=WHITE)
            
            entry_group = VGroup(node_text, dist_text).arrange(RIGHT, buff=0.3)
            
            if i == 0:
                entry_group.next_to(dist_container.get_top(), DOWN, buff=0.2)
                entry_group.align_to(dist_container, LEFT).shift(RIGHT * 0.2)
            else:
                entry_group.next_to(dist_items[-1], DOWN, buff=0.2)
                entry_group.align_to(dist_items[-1], LEFT)
            
            dist_items.add(entry_group)
            dist_entries[v] = dist_text
            all_dist_text_objects.append(dist_text)  # Track initial distance text
            self.add(entry_group)
        
        self.play(FadeIn(dist_items), run_time=1.5)
        self.wait(1)
        
        # Visited set visualization
        visited_label = MathTex(r"\text{Visited:}", font_size=14)
        visited_label.next_to(dist_container, DOWN, buff=0.3)
        visited_label.align_to(dist_label, LEFT)
        
        self.play(Write(visited_label), run_time=0.5)
        self.wait(1)
        
        # Dijkstra implementation
        visited = set()
        visited_items = VGroup()
        traversal_order = []  # Track the order nodes were visited
        move_label = [None]  # holder for showing "u -> v"
        tree_edges = []
        parent = {}  # Track parent for shortest path tree
        pq_items = []  # Visual items in priority queue
        in_pq = set()  # Track which nodes are in priority queue
        current_node_indicator = None  # Red dot to show current node
        
        # Build adjacency list with weights
        adj = {v: [] for v in vertices}
        for (u, v) in edges:
            weight = edge_weights[(u, v)]
            adj[u].append((v, weight))
            adj[v].append((u, weight))
        
        # Helper: show edge wave + move text
        def show_move(u, v, weight):
            edge_key = (min(u, v), max(u, v))
            if edge_key in graph.edges:
                wave = graph.edges[edge_key].copy().set_stroke(WAVE_COLOR, width=edge_width + 2)
                self.play(
                    ShowPassingFlash(wave, time_width=0.9, run_time=T_WAVE, rate_func=linear),
                )
            # update move label - position at bottom edge, well below graph
            if move_label[0] is not None:
                self.play(FadeOut(move_label[0], run_time=0.2))
            lbl = MathTex(rf"{u} \rightarrow {v} \ (\text{{weight}} = {weight})", font_size=22, color=WHITE)
            lbl.to_edge(DOWN, buff=1.0)  # Position well below graph
            move_label[0] = lbl
            self.play(FadeIn(lbl, shift=UP * 0.08), run_time=T_MOVE_LABEL, rate_func=smooth)
        
        # Helper: reposition priority queue items (min distance on top)
        def layout_pq():
            x_mid = pq_inner.get_center()[0]
            y_start = pq_inner.get_top()[1] - 0.3
            for i, (item, _) in enumerate(pq_items):
                target = np.array([x_mid, y_start - i * 0.7, 0])
                self.play(item.animate.move_to(target), run_time=0.2, rate_func=smooth)
        
        # Enqueue helper for priority queue
        def enqueue_pq(dist, node):
            if node in visited:
                return
            # Check if node already in queue - if so, update it
            for i, (item, (d, n)) in enumerate(pq_items):
                if n == node:
                    # Remove old item
                    old_item, _ = pq_items.pop(i)
                    self.play(FadeOut(old_item, shift=DOWN * 0.2), run_time=0.2, rate_func=smooth)
                    layout_pq()
                    break
            
            # Create the new item but don't add it to scene yet
            box = Rectangle(
                width=0.7,
                height=0.6,
                stroke_color=BLUE,
                stroke_width=1.5,
                fill_color=BLUE,
                fill_opacity=0.3,
            )
            # Show (distance, node) in the box
            dist_str = str(int(dist)) if dist != float('inf') else r"\infty"
            txt = MathTex(rf"({dist_str},{node})", font_size=14, color=WHITE)
            txt.move_to(box.get_center())
            group = VGroup(box, txt)
            new_item_data = (dist, node)
            
            # Temporarily add new item to list and sort to find final positions
            temp_items = pq_items + [(None, new_item_data)]  # None as placeholder for visual item
            temp_items.sort(key=lambda x: (x[1][0], x[1][1]))
            
            # Find the index where new item will be inserted
            insert_index = next(i for i, (_, (d, n)) in enumerate(temp_items) if n == node)
            
            # Calculate final positions for all items
            x_mid = pq_inner.get_center()[0]
            y_start = pq_inner.get_top()[1] - 0.3
            
            # First, shift all existing items to their final positions
            anims = []
            for item, data in pq_items:
                # Find where this item will be in the sorted list
                final_index = next(i for i, (_, (d, n)) in enumerate(temp_items) if (d, n) == data)
                target = np.array([x_mid, y_start - final_index * 0.7, 0])
                anims.append(item.animate.move_to(target))
            
            # Play all shift animations
            if anims:
                self.play(*anims, run_time=0.3, rate_func=smooth)
            
            # Now add the new item to the list and scene
            pq_items.append((group, new_item_data))
            pq_items.sort(key=lambda x: (x[1][0], x[1][1]))
            
            # Position new item at its correct location (start from bottom, animate to position)
            target_pos = np.array([x_mid, y_start - insert_index * 0.7, 0])
            group.move_to(pq_inner.get_bottom() + UP * 0.3)
            self.add(group)
            self.play(FadeIn(group, shift=UP * 0.1), group.animate.move_to(target_pos), run_time=0.3, rate_func=smooth)
            
            # queue color on node
            if node not in visited:
                self.play(
                    graph.vertices[node].animate.set_fill("#5FA8FF"),
                    node_labels[node].animate.set_color(WHITE),
                    run_time=0.3,
                    rate_func=smooth,
                )
            in_pq.add(node)
        
        # Dequeue helper for priority queue - removes item matching (dist, node)
        def dequeue_pq(dist, node):
            if not pq_items:
                return
            # Find and remove the matching item
            for i, (item, (d, n)) in enumerate(pq_items):
                if d == dist and n == node:
                    removed_item = pq_items.pop(i)[0]
                    self.play(FadeOut(removed_item, shift=UP * 0.2), run_time=0.3, rate_func=smooth)
                    layout_pq()
                    in_pq.discard(node)
                    return
        
        # Priority queue: (distance, node) - properly initialize as heap
        pq = [(0, 0)]  # Start with source node
        heapq.heapify(pq)  # Ensure it's a proper heap
        enqueue_pq(0, 0)  # Add initial node to visual queue
        
        while pq:
            # Wait 5 seconds before entering new node and erasing it from priority queue
            self.wait(1)
            current_dist, u = heapq.heappop(pq)
            dequeue_pq(current_dist, u)  # Remove from visual queue
            
            if u in visited:
                continue
            
            # Mark as visited
            visited.add(u)
            traversal_order.append(u)
            
            # Remove previous indicator if exists
            if current_node_indicator is not None:
                self.remove(current_node_indicator)
                current_node_indicator = None
            
            # Add current node indicator (red dot)
            current_node_indicator = Dot(radius=0.12, color=RED, fill_opacity=1.0)
            current_node_indicator.move_to(graph.vertices[u].get_center())
            self.add(current_node_indicator)
            
            # Highlight current node
            self.play(
                graph.vertices[u].animate.set_fill(NODE_ACTIVE),
                node_labels[u].animate.set_color(BLACK),
                run_time=T_NODE,
                rate_func=smooth
            )
            
            # Update distance display when node is processed
            old_dist = dist_entries[u]
            dist_val = int(distances[u]) if distances[u] != float('inf') else r"\infty"
            new_dist = MathTex(str(dist_val), font_size=22, color=WHITE)
            new_dist.move_to(old_dist.get_center())
            all_dist_text_objects.append(new_dist)  # Track the new transformed object
            
            self.play(
                Transform(old_dist, new_dist),
                run_time=T_DIST_UPDATE,
                rate_func=smooth
            )
            dist_entries[u] = new_dist
            
            self.wait(1)
            
            # Add to visited set visualization
            visited_item = MathTex(str(u), font_size=14, color=BLUE)
            if len(visited_items) == 0:
                visited_item.next_to(visited_label, DOWN, buff=0.15)
                visited_item.align_to(visited_label, LEFT).shift(RIGHT * 0.25)
            else:
                visited_item.next_to(visited_items[-1], RIGHT, buff=0.25)
                visited_item.align_to(visited_items[-1], DOWN)
            
            visited_items.add(visited_item)
            self.add(visited_item)
            
            # Remove current node indicator when marking as visited
            if current_node_indicator is not None:
                self.play(FadeOut(current_node_indicator), run_time=0.2)
                self.remove(current_node_indicator)
                current_node_indicator = None
            
            # Node fully visited: color it green
            self.play(
                FadeIn(visited_item, scale=0.9),
                graph.vertices[u].animate.set_fill(NODE_VISITED),
                node_labels[u].animate.set_color(WHITE),
                run_time=T_VISITED,
                rate_func=smooth
            )
            
            self.wait(1)
            
            # NEW FLOW: Add all unvisited neighbors to priority queue first
            for v, weight in adj[u]:
                if v in visited:
                    continue
                
                edge_key = (min(u, v), max(u, v))
                old_dist_v = distances[v]
                new_dist_v = distances[u] + weight
                
                # Show edge being considered
                show_move(u, v, weight)
                
                if new_dist_v < old_dist_v:
                    # Relaxation: update distance
                    distances[v] = new_dist_v
                    parent[v] = u
                    
                    # Highlight edge
                    self.play(
                        graph.edges[edge_key].animate.set_stroke(
                            color=EDGE_HIGHLIGHT,
                            width=edge_width + 1.5
                        ),
                        run_time=0.4,
                        rate_func=smooth
                    )
                    self.wait(1)
                    
                    # Update distance display with highlight
                    old_dist_text = dist_entries[v]
                    new_dist_text = MathTex(str(int(new_dist_v)), font_size=22, color=YELLOW)
                    new_dist_text.move_to(old_dist_text.get_center())
                    all_dist_text_objects.append(new_dist_text)  # Track yellow highlight
                    
                    self.play(
                        Transform(old_dist_text, new_dist_text),
                        run_time=T_RELAX,
                        rate_func=smooth
                    )
                    self.wait(1)
                    
                    # Change back to white after update
                    final_dist_text = MathTex(str(int(new_dist_v)), font_size=22, color=WHITE)
                    final_dist_text.move_to(old_dist_text.get_center())
                    all_dist_text_objects.append(final_dist_text)  # Track final white text
                    self.play(
                        Transform(old_dist_text, final_dist_text),
                        run_time=0.5
                    )
                    dist_entries[v] = final_dist_text
                    self.wait(1)
                    
                    # Restore edge color
                    self.play(
                        graph.edges[edge_key].animate.set_stroke(
                            color=EDGE_COLOR,
                            width=edge_width
                        ),
                        run_time=0.4,
                        rate_func=smooth
                    )
                    self.wait(1)
                    
                    # Add to priority queue
                    heapq.heappush(pq, (new_dist_v, v))
                    enqueue_pq(new_dist_v, v)  # Add to visual queue
                    self.wait(1)
                else:
                    # Edge considered but not relaxed
                    self.play(
                        graph.edges[edge_key].animate.set_stroke(
                            color=EDGE_HIGHLIGHT,
                            width=edge_width + 1.5
                        ),
                        run_time=0.3,
                        rate_func=smooth
                    )
                    self.wait(1)
                    self.play(
                        graph.edges[edge_key].animate.set_stroke(
                            color=EDGE_COLOR,
                            width=edge_width
                        ),
                        run_time=0.3,
                        rate_func=smooth
                    )
                    self.wait(1)
            
            # Wait after processing all neighbors, before dequeuing next element
            self.wait(1)
        
        self.wait(1)
        
        # Fade out move label
        if move_label[0] is not None:
            self.play(FadeOut(move_label[0]), run_time=0.5)
            move_label[0] = None

        # Fade out all UI elements (distance array, priority queue, weights, etc.)
        fade_anims = [
            FadeOut(dist_label),
            FadeOut(dist_container),
            FadeOut(dist_inner),
            FadeOut(dist_items),
            FadeOut(visited_label),
            FadeOut(visited_items),
            FadeOut(title),
            FadeOut(weight_labels),
            FadeOut(pq_label),
            FadeOut(pq_container),
            FadeOut(pq_inner),
        ]
        if pq_items:
            fade_anims.append(FadeOut(VGroup(*[item for item, _ in pq_items])))
        if move_label[0] is not None:
            fade_anims.append(FadeOut(move_label[0]))
        self.play(*fade_anims)
        
        # Wait for fade out animation to complete
        self.wait(1)
        
        # Now explicitly remove ALL distance-related mobjects from the scene
        # This includes all entry groups, their components, and ALL transformed objects
        all_dist_removals = []
        
        # Add main containers
        all_dist_removals.extend([dist_label, dist_container, dist_inner, dist_items])
        
        # Add all entry groups and recursively get all their submobjects
        for entry_group in dist_items:
            all_dist_removals.append(entry_group)
            # Get all submobjects recursively
            def get_all_submobjects(mob):
                result = [mob]
                if hasattr(mob, 'submobjects'):
                    for submob in mob.submobjects:
                        result.extend(get_all_submobjects(submob))
                return result
            all_dist_removals.extend(get_all_submobjects(entry_group))
        
        # Add ALL distance text objects that were ever created (including transformed ones)
        all_dist_removals.extend(all_dist_text_objects)
        
        # Also add current entries from dist_entries (in case some weren't tracked)
        all_dist_removals.extend(dist_entries.values())
        
        # Remove all collected mobjects
        for mob in all_dist_removals:
            try:
                self.remove(mob)
            except (ValueError, KeyError):
                # Already removed or not in scene, continue
                pass

        # Fade out graph and node labels
        self.play(
            FadeOut(graph),
            FadeOut(node_labels),
            run_time=2.0,
            rate_func=smooth,
        )

        self.wait(1)

    def show_priority_queue_explanation(self):
        """Show priority queue explanation once before examples"""
        # Create temporary UI for explanation
        pq_label = MathTex(r"\text{Priority Queue}", font_size=22)
        pq_label.to_edge(RIGHT, buff=0.4).shift(UP * 1.6)

        pq_container = Rectangle(
            width=1.8,
            height=3.2,
            stroke_color=BLUE,
            stroke_width=2.5,
            fill_opacity=0.05,
            fill_color=BLUE,
        )
        pq_container.next_to(pq_label, DOWN, buff=0.25)
        pq_container.align_to(pq_label, LEFT)

        pq_inner = Rectangle(
            width=1.6,
            height=3.0,
            stroke_color=BLUE,
            stroke_width=1,
            stroke_opacity=0.3,
        )
        pq_inner.move_to(pq_container.get_center())
        
        # Explanation title at the top
        explanation_title = MathTex(r"\text{Priority Queue Explanation}", font_size=28, color=YELLOW)
        explanation_title.to_edge(UP, buff=0.3)
        
        self.play(
            Write(pq_label),
            Create(pq_container),
            Create(pq_inner),
            Write(explanation_title),
            run_time=1.4
        )
        self.wait(1)
        
        # Create example items to demonstrate priority queue behavior
        demo_items = []
        demo_pq_items = []
        
        x_mid = pq_inner.get_center()[0]
        y_start = pq_inner.get_top()[1] - 0.3
        
        # Show explanation text - larger font sizes
        explanation_text1 = MathTex(r"\text{Format: (weight, node)}", font_size=22, color=WHITE)
        explanation_text1.next_to(explanation_title, DOWN, buff=0.4)
        self.play(Write(explanation_text1), run_time=1.0)
        self.wait(1)
        
        explanation_text2 = MathTex(r"\text{Elements ordered by weight (smallest on top)}", font_size=22, color=WHITE)
        explanation_text2.next_to(explanation_text1, DOWN, buff=0.25)
        self.play(Write(explanation_text2), run_time=1.2)
        self.wait(1)
        
        # Create first demo item: (8, 1)
        box1 = Rectangle(width=0.7, height=0.6, stroke_color=BLUE, stroke_width=1.5, fill_color=BLUE, fill_opacity=0.3)
        txt1 = MathTex(r"(8,1)", font_size=14, color=WHITE)
        txt1.move_to(box1.get_center())
        group1 = VGroup(box1, txt1)
        # Show it appearing at bottom first
        group1.move_to(pq_inner.get_bottom() + UP * 0.3)
        demo_items.append((group1, (8, 1)))
        demo_pq_items.append((group1, (8, 1)))
        self.add(group1)
        self.play(FadeIn(group1, shift=UP * 0.1), run_time=0.75)
        self.wait(0.5)
        # Move to top position
        group1.move_to([x_mid, y_start, 0])
        self.play(group1.animate.move_to([x_mid, y_start, 0]), run_time=0.5, rate_func=smooth)
        self.wait(1)
        
        # Create second demo item: (5, 2) - should go to top since 5 < 8
        box2 = Rectangle(width=0.7, height=0.6, stroke_color=BLUE, stroke_width=1.5, fill_color=BLUE, fill_opacity=0.3)
        txt2 = MathTex(r"(5,2)", font_size=14, color=WHITE)
        txt2.move_to(box2.get_center())
        group2 = VGroup(box2, txt2)
        new_item_data2 = (5, 2)
        
        # Show it appearing at bottom first
        group2.move_to(pq_inner.get_bottom() + UP * 0.3)
        self.add(group2)
        self.play(FadeIn(group2, shift=UP * 0.1), run_time=0.75)
        self.wait(0.5)
        
        # Sort and reposition: (5,2) should go to top, (8,1) shifts down
        temp_demo2 = demo_pq_items + [(None, new_item_data2)]
        temp_demo2.sort(key=lambda x: (x[1][0], x[1][1]))
        
        # Move existing item down
        anims2 = []
        for item, data in demo_pq_items:
            final_index = next(j for j, (_, (d, n)) in enumerate(temp_demo2) if (d, n) == data)
            target = np.array([x_mid, y_start - final_index * 0.7, 0])
            anims2.append(item.animate.move_to(target))
        
        # Move new item to top
        insert_index2 = next(i for i, (_, (d, n)) in enumerate(temp_demo2) if n == 2)
        target_pos2 = np.array([x_mid, y_start - insert_index2 * 0.7, 0])
        anims2.append(group2.animate.move_to(target_pos2))
        
        demo_pq_items.append((group2, new_item_data2))
        demo_pq_items.sort(key=lambda x: (x[1][0], x[1][1]))
        
        self.play(*anims2, run_time=1.0, rate_func=smooth)
        self.wait(1)
        
        # Now add a new element with weight 3 (less than existing ones)
        box3 = Rectangle(width=0.7, height=0.6, stroke_color=GREEN, stroke_width=1.5, fill_color=GREEN, fill_opacity=0.3)
        txt3 = MathTex(r"(3,3)", font_size=14, color=WHITE)
        txt3.move_to(box3.get_center())
        group3 = VGroup(box3, txt3)
        new_item_data3 = (3, 3)
        
        # Show it appearing at bottom first
        group3.move_to(pq_inner.get_bottom() + UP * 0.3)
        self.add(group3)
        self.play(FadeIn(group3, shift=UP * 0.1), run_time=0.75)
        self.wait(0.5)
        
        explanation_text3 = MathTex(r"\text{Adding (3,3): weight 3 is smallest}", font_size=22, color=GREEN)
        explanation_text3.next_to(explanation_text2, DOWN, buff=0.25)
        self.play(Write(explanation_text3), run_time=1.0)
        self.wait(0.5)
        
        # Sort and reposition: (3,3) should go to top, others shift down
        temp_demo3 = demo_pq_items + [(None, new_item_data3)]
        temp_demo3.sort(key=lambda x: (x[1][0], x[1][1]))
        
        # Move existing items down
        anims3 = []
        for item, data in demo_pq_items:
            final_index = next(j for j, (_, (d, n)) in enumerate(temp_demo3) if (d, n) == data)
            target = np.array([x_mid, y_start - final_index * 0.7, 0])
            anims3.append(item.animate.move_to(target))
        
        # Move new item to top
        insert_index3 = next(i for i, (_, (d, n)) in enumerate(temp_demo3) if n == 3)
        target_pos3 = np.array([x_mid, y_start - insert_index3 * 0.7, 0])
        anims3.append(group3.animate.move_to(target_pos3))
        
        self.play(*anims3, run_time=1.2, rate_func=smooth)
        self.wait(1)
        
        explanation_text4 = MathTex(r"\text{It moves to top, others shift down}", font_size=22, color=GREEN)
        explanation_text4.next_to(explanation_text3, DOWN, buff=0.25)
        self.play(Write(explanation_text4), run_time=0.8)
        self.wait(1)
        
        # Fade out explanation and demo items
        fade_outs = [
            FadeOut(explanation_title),
            FadeOut(explanation_text1),
            FadeOut(explanation_text2),
            FadeOut(explanation_text3),
            FadeOut(explanation_text4),
            FadeOut(group1),
            FadeOut(group2),
            FadeOut(group3),
            FadeOut(pq_label),
            FadeOut(pq_container),
            FadeOut(pq_inner),
        ]
        self.play(*fade_outs, run_time=1.0)
        self.wait(1)

    def construct(self):
        # ============================================================
        # Introduction
        # ============================================================
        intro_title = Text("Graph Theory – Dijkstra's Algorithm", font_size=48)
        self.play(FadeIn(intro_title, shift=UP * 0.5), run_time=1.5)
        self.wait(1)
        self.play(FadeOut(intro_title, shift=UP * 0.5), run_time=0.8)

        # Add dog.png image
        try:
            dog_img = ImageMobject("assets/dog.png")
            dog_img.scale(1.5)
            dog_img.move_to(ORIGIN)
            self.play(FadeIn(dog_img), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(dog_img), run_time=1.0)
        except:
            # If image not found, show a placeholder text
            dog_text = Text("🐕 DOG 🐕", font_size=64, color=YELLOW)
            self.play(FadeIn(dog_text), run_time=1.5)
            self.wait(2)
            self.play(FadeOut(dog_text), run_time=1.0)

        # Show priority queue explanation once before any examples
        self.show_priority_queue_explanation()

        # ============================================================
        # Dijkstra's Algorithm Steps (shown once after priority queue explanation)
        # ============================================================
        dijk_algo_title = Text("Dijkstra's Algorithm", font_size=40).to_edge(UP)
        self.play(Write(dijk_algo_title), run_time=1.2)
        
        dijk_algo_text = VGroup(
            MathTex(r"\text{1. Initialize distances: source = 0, others = } \infty", font_size=24),
            MathTex(r"\text{2. Add source to priority queue (distance, vertex).}", font_size=24),
            MathTex(r"\text{3. Extract vertex with minimum distance from queue.}", font_size=24),
            MathTex(r"\text{4. For each neighbor, relax edges (update if shorter path found).}", font_size=24),
            MathTex(r"\text{5. Add/update neighbors in priority queue.}", font_size=24),
            MathTex(r"\text{6. Repeat until queue is empty.}", font_size=24),
            MathTex(r"\text{7. Final distances are shortest paths from source.}", font_size=24),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        dijk_algo_text.next_to(dijk_algo_title, DOWN, buff=0.4)
        self.play(Write(dijk_algo_text), run_time=4.5)
        self.wait(1)
        
        self.play(
            FadeOut(dijk_algo_title), FadeOut(dijk_algo_text),
            run_time=1.2
        )
        
        # Example 1: New graph with 4 nodes
        vertices1 = [0, 1, 2, 3]
        edges1 = [(0, 1), (0, 2), (1, 3), (2, 3)]
        edge_weights1 = {
            (0, 1): 6,
            (0, 2): 5,
            (1, 3): 5,
            (2, 3): 5,
        }
        layout1 = {
            0: UP * 1.5 + LEFT * 1.5,
            1: UP * 1.5 + RIGHT * 1.5,
            2: DOWN * 1.5 + LEFT * 1.5,
            3: DOWN * 1.5 + RIGHT * 1.5,
        }
        
        # Run first example
        self.run_dijkstra_example(vertices1, edges1, edge_weights1, layout1, 1)
        
        # Add shelby.jpg image after first example
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
        
        # Example 2: Original graph with 7 nodes
        vertices2 = [0, 1, 2, 3, 4, 5, 6]
        edges2 = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (3, 6), (4, 6)]
        edge_weights2 = {
            (0, 1): 4,
            (0, 2): 2,
            (1, 3): 5,
            (1, 4): 3,
            (2, 5): 6,
            (3, 6): 4,
            (4, 6): 2,
        }
        layout2 = {
            0: UP * 2.2,
            1: LEFT * 2.0 + UP * 0.8,
            2: RIGHT * 2.0 + UP * 0.8,
            3: LEFT * 3.0 + DOWN * 0.8,
            4: LEFT * 0.4 + DOWN * 1.2,
            5: RIGHT * 3.0 + DOWN * 0.8,
            6: DOWN * 2.2,
        }
        
        # Run second example
        self.run_dijkstra_example(vertices2, edges2, edge_weights2, layout2, 2)
        
        # ============================================================
        # Summary
        # ============================================================
        summary_title = Text("Summary", font_size=48)
        self.play(FadeIn(summary_title, shift=UP * 0.5), run_time=1.0)
        self.wait(1)
        self.play(summary_title.animate.to_edge(UP), run_time=0.8)

        summary_points = VGroup(
            MathTex(r"\text{Dijkstra's: Finds shortest paths from source to all nodes}", font_size=26),
            MathTex(r"\text{Works on weighted graphs with non-negative edges}", font_size=26),
            MathTex(r"\text{Uses priority queue (min-heap) for efficiency}", font_size=26),
            MathTex(r"\text{Greedy algorithm: always picks closest unvisited vertex}", font_size=26),
            MathTex(r"\text{Time complexity: } O((V + E) \log V) \text{ with binary heap}", font_size=26),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        summary_points.next_to(summary_title, DOWN, buff=0.6)
        self.play(Write(summary_points), run_time=2.5)
        self.wait(1)

        self.play(
            FadeOut(summary_title), FadeOut(summary_points),
            run_time=1.0
        )
        self.wait(1)
