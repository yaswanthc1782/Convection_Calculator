import openpyxl
def values(temp): 
# Open the spreadsheet
    workbook = openpyxl.load_workbook("POA.xlsx")
  
# Get the first sheet
    sheet = workbook.worksheets[0]
# Create a list to store the values
    head = []
# Iterate over the rows in the sheet
    a=[]
    temp1=0
    if(temp%50!=0):
        temp1=temp-temp%50
    for row in sheet:
    # Get the value of the first cell
    # in the row (the "Name" cell)
        name = row[0].value
    # Add the value to the list
        if(name==temp):
            for col in range(5):
                head.append(row[col].value)
            return head
        elif(name==temp1):
            for col in range(5):
                a.append(row[col].value)
        elif(name==temp1+50):
            b=[]
            for col in range(5):
                b.append(row[col].value)
            head.append(a)
            head.append(b)
            return(head)
# Print the list of names
    return(head)
