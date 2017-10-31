# Title

# Abstract
A 150 word description of the project idea, goals, dataset used. What story you would like to tell and why? What's the motivation behind your project?

For our project we decided to make use of both UCDP (complemented with GDELT) and Twitter datasets. From these, we would like to figure out any existing biases in the information proliferation around the globe, regarding the conflicts' locations.

As for our story, we thought it would be interesting to shed some light on world-wide situations to which the general public might be oblivious to. Bear in mind, our purpose is not to figure out *why* these biases may exist (e.g. political or media influences) but *where* they exist.

Because the world might be focusing on some regions more than others, this unequally raises social concern and may impact social causes' resourcefulness. Although we do not believe we can fix the latter problem in this project, we do think this information would be empowering for people, for better decision-making and awareness.

# Research questions
A list of research questions you would like to address during the project. 

1. Country-specific conflicts
2. Country-specific Twitter text content
3. Check for generalized, globally existing biases

# Dataset
List the dataset(s) you want to use, and some ideas on how do you expect to get, manage, process and enrich it/them. Show us you've read the docs and some examples, and you've a clear idea on what to expect. Discuss data size and format if relevant.

1. UCDP

 * Get date and location for conflicts around the world
 * Do a region-based aggregation (to reduce the amount of data to handle)

2. GDELT (v2.0)

 * Get published articles' by theme - related to conflict
 * Find the regions they focus on
 * Do a region-based aggregation (to reduce the amount of data to handle)

3. Twitter

 * Get Tweets by theme - related to conflict
 * Find the regions they focus on
 * Do a region-based aggregation (to reduce the amount of data to handle)

After we get all the above information from the target datasets, we just use the region-based aggregations for statistical analysis.

# A list of internal milestones up until project milestone 2

1. Get raw data for all the datasets and handle missing (or incomplete) information
2. Get GDELT and Twitter data organized by theme
3. Get GDELT and Twitter data's region of focus
4. Prune unnecessary data from all datasets
5. For each dataset, organize data by region
6. Do exploratory analysis based on region equality

# Questions for TAs
Add here some questions you have for us, in general or project-specific.

1. Does the Twitter dataset contain dates?
