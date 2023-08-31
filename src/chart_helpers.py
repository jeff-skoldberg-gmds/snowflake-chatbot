import pandas as pd
import streamlit as st

class ChartDrawer:
    def __init__(self, df):
        self.df = df

    def _check_line_chart_friendly(self, date_threshold=0.9, num_threshold=0.9):
        date_cols = []
        num_cols = []

        for col in self.df.columns:
            # Check for date columns
            valid_dates = pd.to_datetime(self.df[col], errors='coerce').notna().sum()
            if valid_dates / len(self.df) >= date_threshold:
                self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
                date_cols.append(col)
            else:
                # Check for numeric columns
                valid_nums = pd.to_numeric(self.df[col], errors='coerce').notna().sum()
                if valid_nums / len(self.df) >= num_threshold:
                    self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
                    num_cols.append(col)

        return len(date_cols) >= 1 and len(num_cols) >= 1, date_cols, num_cols

    @staticmethod
    def is_numeric_series(series):
        try:
            pd.to_numeric(series, errors='raise')
            return True
        except:
            return False

    def _check_bar_chart_friendly(self):
        num_cols = []
        text_cols = []

        for col in self.df.columns:
            if self.is_numeric_series(self.df[col]):
                num_cols.append(col)
            else:
                text_cols.append(col)

        is_friendly = len(num_cols) == 1 and len(text_cols) == 1
        text_col = text_cols[0] if text_cols else None
        num_col = num_cols[0] if num_cols else None

        return is_friendly, text_col, num_col

    def draw_chart(self):
        line_friendly, date_cols, num_cols = self._check_line_chart_friendly()
        bar_friendly, text_col, num_col = self._check_bar_chart_friendly()

        if line_friendly:
            st.line_chart(data=self.df, x=date_cols[0], y=num_cols)
        elif bar_friendly:
            self.df = self.df.sort_values(by=num_col, ascending=False)
            st.bar_chart(data=self.df, x=text_col, y=num_col)
        else:
            pass
            st.write("I cannot easily chart this data.")

# Example usage


#######################################################################
#######################################################################
#######################################################################

##########################you can debug streamlit with config found here#############################################

#  https://www.youtube.com/watch?v=Rtup0kVVCe8&ab_channel=MastersofTechnology


#######################################################################
#######################################################################
#######################################################################
#######################################################################

if __name__ == "__main__":
    df = pd.DataFrame({
    'Date': pd.date_range('2023-08-01', periods=5),
    'Value': [10, 20, 30, 15, 25],
    'Category': ['A', 'B', 'C', 'D', 'E']
})
    chart_drawer = ChartDrawer(df)
    chart_drawer.draw_chart()