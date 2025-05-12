import pandas as pd


def extract(file_path):
    extracted_data = pd.read_csv(file_path)
    return extracted_data


def transform(extracted_data):
    # remove row ID column
    extracted_data.drop(["Row ID"], axis=1, inplace=True)

    # change order date and ship date columns to YYYY-MM-DD
    extracted_data["Order Date"] = pd.to_datetime(extracted_data["Order Date"], dayfirst=True)
    extracted_data["Ship Date"] = pd.to_datetime(extracted_data["Ship Date"], dayfirst=True)

    # round sales and profit columns to two decimal places
    extracted_data["Sales"] = extracted_data["Sales"].round(2)
    extracted_data["Profit"] = extracted_data["Profit"].round(2)
    # create dict to store csvs for Power BI
    tables = {}

    # dataframe for the fact table (orders table)
    fact_orders = extracted_data.loc[:, ["Order ID", "Order Date", "Ship Date", "Ship Mode", "Customer ID", "Product ID", "Sales", "Quantity", "Discount", "Profit"]].copy()
    tables["fact_orders"] = fact_orders

    # dataframe for customer dimension table
    dim_customer = extracted_data.loc[:, ["Customer ID", "Customer Name", "Segment", "Country", "City", "State", "Postal Code", "Region"]].copy()
    tables["dim_customer"] = dim_customer

    # dataframe for product dimension table
    dim_product = extracted_data.loc[:, ["Product ID", "Category", "Sub-Category", "Product Name"]].copy()
    tables["dim_product"] = dim_product

    return tables


def load(transformed_data):
    # create FactOrder csv file
    transformed_data["fact_orders"].to_csv("FactOrder", index=False)

    # create DimCustomer csv file
    transformed_data["dim_customer"].to_csv("DimCustomer", index=False)

    # create DimProduct csv file
    transformed_data["dim_product"].to_csv("DimProduct", index=False)


if __name__ == "__main__":
    extracted_data = extract("Superstore.csv")
    print(extracted_data)
    transformed_data = transform(extracted_data)
    load(transformed_data)
