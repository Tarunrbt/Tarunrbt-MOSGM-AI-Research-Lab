import numpy as np
from scipy.stats import spearmanr
from theory.response_potential import ResponsePotential

# =================================================================
# SECTION 1: INITIALIZATION & GLOBAL PARAMS
# =================================================================
ALPHA_DEFAULT = 0.1 
mosgm_response_default = ResponsePotential(alpha=ALPHA_DEFAULT)

# =================================================================
# SECTION 2: CORE MOSGM-II LOGIC (Default Pipeline)
# =================================================================

def compute_effective_potential(phi_newton, omega):
    return mosgm_response_default.effective_potential(phi_newton, omega)

def compute_modified_acceleration(grad_phi_newton, phi_newton, omega):
    return mosgm_response_default.modified_acceleration(grad_phi_newton, phi_newton, omega)

# =================================================================
# SECTION 3: AUTOMATED ALPHA SCAN & STABILITY UTILITIES
# =================================================================

def build_response(alpha):
    return ResponsePotential(alpha=alpha)

def run_pipeline_with_alpha(alpha, phi_newton, grad_phi_newton, omega, observed_data):
    response = build_response(alpha)
    
    phi_newton_result = phi_newton
    phi_mosgm_result = response.effective_potential(phi_newton, omega)
    acc_mosgm_result = response.modified_acceleration(grad_phi_newton, phi_newton, omega)

    # Statistical Validation with Stability Handling
    res_newton = spearmanr(observed_data, phi_newton_result)
    res_mosgm = spearmanr(observed_data, phi_mosgm_result)
    
    rho_newton = res_newton.correlation if res_newton.correlation is not None else np.nan
    rho_mosgm = res_mosgm.correlation if res_mosgm.correlation is not None else np.nan

    return {
        "alpha": alpha,
        "rho_newton": rho_newton,
        "rho_mosgm": rho_mosgm,
        "newton_signal": phi_newton_result,
        "mosgm_signal": phi_mosgm_result,
        "acceleration": acc_mosgm_result,
    }

def alpha_grid(start=0.0, stop=0.5, step=0.05):
    """Generates a clean, precision-fixed parameter space."""
    grid = np.arange(start, stop + step, step)
    return np.round(grid, 5) # Prevents floating-point drift

def run_alpha_scan(phi_newton, grad_phi_newton, omega, observed_data,
                   start=0.0, stop=0.5, step=0.05):
    results = []
    for a in alpha_grid(start, stop, step):
        out = run_pipeline_with_alpha(a, phi_newton, grad_phi_newton, omega, observed_data)
        results.append(out)
    return results

def best_alpha_by_rho(scan_results):
    """Extracts the Golden Alpha using robust NaN handling."""
    best = max(scan_results, key=lambda x: (np.nan_to_num(x["rho_mosgm"], nan=-1.0)))
    return best["alpha"], best["rho_mosgm"]

# =================================================================
# COMMIT MESSAGE: Add precision-fixed alpha scan and Spearman stability
# =================================================================
