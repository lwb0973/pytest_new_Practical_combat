import xlrd

# 处理表格数据转换成@pytest.mark.parametrize可以读取的数据类型[{name:user1,pwd:123},{name:user2,pwd:123}]
def dict_data(excel_case_path, sheet_name):
    data = xlrd.open_workbook(excel_case_path)
    table = data.sheet_by_name(sheet_name)
    headers = table.row_values(0)
    rownum = table.nrows
    colnum = table.ncols
    datas = []
    j = 1
    # 这里的循环实际上只是遍历有效长度，没有参与读取数据
    for i in range(rownum - 1):
        s = {}
        # 真正读取数据是在这个部分，j才是真正读取行中的数据
        values = table.row_values(j)
        j = j + 1
        for x in range(colnum):
            s[headers[x]] = values[x]
        datas.append(s)
    return datas