import numpy as np
import mbuild as mb


def boundary_positions(compounds):
    xs, ys, zs = list(), list(), list()
    if isinstance(compounds, mb.Compound):
        for part in compounds.particles():
            xs.append(part.pos[0])
            ys.append(part.pos[1])
            zs.append(part.pos[2])
    elif isinstance(compounds, (list, tuple)):
        for molecule in compounds:
            for part in molecule.particles():
                xs.append(part.pos[0])
                ys.append(part.pos[1])
                zs.append(part.pos[2])

    minima = (min(xs), min(ys), min(zs))
    maxima = (max(xs), max(ys), max(zs))
    return np.array(minima), np.array(maxima)

