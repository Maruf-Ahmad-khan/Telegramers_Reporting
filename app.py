import pandas as pd
import streamlit as st
import plotly.express as px

class DashboardApp:
    def __init__(self):
        self.df = None
        self.filtered_data = None
        self.required_columns = ["name", "camp_name", "action_date", "Total_Order", "Total_Payout"]

    def upload_file(self):
        """Handles file upload and data loading."""
        st.title("Interactive Dashboard with Uploaded Data")
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file:
            self.df = pd.read_csv(uploaded_file)
            st.subheader("Uploaded Data")
            st.dataframe(self.df)
            if not all(col in self.df.columns for col in self.required_columns):
                st.error(f"Uploaded file must include the following columns: {self.required_columns}")
                self.df = None
        else:
            st.info("Please upload a CSV file to get started.")

    def create_pivot_table(self):
        """Creates and displays the pivot table."""
        if self.df is not None:
            st.sidebar.header("Filters")
            selected_names = st.sidebar.multiselect(
                "Select Name(s):", options=self.df["name"].unique(), default=self.df["name"].unique()
            )
            self.filtered_data = self.df[self.df["name"].isin(selected_names)]

            pivot_table = self.filtered_data.pivot_table(
                index=["name", "camp_name", "action_date"],
                values=["Total_Order", "Total_Payout"],
                aggfunc="sum",
            )
            st.subheader("Pivot Table")
            st.dataframe(pivot_table)

    def plot_charts(self):
        """Plots the bar charts for Total_Order and Total_Payout."""
        if self.filtered_data is not None:
            st.subheader("Bar Chart - Total Orders")
            fig_orders = px.bar(
                self.filtered_data,
                x="name",
                y="Total_Order",
                color="camp_name",
                barmode="group",
                facet_row="action_date",
                labels={"name": "Name", "Total_Order": "Total Orders"},
                title="Total Orders by Campaign and Date",
            )
            st.plotly_chart(fig_orders)

            st.subheader("Bar Chart - Total Payouts")
            fig_payouts = px.bar(
                self.filtered_data,
                x="name",
                y="Total_Payout",
                color="camp_name",
                barmode="group",
                facet_row="action_date",
                labels={"name": "Name", "Total_Payout": "Total Payouts"},
                title="Total Payouts by Campaign and Date",
            )
            st.plotly_chart(fig_payouts)

    def run(self):
        """Runs the entire dashboard application."""
        self.upload_file()
        if self.df is not None:
            self.create_pivot_table()
            self.plot_charts()


# Run the application
if __name__ == "__main__":
    app = DashboardApp()
    app.run()
