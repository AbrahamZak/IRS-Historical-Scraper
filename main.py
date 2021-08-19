import sys
import json
import requests
import os
from bs4 import BeautifulSoup


# Taking a list of tax form names (ex: "Form W-2", "Form 1095-C"), this function returns the "Product Number",
# the "Title", and the maximum and minimum years the form is available for download from the
# IRS Prior Year Products page.
def tax_forms_data(forms):
    # Create a list for the result of each form we are searching for
    results = []
    # The base URL of prior year products
    irs_base_url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"
    for form in forms:
        # Initialize title, min_year, and max_year for this form
        title = ""
        min_year = sys.maxsize
        max_year = 0
        # index of current initial result
        idx = 0
        has_next = True
        while has_next:
            # Load the page using requests library and into beautiful soup
            page = requests.get(irs_base_url + f"?indexOfFirstRow={idx}&sortColumn=sortOrder&value={form}&criteria=formNumber&resultsPerPage=200&isDescending=false")
            soup = BeautifulSoup(page.content, "html.parser")
            # Find the table and get the rows
            table = soup.find('table', {"class": "picklist-dataTable"})
            rows = table.find_all('tr', {"class": ["even", "odd"]})
            # Iterate through each row
            for row in rows:
                # If Product Number on the row matches the product number searched, update variables for form if needed
                row_data = row.find_all("td")
                if row_data[0].get_text().lstrip().rstrip() == form:
                    year = int(row_data[2].get_text())
                    # If we don't have the title for this form yet, update the title (this is only done once)
                    if title == "":
                        title = row_data[1].get_text().lstrip().rstrip()
                    # If the year of the row is less than the current min_year, update min_year
                    if year < min_year:
                        min_year = year
                    # If the year of the row is greater than the current max_year, update max_year
                    if year > max_year:
                        max_year = year

            # Check if there exists a next page and if so, set its index for the next run, if not exit the loop
            next_page = soup.find('th', {"class": "NumPageViewed"})
            links = next_page.find_all('a')
            next_page = False
            for link in links:
                if link.contents[0] == "Next »":
                    idx += 200
                    next_page = True
                    break
            has_next = next_page

        # When loop is completed create a dict from the data and insert into the list
        form_result = {
            "form_number": form,
            "form_title": title,
            "min_year": min_year,
            "max_year": max_year
        }
        results.append(form_result)
    # Convert list of dicts to json and return
    return json.dumps(results)


# Taking a tax form name (ex: "Form W-2") and a range of years (inclusive, 2018-2020) downloads all PDFs available
# within that range. The downloaded PDFs are downloaded to a subdirectory under the
# script's main directory with the name of the form, and the file name will be the "Form
# Name - Year" (ex: Form W-2/Form W-2 - 2020.pdf)
def tax_forms_download(form, from_year, to_year):
    # The base URL of prior year products
    irs_base_url = "https://apps.irs.gov/app/picklist/list/priorFormPublication.html"
    # index of current initial result
    idx = 0
    has_next = True
    while has_next:
        # Load the page using requests library and into beautiful soup
        page = requests.get(irs_base_url + f"?indexOfFirstRow={idx}&sortColumn=sortOrder&value={form}&criteria=formNumber&resultsPerPage=200&isDescending=false")
        soup = BeautifulSoup(page.content, "html.parser")
        # Find the table and get the rows
        table = soup.find('table', {"class": "picklist-dataTable"})
        rows = table.find_all('tr', {"class": ["even", "odd"]})
        # Iterate through each row
        for row in rows:
            # If Product Number on the row matches the product number searched
            # and year is within range, download the form
            row_data = row.find_all("td")
            year = int(row_data[2].get_text())
            if row_data[0].get_text().lstrip().rstrip() == form and from_year <= year <= to_year:
                # Extract the pdf link
                pdf_link = row_data[0].find('a')
                # Establish the filename
                response = requests.get(pdf_link.get('href'))
                filename = form + "/" + form + " - " + str(year)
                # Create directory if it doesn't already exist
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                pdf = open(filename + ".pdf", 'wb')
                pdf.write(response.content)
                pdf.close()
        # Check if there exists a next page and if so, set its index for the next run, if not exit the loop
        next_page = soup.find('th', {"class": "NumPageViewed"})
        links = next_page.find_all('a')
        next_page = False
        for link in links:
            if link.contents[0] == "Next »":
                idx += 200
                next_page = True
                break
        has_next = next_page


# Test out our scripts
if __name__ == '__main__':
    print(tax_forms_data(["Form W-2", "Form 1095-C"]))
    tax_forms_download("Form W-2", 2018, 2020)

