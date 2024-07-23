import pandas as pd
import matplotlib.pyplot as plt

# Define the initial values and increments
initial_income = 20  # in lakhs
annual_income_increment_rate = 0.10  # 10%
job_change_increment_rate = 0.25  # 25% every 3 years
reduced_job_change_increment_rate = 0.15  # 15% after reaching 50 lakhs
reduced_annual_income_increment_rate = 0.05  # 5% after reaching 50 lakhs
initial_expenditure = 4  # in lakhs
pre_marriage_expenditure_increment_rate = 0.15  # 15%
post_marriage_expenditure_increment_rate = 0.30  # 30%
baby_expenditure_increment_rate = 0.50  # 50% for the first 4 years after baby expenditure
constant_expenditure_threshold = 35  # in lakhs
constant_expenditure_value = 35  # in lakhs
equity_return_rate = 0.15  # 15%
fd_return_rate = 0.07  # 7%
initial_capital = 20  # in lakhs
current_age = 26  # initial age
future_age = 40  # future age
sudden_marriage_age = 29  # age when sudden expenditure for marriage occurs
sudden_marriage_amount = 20  # in lakhs
sudden_baby_age = 33  # age when sudden expenditure for baby occurs
sudden_baby_amount = 10  # in lakhs
baby_years = 4  # number of years with increased expenditure rate after baby expenditure

# Calculate the number of years based on the age difference
years = future_age - current_age

# Initialize variables to track total savings and the initial values
total_savings = initial_capital  # start with initial capital
current_income = initial_income
current_expenditure = initial_expenditure
expenditure_increment_rate = pre_marriage_expenditure_increment_rate

# Lists to store data for the table and graph
year_list = [0]
age_list = [current_age]
income_list = [initial_income]
post_tax_income_list = [initial_income * 0.70]
expenditure_list = [initial_expenditure]
savings_list = [initial_income * 0.70 - initial_expenditure]
total_savings_list = [total_savings]
annotation_years = []  # To store the years of sudden expenditures

# Iterate over each year to calculate the savings and total net worth
for year in range(1, years + 1):
    age = current_age + year
    
    # Apply 30% tax to the current income
    income_after_tax = current_income * 0.70
    
    # Calculate the savings for the current year
    savings = income_after_tax - current_expenditure
    
    # Apply the sudden expenditure for marriage if it's the specified year
    if age == sudden_marriage_age:
        savings -= sudden_marriage_amount  # Deduct the marriage expenditure from savings
        annotation_years.append(year)  # Store the year for annotation
    
    # Apply the sudden expenditure for baby if it's the specified year
    if age == sudden_baby_age:
        savings -= sudden_baby_amount  # Deduct the baby expenditure from savings
        annotation_years.append(year)  # Store the year for annotation
        
        # Update expenditure increment rate for the next few years after baby expenditure
        expenditure_increment_rate = baby_expenditure_increment_rate
    
    # Revert expenditure increment rate to post-marriage rate after specified baby years
    if age >= sudden_baby_age + baby_years:
        expenditure_increment_rate = post_marriage_expenditure_increment_rate

    # Check if expenditure exceeds threshold and set to constant value if true
    if current_expenditure >= constant_expenditure_threshold:
        current_expenditure = constant_expenditure_value

    # Add the savings to the total savings and apply the interest
    equity_investment = total_savings * 0.75  # 75% in equity
    fd_investment = total_savings * 0.25  # 25% in FD
    
    equity_return = equity_investment * equity_return_rate
    fd_return = fd_investment * fd_return_rate
    
    total_savings = total_savings + savings + equity_return + fd_return
    
    # Store the values in the lists
    year_list.append(year)
    age_list.append(age)
    income_list.append(current_income)
    post_tax_income_list.append(income_after_tax)
    expenditure_list.append(current_expenditure)
    savings_list.append(savings)
    total_savings_list.append(total_savings)
    
    # Update income and expenditure for the next year
    if current_income < 50:
        if year % 3 == 0:
            current_income *= (1 + job_change_increment_rate)
        else:
            current_income *= (1 + annual_income_increment_rate)
    else:
        if current_income < 100:  # Check if income is less than 100 lakhs
            if year % 3 == 0:
                current_income *= (1 + reduced_job_change_increment_rate)
            else:
                current_income *= (1 + reduced_annual_income_increment_rate)
        else:
            if year % 3 == 0:
                current_income *= (1 + reduced_job_change_increment_rate)
            else:
                current_income *= (1 + 0.01)  # Set increment to 1% after reaching 100 lakhs
    
    current_expenditure *= (1 + expenditure_increment_rate)

# Create a DataFrame to display the data in a table
data = {
    'Year': year_list,
    'Age': age_list,
    'Income (lakhs)': income_list,
    'Post-tax Income (lakhs)': post_tax_income_list,
    'Expenditure (lakhs)': expenditure_list,
    'Savings (lakhs)': savings_list,
    'Total Savings (lakhs)': total_savings_list
}
df = pd.DataFrame(data)

# Display the DataFrame as a table
with pd.option_context('display.float_format', '{:.2f}'.format):
    print(df.to_string(index=False))

# Plot the income, expenditure, and total savings over the years
plt.figure(figsize=(12, 6))

plt.plot(df['Year'], df['Income (lakhs)'], label='Income (lakhs)', marker='o', color='darkblue', linewidth=2.5)
plt.plot(df['Year'], df['Post-tax Income (lakhs)'], label='Post-tax Income (lakhs)', marker='o', color='skyblue', linewidth=2.5)
plt.plot(df['Year'], df['Expenditure (lakhs)'], label='Expenditure (lakhs)', marker='o', color='darkred', linewidth=2.5)
plt.plot(df['Year'], df['Total Savings (lakhs)'], label='Total Savings (lakhs)', marker='o', color='darkgreen', linewidth=2.5)

# Highlight the sudden expenditures on the graph
for year in annotation_years:
    plt.scatter(year, df.loc[df['Year'] == year, 'Expenditure (lakhs)'], color='red', s=200, label='Sudden Expenditure')

plt.xlabel('Year')
plt.ylabel('Amount (lakhs)')
plt.title('Financial Growth Over Years')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(year_list)  # Ensure all years are shown on the x-axis
plt.tight_layout()  # Adjust layout to fit all elements
plt.show()
