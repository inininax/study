package main

import (
	"image/color"
	"math"

	"github.com/hajimehoshi/ebiten/v2"
	"github.com/hajimehoshi/ebiten/v2/ebitenutil"
)

// --- Simulation constants ---
const (
	screenWidth         = 800
	screenHeight        = 600
	dt                  = 1.0 / 60.0 // fixed time step (in seconds)
	gravity             = 500.0      // pixels/s^2
	ballRadius          = 10.0
	restitution         = 0.9  // energy loss on bounce (1.0 = perfectly elastic)
	collisionFriction   = 0.1  // friction applied at collision (reduces tangential speed)
	airFriction         = 0.99 // simple damping factor per frame
	hexagonRadius       = 200.0
	initialHexagonAngle = 0.0
	hexagonAngularVel   = 1.0 // radian/s (counterclockwise rotation)
)

// --- Basic vector math ---
type Vector struct {
	X, Y float64
}

func (v Vector) Add(o Vector) Vector  { return Vector{v.X + o.X, v.Y + o.Y} }
func (v Vector) Sub(o Vector) Vector  { return Vector{v.X - o.X, v.Y - o.Y} }
func (v Vector) Mul(s float64) Vector { return Vector{v.X * s, v.Y * s} }
func (v Vector) Dot(o Vector) float64 { return v.X*o.X + v.Y*o.Y }
func (v Vector) Length() float64      { return math.Sqrt(v.X*v.X + v.Y*v.Y) }
func (v Vector) Normalize() Vector {
	l := v.Length()
	if l == 0 {
		return Vector{}
	}
	return Vector{v.X / l, v.Y / l}
}
func (v Vector) Perp() Vector { return Vector{-v.Y, v.X} } // 90° counterclockwise

// --- Ball definition ---
type Ball struct {
	Pos    Vector // position in pixels
	Vel    Vector // velocity in pixels/second
	Radius float64
}

// --- Hexagon definition ---
// The hexagon is defined by its center, the distance from its center to each vertex,
// its current rotation angle, and its constant angular velocity.
type Hexagon struct {
	Center          Vector
	Radius          float64 // distance from center to vertex
	Angle           float64 // current rotation angle (radians)
	AngularVelocity float64 // in radians/second
}

// Vertices returns the six vertices of the hexagon based on its current angle.
func (h *Hexagon) Vertices() []Vector {
	vertices := make([]Vector, 6)
	for i := 0; i < 6; i++ {
		angle := h.Angle + float64(i)*math.Pi/3.0 // 60° intervals
		vertices[i] = Vector{
			X: h.Center.X + h.Radius*math.Cos(angle),
			Y: h.Center.Y + h.Radius*math.Sin(angle),
		}
	}
	return vertices
}

// --- Game definition ---
type Game struct {
	ball Ball
	hex  Hexagon
}

// Update is called every frame (60 times per second).
func (g *Game) Update() error {
	// --- Update ball physics ---
	// 1. Apply gravity (accelerate downward).
	g.ball.Vel.Y += gravity * dt

	// 2. Update ball position.
	g.ball.Pos = g.ball.Pos.Add(g.ball.Vel.Mul(dt))

	// 3. Apply air friction (damping).
	g.ball.Vel = g.ball.Vel.Mul(airFriction)

	// --- Update hexagon rotation ---
	g.hex.Angle += g.hex.AngularVelocity * dt

	// --- Collision detection and response ---
	vertices := g.hex.Vertices()
	// Process each of the 6 edges of the hexagon.
	for i := 0; i < 6; i++ {
		a := vertices[i]
		b := vertices[(i+1)%6]
		// Compute the closest point on the edge [a,b] to the ball's center.
		closest := closestPointOnSegment(a, b, g.ball.Pos)
		// Vector from the closest point on the edge to the ball center.
		diff := g.ball.Pos.Sub(closest)
		dist := diff.Length()
		if dist < g.ball.Radius {
			// --- Collision detected ---

			// Penetration depth (how far the ball is inside the wall).
			penetration := g.ball.Radius - dist
			// Normal pointing from wall toward ball center.
			n := diff.Normalize()

			// --- Determine wall velocity at collision point ---
			// The wall (hexagon) rotates about its center.
			// For a point "closest" on the wall, its velocity is:
			//   v_wall = ω × (closest - hex.center)
			// In 2D, this is: v_wall = ω * (-r.Y, r.X)
			r := closest.Sub(g.hex.Center)
			wallVel := Vector{
				X: -g.hex.AngularVelocity * r.Y,
				Y: g.hex.AngularVelocity * r.X,
			}

			// --- Collision response ---
			// Compute the relative velocity between ball and wall.
			relVel := g.ball.Vel.Sub(wallVel)
			// Component along the collision normal.
			vn := relVel.Dot(n)
			if vn < 0 {
				// Reflect the relative velocity using the restitution coefficient.
				// v' = v - (1+e)*(v · n)*n
				relVel = relVel.Sub(n.Mul((1 + restitution) * vn))

				// Apply friction on the tangential (parallel) component.
				// First extract the tangential component.
				tangent := relVel.Sub(n.Mul(relVel.Dot(n)))
				tangent = tangent.Mul(1 - collisionFriction)

				// Reconstruct the new relative velocity.
				relVel = n.Mul(relVel.Dot(n)).Add(tangent)

				// The new ball velocity is the wall velocity plus the corrected relative velocity.
				g.ball.Vel = wallVel.Add(relVel)
			}

			// Resolve penetration by pushing the ball out along the collision normal.
			g.ball.Pos = g.ball.Pos.Add(n.Mul(penetration))
		}
	}

	// --- (Optional) Fallback boundary: prevent the ball from falling off-screen ---
	if g.ball.Pos.Y > screenHeight-g.ball.Radius {
		g.ball.Pos.Y = screenHeight - g.ball.Radius
		g.ball.Vel.Y = -g.ball.Vel.Y * restitution
	}

	return nil
}

// Draw is called every frame to render the scene.
func (g *Game) Draw(screen *ebiten.Image) {
	// Clear the screen.
	screen.Fill(color.RGBA{30, 30, 30, 255})

	// Draw the hexagon.
	vertices := g.hex.Vertices()
	for i := 0; i < 6; i++ {
		a := vertices[i]
		b := vertices[(i+1)%6]
		ebitenutil.DrawLine(screen, a.X, a.Y, b.X, b.Y, color.RGBA{200, 200, 200, 255})
	}

	// Draw the ball.
	// (For simplicity, we use a custom function to draw a filled circle.)
	drawCircle(screen, int(g.ball.Pos.X), int(g.ball.Pos.Y), int(g.ball.Radius), color.RGBA{220, 50, 50, 255})
}

// Layout specifies the game’s internal resolution.
func (g *Game) Layout(outsideWidth, outsideHeight int) (int, int) {
	return screenWidth, screenHeight
}

// --- Utility functions ---

// closestPointOnSegment returns the closest point on the line segment AB to point P.
func closestPointOnSegment(a, b, p Vector) Vector {
	ab := b.Sub(a)
	t := p.Sub(a).Dot(ab) / ab.Dot(ab)
	// Clamp t to the [0,1] interval to stay within the segment.
	if t < 0 {
		t = 0
	} else if t > 1 {
		t = 1
	}
	return a.Add(ab.Mul(t))
}

// drawCircle draws a filled circle on the given image using a simple algorithm.
func drawCircle(img *ebiten.Image, cx, cy, r int, clr color.Color) {
	// A simple approach: for each y offset in [-r, r], compute the horizontal span.
	for y := -r; y <= r; y++ {
		// xSpan is based on circle equation: x^2 + y^2 <= r^2.
		xSpan := int(math.Sqrt(float64(r*r - y*y)))
		for x := -xSpan; x <= xSpan; x++ {
			img.Set(cx+x, cy+y, clr)
		}
	}
}

// --- Main function ---
func main() {
	ebiten.SetWindowSize(screenWidth, screenHeight)
	ebiten.SetWindowTitle("Bouncing Ball in a Spinning Hexagon")

	game := &Game{
		ball: Ball{
			// Start at the center with an initial velocity.
			Pos:    Vector{X: screenWidth / 2, Y: screenHeight / 2},
			Vel:    Vector{X: 200, Y: -150},
			Radius: ballRadius,
		},
		hex: Hexagon{
			Center:          Vector{X: screenWidth / 2, Y: screenHeight / 2},
			Radius:          hexagonRadius,
			Angle:           initialHexagonAngle,
			AngularVelocity: hexagonAngularVel,
		},
	}

	// Run the Ebiten game loop.
	if err := ebiten.RunGame(game); err != nil {
		panic(err)
	}
}
