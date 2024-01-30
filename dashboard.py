import streamlit as st 
import  plotly.express as px 
import  pandas as pd 
import os
import warnings
import plotly.graph_objects as go
warnings.filterwarnings('ignore')
st.set_page_config(page_title="Superstore!!",page_icon=":bar_chart",layout="wide")
st.title("SuperStore EDA")

st.markdown("<style>div.block-container{padding-top:1rem;}</style>",unsafe_allow_html=True)

  
df=pd.read_excel("Dataset Store sales.xlsx")


df_view=df


st.sidebar.image('logo.png',caption='online analytics')
company_name = "SuperStore EDA "  # Replace with your company name
 # Replace with your desired header color in HTML color code format




st.sidebar.title(f"{company_name}")
st.sidebar.header("Chose your filter :  ")  
month=st.sidebar.multiselect("Pick the  Month",df_view["Order date"].dt.month.unique())
year=st.sidebar.multiselect("Pick the  Year",df_view["Order date"].dt.year.unique())
category=st.sidebar.multiselect("Pick the  Category",df_view["Category"].unique())
sub_category=st.sidebar.multiselect("Pick the  Sub-Category",df_view["Sub-Category"].unique())
Distribution_chanel=st.sidebar.multiselect("Pick the  Distribution chanel",df_view["Distribution chanel"].unique())
Payment_type=st.sidebar.multiselect("Pick the  Payment type",df_view["Payment type"].unique())
Consumer_type=st.sidebar.multiselect("Pick the  Consumer type",df_view["Consumer type"].unique())
df_filtred=df_view
if(month):
    df_filtred=df_filtred[df_filtred['Order date'].dt.month.isin(month)]
if(year):
    df_filtred=df_filtred[df_filtred['Order date'].dt.year.isin(year)]
if(category):
    df_filtred=df_filtred[df_filtred['Category'].isin(category)]
if(sub_category):
    df_filtred=df_filtred[df_filtred['Sub-Category'].isin(sub_category)]
if(Distribution_chanel):
    df_filtred=df_filtred[df_filtred['Distribution chanel'].isin(Distribution_chanel)]
if(Payment_type):
    df_filtred=df_filtred[df_filtred['Payment type'].isin(Payment_type)]
if(Consumer_type):
    df_filtred=df_filtred[df_filtred['Consumer type'].isin(Consumer_type)]
if( df_filtred.empty):
    st.write("No Data selected  With This Filter  !!! data is empty ")
else:
    c1_style = "color:#FF69B4"
    c2_style = "color:black"
    c1,c2,c3 = st.columns(3)
    totale_sales=df_filtred["Sales"].sum()
    totale_profit=df_filtred["Total profits"].sum()
    totale_quantity=df_filtred["Quantity"].sum()
    #print(totale_sales)
    
    with c1:
        st.markdown(f'<h2 style="{c1_style}">Total Sales  ✅</h2>', unsafe_allow_html=True)
        st.markdown(f'<h4 ">{totale_sales:,.0f} $</h4>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<h2 style="{c1_style}">Total Profits ✅</h2>', unsafe_allow_html=True)
        st.markdown(f'<h4 ">{totale_profit:,.0f} $</h4>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<h2 style="{c1_style}">Total Quantity✅</h2>', unsafe_allow_html=True)
        st.markdown(f'<h4 ">{totale_quantity:,.0f} </h4>', unsafe_allow_html=True)
    st.write("")
    st.write("")
    st.subheader("Data Visualisation 🔎 ")

    df_filtred["Month"]=df_filtred['Order date'].dt.strftime('%B')
    profits_by_month = df_filtred.groupby('Month')['Total profits'].sum()
    sales_by_month = df_filtred.groupby('Month')['Sales'].sum()
    v1,v2=st.columns(2)
    with v1:
   # st.subheader("Profits evolution / month")
      fig = px.bar(profits_by_month,x=profits_by_month.index,y=profits_by_month.values,
                 text=['${:,.2f}'.format(x) for x in profits_by_month.values],
                 template="seaborn",
                  color_discrete_sequence=["#F11A7B"])
      fig.update_layout(
      title='Profits Evolution by Month',
       xaxis_title='Month',
       yaxis_title='Total Profits',
     
          )
      st.plotly_chart(fig,use_container_width=True,height=200)
    with v2 :
       # st.subheader("Sales evolution / month")
        fig = px.bar(sales_by_month,x=sales_by_month.index,y=sales_by_month.values,
                    text=['${:,.2f}'.format(x) for x in sales_by_month.values],
                    template="seaborn",
                    color_discrete_sequence=["#8062D6"])
        fig.update_layout(
       title='Sales Evolution by Month',
        xaxis_title='Month',
        yaxis_title='Sales',
        
            )
        st.plotly_chart(fig,use_container_width=True,height=200)
    v3,v4 =st.columns(2)
    with v3 :
                customer_sales = df_filtred.groupby(['Customer ID', 'Customer name'])['Sales'].sum().reset_index()
                # Sort the data in descending order based on sales and select the top 10 customers
                top_10_customers = customer_sales.nlargest(10, 'Sales')
                fig = px.bar(
                data_frame=top_10_customers,
                y='Customer name',  # Change y to 'Customer name' to place it on the y-axis
                x='Sales',  # Change x to 'Sales' to place it on the x-axis
                text=['${:,.2f}'.format(x) for x in top_10_customers['Sales']],  # Format text with dollar sign and comma
                template="seaborn",
                color_discrete_sequence=["#ACFADF"],
                orientation='h',  # Set orientation to 'h' for horizontal bars
                
            )

                fig.update_layout(
                    title='Top 10 Customers by Sales',
                    yaxis_title='Customer Name',  # Update y-axis title
                    xaxis_title='Total Sales',  # Update x-axis title
                    margin=dict(l=50, r=0, t=30, b=0),  # Adjust the margin to accommodate longer customer names
                )

                st.plotly_chart(fig, use_container_width=True)
 
    custom_colors = ['#F11A7B', '#8062D6', '#ACFADF', '#FF33A3', '#A333FF']
    with v4 :
        grouped_data = df_filtred.groupby(['Category', 'Sub-Category', 'Product Name']).size().reset_index(name='Count')
        fig=px.sunburst(data_frame=grouped_data,path=['Category', 'Sub-Category', 'Product Name'])
        # Update the layout of the chart
        fig.update_traces(marker=dict(colors=custom_colors, line=dict(color='#000000', width=1)))
        fig.update_layout(
            title='Sunburst Chart of Category / Subcategory / Article',
        )

        # Display the chart using Streamlit
        st.plotly_chart(fig, use_container_width=True)
    v5,v6=st.columns(2)
    with v5 :
          sales_by_payment=df_filtred.groupby("Payment type")["Sales"].sum()
    
          fig=px.pie(sales_by_payment,values=sales_by_payment.values,names=sales_by_payment.index,hole=0.5)
    
          fig.update_traces(
            text=sales_by_payment.index,
            textposition="outside",
            
            marker=dict(colors=custom_colors, line=dict(color='#000000', width=1))
        )


          fig.update_layout(
            title=' Sales by Payment ',
            xaxis_title='Payment type',
            yaxis_title='Total Sales',
             margin=dict(l=50, r=0, t=20, b=20)
        )
          st.plotly_chart(fig, use_container_width=True)
    with v6 :
            sales_by_distribution=df_filtred.groupby("Distribution chanel")["Sales"].sum()
            
            fig=px.pie(sales_by_distribution,values=sales_by_distribution.values,names=sales_by_distribution.index,hole=0.5)
            fig.update_traces(text=sales_by_distribution.index,textposition="outside"
                            , marker=dict(colors=custom_colors, line=dict(color='#000000', width=1)))
            fig.update_layout(
                    title=' Sales by Distribution chanel ',
                    xaxis_title='Distribution chanel',
                    yaxis_title='Total Sales',
                    
                )
            st.plotly_chart(fig, use_container_width=True)
    v7,v8,v9=st.columns(3)
    with v7 :
        sales_by_custumer=df_filtred.groupby('Consumer type')["Sales"].sum()
        fig=px.pie(sales_by_custumer,values=sales_by_custumer.values,names=sales_by_custumer.index,hole=0.5)
        fig.update_traces(text=sales_by_custumer.index,textposition="outside"
                        ,marker=dict(colors=custom_colors, line=dict(color='#000000', width=1)))
        fig.update_layout(
                title=' Sales by Cunsumer type ',
                xaxis_title=' Cunsumer type',
                yaxis_title='Total Sales',
                margin=dict(l=50, r=0, t=35, b=20)
            )
        st.plotly_chart(fig, use_container_width=True)
    with v8:
        sales_by_region=df_filtred.groupby('Region')["Sales"].sum()
        fig=px.pie(sales_by_region,values=sales_by_region.values,names=sales_by_region.index,hole=0.5)
        fig.update_traces(text=sales_by_region.index,textposition="outside"
                        ,marker=dict(colors=custom_colors, line=dict(color='#000000', width=1)))
        fig.update_layout(
                title=' Sales by Region',
                xaxis_title=' Region',
                yaxis_title='Total Sales',
                margin=dict(l=50, r=0, t=35, b=20)
            )
        st.plotly_chart(fig, use_container_width=True)
    with v9 :
        sales_by_branch=df_filtred.groupby("Company Branch")["Sales"].sum()   
        fig=px.pie(sales_by_branch,values=sales_by_branch.values,names=sales_by_branch.index,hole=0.5)
        fig.update_traces(text=sales_by_branch.index,textposition="outside"
                        , marker=dict(colors=custom_colors, line=dict(color='#000000', width=1)))
        fig.update_layout(
                title=' Sales by Company Branch ',
                xaxis_title='Company Branch',
                yaxis_title='Total Sales',
                margin=dict(l=50, r=0, t=35, b=20)
            )
        st.plotly_chart(fig, use_container_width=True)
    st.divider()
    df_filtred.index=df_filtred["Order date"]
    df=df_filtred.groupby("Month")["Sales"].sum()
    fig=st.line_chart(df)
   
   


