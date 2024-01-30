import pandas as pd
import pprint

def getcol( df, colname ):
    return df.columns.get_loc( colname )


def getvalue( df, index, colname ):
    return df.iat[ index, getcol( df, colname ) ]


def overwrite( df, index, colname, new_value ):
    df.iat[ index, getcol( df, colname ) ] = new_value


def remove_commas_from_columns(df, columns):
    for column in columns:
        # カラムの各値から3桁区切りのコンマを除去
        df[column] = df[column].astype(str).str.replace(',',
        '').replace( " ", "" )

    return df


def main():
    df = pd.read_csv( "../data/countries.csv" )
    columns = [
        'Density (P/Km2)',
        'Agricultural Land( %)',
        'Land Area(Km2)',
        'Armed Forces size',
        'Birth Rate',
        'Calling Code',
        'Co2-Emissions',
        'CPI',
        'CPI Change (%)',
        'Fertility Rate',
        'Forested Area (%)',
        'Gasoline Price',
        'GDP',
        'Gross primary education enrollment (%)',
        'Gross tertiary education enrollment (%)',
        'Infant mortality',
        'Life expectancy',
        'Maternal mortality ratio',
        'Minimum wage',
        'Out of pocket health expenditure',
        'Physicians per thousand',
        'Population',
        'Population: Labor force participation (%)',
        'Tax revenue (%)',
        'Total tax rate',
        'Unemployment rate',
        'Urban_population',
        'Latitude',
        'Longitude',
    ]

    df = remove_commas_from_columns( df, columns=columns )
    df.to_csv( "../data/countries.csv", index=False )


if __name__=="__main__":
    main()
