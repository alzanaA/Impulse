#Program Waras+

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
data = pd.read_csv("test2.csv", header=0)
filename = "test2.csv"
data_diabetes = pd.read_csv("PimaIndiansdata.csv", header=0)
data_heart = pd.read_csv("heart.csv", header=0)
data_user = pd.read_csv("user.csv",header=0)
data['Nama'] = data['Nama'].str.lower()

def log_in():
	#Inisialisasi variabel
	valid = 0
	#Fungsi
	clear()
	print("\nLOGIN\n___________________________")
	while (valid == 0):
		input_user = input("\nMasukkan Username: ")
		input_pass = input("\nMasukkan Password: ")
		hasil = data_user.loc[data_user['username'] == input_user]
		if ((hasil.empty == True) or (hasil.values[0][1] != input_pass)):
			clear()
			print("\nLOGIN\n___________________________\n")
			print("Username/Password Salah! Coba Lagi.\n")
		else:
			valid = 1
	return(valid)

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls')  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def DTpredict(data_target,predict_target):
	# load dataset
	if (predict_target == 'Diabetes'):
		data = data_diabetes
		feature_cols = ['glucose', 'BMI', 'Age','dbp']
	elif (predict_target == 'Penyakit Jantung'):
		data = data_heart
		feature_cols = ['Age','sbp','chol','fbs','cp']
		#cp: chest pain type (1-typical angina; 2-atypical angina 3-non-anginal pain; 4-asymptomatic)
		#fbs: fasting blood sugar > 120 mg/dl (1 = true; 0 = false) 

	# split dataset in features and target variable
	X = data[feature_cols] # Features -> independent variables
	y = data.label # Target variable -> dependant variables

	# Split dataset into training set and test set
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1) # 70% training and 30% test
	test_data = data_target.head(1)[feature_cols]

	# Create Decision Tree 
	clf = DecisionTreeClassifier(criterion="entropy", max_depth=3)
	clf = clf.fit(X_train,y_train)

	#Predict the response for test dataset
	y_pred = clf.predict(X_test)
	y_pred_test = clf.predict(test_data)	
	node_idx = clf.tree_.apply(check_array(test_data, dtype=DTYPE))
	y_pred_prob = y_train[clf.tree_.apply(check_array(X_train, dtype=DTYPE)) == node_idx].mean()
	accuracy = metrics.accuracy_score(y_test, y_pred)

	#Showing the result
	category_target = ""
	probabilty_target = y_pred_prob * accuracy * 100
	if (probabilty_target <= 15):
		category_target = "Sangat Rendah"
	elif (probabilty_target > 15 and probabilty_target <= 25):
		category_target = "Rendah"
	elif (probabilty_target > 25 and probabilty_target <= 35):
		category_target = "Cukup Rendah"
	elif (probabilty_target > 35 and probabilty_target <= 45):
		category_target = "Sedang"
	elif (probabilty_target > 45 and probabilty_target <= 60):
		category_target = "Cukup Tinggi"
	elif (probabilty_target > 60):
		category_target = "Tinggi"

	print("Kemungkinan Mengidap %s: " % (predict_target),end="") 
	print ('%s (' % (category_target) + '%.2f' % (y_pred_prob * accuracy * 100) + '%)') 

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
	print("\t\tData Kesehatan Terbaru \n\t(terakhir diperbaharui: %s)\n__________________________________________________\n" % (curr_month_year))
	idx = data.groupby(['Nama','Tahun'])['Bulan'].transform(max) == data['Bulan']
	idy = data[idx].groupby(['Nama'])['Tahun'].transform(max) == data[idx]['Tahun']
	print(data[idx][idy][['ID','Nama','Level BMI','Level Cholesterol','Level Tekanan Darah',
		'Level Gula Darah','Tahun','Bulan']].sort_values(by = ['ID']).to_string(index=False))
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
	valid = 0
	#Fungsi
	while (valid == 0):
		clear()
		print("\nPENCARIAN DATA\n__________________________________________________")
		input_data = input("\nMasukkan ID / Nama Lengkap: ")
		if (input_data.isnumeric()):
			attribute = "ID"
			input_data = int(input_data)
		else:
			attribute = "Nama"
		hasil = data.loc[data[attribute] == input_data].sort_values(by = ["Tahun","Bulan"],ascending=False).head()
		
		# Menampilkan data
		if (hasil.empty == True):
			print("Data tidak ditemukan.")
		else:
			print('__________________________________________________\n')
			print(hasil.loc[:, 'Bulan':'cp'].to_string(index=False))
			print('\n__________________________________________________\n')
			print("\nLevel Pengukuran Terbaru: \n")
			print(hasil.loc[:, 'Level BMI':'Level Gula Darah'].head(1).T.to_string(header=False)) 
			print('\n__________________________________________________\n')
			print("\nPrediksi Penyakit Terbaru: \n")
			DTpredict(hasil,'Diabetes')
			DTpredict(hasil,'Penyakit Jantung')
			print('\n__________________________________________________\n')

		# Melanjutkan Pencarian
		valid = int(input("\nLanjutkan Pencarian?   0. Ya 	1. Tidak\n\nPilihan: "))
		while ((valid != 0) and (valid != 1)):
			valid = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	clear()
	return()

# def cekData_update(filename):
# 	#Inisiasi Variabel
# 	valid = 0
# 	#Fungsi
# 	while (valid == 0):
# 		clear()
# 		print("\nUPDATE DATA KESEHATAN\n___________________________\nMasukkan Data: \n")
# 		#Update Data (Sesuaikan dengan data apa saja yang akan diinput)
# 		id_upd = input("No. ID: ")
# 		name_upd = input("Nama Lengkap: ")
# 		bulan_upd = int(today.strftime("%m"))
# 		tahun_upd = int(today.strftime("%Y"))
# 		angka_upd = input("Angka: ")
# 		new_data = {'id': [ide_upd], 'nama':[name_upd], 'bulan':[bulan_upd], 'tahun':[tahun_upd], 'angka':[angka_upd]}
# 		df_new_data = pd.DataFrame(new_data)
# 		# data = data.append(new_upd, ignore_index=True)
# 		df_new_data.to_csv(filename, mode='a', header=False, index=False)
# 		print("\nData berhasil disimpan!\n")
# 		#Pilihan
# 		valid = int(input("Lanjutkan Update Data?   0. Ya 	1. Tidak\nPilihan: "))
# 		while ((valid != 0) and (valid != 1)):
# 			valid = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
# 	return()

def menu_cekGizi():
	#Inisialisasi variabel
	valid = 0

	#Fungsi
	in_menu = int(input("Pilih fitur:\n1. Rekomendasi menu\n2. Pantangan Konsumsi\n3. Kembali\n Pilihan: "))
	while (valid == 0):
		if (in_menu > 0 and in_menu <= 3):
			valid = 1
		else:
			in_menu = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return (in_menu)

def isLevelChol(amount):
	level = ""
	if amount < 200:
		level = "Normal"
	elif (amount >= 200 and amount <= 239):
		level = "Sedang"
	else:
		level = "Tinggi"
	return (level)

def isLevelBP(amount):
	level = ""
	if amount < 90:
		level = "Rendah"
	if (amount >= 90 and amount < 120):
		level = "Normal"
	elif (amount >= 120 and amount <= 140):
		level = "Sedang"
	else:
		level = "Tinggi"
	return(level)

def isLevelGlucose(amount):
	level = ""
	if amount < 100:
		level = "Normal"
	elif (amount >= 100 and amount <= 125):
		level = "Sedang"
	else:
		level = "Tinggi"
	return (level)

def isLevelBMI(amount):
	level = ""
	if amount < 18.5:
		level = "Underweight"
	elif (amount >= 18.5 and amount < 25):
		level = "Normal"
	elif (amount >= 25 and amount < 30):
		level = "Obesitas"
	else:
		level = "Obesitas Ekstrim"
	return(level)


# Main Program
#Login
login = log_in()

#After Login
while (login == 1):

	#Inisialisasi Variabel
	in_menu = 0
	in_menuCekData = 0
	in_menuCekGizi = 0

	#Menu
	in_menu = menu()
	if (in_menu == 1): #Cek Data
		while (in_menuCekData != 3):
			in_menuCekData = menu_cekData()
			if (in_menuCekData == 1): #Cek Data Individu
				cekData_search() 
			elif (in_menuCekData == 2): #Update Data
				# cekData_update()
				print("On Progress.....")
	elif (in_menu == 2): #Cek Gizi
		while (in_menuCekGizi != 3):
			in_menuCekGizi = menu_cekGizi()
			if (in_menuCekGizi == 1): #Rekomendasi Menu
				print("Rekomendasi menu")
			elif (in_menuCekGizi == 2): #Pantangan
				print("Pantangan")
	elif (in_menu == 3):
		login = 0

#Logout
clear()
print("Terima Kasih\nTetap Jaga Kesehatan Bersama\n--- WARAS+ ---")


