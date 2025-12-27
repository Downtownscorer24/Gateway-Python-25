#----------------------------------------------------------------------------------------------------#
# FILE: projectd_template.py									#
# PURPOSE: Analyze eddy flux data from Harvard Forest						#
#												#
#----------------------------------------------------------------------------------------------------#


#----------#
# Notes:   #
#----------#


#----------------------#
# Required libraries   #
#----------------------#

import numpy as np
import matplotlib.pyplot as plt


#---------------------------#
# FUNCTION: readdata        #
#---------------------------#

def readdata(filename):
    
    # Purpose: Read in Harvard Forest data 
    
    hf = np.genfromtxt(filename, delimiter=",", dtype=float, skip_header=1)
    return hf

#---------------------------#
# FUNCTION: summarizedata   #
#---------------------------#

def summarizedata(hf):
    
    # Purpose:
    #	Create a plot of the CO2 data as a time series
    #	Calculate several summary statistics about the dataset.
    
    # Create a time series plot of the data
    t = hf[:,0] + (hf[:,1]*30.5 + hf[:,2]) / 365 # Formula to compute year+decimal form
    y = hf[:,3]
    
    #Plotting time series
    
    plt.figure()
    plt.plot(t, y, 'bo')
    plt.title("CO2 Flux Over Time")
    plt.xlabel("Time (Year)")
    plt.ylabel("CO2 Flux")
    
    # Display the plot
    # plt.show()

    # Find the number of data points
    num_data_pts = len(hf[:,0])
    
    # Find the mean of the data
    mean = round((np.mean(hf[:,3])),3)
    
    # Find the 25th percentile of the data points
    q1 = round((np.percentile(hf[:,3], 25)),3)
    
    # Find the 75th percentile of the data points
    q3 = round((np.percentile(hf[:,3], 75)),3)
    
    # Return the number of data points, the mean, the 25th percentile, and the 75th percentile
    
    return [num_data_pts, mean, q1, q3]

#---------------------------#
# FUNCTION: missingdata     #
#---------------------------#

def missingdata(hf):
    
    # Purpose: 
    # Find the percentage of missing data points in each year
    
    # Find the percentage of data in each year that are missing
    pct_missing = []
    
    start_year = int(np.min(hf[:,0]))
    end_year = int(np.max(hf[:,0]))
    
    # Year list as a 1 dimensional array
    
    year_list = hf[:,0]
    
    for i in range(start_year, end_year + 1):
        num_days = np.count_nonzero(year_list == i) # Count number of days for each year
        if (i % 4 == 0 and i % 100 != 0) or (i % 400 == 0): # Check if the year is a leap year
            pct = (1 - (num_days / 366)) * 100
        else:
            pct = (1 - (num_days / 365)) * 100

        pct_missing.append(round(pct,3))
    
    # Create a bar plot showing the percentage of data that are
    # missing in each year
    
    years = list(range(int(start_year), int(end_year + 1))) #Unique set of years
    years = [str(i) for i in years]
    
    #Plot bar graph
    
    plt.figure()
    plt.bar(years, pct_missing)
    plt.xticks(rotation=90)   # rotate x labels
    plt.xlabel("Year")
    plt.ylabel("Percent of Days Missing")
    plt.title("Percent of Days Missing Every Year")
    
    # Display the plot
    plt.show()
    
    # Return the result
    return (pct_missing)


#---------------------------#
# FUNCTION: seasonalcycle   #
#---------------------------#

def seasonalcycle(hf):
    
    # Purpose: 
    # 	Find the average flux by month for each year
    #	Plot the average monthly flux for years 1995 through (and including) 2000.
    
    # Determine the range of years
    
    start_year = int(np.min(hf[:,0]))
    end_year = int(np.max(hf[:,0]))
    
    # Dimensions of the avg_flux by month
    
    rows = end_year - start_year + 1
    cols = 12
    
    # Initialize an array full of np.nan
    
    flux_month = np.full((rows, cols), np.nan)
    
    # Find the average CO2 flux in each month  
       
    for i in range(start_year, end_year + 1):
        row = i - start_year # Adjust to correspond to row
        year_indicies = np.where(hf[:,0] == i) # Find indicies in data where the year is
        for k in range(1,13):
            flux_sum = 0
            days = 0
            for j in year_indicies[0]:
                if hf[j,1] == k: # Check if data point has the same month
                    flux_sum += hf[j,3]
                    days += 1
            if days == 0: # Check if there were no data points that month
                continue
            avg_flux = flux_sum / days
            flux_month[row, k - 1] = avg_flux.astype(float)   
    
    
    # Plot the average fluxes by month in several different years
    plt.figure()
    months = np.arange(1,13)
    
    start = 3 # To start at 1995
    
    colors = ['blue', 'red', 'green', 'orange', 'grey', 'black']
    
    legend = []
    
    for i in range(start, start + 6):
        plt.scatter(months, flux_month[i,:], c = colors[i - start])
        legend.append(f'{i - start + 1995}')
    plt.legend(legend)
    plt.title("Monthly Flux")
    plt.xlabel("Month")
    plt.ylabel("Average Flux")

    
    # Display the plot
    # plt.show()
    
    # Return the result
    return flux_month
    

#---------------------------#
# FUNCTION: HFregression    #
#---------------------------#

def HFregression(hf):
    
    # Purpose: 
        #    Create a regression model for CO2 fluxes
        #    Visualize the outputs of the model

    # Read in the data from the Harvard Forest
    '''your code'''
    
    # Create the X matrix for the regression
    factors = hf[:,4:] # n x 4 array of environmental factors from data   
    X_dim = factors.shape   
    ones_column = np.ones(X_dim[0]) # n x 1 vector of ones   
    X_matrix = np.empty((X_dim[0], 5)) # Intialize an empty array
    X_matrix[:,0] = ones_column    
    X_matrix[:,1:] = factors 
    flux_vector = hf[:,3]
    
    # Estimate the regression coefficients
    X_transposed = X_matrix.T
    
    XtX = np.dot(X_transposed, X_matrix)
    
    XtX_inv = np.linalg.inv(XtX)
    
    XtX_invXt = np.dot(XtX_inv, X_transposed)
    
    b_matrix = np.dot(XtX_invXt, flux_vector)
    
    
    
    # Create the model estimate
    Xb = np.dot(X_matrix, b_matrix)
    
    # Calculate the correlation coefficient
    
    correlation_matrix = np.dot(X_matrix, np.diag(b_matrix)) # B_matrix is made into a 5x5 diagonal matrix
    
    
    # Plot the model estimate and add the correlation coefficient to the plot
    t = hf[:,0] + (hf[:,1]*30.5 + hf[:,2]) / 365
    y = hf[:,3]
    
    r = np.corrcoef(y, Xb) # Find r
    
    r = round(r[0][1], 3)

    
    
    # Plotting both plots
    
    fig, ax = plt.subplots(2,1)
    
    ax[0].plot(t, y, 'blue',lw=1.5) 
    ax[0].plot(t, Xb, 'red',lw=1.5)
    ax[0].set_title("CO2 Flux Over Time")
    ax[0].set_xlabel("Time (Year)")
    ax[0].set_ylabel("CO2 Flux")
    ax[0].legend(['Actual', 'Predicted'])
    ax[0].text(2000, 15, f'r = {r}', fontsize=12, color='blue')
    
    colors = ['blue', 'red', 'green', 'orange', 'grey', 'black']
    
    for i in range(4):
        ax[1].plot(t, correlation_matrix[:,i], c = colors[i], lw=1.5)
    ax[1].legend(['Intercept', 'Net Radiation', 'Air Temperature', 'Water Vapor', 'Wind Speed'])
    ax[1].set_title('Coefficents Contributions')
    ax[1].set_xlabel('Time')
    ax[1].set_ylabel('Coefficents Contributions v.s Time')
    
    # Display the plot
    plt.tight_layout()
    # plt.show()
    
    # Return the regression coefficients 
    return b_matrix, Xb


# #----------------------------#
# # FUNCTION: averagecarbon    #
# #----------------------------#

def averagecarbon(hf, modelest):
    
    # PURPOSE: calculate the average carbon flux from the 
    # model for each year of the simulations. Create a time series plot
    # showing the carbon flux by year.
    
    # Calculate the average, modeled CO2 flux for each year
    start_year = int(np.min(hf[:,0]))
    end_year = int(np.max(hf[:,0]))
    
    t = hf[:,0]
    
    # Using dictionary to pool all values under same key(year)
    
    year_dict = {}
    
    for i in range(start_year, end_year + 1):
        year_dict[i] = []
        if i not in t: # For years without any data
            year_dict[i] = np.nan
        else:
            day_indicies = np.where(t == i) #Find indicies of year matching i
            for k in day_indicies:
                year_dict[i].append(modelest[k])
        
    flux_year_avgs = []
    years = []
        
    for y in year_dict.keys():
        if isinstance(year_dict[y], float): # Check if np.nan is the value
            flux_year_avgs.append(np.nan)
        else:
            avg = np.round(sum(year_dict[y][0]) / len(year_dict[y][0]), decimals=3) #Find average of values for each year
        
            flux_year_avgs.append(avg)
        years.append(y)
        
        
    
        
        
    
    # Create a plot of points showing the average modeled CO2 flux for each year
    
    plt.figure()
    plt.plot(years, flux_year_avgs, 'bo')
    plt.title("Average CO2 Flux Every Year")
    plt.xlabel("Time (Year)")
    plt.ylabel("CO2 Flux")
    plt.hlines(0,years[0], years[-1])
    
    # Display the plot
    # plt.show()
    
    # Return the result
    return flux_year_avgs
    
#-----------------------------------------#
# Execute the functions defined above     #
#-----------------------------------------#

if __name__ == "__main__": 
    filename               = 'harvard_forest.csv'
    hf                     = readdata(filename)

    
    # ndata,hfmean,hf25,hf75 = summarizedata(hf)
    # missing_data           = missingdata(hf)
    month_means            = seasonalcycle(hf)
    # betas, modelest        = HFregression(hf)
    # averagecarbon(hf,modelest)

#-----------------------------------------------------------------------------------------------#
# END OF SCRIPT
#-----------------------------------------------------------------------------------------------#
