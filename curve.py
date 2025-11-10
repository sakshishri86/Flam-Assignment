import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import differential_evolution

#Section 1: Data Handling & Visualization
def load_and_prepare_data(filepath: str):
    """Loads and prepares data from the CSV file."""
    try:
        data_df = pd.read_csv(filepath)
    except FileNotFoundError:
        return None, None, None
    x_data = data_df['x'].values
    y_data = data_df['y'].values
    t_data = np.linspace(6, 60, len(x_data))
    return x_data, y_data, t_data

# Section 2: Mathematical Model & Objective Function

def predict_curve_points(params: np.ndarray, t: np.ndarray):
    """Calculates (x, y) coordinates based on the parametric equations."""
    theta_deg, M, X = params
    theta_rad = np.deg2rad(theta_deg)
    exp_term = np.exp(M * np.abs(t)) * np.sin(0.3 * t)
    x_pred = (t * np.cos(theta_rad) - exp_term * np.sin(theta_rad) + X)
    y_pred = (42 + t * np.sin(theta_rad) + exp_term * np.cos(theta_rad))
    return x_pred, y_pred

def calculate_l1_loss(params: np.ndarray, t_data: np.ndarray, x_data: np.ndarray, y_data: np.ndarray):
    """
    This function does EXACTLY what you asked:
    1. It gets the predicted points using predict_curve_points().
    2. It takes the expected points (x_data, y_data) from the CSV.
    3. It calculates the difference and sums them up.
    """
    x_pred, y_pred = predict_curve_points(params, t_data)
    loss = np.sum(np.abs(x_data - x_pred) + np.abs(y_data - y_pred))
    return loss

# Section 3: Optimization & Analysis

def find_optimal_parameters(t_data: np.ndarray, x_data: np.ndarray, y_data: np.ndarray):
    """Runs an aggressive differential evolution optimizer."""
    bounds = [(0, 50), (-0.05, 0.05), (0, 100)]
    result = differential_evolution(
        func=calculate_l1_loss, bounds=bounds, args=(t_data, x_data, y_data),
        strategy='best1bin', maxiter=3000, popsize=50, tol=1e-9,
        recombination=0.8, disp=False, polish=True
    )
    return result

if __name__ == "__main__":
    
    csv_filepath = '/workspaces/Flam-Assignment/xy_data.csv'
    x_points, y_points, t_points = load_and_prepare_data(csv_filepath)

    if x_points is not None:
        
        print(" Finding Best Parameters")
        optimization_result = find_optimal_parameters(t_points, x_points, y_points)
        final_params = optimization_result.x
        total_l1_loss = optimization_result.fun
        print("Optimization complete.\n")
        
        # CALCULATION FOR THE FIRST POINT 
        print("calculation for a single point")
        
        # 1.First EXPECTED point from the CSV file
        first_expected_x = x_points[0]
        first_expected_y = y_points[0]
        
        # 2.First PREDICTED point using our best parameters
        first_predicted_x, first_predicted_y = predict_curve_points(final_params, t_points[0])
        
        # 3.DIFFERENCE for this single point
        single_point_loss = np.abs(first_expected_x - first_predicted_x) + np.abs(first_expected_y - first_predicted_y)
        
        print(f"For the very first point:")
        print(f"   - Expected Point (from CSV):    ({first_expected_x:.4f}, {first_expected_y:.4f})")
        print(f"   - Predicted Point (from formula): ({first_predicted_x:.4f}, {first_predicted_y:.4f})")
        print(f"   - L1 Difference for this point: {single_point_loss:.4f}")

        #Average error per point from the total loss
        average_error = total_l1_loss / len(x_points)
        print(f"\nThe average L1 difference per point across all {len(x_points)} points is: {average_error:.4f}")
        print(f"This is why the TOTAL SUMMED L1 Loss ({len(x_points)} * {average_error:.4f}) is approx {total_l1_loss:.4f}\n")

        #FINAL REPORT
        print("================ FINAL REPORT ================")
        print("The parameters below represent the closest possible fit given the data.")
        
        theta_opt, m_opt, x_opt = final_params
        print(f"Optimal Theta (θ): {theta_opt:.6f} degrees")
        print(f"Optimal M:         {m_opt:.6f}")
        print(f"Optimal X:         {x_opt:.6f}")
        print(f"Minimum TOTAL L1 Loss: {total_l1_loss:.4f}")
        
        theta_rad_opt = np.deg2rad(theta_opt)
        latex_string = (
            f"\\left(t*\\cos({theta_rad_opt:.6f})"
            f"-e^{{{m_opt:.6f}\\left|t\\right|}}\\cdot\\sin(0.3t)\\sin({theta_rad_opt:.6f})"
            f"\\ +{x_opt:.6f},"
            f"42+\\ t*\\sin({theta_rad_opt:.6f})"
            f"+e^{{{m_opt:.6f}\\left|t\\right|}}\\cdot\\sin(0.3t)\\cos({theta_rad_opt:.6f})\\right)"
        )
        print("\nRequired Submission String")
        print(latex_string)
        print("============================================")
