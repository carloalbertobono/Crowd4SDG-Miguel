from flask import Flask, render_template, request, flash
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hola'

df = pd.read_csv(r"C:\Users\leugi\Documents\TFM\Python\Prototipo4\static\new_batch_2.csv", 
                 error_bad_lines=False, index_col=False)
urls = []
##change len(df) to 100
for x in range(len(df)):
    u = {"url": df['media_url'].iloc[x]}
    urls.append(u)
    
applied = []
source_applied = []
count = 0
number_images= 1
s0 = {'ID': "", 'source': "", 'keywords': ""}
source_applied.append(s0)

@app.route('/', methods=['GET','POST'])
def index():
    global count, applied, source_applied, number_images
    if request.method == "POST":
        if 'source_button' in request.form:
            if count == 0:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
                s = {'ID': count, 'source': option, 'keywords': keywords}
                source_applied[0]= s
                f = {'ID': "", 'Filter': "", 'Attribute': ""}
                applied.append(f)
                count+=1
            else:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
                source_applied[0] = {'ID': 0, 'source': option,
                                     'keywords': keywords}
        elif 'apply_button' in request.form:
            if int(request.form['apply_button']) == count:
                if request.form['Filter_select'] != "--":
                    Filter = request.form['Filter_select']
                    if request.form['Filter_select'] == "Remove memes":
                        attribute = "None"
                    elif request.form['Filter_select'] == "Scene detector":
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == "Contains object":
                        attribute = request.form['option2_select']
                    else:
                        attribute = [request.form['latitude_text'], request.form['longitude_text']]
            
                    f = {'ID': count, 'Filter': Filter, 'Attribute': attribute}
                    k = {'ID': "", 'Filter': "", 'Attribute': ""}
                    applied[count-1] = f
                    applied.append(k)
                    count+=1
                else:
                    flash('Select an option')
                    applied[count-1]['Filter'] = ""
            else:
                sel_count = int(request.form['apply_button'])
                if request.form['Filter_select'] != "--":
                    Filter = request.form['Filter_select']
                    if request.form['Filter_select'] == "Remove memes":
                        attribute = "None"
                    elif request.form['Filter_select'] == "Scene detector":
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == "Contains object":
                        attribute = request.form['option2_select']
                    else:
                        attribute = [request.form['latitude_text'], request.form['longitude_text']]
            
                    f = {'ID': count, 'Filter': Filter, 'Attribute': attribute}
                    applied[sel_count-1] = f
                else:
                    flash('Select an option')
                    applied[sel_count-1]['Filter'] = ""
        elif 'reset_button' in request.form:
            count = 0
            source_applied = []
            s0 = {'ID': "", 'source': "", 'keywords': ""}
            source_applied.append(s0)
            applied = []
        elif 'up_button' in request.form:
            a = applied[int(request.form['up_button'])-2]
            applied[int(request.form['up_button'])-2] = applied[int(request.form['up_button'])-1]
            applied[int(request.form['up_button'])-1] = a
        else:
            pass
    return render_template('index.html', count=count, source_applied=source_applied, urls=urls,
                           applied=applied, number_images=number_images)

if __name__ == '__main__':
    app.run(debug=True)

