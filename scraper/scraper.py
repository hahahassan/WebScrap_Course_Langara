# scraper.py
import pandas as pd
from bs4 import BeautifulSoup

def scrape_html_to_xlsx(html_file_path, csv_file_path):
    # Load the HTML content from the uploaded file
    with open(html_file_path, 'r') as file:
        html_content = file.read()

    # Parse the HTML content using Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize a list to hold all course information
    all_courses = []

    # Find all program names
    programs = soup.find_all(['td'], class_='deheader')
    program_names = []
    for program in programs:
        program_name = program.find('span', class_='LargerText').text.strip()
        program_names.append(program_name)

    # get column names
    column_names_tags = soup.find('tr', bgcolor="#FFFFCC").find_all('b')
    column_names = [tag.get_text(strip=True) for tag in column_names_tags]

    # Step 1: Split the HTML by Programs
    program_blocks = soup.find_all('td', class_='deheader')

    # Prepare a list to hold all courses across programs
    all_courses = []
    expected_details_length = 19  # Set this to the expected number of <td> elements in informative rows

    for program_block in program_blocks:
        program_name = program_block.find('span', class_='LargerText').get_text(strip=True)
        program_row = program_block.find_parent('tr')
        next_sib = program_row.find_next_sibling('tr')

        while next_sib and not next_sib.find('td', class_='deheader'):
            course_code_tag = next_sib.find('td', colspan="19", class_='dedefault')
            if course_code_tag:
                course_code = course_code_tag.get_text(strip=True)
                next_sib = next_sib.find_next_sibling('tr')

            while next_sib and not next_sib.find('td', colspan="19", class_='dedefault') and not next_sib.find('td', class_='deheader'):
                details = [td.get_text(strip=True) for td in next_sib.select('td.dedefault, td.dedead')]
                
                # Only process rows where the length of details matches the expected length
                if len(details) == expected_details_length:
                    course_details = {
                        'Program Name': program_name,
                        'Course Code': course_code,
                        # Map the extracted details to the respective fields
                        'CRN': details[4],
                        'Subject': details[5],
                        'Course Number': details[6],
                        'Section': details[7],
                        'Title': details[9],
                        'Type': details[12],
                        'Day(s)': details[13],
                        'Time': details[14],
                        'Room': details[17],
                        'Instructor(s)': details[18]
                    }
                    all_courses.append(course_details)

                next_sib = next_sib.find_next_sibling('tr')

    # convert dict_info to dataframe, and to_excel
    df = pd.DataFrame(all_courses)
    df.replace('', pd.NA, inplace=True)
    df = df.fillna(method='ffill')
    df.to_csv(csv_file_path)