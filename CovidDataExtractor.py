from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

mylist = []
link = "https://covid19.mohp.gov.np/"
js = '''return document.getElementsByClassName("ant-card-grid ant-card-grid-hoverable")'''

# configuration of selenium driver
def configure_firefox_driver():
    # Add additional Options to the webdriver
    firefox_options = webdriver.FirefoxOptions()
    # add the argument and make the browser Headless.
    firefox_options.headless = False
    driver = webdriver.Firefox(executable_path="C:\\Users\Prayush\Downloads\geckodriver-v0.29.1-win64\geckodriver.exe",
                               options=firefox_options)
    return driver

# calling driver
driver = configure_firefox_driver()

# getting data from the list generated by selenium and changing it to dictionary
def getdatafromlist(mylist):
    districtname = []
    districttotal = []
    districtmale = []
    districtfemale = []
    for districtsdata in mylist:
        splitted = str(districtsdata).split("\n")
        districtname.append(splitted[0])
        districttotal.append(splitted[1])
        districtmale.append(splitted[2])
        districtfemale.append(splitted[3])
    distobj = zip(districtname, districttotal)
    dictionaryof = dict(distobj)
    return dictionaryof

def gettodaydata(totalpcr, totalinfected, newcases):
    yesterdayread = open("C:\\Users\Prayush\Desktop\CovidCases\yesterdaycases.txt", "r")
    contnents = yesterdayread.read()
    dlist = list(contnents.split("\n"))

    yesterdaytotalpcr = dlist[0]
    yesterdayinfected = dlist[1]
    yesterdayrecovered = dlist[2]
    yesterdaydead = dlist[3]
    yesterdaypcr = dlist[4]
    yesterdaypercent = dlist[5]

    print(yesterdaypcr)
    if (yesterdaytotalpcr == totalpcr):
        print("Data Not Updated")
        yesterdayread.close()
        return

    #Updating the percentage increased of decreased
    else:
        yesterdaywrite = open("C:\\Users\Prayush\Desktop\CovidCases\yesterdaycases.txt", "w")
        today_pcr = int(totalpcr) - int(yesterdaytotalpcr)
        yesterdaywrite.write(totalpcr)
        yesterdaywrite.write("\n")
        yesterdaywrite.write(yesterdayinfected)
        yesterdaywrite.write("\n")
        yesterdaywrite.write(yesterdayrecovered)
        yesterdaywrite.write("\n")
        yesterdaywrite.write(yesterdaydead)
        yesterdaywrite.write("\n")
        yesterdaywrite.write(yesterdaypcr)
        yesterdaywrite.write("\n")
        yesterdaywrite.write(yesterdaypercent)

        contaminatedpercent = (int(newcases) / today_pcr) * 100
        print(today_pcr)
        print(contaminatedpercent)
        datalist = []
        datalist.append(today_pcr)
        datalist.append(round(contaminatedpercent))
        datalist.append(yesterdayinfected)
        datalist.append(yesterdayrecovered)
        datalist.append(yesterdaydead)
        datalist.append(yesterdaypcr)
        datalist.append(yesterdaypercent)

        return datalist

# getting all data from the site
def getdata(driver):
    today_date = getdate()
    try:
        driver.get(link)
        sleep(60)
        newcases = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div[1]/div/div/p[1]").text
        recoveredcases = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div[2]/div/div/p[1]").text
        deaths = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[2]/div[2]/div[3]/div/div/p[1]").text
        totalinfected = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[2]/div[2]/div/div/p[1]").text
        totalpcr = driver.find_element_by_xpath("/html/body/div[2]/div[1]/div[3]/div[3]/div[1]/div/div/span[2]").text

        startdate = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[6]/div/div[1]/input")
        enddate = driver.find_element_by_xpath("/html/body/div[2]/div[3]/div[6]/div/div[3]/input")
        #filtering start date and end date to get just todays data
        startdate.send_keys(today_date)
        enddate.send_keys(today_date)
        print(f'''Data from {startdate.get_attribute("value")} to {enddate.get_attribute("value")}''')
        enddate.send_keys(Keys.ENTER)
        sleep(30)
        html = driver.execute_script(js)
        for h in html:
            print("-------------------")
            print(h.text)
            mylist.append(h.text)

        #I created a function getdatafromlist(mylist) that extracted the data into dictionary for easy handling
        dictionaryof = getdatafromlist(mylist)
        print(dictionaryof)
        datalist = gettodaydata(totalpcr, totalinfected, newcases)
        todaypcr = datalist[0]
        contaminatedpercent = datalist[1]
        yesterdayinfected = datalist[2]
        yesterdayrecovered = datalist[3]
        yesterdaydead = datalist[4]
        yesterdaypcr = datalist[5]
        yesterdaypercent = datalist[6]

        #using pillow to print the images
        printimage(dictionaryof, todaypcr, contaminatedpercent, newcases, recoveredcases, deaths, yesterdayinfected,
                   yesterdayrecovered, yesterdaydead, yesterdaypcr, yesterdaypercent)


    except Exception as E:
        print(f'Error {E}')

    finally:
        driver.close()

# getting current date
def getdate():
    date = str(datetime.now()).split(" ")[0]
    return date

filename = "C:\\Users\Prayush\Desktop\CovidCases\cases" + getdate() + ".JPG"
filenamesecond = "C:\\Users\Prayush\Desktop\CovidCases\casessecond" + getdate() + ".JPG"

def printimage(dictionaryof, todaypcr, contaminatedpercent, newcases, recoveredcases, death, yesterdayinfected,
               yesterdayrecovered, yesterdaydead, yesterdaypcr, yesterdaypercent):
    image = Image.open("covidtry.jpg").convert('RGB')
    image2 = Image.open("covid3.jpg").convert('RGB')
    ktmtext = "Kathmandu\n      " + dictionaryof["KATHMANDU"].split(" ")[1]
    lallittext = "Lalitpur\n   " + dictionaryof["LALITPUR"].split(" ")[1]
    bkttext = "Bhaktapur\n      " + dictionaryof["BHAKTAPUR"].split(" ")[1]
    district = list(dictionaryof.keys())
    count = list(dictionaryof.values())

    print(todaypcr)
    changeinfected = int(newcases) - int(yesterdayinfected)
    changerecovered = int(recoveredcases) - int(yesterdayrecovered)
    changedead = int(death) - int(yesterdaydead)
    changepcr = int(yesterdaypcr) - int(todaypcr)
    changepercent = int(yesterdaypercent) - int(contaminatedpercent)

    font_type = ImageFont.truetype("sb.otf", 45)
    font_typeLalitpur = ImageFont.truetype("sb.otf", 45)
    font_typeBhaktapur = ImageFont.truetype("sb.otf", 36)
    font_typedata = ImageFont.truetype("sb.otf", 46)
    font_typedata2 = ImageFont.truetype("sb.otf", 35)
    font_typedata3 = ImageFont.truetype("sb.otf", 30)


    draw = ImageDraw.Draw(image)
    updated = "UPDATED : " + getdate()
    draw.text(xy=(190, 550), text=ktmtext, fill=(13, 13, 13), font=font_type)
    draw.text(xy=(214, 1000), text=lallittext, fill=(13, 13, 13), font=font_typeLalitpur)
    draw.text(xy=(376, 695), text=bkttext, fill=(13, 13, 13), font=font_typeBhaktapur)
    draw.text(xy=(810, 1175), text=str(newcases), fill=(255, 255, 255), font=font_typedata)
    draw.text(xy=(810, 1241), text=str(recoveredcases), fill=(255, 255, 255), font=font_typedata)
    draw.text(xy=(810, 1309), text=str(death), fill=(255, 255, 255), font=font_typedata)
    draw.text(xy=(810, 1377), text=str(todaypcr),fill=(255, 255, 255), font=font_typedata)
    draw.text(xy=(810, 1447), text=str(str(contaminatedpercent) + "%"), fill=(255, 255, 255), font=font_typedata)
    draw.text(xy=(548, 1028), text=updated, fill=(255, 255, 255), font=font_typedata)


#Introducting a dynamic aspect to the code on the basis on change infected.
    if changeinfected > 0:
        draw.text(xy=(925, 1175), text=str("+ "+str(changeinfected)), fill=(255,0,0), font=font_typedata2)

    elif changeinfected == 0:
        draw.text(xy=(925, 1175), text=str(str(changeinfected)), fill=(13, 13, 13), font=font_typedata2)

    else:
        draw.text(xy=(925, 1175), text=str(str(changeinfected)), fill=(0,154,23), font=font_typedata2)

    if changerecovered > 0:
        draw.text(xy=(920, 1241), text=str("+ " + str(changerecovered)), fill=(0,154,23), font=font_typedata2)

    elif changerecovered == 0:
        draw.text(xy=(920, 1241), text=str(str(changerecovered)), fill=(13, 13, 13), font=font_typedata2)

    else:
        draw.text(xy=(920, 1241), text=str(str(changerecovered)), fill=(255,0,0), font=font_typedata2)

    if changedead > 0:
        draw.text(xy=(920, 1309), text=str("+ " + str(changedead)), fill=(255,0,0) , font=font_typedata2)

    elif changedead == 0:
        draw.text(xy=(920, 1309), text=str(str(changedead)), fill=(13, 13, 13), font=font_typedata2)

    else:
        draw.text(xy=(920, 1309), text=str(str(changedead)), fill=(0,154,23), font=font_typedata2)

    if changepcr > 0:
        draw.text(xy=(955, 1377), text=str("+ " + str(changepcr)), fill=(255,0,0), font=font_typedata2)

    elif changepcr == 0:
        draw.text(xy=(955, 1377), text=str(str(changepcr)), fill=(13, 13, 13), font=font_typedata2)

    else:
        draw.text(xy=(955, 1377), text=str(str(changepcr)), fill=(0,154,23), font=font_typedata2)

    # if changepercent > 0:SS
    #     draw.text(xy=(920, 1447), text=str("+ " + str(changeinfected) + "%"), fill=(255,0,0), font=font_typedata2)
    #
    # elif changepercent == 0:
    #     draw.text(xy=(920, 1447), text=str(str(changeinfected) + "%"), fill=(13, 13, 13), font=font_typedata2)
    #
    # else:
    #     draw.text(xy=(920, 1447), text=str(str(contaminatedpercent) + "%"), fill=(0,154,23), font=font_typedata2)

    y_cordinate = 228
    x_cordinate = 46
    x_cordinatesecondrow = 429
    y_cordinatesecondrow = 228
    x_cordinatethirdrow = 759
    y_cordinatethirdrow = 228
    print(len(district))
    draw2 = ImageDraw.Draw(image2)
    for i in range(len(district)):

        print(count[i])
        counno = count[i].split()
        finaltext = district[i] + " - " + str(counno[1])
        if i > 66:
            draw2.text(xy=(x_cordinatethirdrow, y_cordinatethirdrow), text=finaltext, fill=(255, 255, 255), font=font_typedata3)
            y_cordinatethirdrow = y_cordinatethirdrow + 47

        elif i > 33:
            draw2.text(xy=(x_cordinatesecondrow, y_cordinatesecondrow), text=finaltext, fill=(255, 255, 255), font=font_typedata3)
            y_cordinatesecondrow = y_cordinatesecondrow + 47

        else:
            draw2.text(xy=(x_cordinate, y_cordinate), text=finaltext, fill=(255, 255, 255), font=font_typedata3)
            y_cordinate = y_cordinate + 47

    image.show()
    image2.show()
    image.save(filename)
    image2.save(filenamesecond)


getdata(driver)


def printimage2():
    image = Image.open("covid3.jpg")
    ktmtext = "Kathmandu\n      " + "2788"
    lallittext = "Lalitpur\n   " + "602"
    bkttext = "Bhaktapur\n      " + "537"
    updated = "UPDATED : " + getdate()
    reobj = {'JAJARKOT': 'Total: 23', 'TANAHU': 'Total: 14', 'LAMJUNG': 'Total: 5', 'GULMI': 'Total: 18',
             'RUPANDEHI': 'Total: 771', 'KAILALI': 'Total: 389', 'JHAPA': 'Total: 300', 'BHAKTAPUR': 'Total: 226',
             'SYANGJA': 'Total: 71', 'DOTI': 'Total: 73', 'MANANG': 'Total: 28', 'MAKWANPUR': 'Total: 183',
             'KASKI': 'Total: 235', 'RAUTAHAT': 'Total: 45', 'SANKHUWASABHA': 'Total: 32', 'MAHOTTARI': 'Total: 25',
             'KATHMANDU': 'Total: 3250', 'LALITPUR': 'Total: 448', 'KHOTANG': 'Total: 3', 'DADELDHURA': 'Total: 39',
             'ACHHAM': 'Total: 68', 'NAWALPARASI EAST': 'Total: 57', 'MORANG': 'Total: 360', 'SINDHULI': 'Total: 44',
             'PARSA': 'Total: 78', 'CHITAWAN': 'Total: 204', 'DAILEKH': 'Total: 37', 'BANKE': 'Total: 287',
             'KAPILBASTU': 'Total: 25', 'SARLAHI': 'Total: 16', 'NUWAKOT': 'Total: 67', 'ARGHAKHANCHI': 'Total: 37',
             'PYUTHAN': 'Total: 10', 'SAPTARI': 'Total: 22', 'PALPA': 'Total: 121', 'GORKHA': 'Total: 23',
             'ILAM': 'Total: 8', 'SUNSARI': 'Total: 130', 'MYAGDI': 'Total: 42', 'DHANUSA': 'Total: 115',
             'SOLUKHUMBU': 'Total: 1', 'UDAYAPUR': 'Total: 9', 'SURKHET': 'Total: 221', 'BAITADI': 'Total: 199',
             'RASUWA': 'Total: 15', 'SINDHUPALCHOK': 'Total: 14', 'KANCHANPUR': 'Total: 31', 'SALYAN': 'Total: 10',
             'KALIKOT': 'Total: 25', 'ROLPA': 'Total: 5', 'SIRAHA': 'Total: 17', 'RAMECHHAP': 'Total: 14',
             'DHADING': 'Total: 52', 'TAPLEJUNG': 'Total: 2', 'DANG': 'Total: 277', 'NAWALPARASI WEST': 'Total: 45',
             'KAVREPALANCHOK': 'Total: 108', 'PARBAT': 'Total: 13', 'RUKUM WEST': 'Total: 6', 'DOLAKHA': 'Total: 11',
             'DARCHULA': 'Total: 78', 'PANCHTHAR': 'Total: 1', 'DHANKUTA': 'Total: 6', 'BARDIYA': 'Total: 44',
             'BARA': 'Total: 24', 'BHOJPUR': 'Total: 35', 'MUSTANG': 'Total: 27', 'JUMLA': 'Total: 5',
             'BAJURA': 'Total: 3', 'BAGLUNG': 'Total: 5', 'TERHATHUM': 'Total: 2', 'OKHALDHUNGA': 'Total: 2',
             'DOLPA': 'Total: 1', 'BAJHANG': 'Total: 1'}
    district = list(reobj.keys())
    count = list(reobj.values())

    font_type = ImageFont.truetype("sb.otf", 45)
    font_typeLalitpur = ImageFont.truetype("sb.otf", 45)
    font_typeBhaktapur = ImageFont.truetype("sb.otf", 36)
    font_typedata = ImageFont.truetype("sb.otf", 38)
    font_typedata2 = ImageFont.truetype("sb.otf", 30)

    draw = ImageDraw.Draw(image)

    y_cordinate = 228
    x_cordinate = 46
    x_cordinatesecondrow = 429
    y_cordinatesecondrow = 228
    x_cordinatethirdrow = 759
    y_cordinatethirdrow = 228
    print(len(district))
    for i in range(len(district)):

        print(count[i])
        counno = count[i].split()
        finaltext = district[i] + " - " + str(counno[1])
        if i > 66:
            draw.text(xy=(x_cordinatethirdrow, y_cordinatethirdrow), text=finaltext, fill=(255), font=font_typedata2)
            y_cordinatethirdrow = y_cordinatethirdrow + 47

        elif i > 33:
            draw.text(xy=(x_cordinatesecondrow, y_cordinatesecondrow), text=finaltext, fill=(255), font=font_typedata2)
            y_cordinatesecondrow = y_cordinatesecondrow + 47

        else:
            draw.text(xy=(x_cordinate, y_cordinate), text=finaltext, fill=(255), font=font_typedata2)
            y_cordinate = y_cordinate + 47

    image.show()
    image.save(filename)

# printimage2()
