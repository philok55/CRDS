/* Computer Graphics, Assignment, Bezier curves
 * Filename ........ bezier.c
 * Description ..... Bezier curves
 * Date ............ 22.07.2009
 * Created by ...... Paul Melis
 *
 * Student name Thijn Albers, Philo Decroos
 * Student email ...
 * Collegekaart 11874295, 11752262
 * Date 16 nov 2018
 * Comments ........
 *
 *
 * (always fill in these fields before submitting!!)
 */

#include <math.h>
#include "bezier.h"
#include <stdio.h>
#include <stdlib.h>

// Calculates the factorial of n recursively
int fact(int n) { return n >= 1 ? n * fact(n - 1) : 1; }

// Calculates the binomail of (n k) recursively
long binomial(long n, long k) { return (k != 0 && n != k) ? binomial(n-1, k) + binomial(n-1, k-1) : 1; }

// Calculates the SBernsteins polynomial
float bernstein(float u, int n, int i) { return binomial(n, i) * pow(u, i) * pow(1 - u, n - i); }

/* Given a Bezier curve defined by the 'num_points' control points
 * in 'p' computes the position of the point on the curve for parameter
 * value 'u'.
 *
 * Returns the x and y values of the point by setting *x and *y,
 * respectively.
 */
void evaluate_bezier_curve(float *x, float *y, control_point p[], int num_points, float u)
{
    float y_result = 0;
    float x_result = 0;
    for (int i = 0; i < num_points; i++) {
        float bernst = bernstein(u, num_points - 1, i);
        x_result += p[i].x * bernst;
        y_result += p[i].y * bernst;
    }
    *x = x_result;
    *y = y_result;
}

/* Draws a Bezier curve defined by the control points in p[], which
 * will contain 'num_points' points.
 *
 * The 'num_segments' parameter determines the "discretization" of the Bezier
 * curve and is the number of straight line segments that approximate the curve.
 */

void draw_bezier_curve(int num_segments, control_point p[], int num_points)
{
    GLuint buffer[1];

    // Define array length and step size
    int length = (num_segments + 1)*2;
    float step = 1 / (float)num_segments;

    // Create the array and set startvalues
    GLfloat segments[length];
    float u, x, y;
    u = x = y = 0;

    // Evaluates num_segments points on the bezier curve.
    // The array is filled as pairs of x and y with x on index
    // i and y on index i + 1.
    for (int i = 0; i < length; i+=2) {
        evaluate_bezier_curve(&x, &y, p, num_points, u);
        segments[i] = x;
        segments[i+1] = y;
        u += step;
    }

    // This creates the VBO and binds an array to it.
    glGenBuffers(1, buffer);
    glBindBuffer(GL_ARRAY_BUFFER, *buffer);
    glBufferData(GL_ARRAY_BUFFER, sizeof(segments[0])*length /* Fill in the right size here*/,
                 segments /*Fill in the pointer to the array*/, GL_STATIC_DRAW);

    // This tells OpenGL to draw what is in the buffer as a Line Strip.
    glEnableClientState(GL_VERTEX_ARRAY);
    glVertexPointer(2, GL_FLOAT, 0, 0);
    glDrawArrays(GL_LINE_STRIP, 0, num_segments+1 /* Fill in the number of steps to be drawn*/);
    glDisableClientState(GL_VERTEX_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glDeleteBuffers(1, buffer);
}

/* Finds an intersection of a cubic Bezier curve with the line X=x.
   Returns 1 if an intersection was found and places the corresponding y
   value in *y.
   Returns 0 if there is no intersection exists.
*/
int intersect_cubic_bezier_curve(float *y, control_point p[], float x)
{
    float x_curve, y_curve;
    int num_points = 4;
    float u = 0.5;
    float diff = 0.25;
    int max_steps = 1000;

    // Finds the intersection with a binary search. If the x is closer than 10^-3
    // to the evaluation result we say they intersect.
    for (int i = 0; i < max_steps; i++) {
        evaluate_bezier_curve(&x_curve, &y_curve, p, num_points, u);
        if (fabs(x - x_curve) < 0.001) {
            *y = y_curve;
            return 1;
        } else {
            if (x < x_curve)
                u -= diff;
            else
                u += diff;
            diff *= 0.5;
        }
    }
    return 0;
}
