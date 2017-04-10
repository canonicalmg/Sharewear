from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
import json
from django.contrib.auth import authenticate,login, logout as auth_logout
from .models import *
from django.contrib.auth.models import User
# from amazon.api import AmazonAPI
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from .models import *
import requests
import bottlenose
from bs4 import BeautifulSoup
import xmltodict
import ast

def populate_db_amazon(request):
    try:
        amazon = bottlenose.Amazon('AKIAJOR5NTXK2ERTU6AQ',
                                   'kck/SKuTJif9bl7qeq5AyB4CU8HWsdz14VW4Iaz2',
                                   'can037-20',
                                   )
        cloth_types = ["Shirt", "Pants", "Shoes"]
        gender = [
            "Women",
            # "Men"
        ]
        pages = [1,2,3,4,5,6,7,8,9,10]
        for each_gender in gender:
            for each_cloth_type in cloth_types:
                for each_page in pages:
                    product = amazon.ItemSearch(Keywords="%s's %s" % (each_gender, each_cloth_type),
                                                SearchIndex="All",
                                                ResponseGroup="Images, SalesRank, OfferFull, ItemAttributes",
                                                Availability="Available",
                                                paginate=True,
                                                ItemPage=each_page)
                    soup = BeautifulSoup(product, "xml")

                    newDictionary = xmltodict.parse(str(soup))
                    try:
                        for each_item in newDictionary['ItemSearchResponse']['Items']['Item']:
                            try:
                                current_clothing = clothing.objects.get(carrier='amazon',
                                                                        carrier_id=each_item['ASIN'])
                            except:
                                #clothing does not exist in db
                                try:
                                    if each_gender == "Women":
                                        gender_bool = True
                                    else:
                                        gender_bool = False
                                    new_clothing = clothing(name=each_item['ItemAttributes']['Title'],
                                                            carrier="amazon",
                                                            carrier_id=each_item['ASIN'],
                                                            small_url=each_item['SmallImage']['URL'],
                                                            large_url=each_item['LargeImage']['URL'],
                                                            gender=gender_bool,
                                                            price=each_item['OfferSummary']['LowestNewPrice']['FormattedPrice'],
                                                            color=each_item['ItemAttributes']['Color'],
                                                            brand=each_item['ItemAttributes']['Brand'],
                                                            aff_url=generate_amazon_link(each_item['ASIN']),
                                                            cloth_type=each_cloth_type)
                                    new_clothing.save()
                                    print "added item"
                                except Exception as e:
                                    print "error ", e
                                    pass
                    except Exception as e:
                        print "Error on upper try: ", e
        return HttpResponse("Success")
    except Exception as e:
        print "error ", e
        return HttpResponse("Error")

def populate_db(request):
    try:
        amazon = bottlenose.Amazon('AKIAJOR5NTXK2ERTU6AQ',
                                    'kck/SKuTJif9bl7qeq5AyB4CU8HWsdz14VW4Iaz2',
                                    'can037-20',
                                   # Parser=lambda text: BeautifulSoup(text, 'xml')
                                    # region="US"
                                   )
        # cloth_types = ["Shirt", "Pants", "Shoes"]
        # gender = ["Women", "Men"]
        # for each_gender in gender:
        #         for each_cloth_type in cloth_types:
        product = amazon.ItemSearch(Keywords="Women's Shirt",
                                    SearchIndex="All",
                                    ResponseGroup="Images, SalesRank, OfferFull, ItemAttributes",
                                    Availability="Available",
                                    paginate=True,
                                    ItemPage=2)
        soup = BeautifulSoup(product, "xml")
        print soup

        newDictionary = xmltodict.parse(str(soup))
        for each_item in newDictionary['ItemSearchResponse']['Items']['Item']:
            print each_item
            print "_____"
                        # try:
                        #     current_clothing = clothing.objects.get(carrier='amazon',
                        #                                             carrier_id=each_item['ASIN'])
                        # except:
                        #     #clothing does not exist in db
                        #     try:
                        #         if each_gender == "Women":
                        #             gender_bool = True
                        #         else:
                        #             gender_bool = False
                        #         new_clothing = clothing(name=each_item['ItemAttributes']['Title'],
                        #                                 carrier="amazon",
                        #                                 carrier_id=each_item['ASIN'],
                        #                                 small_url=each_item['SmallImage']['URL'],
                        #                                 large_url=each_item['LargeImage']['URL'],
                        #                                 gender=gender_bool,
                        #                                 price=each_item['OfferSummary']['LowestNewPrice']['FormattedPrice'],
                        #                                 color=each_item['ItemAttributes']['Brand'],
                        #                                 brand=each_item['ItemAttributes']['Color'],
                        #                                 aff_url=generate_amazon_link(each_item['ASIN']),
                        #                                 cloth_type=each_cloth_type)
                        #         new_clothing.save()
                        #         print "added item"
                        #     except Exception as e:
                        #         print "error ", e
                        #         pass
            # print "item = ", each_item['ASIN']
            # print "img = ", each_item['SmallImage']['URL']
            # print "large = ", each_item['LargeImage']['URL']
            # print "offer summary = ", each_item['OfferSummary']['LowestNewPrice']['FormattedPrice']
            # print "url = ", generate_amazon_link(each_item['ASIN'])
            # print "title = ", each_item['ItemAttributes']['Title']
            # # response = amazon.ItemLookup(ItemId=each_item['ASIN'])
            # # print "response = ", response
            # print "________"



        # products = amazon.search_n(1, Keywords="Women's Shirt", SearchIndex="Apparel")
        # for each_product in products:
        #     print dir(each_product)
        #     print each_product.availability
        #     print each_product.availability_type
        #     print each_product.price_and_currency
        #     print each_product.list_price
        #     print each_product.formatted_price
        #     print each_product.get_parent

    #     for each_gender in gender:
    #         for each_cloth_type in cloth_types:
    #             products = amazon.search_n(99, Keywords=each_gender + "'s " + each_cloth_type, SearchIndex="Apparel")
    #             for each_product in products:
    #                 current_id = each_product.asin
    #                 current_carrier = "amazon"
    #                 print "price = ", each_product.price_and_currency
    #                 if each_product.price_and_currency[0] is not None:
    #                     try:
    #                         current_clothing = clothing.objects.get(carrier=current_carrier,
    #                                                                 carrier_id=current_id)
    #                     except:
    #                         #clothing does not exist in db
    #                         if gender == "Women":
    #                             gender_bool = True
    #                         else:
    #                             gender_bool = False
    #                         new_clothing = clothing(name=each_product.title,
    #                                                 carrier="amazon",
    #                                                 carrier_id=each_product.asin,
    #                                                 small_url=each_product.small_image_url,
    #                                                 large_url=each_product.large_image_url,
    #                                                 gender=gender_bool,
    #                                                 price=each_product.price_and_currency[0],
    #                                                 cloth_type=each_cloth_type)
    #                         new_clothing.save()
    #                         print "added item"
        return HttpResponse("Success")
    except Exception as e:
        print "error ", e
        return HttpResponse("Error")

def generate_amazon_link(ASIN):
    return "https://www.amazon.com/dp/%s/?tag=can037-20" % (ASIN)

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect("/")

@csrf_exempt
def headerSignIn(request):
    if request.is_ajax():
        if request.method == "POST":
            data = request.POST.getlist("data[]")
            print "data = ", data

            user = authenticate(username=str(data[0]), password=str(data[1]))
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Success")
            else:
                return HttpResponse("Does not match")

@csrf_exempt
def headerSignUp(request):
    if request.is_ajax():
        if request.method == "POST":
            data = request.POST.getlist("data[]")
            try:
                user = User.objects.create_user(username=str(data[0]),
                                                email=str(data[2]),
                                                password=str(data[1]))
                gender = data[3]
                if gender == "true":
                    gender = True
                else:
                    gender = False
                #create profile
                profile_obj = profile(user=user,
                                      gender=gender)
                profile_obj.save()
            except Exception as e:
                print "e = ", str(e)
                if str(e) == "column username is not unique":
                    return HttpResponse("Username Exists")

            if user is not None:
                if profile_obj is not None:
                    if user.is_active:
                        login(request, user)
                        return HttpResponse("Success")
            else:
                return HttpResponse("Does not match")

def get_featured_outfits(current_profile):
    outfit_objs = outfit.objects.filter()
    outfits = get_outfit_items(outfit_objs, current_profile)
    return outfits

def get_new_outfits(current_profile):
    outfit_objs = outfit.objects.filter().order_by('-id')[:10]
    outfits = get_outfit_items(outfit_objs, current_profile)
    return outfits

def get_popular_outfits(current_profile):
    outfit_objs = outfit.objects.filter().order_by('-likes')[:10]
    outfits = get_outfit_items(outfit_objs, current_profile)
    return outfits

def get_outfit_items(outfits, current_profile):
    outfits_arr = []
    for each_outfit in outfits:
        outfit_items = outfit_item.objects.filter(outfit=each_outfit)
        inner_outfit = []
        for each_outfit_item in outfit_items:
            inner_outfit.append({"pk": each_outfit_item.pk,
                                 "transform": ast.literal_eval(each_outfit_item.transform_matrix,),
                                 "large_url": each_outfit_item.clothing.large_url,
                                 "zIndex": each_outfit_item.zIndex})
        is_following = each_outfit.profile.is_following(current_profile)
        outfits_arr.append({"outfit": inner_outfit,
                        "user": {"username": each_outfit.profile.user.username,
                                 "profile_img": each_outfit.profile.profile_image,
                                 "location": each_outfit.profile.location,
                                 "user_id": each_outfit.profile.pk,
                                 "is_following": is_following,
                                 "is_self": each_outfit.profile == current_profile},
                        "outfit_pk": each_outfit.pk,
                        "canvasHeight": each_outfit.canvas_height,
                        "canvasWidth": each_outfit.canvas_width,
                        "total_likes": each_outfit.likes,
                        "liked": each_outfit.does_user_like(current_profile),})
    return outfits_arr

def get_front_page(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            if request.is_ajax():
                index = request.POST.get("index")
                current_profile = profile.objects.get(user=request.user)
                featured_outfits = get_featured_outfits(current_profile)
                popular_outfits = get_popular_outfits(current_profile)
                new_outfits = get_new_outfits(current_profile)

                print "index = ", index
                json_stuff = json.dumps({"featured": featured_outfits,
                                         "new": new_outfits,
                                         "popular": popular_outfits,})
                return HttpResponse(json_stuff, content_type="application/json")
    return HttpResponse("Error")

def signUpLogIn(request):
    if request.user.is_authenticated():
        #send them to /home
        template = loader.get_template('index.html')
        current_profile = profile.objects.get(user=request.user)

        context = {
            "current_profile": current_profile
        }
    else:
        template = loader.get_template('headerLogin.html')
        context = {
            "asd": "asd"
        }
    return HttpResponse(template.render(context, request))

def about(request):
    template = loader.get_template('about.html')
    context = {}
    return HttpResponse(template.render(context, request))

def contact(request):
    template = loader.get_template('contact.html')


    context = {}
    return HttpResponse(template.render(context, request))

@csrf_exempt
def user_submit_outfit(request):
    if request.is_ajax():
        if request.method == 'POST':
            items = request.POST.getlist('data[]')
            items = json.loads(items[0])
            print "items = ", items['caption']
            if not request.user.is_authenticated:
                print "error: user needs to sign up"
                return HttpResponse("SignUp")
            current_profile = profile.objects.get(user=request.user)
            #create outfit
            new_outfit = outfit(profile=current_profile,
                                gender=items['gender'],
                                description=items['caption'],
                                tags=items['tag'],
                                canvas_height=items['canvasHeight'],
                                canvas_width=items['canvasWidth'])
            new_outfit.save()

            #create outfit items
            for each_item in items['items']:
                current_clothing = clothing.objects.get(carrier_id = each_item['item_id'],
                                                        carrier=each_item['carrier'])
                new_item = outfit_item(clothing=current_clothing,
                                       outfit=new_outfit,
                                       transform_matrix=each_item['transform'],
                                       zIndex=each_item['zIndex'])
                new_item.save()


            json_stuff = json.dumps({"success":"yes"})
            return HttpResponse(json_stuff, content_type="application/json")
    return HttpResponse("Error")

@csrf_exempt
def get_product(request):
    if request.is_ajax():
        if request.method == 'POST':
            cloth_type = request.POST.get('cloth_type')

            # amazon = AmazonAPI('AKIAJOR5NTXK2ERTU6AQ',
            #                    'kck/SKuTJif9bl7qeq5AyB4CU8HWsdz14VW4Iaz2',
            #                    'can037-20',
            #                    region="US")
            # products = amazon.search_n(15, Keywords="Women's " + cloth_type, SearchIndex="Apparel")
            current_gender = request.POST.get('gender')
            if current_gender == 'true':
                current_gender = True
            else:
                current_gender = False
            print "cloth type = ", cloth_type
            print "gender = ", current_gender
            products = clothing.objects.filter(gender=current_gender,
                                              cloth_type=cloth_type,
                                              )
            print "products = ", products
            product_list = []
            for each_product in products:
                if (each_product.small_url is not None) and (each_product.large_url is not None):
                    product_list.append({'small_url': each_product.small_url,
                                         'cloth_type': cloth_type,
                                         'item_id': str(each_product.carrier_id),
                                         'large_url': each_product.large_url,
                                         'carrier': each_product.carrier,
                                         'price': each_product.price,
                                         'brand': each_product.brand})
            json_stuff = json.dumps({"products": product_list,
                                     "cloth_type": cloth_type,
                                     })
            return HttpResponse(json_stuff, content_type="application/json")
    return HttpResponse("Error")

@csrf_exempt
def get_product_full(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                cloth_type = request.POST.get('cloth_type')
                amazon = AmazonAPI('AKIAJOR5NTXK2ERTU6AQ',
                                   'kck/SKuTJif9bl7qeq5AyB4CU8HWsdz14VW4Iaz2',
                                   'can037-20',
                                   region="US")
                products = amazon.search_n(99, Keywords="Women's " + cloth_type, SearchIndex="Apparel")
                product_list = []
                for each_product in products:
                    if each_product.small_image_url is not None:
                        product_list.append({'small_url': each_product.small_image_url,
                                             'cloth_type': cloth_type,
                                             'item_id': str(each_product.asin),
                                             'large_url': each_product.large_image_url,
                                             'carrier': each_product.carrier})
                json_stuff = json.dumps({"products": product_list,
                                         "cloth_type": cloth_type})
                return HttpResponse(json_stuff, content_type="application/json")
            except Exception as e:
                print "Error ", e
    return HttpResponse("Error")

def addNew(request):
    if request.user.is_authenticated():
        template = loader.get_template('addNew.html')
        current_profile = profile.objects.get(user=request.user)
        context = {
        }
    else:
        template = loader.get_template('headerLogin.html')
        context = {
        }
    return HttpResponse(template.render(context, request))

def myCart(request):
    if request.user.is_authenticated():
        template = loader.get_template('myCart.html')
        current_profile = profile.objects.get(user=request.user)
        is_empty = True
        context = {
            "current_profile": current_profile,
            "is_empty": is_empty
        }
    else:
        template = loader.get_template('headerLogin.html')
        context = {
        }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def like_outfit(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            if request.method == 'POST':
                try:
                    outfit_key = request.POST.get('outfit')
                    current_outfit = outfit.objects.get(pk=outfit_key)
                    current_profile = profile.objects.get(user=request.user)
                    try:
                        current_like_obj = profile_likes_outfit.objects.get(profile=current_profile,
                                                                            outfit=current_outfit)
                        current_like_obj.delete()
                        return HttpResponse("Unlike")
                    except Exception as e:
                        current_like_obj = profile_likes_outfit(profile=current_profile,
                                                                outfit=current_outfit)
                        current_like_obj.save()
                        return HttpResponse("Like")
                except Exception as e:
                    print "Error ", e
    return HttpResponse("Error")

@csrf_exempt
def follow_user(request):
    if request.user.is_authenticated():
        if request.is_ajax():
            if request.method == 'POST':
                try:
                    profile_key = request.POST.get('user')
                    current_profile = profile.objects.get(user=request.user)
                    selected_profile = profile.objects.get(pk=profile_key)
                    try:
                        current_follow_obj = profile_follows.objects.get(profile_main=current_profile,
                                                                         profile_following=selected_profile)
                        current_follow_obj.delete()
                        return HttpResponse("Unfollow")
                    except Exception as e:
                        current_follow_obj = profile_follows(profile_main=current_profile,
                                                             profile_following=selected_profile)
                        current_follow_obj.save()
                        return HttpResponse("Follow")
                except Exception as e:
                    print "Error ", e
    return HttpResponse("Error")

def userProfile(request, pk):
    if request.user.is_authenticated():
        template = loader.get_template('userProfile.html')
        current_profile = profile.objects.get(pk=pk)
        all_outfits = outfit.objects.filter(profile=current_profile)
        outfit_number = len(all_outfits)
        current_profile_outfits = get_outfit_items(all_outfits, current_profile)
        context = {
            "current_profile": current_profile,
            "outfit_number": outfit_number,
            "is_self": current_profile.user == request.user,
            "outfits": json.dumps(current_profile_outfits)
        }
    else:
        template = loader.get_template('headerLogin.html')
        context = {
        }
    return HttpResponse(template.render(context, request))


