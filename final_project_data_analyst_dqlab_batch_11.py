# -*- coding: utf-8 -*-
"""Final Project - Data Analyst - DQLab Batch 11.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12jxgRfNuGf3K0NHHLjICsqshihFwbIwf

# **Final Project DQLab DA Batch 11**

Dalam project ini, data yang digunakan yaitu **Mexico Toy Sales** dari
https://mavenanalytics.io/

Project ini bertujuan untuk mengetahui beberapa hal, yaitu:
  1. Jumlah penjualan
  2. Total keuntungan
  3. Mainan yang paling laku
  4. Toko yang paling banyak dikunjungi

## Tools
Terdapat 3 tools yang digunakan dalam project ini
1. `pandas` berfungsi untuk melakukan manipulasi data
2. `matplotlib.pyplot` berfungsi untuk memberikan *style* pada *data visualisation*
3. `seborn` berfungsi untuk membuat grafik *data visualisation*
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""## Dataset

Dataset yang digunakan yaitu berasal dari https://mavenanalytics.io/data-playground

Kemudian, dataset yang ada dipindahkan ke *google drive* pribadi dengan link [Dataset - Maven Toys Data](https://drive.google.com/drive/folders/1_50O0bQu7rOwxHW6bDMtif9nvGw3W4Jt?usp=sharing)

*Table* yang diperlukan di *folder google drive* tersebut dipanggil menggunakan perintah

```
# data_variable = pd.read_csv('data location')
```

Terdapat sekitar 6 *table* yang dipanggil

"""

# Memanggil setiap table yang ada

calendar = pd.read_csv('/content/drive/MyDrive/dataset/Maven Toys Data/calendar.csv')
data_dict = pd.read_csv('/content/drive/MyDrive/dataset/Maven Toys Data/data_dictionary.csv')
inventory = pd.read_csv('/content/drive/MyDrive/dataset/Maven Toys Data/inventory.csv')
products = pd.read_csv('/content/drive/MyDrive/dataset/Maven Toys Data/products.csv')
sales = pd.read_csv('/content/drive/MyDrive/dataset/Maven Toys Data/sales.csv')
stores = pd.read_csv('/content/drive/MyDrive/dataset/Maven Toys Data/stores.csv')

"""## Join Table

Dikarenakan *table* yang ada dipisah-pisah, oleh karena itu dilakukan *join* untuk menggabungkan semua data menjadi 1 table

Terdapat beberapa metode untuk join table
1. Menggunakan `.join`
2. Menggunakan `.concat`
3. Menggunakan `.merge`

Pada kesempatan ini, data digabungkan menggunakan metode `.merge` dengan menerapkan metode `inner join`.

`inner join` merupakan metode penggabungan *table* dengan mengambil kolom *primary key table* pertama dan *foreign key table* kedua

Terdapat beberapa kali penggabungan sehingga menjadi 1 table

"""

# Menggabungkan table products dan sales
products_sales = pd.merge(products, sales, how='inner', on='Product_ID')

# Menggabungkan table (products dan sales) dan stores
products_sales_stores = pd.merge(products_sales, stores, how='inner', on='Store_ID')

# Menggabungkan table (products, sales, dan stores) dan inventory
toys_data = pd.merge(products_sales_stores, inventory, how='inner', on=['Store_ID', 'Product_ID'])

"""## Data Preview

> Data dilakukan `.copy` yang bertujuan agar data awal tidak dilakukan perubahan

Berdasarkan data yang ada, dilakukan *preview* untuk mengetahui gambaran besar data tersebut

Adapun preview yang dilakukan dengan beberapa metode, yaitu:
1. Menggunakan `.info` untuk mengecek nama kolom, jumlah baris, dan jenis tipe data setiap *value* kolom
2. Menggunakan `.isna.sum()` untuk mengecek jumlah data *null* pada setiap kolom
3. Menggunakan `.describe` baik untuk analisis statistikan data *countable* dan data *object* / *uncountable*
4. Menggunakan `.head` untuk melihat beberapa data paling atas


"""

# Melalukan copy untuk menjaga data yang asli
data_frame = toys_data.copy()

# Mengecek gambaran besar table (nama kolom, jumlah baris, dan tipe data kolom)
data_frame.info()

# Mengecek jumlah data null
data_frame.isna().sum()

# Mengecek hasil statistik dari kolom countable
data_frame.describe()

# Mengecek hasil statistik dari kolom uncountable
data_frame.describe(include=['object'])

# Mengecek 5 data teratas
data_frame.head()

"""Berdasarkan data preview yang dilakukan terdapat beberapa penemuan, yaitu:
1. Mainan yang paling banyak dibeli yaitu color buds dengan total penjualan sebanyak 72.988
2. Terdapat 45 jenis mainan
3. Terdapat 5 kategori mainan
4. Terdapat 50 toko mainan di Mexico
5. Maven Toys Ciudad de Mexico 2 merupakan toko paling populer dengan 28.497 pengunjung
6. 50 toko mainan tersebut, tersebar di 29 kota

## Data Cleaning & Data Manipulation

Data Cleaning untuk membersihkan data yang kurang lengkap, data yang salah, dll.

Data Manipulation untuk mengubah, memodifikasi data, atau memformat data agar data dapat lebih mudah untuk dipahami atau digunakan
"""

data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%Y-%m-%d')

"""### 1. Melakukan perhitungan untuk *Total Sales*

> `Total_Sales` diperoleh dengan penjumlahan `Product_Price` dengan `Units`

Berdasarkan *data preview* yang telah dilakukan, dapat diketahui bahwa tipe data `Product_Price` adalah *object*. Oleh karena itu tipe data `Product_Price` harus diubah antara `float` ataupun `integer` untuk memudahkan operasi matematika.


Karena *value* `Product_Price` tidak bulat, maka dari itu tipe data `Product_Price` akan diganti menjadi `float`.


Namun tipe data `Product_Price` tidak dapat langsung diubah, karena terdapat simbol **'&'**. Oleh karena itu, dilakukan metode `.split` untuk memisahkan simbol **'&'** dengan angka `Product Price`


"""

# Memisahkan simbol $ dengan angka harga
# Memisahkan dan membuat kolom baru
data_frame[['Product_Price_Symbol', 'Product_Price_Number']] = (
    data_frame['Product_Price'].str.split('$', expand=True))

# Mengubah tipe data kolom Product_Price_Number menjadi float
data_frame['Product_Price_Number'] = data_frame['Product_Price_Number'].astype('float')

# Melakukan operasi untuk menghitung total penjualan dari setiap produk
data_frame['Total_Sales'] = data_frame['Product_Price_Number'] * data_frame['Units']

# Untuk melihat isi data_frame setelah melakukan proses penjumlahan Total_Sales
data_frame.head()

"""### 2. Melakukan Perhitungan Keuntungan / *Profit*

> `Profit` diperoleh dengan pengurangan `Product_Price` dengan `Product_Cost`


> `Profit_Percentage` diperoleh dengan pembagian `Profit` dengan `Product_Cost`


Sama halnya dengan cara melakukan perhitungan `Total_Sales`, perhitungan `Profit` memiliki masalah yang sama.

Berdasarkan *data preview* yang telah dilakukan, dapat diketahui bahwa tipe data `Product_Cost` adalah *object*. Oleh karena itu tipe data `Product_Cost` harus diubah antara `float` ataupun `integer` untuk memudahkan operasi matematika.


Karena *value* `Product_Cost` tidak bulat, maka dari itu tipe data `Product_Cost` akan diganti menjadi `float`.


Namun tipe data `Product_Cost` tidak dapat langsung diubah, karena terdapat simbol **'&'**. Oleh karena itu, dilakukan metode `.split` untuk memisahkan simbol **'&'** dengan angka `Product Cost`
"""

# Memisahkan simbol $ dengan angka product_cost
# Memisahkan dan membuat kolom baru
data_frame[['Product_Cost_Symbol', 'Product_Cost_Number']] = (
    data_frame['Product_Cost'].str.split('$', expand=True))

# Mengubah tipe data kolom Product_Cost_Number menjadi float
data_frame['Product_Cost_Number'] = data_frame['Product_Cost_Number'].astype('float')

# Melakukan operasi untuk menghitung keuntungan setiap penjualan produk
data_frame['Profit'] = data_frame['Total_Sales'] - data_frame['Product_Cost_Number']

# Melakukan operasi untuk melakukan persentase keuntungan setiap penjualan produk
data_frame['Profit_Percentage'] = round(
      data_frame['Profit'] / data_frame['Product_Cost_Number'] * 100, 2
    )

# Untuk melihat isi data_frame setelah melakukan proses perhitungan Profit
data_frame.head()

"""### 3. Melakukan Perhitungan Kerugian / Loss

Perhitungan kerugian dimaksudkan untuk melihat apakah ada kerugian (nilai minus ' - ') yang terdapat dalam `data_frame`
"""

# Melihat data rugi
df_rugi = data_frame['Profit'] < 0

print(df_rugi)

"""## *Data Sorting*

*Data sorting* bertujuan untuk melihat data yang diurutkan mulai dari terkecil maupun terbesar

Pada kesempatan ini terdapat beberapa kolom yang dilakukan *data sorting*, yaitu:
1. `Product_Category`
2. `Product_Name`
3. `Store_City`
4. `Store_Name`
5. `Store_Location`
6. `.nlargest` untuk `Total_Sales` dan `Profit`
7. `.nsmallest` untuk `Total_Sales` dan `Profit`
8. `Max` untuk `Total_Sales` dan `Profit`
9. `Min` untuk `Total_Sales` dan `Profit`
10. `Mean` untuk `Total_Sales` dan `Profit`
"""

# Menghitung jumlah tiap kategori
data_frame['Product_Category'].value_counts()

# Menghitung jumlah tiap produk
data_frame['Product_Name'].value_counts()

# Menghitung jumlah penjualan tiap kota
data_frame['Store_City'].value_counts()

# Menghitung jumlah penjualan tiap toko
data_frame['Store_Name'].value_counts()

# Menghitung jumlah penjualan tiap lokasi
data_frame['Store_Location'].value_counts()

# Melihat data penjualan tertinggi
data_frame.nlargest(5, 'Total_Sales')

# Melihat data penjualan terendah
data_frame.nsmallest(5, 'Total_Sales')

# Melihat profit tertinggi
data_frame.nlargest(5, 'Profit')

# Melihat profit terendah
data_frame.nsmallest(5, 'Profit')

# Melihat penjualan tertinggi
data_frame['Total_Sales'].max()

# Melihat penjualan terendah
data_frame['Total_Sales'].min()

# Melihat rata-rata penjualan
data_frame['Total_Sales'].mean()

# Melihat profit tertinggi
data_frame['Profit'].max()

# Melihat profit terendah
data_frame['Profit'].min()

# Melihat rata-rata profit
data_frame['Profit'].mean()

data_frame.head()

"""## Pivot Table

Pivot table berfungsi untuk melakukan analisis data, mengelompokkan data, dan meringkas data
"""

pd.pivot_table(
    data=data_frame,
    index=['Product_Category'],
    values='Total_Sales',
    columns='Store_Location',
    aggfunc=['sum', 'count', 'mean'],
    margins=True,
    margins_name='Total'
)

data_frame.Date = data_frame.Date.dt.strftime('%Y-%m')

pd.pivot_table(
    data=data_frame,
    index=['Date'],
    values='Total_Sales',
    columns='Product_Category',
    aggfunc=['sum', 'count', 'mean'],
    margins=True,
    margins_name='Total'
)

"""## Data Visualisation"""

plt.figure(figsize=(15, 5))
sns.barplot(
    data=data_frame,
    x='Store_Location',
    y='Product_Category'
)
plt.xlabel('Store Location')
# plt.xticks(data_jml_flights['month'].unique())
plt.ylabel('Product Category')
plt.title("Jumlah Penjualan Produk Untuk Setiap Kategori Berdasarkan Lokasi")
plt.grid()
plt.show()

"""## Export Data

Export data berfungsi untuk menyimpan data yang sudah dilakukan *cleaning* dan modifikasi

### Pemisahan Column

Dikarenakan data yang besar, maka data akan dipisah sesuai dengan kategorinya

Terdapat 4 kategori, yaitu:
1. `Producs`
2. `Stores`
3. `Sales`
4. `Inventory`
"""

df_product = data_frame[['Product_ID', 'Product_Name', 'Product_Category', 'Product_Cost', 'Product_Price', 'Product_Cost_Number', 'Product_Price_Number']]

df_sales = data_frame[['Sale_ID', 'Date', 'Store_ID', 'Product_ID', 'Units', 'Total_Sales', 'Profit', 'Profit_Percentage']]

df_store = data_frame[['Store_ID', 'Store_Name', 'Store_City', 'Store_Location', 'Store_Open_Date']]

df_inventory = data_frame[['Store_ID', 'Product_ID', 'Stock_On_Hand']]

"""## Metode Penyimpanan

Metode penyimpanan yang dapat digunakan, yaitu:
1. Menyimpan ke *google cloud drive*
2. Menyimpan ke *device*

### 1. Menyimpan data ke *Google Cloud Drive*
"""

df_product.to_csv(
    'df_product',
    encoding='utf-8',
    index=False)

"""### 2. Menyimpan data ke *Device*"""

# Menyimpan data product
from google.colab import files
df_product.to_csv('df_product.csv',encoding='utf-8', index=False)
files.download('df_product.csv')

# Menyimpan data sales
from google.colab import files
df_sales.to_csv('df_sales.csv',encoding='utf-8', index=False)
files.download('df_sales.csv')

# Menyimpan data store
from google.colab import files
df_store.to_csv('df_store.csv',encoding='utf-8', index=False)
files.download('df_store.csv')

from google.colab import files
df_inventory.to_csv('df_inventory.csv',encoding='utf-8', index=False)
files.download('df_inventory.csv')