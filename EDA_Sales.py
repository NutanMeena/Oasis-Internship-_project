import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("retail_sales_dataset.csv",index_col=False)

df = pd.DataFrame(data,index=None)
df = df.reset_index(drop=True)
print("Data imported")
df.head()

df.info()
print("Total sales: {}".format(df["Quantity"].sum()))
print("Total profit: {}".format(df["Total Amount"].sum()))
df.columns

print("mean average of total amount = {}".format(df["Total Amount"].mean()))
print("median average of total amount = {}".format(df["Total Amount"].median()))
print("mode of total amount = {}".format(df["Total Amount"].mode()))

df.describe()

sns.relplot(data=df['Total Amount'],kind='scatter')
plt.show()
df['Product Category'].value_counts()
sns.countplot(x=df['Product Category'])
sns.pairplot(data=df,hue="Product Category")
grp = df.groupby("Product Category")[["Quantity","Total Amount"]].sum()
print(grp)
cat = df["Product Category"].value_counts()
cat

grp.plot(kind='bar',figsize=(12,5))
plt.title("Quanitity v/s total amount")
plt.ylabel("Quantity and Total amount")
plt.show()

colour_list = ["red","green","blue"]
cat.plot(kind='pie',figsize=(16,7))
plt.title("pie chart of product category")
plt.axis("equal")
plt.show()

gen = df['Gender'].value_counts()
gen

gen.plot(kind="pie",figsize=(12,5),shadow=True, labels=None,colors=["orange","skyblue"])
gender_list = ['Female', 'Male']
plt.title("pie chart of gender")
plt.axis("equal")
plt.legend(labels=gender_list,loc="upper right")
plt.show()

df["Price per Unit"].corr(df["Total Amount"])
sns.lineplot(x="Price per Unit",y="Total Amount",data=df)
plt.show()