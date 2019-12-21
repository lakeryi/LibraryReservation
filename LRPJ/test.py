from django.http import HttpResponse
from django.shortcuts import render

def hello(request):
    return HttpResponse("Hello world ! ")

def input(request):
    str = "<form action=\"/search\" method=\"get\">\
        row   : <input type=\"text\" name=\"row\"><br>\
        column: <input type=\"text\" name=\"column\"><br>\
        <input type=\"submit\" value=\"submit\">\
        </form>"
    context = {}
    stu_list = [{'name':'a','student_id':123,'major':'cs'},{'name':'a','student_id':12,'major':'cs'},{'name':'a','student_id':1,'major':'cs'}]
    context['stu_list'] = stu_list
    # context['row'] = [0,1,2]
    # context['column'] = [0,1,2,3,4]
    # context['rows'] = [0,1,1,2]
    # context['columns'] = [0,2,3,4]
    # context['loc'] = [(0,0),(1,2),(1,3),(2,4)]
    # context['seat_num'] = [0,1,2,3]
    location = [(0,0),(1,2),(1,3),(2,4),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9)]

    one_seat_free = "<li><form action=\"/choose\" method=\"POST\" name=\"sentMessage\" id=\"contactForm\">\
                        <div class=\"w3_grid_effect_\">\
                        <span class=\"cbp-ig-icon_ w3_cube\" onclick=\"javascript:print_user_info(1)\"></span>\
                        <button name = \"id\"  value = 1 class=\"cbp-ig-category\">{{ seat.seat1 }}</button>\
                        </div>\
                </form></li>"
    one_seat_busy = "<li><form action=\"/choose\" method=\"POST\" name=\"sentMessage\" id=\"contactForm\">\
                            <div class=\"w3_grid_effect\">\
                                <span class=\"cbp-ig-icon w3_cube\" onclick=\"javascript:print_user_info(1)\"></span>\
                                <button name = \"id\"  value = 1 class=\"cbp-ig-category\">Free</button>\
                            </div>\
                    </form></li>"

    no_seat = "<li><form action=\"/choose\" method=\"POST\" name=\"sentMessage\" id=\"contactForm\">\n\
                        <div class=\"w3_grid_effect_space\">\n\
                        <span class=\"cbp-ig-icon_ w3_road\" onclick=\"javascript:print_user_info(1)\"></span>\n\
                        </div>\n\
                </form></li>"
    part = ""
    seat_available=[0]*100
    for r in range(10):
        part = part+"<ul class=\"cbp-ig-grid\">"
        for c in range(10):
            if (r,c) in location:
                if seat_available[r*10+c]:
                    part = part + one_seat_free
                else:
                    part = part+one_seat_busy

            else:
                part = part + no_seat
        part = part+"</ul>"

    context['part'] = part

    return render(request, 'book_seat_int.html',context)#HttpResponse(str)

def generate_form_unit(attr):
    form = "<form "
    if attr['if_last'] == 0:
        form = form + "style=\"float:left;\" "
    form = form + "action=\"/generate_seat\" method=\"get\">\
                    <input type=\"submit\" value=\"" + attr['value'] + "\" name = \"" + attr['name'] + "\"></form>"
    return form
output_form_list = []
seat_location = []
r = -1
c = -1
def search(request):
    global r
    global c
    global output_form_list
    global seat_location
    seat_location = []
    request.encoding='utf-8'
    if 'row' in request.GET and request.GET['row']:
        r = int(request.GET['row'])
    else:
        r = -1
    if 'column' in request.GET and request.GET['column']:
        c = int(request.GET['column'])
    else:
        c = -1
    one_submit_attr = {}
    output_form_list = []

    output = ""
    for i in range(r):
        for j in range(c-1):
            one_submit_attr['if_last'] = 0
            one_submit_attr['value'] = str(i)+"-"+str(j)
            one_submit_attr['name'] = "submit"+str(i)+"-"+str(j)

            output = output + generate_form_unit(one_submit_attr)
            output_form_list.append(generate_form_unit(one_submit_attr))
        j=j+1
        one_submit_attr['if_last'] = 1
        one_submit_attr['value'] = str(i) + "-" + str(j)
        one_submit_attr['name'] = "submit" + str(i) + "-" + str(j)
        output = output+generate_form_unit(one_submit_attr)
        output_form_list.append(generate_form_unit(one_submit_attr))

    output = output + "<form action=\"/final_map\" method=\"get\">\
                                        <input type=\"submit\" value=\"submit your map\">\
                                        </form>"
    print("****",output_form_list)
    return HttpResponse(output)


def generate_seat(request):
    request.encoding = 'utf-8'

    global output_form_list
    global seat_location
    print("----",output_form_list)

    for i in range(r):
        for j in range(c):
            expect = "submit" + str(i) + "-" + str(j)
            if expect in request.GET and request.GET[expect]:
                seat_location.append({'r':i,"c":j})
                if j != c-1:
                    output_form_list[i*c+j]="<form style=\"float:left;\" action=\"/generate_seat\" method=\"get\">\
                    <input type=\"submit\" value=\"selected\">\
                    </form>"
                else:
                    output_form_list[i * c + j] = "<form action=\"/generate_seat\" method=\"get\">\
                                        <input type=\"submit\" value=\"selected\">\
                                        </form>"
                break
    output = ""
    for form in output_form_list:
        output = output + form

    output = output + "<form action=\"/final_map\" method=\"get\">\
                                            <input type=\"submit\" value=\"submit your map\">\
                                            </form>"


    return HttpResponse(output)


def final_map(request):
    output_form_list = []
    one_seat = "<li><form action=\"/choose\" method=\"POST\" name=\"sentMessage\" id=\"contactForm\">\
                        {% csrf_token %}\
                        {% if request.session.seat.seat1 %}\
                        <div class=\"w3_grid_effect_\">\
                            <span class=\"cbp-ig-icon_ w3_cube\" onclick=\"javascript:print_user_info(1)\"></span>\
                            <button name = 'id'  value = 1 class=\"cbp-ig-category\">{{ seat.seat1 }}</button>\
                        </div>\
                        {% else %}\
                        <div class=\"w3_grid_effect\">\
                            <span class=\"cbp-ig-icon w3_cube\" onclick=\"javascript:print_user_info(1)\"></span>\
                            <button name = 'id'  value = 1 class=\"cbp-ig-category\">闲置座位</button>\
                        </div>\
                        {% endif %}\
                    </form></li>"
    no_seat = "<li><form action=\"/choose\" method=\"POST\" name=\"sentMessage\" id=\"contactForm\">\
                        {% csrf_token %}\
                        {% if request.session.seat.seat1 %}\
                        <div class=\"w3_grid_effect_\">\
                            <span class=\"cbp-ig-icon_ w3_road\"></span>\
                        </div>\
                        {% else %}\
                        <div class=\"w3_grid_effect\">\
                            <span class=\"cbp-ig-icon w3_road\"></span>\
                        </div>\
                        {% endif %}\
                    </form></li>"
    output_form_list.append("<div class=\"w3ls_banner_bottom_grids\">")

    for i in range(r):
        output_form_list.append("<ul class =\"cbp-ig-grid\">")
        for j in range(c):
            loc = {'r':i, 'c':j}
            if loc in seat_location:
                output_form_list.append(one_seat)
            else:
                output_form_list.append(no_seat)
        output_form_list.append("</ul>")

    output_form_list.append("</div>")
    head = "<!DOCTYPE html>\
            <html lang=\"en\">\
            <head>\
            <title>座位预约</title>\
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\
            <meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />\
            <meta name=\"keywords\" content=\"\" />\
            <script type=\"application/x-javascript\">\
                addEventListener(\"load\", function() {\
                setTimeout(hideURLbar, 0);\
                }, false);\
                function hideURLbar() {\
                    window.scrollTo(0, 1);\
                }\
            </script>\
    <link href=\"/static/css/bootstrap.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" />\
    <link href=\"/static/css/font-awesome.css\" rel=\"stylesheet\">\
    <link rel=\"stylesheet\" href=\"/static/css/chocolat.css\" type=\"text/css\" media=\"screen\">\
    <link href=\"/static/css/easy-responsive-tabs.css\" rel='stylesheet' type='text/css' />\
    <link rel=\"stylesheet\" href=\"/static/css/flexslider.css\" type=\"text/css\" media=\"screen\" property=\"\" />\
    <link rel=\"stylesheet\" href=\"/static/css/jquery-ui.css\" />\
    <link href=\"/static/css/style.css\" rel=\"stylesheet\" type=\"text/css\" media=\"all\" />\
    <script type=\"text/javascript\" src=\"/static/js/modernizr-2.6.2.min.js\"></script>\
    <link href=\"http://fonts.googleapis.com/css?family=Oswald:300,400,700\" rel=\"stylesheet\">\
    <link href=\"http://fonts.googleapis.com/css?family=Federo\" rel=\"stylesheet\">\
</head>\
<body>\
    <script type=\"text/javascript\">\
        function print_user_info(pos) {\
            var data = [\"{{ user_info.login }}\", \
            \"{{ user_info.seat1 }}\", \"{{ user_info.seat2 }}\", \"{{ user_info.seat3 }}\", \"{{ user_info.seat4 }}\", \"{{ user_info.seat5 }}\", \"{{ user_info.seat6 }}\",];\
            var info = data[pos]\
            info = info.replace(/WangSaWangSaORZORZWangSaWangSa/g, \"\n\");\
            alert(info);\
        }\
    </script>\
    <div class=\"banner-bottom\">\
        <div class=\"container\">\
            <div class=\"w3ls_banner_bottom_grids\">\
                    <ul class=\"cbp-ig-grid_\">\
                        <li>\
                            <div class=\"w3_grid_effect_\">\
                                <script type=\"text/javascript\">\
                                    function logout() {\
                                        window.location.href = \"/logout\";}</script>  \
                                <p class=\"cbp-ig-category_\">热爱学习的你</p>\
                                <span class=\"cbp-ig-icon_ w3_cube\" onclick=\"javascript:print_user_info(0)\"></span>\
                                <button class=\"cbp-ig-category_\" onclick=\"javascript:logout()\">&#8195登&#8195&#8194出&#8195</button>\
                            </div>\
                        </li>\
                    </ul>\
            </div>\
            <div class=\"agileits_banner_bottom\">\
                <h3><span>预约一个闲置的位置，开始一天愉快的自习吧</span>最下面是你可能感兴趣的人</h3>\
            </div>"
    tail = "</div>\
    </div>\
    </body>\
</html>"

    output_str = head
    for f in output_form_list:
        output_str = output_str + f
    output_str = output_str + tail

    print(output_str)


    return HttpResponse(output_str)