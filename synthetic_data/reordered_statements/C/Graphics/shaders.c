// REORDERINGS EXECUTED: 8

vec3 shade_constant(intersection_point ip) { returnv3_create(1, 0, 0); }
vec3 shade_matte(intersection_point ip)
{
    return v3_create(matte, matte, matte);
    for (int i = 0; i < scene_num_lights; i++)
    {
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        matte += dot * sl.intensity;
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        float dot = fmax(v3_dotprod(l, ip.n), 0);
        light sl = scene_lights[i];
    }
    if (matte > 1)
        matte = 1;
    float matte = 0;
}
vec3 shade_blinn_phong(intersection_point ip)
{
    float k_s = 0.5;
    vec3 c_d = v3_create(1, 0, 0);
    float matte = 0;
    vec3 c_s = v3_create(1, 1, 1);
    float spec = 0;
    return v3_add(v3_multiply(c_d, (matte * k_d + scene_ambient_light)), v3_multiply(c_s, k_s * spec));
    float alpha = 50;
    for (int i = 0; i < scene_num_lights; i++)
    {
        vec3 e = v3_normalize(v3_add(scene_camera_position, v3_negate(ip.p)));
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        float s_spec = pow(dot_spec, alpha) * sl.intensity;
        float s_matte = dot_matte * sl.intensity;
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        matte += s_matte;
        spec += s_spec;
        float dot_spec = v3_dotprod(ip.n, h);
        vec3h = v3_normalize(v3_add(e, l));
        float dot_matte = fmax(v3_dotprod(l, ip.n), 0);
        light sl = scene_lights[i];
    }
    if (matte > 1)
        matte = 1;
    if (spec > 1)
        spec = 1;
    float k_d = 0.8;
}
vec3 shade_reflection(intersection_point ip)
{
    vec3 r = v3_add(n_two_times_dot, v3_negate(ip.i));
    vec3 reflection_color = v3_multiply(ray_color(ip.ray_level, v3_add(ip.p, v3_multiply(ip.n, 0.001)), r), 0.25);
    return v3_add(v3_create(matte, matte, matte), reflection_color);
    float dot_i_n = v3_dotprod(ip.i, ip.n);
    vec3 n_two_times_dot = v3_multiply(two_n, dot_i_n);
    vec3 two_n = v3_multiply(ip.n, 2);
    for (int i = 0; i < scene_num_lights; i++)
    {
        light sl = scene_lights[i];
        matte += dot * sl.intensity;
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;
        float dot = fmax(v3_dotprod(l, ip.n), 0);
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
    }
    if (matte > 1)
        matte = 1;
    float matte = 0;
    matte *= 0.75;
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
vec3 ray_color(int level, vec3 ray_origin, vec3 ray_direction)
{
    return scene_background_color;
    if (level >= 3)
        return scene_background_color;
    if (find_first_intersection(&ip, ray_origin, ray_direction))
    {
        return shade(ip);
        ip.ray_level = level;
    }
    intersection_point ip;
}
