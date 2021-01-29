#Program Waras+
#Made by: Sarah Alyaa

# Load libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.utils import check_array
from sklearn.tree._tree import DTYPE
from os import system, name 

# Load time
from datetime import date
today = date.today()

#Load Database
col_names = ['pregnant', 'glucose', 'bp', 'skin', 'insulin', 'bmi', 'pedigree', 'age', 'label']
data = pd.read_csv("database.csv", header=None, names=col_names).apply(lambda x: x.astype(str).str.lower())

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls')  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

# Fungsi get_node untuk mengambil suatu node dari dataset
def get_node(X):
    return clf.tree_.apply(check_array(X, dtype=DTYPE))

def menu():
	#Inisialisasi variabel
	valid = 0
	#Fungsi
	clear()
	in_menu = int(input("Pilih menu:\n1. Data Kesehatan\n2. Info Gizi\n3. Log Out\n Pilihan: "))
	while (valid == 0):
		if (in_menu > 0 and in_menu <= 3):
			valid = 1
		else:
			in_menu = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return (in_menu)

def menu_cekData():
	#Inisialisasi variabel
	valid = 0
	#Fungsi
	clear()
	curr_month_year = today.strftime("%B %Y")
	print("Data Kesehatan Terbaru (Update: %s)" % (curr_month_year))
	idx = data.groupby(['nama','tahun'])['bulan'].transform(max) == data['bulan']
	idy = data[idx].groupby(['nama'])['tahun'].transform(max) == data[idx]['tahun']
	print(data[idx][idy])
	print("\nCatatan: Data lengkap dapat dicek pada data Individu\n")
	
	in_menu = int(input("Pilih fitur:\n1. Data Individu\n2. Update Data\n3. Kembali\nPilihan: "))
	while (valid == 0):
		if (in_menu > 0 and in_menu <= 3):
			valid = 1
		else:
			in_menu = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return (in_menu)

def cekData_search():
	#Inisialisasi variabel
	in_menu = 0
	#Fungsi
	clear()
	while (in_menu != 3):
		print("\nPENCARIAN DATA\n___________________________")
		in_menu = int(input("\nCari Data Berdasarkan: \n1. ID; \n2. Nama Lengkap\n3. Kembali\nPilihan: "))
		while ((in_menu < 1) and (valid > 3)):
			valid = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
		if (in_menu == 1):
			cekData_searchID()			
		elif (in_menu == 2):
			cekData_searchNamaLengkap()
	return()

def cekData_searchID():
	#Inisialisasi variabel
	valid = 0
	#Fungsi
	while (valid == 0):
		clear()
		print("\nPENCARIAN DATA BERDASARKAN ID\n")
		inputID = input("\nMasukkan ID: ")
		hasil = data.loc[data["id"] == inputID]
		# Menampilkan data
		if (hasil.empty == True):
			print("Data tidak ditemukan.")
		else:
			print(hasil.sort_values(by = ["tahun","bulan"],ascending=False))
		# Melanjutkan Pencarian
		valid = int(input("\nLanjutkan Pencarian?   0. Ya 	1. Tidak\n\nPilihan: "))
		while ((valid != 0) and (valid != 1)):
			valid = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return()


def cekData_searchNama():
	#Inisialisasi variabel
	valid = 0
	#Fungsi
	while (valid == 0):
		clear()
		print("\nPENCARIAN DATA BERDASARKAN NAMA LENGKAP\n___________________________")
		inputNama = input("\nMasukkan Nama Lengkap (non-kapital): ")
		hasil = data.loc[data["nama"] == inputNama]
		# Menampilkan data
		if (hasil.empty == True):
			print("Data tidak ditemukan.")
		else:
			print("Laporan Kesehatan %s\n" % (inputNama))
			print(hasil.sort_values(by = ["tahun","bulan"],ascending=False).head(10))
		# Melanjutkan Pencarian
		valid = int(input("\nLanjutkan Pencarian?   0. Ya 	1. Tidak\n\nPilihan: "))
		while ((valid != 0) and (valid != 1)):
			valid = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return()

def cekData_update():
	#Inisiasi Variabel
	valid = 0
	#Fungsi
	while (valid == 0):
	clear()
	print("\nUPDATE DATA KESEHATAN\n___________________________\nMasukkan Data: \n")
	#Update Data (Sesuaikan dengan data apa saja yang akan diinput)
	id_upd = input("No. ID: ")
	name_upd = input("Nama Lengkap: ")
	bulan_upd = int(today.strftime("%m"))
	tahun_upd = int(today.strftime("%Y"))
	angka_upd = input("Angka: ")
	new_data = {'id': [ide_upd], 'nama':[name_upd], 'bulan':[bulan_upd], 'tahun':[tahun_upd], 'angka':[angka_upd]}
	df_new_data = pd.DataFrame(new_data)
	# data = data.append(new_upd, ignore_index=True)
	df_new_data.to_csv('database.csv', mode='a', header=False, index=False)
	print("\nData berhasil disimpan!\n")
	#Pilihan
	valid = int(input("Lanjutkan Update Data?   0. Ya 	1. Tidak\nPilihan: "))
	while ((valid != 0) and (valid != 1)):
		valid = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return()

def DTpredict():
	# load dataset
	data = pd.read_csv("PimaIndiansdata.csv", header=0) #header 0 = if there is column name on the first row

	# split dataset in features and target variable
	feature_cols = ['insulin', 'bmi','age','glucose','bp','pedigree']
	X = data[feature_cols] # Features -> independent variables
	y = data.label # Target variable -> dependant variables

	# Split dataset into training set and test set
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test

	# Create Decision Tree 
	clf = DecisionTreeClassifier(criterion="entropy", max_depth=5)
	clf = clf.fit(X_train,y_train)

	#Predict the response for test dataset
	data_test = {'insulin': [insulin_test], 'bmi':[bmi_test], 'age':[age_test], 'glucose':[glucose_test], 'bp':[bp_test], 'pedigree':[pedigree_test]}
	df_data_test = pd.DataFrame(data_test)
	y_pred = clf.predict(X_test)
	y_pred_test = clf.predict(df_data_test)
	i = 0
	j = 1
	for j in range(1,51):
		node_idx = get_node(X_test[i:j])
		y_pred_prob = y_train[get_node(X_train) == node_idx].mean()
		print ("Actual: %s. Predicted: %s. Possibility: %s" % (y_test.iloc[i], y_pred[i], y_pred_prob))
		i = j

	# Model Accuracy, how often is the classifier correct?
	print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


def menu_cekGizi():
	#Inisialisasi variabel
	valid = 0

	#Fungsi
	menu = int(input("Pilih fitur:\n1. Rekomendasi menu\n2. Pantangan Konsumsi\n3. Kembali\n Pilihan: "))
	while (valid == 0):
		if (in_menu > 0 and in_menu <= 3):
			valid = 1
		else:
			in_menu = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return (in_menu)


# Main Program
# Inisialisasi
in_menu = 0
in_menuCekData = 0
in_menuCekGizi = 0

#After Login
login = log_in()
while (login == 1):
	in_menu = menu()
	if (in_menu == 1): #Cek Data
		while (in_menuCekData != 3):
			in_menuCekData = menu_cekData()
			if (in_menuCekData == 1): #Cek Data Individu
				cekData_search() 
			elif (in_menuCekData == 2): #Update Data
				cekData_update()
	elif (in_menu == 2): #Cek Gizi
		while (in_menuCekGizi != 3):
			in_menuCekGizi = menu_cekGizi()
			if (in_menuCekGizi == 1): #Rekomendasi Menu
				print("Rekomendasi menu")
			elif (in_menuCekGizi == 2): #Pantangan
				print("Pantangan")
	elif (in_menu == 3):
		login = 0
log_out()











