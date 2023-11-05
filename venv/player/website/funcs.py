from bs4 import BeautifulSoup
import urllib.parse
import requests
from multiprocessing import Queue
import mysql.connector
from .models import card_user_table,team_names,User,grader_names
import boto3
import environ
from pathlib import Path 


   

s3 = boto3.client('s3')
env = environ.Env(
    DEBUG=(bool,False)
)

BASE_DIR = Path(__file__).resolve().parent

environ.Env.read_env(BASE_DIR /'.env')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
           
            

def add_record_to_db(search_data, result_data):
    try:
      
        if search_data['grader_id'] is not None:
            grader_obj = grader_names.objects.get(grader_id=search_data['grader_id'])
        else:
            grader_obj = None
        user_obj = User.objects.get(id=search_data['user_id'])
        team_obj = team_names.objects.get(team_id=search_data['team_id'])
    
    except:
        print('Foreign Key does not exist')
    try:
        new_card = card_user_table(year=search_data['year'],set_name=search_data['set_name'],player_name=search_data['player_name'],
                                   autographed=search_data['autographed'],graded=search_data['graded'],grade=search_data['grade'],
                                   parallel=search_data['parallel'],parallel_number=search_data['parallel_number'],average_price=result_data['average_price'],
                                   card_img_url=result_data['img'],search_criteria=search_data['search_criteria'],grader=grader_obj,user=user_obj,team=team_obj,parallel_name=search_data['parallel_name'])
        new_card.save()
        print('card added!')
    except:
        print('Failed to Insert record into database')

def lookup_card(search_str):
    try:
        pics = []
        base_url= 'https://www.ebay.com/sch/i.html?_nkw='
        sold_url_end = '&_sacat=0&LH_Complete=1&LH_Sold=1'
        words = search_str.split(' ')
        len_words = len(words)-1
        search_str = ''
        first_card= None
        i=0

        while i <= len_words:
            if i !=len_words:
                words[i]= urllib.parse.quote(words[i])+'+'
                search_str = search_str+words[i]
            else:
                urllib.parse.quote(words[i])
                search_str = search_str+words[i]
            i+=1      
        search_str_enc = base_url+search_str+sold_url_end
        # print(search_str_enc)

        response = requests.get(search_str_enc)
        html = response.content
        soup = BeautifulSoup(html,'html.parser')
        res_con = soup.find('ul',class_="srp-results srp-list clearfix")
        completed_price_elements = res_con.find_all("li")
        prices = []
        for item in completed_price_elements:
            if (item.find("div","s-message__content") is not None and 'fewer' in item.find("div","s-message__content").text):
                break
            if(item.find("span",class_="s-item__price") is not None):
                price_str = item.find("span",class_="s-item__price").text.strip('$').replace(',','').split(' ')[0]
                price_flt = float(price_str)
                prices.append(price_flt) 
                pics.append(item.find("img").get("src"))
        total = 0  
        if prices is not None:
            for price in prices:
                total = total + price
                ave = round(total/ len(prices),2)
        # print(prices)                
        results={
		'average_price':ave,
		'min':min(prices),
		'max':max(prices),
        'search_crit':search_str
		}
        if len(pics)>0:
            results['img'] = pics[0]
        # print(results)
        return results
    except:
	    return None


def create_search_query(form,user_id):
    player_name = form.cleaned_data['player_name']
    #id:
    year_id = form.data['year']
    #DISPLAY VAL:
    year = form.cleaned_data['year']
    team_id = form.data['team']
    team_name = form.cleaned_data['team']
    set_name = form.cleaned_data['set_name']
    parallel_number = form.cleaned_data['parralel']
    autographed = form.cleaned_data['autographed']
    grader_id = form.data['grader']
    grader_name = form.cleaned_data['grader']
    grade = form.cleaned_data['grade']
    parallel_name = form.cleaned_data['parralel_name']
    if autographed == True:
        auto_str = ' auto autograph'
    if autographed == False:
        auto_str = ' -auto -autograph'

    if grader_name is not None:
        grader_str = ' ' + str(grader_name)
        grader_switch = True
    else:
        grader_str = ''
        grader_switch = False

    if parallel_number is not None:
        parallel_str = ' /'+str(parallel_number)
        parallel_num = parallel_str.replace(" ", "").replace("/","")
    else:
        parallel_str = ''
        parallel_num = None

    if grade != 'None':
        grade_str = ' ' +str(grade)
        grade_num = int(grade_str.replace(" ", ""))
    else:
        grade_str = ''
        grade_num = None

    if len(parallel_str) > 0:
        parallel_switch = True 
    else:
        parallel_switch = False

    if grader_id == '':
        grader_id = None

    search_query = player_name + ' ' + str(year) + ' ' + set_name + ' ' + str(team_name) + ' ' + parallel_name + parallel_str + auto_str + grader_str + grade_str
    add_data = {
            'year':str(year),
            'set_name':set_name,
            'player_name':player_name,
            'autographed':autographed,
            'graded': grader_switch,
            'grade':grade_num,
            'parallel':parallel_switch,
            'parallel_name':parallel_name,
            'parallel_number':parallel_num,
            'average_price': None,
            'card_img_url':None,
            'search_criteria': search_query,
            'grader_id':grader_id,
            'team_id':team_id,
            'user_id':user_id     
    }
    return (search_query,add_data)

def get_s3_url(object_key):
    
    # s3 = boto3.client('s3')
    base_url = 'https://cardappshum.s3.amazonaws.com/'
    full_url = base_url+object_key
    print(full_url)
    # s3_url = s3.generate_presigned_url(
    #     ClientMethod='get_object',
    #     Params={'Bucket': AWS_STORAGE_BUCKET_NAME, 'Key': object_key,'ResponseExpires':157680000}
    # )
    # print(s3_url)
    # s3.close()
    return full_url
