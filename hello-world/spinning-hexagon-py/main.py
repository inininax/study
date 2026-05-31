#!/usr/bin/env python3
"""
A simulation of a ball bouncing inside a spinning hexagon.

Features:
- The hexagon rotates continuously about its center.
- The ball is affected by gravity and a damping factor (simulating friction/air drag).
- Collisions are detected between the ball (a circle) and each hexagon wall (line segments).
- When a collision occurs, the ball’s velocity is adjusted based on the collision
  with the moving (rotating) wall. The wall’s velocity is computed at the contact point.

Physics notes:
- The collision response uses a relative velocity formulation:
    1. Compute the wall’s velocity at the contact point (due to rotation).
    2. Compute the ball’s velocity relative to the wall.
    3. Reflect the relative velocity about the wall’s inward normal.
    4. Re-add the wall’s velocity to get the new ball velocity.
- A restitution coefficient (< 1) is applied for an inelastic bounce.
- If penetration is detected (ball overlapping the wall), the ball is pushed out along
  the wall’s normal to avoid sticking.

This example uses a simple Euler integration with fixed time steps.
"""

import pygame
import math

# ----------------------------
# Configuration & Simulation Constants
# ----------------------------
WIDTH, HEIGHT = 800, 600  # Window size
FPS = 60  # Frames per second

# Physics parameters
GRAVITY = 800  # Gravity acceleration (pixels/sec^2)
DAMPING = 0.995  # Global damping factor (simulating friction/air resistance)
RESTIUTION = 0.9  # Bounce restitution coefficient

# Ball parameters
BALL_RADIUS = 10  # Ball radius in pixels
INITIAL_BALL_POS = (WIDTH // 2, HEIGHT // 2 - 150)
INITIAL_BALL_VEL = (150, 0)  # Initial velocity (pixels/sec)

# Hexagon parameters
HEX_CENTER = (WIDTH // 2, HEIGHT // 2)
HEX_RADIUS = 250  # Distance from center to vertex
HEX_ANGULAR_SPEED = math.radians(20)  # Rotation speed in rad/sec


# ----------------------------
# Helper Functions
# ----------------------------

def compute_hexagon_vertices(center, radius, rotation):
    """
    Compute the six vertices of a hexagon given the center, radius, and current rotation.
    The vertices are returned in counterclockwise order.
    """
    cx, cy = center
    vertices = []
    for i in range(6):
        # Each vertex is separated by 60 degrees (pi/3 radians)
        theta = rotation + i * (math.pi / 3)
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices


def closest_point_on_segment(A, B, P):
    """
    Compute the closest point Q on segment AB to point P.
    Returns Q and the parameter t (0 <= t <= 1).
    """
    ax, ay = A
    bx, by = B
    px, py = P

    # Vector from A to P and from A to B
    APx, APy = px - ax, py - ay
    ABx, ABy = bx - ax, by - ay
    ab_squared = ABx * ABx + ABy * ABy

    # Avoid division by zero if A and B are the same
    if ab_squared == 0:
        return A, 0

    t = (APx * ABx + APy * ABy) / ab_squared
    t = max(0, min(1, t))  # Clamp t to the segment [0, 1]
    qx = ax + t * ABx
    qy = ay + t * ABy
    return (qx, qy), t


def normalize(vec):
    """
    Return the normalized vector of vec. If vec is zero, return (0, 0).
    """
    x, y = vec
    mag = math.hypot(x, y)
    if mag == 0:
        return (0, 0)
    return (x / mag, y / mag)


def vector_sub(a, b):
    """Subtract vector b from a."""
    return (a[0] - b[0], a[1] - b[1])


def vector_add(a, b):
    """Add vectors a and b."""
    return (a[0] + b[0], a[1] + b[1])


def vector_mul(vec, scalar):
    """Multiply vector by scalar."""
    return (vec[0] * scalar, vec[1] * scalar)


def dot(a, b):
    """Dot product of vectors a and b."""
    return a[0] * b[0] + a[1] * b[1]


def reflect(vel, normal):
    """
    Reflect velocity vector vel about the given normal.
    Assumes normal is normalized.
    """
    v_dot_n = dot(vel, normal)
    return vector_sub(vel, vector_mul(normal, 2 * v_dot_n))


def wall_velocity_at_point(point, center, angular_speed):
    """
    For a wall that is part of a rigid body rotating around 'center',
    compute the velocity at 'point'. The velocity is perpendicular to the
    radius vector (using a 2D cross product with angular speed).
    """
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    # In 2D, the tangential velocity is (-angular_speed * dy, angular_speed * dx)
    return (-angular_speed * dy, angular_speed * dx)


# ----------------------------
# Main Simulation Code
# ----------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bouncing Ball in a Spinning Hexagon")
    clock = pygame.time.Clock()

    # Initialize ball state
    ball_pos = list(INITIAL_BALL_POS)
    ball_vel = list(INITIAL_BALL_VEL)

    # Initialize hexagon rotation
    hex_rotation = 0.0

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Update Simulation State ---
        # Apply gravity (only y-direction)
        ball_vel[1] += GRAVITY * dt

        # Update ball position using Euler integration
        ball_pos[0] += ball_vel[0] * dt
        ball_pos[1] += ball_vel[1] * dt

        # Apply global damping (friction/air drag)
        ball_vel[0] *= DAMPING
        ball_vel[1] *= DAMPING

        # Update hexagon rotation
        hex_rotation += HEX_ANGULAR_SPEED * dt

        # Compute current hexagon vertices
        vertices = compute_hexagon_vertices(HEX_CENTER, HEX_RADIUS, hex_rotation)

        # For each wall (edge of hexagon), check for collision with the ball.
        # The hexagon is convex so the walls are defined by consecutive vertices.
        num_vertices = len(vertices)
        for i in range(num_vertices):
            A = vertices[i]
            B = vertices[(i + 1) % num_vertices]
            # Get the closest point on the wall segment from the ball center
            Q, _ = closest_point_on_segment(A, B, ball_pos)
            # Vector from Q to ball position
            diff = vector_sub(ball_pos, Q)
            dist = math.hypot(diff[0], diff[1])

            if dist < BALL_RADIUS:
                # --- Collision Detected ---
                penetration = BALL_RADIUS - dist

                # Compute wall's inward normal.
                # First, compute the wall's tangent vector:
                tangent = (B[0] - A[0], B[1] - A[1])
                # A candidate normal is perpendicular to tangent.
                candidate = (-tangent[1], tangent[0])
                candidate = normalize(candidate)

                # Determine which direction is inward.
                # We do this by checking the dot product with the vector from the wall midpoint to the hexagon center.
                mid = ((A[0] + B[0]) / 2, (A[1] + B[1]) / 2)
                to_center = vector_sub(HEX_CENTER, mid)
                if dot(candidate, to_center) < 0:
                    normal = vector_mul(candidate, -1)
                else:
                    normal = candidate

                # Compute the wall's velocity at the contact point (Q)
                v_wall = wall_velocity_at_point(Q, HEX_CENTER, HEX_ANGULAR_SPEED)

                # Compute the relative velocity (ball relative to wall)
                rel_vel = vector_sub(tuple(ball_vel), v_wall)

                # Only resolve if the ball is moving into the wall.
                if dot(rel_vel, normal) < 0:
                    # Reflect the relative velocity.
                    # The reflection formula with restitution:
                    # v'_rel = v_rel - (1 + restitution) * (v_rel dot normal) * normal
                    v_rel_dot = dot(rel_vel, normal)
                    rel_vel_reflected = vector_sub(rel_vel, vector_mul(normal, (1 + RESTIUTION) * v_rel_dot))
                    # New ball velocity is the reflected relative velocity plus the wall's velocity.
                    new_ball_vel = vector_add(rel_vel_reflected, v_wall)
                    ball_vel[0], ball_vel[1] = new_ball_vel

                    # Position correction: push the ball out of the wall along the normal.
                    ball_pos[0] += normal[0] * penetration
                    ball_pos[1] += normal[1] * penetration

        # --- Rendering ---
        screen.fill((30, 30, 30))  # Dark background

        # Draw the hexagon
        pygame.draw.polygon(screen, (200, 200, 200), vertices, width=3)

        # Draw the ball
        pygame.draw.circle(screen, (255, 50, 50), (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

        # Optionally, display FPS or debug info
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
