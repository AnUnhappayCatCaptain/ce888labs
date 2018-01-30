import matplotlib
matplotlib.use('Agg')

import pandas as pd
import random
import matplotlib.pyplot as plt
import seaborn as sns

import numpy as np 

# def permutation(statistic, error):


# ------------------------------------------------------------------------
# sub-function for calculating mad.
# ------------------------------------------------------------------------

def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
        http://stackoverflow.com/questions/8930370/where-can-i-find-mad-mean-absolute-deviation-in-scipy
    """
    arr = np.ma.array(arr).compressed() # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))

# ------------------------------------------------------------------------
# sub-function for boostraping(std).
# ------------------------------------------------------------------------

def boostrap(statistic_func, iterations, data):
	samples  = np.random.choice(data,replace = True, size = [iterations, len(data)])
	#print samples.shape
	data_std = data.std()
	vals = []
	for sample in samples:
		sta = statistic_func(sample)
		#print sta
		vals.append(sta)
	b = np.array(vals)
	#print b
	lower, upper = np.percentile(b, [2.5, 97.5])
	return data_std,lower, upper

# -----------------------------------------------------------------------
# Main function.
# Firstly use pandas library processing data.
# Then plot scater and histogram of data.
# Thirdly give the specific variables for each fleet.#
# Finally boostrap to support results.
# -----------------------------------------------------------------------

if __name__ == "__main__":

# -----------------------------------------------------------------------
# Data processing
# -----------------------------------------------------------------------

	df = pd.read_csv('./vehicles.csv')
	df_column_C = df['Current fleet']
	df_column_N = df['New Fleet']
	df_column_N = df_column_N.dropna(how = 'any')
	df_new = df.dropna(how = 'any')

# -----------------------------------------------------------------------
# Scater plot scaters here.
# Scater x: current fleets.
# Scater y: new fleets.
# -----------------------------------------------------------------------

	sns_plot = sns.lmplot(df_new.columns[0], df_new.columns[1], data = df_new, fit_reg=False)

	sns_plot.axes[0,0].set_ylim(0,)
	sns_plot.axes[0,0].set_xlim(0,)

	sns_plot.savefig("scaterplotv.png",bbox_inches='tight')
	sns_plot.savefig("scaterplotv.pdf",bbox_inches='tight')

# ------------------------------------------------------------------------
# variables calculation.
# ------------------------------------------------------------------------

	data_C = df_column_C.values.T
	data_N = df_column_N.values.T
	print (data_C)
	print (data_N)

	print("")
	
	print("variables of current fleets:")
	print((("Mean of current fleets: %f")%(np.mean(data_C))))
	print((("Median of current fleets: %f")%(np.median(data_C))))
	print((("Var of current fleets: %f")%(np.var(data_C))))
	print((("std of current fleets: %f")%(np.std(data_C))))
	print((("MAD of current fleets: %f")%(mad(data_C))))

	print("")

	print("variables of new fleets:")
	print((("Mean of new fleets: %f")%(np.mean(data_N))))
	print((("Median of new fleets: %f")%(np.median(data_N))))
	print((("Var of new fleets: %f")%(np.var(data_N))))
	print((("std of new fleets: %f")%(np.std(data_N))))
	print((("MAD of new fleets: %f")%(mad(data_N))))

# ------------------------------------------------------------------------
# histogram plotting.
# ------------------------------------------------------------------------

	plt.clf()
	sns_plot2 = sns.distplot(data_C, bins=20, kde=False, rug=True).get_figure()
	axes = plt.gca()
	axes.set_xlabel('Current fleets') 
	axes.set_ylabel('Counts')
	sns_plot2.savefig("histogramv_C.png",bbox_inches='tight')
	sns_plot2.savefig("histogramv_C.pdf",bbox_inches='tight')

	plt.clf()
	sns_plot3 = sns.distplot(data_N, bins=20, kde=False, rug=True).get_figure()
	axes = plt.gca()
	axes.set_xlabel('New fleets') 
	axes.set_ylabel('Counts')
	sns_plot2.savefig("histogramv_N.png",bbox_inches='tight')
	sns_plot2.savefig("histogramv_N.pdf",bbox_inches='tight')

# -------------------------------------------------------------------------
# bootstraping for Current fleet.
# -------------------------------------------------------------------------
	boots_C = []
	for i in range(100,100000,1000):
		boot = boostrap(np.std, i, data_C)
		boots_C.append([i,boot[0], "std"])
		boots_C.append([i,boot[1], "lower"])
		boots_C.append([i,boot[2], "upper"])



	df_boot_C = pd.DataFrame(boots_C,  columns=['Boostrap Iterations','Std',"Value"])
	sns_plot = sns.lmplot(df_boot_C.columns[0],df_boot_C.columns[1], data=df_boot_C, fit_reg=False,  hue="Value")




	sns_plot.axes[0,0].set_ylim(0,)
	sns_plot.axes[0,0].set_xlim(0,100000)

	sns_plot.savefig("bootstrap_confidence_C.png",bbox_inches='tight')
	sns_plot.savefig("bootstrap_confidence_C.pdf",bbox_inches='tight')

# -------------------------------------------------------------------------
# bootstraping for New fleet.
# -------------------------------------------------------------------------
	boots_N = []
	for i in range(100,100000,1000):
		boot = boostrap(np.std, i, data_N)
		boots_N.append([i,boot[0], "Std"])
		boots_N.append([i,boot[1], "lower"])
		boots_N.append([i,boot[2], "upper"])



	df_boot_N = pd.DataFrame(boots_N,  columns=['Boostrap Iterations','Std',"Value"])
	sns_plot = sns.lmplot(df_boot_N.columns[0],df_boot_N.columns[1], data=df_boot_N, fit_reg=False,  hue="Value")




	sns_plot.axes[0,0].set_ylim(0,)
	sns_plot.axes[0,0].set_xlim(0,100000)

	sns_plot.savefig("bootstrap_confidence_N.png",bbox_inches='tight')
	sns_plot.savefig("bootstrap_confidence_N.pdf",bbox_inches='tight')
	


	
