# Should you Buy or Lease your Next Car?

## Project Goal

The goal of this project is to determine whether car leases are a good deal by comparing the total expense of a lease with the depreciation cost of a car. If the lease is more expensive we can conclude that it is more cost effective to buy the car new and resell it. However, if the lease is less expensive than we conclude you should lease instead of buy. 

By using Machine Learning we predict the price of cars and use it to calculate the depreciation cost with which we compare to the cost of its lease. 

The metric we use is Root-Mean-Squared-Error (RMSE) because it gives an idea of how much error the system typically makes in its predictions, with a higher weight for large errors.

## The Data

Instead of collecting data on hundreds of different cars we only collect data on one of the best rated cars to lease, the Acura TLX. This helps us simplify the problem and if we conclude that you should buy instead of lease this car, we can conclude the same for lower rated cars.

In this project we collect our data using BeautifulSoup's library. We webscrape Acura TLX car listings off of Truecar.com. The notebook complete with code used for webscraping can be found [here](https://github.com/lukenew2/car-leases/blob/master/collect_data_webscraping.ipynb). 

Here is the list of column names, their data type, and a short description that were used in the project:

| Column Name | Type | Description | 
| --- | --- | --- |
| Year | Numerical | Year made |
| Price | Numerical | Price of car (target variable) |
| Mileage | Numerical | Amount of miles the car has been driven |
| Drive | Categorical | Type of drive (either "FWD" or "SH-AWD") |
| Engine | Categorical | Type of engine (either "2.4L Inline-4" or "3.5L V-6" |
| Trim | Categorical | Contains info on performance package |
| Location | Categorical | Where the car is listed for sale |
| Accidents | Numerical | Amount of accidents on car's title |

To check for correlation between attributes we use pandas scatter_matrix() function, which plots every numerical attribute against every other numerical attribute.

<p align="center"> 
<img src="images/scatter_matrix_plot.png" width="600" height="400"/>
</p>

## Results

Notebook complete with code can be found [here](https://github.com/lukenew2/car-leases/blob/master/buy_or_lease.ipynb).

Our first base model is a Linear Regression with which we will try to improve from.  I was able to iterate on top of that and improve performance by a small margin using Polynomial Regression.  However, two models performed significantly better than the linear models, Random Forest Regressor and Gradient Boosting Regressor.  I performed grid searches on both to optimize the hyperparameters and was able to boost performance even more by creating an ensemble of the two best models averaging the predictions.  

The figure below shows the 4 best model's performance score (RMSE) over 10 different folds on the training set.  Using boxplots we can easily see the mean, interquartile range, and min/max scores across all folds. 

<p align="center"> 
<img src="images/best_models_box_plot_scores.png" width="600" height="450"/>
</p>

To analyze errors of best model we plot our predicted price against the actual price. If all of our points were on the diagonal line that would mean our model is perfect and has an error of 0. 

<p align="center"> 
<img src="images/actual_vs_predicted_price.png" width="600" height="450"/>
</p>

This looks pretty good our errors are normally distributed opposed to missing low for one region and high for another.  My model seemed to perform well for the entire range of values.  

## Conclusion

Now back to the original problem. Should you buy or lease your next car? 

Now that we have our final model and performance score on the test set we can use it to predict the prices of Acura TLXs with features corresponding to various leases. The leases we use for comparison are from Acura's website. Let's look at multiple different lease terms and see what we find out!

<p align="center"> 
<img align="center" src="images/depreciation_vs_cost_of_lease.png" width="1300" height="400"/>
</p>

The red line represents the predicted depreciation cost while the blue line represents the cost of the lease. The shaded area represents the 95% confidence intervals around our predicted depreciation. We see that in all three cases the lease is a lot more expensive.

You can save up to $10,000 if you choose to buy the car new. Leasing happens to be a lot more expensive even for one of the best rated cars.