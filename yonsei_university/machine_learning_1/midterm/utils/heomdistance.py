from distython import HEOM
from overrides import overrides
import numpy as np


class HeomDistance(HEOM):
    """Modified ``heom`` method from parent class ``HEOM`` to make it compatible to Scikit-Learn's KNNImputer.
    
    Original code can be found @ "https://github.com/KacperKubara/distython/blob/master/HEOM.py"
    """
    def __init__(self, X, cat_ix, normalised):
        super().__init__(X=X, cat_ix=cat_ix, normalised=normalised)
        
    @overrides
    def heom(self, x, y, **kwargs):
        nan_equivalents = kwargs['missing_values']
        
        # Initialise results' array
        results_array = np.zeros(x.shape)

        # Get indices for missing values, if any
        nan_x_ix = np.flatnonzero( np.logical_or(np.isin(x, [nan_equivalents]), np.isnan(x)))
        nan_y_ix = np.flatnonzero( np.logical_or(np.isin(y, [nan_equivalents]), np.isnan(y)))
        nan_ix = np.unique(np.concatenate((nan_x_ix, nan_y_ix)))
        # Calculate the distance for missing values elements
        results_array[nan_ix] = 1

        # Get categorical indices without missing values elements
        cat_ix = np.setdiff1d(self.cat_ix, nan_ix)
        # Calculate the distance for categorical elements
        results_array[cat_ix]= np.not_equal(x[cat_ix], y[cat_ix]) * 1 # use "* 1" to convert it into int

        # Get numerical indices without missing values elements
        num_ix = np.setdiff1d(self.col_ix, self.cat_ix)
        num_ix = np.setdiff1d(num_ix, nan_ix)
        # Calculate the distance for numerical elements
        results_array[num_ix] = np.abs(x[num_ix] - y[num_ix]) / self.range[num_ix]
        
        # Return the final result
        # Square root is not computed in practice
        # As it doesn't change similarity between instances
        return np.sum(np.square(results_array))