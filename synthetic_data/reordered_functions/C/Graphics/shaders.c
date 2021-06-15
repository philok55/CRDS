// REORDERINGS EXECUTED: 1

vec3 shade_reflection(intersection_point ip)
{
    float dot_i_n = v3_dotprod(ip.i, ip.n);
    vec3 two_n = v3_multiply(ip.n, 2);
    vec3 n_two_times_dot = v3_multiply(two_n, dot_i_n);
    vec3 r = v3_add(n_two_times_dot, v3_negate(ip.i));
    vec3 reflection_color = v3_multiply(ray_color(ip.ray_level, v3_add(ip.p, v3_multiply(ip.n, 0.001)), r), 0.25);
    float matte = 0;
    for (int i = 0; i < scene_num_lights; i++)
    {
        light sl = scene_lights[i];
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        float dot = fmax(v3_dotprod(l, ip.n), 0);
        matte += dot * sl.intensity;
    }
    if (matte > 1)
        matte = 1;
    matte *= 0.75;
    return v3_add(v3_create(matte, matte, matte), reflection_color);
}
vec3 shade(intersection_point ip)
{
    switch (ip.material)
    {
    case 0:
        return shade_constant(ip);
    case 1:
        return shade_matte(ip);
    case 2:
        return shade_blinn_phong(ip);
    case 3:
        return shade_reflection(ip);
    default:
        return shade_constant(ip);
    }
}
vec3 shade_blinn_phong(intersection_point ip)
{
    vec3 c_d = v3_create(1, 0, 0);
    vec3 c_s = v3_create(1, 1, 1);
    float k_d = 0.8;
    float k_s = 0.5;
    float alpha = 50;
    float matte = 0;
    float spec = 0;
    for (int i = 0; i < scene_num_lights; i++)
    {
        light sl = scene_lights[i];
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        vec3 e = v3_normalize(v3_add(scene_camera_position, v3_negate(ip.p)));
        vec3 h = v3_normalize(v3_add(e, l));
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        float dot_matte = fmax(v3_dotprod(l, ip.n), 0);
        float dot_spec = v3_dotprod(ip.n, h);
        float s_matte = dot_matte * sl.intensity;
        float s_spec = pow(dot_spec, alpha) * sl.intensity;
        matte += s_matte;
        spec += s_spec;
    }
    if (matte > 1)
        matte = 1;
    if (spec > 1)
        spec = 1;
    return v3_add(v3_multiply(c_d, (matte * k_d + scene_ambient_light)), v3_multiply(c_s, k_s * spec));
}
vec3 shade_constant(intersection_point ip) { return v3_create(1, 0, 0); }
vec3 ray_color(int level, vec3 ray_origin, vec3 ray_direction)
{
    intersection_point ip;
    if (level >= 3)
        return scene_background_color;
    if (find_first_intersection(&ip, ray_origin, ray_direction))
    {
        ip.ray_level = level;
        return shade(ip);
    }
    return scene_background_color;
}
vec3 shade_matte(intersection_point ip)
{
    float matte = 0;
    for (int i = 0; i < scene_num_lights; i++)
    {
        light sl = scene_lights[i];
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        float dot = fmax(v3_dotprod(l, ip.n), 0);
        matte += dot * sl.intensity;
    }
    if (matte > 1)
        matte = 1;
    return v3_create(matte, matte, matte);
}
