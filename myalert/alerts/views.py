from .forms import SubmitForm, EditForm
from django.template import RequestContext
from django.http import HttpResponse,request
from .models import submittal
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.contrib.auth import logout
from django.contrib import messages
from django.utils.safestring import mark_safe
from datetime import date
import io
import os
from django.template.loader import get_template
from django.views.generic import View
from io import BytesIO
from django.http import HttpResponse,HttpResponseRedirect
from django.http import FileResponse
from PIL import Image
from django.shortcuts import render
from django.conf import settings
import django_tables2 as tables
from django_tables2 import RequestConfig
from .table import alertrecs
import colorama
from colorama import Fore, Style
from django.core.mail import send_mail
from myalert.functions import handle_uploaded_file


def testform():

    initialdict = {'submitted':'2021-12-01','urgency':'normal','title':'test alert message','lname':'Higgins',
                   'fname':'Peter','affiliation':'none', 'contact':'higgins41@icloud.com','startdate':'2021-12-10',
                   'enddate':'2021-12-30','justification':'testing','instructions':'make observations','notes':'none',
                   'table':'stars.jpg','HR': 'on', 'variability': 'Cataclysmic Variable (CV)',
                    'wavelengths': '4000-10000/A', 's1': 'VY Scl'}

    form=SubmitForm(initial=initialdict)
    return form

def makeeditform(dt):
    initialdict = {'submitted': dt.submitted, 'urgency': dt.urgency, 'title': dt.title, 'lname': dt.lname,
                   'fname': dt.fname, 'affiliation': dt.affiliation,'annum':dt.annum,
                   'contact': dt.contact, 'status': dt.status, 'approved': dt.approved, 'priority': dt.priority,
                   'startdate': dt.startdate, 'enddate': dt.enddate, 'justification': dt.justification,
                   'instructions': dt.instructions, 'notes': dt.notes, 'feedback': dt.feedback, 'forums':dt.forums,'table': dt.table,
                   'TS': dt.TS, 'HR': dt.HR, 'NI': dt.NI, 'WK': dt.WK, 'MO': dt.MO,
                   'spectroscopy': dt.spectroscopy, 'wavelengths': dt.wavelengths,
                   'Vp': dt.Vp, 'Cp': dt.Cp, 'Dp': dt.Dp, 'Pp': dt.Pp, 'CT': dt.CT, 'EB': dt.EB, 'XP': dt.XP,
                   'HE': dt.HE, 'LV': dt.LV, 'SP': dt.SP, 'SO': dt.SO,
                   'U': dt.U, 'B': dt.B, 'V': dt.V, 'R': dt.R, 'I': dt.I, 'uu': dt.uu, 'g': dt.g, 'rr': dt.rr,
                   'l': dt.l, 'z': dt.z, 'cv': dt.cv, 'cr': dt.cr,
                   's1': dt.s1, 's2': dt.s2, 's3': dt.s3, 's4': dt.s4, 's5': dt.s5, 's6': dt.s6, 's7': dt.s7,
                   's8': dt.s8, 's9': dt.s9, 's10': dt.s10, 's11': dt.s11, 's12': dt.s12,
                   's13': dt.s13, 's14': dt.s14, 's15': dt.s15, 's16': dt.s16, 's17': dt.s17, 's18': dt.s18,
                   's19': dt.s19, 's20': dt.s20,
                   's21': dt.s21, 's22': dt.s22, 's23': dt.s23, 's24': dt.s24, 's25': dt.s25}

    form=EditForm(initial=initialdict)
    return form


def makeform(dt):

    initialdict = {'submitted':dt.submitted,'urgency':dt.urgency,'title':dt.title,'lname':dt.lname,'fname':dt.fname,'affiliation':dt.affiliation,
                   'contact':dt.contact,'status':dt.status,'approved':dt.approved,'priority':dt.priority,'startdate':dt.startdate,'enddate':dt.enddate,'justification':dt.justification,
                   'instructions':dt.instructions,'notes':dt.notes,'feedback':dt.feedback,'forums':dt.forums,'table':dt.table,
                   'TS':dt.TS,'HR':dt.HR,'NI':dt.NI,'WK':dt.WK,'MO':dt.MO,
                   'spectroscopy':dt.spectroscopy,'wavelengths':dt.wavelengths,
                   'Vp':dt.Vp, 'Cp':dt.Cp, 'Dp': dt.Dp, 'Pp':dt.Pp,'CT':dt.CT,'EB':dt.EB,'XP':dt.XP,'HE':dt.HE,'LV':dt.LV,'SP':dt.SP,'SO':dt.SO,
                   'U':dt.U,'B':dt.B,'V':dt.V,'R':dt.R,'I':dt.I,'uu':dt.uu,'g':dt.g,'rr':dt.rr,'l':dt.l,'z':dt.z,'cv':dt.cv,'cr':dt.cr,
                   's1': dt.s1, 's2': dt.s2, 's3': dt.s3, 's4': dt.s4, 's5': dt.s5, 's6': dt.s6, 's7': dt.s7,
                   's8': dt.s8, 's9': dt.s9, 's10': dt.s10, 's11': dt.s11, 's12': dt.s12,
                   's13':dt.s13, 's14':dt.s14, 's15':dt.s15, 's16':dt.s16, 's17':dt.s17, 's18':dt.s18, 's19':dt.s19, 's20':dt.s20,
                   's21':dt.s21, 's22':dt.s22, 's23':dt.s23, 's24':dt.s24, 's25':dt.s25}


    form=SubmitForm(initial=initialdict)
    return form

def lout(request):
    print("in logout")
    logout(request)
    return HttpResponse('logged out')

@login_required
def menu(request):
    if request.method == 'POST':
        
        if "lout" in request.POST:
            print("in logout")
            logout(request)
            return HttpResponse('logged out')   

        if "screate" in request.POST:
            form = SubmitForm() #used in production, produces blank form
            #form = testform() #used for testing form with values
            return render(request, "message2.html", {'form': form})
        
        if "sdelete" in request.POST:
            print("alertmenu/delete")
            pks = request.POST.getlist("selection")
            print('pks', pks)
            sid = int(pks[0])
            print("sid", sid)
            try:
                submittal.objects.get(pk=sid).delete()
                submitmsg = "You have sucessfully deleted this submittal"
                messages.success(request, submitmsg)
            except:
                submitmsg = "no record checked"
                messages.success(request, submitmsg)

            table = alertrecs(submittal.objects.all())
            print("in home table")
            RequestConfig(request).configure(table)
            return render(request, 'recordstaff.html', {'table': table})

        if "sview" in request.POST:
            try:
                pks = request.POST.getlist("selection")
                request.session['editrec'] = pks
                sid = int(pks[0])
                dt = submittal.objects.get(id=sid)
                form = makeeditform(dt)
                return render(request, "smessage.html", {'form': form})
            except:
                submitmsg = "no record selected."
                messages.success(request, submitmsg)

        def upload_file(form):
            print("in upload file")
            #form = SubmitForm(request.POST, request.FILES)
            if form.is_valid():
                handle_uploaded_file(request.FILES['graphic'])
                return HttpResponseRedirect('/success/url/')
            else:
                form = SubmitForm()
            return render(request, 'message2.html', {'form': form})

        if "new" in request.POST:
            print("in new")
            sform = SubmitForm(request.POST, request.FILES)
            et=sform.errors
            print("et",et)
            rqp = request.POST
            title = rqp.get('title');
            tblblank = rqp.get('table')
            if sform.is_valid():
                if tblblank:
                    handle_uploaded_file(request.FILES['table'])
                sform.save()
                k = 0
                poststars(request, k)
                submitmsg = "Thank you for your submission of the Alert Notice \
                            entitled %s.<br> Your submission is now being reviewed. \
                            If you have any further questions,<br> \
                            please email eowaagen@aavso.org." %title
                messages.success(request, mark_safe(submitmsg))

        if "edit" in request.POST:
            # get the include graphic in original posting, first get record
            pid = request.session['editrec']
            idd = int(pid[0])
            print("edit", idd)
            # make query dictionary from this record using the session stored id key
            tb = submittal.objects.get(id=idd)
            print("tb", tb.table)
            # get fields needed for success message
            rqp = request.POST
            sid = rqp.get('ld')
            title = rqp.get('title')
            # get new graphic if the user chose another
            tblblank = rqp.get('table')
            print("sform table", tblblank)
            # make an edit form of the edited record
            sform = EditForm(request.POST, request.FILES)
            if sform.is_valid():
                print("sform is valid")
                # if the user chose another, try will work and the form is saved and new include uploaded
                try:
                    handle_uploaded_file(request.FILES['table'])
                    sform.save()
                    poststars(request, 0)
                    submittal.objects.filter(id=pid).delete()
                    submitmsg = "Thank you for your edited submission of the Alert Notice \
                                           entitled %s.<br> Your edited submission is now being reviewed. \
                                           If you have any further questions,<br> \
                                           please email eowaagen@aavso.org." % title
                    messages.success(request, mark_safe(submitmsg))
                # but if the user didn't chose another, and if original had an include
                except:
                    sform.save()
                    poststars(request, 0)
                    print("point A")
                    # since the form is saved without any include the last id is the record
                    lastid = submittal.objects.order_by('pk').last().id
                    print("lastid", lastid)
                    # make a recordset of the record just saved and update it with previous include
                    r = submittal.objects.get(id=lastid)
                    setattr(r, 'table', tb.table)
                    print('last table', tb.table)
                    r.save()
                    # but don't delete the original, let staff do it after checking
                    """
                    submittal.objects.filter(id=pid).delete()
                    """
                    # submit success record
                    submitmsg = "Thank you for your edited submission of the Alert Notice \
                                       entitled %s.<br> Your edited submission is now being reviewed. \
                                       If you have any further questions,<br> \
                                       please email eowaagen@aavso.org." % title
                    messages.success(request, mark_safe(submitmsg))


        if "email" in request.POST:
            rqp = request.POST
            emsg = rqp.get('feedback');
            print("in feedback, emsg",emsg)
            fcontact = rqp.get('contact');
            print("in feedback, fcontact", fcontact)
            ftitle = rqp.get('title');
            subj = "Problems with " + ftitle
            print("in feedback, subject",subj)
            fstaff = "higgins41@icloud.com"  #"phstpete@gmail.com"   #"eowaagen.aacso.org"
            send_mail(subj, emsg, fstaff,[fcontact],fail_silently=False)


        if "ucreate" in request.POST:
            print("usermenu/ucreate")
            try:
                print('in try')
                nextid = submittal.objects.order_by('pk').last().id + 1
                request.session['recnum'] = str(nextid)
            except:
                nextid = 1
                request.session['recnum'] = "1"
            usr = 0
            print("first init")
            #form = SubmitForm()
            form = testform()
            return render(request, "umessage.html", {'form': form})

        if "pdf" in request.POST:
            print("in pdf")
            pks = request.POST.getlist("selection")
            print('pks', pks)
            sid = int(pks[0])
            print("sid", sid)
            dt = submittal.objects.get(id=sid)
            """
            if dt.status != 'accepted':
                submitmsg = "This message is not accepted"
                messages.success(request, submitmsg)
            else:
                name = release(request,sid)
                print("save alert html file",name)

                #return HttpResponse("Alert html created successfuly")

                return FileResponse(open( name, 'rb'))
            """
            name = release(request,sid)
            print("save alert html file",name)
            return FileResponse(open( name, 'rb'))

        if "udelete" in request.POST:
            print("alertmenu/delete")
            pks = request.POST.getlist("selection")
            print('pks', pks)
            sid = int(pks[0])
            print("sid", sid)
            auth = permit(request, sid)
            print("delete auth", auth)
            print("sid and session id",sid,request.session['0'])
            if auth == 1 and sid == request.session['0']:
                submittal.objects.get(pk=sid).delete()
                submitmsg = "You have sucessfully deleted your last submittal"
                messages.success(request, submitmsg)
            else:
                text = '<span style="color: red">you can only delete your latest notice</span>'
                return HttpResponse(text)
                #submitmsg = text
                #messages.success(request, submitmsg)

        if "uview" in request.POST:
            print("in view, user")
            try:
                pks = request.POST.getlist("selection")
                print('pks', pks)
                sid = int(pks[0])
                print("sid", sid)
                auth = permit(request, sid)
                lastsubmit = submittal.objects.order_by('pk').last().id
                skey=request.session['recnum']
                print('skey',skey)
                skey = int(request.session['recnum'])
                print("sid and session id", sid, skey)
                if auth == 1 and sid == lastsubmit:
                    dt = submittal.objects.get(id=sid)
                    print("dt.title", dt.title, dt.lname, dt.urgency, dt.table)
                    form = makeeditform(dt)
                    return render(request, "umessage.html", {'form': form})
                else:
                    submitmsg = "you can only edit your last submittal"
                    messages.success(request, submitmsg)
            except:
                submitmsg = "no record selected."
                messages.success(request, submitmsg)


    print("in home init")
    try:
        table = alertrecs(submittal.objects.all())
    except:
        print("empty records")
        table = alertrecs("")
        print("in home table")
        RequestConfig(request).configure(table)

    if request.user.is_staff:
        table = alertrecs(submittal.objects.all())
        print("in home table")
        RequestConfig(request).configure(table)
        return render(request, 'recordstaff.html', {'table': table})
    else:
        umail = request.user.email
        table = alertrecs(submittal.objects.filter(contact=umail))
        return render(request, 'recordsuser.html', {'table': table})


def decdeg2dms(dd):
    negative = False
    if dd < 0:
        negative=True
    dd = abs(dd)
    minutes,seconds = divmod(dd*3600,60)
    degrees,minutes = divmod(minutes,60)
    if negative:
        if degrees > 0:
            degrees = -degrees
        elif minutes > 0:
            minutes = -minutes
        else:
            seconds = -seconds
    return (degrees,minutes,seconds)

def permit(request,r):
    print("in permit")
    if request.user.is_staff:
        print("permitted, is staff")
        return 1
    rqp = request.POST
    uname= request.user.username
    rt = submittal.objects.get(id=r)
    fname = rt.lname  #rqp.get('lname')
    print("user name  in form is...", fname)
    fmail = rt.contact #rqp.get('contact')
    print("user mail in form is...", fmail)
    umail = request.user.email
    print("user mail in login is...", umail)
    authmail = fmail in umail

    authuser = fmail in umail
    print("authuser",authuser)
    if authuser:
        return 1
    return 0

# ----------------- SYSTEM----------------------
def logout_page(request):
    print("in logout")
    logout(request)
    return HttpResponse('logged out')

def getvsx(request,s1):
    import os
    import urllib.request, urllib.parse, urllib.error
    import xml.etree.ElementTree as ET
    try:
        slist = []
        sta1 = s1
        #print("vsx 1")
        sta1 = sta1.strip()
        star = sta1.replace(' ', '+')
        starb = bytes(star, 'utf-8')
        #print("vsx 2",star)
        #contents = urllib.request.urlopen("http://www.aavso.org/vsx/index.php?view=query.votable&ident=" + starb).read()
        url = ('https://www.aavso.org/vsx/index.php?view=api.object&ident=' + star)
        uh = urllib.request.urlopen(url)
        #print("uh",uh)
        try:
            data = uh.read()
            #print(data)
            tree = ET.fromstring(data)
            t1 = (tree.find('Name').text)
            t3 = (tree.find('MaxMag').text)
            t4 = (tree.find('MinMag').text)
            t5 = (tree.find('RA2000').text)
            t6 = (tree.find('Declination2000').text)
            return (t1,t3,t4,t5,t6)
        except:
            notstar = '%s*' %s1
            #print('vsx 3')
            return (notstar,'','','','')
    except:
        #notstar = '%s*' % s1
        #print('vsx 3')
        return ('','','','','')


def poststars(request,k):

    rqp = request.POST
    if k == 0:
        r = submittal.objects.last()
    else:
        r = submittal.objects.get(id=k)
    for f in range(1, 25):
        fld = "s%d" %f
        s = rqp.get(fld);
        print("f s is",f,s)
        if len(s) < 2:
            continue
        else:
            star = s[0:10];
        #print("star to find in VSX", star)
        (t1, t3, t4, t5, t6) = getvsx(request,star)
        #print("returned t",t1,t3,t4,t5,t6)
        if len(t5) > 0:
            t5d, t5m, t5s = decdeg2dms(float(t5)/15)
            f5d = '{:.0f}'.format(t5d, 3)
            if abs(t5d < 10):
                print('formating 0 fill f5d', f5d)
                f5d = f5d.zfill(2)
            f5m = '{:.0f}'.format(t5m, 0)
            if abs(t5m < 10):
                 print("in minute", f5m)
                 f5m = f5m.zfill(2)
                 print("in minute after fill", f5m)
            f5s = '{:.2f}'.format(t5s, 2)
            if abs(t5s < 10):
                f5s = f5s.zfill(2)
            if '-' in t5:
                t5 = f5d + 'h ' + f5m + 'm ' + f5s + 's '
            else:
                t5 = f5d + 'h ' + f5m + 'm ' + f5s + 's '

            t6d, t6m, t6s = decdeg2dms(float(t6))
            print("returned t6d",t6d)
            f6d = '{:.0f}'.format(t6d, 4)
            print("f6d.....",f6d)
            print("formatted t6d", f6d)


            if abs(t6d < 10):
                f6d = f6d.zfill(3)
                print("f6d",f6d)
            f6m = '{:.0f}'.format(t6m, 0)
            if abs(t6m < 10):
                f6m = f6m.zfill(2)
            f6s = '{:.1f}'.format(t6s, 2)
            if abs(t6s < 10):
                f6s = f6s.zfill(5)
            if '-' in t6:
                t6 = f6d + 'd ' + f6m + 'm ' + f6s + 's '
            else:
                t6 = '+' + f6d + 'd ' + f6m + 'm ' + f6s + 's '
        print("here f",f)
        upfield = "s%d" % (f)
        print("here update", upfield)
        if len(str(t1)) > 3:
            u = str(t1) + "    " + str(t3) + "    " + str(t4) + "    " + str(t5) + "    " + str(t6)
        else:
            u = ""

        print("u",u)
        setattr(r, upfield, u)
        r.save()
        print("here r saved", r)

def release(request,rid):
    from datetime import date
    import PIL

    sb = submittal.objects.get(id=rid)

    today = date.today()

    fname = 'AN' + str(sb.annum) + '.html'
    f = open(fname, "w")
    f.write("<html>")
    f.write("<head>")
    f.write("<style>")
    f.write("table,th,td{border: none;}")
    f.write("</style>")
    f.write("</head>")
    f.write("<body>")

    full_name = "Attn AAVSO observers"
    f.write("<img src='static/aavso_logo.png' />")
    f.write("         ")
    if sb.annum:
        ptitle = "<p>" + "<strong>" + sb.title + ": number " + sb.annum + "</strong> " + "</p>"
    else:
        ptitle = "<p>" + "<strong>" + sb.title + ": number not assigned" "</strong> " + "</p>"

    f.write(ptitle)
    f.write("       ")

    ptext = "<p>" + '%s' % today + "</p>"
    f.write(ptext)

    if sb.forums:
        f.write("RELEVANT FORUMS<br>")
        ftxt = "AAVSO Forum threads(scroll to the bottom of a thread for latests posts);<br>"
        f.write(ftxt)
        f.write("       ")
        l = sb.forums
        flist = l.split("#")
        try:
            f.write(flist[1]+" ")
            ftxt1 = "<a href=" + flist[2] + ">forum 1</a><br>"
            f.write(ftxt1)
        except:
           ''

        try:
            f.write(flist[3]+" ")
            ftxt2 = "<a href=" + flist[4] + ">forum 2</a><br>"
            f.write(ftxt2)
        except:
            ''

        try:
            f.write(flist[5] + " ")
            ftxt2 = "<a href=" + flist[6] + ">forum 3</a><br>"
            f.write(ftxt2)
        except:
            ''



    f.write("       ")
    ptext = "<p>"+'%s' % full_name + "</p>"
    f.write(ptext)

    f.write("       ")
    ptext ="<p>" + 'Colleagues:' + "</p>"
    f.write(ptext)
    f.write("       ")

    ptext0 = "<p>" +'An alert message entitled %s has been submitted by %s %s with %s on %s and was approved on %s. \
            This request is asking for community observation support beginning %s through %s.'\
            % (sb.title, sb.fname, sb.lname, sb.affiliation, sb.submitted, sb.approved, sb.startdate, sb.enddate) + "</p>"

    f.write(ptext0)
    f.write("       ")

    ptext1 = "<p>" + 'The justification given in this request is: %s.' \
            % (sb.justification) + "</p>"

    f.write(ptext1)
    f.write("       ")

    ptext2 = "<p>" + 'The submitters instructions are: %s' \
             % (sb.instructions) + "</p>"

    f.write(ptext2)
    f.write("       ")

    ptext22 = "<p>" + 'The submitters notes to observers follow: %s'\
            % (sb.notes) + "</p>"

    f.write(ptext22)
    f.write("       ")

    if sb.table:
        #if len(sb.table) > 4:
        ptext3 = "<p>" + 'The submitters have included the following table:' + "</p>"
        f.write(ptext3)
        f.write("       ")
        #image = PIL.Image.open('static/%s' % sb.table)
        image = PIL.Image.open('myalert/static/%s' % sb.table)
        width, height = image.size
        print("w,h", width / 2, height / 2)
        w = 294  # int(width/2)
        h = 348  # int(height)/2
        newimage = image.resize((w, h))
        s = newimage.save('static/s.jpg')
        f.write("<img src= 'static/s.jpg' />")

    c = ''
    ptext3 = "<p>" + 'Cadences selected are:'
    if sb.TS == True: c = c + 'time-series' + ' '
    if sb.HR == True: c = c + ' ' + 'hourly' + ' '
    if sb.NI == True: c = c + ' ' + 'nightly' + ' '
    if sb.WK == True: c = c + ' ' + 'weekly' + ' '
    if sb.MO == True: c = c + ' ' + 'weekly' + ' '
    c = c + "</p>"
    ptext7 = ptext3 + c
    f.write(ptext7)
    f.write("       ")
    c = ''

    ptext8 = "<p>" + 'Variability types indicated are:'
    if sb.CT == True: c = c + ' ' + 'cataclymic variables'+ ' '
    if sb.EB == True: c = c + ' ' + 'eclipsing binary' + ' '
    if sb.XP == True: c = c + ' ' + 'exoplanet'+ ' '
    if sb.HE == True: c = c + ' ' + 'high energy' + ' '
    if sb.LV == True: c = c + ' ' + 'long period variable' + ' '
    if sb.SP == True: c = c + ' ' + 'short period puksators + ' ''
    if sb.SO == True: c = c + ' ' + 'young steller objects' + ' '
    ptext8 = ptext8 + c + "</p>"
    f.write(ptext8)
    f.write("       ")

    c = ''
    Pstr = "<p>" + 'Modes of Observing selected are:'
    if sb.Vp == True: c = c + ' ' +'Visual' + ' '
    if sb.Cp == True: c = c + ' ' + 'CCD-CMOS' + ' '
    if sb.Dp == True: c = c + ' ' + 'DSLR' + ' '
    if sb.Pp == True: c = c + ' ' + 'PEP' + ' '
    ptext7 = Pstr + c + "</p>"
    f.write(ptext7)
    f.write("       ")

    fstr = "<p>" + 'Photometry filters that may be used include:'
    for s in range(1, 11):
        if s == 1 and sb.U:  fstr = fstr + "  U" + ' '
        if s == 2 and sb.B:  fstr = fstr + " B " + ' '
        if s == 3 and sb.V:  fstr = fstr + " V " + ' '
        if s == 4 and sb.R:  fstr = fstr + " R " + ' '
        if s == 5 and sb.I:  fstr = fstr + " I " + ' '
        if s == 6 and sb.uu:  fstr = fstr + " u " + ' '
        if s == 7 and sb.g:  fstr = fstr + " g " + ' '
        if s == 8 and sb.rr:  fstr = fstr + " r " + ' '
        if s == 9 and sb.l:  fstr = fstr + " l " + ' '
        if s == 10 and sb.z:  fstr = fstr + " z " + ' '
        fstr + "</p>"
    f.write(fstr)
    f.write("       ")
    f.write("<p>")
    f.write("</p>")
    ptext11 = 'Target stars are (* indicates not found in VSX):'
    f.write(ptext11    )
    f.write("<p>")
    s0 = ["Star",  "Con", "MinV", "MaxV", "RA 2000 h:m:s","Dec 2000 d:m:s"]
    s1 = ['', '', '', '', '', '', '', '']
    s2 = ['', '', '', '', '', '', '', '']
    s3 = ['', '', '', '', '', '', '', '']
    s4 = ['', '', '', '', '', '', '', '']
    s5 = ['', '', '', '', '', '', '', '']
    s6 = ['', '', '', '', '', '', '', '']
    s7 = ['', '', '', '', '', '', '', '']
    s8 = ['', '', '', '', '', '', '', '']
    s9 = ['', '', '', '', '', '', '', '']
    s10 = ['', '', '', '', '', '', '', '']
    print("sb.s1....",sb.s1,sb.s2,sb.s3)
    if sb.s1:
        print("sb.s1",sb.s1)
        s1 = sb.s1.split()
        print("s1",s1)
        if '*' in sb.s1:
            s1 = [s1[0]+'*', '', '', '', '', '']
        else:
            tm6=str(s1[6]);
            t6 = tm6.replace("h"," ")
            tm7=s1[7];
            t7 = tm7.replace("m", " ")
            tm8=s1[8];
            t8 = tm8.replace("s"," ")
            tm9 = s1[9];
            t9 = tm9.replace("d", " ")
            if len(t9)==3:
                t9 = t9.replace("-","-0")
            tm10 = s1[10];
            t10 = tm10.replace("m"," ")
            tm11 = s1[11]
            t11 = tm11.replace("s"," ")
            s1 = [s1[0],s1[1],s1[2],s1[4], t6 + t7 + t8, t9 + t10+ t11]

    if sb.s2:
        print("sb.s2", sb.s2)
        s2 = sb.s2.split()
        if '*' in sb.s2:
            s2 = [s2[0] , '*', '', '', '', '', '', '']
        else:
            tm6 = str(s2[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s2[7];
            t7 = tm7.replace("m", " ")
            tm8 = s2[8];
            t8 = tm8.replace("s", " ")
            tm9 = s2[9];
            t9 = tm9.replace("d", " ")
            if len(t9)==3:
                t9 = t9.replace("-","-0")
            tm10 = s2[10];
            t10 = tm10.replace("m", " ")
            tm11 = s2[11]
            t11 = tm11.replace("s", " ")
            s2 = [s2[0], s2[1], s2[2], s2[4], t6 + t7 + t8, t9 + t10 + t11]

    if sb.s3:
        s3 = sb.s3.split()
        if '*' in sb.s3:
            s3 = [s3[0] ,'*', '', '', '', '', '', '']
        else:
            tm6 = str(s3[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s3[7];
            t7 = tm7.replace("m", " ")
            tm8 = s3[8];
            t8 = tm8.replace("s", " ")
            tm9 = s3[9];
            t9 = tm9.replace("d", " ")
            if len(t9)==3:
                t9 = t9.replace("-","-0")
            if len(t9)==3:
                t9 = t9.replace("-","-0")
            tm10 = s3[10];
            t10 = tm10.replace("m", " ")
            tm11 = s3[11]
            t11 = tm11.replace("s", " ")
            s3 = [s3[0], s3[1], s3[2], s3[4], t6 + t7 + t8, t9 + t10 + t11]

    if sb.s4:
        s4 = sb.s4.split()
        print("sb.s4",s4)
        if '*' in sb.s4:
            s4 = [s4[0] ,'*', '', '', '', '', '', '']
        else:
            tm6 = str(s4[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s4[7];
            t7 = tm7.replace("m", " ")
            tm8 = s4[8];
            t8 = tm8.replace("s", " ")
            tm9 = s4[9];
            t9 = tm9.replace("d", " ")
            tm10 = s4[10];
            t10 = tm10.replace("m", " ")
            tm11 = s4[11]
            t11 = tm11.replace("s", " ")
            s4 = [s4[0], s4[1], s4[2], s4[4],  t6 + t7 + t8, t9 + t10 + t11]

    if sb.s5:
        s5 = sb.s5.split()
        if '*' in sb.s5:
            s5 = [s5[0] ,'*', '', '', '', '', '', '']
        else:
            tm6 = str(s5[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s5[7];
            t7 = tm7.replace("m", " ")
            tm8 = s5[8];
            t8 = tm8.replace("s", " ")
            tm9 = s5[9];
            t9 = tm9.replace("d", " ")
            tm10 = s5[10];
            t10 = tm10.replace("m", " ")
            tm11 = s5[11]
            t11 = tm11.replace("s", " ")
            s5 = [s5[0], s5[1], s5[2], s5[4], t6 + t7 + t8, t9 + t10 + t11]
            print("s5",s5)

    if sb.s6:
        s6 = sb.s6.split()
        if '*' in sb.s6:
            s6 = [s6[0] ,'*', '', '', '', '', '', '']
        else:
            tm6 = str(s6[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s6[7];
            t7 = tm7.replace("m", " ")
            tm8 = s6[8];
            t8 = tm8.replace("s", " ")
            tm9 = s6[9];
            t9 = tm9.replace("d", " ")
            tm10 = s6[10];
            t10 = tm10.replace("m", " ")
            tm11 = s6[11]
            t11 = tm11.replace("s", " ")
            s6 = [s6[0], s6[1], s6[2], s6[4], t6 + t7 + t8, t9 + t10 + t11]

    if sb.s7:
        s7 = sb.s7.split()
        if '*' in sb.s7:
            s7 = [s7[0] ,'*', '', '', '', '', '', '']
        else:
            tm6 = str(s7[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s7[7];
            t7 = tm7.replace("m", " ")
            tm8 = s7[8];
            t8 = tm8.replace("s", " ")
            tm9 = s7[9];
            t9 = tm9.replace("d", " ")
            tm10 = s7[10];
            t10 = tm10.replace("m", " ")
            tm11 = s7[11]
            t11 = tm11.replace("s", " ")
            s7 = [s7[0], s7[1], s7[2], s7[4], t6 + t7 + t8, t9 + t10 + t11]

    if sb.s8:
        s8 = sb.s8.split()
        if '*' in sb.s8:
            s8 = [s8[0] ,'*', '', '', '', '', '', '']
        else:
            tm6 = str(s8[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s8[7];
            t7 = tm7.replace("m", " ")
            tm8 = s8[8];
            t8 = tm8.replace("s", " ")
            tm9 = s8[9];
            t9 = tm9.replace("d", " ")
            if len(t9)==3:
                t9 = t9.replace("-","-0")
            tm10 = s8[10];
            t10 = tm10.replace("m", " ")
            tm11 = s8[11]
            t11 = tm11.replace("s", " ")
            s8 = [s8[0], s8[1], s8[2], s8[4], t6 + t7 + t8, t9 + t10 + t11]

    if sb.s9:
        s9 = sb.s9.split()
        if '*' in sb.s9:
            s9 = [s9[0] ,'*', '', '', '', '', '', '']
        else:

            tm6 = str(s9[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s9[7];
            t7 = tm7.replace("m", " ")
            tm8 = s9[8];
            t8 = tm8.replace("s", " ")
            tm9 = s9[9];
            t9 = tm9.replace("d", " ")
            if len(t9)==3:
                t9 = t9.replace("-","-0")
            tm10 = s9[10];
            t10 = tm10.replace("m", " ")
            tm11 = s9[11]
            t11 = tm11.replace("s", " ")
            s9 = [s9[0], s9[1], s9[2], s9[4],  t6 + t7 + t8, t9 + t10 + t11]

    if sb.s10:
        s10 = sb.s10.split()
        if '*' in sb.s10:
            s10 = [s10[0] ,'*', '', '', '', '', '', '']
        else:
            tm6 = str(s10[6]);
            t6 = tm6.replace("h", " ")
            tm7 = s10[7];
            t7 = tm7.replace("m", " ")
            tm8 = s10[8];
            t8 = tm8.replace("s", " ")
            tm9 = s10[9];
            t9 = tm9.replace("d", " ")
            if len(t9)==3:
                t9 = t9.replace("-","-0")
            tm10 = s10[10];
            t10 = tm10.replace("m", " ")
            tm11 = s10[11]
            t11 = tm11.replace("s", " ")
            s10 = [s10[0], s10[1], s10[2], s10[4], t6 + t7 + t8, t9 + t10 + t11]

    f.write("<table width=40%;border:none;>\n")
    for r in range (0,10):
        if r==0:
            f.write("<tr bgcolor='lightblue';>\n")
        else:
            f.write("<tr>\n")

        ff = [s0,s1,s2,s3,s4,s5,s6,s7,s8,s9,s10]
        for q in range (0,6):
            try:
                f.write("<td>")
                #f.write(ff[r][q])
                v = ff[r][q]
                print("v",r,v)
                f.write(v)
                f.write("</td>")
            except:
                break
        f.write("</tr>\n")
    f.write("</table>\n")


    f.write("<p>")
    ptext = 'Thank you very much for your support.'
    f.write(ptext)
    f.write(  "\n" )
    f.write("<p>")
    ptext = 'Sincerely,'
    f.write(ptext)
    f.write(  "\n" )
    f.write("<p>")
    ptext = 'AAVSO staff'
    f.write(ptext)
    f.write(  "\n" )
    f.write("</html>")

    f.write("</body>")
    f.close()
    return fname 
