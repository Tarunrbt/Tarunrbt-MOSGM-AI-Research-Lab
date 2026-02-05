# MOSGM Sensitivity Scan

from theory.response_potential import ResponsePotential

# --- Test parameter ---
alpha = 0.1

# Create MOSGM-II response object
mosgm_response = ResponsePotential(alpha=alpha)


def compute_effective_potential(phi_newton, omega):
    """
    Returns MOSGM-II modified potential
    """
    phi_mosgm = mosgm_response.effective_potential(
        phi_newton,
        omega
    )

    return phi_mosgm


def compute_modified_acceleration(
    grad_phi_newton,
    phi_newton,
    omega
):
    """
    Returns MOSGM-II modified acceleration
    """
    acc_mosgm = mosgm_response.modified_acceleration(
        grad_phi_newton,
        phi_newton,
        omega
    )

    return acc_mosgm
