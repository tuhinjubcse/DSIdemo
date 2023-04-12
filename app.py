from flask import Flask, render_template, request
import random
import os
import json
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
	concept=''
	if request.method == 'POST':
		user_input = request.form.get('input_text')
		concept=user_input
		generated_texts = generate_texts(user_input)
		return render_template('index.html', generated_texts=generated_texts,concept=concept)
	
	return render_template('index.html',concept=concept)

def generate_texts(input_text):
	completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "You are a creative assistant"}, {"role": "user", "content": "Generate 5 metaphors given the topic:"+input_text}])
	response = completion['choices'][0]['message']['content']
	prefixes = response.split('\n')
	print(prefixes)
	p = []
	for pref in prefixes:
		if len(pref)>0 and '. ' in pref:
			p.append(pref.split('.')[1].replace('"',''))
	return p

@app.route('/generate_images', methods=['POST'])
def generate_images():
	metaphor = request.form.get('selected_text')
	with open("./viselab.txt", "r") as f:
		viselabprompt = f.read().strip()
	completion = openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "system", "content": "You are a creative assistant"}, 
		{"role": "user", "content": viselabprompt+metaphor}])
	viselab = completion['choices'][0]['message']['content'].split("Visual Elaboration: ")[1].lower()
	viselab = "An illustration of"+viselab
	response = openai.Image.create(prompt=viselab,n=4,size="256x256")
	print(response['data'])
	image_url = [response['data'][0]['url'],response['data'][1]['url'],response['data'][2]['url'],response['data'][3]['url']]
	return json.dumps(image_url)
if __name__ == '__main__':
    app.run(debug=True)