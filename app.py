from flask import Flask, render_template, request, flash, redirect, Response, session
import pandas as pd
import requests
from io import StringIO
import uuid
from geopy.geocoders import Nominatim
from geotext import GeoText
from config import *
import uuid as myuuid
import shelve

# for maps
import folium
from folium.plugins import MarkerCluster
import json
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hola'
geolocator = Nominatim(user_agent="example app")

server = '131.175.120.2:7779'
test = '127.0.0.1:8000'

address = test

def failsafe(df):
    if 'user_country' not in df:
        df['user_country'] = "Not initialized"
    if 'CIME_geolocation_string' not in df:
        df['CIME_geolocation_string'] = "Not Initialized"

user_data = {}

def get_or_setandget(mydict, key, default):
    if key not in mydict:
        mydict[key] = default
    return mydict[key]

# Session - level variables
def get_session_data(session):
    # recover identifier from cookie
    uuid = get_or_setandget(session, 'uiid', myuuid.uuid1()).hex

    if uuid not in user_data:
        user_data[uuid] = {}
    mystuff = user_data[uuid]

    #recover all data locally
    return ( get_or_setandget(mystuff, 'count', 0),
    get_or_setandget(mystuff, 'applied', []),
    get_or_setandget(mystuff, 'source_applied', [{'ID': "", 'source': "", 'keywords': ""}]),
    get_or_setandget(mystuff, 'number_images', 100),
    get_or_setandget(mystuff, 'tweets', []),
    get_or_setandget(mystuff, 'csv_contents', []),
    get_or_setandget(mystuff, 'confidence', 90),
    get_or_setandget(mystuff, 'confidence_', 0.9),
    get_or_setandget(mystuff, 'alert', ""),
    get_or_setandget(mystuff, 'locations', []),
    uuid, mystuff)

def set_session_data(session, count, applied, source_applied, number_images, tweets, csv_contents, confidence, confidence_, alert, locations, uuid, mystuff):
    mystuff['count'] = count
    mystuff['applied'] = applied
    mystuff['source_applied'] = source_applied
    mystuff['number_images'] = number_images
    mystuff['tweets'] = tweets
    mystuff['csv_contents'] = csv_contents
    mystuff['confidence'] = confidence
    mystuff['confidence_'] = confidence_
    mystuff['alert'] = alert
    mystuff['locations'] = locations
    user_data[uuid] = mystuff
    return

@app.route('/', methods=['GET','POST'])
def index():

    # Init all variables at user session level (not globals)
    count, applied, source_applied, number_images, tweets, csv_contents, confidence, confidence_, alert, locations, uuid, mystuff = get_session_data(session)
    
    print(applied)
    print(source_applied)

    print("GOT REQUEST FROM", uuid)

    if request.method == "POST":
        # Before the crawling
        if 'source_button' in request.form:
            if count == 0:
                option = request.form['source']
                keywords = request.form['keywords']
                number_images = request.form['number_pic']
            
                r = requests.post('http://'+address+'/Crawler/API/CrawlCSV',
                                  json={'query': keywords,
                                        'count': number_images})
            
                if len(r.text) != 1:

                    s = {'ID': count, 'source': option, 'keywords': keywords}
                    source_applied[0]= s

                    f = {'ID': "", 'Filter': "", 'Attribute': "", 'Confidence': 90}
                    applied.append(f)

                    tmp= StringIO(r.text)
                    df= pd.read_csv(tmp)
                    failsafe(df)

                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x],
                             "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                        u.append(p)
                        continue  # TODO: we are bypassing geo enrichment her

                        user_loc = df['user_loc'].iloc[x]
                        geolocated_text = geolocator.geocode(user_loc, timeout= 10)
                        if geolocated_text == None:
                            full_location_list = GeoText(user_loc).cities + GeoText(user_loc).countries
                            full_location = ''.join(str(e) for e in full_location_list)
                            geolocated_full_location = geolocator.geocode(full_location, timeout= 10)
                            if geolocated_full_location == None:
                                df['user_country'].iloc[x] = 'Not defined'
                            else:
                                df['user_country'].iloc[x] = geolocated_full_location.address.split(', ')[-1]
                        else:
                            df['user_country'].iloc[x] = geolocated_text.address.split(', ')[-1]


                    tweets.append(u)
                    if 'user_country' in df:
                        df_sorted = df.sort_values(by=['user_country'], ascending = True)
                        locations.append(df_sorted['user_country'].astype(str).unique().tolist())
                    csv_string = df.to_csv(encoding= "utf-8")                    
                    #csv_contents.append(url_csv_get.text)
                    csv_contents.append(csv_string)
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
                r = requests.post('http://'+address+'/Crawler/API/CrawlCSV',
                                  json={'query': keywords,
                                        'count': number_images})
                if len(r.text) != 1:                    
                    s = {'ID': 0, 'source': option, 'keywords': keywords}
                    source_applied[0]= s

                    tmp= StringIO(r.text)
                    df= pd.read_csv(tmp)
                    failsafe(df)

                    u = []
                    for x in range(len(df)):

                        p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x],
                             "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                        u.append(p)
                        continue  # TODO: we are bypassing geo enrichment her

                        user_loc = df['user_loc'].iloc[x]
                        geolocated_text = geolocator.geocode(user_loc, timeout= 10)
                        if geolocated_text == None:
                            full_location_list = GeoText(user_loc).cities + GeoText(user_loc).countries
                            full_location = ''.join(str(e) for e in full_location_list)
                            geolocated_full_location = geolocator.geocode(full_location, timeout= 10)
                            if geolocated_full_location == None:
                                df['user_country'].iloc[x] = 'Not defined'
                            else:
                                df['user_country'].iloc[x] = geolocated_full_location.address.split(', ')[-1]
                        else:
                            df['user_country'].iloc[x] = geolocated_text.address.split(', ')[-1]

                    tweets[0]= u

                    df_sorted = df.sort_values(by=['user_country'], ascending = True)
                    locations[0] = df_sorted['user_country'].astype(str).unique().tolist()
                    csv_string = df.to_csv(encoding= "utf-8")
                    #csv_contents[0]= url_csv_get.text
                    csv_contents[0]= csv_string
                    alert = ""
                else:
                    alert = "Your search query did not return any images. Please try to either shorten the query or make use of the OR keyword to make some of the terms optional"
                    
        # After the crawling
        elif 'apply_button' in request.form:
            if int(request.form['apply_button']) == count:
                extraparams={}
                if request.form['Filter_select'] != "" and request.form['Filter_select'] != d['user_location_sel_tag'] :
                    Filter = request.form['Filter_select']
                    if request.form['Filter_select'] == d['duplicates_tag']:
                        attribute = "PHashDeduplicator"
                        extraparams['bits'] = request.form['bit']
                    elif request.form['Filter_select'] == d['meme']:
                        attribute = "MemeDetector"
                    elif request.form['Filter_select'] == d['scene_tag']:
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == d['object_tag']:
                        attribute = 'YOLOv3ObjectDetector'
                        extraparams['object'] = request.form['option2_select']
                    elif request.form['Filter_select'] == d['object_tag_detr']:
                        attribute = 'DETRObjectDetector'
                        extraparams['object'] = request.form['option_obj_select']
                    elif request.form['Filter_select'] == d['flood_tag']:
                        attribute = "FloodClassifier"
                    elif request.form['Filter_select'] == d["nsfw_tag"]:
                        attribute = "NSFWClassifier"
                    elif request.form['Filter_select'] == d['post_location_tag']:
                        attribute = "CimeAugmenter"
                    elif request.form['Filter_select'] == "Add user country":
                        attribute = "GeotextAugmenter"
                    #else:
                    #    attribute = [request.form['latitude_text'], request.form['longitude_text']]
                    confidence_ = request.form['confidence']
                    confidence = float(confidence_)/100
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    params = {'filter_name_list': [attribute],
                              #'confidence_threshold_list': [float(attribute.split()[1])],
                              'confidence_threshold_list': [confidence],
                              'column_name': 'media_url',
                              'csv_file': csv_contents[count-1]
                              }

                    # build filters
                    filter = {attribute: {'confidence': confidence}}
                    for k,v in extraparams.items():
                        filter[attribute][k] = v
                    params = {'filters': filter,
                              'column_name': 'media_url',
                              'csv_file': csv_contents[count - 1]
                              }

                    print("###", params['filters'])
                    r = requests.post(url='http://'+address+'/Filter/API/FilterCSV', json=params)
                    
                    if len(r.text) > 160:
                        f = {'ID': count, 'Filter': Filter, 'Attribute': attribute, 'Confidence': confidence_}
                        f = {**extraparams, **f}
                        k = {'ID': "", 'Filter': "", 'Attribute': "", 'Confidence': 90}
                        applied[count-1] = f
                        applied.append(k)

                        csv_contents.append(r.text)
                        tmp= StringIO(r.text)
                        df= pd.read_csv(tmp)
                        failsafe(df)

                        df_sorted = df.sort_values(by=['user_country'], ascending = True)
                        locations.append(df_sorted['user_country'].astype(str).unique().tolist())
                        u = []
                        for x in range(len(df)):
                            p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x], "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                            u.append(p)
                        tweets.append(u)
                        count+=1
                        alert = ""
                    else:
                        alert = "After running the above filter, no images remain. Either increase the number of images or change the filter. (1)"
                        
                elif request.form['Filter_select'] == d['user_location_sel_tag'] :
                    Filter = d['user_location_sel_tag']
                    attribute = request.form['option3_select']
                    f = {'ID': count, 'Filter': Filter, 'Attribute': attribute, 'Confidence': confidence_}
                    k = {'ID': "", 'Filter': "", 'Attribute': "", 'Confidence': 90}
                    applied[count-1] = f
                    applied.append(k)
                                       
                    tmp = StringIO(csv_contents[count-1])
                    df0 = pd.read_csv(tmp)
                    df = df0.loc[df0['user_country'] == attribute]
                    failsafe(df)

                    df_sorted = df.sort_values(by=['user_country'], ascending = True)
                    locations.append(df_sorted['user_country'].astype(str).unique().tolist())
                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x], "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                        u.append(p)
                    tweets.append(u)                     
                    csv_string = df.to_csv(encoding= "utf-8")
                    csv_contents.append(csv_string)
                    count+=1
                    alert = ""
                    
                #else:
                #    flash('Select an option')
                #    applied[count-1]['Filter'] = ""
            # not last request
            else:
                sel_count = int(request.form['apply_button'])

                extraparams = {}

                if request.form['Filter_select'] != "" and request.form['Filter_select'] != d['user_location_sel_tag'] :
                    Filter = request.form['Filter_select']
                    if request.form['Filter_select'] == d['duplicates_tag']:
                        attribute = "PHashDeduplicator"
                        extraparams['bits'] = request.form['bit']
                    elif request.form['Filter_select'] == d['meme']:
                        attribute = "MemeDetector"
                    elif request.form['Filter_select'] == d['scene_tag']:
                        attribute = request.form['option1_select']
                    elif request.form['Filter_select'] == d['object_tag']:
                        attribute = 'YOLOv3ObjectDetector'
                        extraparams['object'] = request.form['option2_select']
                    elif request.form['Filter_select'] == d['object_tag_detr']:
                        attribute = 'DETRObjectDetector'
                        extraparams['object'] = request.form['option_obj_select']
                    elif request.form['Filter_select'] == d['flood_tag']:
                        attribute = "FloodClassifier"
                    elif request.form['Filter_select'] == d["nsfw_tag"]:
                        attribute = "NSFWClassifier"
                    elif request.form['Filter_select'] == d['post_location_tag']:
                        attribute = "CimeAugmenter"
                    elif request.form['Filter_select'] == "Add user country":
                        attribute = "GeotextAugmenter"
                    else:
                        attribute = [request.form['latitude_text'], request.form['longitude_text']]
                    
                    confidence_ = request.form['confidence'] # form value
                    confidence = float(confidence_)/100 # post value
                    #url_csv = "https://polimi365-my.sharepoint.com/:x:/g/personal/10787953_polimi_it/EczlUzJfhFdFjwNqc8NThlQB-pYmb6CbxDZbxbwB4xHQCQ?Download=1"
                    #url_csv = r"http://131.175.120.2:7777/Filter/API/filterImageURL?filter_name_list=PeopleDetector&filter_name_list=MemeDetector&filter_name_list=PublicPrivateClassifier&confidence_threshold_list=0.98&confidence_threshold_list=0.89&confidence_threshold_list=0.93&column_name=media_url&csv_url=https%3A%2F%2Fdrive.google.com%2Fuc%3Fexport%3Ddownload%26id%3D12hy5NRkFiNG2lI9t6oXQ_12_QDUQz94c"

                    params = {'filter_name_list': [attribute],
                              #'confidence_threshold_list': [float(attribute.split()[1])],
                              'confidence_threshold_list': [confidence],
                              'column_name': 'media_url',
                              'csv_file': csv_contents[sel_count-1]
                              }

                    filter = {attribute: {'confidence': confidence}}
                    for k,v in extraparams.items():
                        filter[attribute][k] = v
                    params = {'filters': filter,
                              'column_name': 'media_url',
                              'csv_file': csv_contents[sel_count - 1]
                              }

                    print("###", params['filters'])
                    
                    r = requests.post(url='http://'+address+'/Filter/API/FilterCSV', json=params)
                    #print(len(r.text))
                    if len(r.text) > 160:
                        f = {'ID': sel_count, 'Filter': Filter, 'Attribute': attribute, 'Confidence': confidence_}
                        f = {**extraparams, **f}
                        applied[sel_count-1] = f
                        csv_contents[sel_count] = r.text                    
                        #url_csv_get = requests.get(url_csv)
                        #url_request = io.StringIO(url_csv_get.content.decode('utf-8'))
                        tmp= StringIO(r.text)
                        df= pd.read_csv(tmp)

                        failsafe(df)

                        df_sorted = df.sort_values(by=['user_country'], ascending = True)
                        locations[sel_count]= df_sorted['user_country'].astype(str).unique().tolist()
                        u = []
                        for x in range(len(df)):
                            p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x], "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                            u.append(p)
                        tweets[sel_count]= u 
                        alert = ""
                    else:
                        alert = "After running the above filter, no images remain. Either increase the number of images or change the filter. (2)"
                
                elif request.form['Filter_select'] == d['user_location_sel_tag'] :
                    Filter = d['user_location_sel_tag']
                    attribute = request.form['option3_select']
                    f = {'ID': sel_count, 'Filter': Filter, 'Attribute': attribute, 'Confidence': confidence_}
                    applied[sel_count-1] = f                  
                    tmp = StringIO(csv_contents[sel_count-1])
                    df0 = pd.read_csv(tmp)
                    df = df0.loc[df0['user_country'] == attribute]
                    failsafe(df)


                    df_sorted = df.sort_values(by=['user_country'], ascending = True)
                    locations[sel_count]= df_sorted['user_country'].astype(str).unique().tolist()
                    u = []
                    for x in range(len(df)):
                        p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x], "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                        u.append(p)
                    tweets[sel_count]= u                     
                    csv_string = df.to_csv(encoding= "utf-8")
                    csv_contents[sel_count]= csv_string
                    alert = ""
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
            locations = []
            alert = ""
        elif 'up_button' in request.form:

            sel_count = int(request.form['up_button'])

            a = applied[sel_count-2]
            applied[sel_count-2] = applied[sel_count-1]
            applied[sel_count-1] = a
            
            for a in range(count-sel_count+1):
                if applied[sel_count-2+a]['Filter'] != d['user_location_sel_tag'] :
                    params = {'filter_name_list': [applied[sel_count-2+a]['Attribute']],
                              'confidence_threshold_list': [int(applied[sel_count-2+a]['Confidence'])/100],
                              'column_name': 'media_url',
                              'csv_file': csv_contents[sel_count-2+a]
                              }
                    params = {'filters': {applied[sel_count-2+a]['Attribute']: {'confidence': int(applied[sel_count-2+a]['Confidence'])/100}},
                              'column_name': 'media_url',
                              'csv_file': csv_contents[sel_count-2+a]
                              }
                    r = requests.post(url='http://'+address+'/Filter/API/FilterCSV', json=params)
                    if len(r.text) > 160:

                        csv_contents[sel_count-1+a] = r.text
                        tmp= StringIO(r.text)
                        df= pd.read_csv(tmp)
                        failsafe(df)

                        df_sorted = df.sort_values(by=['user_country'], ascending = True)
                        locations[sel_count-1+a]= df_sorted['user_country'].astype(str).unique().tolist()
                        u = []
                        for x in range(len(df)):
                            p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x], "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                            u.append(p)
                        tweets[sel_count-1+a]= u
                        alert = ""
                        #pass
                    else:
                        print(r.text)
                        alert = "After running the above filter, no images remain. Either increase the number of images or change the filter. (3)"
                        break
                else:
                    tmp = StringIO(csv_contents[sel_count-2+a])
                    df0 = pd.read_csv(tmp)
                    df = df0.loc[df0['user_country'] == applied[sel_count-2+a]['Attribute']]
                    failsafe(df)

                    csv_string = df.to_csv(encoding= "utf-8")
                    print("The length is", len(csv_string))
                    if len(csv_string) > 160:
                        print("location: ", applied)
                        df_sorted = df.sort_values(by=['user_country'], ascending = True)
                        locations[sel_count-1+a]= df_sorted['user_country'].astype(str).unique().tolist()
                        u = []
                        for x in range(len(df)):
                            p = {"url": df['media_url'].iloc[x], "text": df['full_text'].iloc[x], "user_country": df['user_country'].iloc[x], "tweet_location": df['CIME_geolocation_string'].iloc[x]}
                            u.append(p)
                        tweets[sel_count-1+a]= u                     
                        csv_contents[sel_count-1+a]= csv_string
                        alert = ""
                    else:
                        alert = "After running the above filter, no images remain. Either increase the number of images or change the filter. (4)"
                        break
        else:
            #url_download = int(request.form['download_button'])
            #with open('result1.csv', 'w+', encoding= "utf-8") as file:
            #    file.write(csv_contents[url_download])            
            pass

    # Keep track of user data at session level
    set_session_data(session, count, applied, source_applied, number_images, tweets, csv_contents, confidence,
                      confidence_, alert, locations, uuid, mystuff)

    hasmap, df = checkmap(csv_contents)
    mapdata = map(small=True) if hasmap else None

    return render_template('index.html', count=count, source_applied=source_applied, tweets=tweets,
                           applied=applied, alert=alert, locations=locations,
                           number_images=number_images, confidence=confidence, hasmap=hasmap, mapdata=mapdata)

@app.route("/downloadCSV")
def downloadCSV():
    #print("length of csv_contents: ", len(csv_contents))
    #print("int(request.args.get('id')): ", int(request.args.get('id')))
    #print("csv_contents:\n\n", csv_contents)

    count, applied, source_applied, number_images, tweets, csv_contents, confidence, confidence_, alert, locations, uuid, mystuff = get_session_data(
        session)

    return Response(
        csv_contents[int(request.args.get('id'))],
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=download.csv"})

def checkmap(csv_contents):
    lastid = len(csv_contents) - 1 # only last id
    try:
        df = csv_contents[lastid]
        tmp = StringIO(df)
        df = pd.read_csv(tmp)
    except Exception:
        return False, None

    if 'CIME_geolocation_centre' in df:
        return True, df

    return False, None

@app.route('/map', methods=['GET','POST'])
def map(small=False):
    count, applied, source_applied, number_images, tweets, csv_contents, confidence, confidence_, alert, locations, uuid, mystuff = get_session_data(
        session)

    hasmap, df = checkmap(csv_contents)
    if not hasmap:
        return "Not initialized"

    # parse json
    df['CIME_list'] = df['CIME_geolocation_centre'].replace('None', np.nan).fillna('[]').apply(json.loads)
    # get first
    df['CIME_first'] = df['CIME_list'].apply(lambda l: [l[0][1], l[0][0]] if l else None)
    # get valid
    dfout = df[~df['CIME_first'].isnull()]
    # to records
    records = dfout[['full_text', 'media_url', 'CIME_first']].to_dict('records')

    if small:
        f = folium.Figure(width='50%')
        m = folium.Map(location=[10.0, 0.0], tiles="cartodbpositron" , zoom_start=2)
        m.add_to(f)
        # m = folium.Map(location=[10.0, 0.0], tiles="cartodbpositron", zoom_start=1, height='30%', width='40%', left ='30%', right='30%', padding='0%')
    else:
        m = folium.Map(location=[10.0, 0.0], tiles="cartodbpositron", zoom_start=3)

    mk = MarkerCluster()
    fg = folium.FeatureGroup(name='')

    for r in records:
        ma = folium.Marker(
            location=r['CIME_first'],
            popup='<p>' + r['full_text'] + '</p>' + '<img src="' + r['media_url'] + '" height=100>',
            icon=folium.Icon(color="red", icon="info-sign"),
        )
        mk.add_child(ma)

    fg.add_child(mk)
    m.add_child(fg)

    if small:
        h = f._repr_html_()
        h = h.replace("position:relative;width:100%;height:0;padding-bottom:60%;", "position:relative;width:100%;height:0;padding-bottom:60vh;")
    else:
        h = m._repr_html_()
    return h

if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, use_reloader=True)

@app.context_processor
def inject_tags():
    return get_tags()

