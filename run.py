# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

def get_sales_data():
    '''
    Get sales figures input from the user
    '''
    while True:
        print("Please enter sales data from the last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 20, 30, 45, 50, 22, 10\n")

        data_str = input("Please enter your data here:  ")
  
        sales_data = data_str.split(",")
        #called up here, don't ask me why!
        
        if validate_data(sales_data):
            print("Data is valid")
            break
    return(sales_data)

def validate_data(values):
    '''
    Inside the try, converts all string values into integers.
    Raises vlaue error is strings cannot be converted into integers,
    or if there aren't exactly 6 values
    '''
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)} "
            )

    except ValueError as e:
                print(f"Invalid data: {e}, please try again.\n")
                return False

    return True

def update_sales_worksheet(data):
    '''
    update sales w/sheet, add new row w the list data provided
    '''
    print("updating sales data...\n")
    #now need to access sales data from google worksheet
    sales_worksheet = SHEET.worksheet("sales")
    #This line v adds an additional row to the bottom of the google sheet
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully!\n")

def calculate_surplus_data(sales_data):
    '''
    Compare sales w stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    Positive surplus = waste
    Negative surplus = extra made when stock out
    '''
    print("Calculating surplus data")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
  
    surplus_data = []

    for stock, sales in zip(stock_row, sales_data):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def main():
    '''
    Run all program functions in python
    '''
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    


print("Welcome to Love Sandwiches data automation!\n")
main()
