import pandas as pd

def getcol( df, colname ):
    return df.columns.get_loc( colname )


def getvalue( df, index, colname ):
    return df.iat[ index, getcol( df, colname ) ]


def overwrite( df, index, colname, new_value ):
    df.iat[ index, getcol( df, colname ) ] = new_value


def main():
    df = pd.read_csv( "../test/test.csv" )
    print( getvalue( df, 1, "残高（円）" ) )
    overwrite( df, 4, "年月日", "hoge" )
    print( df )


if __name__=="__main__":
    main()
