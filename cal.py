import numpy as np
import pandas as pd
import io

def calculation(unit, cogs_unit, gross_revenue, discount_sign_min, discount_sign_max, discount_promotion_min, discount_promotion_max, ams_state):
    unit = int(unit)
    cogs_unit = int(cogs_unit)
    gross_revenue = int(gross_revenue)
    discount_sign_min = int(discount_sign_min)
    discount_sign_max = int(discount_sign_max)
    discount_promotion_min = int(discount_promotion_min)
    discount_promotion_max = int(discount_promotion_max)
    ams_state = ams_state
    # Outputs Dictionary
    Output = {
        'Discount Sign': [],
        'Discount Promotion': [],
        'Initial Sale': [],
        'Gross Revenue': [],
        'Net Income': [],
        'Net Income(%)': [],
        'Tax Diff': [],
        'Selling Expenses': [],
        'Possible Income': []
    }
    
    # Constants (these values are percentages in decimal form)
    Ams_commission_percent = 0.0749
    Normal_commission_percent = 0.0535
    Service_commission_percent = 0.0535
    Transaction_commission_percent = 0.0321
    # Function to calculate net income
    def calculate_net_income_unit(cogs_unit, gross_revenue, discount_sign, discount_promotion, ams_state):
        # change to %
        discount_sign = discount_sign/100
        discount_promotion = discount_promotion/100

        # Calculate gross profit
        # gross_revenue = (init_sales) * (1-discount_sign)
        init_sales = gross_revenue / (1 - discount_sign)
        init_sales =int(init_sales)

        # Tax difference
        tax_diff = 0.07 * (gross_revenue - cogs_unit)

        if ams_state == True:
            # Affliate commission
            Ams_commission = Ams_commission_percent * gross_revenue
        else:
            Ams_commission = 0

        # Selling expense
        selling_expense = Ams_commission + ((Normal_commission_percent + Service_commission_percent) * gross_revenue) + ((Transaction_commission_percent) * (gross_revenue) * (1-discount_promotion) ) 
        
        # Net income
        net_income = (gross_revenue - cogs_unit) - tax_diff - selling_expense - (discount_promotion * gross_revenue)
        # print(f'sale: {init_sales} tun: {cogs_unit * unit}  gross:{gross_profit} net_income: {net_income} exp: {selling_expense} discount_promotion: {discount_promotion} tax_diff: {tax_diff}')

        return init_sales, net_income, tax_diff, selling_expense

    # Define ranges for discount sign and discount promotion
    discount_sign_step = (discount_sign_max - discount_sign_min) / 4
    discount_promotion_step = (discount_promotion_max - discount_promotion_min) / 4
    discount_sign_range = np.arange(discount_sign_min, (discount_sign_max + 1), discount_sign_step)
    discount_promotion_range =np.arange(discount_promotion_min, (discount_promotion_max + 1), discount_promotion_step)



    # Loop through the ranges and calculate for each combination
    for discount_sign in discount_sign_range:
        for discount_promotion in discount_promotion_range:
            init_sales, net_income, tax_diff, selling_expense = calculate_net_income_unit(cogs_unit, gross_revenue, discount_sign, discount_promotion, ams_state)
            net_income_percent = net_income/cogs_unit * 100
            possible_income = net_income * unit
            
            Output['Discount Sign'].append(int(discount_sign))
            Output['Discount Promotion'].append(int(discount_promotion))
            Output['Initial Sale'].append(int(init_sales))
            Output['Gross Revenue'].append(int(gross_revenue))
            Output['Net Income'].append(int(net_income))
            Output['Net Income(%)'].append(int(net_income_percent))
            Output['Tax Diff'].append(int(tax_diff))
            Output['Selling Expenses'].append(int(selling_expense))
            Output['Possible Income'].append(int(possible_income))
            # print(f'OFFER: Init Sales = {init_sales}, Gross Revenue = {gross_revenue}, Discount Sign: {discount_sign}%, Discount Promotion: {discount_promotion}%')
            # print(f'Details: net_income = {net_income}, net_income_% = {net_income/cogs_unit *100}%, possible_income = {possible_income}, tax_diff = {tax_diff}, selling_expense = {selling_expense}')
        
    # Create DataFrame
    df = pd.DataFrame(Output)

    return df
    
# Export DataFrame to CSV
def export_csv(df, full_path):
    df.to_csv(full_path, index=False)
    
    # Create a buffer to store CSV as a string in memory
    csv_buffer = io.StringIO()

    # Write the DataFrame to the buffer (no file saving here)
    df.to_csv(csv_buffer, index=False)

    # Get CSV data as a string from the buffer
    csv_data = csv_buffer.getvalue()
    return csv_data
    
# if __name__ == '__main__':
#     cogs_unit = 220
#     unit = 24
#     gross_revenue = 296
#     discount_sign_min = 10
#     discount_sign_max = 20
#     discount_promotion_min = 1
#     discount_promotion_max = 20
#     df = calculation(unit, cogs_unit, gross_revenue, discount_sign_min, discount_sign_max, discount_promotion_min, discount_promotion_max)
#     full_path = 'C:/Users/nack/Desktop/3rd_year/prompt eng/Buildmate ProfitCalculation/test.csv'
#     csv_data = export_csv(df, full_path)
#     print(csv_data)