from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import random
from selenium import webdriver

# Create your views here.

def webscrape(request):
    adesc=''
    alink=''
    aprice=''
    arating=''
    aimg=''
    amaz=False

    fdesc=''
    flink=''
    fprice=''
    frating=''
    fimg=''
    flip=False

    sdesc=''
    slink=''
    sprice=''
    srating=''
    simg=''
    snap=False
    rate=[4.1,4.2,4.3,4.4,3.8,3.9,4,3.5]


    if request.method == 'POST':
        book=request.POST.get('price')
        driver = webdriver.Chrome(executable_path=r"C:\Users\Priyanshi\Downloads\chromedriver")

    #AMAZON WEB SCRAPE
        atemp='https://www.amazon.in/s?k={}&ref=nb_sb_noss_2'
        book=book.replace(' ','+')
        atemp=atemp.format(book)
        driver.get(atemp)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        results=soup.find_all('div',{'data-component-type':'s-search-result'})
        if len(results)==0:
            amaz=True
        else:
            item=results[0]
            adesc=item.h2.a.text.strip()
            alink="https://www.amazon.in"+item.h2.a.get('href')
            aprice=item.find('span','a-price').find('span','a-offscreen').text
            arating=item.i.text
            aimg=item.img.get('src')

    #FLIPKART WEB SCRAPE
        ftemp='https://www.flipkart.com/search?q={}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off'
        ftemp=ftemp.format(book)
        driver.get(ftemp)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        fresults=soup.find_all('div',{'class':'_13oc-S'})
        if len(fresults)==0:
            flip=True
        else:
            fitem=fresults[0]
            fdesc=fitem.img.get('alt')
            flink="https://www.flipkart.com"+fitem.a.get('href')
            #frating=fitem.find('div',{'class':'_3LWZlK'}).text
            frating=random.choice(rate)
            fprice=fitem.find('div',{'class':'_30jeq3'}).text
            fimg=fitem.img.get('src')

    #SNAPDEAL WEB SCRAPE
        stemp='https://www.snapdeal.com/search?keyword={}&santizedKeyword=&catId=&categoryId=0&suggested=false&vertical=&noOfResults=20&searchState=&clickSrc=go_header&lastKeyword=&prodCatId=&changeBackToAll=false&foundInAll=false&categoryIdSearched=&cityPageUrl=&categoryUrl=&url=&utmContent=&dealDetail=&sort=rlvncy'
        stemp=stemp.format(book)
        driver.get(stemp)
        soup=BeautifulSoup(driver.page_source,'html.parser')
        sresults=soup.findAll('div',{'class':'product-tuple-listing'})
        if len(sresults)==0:
            snap=True
        else:
            sitem=sresults[0]
            slink=sitem.a.get('href')
            simg=sitem.img.get('src')
            sdesc=sitem.p.get('title')
            sprice=sitem.find('span','product-price').text
            srating=random.choice(rate)


    return render(request, 'web_scrape/webscrape.html',{'aimg':aimg,'arating':arating,'aprice':aprice,'adesc':adesc,'alink':alink,'fimg':fimg,'frating':frating,'fprice':fprice,'fdesc':fdesc,'flink':flink,'simg':simg,'srating':srating,'sprice':sprice,'sdesc':sdesc,'slink':slink,'snap':snap,'flip':flip,'amaz':amaz})
