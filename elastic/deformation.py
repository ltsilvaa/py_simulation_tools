import numpy as np

"""
    Possible deformations in a material for compute elastic constatns followin the Voigt notataion: 
    1 - xx, 2 - yy, 3 - zz, 4 - yz, 5 - xz, 6 - xy.
    
    Also the isotropic deformation for bulk modulus calculation.
"""

def def_11(R, eps: float): 
    """
        Apply pure normal stain in x direction.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_11 = np.array([[eps, 0, 0],[0, 0, 0],[0, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_11))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_12(R, eps: float):
    """
        Apply pure normal stain in x and y directions simultaneously.
 
        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_12 = np.array([[eps, 0, 0],[0, eps, 0],[0, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_12))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_13(R, eps: float):
    """
        Apply pure normal stain in x and z directions simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_13 = np.array([[eps, 0, 0],[0, 0, 0],[0, 0, eps]])
    R_deformed = np.matmul(R,(np.eye(3)+def_13))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )


def def_14(R, eps: float):
    """
        Apply normal stain in x direction and shear strain in yz plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_14 = np.array([[eps, 0, 0],[0, 0, eps],[0, eps, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_14))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_15(R, eps: float):
    """
        Apply normal stain in x direction and shear strain in xz plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_15 = np.array([[eps, 0, eps],[0, 0, 0],[eps, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_15))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_16(R, eps: float):
    """
        Apply normal stain in x direction and shear strain in xy plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_16 = np.array([[eps, eps, 0],[eps, 0, 0],[0, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_16))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_22(R, eps: float):
    """
        Apply pure normal stain in y direction.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_22 = np.array([[0, 0, 0],[0, eps, 0],[0, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_22))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )


def def_23(R, eps: float):
    """
        Apply pure normal stain in y and z directions simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_23 = np.array([[0, 0, 0],[0, eps, 0],[0, 0, eps]])
    R_deformed = np.matmul(R,(np.eye(3)+def_23))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_24(R, eps: float):
    """
        Apply normal stain in y direction and shear strain in yz plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_24 = np.array([[0, 0, 0],[0, eps, eps],[0, eps, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_24))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_25(R, eps: float):
    """
        Apply normal stain in y direction and shear strain in xz plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_25 = np.array([[0, 0, eps],[0, eps, 0],[eps, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_25))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_26(R, eps: float):
    """
        Apply normal stain in y direction and shear strain in xy plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_26 = np.array([[0, eps, 0],[eps, eps, 0],[0, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_26))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_33(R, eps: float):
    """
        Apply pure normal stain in z direction.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_33 = np.array([[0, 0, 0],[0, 0, 0],[0, 0, eps]])
    R_deformed = np.matmul(R,(np.eye(3)+def_33))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_34(R, eps: float):
    """
        Apply normal stain in z direction and shear strain in yz plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_34 = np.array([[0, 0, 0],[0, 0, eps],[0, eps, eps]])
    R_deformed = np.matmul(R,(np.eye(3)+def_34))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )


def def_35(R, eps: float):
    """
        Apply normal stain in z direction and shear strain in xz plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_35 = np.array([[0, 0, eps],[0, 0, 0],[eps, 0, eps]])
    R_deformed = np.matmul(R,(np.eye(3)+def_35))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_36(R, eps: float):
    """
        Apply normal stain in z direction and shear strain in xy plane simultaneously.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_36 = np.array([[0, eps, 0],[0, eps, 0],[0, 0, eps]])
    R_deformed = np.matmul(R,(np.eye(3)+def_36))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_44(R, eps: float):
    """
        Apply pure shear stain in yz plane.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_44 = np.array([[0, 0, 0],[0, 0, eps],[0, eps, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_44))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_45(R, eps: float):
    """
        Apply pure shear stain in yz plane.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_44 = np.array([[0, 0, eps],[0, 0, eps],[eps, eps, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_44))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_46(R, eps: float):
    """
        Apply pure shear stain in yz plane.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_44 = np.array([[0, eps, 0],[eps, 0, eps],[0, eps, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_44))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_55(R, eps: float):
    """
        Apply pure shear stain in xz plane.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_55 = np.array([[0, 0, eps],[0, 0, 0],[eps, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_55))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_56(R, eps: float):
    """
        Apply pure shear stain in xz plane.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_55 = np.array([[0, eps, eps],[eps, 0, 0],[eps, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_55))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_66(R, eps: float):
    """
        Apply pure shear stain in xy plane.

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_66 = np.array([[0, eps, 0],[eps, 0, 0],[0, 0, 0]])
    R_deformed = np.matmul(R,(np.eye(3)+def_66))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )

def def_isotropic(R, eps: float): 
    """
        Apply isotropic normal stain (x,y, and directions simultaneously).

        Args: 
            R (np.list): Conventional cell, primitive cell or supercell vectors matrix of the crystal.
            eps (float): Deformation percentage of the cell.

        Retuns:
            Deformed vectors matrix.
    """
    def_iso = np.array([[eps, 0, 0],[0, eps, 0],[0, 0, eps]])
    R_deformed = np.matmul(R,(np.eye(3)+def_iso))
    return "\n".join(
        " ".join(f"{x:12.6f}" for x in line)
        for line in R_deformed
    )+"\n"