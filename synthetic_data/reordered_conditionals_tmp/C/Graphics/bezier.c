// REORDERINGS EXECUTED: 2

intfact(intn) { returnn >= 1 ? n *fact(n - 1) : 1; }
longbinomial(longn, longk) { return (k != 0 && n != k) ? binomial(n - 1, k) + binomial(n - 1, k - 1) : 1; }
floatbernstein(floatu, intn, inti) { returnbinomial(n, i) * pow(u, i) * pow(1 - u, n - i); }
voidevaluate_bezier_curve(float *x, float *y, control_pointp[], intnum_points, floatu)
{
    floaty_result = 0;
    floatx_result = 0;
    for (inti = 0; i < num_points; i++)
    {
        floatbernst = bernstein(u, num_points - 1, i);
        x_result += p[i].x * bernst;
        y_result += p[i].y * bernst;
    }
    *x = x_result;
    *y = y_result;
}
voiddraw_bezier_curve(intnum_segments, control_pointp[], intnum_points)
{
    GLuintbuffer[1];
    intlength = (num_segments + 1) * 2;
    floatstep = 1 / (float)num_segments;
    GLfloatsegments[length];
    floatu, x, y;
    u = x = y = 0;
    for (inti = 0; i < length; i += 2)
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
intintersect_cubic_bezier_curve(float *y, control_pointp[], floatx)
{
    floatx_curve, y_curve;
    intnum_points = 4;
    floatu = 0.5;
    floatdiff = 0.25;
    intmax_steps = 1000;
    for (inti = 0; i < max_steps; i++)
    {
        evaluate_bezier_curve(&x_curve, &y_curve, p, num_points, u);
        if (fabs(x - x_curve) < 0.001)
        {
            if (x < x_curve)
                u += diff;
            elseu -= diff;
            diff *= 0.5;
        }
        else
        {
            *y = y_curve;
            return1;
        }
    }
    return0;
}
<EOF>