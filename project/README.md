# Conflicts' locations and their information proliferation

# Abstract
For our project we decided to make use of both UCDP (complemented with GDELT) and Twitter datasets. From these, we would like to figure out any existing biases in the information proliferation around the globe, regarding the conflicts' locations. In other words, we are interested in comparing the reach of information on conflicts depending on the place where said conflicts take place.

As for our story, we believe it would be interesting to shed some light on world-wide situations to which the general public might be oblivious to. Bear in mind, our purpose is not to figure out *why* these biases may exist (e.g. political or media influences) but *where* they exist.

Because the world might be focusing on some regions more than others, this unequally raises social concern and may impact social causes' resourcefulness. Although we do not believe we can fix the latter problem in this project, we do think this information would be empowering for people for better decision-making and awareness.

# Research questions
The following are the research questions that we would like to address:

1. **Region-specific conflicts**
 * Which conflicts take place in each region
2. **Region-specific Twitter text content**
 * Find Tweets related with conflicts and identify the region they are referring to.
3. **Check for generalized, globally existing biases**
 * Is the information proliferation different depending on where the conflicts take place? If so, do these biases change or evolve over time?

# Dataset
The following are the three datasets that we would like to use:

1. UCDP

 * Get date and location for conflicts around the world
 * Do a region-based aggregation (to reduce the amount of data to handle)

2. GDELT (v2.0) - 2.5Tb (GKG)

 * Get published articles' by theme, identifying the ones related to *conflicts*
 * Find the regions the articles focus on
 * Do a region-based aggregation of the articles (to reduce the amount of data to handle) based on the conflicts' locations

3. Twitter

 * Get Tweets by theme, identifying the ones related to *conflicts*
 * Find the regions they focus on
 * Do a region-based aggregation  of the tweets (to reduce the amount of data to handle) based on the conflicts' locations

After we get all the above information from the target datasets, we will use the region-based aggregations for carrying out the statistical analysis.

To note that both GDELT and Twitter datasets are pretty big - which would put a huge toll on in-memory operations. Thankfully, we can make use the cluster (mentioned in class) to handle the Twitter one but we will simply try to trim down the amount of data we work with on GDELT - the first time we read the data may still take a long time but, afterwards, serialization should allow us to speed up the process.

# List of internal milestones up until project milestone 2

1. Get raw data for all the datasets and handle missing (or incomplete) information
2. Get GDELT and Twitter data organized by theme
3. Get GDELT and Twitter data's region of focus
4. Prune unnecessary data from all datasets
5. For each dataset, organize data by region
6. Do exploratory analysis based on region equality

# Questions for TAs
1. Does the Twitter dataset contain dates? This would be useful for us to see bias evolution (over time).
2. Can we use GDELT 2.0? Or the one that is provided is GDELT 1.0?
