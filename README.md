# Darts
Very simple darts application, to play around with tkinter. 
Besides standard Python packages, `astropy`, `pandas`, `functools`, `emcee` and `colormath` are required. 

To be done:
1. Bot is not yet fully functional
1. Output of skill-level doesn't work as expected
1. Add 'simple game' functionality. 
1. Testing. 

The app can be run from the command line with `python main.py`

With this application, there are a couple of things you can do:
1. Play a game (against another person or a bot) (where you can specify some of the game parameters; defaults to a standard 3-leg, 501 + double finish game). 
1. Simply registering consecutive throws, returning some statistics.
1. Calculate your skill level and determine your ideal aiming location. (see below)

![Game screen](https://github.com/Josha91/Darts/blob/master/images/Game_screen.png)

![Skill variations](https://github.com/Josha91/Darts/blob/master/images/Skills.png)


In Darts, there is a lot of data to play with. In professional matches, the quality of a player is usually assessed by his 3-dart average, and the number of darts he needs on a double to finish a leg. For non-professionals, these statistics are a bit cumbersome, as it requires a lot of data registration. There are alternative ways of assessing the skill of a player.

* For the skill determination, I provide a Python implemenetation of the algorithm described by Tibshirani, Price, Taylor (https://www.stat.cmu.edu/~ryantibs/darts/, published in JRSS Series A, Vol. 174, No. 1, 213-226, 2011). This maximizes the likelihood for the (co)variance of a two dimensional Gaussian of dart locations with respect to the bullseye, given the dart *scores* as proxies. Remarkably, a relatively low number of scores (N~50, aiming at the bullseye) is enough to constrain a player's accuracy, under the Gaussian assumption, *without* the need to measure the position of the darts in the board. 

* This is because of the properties of the different scores on the board: many triples, prime-valued singles, and both the bull and the bullseye are unique. In fact, even registering the number of bull and bullseye as a fraction of the total throws gives a reasonably accurate constraint on sigma, as I show by maximizing the likelihood of sigma given the fraction (through a Bernouilli distribution). 

* A heatmap of E(X) where X is the expected 1-dart score, plus the optimal location to aim for (given the skill level calculated above), can be calculated using plot_heatmap.py. This is a convolutioin of the score grid with the accuracy-Gaussian, and is again a Python implementation of the work by Tibshirani, Price and Taylor (2011). 
