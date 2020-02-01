# ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
#
# column_formater = {f'{ordinal(x)}': lambda s: f'{s:.2f}' for x in range(10)}
#
# print(column_formater)


def format_df(df, column_style=None, table_style=None):
    if column_style is None:
        column_style = dict()
    if table_style is None:
        table_style = []
    return df.style.format(column_style).set_table_styles(table_style)


def hover(hover_color="#ffff99"):
    return dict(selector="tr:hover",
                props=[("background-color", f"{hover_color}")])


flatten = lambda l: [item for sublist in l for item in sublist]
ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n/10%10!=1)*(n%10<4)*n%10::4])
column_formater = {f'{ordinal(x)} Weight': lambda s: f'{s:.2f}' for x in range(10)}.update(
                  {f'{ordinal(x)} Reps': lambda s: f'{s:.2f}' for x in range(10)}
                    )

table_formatter = [
    dict(selector='th',
         props=[
             ('text-align', 'center'),
             ('color', 'black'),
             ('font-family', 'serif')
         ]),
    dict(selector='tbody',
         props=[
             ('color', 'black')
         ]),
    dict(selector='tbody tr:nth-child(even)',
         props=[
             ('background', 'gray'),
         ]),
    dict(selector='tbody tr:nth-child(odd)',
         props=[
             ('background', 'lightgrey')
         ]),
    dict(selector='tbody tr:hover td',
         props=[
             ('background-color', '#101010'),
             ('color', 'white')
         ]),
    dict(selector='tbody th',
         props=[
             ('text-align', 'left'),
             ('color', 'black')
         ]),
    dict(selector='thead tr:nth-child(1)',
         props=[
             ('background-color', 'gray'),
             ('color', 'black')
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
             ('background-color', 'white')
         ])
                ]