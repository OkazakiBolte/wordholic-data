import pandas as pd
import math
from googletrans import Translator
import time

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

def translate_and_overwrite( csv ):
    df = pd.read_csv( csv )
    translator = Translator()
    df[ "国名" ] = ""
    df[ "首都" ] = ""

    for i in df.index:
        country_name_en = utils.getvalue( df, i, "Country" )
        capital_name_en = utils.getvalue( df, i, "Capital/Major City" )
        country_name_jp = translator.translate( country_name_en, dest="ja" ).text
        capital_name_jp = translator.translate( capital_name_en, dest="ja" ).text
        print( country_name_jp, capital_name_jp )
        utils.overwrite( df, i, "国名", country_name_jp )
        utils.overwrite( df, i, "首都", capital_name_jp )
        time.sleep(1)

    df.to_csv( csv, index=False )

def main():
    df = pd.read_csv( "../data/countries.csv", thousands="," )
    df = countries.tirm_upper( df, upper=1, by="Capital/Major City" )
    # df = df.sort_values( by="Capital/Major City", ascending=False )
    df = wordholic( df=df, FrontText_colunm="Country", BackText_column="Capital/Major City" )
    df.to_csv( "../outputs/countries_and_capitals.csv", index=False )



if __name__=="__main__":
    # main()
    translate_and_overwrite( "../data/countries.csv" )