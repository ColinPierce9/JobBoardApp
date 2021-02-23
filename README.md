# JobBoardApp
Application was built with Python and Django framework to find and post all recent Chemical Engineering job listings. The app was built to help engineers of all experience levels search andapply to relevant jobs. The job sites included in the search are Linkedin, Indeed, and Monster, and only conisders roles that are located within 50 miles from Phildelphia. Note: changing the search terms to any job title or location would require little alteration of the code. 

# Process
- Application is initiated upon visit using the Django views.py file
- Job sites are scraped with Requests and BeautifulSoup
- Date posted, title, company, and page link are collected from each site
- All postings are combined together, sorted by date posted, and cleaned for any duplicates
- Finished job data is sent to the home.html to be shown. Bootstrap css was used styling.

# Future Work
- If desired, a search input for role and location can be added to expand the users can search for any job they'd prefer. 
