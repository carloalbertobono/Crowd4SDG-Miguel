from flask import Flask, render_template, request, flash, redirect, Response
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

tweets = []
##change len(df) to 100
#for x in range(len(df)):
#    u = {"url": df['media_url'].iloc[x]}
#    tweets.append(u)


csv_contents = []
applied = []
source_applied = []
count = 0
number_images= 100
confidence= 0.9
alert = ""
s0 = {'ID': "", 'source': "", 'keywords': ""}
source_applied.append(s0)

@app.route('/', methods=['GET','POST'])
def index():
    global count, applied, source_applied, number_images, tweets, csv_contents, confidence, alert
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
                #print("The text is:", r.text, ">")
                #print(len(r.text))
                if len(r.text) != 1:
                    tmp= StringIO(r.text)
                    df= pd.read_csv(tmp)                    
                    s = {'ID': count, 'source': option, 'keywords': keywords}
                    source_applied[0]= s
                    print(source_applied)
                    f = {'ID': "", 'Filter': "", 'Attribute': "", 'Confidence': 0.9}
                    applied.append(f)
                
                    #url_csv_get = requests.get(url_csv)
                    #url_request = StringIO(url_csv_get.content.decode('utf-8'))
                    #df = pd.read_csv(url_request, error_bad_lines=False, index_col=False)
                    #file = pd.DataFrame.to_csv(df, path_or_buf=(None))
                    #print(df)

                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x]}
                        u.append(p)
                    tweets.append(u)
                    #csv_contents.append(url_csv_get.text)
                    csv_contents.append(r.text)
                    count+=1
                    alert = ""
                else:
                    alert = "Your search query did not return any images. Please try to either shorten the query or make use of the OR keyword to make some of the terms optional"
                
            else:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
                #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/ETUZnzuvqtlHv0iHyyOI0MYBO7O1yFXIqu0QPeIhHUJZnw?Download=1"
                #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/ETpS3YrdzspLjVs9TGF7JksBSVwPjpVWYKSdEAEqYEMW_w?Download=1"                
                r = requests.post('http://131.175.120.2:7777/Crawler/API/CrawlCSV',
                                  json={'query': keywords,
                                        'count': number_images})
                #print(len(r.text))
                if len(r.text) != 1:
                    tmp= StringIO(r.text)
                    df= pd.read_csv(tmp)                    
                    s = {'ID': 0, 'source': option, 'keywords': keywords}
                    source_applied[0]= s
                    print(source_applied)
                
                    #url_csv_get = requests.get(url_csv)
                    #url_request = StringIO(url_csv_get.content.decode('utf-8'))
                    #df = pd.read_csv(url_request, error_bad_lines=False, index_col=False)
                    #file = pd.DataFrame.to_csv(df, path_or_buf=(None))
                    
                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x]}
                        u.append(p)
                    tweets[0]= u                
                    #csv_contents[0]= url_csv_get.text
                    csv_contents[0]= r.text
                    alert = ""
                else:
                    alert = "Your search query did not return any images. Please try to either shorten the query or make use of the OR keyword to make some of the terms optional"
                    #print("alert is read")
        elif 'apply_button' in request.form:
            if int(request.form['apply_button']) == count:
                if request.form['Filter_select'] != "":
                    Filter = request.form['Filter_select']
                    if request.form['Filter_select'] == "Remove memes":
                        attribute = "MemeDetector"
                    elif request.form['Filter_select'] == "Scene detector":
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == "Contains object":
                        attribute = request.form['option2_select']
                    else:
                        attribute = [request.form['latitude_text'], request.form['longitude_text']]
                    confidence = request.form['confidence']
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    params = {'filter_name_list': [attribute],
                              #'confidence_threshold_list': [float(attribute.split()[1])],
                              'confidence_threshold_list': [request.form['confidence']],
                              'column_name': 'media_url',
                              'csv_file': csv_contents[count-1]
                              }
                        
                    r = requests.post(url='http://131.175.120.2:7777/Filter/API/FilterCSV', json=params)
                    print(len(r.text))
                    if len(r.text) > 116:
                        f = {'ID': count, 'Filter': Filter, 'Attribute': attribute, 'Confidence': confidence}
                        k = {'ID': "", 'Filter': "", 'Attribute': "", 'Confidence': 0.9}
                        applied[count-1] = f
                        applied.append(k)
                        print(applied)
                        csv_contents.append(r.text)
                        tmp= StringIO(r.text)
                        df= pd.read_csv(tmp)
                        u = []
                        for x in range(len(df)):
                            p = {"url": df['media_url'].iloc[x]}
                            u.append(p)
                        tweets.append(u)                    
                        count+=1
                        alert = ""
                    else:
                        alert = "After running the above filter, no images remain. Either increase the number of images or change the filter."
                #else:
                #    flash('Select an option')
                #    applied[count-1]['Filter'] = ""
            else:
                sel_count = int(request.form['apply_button'])
                if request.form['Filter_select'] != "":
                    Filter = request.form['Filter_select']
                    if request.form['Filter_select'] == "Remove memes":
                        attribute = "MemeDetector"
                    elif request.form['Filter_select'] == "Scene detector":
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == "Contains object":
                        attribute = request.form['option2_select']
                    else:
                        attribute = [request.form['latitude_text'], request.form['longitude_text']]
                    confidence = request.form['confidence']
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    #url_csv = r"http://131.175.120.2:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c"

                    params = {'filter_name_list': [attribute],
                              #'confidence_threshold_list': [float(attribute.split()[1])],
                              'confidence_threshold_list': [request.form['confidence']],
                              'column_name': 'media_url',
                              'csv_file': csv_contents[sel_count-1]
                              }                        
                    
                    r = requests.post(url='http://131.175.120.2:7777/Filter/API/FilterCSV', json=params)
                    #print(len(r.text))
                    if len(r.text) > 116:
                        f = {'ID': sel_count, 'Filter': Filter, 'Attribute': attribute, 'Confidence': confidence}
                        applied[sel_count-1] = f
                        print(applied)
                        csv_contents[sel_count] = r.text                    
                        #url_csv_get = requests.get(url_csv)
                        #url_request = io.StringIO(url_csv_get.content.decode('utf-8'))
                        tmp= StringIO(r.text)
                        df= pd.read_csv(tmp)
                        u = []
                        for x in range(len(df)):
                            p = {"url": df['media_url'].iloc[x]}
                            u.append(p)
                        tweets[sel_count]= u 
                        alert = ""
                    else:
                        alert = "After running the above filter, no images remain. Either increase the number of images or change the filter."
                #else:
                #    flash('Select an option')
                #    applied[sel_count-1]['Filter'] = ""
        elif 'reset_button' in request.form:
            count = 0
            source_applied = []
            s0 = {'ID': "", 'source': "", 'keywords': ""}
            source_applied.append(s0)
            applied = []
            tweets = []
            csv_contents = []
            alert = ""
        elif 'up_button' in request.form:
            print(len(applied))
            print(len(tweets))
            print(len(csv_contents))
            #sel_count = int(request.form['up_button'])
            #a = applied[sel_count-2]
            #applied[sel_count-2] = applied[sel_count-1]
            #applied[sel_count-1] = a
            
            #for x in range(count-sel_count+1):
            #    params = {'filter_name_list': [applied[sel_count-2+x]['Attribute'].split()[0]],
            #              'confidence_threshold_list': [float(applied[sel_count-2+x]['Attribute'].split()[1])],
            #              'column_name': 'media_url',
            #              'csv_file': csv_contents[sel_count-2+x]
            #             }
            #    r = requests.post(url='http://131.175.120.2:7777/Filter/API/FilterCSV', json=params)
            #    csv_contents[sel_count-1+x] = r.text
            #    tmp= StringIO(r.text)
            #    df= pd.read_csv(tmp)
            #    u = []
            #    for x in range(len(df)):
            #        p = {"url": df['media_url'].iloc[x]}
            #        u.append(p)
            #    tweets[sel_count-1+x]= u   
            pass
                
        else:
            #url_download = int(request.form['download_button'])
            #with open('result1.csv', 'w+', encoding= "utf-8") as file:
            #    file.write(csv_contents[url_download])            
            pass
    return render_template('index.html', count=count, source_applied=source_applied, tweets=tweets,
                           applied=applied, alert=alert, number_images=number_images, confidence=confidence)

@app.route("/downloadCSV")
def downloadCSV():
    #print("length of csv_contents: ", len(csv_contents))
    #print("int(request.args.get('id')): ", int(request.args.get('id')))
    #print("csv_contents:\n\n", csv_contents)
    return Response(
        csv_contents[int(request.args.get('id'))],
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=download.csv"})


if __name__ == '__main__':
    app.run(debug=True)

