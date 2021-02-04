import pandas as pd
import pandas as pd
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.utils import check_array
from sklearn.tree._tree import DTYPE
from os import system, name 
data = pd.read_csv("test2.csv", header=0)
data_heart = pd.read_csv("heart.csv", header=0)

print(data['cp'])

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

for i in range(len(data)):
	DTpredict(data.iloc[[i]],'Penyakit Jantung')

