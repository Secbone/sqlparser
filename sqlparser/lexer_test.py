from .lexer import parse


sql = '''
    SELECT 
    col1, 
    col2, 
    count(10) 
    from tab1 
    where id > 10 
    and col2 in (
        select * from (
            select col2 from tab2 left join schema1.tab3
        ) as t2
        where t2 > 11
        order by col4 + 2
    )
    order by col2-1
'''

for t in parse(sql):
    print(t)



def test_lexer():
    pass