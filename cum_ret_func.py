import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)
pd.set_option("display.max_colwidth", None)
pd.set_option("display.width", None)


df_sic_peers = pd.read_csv("df_sic_peers.csv")

df_sic_peers[["ticker", "datekey"]][df_sic_peers["ticker"] == "ACI"]

# Per manual inspection, ACI's price series starts around the end of
# 6/2020, but there are financial statement obs going back to 2018.
# I think this is because of the data filed with the S1 statement
# for the IPO.

len(df_sic_peers["ticker"].unique())

df_sic_peers["ticker"].unique()

df_prices = pd.read_csv("prices.csv")

len(df_prices["ticker"].unique())

# There are 19 unique tickers in the financial statement data,
# but 20 in the price data.
df_prices["ticker"].unique()

# Below identifies the ticker in the price data that is not in the
# financial statement data.
for i in df_prices["ticker"].unique():
    if i not in df_sic_peers["ticker"].unique():
        print(i)

# Per manual inspection of the SF1 table, CBD only has ART, ARY, MRT and MRY
# for dimension so they weren't included in the original data pull.
# The original data query had dimension="ARQ"


df_prices[df_prices["ticker"] == "ACI"]

df_prices[
    (df_prices["ticker"] == "ACI")
    & (df_prices["date"] >= "2018-05-07")
    & (df_prices["date"] <= "2020-06-24")
]

# Above shows no price data before the end of June, 2020.
df_sic_peers.head()

# Below identifies SEC filing dates without a stock price date. At first,
# I thought these would all be cases of companies filing on holidays or
# weekends, but after manual inspection it appears that most of these
# are related to IPO's. See notes and further inspection below the loop.

# First, itererate through the dataframe based on the unique tickers.
for i in df_sic_peers["ticker"].unique():
    df_temp_sic = df_sic_peers[df_sic_peers["ticker"] == i]
    df_temp_prices = df_prices[df_prices["ticker"] == i]

    # Create two lists, one that contains the dates from the SEC fillings
    # and the other that contains dates from the stock prices series.
    lister = []
    lister_2 = []
    for j in df_temp_sic["datekey"]:
        lister.append(j)
    for q in df_temp_prices["date"]:
        lister_2.append(q)

    # Identify financial statement dates without stock price data. Also,
    # see if shifting the SEC reporting dates forward by a day or two and
    # backward by a day or two result in mergeable dates. Note that this
    # only worked for GO and FWMHQ around their IPOs. This is further
    # examined below the loop. GO's first trading day was 6/20/19
    # and FWMHQ's first trading day was 4/15/13. The loops further
    # condition on pd.dattime().weekday() values which are 0 for Monday
    # and 6 for Sunday. .weekday() values in the data are [0-4].
    for z in lister:
        if z not in lister_2:
            print("Non-trading date fillings:", i, z)
            print("Day of the week is:", i, z, pd.to_datetime(z).weekday())
            print(
                str(pd.to_datetime(z).date()),
                str(pd.to_datetime(z).date() + pd.Timedelta("1 day")),
            )
            if pd.to_datetime(z).weekday() <= 3:
                print(
                    "Plus one day:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() + pd.Timedelta("1 day")),
                    str(pd.to_datetime(z).date() + pd.Timedelta("1 day"))
                    in lister_2,
                )
            if pd.to_datetime(z).weekday() <= 3:
                print(
                    "Minus one day:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() - pd.Timedelta("1 day")),
                    str(pd.to_datetime(z).date() - pd.Timedelta("1 day"))
                    in lister_2,
                )
            if pd.to_datetime(z).weekday() <= 3:
                print(
                    "Plus two days:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() + pd.Timedelta("2 days")),
                    str(pd.to_datetime(z).date() + pd.Timedelta("2 days"))
                    in lister_2,
                )
            if pd.to_datetime(z).weekday() <= 3:
                print(
                    "Minus two days:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() - pd.Timedelta("2 days")),
                    str(pd.to_datetime(z).date() - pd.Timedelta("2 days"))
                    in lister_2,
                )
            if (pd.to_datetime(z).weekday() > 3) & (
                pd.to_datetime(z).weekday() <= 5
            ):
                print(
                    "Plus one day:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() + pd.Timedelta("1 day")),
                    str(pd.to_datetime(z).date() + pd.Timedelta("1 day"))
                    in lister_2,
                )
                print(
                    "Minus one day:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() - pd.Timedelta("1 day")),
                    str(pd.to_datetime(z).date() - pd.Timedelta("1 day"))
                    in lister_2,
                )
                print(
                    "Plus two days:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() + pd.Timedelta("2 days")),
                    str(pd.to_datetime(z).date() + pd.Timedelta("2 days"))
                    in lister_2,
                )
                print(
                    "Minus two days:",
                    i,
                    z,
                    str(pd.to_datetime(z).date() - pd.Timedelta("2 days")),
                    str(pd.to_datetime(z).date() - pd.Timedelta("2 days"))
                    in lister_2,
                )

# Manual inspection of some of the firms discussed above.
df_prices[
    (df_prices["ticker"] == "SWY")
    & (df_prices["date"] >= "2015-03-01")
    & (df_prices["date"] <= "2015-03-10")
]

df_prices[df_prices["ticker"] == "SWY"]

df_prices[
    (df_prices["ticker"] == "GO")
    & (df_prices["date"] >= "2019-06-01")
    & (df_prices["date"] <= "2019-06-30")
]

df_prices[
    (df_prices["ticker"] == "FWMHQ")
    & (df_prices["date"] >= "2013-04-01")
    & (df_prices["date"] <= "2013-04-30")
]

df_sic_peers.head()

# Manually overwrite the EDGAR filling date for GO and FWMHQ to faciliate
# merging with the price data.
df_sic_peers.loc[
    (df_sic_peers["datekey"] == "2019-06-18")
    & (df_sic_peers["ticker"] == "GO")
]

df_sic_peers.loc[
    (df_sic_peers["datekey"] == "2019-06-18")
    & (df_sic_peers["ticker"] == "GO"),
    "datekey",
] = "2019-06-20"

df_sic_peers.loc[
    (df_sic_peers["datekey"] == "2019-06-20")
    & (df_sic_peers["ticker"] == "GO")
]

df_sic_peers.loc[
    (df_sic_peers["datekey"] == "2013-04-16")
    & (df_sic_peers["ticker"] == "FWMHQ")
]

df_sic_peers.loc[
    (df_sic_peers["datekey"] == "2013-04-16")
    & (df_sic_peers["ticker"] == "FWMHQ"),
    "datekey",
] = "2013-04-17"

df_sic_peers.loc[
    (df_sic_peers["datekey"] == "2013-04-17")
    & (df_sic_peers["ticker"] == "FWMHQ")
]


# Left join df_prices and df_sic_peers.
df_sic_peers.info(verbose=True)
df_prices.info()

# Convert date variables to datetime.
df_sic_peers["datekey"] = pd.to_datetime(df_sic_peers["datekey"])
df_prices["date"] = pd.to_datetime(df_prices["date"])

df_sic_peers.rename(columns={"datekey": "date"}, inplace=True)


# Merge
df = pd.merge(df_prices, df_sic_peers, on=["ticker", "date"], how="left")


df.head()

len(df)
len(df_prices)
len(df_sic_peers)

# Sort by ticker and datekey
df.sort_values(by=["ticker", "date"], ascending=[True, True], inplace=True)
df.head()

df.reset_index(drop=True, inplace=True)
df.head()


lister = []


def cumRet(df, window):

    """ This function calculates the return for the period of t-1 from the
    EDGAR file date through t + window. New dataframes for each ticker
    are then stored into a list, lister. These will be merged in later
    with the dataframe, df, that has both price and financial
    statement data.  """

    for i, t in enumerate(df["ticker"].unique()):
        df_temp = df[df["ticker"] == t].copy()
        # df_temp['cum_ret']= np.nan
        df_temp.loc[:, "cum_ret"] = np.nan

        cut_offs = []
        for j in df_temp["calendardate"][
            df_temp["calendardate"].notnull()
        ].index:
            cut_offs.append(j)

        for x in cut_offs:
            # start the window from the day before earnings are announced.
            # this is to try and deal with companies that may release earnings
            # either after markets close on a given day, before
            # markets open on a given day, or during a trading day.

            # Below modifies starting index for GO and FWMHQ who
            # have no price observations before the IPO filings.
            if x - 1 not in df_temp.index:
                start_index = df_temp.index.min()
            else:
                start_index = x - 1

            # if there are not t-1 plus 16 trading days after a
            # given announcement, use the last trading day for the
            # company in the dataframe.
            if x + window not in df_temp.index:
                end_index = df_temp.index.max()
            else:
                end_index = start_index + window

            print(
                "ticker is",
                t,
                "start_index",
                start_index,
                "end_index",
                end_index,
            )
            print(
                "start_price",
                df_temp["close"].loc[start_index],
                "end_price",
                df_temp["close"].loc[end_index],
            )
            # modify the start_index by adding one to line up with
            # the actual earnings report release date.
            df_temp["cum_ret"].loc[start_index + 1] = (
                df_temp["close"].loc[end_index]
                - df_temp["close"].loc[start_index]
            ) / df_temp["close"].loc[start_index]

        print("appending", df_temp["ticker"].iloc[0])
        lister.append(df_temp[["ticker", "date", "cum_ret"]])


cumRet(df, 16)
len(lister)

combined_df = pd.concat([i for i in lister])
len(combined_df)
combined_df.head()

df_fin = pd.merge(df_sic_peers, combined_df, on=["ticker", "date"], how="left")

df_fin.shape
df_fin.head()

df_fin.sort_values(by=["ticker", "date"], ascending=[True, True], inplace=True)

# Visual inspection and reasonableness checks.
df_fin[["ticker", "date", "cum_ret"]]


len(df_fin["ticker"].unique())

df_fin["ticker"].unique()
