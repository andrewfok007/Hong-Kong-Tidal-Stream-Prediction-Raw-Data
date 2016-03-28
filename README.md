# Hong-Kong-Tidal-Stream-Prediction-Raw-Data

Here is a brief description of the project,

- Django was the framework used.
- Celery and rabbitmq for asynchronous work, it is used to retrieve csv data from the tidal stream prediction site periodically. (Currently set to 4am daily, which avoids the maintenance period)
- The "tidal" directory contains the main settings, celery settings, url handlers and wsgi
- The "hydo" directory contains database model, custom utilities, celery tasks, testings and views
- The sqlite3 database contains sample data for 2016-03-16, so you can run "python manage.py runserver", visit "http://localhost:8000/hydro/" and select 2016-03-16 to 2016-03-17 in date range to display the data
- By scrolling to the bottom of the page, or changing to a different time period, it makes an ajax get call to retrieve updated json data.
- I have capped the json data to 15 minutes interval (1172 row entries in every 15 minutes) This stops users requesting large amount of data at a time.
- Front-end wise, I used D3.js to do graph plotting.
- With my background is mechanical engineering, I thought it would be interesting to estimate and display the kW energy generation if a tidal generator was installed in area (lat 22.16 long 114.48), feel free to change turbine power coefficient, sea water density and radius of the turbine blade to see the energy generation changes. (In reality, there should also a time delay in tidal flow and energy generation, I have ignored it here for simplicity.)

Future work:
- Display tidal flow on map, using https://developers.google.com/maps/documentation/javascript/examples/overlay-symbol-arrow
- More research on how these tidal data could be useful for other people e.g. fishermen might want to know the speed of current flow to decide fishing time, or civil engineers calculating potential soil erosion rate from sea bed when installing bridges or tunnels. - - With more domain knowledge, I can then present the data in a meaning way.
- Explore various plotting techniques with D3.js, would like to challenge myself with something like this  http://charts.animateddata.co.uk/uktemperaturelines/ 
- Adding a feedback/complain form if users have any problems or improvement suggestions
- Use selenium webdriver to test the frond end. Most of my current testings are backend related.
- Use some sort of tools to test server loading (need to do some learning first)
- Not sure if pandas is the most efficient way to handling the csv data, will also try numpy
- Custom 404 page
