// REORDERINGS EXECUTED: 1

int fact(int n) { return n >= 1 ? n *fact(n - 1) : 1; }
long binomial(long n, long k) { return (k != 0 && n != k) ? binomial(n - 1, k) + binomial(n - 1, k - 1) : 1; }
float bernstein(float u, int n, int i) { return binomial(n, i) * pow(u, i) * pow(1 - u, n - i); }
void evaluate_bezier_curve(float *x, float *y, control_point p[], int num_points, float u)
{
    float y_result = 0;
    float x_result = 0;
    for (int i = 0; i < num_points; i++)
    {
        float bernst = bernstein(u, num_points - 1, i);
        x_result += p[i].x * bernst;
        y_result += p[i].y * bernst;
    }
    *x = x_result;
    *y = y_result;
}
void draw_bezier_curve(int num_segments, control_point p[], int num_points)
{
    GLuint buffer[1];
    int length = (num_segments + 1) * 2;
    float step = 1 / (float)num_segments;
    GLfloat segments[length];
    float u, x, y;
    u = x = y = 0;
    for (int i = 0; i < length; i += 2)
    {
        evaluate_bezier_curve(&x, &y, p, num_points, u);
        segments[i] = x;
        segments[i + 1] = y;
        u += step;
    }
    glGenBuffers(1, buffer);
    glBindBuffer(GL_ARRAY_BUFFER, *buffer);
    glBufferData(GL_ARRAY_BUFFER, sizeof(segments[0]) * length, segments, GL_STATIC_DRAW);
    glEnableClientState(GL_VERTEX_ARRAY);
    glVertexPointer(2, GL_FLOAT, 0, 0);
    glDrawArrays(GL_LINE_STRIP, 0, num_segments + 1);
    glDisableClientState(GL_VERTEX_ARRAY);
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glDeleteBuffers(1, buffer);
}
int intersect_cubic_bezier_curve(float *y, control_point p[], float x)
{
    float x_curve, y_curve;
    int num_points = 4;
    float u = 0.5;
    float diff = 0.25;
    int max_steps = 1000;
    for (int i = 0; i < max_steps; i++)
    {
        evaluate_bezier_curve(&x_curve, &y_curve, p, num_points, u);
        if (fabs(x - x_curve) < 0.001)
        {
            *y = y_curve;
            return 1;
        }
        else
        {
            if (x < x_curve)
                u -= diff;
            else u += diff;
            diff *= 0.5;
        }
    }
    return 0;
}
