import os
from flask import Flask, render_template,request
app = Flask(__name__)

from inference import get_flower_name,get_probability

@app.route('/',methods=['GET','POST'])
def hello_world():
	if request.method=='GET':
		return render_template('index.html')
	if request.method=='POST':
		file=request.files['file']
		image=file.read()
		flower_name=get_flower_name(image_bytes=image)
		probabilities=get_probability(image_bytes=image)
		return render_template('result.html',flower=flower_name,prob=probabilities)
		# try:
		# 	file=request.files['file']
		# 	image=file.read()
		# 	flower_name=get_flower_name(image_bytes=image)
		# 	return render_template('result.html',flower=flower_name)

			
		# except:
		# 	return render_template('index.html')
	#HAHAHAHAHAHA
#HHAHAHA
    

if __name__ == '__main__':
	app.run(debug=True)
	




				
		    
		    
		    