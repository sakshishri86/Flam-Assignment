
# Flam-Assignment
# Estimation of Unknown Parameters in a Parametric Curve Equation

---

## 1. Problem Overview

The task was to determine the unknown variables `θ` (theta), `M`, and `X` in the given parametric equations of a curve:

> $$
> x = t \cdot \cos(\theta) - e^{M|t|} \cdot \sin(0.3t) \cdot \sin(\theta) + X
> $$
> $$
> y = 42 + t \cdot \sin(\theta) + e^{M|t|} \cdot \sin(0.3t) \cdot \cos(\theta)
> $$

A list of points `(x, y)` corresponding to the parameter range `6 < t < 60` was provided in the dataset `xy_data.csv`. The objective was to estimate the parameters such that the predicted curve closely fits the given data points.

## 2. Objective

To find the optimal values of `θ`, `M`, and `X` that minimize the **L1 distance** (sum of absolute differences) between the actual and predicted curve coordinates.

---

## 3. Approach

### Step 1: Data Handling
*   The dataset `xy_data.csv` was read using the **pandas** library.
*   The `x` and `y` coordinates were extracted into NumPy arrays.
*   A corresponding `t` array was generated using linear spacing between 6 and 60 to match the number of data points.

### Step 2: Mathematical Model
*   The parametric equations were implemented in a function that computes predicted `(x, y)` coordinates for any given set of parameters `(θ, M, X)`.
*   The value of `θ` was converted from degrees to radians for trigonometric operations.
*   The exponential component `e^(M|t|) * sin(0.3t)` was included to account for periodic and exponential variations.

### Step 3: Loss Function
*   An **L1 loss function** was used to quantify the difference between actual and predicted coordinates. This function provides a robust measure for curve fitting by penalizing deviations equally.
    > $$
    > L = \sum (|x_{true} - x_{pred}| + |y_{true} - y_{pred}|)
    > $$

### Step 4: Optimization
*   The **Differential Evolution** algorithm from the `scipy.optimize` module was employed to minimize the L1 loss.
*   The parameter search space was constrained by the following bounds:
    *   `θ` ∈ [0°, 50°]
    *   `M` ∈ [–0.05, 0.05]
    *   `X` ∈ [0, 100]
*   The optimizer iteratively refined these parameters until a solution that minimized the loss was found.
### Step 5: Sample Calculation for One Point

To validate the formula, one sample point from the dataset was used to manually verify the model’s computation.
The L1 loss (sum of absolute differences) was calculated as:

L1 = |x_actual − x_pred| + |y_actual − y_pred|


For the first point:

(x_actual, y_actual) = (88.3645, 57.7844)
(x_pred, y_pred)     = (59.6701, 45.8043)


Step-by-step Calculation:

|88.3645 − 59.6701| = 28.6944
|57.7844 − 45.8043| = 11.9801
L1 = 28.6944 + 11.9801 = 40.6745


Conclusion:
The manual computation confirms that the calculated loss matches the objective function implemented in the code.

### Step 6: Evaluation
*   After optimization, the loss for the first data point was computed to verify the calculation.
*   The total L1 loss and the average difference per point were calculated to measure the overall goodness of fit for the model.

---

## 4. Results

| Parameter                         | Optimal Value   |
| --------------------------------- | --------------- |
| **θ (degrees)**                   | `28.118424`     |
| **M**                             | `0.021389`      |
| **X**                             | `54.900052`     |
| **Minimum Total L1 Loss**         | `37865.0938`    |
| **Average L1 Difference per Point**| `25.2434`       |

#### Verification for the First Point
*   **Expected:** `(88.3645, 57.7844)`
*   **Predicted:** `(59.6701, 45.8043)`
*   **L1 Difference:** `40.6745`

### Final Submission Equation

The final optimized equation representing the curve is given below:

**(x, y) = ( t * cos(0.490759) – e^(0.021389|t|) * sin(0.3t) * sin(0.490759) + 54.900052,  42 + t * sin(0.490759) + e^(0.021389|t|) * sin(0.3t) * cos(0.490759) )**

These parameters correspond to the best possible fit between the predicted and actual data points.


## 5. How to Run the Code

1.  Place the file `xy_data.csv` in the same directory as `curve.py`.
2.  Run the following command in the terminal:
    ```bash
    python curve.py
    ```
The script will perform the parameter optimization and display the final results in a structured report.

---

## 6. Conclusion

This project successfully identified the parameters `θ`, `M`, and `X` that best fit the given curve data using a numerical optimization approach. The Differential Evolution algorithm efficiently minimized the L1 loss, leading to a close approximation of the provided dataset. The implementation demonstrates the application of optimization techniques in mathematical modeling and parameter estimation. While a moderate L1 loss remains, the obtained parameters provide a reasonable and computationally stable fit for the given curve, suggesting a potential discrepancy between the idealized model and the provided data.
