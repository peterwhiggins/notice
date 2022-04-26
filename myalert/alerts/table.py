import django_tables2 as tables

class alertrecs(tables.Table):
    selection = tables.CheckBoxColumn(accessor='pk')
    title = tables.Column(verbose_name='Notice Title')
    annum = tables.Column(verbose_name='ANnum')
    submitted = tables.Column()
    lname = tables.Column()
    startdate = tables.Column()
    enddate = tables.Column()
    status = tables.Column()


    class Meta:
        attrs = {'*': {'style': "width:400px; background-color:lightblue"}}
        attrs = {'selection': {'style': "width:10px; background-color:lightblue"}}
