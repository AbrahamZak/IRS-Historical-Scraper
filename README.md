# IRS-Historical-Scraper
Python version used: 3.9

## Original Problem Description
Taking a list of tax form names (ex: "Form W-2", "Form 1095-C"), search the website and return some informational results. Specifically, you must return the "Product Number", the "Title", and the maximum and minimum years the form is available for download. The forms returned should be an exact match for the input (ex: "Form W-2" should not return "Form W-2 P", etc.) The results should be returned as json, in the format of the following example:
```
[
	{
		"form_number": "Form W-2", 
		"form_title": "Wage and Tax Statement (Info Copy Only)", 
		"min_year": 1954, 
		"max_year": 2021
	}, 
	...
]
```

Taking a tax form name (ex: "Form W-2") and a range of years (inclusive, 2018-2020 should fetch three years), download all PDFs available within that range. The forms returned should be an exact match for the input (ex: "Form W-2" should not return "Form W-2 P", etc.) The downloaded PDFs should be downloaded to a subdirectory under your script's main directory with the name of the form, and the file name should be the "Form Name - Year" (ex: Form W-2/Form W-2 - 2020.pdf)

## Dependencies Used
sys - Used for maxsize variable to establish min_year

requests - Used to establish HTTP requests to load webpages and pdf data for both functions

BeautifulSoup - Used to find elements from the HTTP requests

json - Used to convert the list of dictionaries created in tax_forms_data to JSON

os - Used to create the directory for the pdf downloads if it does not currently exist

## How to run:

tax_forms_data method takes in 1 parameter which is a list of form names

This is tested in main method (print(tax_forms_data(["Form W-2", "Form 1095-C"])))

The method returns JSON, which is printed in our test case to the console


tax_forms_download method takes in 3 parameters which is the form name, from year, and to year

This is tested in main method (tax_forms_download("Form W-2", 2018, 2020))

The method will download the "Form W-2" pdfs to the directory where the script is running (in the correctly titled directory with the correctly given filenames)

Both functions are located in main.py

