/* Computer Graphics and Game Technology, Assignment Ray-tracing
 *
 * Student name Thijn Albers, Philo Decroos
 * Student email ....
 * Collegekaart 11874295, 11752262
 * Date ............
 * Comments ........
 *
 *
 * (always fill in these fields before submitting!!)
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include "shaders.h"
#include "perlin.h"
#include "v3math.h"
#include "intersection.h"
#include "scene.h"
#include "quat.h"
#include "constants.h"

// shade_constant()
//
// Always return the same color. This shader does no real computations
// based on normal, light position, etc. As such, it merely creates
// a "silhouette" of an object.

vec3 shade_constant(intersection_point ip)
{
    return v3_create(1, 0, 0);
}

// Shader that implements the matte shader
vec3 shade_matte(intersection_point ip)
{
    float matte = 0;

    // for every light source calculate its intensity on the surface
    for (int i = 0; i < scene_num_lights; i++)
    {
        light sl = scene_lights[i];

        // calculate the vector from object to ligthsource
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));

        // add an offstet of 0.01 to the origin point relative to the surface
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;

        // calculate the intensity of this lightsource
        float dot = fmax(v3_dotprod(l, ip.n), 0);
        matte += dot * sl.intensity;
    }
    // capping the intensity to 1
    if (matte > 1)
        matte = 1;

    return v3_create(matte, matte, matte);
}

// Shader that implmeents blinn phong's lightning model
vec3 shade_blinn_phong(intersection_point ip)
{
    // setting standard variables values as given in the assignment
    vec3 c_d = v3_create(1, 0, 0);
    vec3 c_s = v3_create(1, 1, 1);
    float k_d = 0.8;
    float k_s = 0.5;
    float alpha = 50;

    // the final color will have a matte and spec part
    float matte = 0;
    float spec = 0;

    // for every lightsource compute the matte and specular color
    for (int i = 0; i < scene_num_lights; i++)
    {
        light sl = scene_lights[i];

        // calculate the vector from object to ligthsource
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));
        vec3 e = v3_normalize(v3_add(scene_camera_position, v3_negate(ip.p)));
        vec3 h = v3_normalize(v3_add(e, l));

        // add an offstet of 0.001 to the origin point relative to the surface
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;

        // calculate the intensity of this lightsource
        float dot_matte = fmax(v3_dotprod(l, ip.n), 0);
        float dot_spec = v3_dotprod(ip.n, h);
        float s_matte = dot_matte * sl.intensity;
        float s_spec = pow(dot_spec, alpha) * sl.intensity;

        // adding to the total color
        matte += s_matte;
        spec += s_spec;
    }
    // capping intensity to 1
    if (matte > 1)
        matte = 1;
    if (spec > 1)
        spec = 1;

    // full formula for lightning model
    return v3_add(v3_multiply(c_d, (matte * k_d + scene_ambient_light)), v3_multiply(c_s, k_s * spec));
}

// Shader that implements the reflection lightning model
vec3 shade_reflection(intersection_point ip)
{
    // calculating the reflection ray 2n(i * n) - i
    float dot_i_n = v3_dotprod(ip.i, ip.n);
    vec3 two_n = v3_multiply(ip.n, 2);
    vec3 n_two_times_dot = v3_multiply(two_n, dot_i_n);
    vec3 r = v3_add(n_two_times_dot, v3_negate(ip.i));

    // shooting the ray and multiplying it by 0.25
    vec3 reflection_color = v3_multiply(ray_color(ip.ray_level, v3_add(ip.p, v3_multiply(ip.n, 0.001)), r), 0.25);

    float matte = 0;

    // for every light source calculate its intensity on the surface
    for (int i = 0; i < scene_num_lights; i++)
    {
        light sl = scene_lights[i];

        // calculate the vector from object to ligthsource
        vec3 l = v3_normalize(v3_add(sl.position, v3_negate(ip.p)));

        // add an offstet of 0.01 to the origin point relative to the surface
        if (shadow_check(v3_add(ip.p, v3_multiply(ip.n, 0.001)), l))
            continue;

        // calculate the intensity of this lightsource
        float dot = fmax(v3_dotprod(l, ip.n), 0);
        matte += dot * sl.intensity;
    }

    // capping the intensity to 1
    if (matte > 1) matte = 1;

    // matte determines 75% of the final color
    matte *= 0.75;

    return v3_add(v3_create(matte, matte, matte), reflection_color);
}

// Returns the shaded color for the given point to shade.
// Calls the relevant shading function based on the material index.
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

// Determine the surface color for the first object intersected by
// the given ray, or return the scene background color when no
// intersection is found
vec3 ray_color(int level, vec3 ray_origin, vec3 ray_direction)
{
    intersection_point ip;

    // If this ray has been reflected too many times, simply
    // return the background color.
    if (level >= 3)
        return scene_background_color;

    // Check if the ray intersects anything in the scene
    if (find_first_intersection(&ip, ray_origin, ray_direction))
    {
        // Shade the found intersection point
        ip.ray_level = level;
        return shade(ip);
    }

    // Nothing was hit, return background color
    return scene_background_color;
}
