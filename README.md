# Buy or Lease: Using Machine Learning to Predict Residual Price of Cars
## Revealing whether car leases are a good deal.

In this project I used machine learning to predict the residual price of a car given a specific lease agreement (three years and 10,000 miles per year). To simplify this project I chose to model the Acura TLX. It was rated in the top ten cars to lease in 2019 by Autotrader.com.

My data consisted of used 2016–2019 Acura TLX’s price along with their specs (year, mileage, transmission, engine, package, etc.), obtained from online car marketplaces such as Autotrader.com and Truecar.com. By utilizing linear regression I predict the residual price for a new Acura TLX after a three year and 30,000 mile lease.

Once I predict the residual price I subtracted it from the MSRP and calculated the depreciation. In this project we looked at the Standard Inline-4 FWD.

The lease I used for my analysis is from Acura’s website. You can find it [here](https://www.acura.com/tlx). By clicking on Full Description & Terms it lists the residual as the buyout price. We then compared our predicted residual with the lessor’s predicted residual.