databurndown
============

Little webapp to show my broadband data usage as a burndown graph against my quota for my ISP Andrews &amp; Arnold


Runs quite happily on a RPi, see the install packages script for what you need to add to stock Raspbian then just run the burndown.py script on nohup or something.

The crontab needs to be installed to update the data, there are 2 urls to call the /update fetches a new value from clueless which I currently do every 6hrs and the /newmonth needs to be run on the 1st of each month to create a new pkl file with a fresh quota, this newmonth should run before any updates are called.
Once installed and running call the /newmonth url first to create a blank graph and then call the /update to fetch from clueless, you might not see much until there are 2 days worth of points to plot, you can also manually edit the data to put in your previous days totals if you can work that out! I'll do an update script later....

This hasn't been tested much and I've only got 5 days usage in my graph so it might all break! 

I should be taking care of the length of the month in newmonth, don't ask me what happens when the clocks change I guess we'll see in a few weeks!
