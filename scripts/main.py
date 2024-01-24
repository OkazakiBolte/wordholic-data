import pandas as pd




def main():
    # print( "Hello World!" )
    df = pd.read_csv( "../materials/world-data-2023.csv", encoding="utf-8" )
    df.to_csv( "../data/countries.csv", index=False )


if __name__=="__main__":
    main()