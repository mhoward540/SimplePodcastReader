# SimplePodcastReader
A Simple Command Line UI for fetching and listening to podcasts.  Uses Python 2.7 with no external dependencies.

# How to use it
Paste the URL to the Podcast XML feed when prompted.  After validation, the link will be added to a list of saved feeds (feeds.txt).  You can then go page by page to find the episode you would like to listen to (or jump to pages by typing, for example, j10, to jump to page 10). The progam will then download the episode (if it is not already downloaded), and play the file using the PC's default action.

# Issues & Concerns
-Only handles mp3 files at this point.
-Media is downloaded all in the same folder, which means that there may be name conflicts between files.

# Future Feature Plans
-Mark which episodes are already downloaded

#Other Comments
I wrote this program simply because I couldn't find any browser-based PodCatchers, so I figured a simple desktop version would be almost as useful. This program isn't exactly the most robust, but it seems like it can handle most of what you throw at it. 
