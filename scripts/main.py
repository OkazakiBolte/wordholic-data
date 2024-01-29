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


    def check_japanese_name():
        # https://note.com/kentoide/n/n16354c4b3458 こちらから日本語の国名と首都のデータを拝借
        # 機械翻訳したもののうち、こちらにないものを手直ししていく
        df_correct = pd.read_csv( "../data/capital_cities_2022_0.csv" )

        df = pd.read_csv( "../data/countries.csv" )

        print( "国名" )
        for i in df.index:
            name_jp = utils.getvalue( df, i, "国名" )
            if name_jp not in df_correct[ "国名" ].tolist():
                # 日本語名で一致しているものがなければ、英語名で一致しているものの日本語で置き換える
                found = False
                name_en = utils.getvalue( df, i, "Country" )
                for j in df_correct.index:
                    name_en_correct = utils.getvalue( df_correct, j, "Country" )
                    name_jp_correct = utils.getvalue( df_correct, j, "国名" )
                    if name_en==name_en_correct:
                        # print( f"Replacing {name_jp} -> {name_jp_correct}" )
                        utils.overwrite( df, i, "国名", new_value=name_jp_correct )
                        found = True

                if not found:
                    print( f"Not found: { name_en }, { name_jp }" )

        # 同様の置き換えを首都についても行う
        print( "首都" )
        for i in df.index:
            name_jp = utils.getvalue( df, i, "首都" )
            if name_jp not in df_correct[ "首都" ].tolist():
                # 日本語名で一致しているものがなければ、英語名で一致しているものの日本語で置き換える
                found = False
                name_en = utils.getvalue( df, i, "Capital/Major City" )
                for j in df_correct.index:
                    name_en_correct = utils.getvalue( df_correct, j, "Capital" )
                    name_jp_correct = utils.getvalue( df_correct, j, "首都" )
                    if name_en==name_en_correct:
                        # print( f"Replacing {name_jp} -> {name_jp_correct}" )
                        utils.overwrite( df, i, "首都", new_value=name_jp_correct )
                        found = True

                if not found:
                    print( f"Not found: { name_en }, { name_jp }" )

        df.to_csv( "../data/countries.csv", index=False )


    def japanese_and_english_name( csv="../data/countries.csv" ):
        df = pd.read_csv( csv )
        df[ "国名 (Country)" ] = ""
        df[ "首都 (Capital)" ] = ""
        for i in df.index:
            country_jp = utils.getvalue( df, i, "国名" )
            capital_jp = utils.getvalue( df, i, "首都" )
            country_en = utils.getvalue( df, i, "Country" )
            capital_en = utils.getvalue( df, i, "Capital/Major City" )
            utils.overwrite( df, i, "国名 (Country)", f"{country_jp} ({country_en})" )
            utils.overwrite( df, i, "首都 (Capital)", f"{capital_jp} ({capital_en})" )
        df.to_csv(csv, index=False )



def main():
    df = pd.read_csv( "../data/countries.csv", thousands="," )
    df = countries.tirm_upper( df, upper=0.6, by="Population" )
    # df = df.sort_values( by="Capital/Major City", ascending=False )
    df = wordholic( df=df, FrontText_colunm="Country", BackText_column="Capital/Major City" )
    df.to_csv( "../outputs/countries_and_capitals_upper_60%.csv", index=False )



if __name__=="__main__":
    # main()
    countries.japanese_and_english_name( csv="../data/countries.csv" )