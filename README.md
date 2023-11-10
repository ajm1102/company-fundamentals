# company-fundamentals
Next js frontend allows the input of stock ticker which once entered will make a request to the backend. The flask backend then uses pandas to extract from a set of tables all the xbrl finiancial metrics used in the SEC fillings. To acces the data the download button needs to be pressed. This will extract around 130gb of tables from SEC website.

The entire dataset can show metrics such as assets and earnings per share since 2009. One metric can be chosen from a listbox to display the values in a table and graph. A button is implement to then download the table in a CSV format.

To start the the app use npm run dev in the client and the start the server.py file with python.

