import numpy as np
import keras
import keras.backend as K

class MCDropoutModel:
    """
        Monte Carlo Dropout implementation over a keras model.
        This class just wraps a keras model to enable dropout at inference time.
    """
    def __init__(self, model):
        """
            Builds a MC Dropout model from a keras model. The model should already be trained.
        """

        self.model = model
        self.mc_func = K.function([model.layers[0].input, K.learning_phase()],
                                  [model.layers[-1].output])
        self.mc_pred = lambda x: self.mc_func([x, 1])

    def predict(self, x, num_samples=10):
        """
            Performs a prediction using MC Dropout, and returns the mean and standard deviation of the model output.
        """
        samples = []

        for i in range(num_samples):
            samples.append(self.mc_pred(x))

        samples = np.array(samples)
        mean_pred = np.mean(samples, axis=0)[0]
        std_pred = np.std(samples, axis=0)[0]

        return mean_pred, std_pred

    def predict_samples(self, x, num_samples=10):
        """
            Performs a prediction using MC Dropout, and returns the produced output samples from the model.
        """

        samples = []

        for i in range(num_samples):
            samples.append(self.mc_pred(x))

        return np.array(samples)
