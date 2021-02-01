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

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls')  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

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

def isfbs(amount):
	if (amount > 120):
		return(1)
	else: 
		return(0)

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

def log_in():
	#Inisialisasi variabel
	valid = 0
	#Fungsi
	clear()
	print("------------------------------------\n----------- WARAS+:LOGIN -----------\n------------------------------------\n")
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

def menu():
	#Inisialisasi variabel
	valid = 0
	#Fungsi
	clear()
	print("------------------------------------\n-------- WARAS+: MAIN MENU ---------\n------------------------------------\n")
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
	print("Keterangan:\nBMI: underweight (<18.5); normal (18.5-25); obesitas (25-30); obesitas ekstrim (>30)\nCholesterol: normal (<200); sedang (200-239); tinggi (>239)")
	print("Tekanan Darah (Sistol): rendah (<90); normal (90-120); sedang (120-140); tinggi (>140)\nGula Darah: normal (<100); sedang (100-140); tinggi (>140)\n")

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
		input_data = input("\nMasukkan ID / Nama Lengkap: ").lower()
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

def cekData_update():
	#Inisiasi Variabel
	valid = 0
	valid2 = 0
	#Fungsi
	while (valid == 0):
		clear()
		print("\nUPDATE DATA KESEHATAN\n_________________________________\n\nMasukkan Data: \n")
		#Update Data (Sesuaikan dengan data apa saja yang akan diinput)
		bulan_upd = int(today.strftime("%m"))
		tahun_upd = int(today.strftime("%Y"))
		#Input data
		name_upd = input("Nama Lengkap: ").lower()
		hasil = data.loc[data['Nama'] == name_upd]

		if ((hasil.empty == True)): #Nama tidak ada di database
			in_menu = int(input("Nama tidak ditemukan. Buat baru?   0. Ya 	1. Tidak\nPilihan: ")) 
			while (valid2 == 0):
				if (in_menu == 0): #Pembuatan data anggota baru
					clear()
					print("\nUPDATE DATA KESEHATAN\n_________________________________\n\nPembuatan Data Baru\n")
					print("Nama Lengkap: %s" % (name_upd))
					#Input data baru
					print(type(data["ID"].max()))
					print(data["ID"].max())
					id_upd = data["ID"].max() + 1
					print(id_upd)
					age_upd = int(input("Umur: "))
					glucose_upd = int(input("Gula Darah: "))
					bmi_upd = int(input("BMI: "))
					sbp_upd = int(input("Tekanan Darah Sistole: "))
					dbp_upd = int(input("Tekanan Darah Diastole: "))
					chol_upd = int(input("Total Cholesterol: "))
					cp_upd = int(input("Chest Pain Level (chest pain type (1-typical angina; 2-atypical angina\n3-non-anginal pain; 4-asymptomatic): "))
					fbs_upd = isfbs(glucose_upd)
					levBMI_upd = isLevelBMI(bmi_upd)
					levChol_upd = isLevelChol(chol_upd)
					levbp_upd = isLevelBP(sbp_upd)
					levGluc_upd = isLevelGlucose(glucose_upd)
					#Input selesai
					new_data = {'ID':[id_upd],'Nama': [name_upd],'Bulan': [bulan_upd],'Tahun':[tahun_upd],'glucose':[glucose_upd],'Age':[age_upd],
						'BMI':[bmi_upd],'dbp':[dbp_upd],'sbp':[sbp_upd],'chol':[chol_upd],'fbs':[fbs_upd],'cp':[cp_upd],'Level BMI':[levBMI_upd],
						'Level Cholesterol':[levChol_upd],'Level Tekanan Darah':[levGluc_upd],'Level Gula Darah':[levGluc_upd]}
					df_new_data = pd.DataFrame(new_data)
					df_new_data.to_csv(filename, mode='a', header=False, index=False)
					print("\nData berhasil disimpan!")
					valid2 = 1
				elif (in_menu == 1): #Tidak ingin menambahkan data
					valid2 = 1
				else:
					in_menu = int(input("Pilihan salah! Coba lagi: "))
		else: #Update data dari anggota terdaftar
			id_upd = hasil["ID"].max()
			age_upd = hasil["Age"].max()
			glucose_upd = int(input("Gula Darah: "))
			bmi_upd = int(input("BMI: "))
			sbp_upd = int(input("Tekanan Darah Sistole: "))
			dbp_upd = int(input("Tekanan Darah Diastole: "))
			chol_upd = int(input("Total Cholesterol: "))
			cp_upd = int(input("Chest Pain Level (chest pain type (1-typical angina; 2-atypical angina\n3-non-anginal pain; 4-asymptomatic): "))
			fbs_upd = isfbs(glucose_upd)
			levBMI_upd = isLevelBMI(bmi_upd)
			levChol_upd = isLevelChol(chol_upd)
			levbp_upd = isLevelBP(sbp_upd)
			levGluc_upd = isLevelGlucose(glucose_upd)
			
			new_data = {'ID':[id_upd],'Nama': [name_upd],'Bulan': [bulan_upd],'Tahun':[tahun_upd],'glucose':[glucose_upd],'Age':[age_upd],
						'BMI':[bmi_upd],'dbp':[dbp_upd],'sbp':[sbp_upd],'chol':[chol_upd],'fbs':[fbs_upd],'cp':[cp_upd],'Level BMI':[levBMI_upd],
						'Level Cholesterol':[levChol_upd],'Level Tekanan Darah':[levGluc_upd],'Level Gula Darah':[levGluc_upd]}
			df_new_data = pd.DataFrame(new_data)
			df_new_data.to_csv(filename, mode='a', header=False, index=False)
			print("\nData berhasil disimpan!")
			#Pilihan
		valid = int(input("\nLanjutkan Update Data?   0. Ya 	1. Tidak\nPilihan: "))
		while ((valid != 0) and (valid != 1)):
			valid = int(input("Pilihan tidak valid! Masukkan kembali pilihan Anda: "))
	return()

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

#Logout
clear()
print("Terima Kasih\nTetap Jaga Kesehatan Bersama\n--- WARAS+ ---\n")


