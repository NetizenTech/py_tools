#!/usr/bin/python3
import pandas as pd
from sqlalchemy import create_engine

TSV = "db-text/db.tsv"
SQL = "db-text/db.sqlite"
TBL = "data"


def main():
    df1 = pd.read_csv(TSV, sep="\t")
    engine = create_engine('sqlite:///{}'.format(SQL))
    df1.to_sql(TBL, con=engine,  if_exists='replace', index_label='id')


if __name__ == '__main__':
    main()
