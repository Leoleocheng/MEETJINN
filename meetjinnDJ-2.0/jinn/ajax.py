def searchajax(list):
    html = ''
    for view in list:
        html = html + '<div class="col-md-4 column"><img src="' + view[
            'scenicspot_img_url'] + '" alt="" style="width: 100%;"><div style="position: absolute; top: 0; left: 0;width: 100%;text-align: center;font-size: 1vw;color: white"><b>' + \
               view['scenicspot_name'] + '</b></div></div>'
    return html


def companionsajax(list):
    html = ''
    for view in list:
        html = html + '<a href="/travelnotes/?data=' + str(
            view['companions_id']) + '"><div class="col-md-3 col-6 column"><img src="' + view[
                   'companions_img_url'] + '" alt="" width="100%"><hr><h4>' + view[
                   'city_name'] + '</h4><span style="font-size: 12px">' + view[
                   'companions_title'] + '</span><br><table><tr><td><img src="' + view[
                   'user_img'] + '" class="round_icon" alt=""></td><td><span style="color: red;font-size: 20px">' + \
               view['user_name'] + '</span></td></tr></table>期望人数' + str(
            view['companions_people_expect']) + '，' + str(view['companions_people']) + '人已报名</div></a>'
    return html


def regionajax1():
    for i in range(5):
        str1 = '''<table id="tab1"><tr><td></td><td rowspan="4"><img src="''' + list1[i]['scenicspot_img_url'] + '''" alt=""></td></tr><tr><td>
                    <h4>''' + str(i + 1) + ' ' + list1[i]["scenicspot_name"] + '''</h4><br>''' + list1[i][
            'md'] + '''</td></tr><tr><td></td></tr></table><hr>'''
        list = list + str1
    list = list + '</div></div>'
