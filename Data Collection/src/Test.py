# Test.py
# Author: Yasin Holzenkämpfer
# Last Modified: 15.12.2025
#
# Description: This module tests the CloudSheetService and TimeService modules.

# The following code will add a line to a csv. If the csv does not exist yet it will create it.
from CloudSheetService import *
from TimeService import *

peoples = ["First Name", "Second Name", "Age", "Date", "Time"]

for i in range(5):
    first_name = f"FirstName{i}"
    second_name = f"SecondName{i}"
    age = str(20 + i)
    date = get_current_date()
    time = get_current_time()
    person = [first_name, second_name, age, date, time]
    peoples.append(person)

sheet_name = "TestSheet-" + get_current_date()
sheet_id = find_sheet_id_by_name(sheet_name)
if not sheet_id:
    sheet_id = create_new_google_sheet(sheet_name)

set_csv_data(sheet_id, peoples)