import numpy as np


def kalman_block(x, P, s, A, H, Q, R):
    """
    Prediction and update in Kalman filter
    input:
        - signal: signal to be filtered
        - x: previous mean state
        - P: previous variance state
        - s: current observation
        - A, H, Q, R: kalman filter parameters
    output:
        - x: mean state prediction
        - P: variance state prediction
    """

    # check laaraiedh2209 for further understand these equations

    x_mean = A * x + np.random.normal(0, Q, 1)
    P_mean = A * P * A + Q

    K = P_mean * H * (1 / (H * P_mean * H + R))
    x = x_mean + K * (s - H * x_mean)
    P = (1 - K * H) * P_mean

    return x, P


def kalman_filter(signal, A, H, Q, R):
    """
    Implementation of Kalman filter.
    Takes a signal and filter parameters and returns the filtered signal.
    input:
        - signal: signal to be filtered
        - A, H, Q, R: kalman filter parameters
    output:
        - filtered signal
    """

    predicted_signal = []

    # takes first value as first filter prediction
    x = signal[0]
    P = 0                                         # set first covariance state value to zero

    predicted_signal.append(x)
    # iterates on the entire signal, except the first element
    for j, s in enumerate(signal[1:]):

        # calculates next state prediction
        x, P = kalman_block(x, P, s, A, H, Q, R)

        # update predicted signal with this step calculation
        predicted_signal.append(x)

    return predicted_signal
