import pandas as pd
import math

import utils


def wordholic( df, FrontText_colunm, BackText_column, Comment=None, FrontTextLanguage="en-US", BackTextLanguage="en-US" ):
    # FrontText_colunm_number = utils.getcol( df, colname=FrontText_colunm )
    # BackText_column_number = utils.getcol( df, colname=BackText_column )
    # print( df.iloc[ FrontText_colunm_number, BackText_column_number ] )

    df_tmp = df[[ FrontText_colunm, BackText_column ]]
    df_tmp = df_tmp.rename( columns={ FrontText_colunm : "FrontText", BackText_column : "BackText" } )
    df_tmp[ "Comment" ] = Comment
    df_tmp[ "FrontTextLanguage" ] = FrontTextLanguage
    df_tmp[ "BackTextLanguage" ] = BackTextLanguage
    return df_tmp


class countries:
    # 引数 by によって指定された列の、上位 uppper の割合に含まれるデータを抜き出して返す
    def tirm_upper( df, upper=0.70, by="Population" ):
        first_column = df.columns[0]
        df = df.sort_values( by=by )
        length = len( df )
        df = df[ : math.floor( length * upper ) ]
        df = df.sort_values( by=first_column )
        df = df.reset_index( drop=True )

        return df


def main():
    df = pd.read_csv( "../materials/world-data-2023.csv" )
    df = countries.tirm_upper( df, upper=0.70, by="Population" )
    df = wordholic( df=df, FrontText_colunm="Country", BackText_column="Capital/Major City" )
    df.to_csv( "../outputs/countries_and_capitals.csv", index=False )



if __name__=="__main__":
    main()