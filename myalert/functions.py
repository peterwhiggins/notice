def handle_uploaded_file(f):
    with open('myalert/staticfiles/'+f, 'wb+') as destination:
        f.encode()
        destination.write(f)


