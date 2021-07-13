from flask import Flask, render_template, request, flash, redirect
import pandas as pd
import requests
from io import StringIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hola'

#url_test = r"http://131.175.120.2:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c"
#url_new_batch_computer = r"C:\Users\leugi\Documents\TFM\Python\Prototipo4\static\new_batch_2.csv"
#url_request_new_batch_drive = requests.get("https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1", headers={'User-Agent': 'Mozilla/5.0'})
#url_request_test2 = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/ETpS3YrdzspLjVs9TGF7JksBSVwPjpVWYKSdEAEqYEMW_w?Download=1"
#df = pd.read_csv(url_request1, error_bad_lines=False, index_col=False)
#url_request31 = io.StringIO(url_request3.content.decode('utf-8'))
#df = pd.read_csv(url_request31, error_bad_lines=False, index_col=False)

urls = []
##change len(df) to 100
#for x in range(len(df)):
#    u = {"url": df['media_url'].iloc[x]}
#    urls.append(u)


paths = []
applied = []
source_applied = []
count = 0
number_images= 100
confidence= 0.9
s0 = {'ID': "", 'source': "", 'keywords': ""}
source_applied.append(s0)

@app.route('/', methods=['GET','POST'])
def index():
    global count, applied, source_applied, number_images, urls, paths, confidence
    if request.method == "POST":
        if 'source_button' in request.form:
            if count == 0:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
                #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/ETUZnzuvqtlHv0iHyyOI0MYBO7O1yFXIqu0QPeIhHUJZnw?Download=1"
                #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/ETpS3YrdzspLjVs9TGF7JksBSVwPjpVWYKSdEAEqYEMW_w?Download=1"
                r = requests.post('http://131.175.120.2:7777/Crawler/API/CrawlCSV',
                                  json={'query': keywords,
                                        'count': number_images})                
                s = {'ID': count, 'source': option, 'keywords': keywords}
                source_applied[0]= s
                f = {'ID': "", 'Filter': "", 'Attribute': "", 'url': ""}
                applied.append(f)
                
                #url_csv_get = requests.get(url_csv)
                #url_request = StringIO(url_csv_get.content.decode('utf-8'))
                #df = pd.read_csv(url_request, error_bad_lines=False, index_col=False)
                #file = pd.DataFrame.to_csv(df, path_or_buf=(None))
                #print(df)
                
                tmp= StringIO(r.text)
                df= pd.read_csv(tmp)                
                
                u = []
                for x in range(len(df)):
                    p = {"url": df['media_url'].iloc[x]}
                    u.append(p)
                urls.append(u)
                #paths.append(url_csv_get.text)
                paths.append(r.text)
    
                count+=1
                
            else:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
                #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/ETUZnzuvqtlHv0iHyyOI0MYBO7O1yFXIqu0QPeIhHUJZnw?Download=1"
                #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/ETpS3YrdzspLjVs9TGF7JksBSVwPjpVWYKSdEAEqYEMW_w?Download=1"                
                r = requests.post('http://131.175.120.2:7777/Crawler/API/CrawlCSV',
                                  json={'query': keywords,
                                        'count': number_images})                
                s = {'ID': count, 'source': option, 'keywords': keywords}
                source_applied[0]= s
                
                #url_csv_get = requests.get(url_csv)
                #url_request = StringIO(url_csv_get.content.decode('utf-8'))
                #df = pd.read_csv(url_request, error_bad_lines=False, index_col=False)
                #file = pd.DataFrame.to_csv(df, path_or_buf=(None))
                
                tmp= StringIO(r.text)
                df= pd.read_csv(tmp)                
                
                u = []
                for x in range(len(df)):
                    p = {"url": df['media_url'].iloc[x]}
                    u.append(p)
                urls[0]= u                
                #paths[0]= url_csv_get.text
                paths[0]= r.text
                
        elif 'apply_button' in request.form:
            if int(request.form['apply_button']) == count:
                if request.form['Filter_select'] != "--":
                    Filter = request.form['Filter_select']
                    if request.form['Filter_select'] == "Remove memes":
                        attribute = "MemeDetector 0.89"
                    elif request.form['Filter_select'] == "Scene detector":
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == "Contains object":
                        attribute = request.form['option2_select']
                    else:
                        attribute = [request.form['latitude_text'], request.form['longitude_text']]
                    confidence = request.form['confidence']
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    params = {'filter_name_list': [attribute.split()[0]],
                              #'confidence_threshold_list': [float(attribute.split()[1])],
                              'confidence_threshold_list': [request.form['confidence']],
                              'column_name': 'media_url',
                              'csv_file': paths[count-1]
                              }
                        
                    r = requests.post(url='http://131.175.120.2:7777/Filter/API/filterImage', json=params)
                    
                    f = {'ID': count, 'Filter': Filter, 'Attribute': attribute}
                    k = {'ID': "", 'Filter': "", 'Attribute': ""}
                    applied[count-1] = f
                    applied.append(k)
                    paths.append(r.text)
                    tmp= StringIO(r.text)
                    df= pd.read_csv(tmp)
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
                        attribute = "MemeDetector 0.89"
                    elif request.form['Filter_select'] == "Scene detector":
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == "Contains object":
                        attribute = request.form['option2_select']
                    else:
                        attribute = [request.form['latitude_text'], request.form['longitude_text']]
                    confidence = request.form['confidence']
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    #url_csv = r"http://131.175.120.2:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c"

                    params = {'filter_name_list': [attribute.split()[0]],
                              #'confidence_threshold_list': [float(attribute.split()[1])],
                              'confidence_threshold_list': [request.form['confidence']],
                              'column_name': 'media_url',
                              'csv_file': paths[sel_count-1]
                              }                        
                    
                    r = requests.post(url='http://131.175.120.2:7777/Filter/API/filterImage', json=params)
                    
                    f = {'ID': count, 'Filter': Filter, 'Attribute': attribute}
                    applied[sel_count-1] = f
                    paths[sel_count] = r.text                    
                    #url_csv_get = requests.get(url_csv)
                    #url_request = io.StringIO(url_csv_get.content.decode('utf-8'))
                    tmp= StringIO(r.text)
                    df= pd.read_csv(tmp)
                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x]}
                        u.append(p)
                    urls[sel_count]= u                     
                    
                else:
                    flash('Select an option')
                    applied[sel_count-1]['Filter'] = ""
        elif 'reset_button' in request.form:
            count = 0
            source_applied = []
            s0 = {'ID': "", 'source': "", 'keywords': ""}
            source_applied.append(s0)
            applied = []
            urls = []
            paths = []
        elif 'up_button' in request.form:
            print(len(applied))
            print(len(urls))
            print(len(paths))
            #sel_count = int(request.form['up_button'])
            #a = applied[sel_count-2]
            #applied[sel_count-2] = applied[sel_count-1]
            #applied[sel_count-1] = a
            
            #for x in range(count-sel_count+1):
            #    params = {'filter_name_list': [applied[sel_count-2+x]['Attribute'].split()[0]],
            #              'confidence_threshold_list': [float(applied[sel_count-2+x]['Attribute'].split()[1])],
            #              'column_name': 'media_url',
            #              'csv_file': paths[sel_count-2+x]
            #             }
            #    r = requests.post(url='http://131.175.120.2:7777/Filter/API/filterImage', json=params)
            #    paths[sel_count-1+x] = r.text
            #    tmp= StringIO(r.text)
            #    df= pd.read_csv(tmp)
            #    u = []
            #    for x in range(len(df)):
            #        p = {"url": df['media_url'].iloc[x]}
            #        u.append(p)
            #    urls[sel_count-1+x]= u   
            pass
                
        else:
            #url_download = int(request.form['download_button'])
            #return redirect(applied[url_download-1]["url"])
            #print(applied[url_download-1]["url"])
            #print(applied)
            #print(url_download)
            pass
    return render_template('index.html', count=count, source_applied=source_applied, urls=urls,
                           applied=applied, number_images=number_images, confidence=confidence)

if __name__ == '__main__':
    app.run(debug=True)

