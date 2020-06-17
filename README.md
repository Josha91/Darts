# Darts
In Darts, there is a lot of data to play with. In professional matches, the quality of a player is usually assessed by his 3-dart average, and the number of darts he needs on a double to finish a leg. 

For non-professionals, these statistics are a bit cumbersome, as it requires a lot of data registration. There are alternative ways of assessing the skill of a player. This is what is explored in this project. 

* EM.py -- here, I provide a Python implemenetation of the algorithm described by Tibshirani, Price, Taylor (https://www.stat.cmu.edu/~ryantibs/darts/, published in JRSS Series A, Vol. 174, No. 1, 213-226, 2011). This maximizes the likelihood for the (co)variance of a two dimensional Gaussian of dart locations with respect to the bullseye, given the dart *scores* as proxies. Remarkably, a relatively low number of scores (N~50, aiming at the bullseye) is enough to constrain a player's accuracy, under the Gaussian assumption, *without* the need to measure the position of the darts in the board. 

* This is because of the properties of the different scores on the board: many triples, prime-valued singles, and both the bull and the bullseye are unique. In fact, even registering the number of bull and bullseye as a fraction of the total throws gives a reasonably accurate constraint on sigma, as I show by maximizing the likelihood of sigma given the fraction (through a Bernouilli distribution). 

* A heatmap of E(X) where X is the expected 1-dart score, plus the optimal location to aim for (given the skill level calculated above), can be calculated using plot_heatmap.py. This is a convolutioin of the score grid with the accuracy-Gaussian, and is again a Python implementation of the work by Tibshirani, Price and Taylor (2011). 
