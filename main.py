import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

    #page setupe
st.set_page_config(layout="wide",page_title="Startup Analysis",page_icon="📊")
df = pd.read_csv("Startup_Cleaned.csv")
df["date"] = pd.to_datetime(df["date"],errors="coerce")
df["year"] = df["date"].dt.year
df["months"]=df["date"].dt.month

     # startup page

def load_startup_details(startup):
    st.title(startup)
    startup_df = df[df["startup"] == startup]
    st.header("Startup Information")
    col1, col2, col3 = st.columns(3)
    with col1:
        vertical = startup_df["vertical"].iloc[0]
        st.metric("Vertical",vertical)
    with col2:
        subvertical = startup_df["subvertical"].iloc[0]
        st.metric("Subvertical",subvertical)
    with col3:
        city = startup_df["city"].iloc[0]
        st.metric("City",city)


    # funding history
    st.header("Funding History")
    funding_history = startup_df[["date", "round", "investor", "amount"]].sort_values("date",ascending=False)
    st.dataframe(funding_history,use_container_width=True)

    # funding graph
    st.subheader("Funding Over Time")
    funding_graph = startup_df.groupby("date")["amount"].sum()
    fig1, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(funding_graph.index,funding_graph.values,marker="o")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Funding Amount")
    ax1.set_title("Funding History of " + startup)
    plt.xticks(rotation=45)
    st.pyplot(fig1)

    def load_investor_details(investor):
        st.title(investor)
        # load the resent 5 investemnt of the investor
        st.subheader("Most Resent Investment")
        last5_df = df[df["investor"].str.contains(investor)].head()[
            ["date", "startup", "vertical", "city", "round", "amount"]]
        st.dataframe(last5_df)
        col1, col2 = st.columns(2)
        with col1:
            # Biggest investemtn
            big_series = df[df["investor"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(
                ascending=False).head()
            st.subheader("Biggest Investment")
            fig, ax = plt.subplots()
            ax.bar(big_series.index, big_series.values)
            st.pyplot(fig)
        with col2:
            vertica_series = df[df["investor"].str.contains(investor)].groupby("vertical")["amount"].sum()
            st.subheader("Sector Invested In")
            fig1, ax1 = plt.subplots()
            ax1.pie(vertica_series, labels=vertica_series.index, autopct="%0.01f%%")
            st.pyplot(fig1)
        col1, col2 = st.columns(2)
        with col1:
            vertica_series = df[df["investor"].str.contains(investor)].groupby("round")["amount"].sum()
            st.subheader("Stage In")
            fig1, ax1 = plt.subplots()
            ax1.pie(vertica_series, labels=vertica_series.index, autopct="%0.01f%%")
            st.pyplot(fig1)
        with col2:
            vertica_series = df[df["investor"].str.contains(investor)].groupby("city")["amount"].sum()
            st.subheader("City In")
            fig1, ax1 = plt.subplots()
            ax1.pie(vertica_series, labels=vertica_series.index, autopct="%0.01f%%")
            st.pyplot(fig1)
        year_series = df[df["investor"].str.contains(investor)].groupby("year")["amount"].sum()
        st.subheader("YoY Investment")
        fig2, ax2 = plt.subplots()
        ax2.plot(year_series.index, year_series.values)
        ax2.set_xlabel("Year")
        ax2.set_ylabel("Investment Amount")
        ax2.set_title(investor)
        st.pyplot(fig2)

    #over all analysis page
def load_overall_analysis():
    st.title("Over All Analysis")
    #tota invested amount
    total = round(df["amount"].sum())
    #maximum amount infused in startup
    max_total = df.groupby("startup")["amount"].max().sort_values(ascending=False).head(1).values[0]
    # average funding
    avg_funding = df.groupby("startup")["amount"].sum().mean()
    # Total funded Startup
    num_startup = df["startup"].nunique()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Amount", str(total) + " Cr")
    with col2:
        st.metric("Max", str(max_total) + " Cr")
    with col3:
        st.metric("Average", str(round(avg_funding)) + " Cr")
    with col4:
        st.metric("Funded Startup",num_startup)

    st.header("MoM Graph")
    selected_option = st.selectbox("Select Type",["Total", "Count"])
    if selected_option == "Total":
        temp_df = df.groupby(["year", "months"])["amount"].sum().reset_index()
    else:
        temp_df = df.groupby(["year", "months"])["amount"].count().reset_index()
    # Sort after creating temp_df
    temp_df = temp_df.sort_values(["year", "months"])
    # Create X-axis
    temp_df["x_axis"] = (
            temp_df["months"].astype(str) + "-" + temp_df["year"].astype(str) )
    # Graph
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    ax3.plot(temp_df["x_axis"], temp_df["amount"])
    ax3.set_xlabel("Month-Year")
    if selected_option == "Total":
        ax3.set_ylabel("Total Funding")
        ax3.set_title("Month-on-Month Total Funding")
    else:
        ax3.set_ylabel("Number of Funding Records")
        ax3.set_title("Month-on-Month Funding Count")
    plt.xticks(rotation=90)
    st.pyplot(fig3)

    # sector analysis
    st.header("Sector Analysis")
    col1, col2 = st.columns(2)
    with col1:
        sector_amount = df.groupby("vertical")["amount"].sum().sort_values(ascending=False).head(10)
        st.subheader("Top Sectors by Funding")
        fig1, ax1 = plt.subplots()
        ax1.pie(sector_amount.values,labels=sector_amount.index,autopct="%0.1f%%")
        st.pyplot(fig1)
    with col2:
        sector_count = df.groupby("vertical")["startup"].nunique().sort_values(ascending=False).head(10)
        st.subheader("Top Sectors by Startup Count")
        fig2, ax2 = plt.subplots()
        ax2.pie(sector_count.values,labels=sector_count.index,autopct="%0.1f%%")
        st.pyplot(fig2)

    # funding type
    st.header("Funding Type")
    funding_type = df.groupby("round")["amount"].sum().sort_values(ascending=False)
    fig4, ax4 = plt.subplots(figsize=(12, 5))
    ax4.bar( funding_type.index,funding_type.values)
    ax4.set_xlabel("Funding Round")
    ax4.set_ylabel("Total Funding")
    ax4.set_title("Funding Amount by Funding Type")
    plt.xticks(rotation=45)
    st.pyplot(fig4)

    # city wise funding
    st.header("City Wise Funding")
    city_funding = df.groupby("city")["amount"].sum().sort_values(ascending=False).head(10)
    fig5, ax5 = plt.subplots(figsize=(12, 5))
    ax5.bar(city_funding.index,city_funding.values)
    ax5.set_xlabel("City")
    ax5.set_ylabel("Total Funding")
    ax5.set_title("Top 10 Cities by Total Funding")
    plt.xticks(rotation=45)
    st.pyplot(fig5)

    # top startups
    st.header("Top Startups")
    selected_year = st.selectbox("Select Year",["Overall"] + sorted(df["year"].dropna().unique().astype(int).tolist(),reverse=True))
    if selected_year == "Overall":
        top_startups = df.groupby("startup")["amount"].sum().sort_values(ascending=False).head(10)
    else:
        top_startups = df[df["year"] == selected_year].groupby("startup")["amount"].sum().sort_values(ascending=False).head(10)
    fig6, ax6 = plt.subplots(figsize=(12, 5))
    ax6.bar(top_startups.index,top_startups.values)
    ax6.set_xlabel("Startup")
    ax6.set_ylabel("Total Funding")
    ax6.set_title("Top Startups")
    plt.xticks(rotation=45,ha="right")
    st.pyplot(fig6)

    # top investors
    st.header("Top Investors")
    top_investors = df.groupby("investor")["amount"].sum().sort_values(ascending=False).head(10)
    fig7, ax7 = plt.subplots(figsize=(12, 5))
    ax7.bar(top_investors.index,top_investors.values)
    ax7.set_xlabel("Investor")
    ax7.set_ylabel("Total Funding")
    ax7.set_title("Top Investors by Funding")
    plt.xticks(rotation=45,ha="right")
    st.pyplot(fig7)

    # funding heatmap
    st.header("Funding Heatmap")
    heatmap_data = pd.pivot_table(df,values="amount",index="vertical",columns="year",aggfunc="sum")
    fig8, ax8 = plt.subplots(figsize=(12, 7))
    image = ax8.imshow(heatmap_data.fillna(0),aspect="auto")
    ax8.set_xticks(range(len(heatmap_data.columns)))
    ax8.set_xticklabels(heatmap_data.columns.astype(int))
    ax8.set_yticks( range(len(heatmap_data.index)))
    ax8.set_yticklabels(heatmap_data.index )
    ax8.set_xlabel("Year")
    ax8.set_ylabel("Sector")
    ax8.set_title("Funding Heatmap")
    fig8.colorbar(image)
    st.pyplot(fig8)

    #investor page
def load_investor_details(investor):
    st.title(investor)
    #load the resent 5 investemnt of the investor
    st.subheader("Most Resent Investment")
    last5_df = df[df["investor"].str.contains(investor)].head()[["date", "startup", "vertical", "city", "round", "amount"]]
    st.dataframe(last5_df)
    col1, col2 = st.columns(2)
    with col1:
        # Biggest investemtn
        big_series = df[df["investor"].str.contains(investor)].groupby("startup")["amount"].sum().sort_values(ascending=False).head()
        st.subheader("Biggest Investment")
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        vertica_series = df[df["investor"].str.contains(investor)].groupby("vertical")["amount"].sum()
        st.subheader("Sector Invested In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertica_series,labels=vertica_series.index,autopct="%0.01f%%")
        st.pyplot(fig1)
    col1, col2 = st.columns(2)
    with col1:
        vertica_series = df[df["investor"].str.contains(investor)].groupby("round")["amount"].sum()
        st.subheader("Stage In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertica_series, labels=vertica_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)
    with col2:
        vertica_series = df[df["investor"].str.contains(investor)].groupby("city")["amount"].sum()
        st.subheader("City In")
        fig1, ax1 = plt.subplots()
        ax1.pie(vertica_series, labels=vertica_series.index, autopct="%0.01f%%")
        st.pyplot(fig1)
    year_series = df[df["investor"].str.contains(investor)].groupby("year")["amount"].sum()
    st.subheader("YoY Investment")
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    ax2.set_xlabel("Year")
    ax2.set_ylabel("Investment Amount")
    ax2.set_title(investor)
    st.pyplot(fig2)



st.sidebar.title("Startup Funding Analysis")
option = st.sidebar.selectbox("Select One",["Over All Analysis","Startup","Investor"])
if option == "Over All Analysis":
    load_overall_analysis()
elif option == "Startup":
    st.title("Startup Funding Analysis")
    selected_startup = st.sidebar.selectbox("Select One",sorted(df["startup"].dropna().unique().tolist()))
    btn1 = st.sidebar.button("Find Startup Details")
    if btn1:
        load_startup_details(selected_startup)

elif option == "Investor":
    selected_investor = st.sidebar.selectbox("Select One",sorted(set(df["investor"].str.split(",").sum())))
    btn2 = st.sidebar.button("Find Investor Details")
    if btn2:
        load_investor_details(selected_investor)
