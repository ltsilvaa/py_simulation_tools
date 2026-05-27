import os
import math
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from elasticipy.tensors.elasticity import StiffnessTensor

"""
    Global variables: Change the color of the surfaces and 2D plots;
                      Control the line width of the 2D projetions and 2D plots;
                      Control the 3D plot definitions

"""

color_maximum = "#3c8e46"
color_minimum = "#0011FF"
color_negative = "#FF0000"

color_2d_young = 'black'
color_2d_poisson = 'black'
color_2d_shear = 'black'

width_2d_projection = 4
width_2d_plot = 4

#General parameters for the 2D plots
mpl.rcParams.update({
        "font.size": 15,
        "axes.titlesize": 13,
        "axes.labelsize": 15,
        "xtick.labelsize": 13,
        "ytick.labelsize": 13,
        "font.weight": "semibold",
        "axes.labelweight": "semibold",
        "axes.titleweight": "semibold",
        "xtick.major.width": 1.5,
        "ytick.major.width": 1.5,
        "xtick.minor.width": 1.2,
        "ytick.minor.width": 1.2,
        "xtick.major.size": 6,
        "ytick.major.size": 6
    })

color_2d_E = "black"
color_2d_nu_positive = "black"
color_2d_nu_negative = "red"
color_2d_G = "black"

def plot_axis_config(maximum, label_x, label_y, label_z):
    return dict(
        scene_camera=dict(
            eye=dict(x=1.28, y=1.28, z=1.28), center=dict(x=0, y=0, z=-0.15)
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        scene=dict(
            aspectmode="cube",
            xaxis=dict(
                showbackground=True,
                backgroundcolor="#FFFFFF",
                gridcolor="#D9D9D9",
                gridwidth=4,
                zeroline=False,
                tickfont=dict(size=14, weight=700, color="#535353"),
                showline=True,
                linecolor="#A7A6A6",
                linewidth=4,
                mirror=True,
                showspikes=False,
                autorange=False,
                range=[-maximum, maximum],
                title=dict(text=label_x, font=dict(size=14, weight=700)),
            ),
            yaxis=dict(
                showbackground=True,
                backgroundcolor="#FFFFFF",
                gridcolor="#D9D9D9",
                gridwidth=4,
                zeroline=False,
                tickfont=dict(size=14, weight=700, color="#535353"),
                showline=True,
                linecolor="#A7A6A6",
                linewidth=4,
                mirror=True,
                showspikes=False,
                autorange=False,
                range=[-maximum, maximum],
                title=dict(text=label_y, font=dict(size=14, weight=700)),
            ),
            zaxis=dict(
                showbackground=True,
                backgroundcolor="#FFFFFF",
                gridcolor="#D9D9D9",
                gridwidth=4,
                zeroline=False,
                tickfont=dict(size=14, weight=700, color="#535353"),
                showline=True,
                linecolor="#A7A6A6",
                linewidth=4,
                mirror=True,
                showspikes=False,
                autorange=False,
                range=[-maximum, maximum],
                title=dict(text=label_z, font=dict(size=14, weight=700)),
            ),
        )
    )

def plot_traces_config():
    return dict(
        contours_x=dict(
            show=True,
            usecolormap=False,
            project_z=False, 
            color="#646464",  
            highlightcolor="red",
            project=dict(x=False)
        ),
         contours_y=dict(
            show=True,
            usecolormap=False,
            project_z=False, 
            color="#646464",   
            highlightcolor="red",
            project=dict(y=False)
        ),
         contours_z=dict(
            show=True,
            usecolormap=False,
            project_z=False,
            color="#646464",  
            highlightcolor="red",
            project=dict(z=False)
        ),
        showscale=False,#
        selector=dict(type='surface')
    )

def find_2D_projections(figure_data, maximum_value, data_type):
    """
    
    """
    def interp2d_points(matrix, rows, cols):
        r0 = np.floor(rows).astype(int)
        r1 = np.minimum(r0 + 1, matrix.shape[0] - 1)
        c0 = np.floor(cols).astype(int)
        c1 = np.minimum(c0 + 1, matrix.shape[1] - 1)
        dr, dc = rows - r0, cols - c0
        return (
            matrix[r0, c0] * (1 - dr) * (1 - dc)
            + matrix[r1, c0] * dr * (1 - dc)
            + matrix[r0, c1] * (1 - dr) * dc
            + matrix[r1, c1] * dr * dc
        )

    contour_vals = [1e-5] # Deslocamento microscópico para evitar buracos na malha zero exata
    projection_value = -maximum_value
    epsilon = (2 * maximum_value) * 0.005    

    planes_data = {
        'YZ': {'negative': {'x':[], 'y':[], 'z':[]}, 'minimum': {'x':[], 'y':[], 'z':[]}, 'maximum': {'x':[], 'y':[], 'z':[]}},
        'ZX': {'negative': {'x':[], 'y':[], 'z':[]}, 'minimum': {'x':[], 'y':[], 'z':[]}, 'maximum': {'x':[], 'y':[], 'z':[]}},
        'XY': {'negative': {'x':[], 'y':[], 'z':[]}, 'minimum': {'x':[], 'y':[], 'z':[]}, 'maximum': {'x':[], 'y':[], 'z':[]}}
    }

    fig_mock, ax_mock = plt.subplots()

    for trace in list(figure_data):
        print(trace)
        if trace.type == "surface":
            X_data = np.array(trace.x)
            Y_data = np.array(trace.y)
            Z_data = np.array(trace.z)
            has_surfacecolor = hasattr(trace, 'surfacecolor') and trace.surfacecolor is not None
            color_data = np.array(trace.surfacecolor) if has_surfacecolor else Z_data
            is_maximum_surface = False
            if hasattr(trace, 'colorscale') and trace.colorscale is not None:
                scale_str = str(trace.colorscale).lower()
                if 'maximum' in scale_str or color_maximum in scale_str:
                    is_maximum_surface = True
            if not is_maximum_surface and np.nanmin(color_data) >= 0 and np.nanmax(color_data) > 0.4:
                is_maximum_surface = True

            configs = [
                ('YZ', X_data, Y_data, Z_data, 'x'), 
                ('ZX', Y_data, X_data, Z_data, 'y'), 
                ('XY', Z_data, X_data, Y_data, 'z')  
            ]

            for plane_name, slice_data, interp1, interp2, proj_axis in configs:
                
                min_val_slice = np.nanmin(slice_data)
                max_val_slice = np.nanmax(slice_data)
                
                if min_val_slice > 1e-4 or max_val_slice < -1e-4:
                    continue
                    
                try:
                    cs = ax_mock.contour(slice_data, levels=contour_vals)
                except ValueError:
                    continue
                
                for path in cs.get_paths():
                    v = path.vertices
                    c = path.codes 

                    segments = []
                    if c is None:
                        segments.append(v)
                    else:
                        cur_seg = []
                        for idx in range(len(v)):
                            code = c[idx]
                            if code == 1: # MOVETO (Começa nova pétala)
                                if cur_seg:
                                    segments.append(np.array(cur_seg))
                                cur_seg = [v[idx]]
                            elif code == 79: # CLOSEPOLY (Fecha a pétala sem usar o (0,0) falso do matplotlib)
                                if cur_seg:
                                    cur_seg.append(cur_seg[0]) # Liga o último ponto ao primeiro perfeitamente
                                    segments.append(np.array(cur_seg))
                                cur_seg = []
                            else: # LINETO (Continua desenhando)
                                cur_seg.append(v[idx])
                        if cur_seg:
                            segments.append(np.array(cur_seg))

                    for seg in segments:
                        if len(seg) < 2:
                            continue
                            
                        cols, rows = seg[:, 0], seg[:, 1]

                        # Mantém a interpolação perfeita que gera as curvas suaves
                        p1_points = interp2d_points(interp1, rows, cols)
                        p2_points = interp2d_points(interp2, rows, cols)
                        line_color_values = interp2d_points(color_data, rows, cols)

                        def add_segment(color_category, arr1, arr2, offset_layer):
                            n_pts = len(arr1)
                            if proj_axis == 'x':
                                xs = [offset_layer] * n_pts
                                ys = list(arr1)
                                zs = list(arr2)
                            elif proj_axis == 'y':
                                ys = [offset_layer] * n_pts
                                xs = list(arr1)
                                zs = list(arr2)
                            else: 
                                zs = [offset_layer] * n_pts
                                xs = list(arr1)
                                ys = list(arr2)
                                
                            planes_data[plane_name][color_category]['x'].extend(xs + [None])
                            planes_data[plane_name][color_category]['y'].extend(ys + [None])
                            planes_data[plane_name][color_category]['z'].extend(zs + [None])

                        if is_maximum_surface:
                            add_segment('maximum', p1_points, p2_points, projection_value + 3 * epsilon)
                        elif data_type == "linear":
                            for i in range(len(p1_points) - 1):
                                v1, v2 = line_color_values[i], line_color_values[i+1]

                                if np.isnan(v1) or np.isnan(v2):
                                    continue

                                p1_a, p1_b = p1_points[i], p1_points[i+1]
                                p2_a, p2_b = p2_points[i], p2_points[i+1]

                                offset_minimum = projection_value + epsilon
                                offset_maximum = projection_value + 2 * epsilon # Trocamos offset_blue por offset_green

                                if v1 < 0 and v2 < 0:
                                    # Tudo negativo -> Vermelho
                                    add_segment('minimum', [p1_a, p1_b], [p2_a, p2_b], offset_minimum)
                                elif v1 >= 0 and v2 >= 0:
                                    # Tudo positivo -> Verde (Substituímos 'blue' por 'green')
                                    add_segment('maximum', [p1_a, p1_b], [p2_a, p2_b], offset_maximum)
                                else:
                                    # CRUZOU O ZERO: Interpolação para cortar a cor no meio exato
                                    t = (0.0 - v1) / (v2 - v1) if (v2 - v1) != 0 else 0.5
                                    p1_zero = p1_a + t * (p1_b - p1_a)
                                    p2_zero = p2_a + t * (p2_b - p2_a)

                                    if v1 < 0:
                                        add_segment('red', [p1_a, p1_zero], [p2_a, p2_zero], offset_negative)
                                        add_segment('green', [p1_zero, p1_b], [p2_zero, p2_b], offset_maximum) # Verde aqui
                                    else:
                                        add_segment('green', [p1_a, p1_zero], [p2_a, p2_zero], offset_maximum) # Verde aqui
                                        add_segment('red', [p1_zero, p1_b], [p2_zero, p2_b], offset_negative)
                        else:
                            for i in range(len(p1_points) - 1):
                                v1, v2 = line_color_values[i], line_color_values[i+1]
                                
                                if np.isnan(v1) or np.isnan(v2):
                                    continue
                                    
                                p1_a, p1_b = p1_points[i], p1_points[i+1]
                                p2_a, p2_b = p2_points[i], p2_points[i+1]
                                
                                offset_negative = projection_value + epsilon
                                offset_minimum = projection_value + 2 * epsilon
                                
                                if v1 < 0 and v2 < 0:
                                    add_segment('negative', [p1_a, p1_b], [p2_a, p2_b], offset_negative)
                                elif v1 >= 0 and v2 >= 0:
                                    add_segment('minimum', [p1_a, p1_b], [p2_a, p2_b], offset_minimum)
                                else:
                                    t = (0.0 - v1) / (v2 - v1) if (v2 - v1) != 0 else 0.5
                                    p1_zero = p1_a + t * (p1_b - p1_a)
                                    p2_zero = p2_a + t * (p2_b - p2_a)
                                    
                                    if v1 < 0:
                                        add_segment('negative', [p1_a, p1_zero], [p2_a, p2_zero], offset_negative)
                                        add_segment('minimum', [p1_zero, p1_b], [p2_zero, p2_b], offset_minimum)
                                    else:
                                        add_segment('minimum', [p1_a, p1_zero], [p2_a, p2_zero], offset_minimum)
                                        add_segment('negative', [p1_zero, p1_b], [p2_zero, p2_b], offset_negative)

    plt.close(fig_mock)

    return planes_data

def maximum_find(max):
    """
    
    """
    if max > 0.01 and max < 0.1:
        return math.ceil(max*100)/100
    elif max > 0.1 and max < 1.0:
        return math.ceil(max*10)/10
    elif max > 1.0 and max < 10.0:
        return math.ceil(max)
    elif max > 10.0 and max < 100.0:
        return math.ceil(max/10)*10
    elif max > 100.0 and max < 1000.0:
        return math.ceil(max/100)*100
    elif max > 1.000 and max < 10.000:
        return math.ceil(max/1000)*1000

def plot_2D_config (angles, values, color, step, label, path_, file_name):
        figure = plt.figure(figsize=(7.5, 7))
        ax_scale = figure.add_axes([0.11, 0.15, 0.03, 0.7])
        ax_polar = figure.add_axes([0.22, 0.15, 0.72, 0.7], projection="polar")

        for spine in ax_polar.spines.values():
            spine.set_linewidth(1.8)
        ax_scale.spines["left"].set_linewidth(1.8)
        ax_polar.grid(True, linewidth=1.4)

        maximum = np.max(values)
        if maximum < 1.0:
            margin = 0.02
        elif maximum > 1.0 and maximum < 30:
            margin = 10.0  
        else:
            margin = 20.0
        rmax = math.ceil(maximum / step) * step
        if rmax - maximum < margin:
            rmax += step

        if "poisson" in file_name: #For negative Poisson's ratio values
            positive = np.copy(values)
            negative = np.copy(values)
            positive[positive < 0] = np.nan
            negative[negative > 0] = np.nan
            ax_polar.plot(angles, positive, lw=width_2d_plot, color=color_2d_nu_positive)
            ax_polar.plot(angles, np.abs(negative), lw=width_2d_plot, color=color_2d_nu_negative)

        ax_polar.plot(angles, values, lw=width_2d_plot, color=color)
        ax_polar.set_theta_zero_location("E")
        ax_polar.set_theta_direction(1)
        ax_polar.set_thetagrids(np.arange(0, 360, 30))
        ax_polar.set_rlim(0, rmax)
        ax_polar.set_rticks(np.arange(0, rmax + 0.0001, step))
        ax_polar.set_yticklabels([])

        ax_scale.set_ylim(-1 * rmax, rmax)
        ax_scale.set_yticks(np.arange(-1 * rmax, rmax + 0.0001, step))
        ax_scale.set_ylabel(label)
        ax_scale.set_xticks([])
        for spine in ["top", "right", "bottom"]:
            ax_scale.spines[spine].set_visible(False)

        path_output_image = os.path.join(path_, f"{file_name}.png")        
        figure.savefig(path_output_image, dpi=600, bbox_inches="tight")
        plt.close(figure)

def young_plot_3D(elastic_matrix, path_output):
    """
        Plot the 3D surfaces for the Young's modulus using Elasticpy and Plotly.

        Args: 
            elastic_matrix (list): Computed matrix with the elastic constants Cij.
            path_: Path to the directory to save the image.
        Returns:
            None.
    """
    stiffness_matrix = StiffnessTensor(elastic_matrix)
    young = stiffness_matrix.Young_modulus
    plot_young = young.plot3D(n_phi=360, n_theta=360, backend='plotly', fig=None, which="minmax", opacity=0.9)
    maximum = maximum_find(young.max())

    plot_young.data[0].update(
        cmin=-maximum,
        cmax=maximum,
        colorscale=[[0, color_maximum], [1, color_maximum]],
        opacity=.6,
        lighting=dict(
            ambient=0.8, 
            diffuse=0.99, 
            specular=0.3, 
            roughness=0.9, 
            fresnel=0.9
        ),
    )

    plot_young.update_layout(plot_axis_config(maximum, "E<sub>x</sub>", "E<sub>y</sub>", "E<sub>z</sub>"))
    plot_young.update_traces(plot_traces_config())

    planes_data = find_2D_projections(plot_young,maximum,'young')
    for plane_name, colors in planes_data.items():
        for color_category, coords in colors.items():
            if coords['x']:
                if color_category == 'maximum':
                    line_color = color_maximum
                elif color_category == 'negative':
                    line_color = color_negative
                else:
                    line_color = color_minimum

                plot_young.add_trace(go.Scatter3d(
                    x=coords['x'], y=coords['y'], z=coords['z'],
                    mode='lines',
                    line=dict(color=line_color, width=width_2d_projection),
                    name=f"Proj {plane_name} ({color_category})",
                    showlegend=False
                ))
    
    plot_young.write_image(os.join.path(path_output,"plot_young_3d.png"), width=800, height=600, scale=3)

def poisson_plot_3D(elastic_matrix, path_output):
    """
        Plot the 3D surfaces for the Poissons's ratio using Elasticpy and Plotly.

        Args: 
            elastic_matrix (list): Computed matrix with the elastic constants Cij.
            path_: Path to the directory to save the image.
        Returns:
            None.
    """
    stiffness_matrix = StiffnessTensor(elastic_matrix)
    poisson = stiffness_matrix.Poisson_ratio
    plot_poisson = poisson.plot3D()
    maximum = maximum_find(poisson.max())
    
    plot_poisson.data[0].update(
        colorscale=[[0, color_negative], [0.5, color_minimum], [1, color_minimum]],
        opacity=1.0,
    )
    plot_poisson.data[1].update(
        colorscale=[[0, color_maximum], [1, color_maximum]],
        opacity=0.6,
        lighting=dict(
            ambient=0.8, 
            diffuse=0.99, 
            specular=0.3, 
            roughness=0.9, 
            fresnel=0.9
        ),
    )

    plot_poisson.update_layout(plot_axis_config(maximum, "ν<sub>x</sub>", "ν<sub>y</sub>", "ν<sub>z</sub>"))
    plot_poisson.update_traces(plot_traces_config())

    planes_data = find_2D_projections(plot_poisson,maximum,'poisson')
    for plane_name, colors in planes_data.items():
        for color_category, coords in colors.items():
            if coords['x']:
                if color_category == 'maximum':
                    line_color = color_maximum
                elif color_category == 'negative':
                    line_color = color_negative
                else:
                    line_color = color_minimum

                plot_poisson.add_trace(go.Scatter3d(
                    x=coords['x'], y=coords['y'], z=coords['z'],
                    mode='lines',
                    line=dict(color=line_color, width=width_2d_projection),
                    name=f"Proj {plane_name} ({color_category})",
                    showlegend=False
                ))
    
    plot_poisson.write_image(os.join.path(path_output,"plot_poisson_3d.png"), width=800, height=600, scale=3)

def shear_plot_3D(elastic_matrix, path_output):
    """
        Plot the 3D surfaces for the shear modulus using Elasticpy and Plotly.

        Args: 
            elastic_matrix (list): Computed matrix with the elastic constants Cij.
            path_: Path to the directory to save the image.
        Returns:
            None.
    """
    stiffness_matrix = StiffnessTensor(elastic_matrix)
    shear = stiffness_matrix.shear_modulus
    plot_shear = shear.plot3D()
    maximum = maximum_find(shear.max())
    
    plot_shear.data[0].update(
        colorscale=[[0, color_negative], [0.5, color_minimum], [1, color_minimum]],
        opacity=1.0,
    )
    plot_shear.data[1].update(
        colorscale=[[0, color_maximum], [1, color_maximum]],
        opacity=0.6,
        lighting=dict(
            ambient=0.8, 
            diffuse=0.99, 
            specular=0.3, 
            roughness=0.9, 
            fresnel=0.9
        ),
    )

    plot_shear.update_layout(plot_axis_config(maximum, "G<sub>yz</sub>", "G<sub>xz</sub>", "G<sub>xy</sub>"))
    plot_shear.update_traces(plot_traces_config())

    planes_data = find_2D_projections(plot_shear,maximum,'shear')
    for plane_name, colors in planes_data.items():
        for color_category, coords in colors.items():
            if coords['x']:
                if color_category == 'maximum':
                    line_color = color_maximum
                elif color_category == 'negative':
                    line_color = color_negative
                else:
                    line_color = color_minimum

                plot_shear.add_trace(go.Scatter3d(
                    x=coords['x'], y=coords['y'], z=coords['z'],
                    mode='lines',
                    line=dict(color=line_color, width=width_2d_projection),
                    name=f"Proj {plane_name} ({color_category})",
                    showlegend=False
                ))
    
    plot_shear.write_image(os.join.path(path_output,"plot_shear_3d.png"), width=800, height=600, scale=3)

def linear_plot(elastic_matrix, path_output):
    """
        Plot the 3D surfaces for the linaer compressibility using Elasticpy and Plotly.

        Args: 
            elastic_matrix (list): Computed matrix with the elastic constants Cij.
            path_output: Path to the directory to save the image.
        Returns:
            None.
    """
    stiffness_matrix = StiffnessTensor(elastic_matrix)
    linear = stiffness_matrix.bulk_modulus
    plot_linear = linear.plot3D()
    maximum = maximum_find(linear.max())
    
    plot_linear.data[0].update(
        colorscale=[[0, color_negative], [0.5, color_minimum], [1, color_minimum]],
        opacity=0.6,
        lighting=dict(
            ambient=0.8, 
            diffuse=0.99, 
            specular=0.3, 
            roughness=0.9, 
            fresnel=0.9
        ),
    )

    plot_linear.update_layout(plot_axis_config(maximum, "β<sub>x</sub>", "β<sub>y</sub>", "β<sub>z</sub>"))
    plot_linear.update_traces(plot_traces_config())

    planes_data = find_2D_projections(plot_linear,maximum,'linear')
    for plane_name, colors in planes_data.items():
        for color_category, coords in colors.items():
            if coords['x']:
                if color_category == 'maximum':
                    line_color = color_maximum
                elif color_category == 'negative':
                    line_color = color_negative
                else:
                    line_color = color_minimum

                plot_linear.add_trace(go.Scatter3d(
                    x=coords['x'], y=coords['y'], z=coords['z'],
                    mode='lines',
                    line=dict(color=line_color, width=width_2d_projection),
                    name=f"Proj {plane_name} ({color_category})",
                    showlegend=False
                ))
    
    plot_linear.write_image(os.join.path(path_output,"plot_linear_3d.png"), width=800, height=600, scale=3)

def young_plot_2D(elastic_matrix, path_output):
    """
        Plot the 3D surfaces for the Young's modulus Plotly.

        Args: 
            elastic_matrix (list): Computed matrix with the elastic constants Cij.
            path_: Path to the directory to save the image.
        Returns:
            None.
    """
    compilance = np.linalg.inv(elastic_matrix)
    theta = np.linspace(0, 2*np.pi, 360)
    c = np.cos(theta)
    s = np.sin(theta)
    S11 = compilance[0,0]
    S22 = compilance[1,1]
    S66 = compilance[2,2]
    S12 = compilance[0,1]
    S16 = compilance[0,2]
    S26 = compilance[1,2]

    E = 1 / ((S11 * c**4) + (2 * S16 * c**3 * s) + ((2 * S12 + S66) * c**2 * s**2) + (2 * S26 * c * s**3) + (S22 * s**4))
    
    if np.max(E) <= 200.00:
        step = 50
    elif np.max(E) >= 200.00 and np.max(E) <= 600.00:
        step = 100
    elif np.max(E) > 600.00:
        step = 200

    plot_2D_config(theta, E, color_2d_E, step, "E (N/m)",  path_output, "plot_young_2d")

def poisson_plot_2D(elastic_matrix, path_output):
    """
        Plot the 3D surfaces for the Poissons's ratio using Plotly.

        Args: 
            elastic_matrix (list): Computed matrix with the elastic constants Cij.
            path_: Path to the directory to save the image.
        Returns:
            None.
    """
    compilance = np.linalg.inv(elastic_matrix)
    theta = np.linspace(0, 2*np.pi, 360)
    c = np.cos(theta)
    s = np.sin(theta)
    S11 = compilance[0,0]
    S22 = compilance[1,1]
    S66 = compilance[2,2]
    S12 = compilance[0,1]
    S16 = compilance[0,2]
    S26 = compilance[1,2]

    nu = -(S12 * (c**4 + s**4) + (S11 + S22 - S66) * c**2 * s**2 - (S16 - S26) * c * s * (c**2 - s**2))/((S11 * c**4) + (2 * S16 * c**3 * s) + ((2 * S12 + S66) * c**2 * s**2) + (2 * S26 * c * s**3) + (S22 * s**4))

    if np.max(nu) <= 0.2:
        step = 0.05
    elif np.max(nu) >= 0.2 and np.max(nu) <= 0.6:
        step = 0.1
    elif np.max(nu) >= 600.00:
        step = 0.2

    plot_2D_config(theta, nu, color_2d_nu_positive, step, "ν", path_output, "plot_poisson_2d")

def shear_plot_2D(elastic_matrix, path_output):
    """
        Plot the 3D surfaces for the shear modulus using Plotly.
        Args: 
            elastic_matrix (list): Computed matrix with the elastic constants Cij.
            path_: Path to the directory to save the image.
        Returns:
            None.
    """
    compilance = np.linalg.inv(elastic_matrix)
    theta = np.linspace(0, 2*np.pi, 360)
    c = np.cos(theta)
    s = np.sin(theta)
    S11 = compilance[0,0]
    S22 = compilance[1,1]
    S66 = compilance[2,2]
    S12 = compilance[0,1]
    S16 = compilance[0,2]
    S26 = compilance[1,2]

    G = 1 / (S66 * (c**2 - s**2)**2 + 4 * (S11 + S22 - 2 * S12) * c**2 * s**2 + 4 * (S16 - S26) * c * s * (c**2 - s**2))

    if np.max(G) <= 1:
        step = 0.25
    elif np.max(G) >= 1.0 and np.max(G) <= 30.0:
        step = 5
    elif np.max(G) >= 30.0 and np.max(G) <= 60:
        step = 10
    else:
        step = 50

    plot_2D_config(theta, G, color_2d_G, step, "G (N/m)", path_output, "plot_shear_2d")