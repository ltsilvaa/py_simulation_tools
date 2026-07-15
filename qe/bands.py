from ase.dft.kpoints import get_special_points, bandpath
from ase.geometry import Cell

def band_path(R0: list, dimension: str):
    """
        Find the high symmetry path to compute bands estructure and phonon dispersion.

        Args: 
            R0 (list): Optimizaed lattice vectors.
            dimension (str): Dimmnsion of the material (1D, 2D or 3D).

        Returns:
            Correct bands path for the lattice
    """
    if dimension == '1D' or dimension == '1d':
        R0[2,2] = 0.0
        R0[1,1] = 0.0
    elif dimension == '2D' or dimension == '2d':
        R0[2,2] = 0.0

    cell = Cell(R0)

    bravais_lattice = cell.get_bravais_lattice() 
    bands = bravais_lattice.bandpath()
    symmetry_path = bands.path
    symmetry_label = [char for char in symmetry_path if char.isupper()]
    symmetry_points = [bands.special_points[str(l)] for l in symmetry_label]

    return bravais_lattice.name, symmetry_label, [arr.tolist() for arr in symmetry_points]

def path_bands_qe(path_points, R0, dimension):
    name, labels, points = band_path(R0, dimension)
    qe_path = rf"{len(labels)}\n"
    for i,j in zip(labels, points):
        qe_path += rf"  {" ".join(point for point in points[i])} {path_points} !{labels[i]}"

    return qe_path