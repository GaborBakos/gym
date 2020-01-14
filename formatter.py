# ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
#
# column_formater = {f'{ordinal(x)}': lambda s: f'{s:.2f}' for x in range(10)}
#
# print(column_formater)

table_formatter = [
    dict(selector='th',
         props=[
             ('text-align', 'center'),
             ('color', 'white')
         ]),
    dict(selector='tbody',
         props=[
             ('color', 'white')
         ]),
    dict(selector='tbody tr:nth-child(even)',
         props=[
             ('background', '#000066'),
         ]),
    dict(selector='tbody tr:nth-child(odd)',
         props=[
             ('background', '#0033cc')
         ]),
    dict(selector='tbody tr:hover td',
         props=[
             ('background-color', '#101010'),
             ('color', 'white')
         ]),
    dict(selector='tbody th',
         props=[
             ('text-align', 'left'),
             ('color', 'white')
         ]),
    dict(selector='thead tr:nth-child(1)',
         props=[
             ('background-color', '#202020'),
             ('color', 'white')
         ]),
    # dict(selector='thead tr:nth-child(2)',
    #      props=[
    #          ('background-color', 'pink')
    #      ]),
    dict(selector='tbody td:nth-child(1)',
         props=[
             ('background-color', 'brown'),
             ('text-align', 'left'),
             ('color', 'white')
         ]),
    dict(selector='thead th:nth-child(1)',
         props=[
             ('background-color', 'purple')
         ])
                ]