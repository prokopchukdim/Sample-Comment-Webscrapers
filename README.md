# Summary
This repository is a set of web scrapers that I created in late 2019 / early 2020 as part of a discontinued research paper aiming to find language patterns in propaganda commentary on government-owned or funded Serbian political news sources. The original idea for my co-writers and I was to manually label a substantial set of scraped comments from political articles and use a mix of computational linguistics and machine learning to find patterns in propaganda language. I individually created these scrapers, which collected 100,000+ comments, as well as a very rudimentary labeling tool using pygame for the UI (not currently included in the repository). Note: as of the original creation of these scrapers, all websites scraped allowed bots in their respective robots.txt directories.

Feel free to view my code, (which is largely undocumented), to get ideas for how to scrape similar style news websites. All 3 scrapers use an approach individualised to each website.

# Requirements To Run
These scrapers require an installation of the following Python libraries:
bs4, requests, selenium, and chromedriver

I cannot guarantee that any of these scrapers still work! While they worked in 2019, any small update to the structure of these websites can render such scrapers disfunctional. 
