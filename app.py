from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import requests
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hola'

#url_request1 = r"http://131.175.120.2:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c"
#url_request2 = r"C:\Users\leugi\Documents\TFM\Python\Prototipo4\static\new_batch_2.csv"
#url_request3 = requests.get("https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1", headers={'User-Agent': 'Mozilla/5.0'})
#df = pd.read_csv(url_request1, error_bad_lines=False, index_col=False)
#url_request31 = io.StringIO(url_request3.content.decode('utf-8'))
#df = pd.read_csv(url_request31, error_bad_lines=False, index_col=False)

urls = []
##change len(df) to 100
#for x in range(len(df)):
#    u = {"url": df['media_url'].iloc[x]}
#    urls.append(u)


    
applied = []
source_applied = []
count = 0
number_images= 100
s0 = {'ID': "", 'source': "", 'keywords': "", 'url': ""}
source_applied.append(s0)

@app.route('/', methods=['GET','POST'])
def index():
    global count, applied, source_applied, number_images, urls
    if request.method == "POST":
        if 'source_button' in request.form:
            if count == 0:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
                url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                s = {'ID': count, 'source': option, 'keywords': keywords, 'url': url_csv}
                source_applied[0]= s
                f = {'ID': "", 'Filter': "", 'Attribute': "", 'url': ""}
                applied.append(f)
                
                url_csv_get = requests.get(url_csv)
                url_request = io.StringIO(url_csv_get.content.decode('utf-8'))
                df = pd.read_csv(url_request, error_bad_lines=False, index_col=False)
                u = []
                for x in range(len(df)):
                    p = {"url": df['media_url'].iloc[x]}
                    u.append(p)
                urls.append(u)
                    
                count+=1
                
            else:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
                url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                s = {'ID': count, 'source': option, 'keywords': keywords, 'url': url_csv}
                source_applied[0]= s
                
                url_csv_get = requests.get(url_csv)
                url_request = io.StringIO(url_csv_get.content.decode('utf-8'))
                df = pd.read_csv(url_request, error_bad_lines=False, index_col=False)
                u = []
                for x in range(len(df)):
                    p = {"url": df['media_url'].iloc[x]}
                    u.append(p)
                urls[0]= u                
                
                
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
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    url_csv = r"http://131.175.120.2:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c"
                    f = {'ID': count, 'Filter': Filter, 'Attribute': attribute, 'url': url_csv}
                    k = {'ID': "", 'Filter': "", 'Attribute': "", 'url': ""}
                    applied[count-1] = f
                    applied.append(k)
                    
                    #url_csv_get = requests.get(url_csv)
                    #url_request = io.StringIO(url_csv_get.content.decode('utf-8'))
                    df = pd.read_csv(url_csv, error_bad_lines=False, index_col=False)
                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x]}
                        u.append(p)
                    urls.append(u)                    
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
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    url_csv = r"http://131.175.120.2:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c"
                    f = {'ID': count, 'Filter': Filter, 'Attribute': attribute, 'url': url_csv}
                    applied[sel_count-1] = f
                    
                    #url_csv_get = requests.get(url_csv)
                    #url_request = io.StringIO(url_csv_get.content.decode('utf-8'))
                    df = pd.read_csv(url_csv, error_bad_lines=False, index_col=False)
                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x]}
                        u.append(p)
                    urls[count]= u                     
                    
                else:
                    flash('Select an option')
                    applied[sel_count-1]['Filter'] = ""
        elif 'reset_button' in request.form:
            count = 0
            source_applied = []
            s0 = {'ID': "", 'source': "", 'keywords': "", 'url': ""}
            source_applied.append(s0)
            applied = []
        elif 'up_button' in request.form:
            a = applied[int(request.form['up_button'])-2]
            applied[int(request.form['up_button'])-2] = applied[int(request.form['up_button'])-1]
            applied[int(request.form['up_button'])-1] = a
        else:
            url_download = int(request.form['download_button'])
            return redirect(applied[url_download-1]["url"])
            #print(applied[url_download-1]["url"])
            #print(applied)
            #print(url_download)
            #pass
    return render_template('index.html', count=count, source_applied=source_applied, urls=urls,
                           applied=applied, number_images=number_images)

if __name__ == '__main__':
    app.run(debug=True)

