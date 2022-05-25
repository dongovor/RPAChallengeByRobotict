import pandas as pd
import datetime

XL_INPUT = "Expenses.xlsx"
XL_OUTPUT = "Expenses_output.xlsx"


def get_data():
    '''
        Reads the data from the excel file
    '''
    data = pd.read_excel(XL_INPUT, header=None, index_col=None)
    data.columns = ["Description", "Date", "Amount"]
    return data


def sort_by_date(df: pd.DataFrame) -> pd.DataFrame:
    '''
        Sorts the dataframe by date/seconds column
    '''
    df = df.sort_values(by=['Date'], ascending=True)
    return df


def group_by_date(df: pd.DataFrame) -> pd.DataFrame:
    '''
        Groups the dataframe by date
    '''
    df['Date'] = pd.to_datetime(df['Date'])
    df_groups = df.groupby([df['Date'].dt.year, df['Date'].dt.month])
    return df_groups


def get_max_rows(df: pd.DataFrame) -> int:
    '''
        Returns the maximum number of rows in the dataframe
    '''
    idx_count_list = []
    for dataframe in df:
        idx_count_list.append(len(dataframe[1].index))

    return max(idx_count_list)


def add_total_amount(df_tuple: pd.DataFrame, idx: int) -> pd.DataFrame:
    '''
        Adds the total amount of the dataframe
    '''
    df_list = []
    for dataframe in df_tuple:
        df = dataframe[1]
        df.sort_index(inplace=True)
        row_value = [f'Total in {dataframe[0][1]}. month',
                     '',
                     df['Amount'].sum()]
        if len(df.index) < idx:
            df = add_empty_rows(df, idx - len(dataframe[1].index))
        df.loc[dataframe[1].index.max() + 1] = ['', '', '']
        df.loc[dataframe[1].index.max() + 2] = row_value
        df_list.append(df)
    return df_list


def add_empty_rows(df: pd.DataFrame, rows_to_add: int) -> pd.DataFrame:
    '''
        Adds empty rows to the dataframe
    '''
    for i in range(rows_to_add):
        df.loc[len(df)] = ['', '', '']
    return df


def write_to_excel(init_df: pd.DataFrame, df_list: pd.DataFrame) -> None:
    '''
        Writes the data to the excel file
    '''
    writer = pd.ExcelWriter(XL_OUTPUT, engine='xlsxwriter')
    init_df.to_excel(writer, sheet_name='Sheet1', index=False)
    column = 0
    for dataframe in df_list:
        dataframe.to_excel(writer, sheet_name="Sheet2",
                           startrow=0,
                           startcol=column,
                           index=False)
        column = column + len(dataframe.columns) + 1
    writer.save()


def main():
    data = get_data()
    sorted_df = sort_by_date(data)
    grouped_df = group_by_date(sorted_df)
    max_idx = get_max_rows(grouped_df)
    list_updated_df = add_total_amount(grouped_df, max_idx)
    write_to_excel(data, list_updated_df)
    print("Done")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
