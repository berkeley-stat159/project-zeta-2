
import numpy.linalg as npl
from scipy.stats import t as t_dist

def batch_make_design(img_dict, convolved_dict):
    matrix = {}
    object_list = ["bottle", "cat", "chair", "face", "house", "scissors", "scrambledpix", "shoe"]
    for key, img in img_dict.iteritems():
        time_course = img.shape[-1]
        matrix[key] = np.ones((time_course,(len(object_list)+3)))
        for i in xrange(matrix[key].shape[-1]-3):
            matrix[key][:,i] = convolved_dict[key[7:] +"-"+ object_list[i]]
        LD = np.linspace(-1,1,time_course)
        LD2 = LD**2
        LD2 = LD2 - np.mean(LD2)
        matrix[key][:, -3] = LD
        matrix[key][:, -2] = LD2
    return matrix


def scale_design_mtx(X):
    """utility to scale the design matrix for display
    This scales the columns to their own range so we can see the variations
    across the column for all the columns, regardless of the scaling of the
    column.
    """
    mi, ma = X.min(axis=0), X.max(axis=0)

    # Vector that is True for columns where values are not
    # all almost equal to each other
    col_neq = (ma - mi) > 1.e-8
    Xs = np.ones_like(X)
    # Leave columns with same value throughout with 1s
    # Scale other columns to min, max in column
    mi = mi[col_neq]
    ma = ma[col_neq]
    Xs[:,col_neq] = (X[:,col_neq] - mi)/(ma - mi)
    return Xs


def batch_scale_matrix (matrix_dict):
    result = {}
    for key, matrix in matrix_dict.iteritems():
        result[key] = scale_design_mtx(matrix)
    return result

def batch_convert_2d (img_dict):
    result = {}
    for key, img in img_dict.iteritems():
        result[key] = np.reshape(img, (-1, img.shape[-1]))
    return result

def t_stat(y, X, c):
    """ betas, t statistic and significance test given data, design matrix, contrast
    This is OLS estimation; we assume the errors to have independent
    and identical normal distributions around zero for each $i$ in
    $\e_i$ (i.i.d).
    """
    # Make sure y, X, c are all arrays
    #y = np.asarray(y)
    #X = np.asarray(X)
    #c = c.T
    c = np.atleast_2d(c).T # As column vector
    # Calculate the parameters - b hat
    beta = npl.pinv(X).dot(y)
    # The fitted values - y hat
    fitted = X.dot(beta)
    # Residual error
    errors = y - fitted
    # Residual sum of squares
    RSS = (errors**2).sum(axis=0)
    # Degrees of freedom is the number of observations n minus the number
    # of independent regressors we have used.  If all the regressor
    # columns in X are independent then the (matrix rank of X) == p
    # (where p the number of columns in X). If there is one column that
    # can be expressed as a linear sum of the other columns then
    # (matrix rank of X) will be p - 1 - and so on.
    df = X.shape[0] - npl.matrix_rank(X)
    # Mean residual sum of squares
    MRSS = RSS / df
    # calculate bottom half of t statistic
    #SE = np.sqrt(MRSS * c.T.dot(npl.pinv(X.T.dot(X)).dot(c)))
    SE = np.sqrt(MRSS * c.T.dot(npl.pinv(X.T.dot(X)).dot(c)))
    t = c.T.dot(beta) / SE
    # Get p value for t value using cumulative density dunction
    # (CDF) of t distribution
    ltp = t_dist.cdf(t, df) # lower tail p
    p = 1 - ltp # upper tail p

    return beta, t, df, p