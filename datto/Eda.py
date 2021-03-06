import pandas as pd


class Eda:
    def separate_cols_by_type(self, df):
        """
        Split the DataFrame into two groups by type

        Parameters
        --------
        df: DataFrame

        Returns
        --------
        numerical_vals: DataFrame
        categorical_vals: DataFrame
        """
        numerical_vals = df.select_dtypes(exclude=["object", "bool"])
        categorical_vals = df.select_dtypes(include=["object", "bool"])

        return numerical_vals, categorical_vals

    def check_for_mistyped_booleans(self, numerical_vals):
        """
        Check for columns coded as ints/floats that should actually be booleans

        Parameters
        --------
        numerical_vals: list

        Returns
        --------
        boolean_cols: list

        """
        boolean_cols = []
        for col in numerical_vals:
            if numerical_vals[col].nunique() <= 2:
                print(col)
                print(numerical_vals[col].unique())
                boolean_cols.append(col)

        return boolean_cols

    def find_cols_to_exclude(self, df):
        """
        Returns columns that may not be helpful for model building.

        Exclusion criteria:
        - Possible PII (address, name, username, date, etc. in col name)
        - Large proportion of nulls
        - Only 1 value in entire col
        - Dates
        - Low variance in col values
        - Large number of categorical values

        Parameters
        --------
        df: DataFrame

        Returns
        --------
        lst: list

        """
        lst = []
        for col in df.columns:
            if (
                "address" in str(col)
                or "first_name" in str(col)
                or "last_name" in str(col)
                or "username" in str(col)
                or "_id" in str(col)
                or "date" in str(col)
                or "time" in str(col)
            ):
                lst.append({col: "Considering excluding because potential PII column."})
            elif df[col].isnull().sum() / float(df.shape[0]) >= 0.5:
                lst.append(
                    {
                        col: "Considering excluding because {}% of column is null.".format(
                            (df[col].isnull().sum() / float(df.shape[0]) * 100.0)
                        )
                    }
                )
            elif len(df[col].unique()) <= 1:
                lst.append(
                    {
                        col: "Considering excluding because column includes only one value."
                    }
                )
            elif df[col].dtype == "datetime64[ns]":
                lst.append(
                    {col: "Considering excluding because column is a timestamp."}
                )
            elif df[col].dtype not in ["object", "bool"]:
                if df[col].var() < 0.00001:
                    lst.append(
                        {
                            col: "Considering excluding because column variance is low ({})".format(
                                df[col].var()
                            )
                        }
                    )
            elif df[col].dtype in ["object", "bool"]:
                if len(df[col].unique()) > 200:
                    lst.append(
                        {
                            col: "Considering excluding because object column has large number of unique values ({})".format(
                                len(df[col].unique())
                            )
                        }
                    )

        [print(x) for x in lst]

        return lst

    def sample_unique_vals(self, df):
        """
        Examine a few unique vals in each column

        Parameters
        --------
        df: DataFrame
        """
        for col in df:
            print(col)
            try:
                print(df[col].unique()[:20])
                print(df[col].nunique())
            except Exception:
                pass
            print("\n------------------------------------\n")

    def find_correlated_features(self, df):
        """
        Find & sort correlated features

        Parameters
        --------
        df: DataFrame

        Returns
        --------
        s: Series

        """
        if df.empty:
            return pd.Series()

        c = df.corr().abs()
        s = c.unstack()
        s = s[s <= 0.99999]
        s = s.sort_values(ascending=False)
        print(s)
        return s
