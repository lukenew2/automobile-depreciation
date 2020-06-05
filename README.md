# Buy or Lease: Predicting Residual Value of Cars

## Project Goal

In this project I aim to determine whether car leases are a good deal by comparing the depreciation cost of cars with the cost of a lease. Using machine learning I built a model that can predict the residual value of cars with which I use to predict the cost of buying a new car and reselling it X years later where X is the amount of years in the term of lease.

If the cost of lease is significantly greater than the predicted cost of buying and reselling a new car I can conclude that leases are not worth it.  However, if the cost of lease is less than the cost of buying and reselling a new car I can conclude that leases are in fact a good deal.

**Metric**: Root Mean Square Error (RMSE)

I used RMSE because it gives an idea of how much error the system typically makes in its predictions, with a higher weight for larger errors. This metric will help me determine whether the cost of lease is signifcantly greater than the cost of buying and reselling.  If the cost of lease is within the error of our prediction I cannot determine whether you should buy or lease.

## The Data

To simplify the project I gathered data on one specific make and model, the Acura TLX.  The Acura TLX is one of the best rated cars to lease because of its super low monthly payments.  It is the perfect example to model for this project and if I can conclude that it is better to buy and resell an Acura TLX than to lease I can conclude the same for lower rated cars (since they are worst deals).

The data was webscraped from Truecar.com, an online car marketplace that posts new and used car listings being sold across the United States. Code can be found in another notebook [here](https://github.com/lukenew2/car-leases/blob/master/collect_data_webscraping.ipynb). 

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

<img src="images/scatter_matrix_plot.png =50x50">

## Results

Notebook can be found [here](https://github.com/lukenew2/car-leases/blob/master/buy_or_lease.ipynb)

My modeling began with a simple Linear Regression as the base model.  I was able to iterate on top of that an improve performance by a small margin through using Polynomial Regression.  However, two models performed significantly better than the linear models.  Random Forest Regressor and Gradient Boosting Regressor.  I performed grid searches on both to optimize the hyperparameters and was able to boost performance even more through an ensemble of the two.  My final model was a Voting Regressor between Random Forest and Gradinet Boosting Regressors.

<img src="images/best_models_box_plot_scores.png =50x50">

To see how my models errors looked like I graphed predicted values vs actual values. If my model was perfect all points would lie on the diagonal.  My model seemed to perform well for the entire range of values.  

<img src="images/actual_vs_predicted_price.png =50x50">

## Conclusion

Here I plotted my final model's predicted depreciation cost of three different trims of the Acura TLX (in red) along with the cost of the respective lease (in blue).  The predicted depreciations have 95% confidence intervals shaded in around them.  As you can see it turns out leasing a car is a lot more expensive than buying and reselling a car in all three cases.  As always, thanks for viewing the project and I hope it was insightful and enjoyable!

<img src="images/depreciation_vs_cost_of_lease.png =50x50">
