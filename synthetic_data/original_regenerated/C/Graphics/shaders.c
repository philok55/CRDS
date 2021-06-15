vec3shade_constant(intersection_pointip) { returnv3_create(1, 0, 0); }
vec3shade_matte(intersection_pointip)
{
    floatmatte = 0;
    for (inti = 0; i < scene_num_lights; i++)
    {
        lightsl = scene_lights[i];
        vec3l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        floatdot = fmax(v3_dotprod(l, ip.n), 0);
        matte += dot * sl.intensity;
    }
    if (matte > 1)
        matte = 1;
    returnv3_create(matte, matte, matte);
}
vec3shade_blinn_phong(intersection_pointip)
{
    vec3c_d = v3_create(1, 0, 0);
    vec3c_s = v3_create(1, 1, 1);
    floatk_d = 0.8;
    floatk_s = 0.5;
    floatalpha = 50;
    floatmatte = 0;
    floatspec = 0;
    for (inti = 0; i < scene_num_lights; i++)
    {
        lightsl = scene_lights[i];
        vec3l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        vec3e = v3_normalize(v3_add(scene_camera_position, v3_negate(ip.p)));
        vec3h = v3_normalize(v3_add(e, l));
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        floatdot_matte = fmax(v3_dotprod(l, ip.n), 0);
        floatdot_spec = v3_dotprod(ip.n, h);
        floats_matte = dot_matte * sl.intensity;
        floats_spec = pow(dot_spec, alpha) * sl.intensity;
        matte += s_matte;
        spec += s_spec;
    }
    if (matte > 1)
        matte = 1;
    if (spec > 1)
        spec = 1;
    returnv3_add(v3_multiply(c_d, (matte * k_d + scene_ambient_light)), v3_multiply(c_s, k_s * spec));
}
vec3shade_reflection(intersection_pointip)
{
    floatdot_i_n = v3_dotprod(ip.i, ip.n);
    vec3two_n = v3_multiply(ip.n, 2);
    vec3n_two_times_dot = v3_multiply(two_n, dot_i_n);
    vec3r = v3_add(n_two_times_dot, v3_negate(ip.i));
    vec3reflection_color = v3_multiply(ray_color(ip.ray_level, v3_add(ip.p, v3_multiply(ip.n, 0.001)), r), 0.25);
    floatmatte = 0;
    for (inti = 0; i < scene_num_lights; i++)
    {
        lightsl = scene_lights[i];
        vec3l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        floatdot = fmax(v3_dotprod(l, ip.n), 0);
        matte += dot * sl.intensity;
    }
    if (matte > 1)
        matte = 1;
    matte *= 0.75;
    returnv3_add(v3_create(matte, matte, matte), reflection_color);
}
vec3shade(intersection_pointip)
{
    switch (ip.material)
    {
    case0:
        returnshade_constant(ip);
    case1:
        returnshade_matte(ip);
    case2:
        returnshade_blinn_phong(ip);
    case3:
        returnshade_reflection(ip);
    default:
        returnshade_constant(ip);
    }
}
vec3ray_color(intlevel, vec3ray_origin, vec3ray_direction)
{
    intersection_pointip;
    if (level >= 3)
        returnscene_background_color;
    if (find_first_intersection(&ip, ray_origin, ray_direction))
    {
        ip.ray_level = level;
        returnshade(ip);
    }
    returnscene_background_color;
}
<EOF>