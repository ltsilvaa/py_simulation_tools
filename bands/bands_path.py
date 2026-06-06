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
    symmetr_label = [char for char in symmetry_path if char.isupper()]
    symmetry_points = [bands.special_points[str(l)] for l in symmetr_label]

    return symmetry_path+" "+bravais_lattice.name, [arr.tolist() for arr in symmetry_points]
