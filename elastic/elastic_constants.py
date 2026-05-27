import numpy as np

def deformations_list(deformations_number: int = 7, max_deformation: float = 0.01):
    """
        Create a list with the deformations to use in the fitting process.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
        Returns:
            Numpy list with all the deformations (epslon) applied in numerical order.
    """
    eps_list = []
    d_eps = max_deformation/((deformations_number-1)/2.0)
    for i in range(deformations_number):
        eps_list.append(-1*max_deformation + i*d_eps)
    return np.array(eps_list)

def fit_energy_strain(strain_energies, deformations_number: int = 7, max_deformation: float = 0.01):
    """
        Fit a fouth-order equation to the calculated energy values in each deformation process.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            strain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            A list of lists containing the adjustment coefficients.
    """
    fit_coefficients = []
    np_strain_energies = np.array(strain_energies)
    for i in range(21):
        if strain_energies[i] == np.zeros((deformations_number,), dtype=np.int):
            fit_coefficients.append(np.zeros((4,), dtype=np.int))
        else:
            fit_coefficients.append(np.polyfit(deformations_list(deformations_number, max_deformation),strain_energies[i],4))
    return fit_coefficients

def check_eigenvalues(elastic_matrix):
    """
        Calculate the eigenvalues to verify the Born stability criteria.

        Args:
            elastic_matrix (list): The 3x3 or 6x6 computed elastic matrix.
        Returns:
            True of false for the stability criteria.
    """
    eigenvalues = np.linalg.eigvals(np.array(elastic_matrix))
    return np.all(eigenvalues > 1e-8)

def elastic_constants_square_2D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 2D square lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    area = np.linalg.norm(np.cross(R0[0], R0[1]))
    C11 = 2*(coefficients[0,2]/area)*16.02176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/area)*16.02176634
    C66 = (coefficients[20,2]/(2*area))*16.02176634
    
    elastic_matrix = [[ C11, C12, 0.0],
                      [ 0.0, C11, 0.0],
                      [ 0.0, 0.0, C66]]
    
    return check_eigenvalues(elastic_matrix), elastic_matrix
                                        
def elastic_constants_rectangular_2D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 2D retangular lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    area = np.linalg.norm(np.cross(R0[0], R0[1]))
    C11 = 2*(coefficients[0,2]/area)*16.02176634
    C22 = 2*(coefficients[6,2]/area)*16.02176634
    C12 = ((coefficients[1,2] - coefficients[0,2] - coefficients[6,2])/area)*16.02176634
    C66 = (coefficients[20,2]/(2*area))*16.02176634

    elastic_matrix = [[ C11, C12, 0.0],
                      [ 0.0, C22, 0.0],
                      [ 0.0, 0.0, C66]]
    
    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_hexagonal_2D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 2D hexagonal lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    area = np.linalg.norm(np.cross(R0[0], R0[1]))
    C11 = 2*(coefficients[0,2]/area)*16.02176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/area)*16.02176634
    C66 = (C11 - C12)/2
    
    elastic_matrix = [[ C11, C12, 0.0],
                      [ 0.0, C11, 0.0],
                      [ 0.0, 0.0, C66]]
    
    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_oblique_2D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 2D oblique lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    area = np.linalg.norm(np.cross(R0[0], R0[1]))
    C11 = 2*(coefficients[0,2]/area)*16.02176634
    C22 = 2*(coefficients[6,2]/area)*16.02176634
    C12 = ((coefficients[1,2] - coefficients[0,2] - coefficients[6,2])/area)*16.02176634
    C16 = ((coefficients[5,2] - coefficients[0,2] - coefficients[20,2])/(2*area))*16.02176634
    C26 = ((coefficients[10,2] - coefficients[0,2] - coefficients[20,2])/(2*area))*16.02176634
    C66 = (coefficients[20,2]/(2*area))*16.02176634
    
    elastic_matrix = [[ C11, C12, C16],
                      [ 0.0, C22, C26],
                      [ 0.0, 0.0, C66]]
    
    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_cubic_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D cubic lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/volume)*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634

    elastic_matrix = [[ C11, C12, C12, 0.0, 0.0, 0.0],
                      [ 0.0, C11, C12, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, C11, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, C44, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C44]]

    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_hexagonal_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D hexagonal lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634

    elastic_matrix = [[ C11, C12, C13, 0.0, 0.0, 0.0],
                      [ 0.0, C11, C13, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, C33, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, C44, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]
    
    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_tetragonal_1_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D tetragonal type 1 lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634

    elastic_matrix = [[ C11, C12, C13, 0.0, 0.0, 0.0],
                      [ 0.0, C11, C13, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, C33, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, C44, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]
    
    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_tetragonal_2_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D tetragonal type 2 lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C16 = ((coefficients[5,2] - coefficients[0,2] - coefficients[20,2])/(2*volume))*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634

    elastic_matrix = [[ C11, C12, C13, 0.0, 0.0, C16],
                      [ 0.0, C11, C13, 0.0, 0.0,-C16],
                      [ 0.0, 0.0, C33, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, C44, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]    

    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_rhombohedral_1_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D rhombohedral type 1 lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C14 = ((coefficients[3,2] - coefficients[0,2] - coefficients[15,2])/(2*volume))*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634

    elastic_matrix = [[ C11, C12, C13, C14, 0.0, 0.0],
                      [ 0.0, C11, C13,-C14, 0.0, 0.0],
                      [ 0.0, 0.0, C33, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, C44, C14],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]

    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_rhombohedral_2_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D rhombohedral type 2 lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - 2*coefficients[0,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C14 = ((coefficients[3,2] - coefficients[0,2] - coefficients[15,2])/(2*volume))*160.2176634
    C15 = ((coefficients[4,2] - coefficients[0,2] - coefficients[18,2])/(2*volume))*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634
    
    elastic_matrix = [[ C11, C12, C13, C14, C15, 0.0],
                      [ 0.0, C11, C13,-C14,-C15, 0.0],
                      [ 0.0, 0.0, C33, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0,-C15],
                      [ 0.0, 0.0, 0.0, 0.0, C44, C14],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]    

    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_orthorhombic_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D orthorhombic lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """ 
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - coefficients[0,2] - coefficients[6,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C22 = 2*(coefficients[6,2]/volume)*160.2176634
    C23 = ((coefficients[7,2] - coefficients[6,2] - coefficients[11,2])/volume)*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C55 = (coefficients[18,2]/(2*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634

    elastic_matrix = [[ C11, C12, C13, 0.0, 0.0, 0.0],
                      [ 0.0, C22, C23, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, C33, 0.0, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, C55, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]
    
    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_monoclinic_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D monoclinic lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """ 
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - coefficients[0,2] - coefficients[6,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C15 = ((coefficients[4,2] - coefficients[0,2] - coefficients[18,2])/(2*volume))*160.2176634
    C22 = 2*(coefficients[6,2]/volume)*160.2176634
    C23 = ((coefficients[7,2] - coefficients[6,2] - coefficients[11,2])/volume)*160.2176634
    C25 = ((coefficients[9,2] - coefficients[6,2] - coefficients[18,2])/(2*volume))*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C35 = ((coefficients[13,2] - coefficients[11,2] - coefficients[18,2])/(2*volume))*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C46 = ((coefficients[17,2] - coefficients[15,2] - coefficients[20,2])/(4*volume))*160.2176634
    C55 = (coefficients[18,2]/(2*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634

    elastic_matrix = [[ C11, C12, C13, 0.0, C15, 0.0],
                      [ 0.0, C22, C23, 0.0, C25, 0.0],
                      [ 0.0, 0.0, C33, 0.0, C35, 0.0],
                      [ 0.0, 0.0, 0.0, C44, 0.0, C46],
                      [ 0.0, 0.0, 0.0, 0.0, C55, 0.0],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]    
    
    return check_eigenvalues(elastic_matrix), elastic_matrix

def elastic_constants_triclinic_3D(R0, max_deformation: float, deformations_number: int, strain_energies):
    """
        Compute the necessary elastic constants for a 3D trilinic lattice.

        Args:
            deformations_number (integer): Number of deformations perfomed.
            max_deformation (float): Maximum deformation applied. 
            srtain_energies (list): Matrix with the strain energies related to each deformation.
        Returns:
            True of false for the Born stability criteria and the computed elastic matrix.
    """ 
    coefficients = fit_energy_strain(deformations_number, max_deformation, strain_energies)
    volume = np.dot(R0[2],(np.cross(R0[0], R0[1])))
    C11 = 2*(coefficients[0,2]/volume)*160.2176634
    C12 = ((coefficients[1,2] - coefficients[0,2] - coefficients[6,2])/volume)*160.2176634
    C13 = ((coefficients[2,2] - coefficients[0,2] - coefficients[11,2])/volume)*160.2176634
    C14 = ((coefficients[3,2] - coefficients[0,2] - coefficients[15,2])/(2*volume))*160.2176634
    C15 = ((coefficients[4,2] - coefficients[0,2] - coefficients[18,2])/(2*volume))*160.2176634
    C16 = ((coefficients[5,2] - coefficients[0,2] - coefficients[20,2])/(2*volume))*160.2176634
    C22 = 2*(coefficients[6,2]/volume)*160.2176634
    C23 = ((coefficients[7,2] - coefficients[6,2] - coefficients[11,2])/volume)*160.2176634
    C24 = ((coefficients[8,2] - coefficients[6,2] - coefficients[15,2])/(2*volume))*160.2176634
    C25 = ((coefficients[9,2] - coefficients[6,2] - coefficients[18,2])/(2*volume))*160.2176634
    C26 = ((coefficients[10,2] - coefficients[6,2] - coefficients[20,2])/(2*volume))*160.2176634
    C33 = 2*(coefficients[11,2]/volume)*160.2176634
    C34 = ((coefficients[12,2] - coefficients[11,2] - coefficients[15,2])/(2*volume))*160.2176634
    C35 = ((coefficients[13,2] - coefficients[11,2] - coefficients[18,2])/(2*volume))*160.2176634
    C36 = ((coefficients[14,2] - coefficients[11,2] - coefficients[20,2])/(2*volume))*160.2176634
    C44 = (coefficients[15,2]/(2*volume))*160.2176634
    C45 = ((coefficients[16,2] - coefficients[15,2] - coefficients[18,2])/(4*volume))*160.2176634
    C46 = ((coefficients[17,2] - coefficients[15,2] - coefficients[20,2])/(4*volume))*160.2176634
    C55 = (coefficients[18,2]/(2*volume))*160.2176634
    C56 = ((coefficients[19,2] - coefficients[18,2] - coefficients[20,2])/(4*volume))*160.2176634
    C66 = (coefficients[20,2]/(2*volume))*160.2176634
    
    elastic_matrix = [[ C11, C12, C13, C14, C15, C16],
                      [ 0.0, C11, C23, C24, C25, C26],
                      [ 0.0, 0.0, C33, C34, C35, C36],
                      [ 0.0, 0.0, 0.0, C44, C45, C46],
                      [ 0.0, 0.0, 0.0, 0.0, C55, C56],
                      [ 0.0, 0.0, 0.0, 0.0, 0.0, C66]]    

    return check_eigenvalues(elastic_matrix), elastic_matrix
