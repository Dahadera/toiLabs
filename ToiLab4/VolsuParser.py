from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import OrderedDict

# Each ordered dict has course as key and value as url with placeholder 'YEAR',
# which can be replaced by number of semester
PRI_URLS = OrderedDict({
        2 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C003718&zach=All&semestr=YEAR&group=%D0%9F%D0%A0%D0%98%D0%B1-191',
        3 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002847&zach=All&semestr=YEAR&group=%D0%9F%D0%A0%D0%98%D0%B1-181',
        4 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002003&zach=All&semestr=YEAR&group=%D0%9F%D0%A0%D0%98-171'
})

IVT_URLS = OrderedDict({
       2 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C003715&zach=All&semestr=YEAR&group=%D0%98%D0%92%D0%A2%D0%B1-191',
       3 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002844&zach=All&semestr=YEAR&group=%D0%98%D0%92%D0%A2%D0%B1-181',
       4 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C001999&zach=All&semestr=YEAR&group=%D0%98%D0%92%D0%A2-171'
})

IST_URLS = OrderedDict({
       2 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C003716&zach=All&semestr=YEAR&group=%D0%98%D0%A1%D0%A2%D0%B1-191',
       3 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002845&zach=All&semestr=YEAR&group=%D0%98%D0%A1%D0%A2%D0%B1-181',
       4 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002002&zach=All&semestr=YEAR&group=%D0%98%D0%A1%D0%A2-171'
})


def parse_page(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, features='html.parser')
    rows = soup.find_all('tr')

    table = []
    headers = []

    # Header information stored in <td> tag. Skipping '\n'.
    # First not empty header is '№ Номер зачётки',
    # the second ones are actual student classes, which has three <div>. First <div> has name of the class,
    # second div has type of examination.
    for header in rows[0]:
        if header == '\n':
            pass
        elif header.find('div'):
            header_divs = header.find_all('div')
            semi_header = header_divs[0].text
            if len(header_divs[2].text) != 0:
                semi_header = "{0} {1}".format(semi_header, header_divs[2].text)
            headers.append(semi_header)
        else:
            headers.append(header.text)

    table.append(headers)

    for row in rows[1::]:
        cells = row.find_all('td')
        cells_data = []
        for cell in cells:
            cells_data.append(cell.text)

        table.append(cells_data)

    return table


def make_dataframes(group_urls):
    group_dataframes = []

    for url in group_urls:
        group_table = parse_page(url)
        # group_table[0] has student ids, which not useful, so we don`t include it in dataframes
        group_df = pd.DataFrame(group_table[1::], columns=group_table[0])
        group_dataframes.append(group_df)

    return group_dataframes


# Those students which don`t have data at least for one class, are getting deleted
def drop_no_data_rows(dataframe):
    for column in dataframe.columns:
        indexes = dataframe.index[dataframe[column] == 'Нет данных']
        if len(indexes) != 0:
            # Reversing list indexes of students to delete, for errors escaping
            indexes = indexes[::-1]
            for index in indexes:
                dataframe = dataframe.drop(index, axis=0)

    return dataframe


def cast_data_to_int(dataframe):
    # Casting all columns to int data type, except column with student ids
    return dataframe[dataframe.columns[1::]].astype('int32')


def process_dataframe_to_plot(dataframe):
    dataframe = drop_no_data_rows(dataframe)
    dataframe = cast_data_to_int(dataframe)
    dataframe = drop_zero_score_sum(dataframe)

    return dataframe


def add_group_name_column(dataframe, group_name):
    dataframe['Группа'] = group_name

    return dataframe


def merge_semesters(semester_dataframes):
    merged_semesters = semester_dataframes[0]
    for semester_dataframe in semester_dataframes[1::]:
        merged_semesters = pd.merge(left=merged_semesters, right=semester_dataframe,
                                    left_on='№ зачетной книжки', right_on='№ зачетной книжки')

    return merged_semesters


def drop_zero_score_sum(dataframe):
    dataframe['Сумма баллов'] = dataframe.sum(axis=1)
    dataframe = dataframe[dataframe["Сумма баллов"] != 0]

    return dataframe.drop('Сумма баллов', axis=1)


def gen_urls(group_urls):
    for key, value in group_urls.items():
        urls = []
        # Key is a course, each course has course * 2 semesters
        semesters = key * 2
        for i in range(1, semesters):
            url = value.replace('YEAR', str(i))
            urls.append(url)

        group_urls[key] = urls

gen_urls(PRI_URLS)
# pri_191_urls = [pair[1] for pair in list(PRI_URLS.items())][0]
# pri_191_dataframes = make_dataframes(pri_191_urls)
# pri_181_urls = [pair[1] for pair in list(PRI_URLS.items())][1]
# pri_181_dataframes = make_dataframes(pri_181_urls)
pri_171_urls = [pair[1] for pair in list(PRI_URLS.items())][2]
pri_171_dataframes = make_dataframes(pri_171_urls)

gen_urls(IVT_URLS)
# ivt_191_urls = [pair[1] for pair in list(IVT_URLS.items())][0]
# ivt_191_dataframes = make_dataframes(ivt_191_urls)
# ivt_181_urls = [pair[1] for pair in list(IVT_URLS.items())][1]
# ivt_181_dataframes = make_dataframes(ivt_181_urls)
ivt_171_urls = [pair[1] for pair in list(IVT_URLS.items())][2]
ivt_171_dataframes = make_dataframes(ivt_171_urls)

gen_urls(IST_URLS)
# ist_191_urls = [pair[1] for pair in list(IST_URLS.items())][0]
# ist_191_dataframes = make_dataframes(ist_191_urls)
# ist_181_urls = [pair[1] for pair in list(IST_URLS.items())][1]
# ist_181_dataframes = make_dataframes(ist_181_urls)
ist_171_urls = [pair[1] for pair in list(IST_URLS.items())][2]
ist_171_dataframes = make_dataframes(ist_171_urls)

classes_sem_1 = [
    '№ зачетной книжки',
    'Алгебра и геометрия Экзамен',
    'Математический анализ Зачет с оценкой'
]

classes_sem_4 = [
    '№ зачетной книжки',
    'Операционные системы Экзамен',
    'Базы данных Экзамен',
    'Численные методы Экзамен'
]

classes_sem_5 = [
    '№ зачетной книжки',
    'Визуальное программирование Зачет с оценкой',
    'Геоинформационные системы Экзамен',
    'Теория вероятностей и математическая статистика Зачет с оценкой',
    'Производственная практика, научно-исследовательская работа Зачет с оценкой'
]

classes_sem_6 = [
    '№ зачетной книжки',
    'Производственная практика, научно-исследовательская работа Зачет с оценкой'
]


ist_171_dataframe_sem_1 = ist_171_dataframes[0][classes_sem_1]
ist_171_dataframe_sem_4 = ist_171_dataframes[3][classes_sem_4]
ist_171_dataframe_sem_5 = ist_171_dataframes[4][classes_sem_5]
ist_171_dataframe_sem_6 = ist_171_dataframes[5][classes_sem_6]

ivt_171_dataframe_sem_1 = ivt_171_dataframes[0][classes_sem_1]
ivt_171_dataframe_sem_4 = ivt_171_dataframes[3][classes_sem_4]
ivt_171_dataframe_sem_5 = ivt_171_dataframes[4][classes_sem_5]
ivt_171_dataframe_sem_6 = ivt_171_dataframes[5][classes_sem_6]

pri_171_dataframe_sem_1 = pri_171_dataframes[0][classes_sem_1]
pri_171_dataframe_sem_4 = pri_171_dataframes[3][classes_sem_4]
pri_171_dataframe_sem_5 = pri_171_dataframes[4][classes_sem_5]
pri_171_dataframe_sem_6 = pri_171_dataframes[5][classes_sem_6]


ist_171_merged = merge_semesters([ist_171_dataframe_sem_1, ist_171_dataframe_sem_4,
                                  ist_171_dataframe_sem_5, ist_171_dataframe_sem_6])

ivt_171_merged = merge_semesters([ivt_171_dataframe_sem_1, ivt_171_dataframe_sem_4,
                                  ivt_171_dataframe_sem_5, ivt_171_dataframe_sem_6])

pri_171_merged = merge_semesters([pri_171_dataframe_sem_1, pri_171_dataframe_sem_4,
                                  pri_171_dataframe_sem_5, pri_171_dataframe_sem_6])


ist_171_merged = process_dataframe_to_plot(ist_171_merged)
ivt_171_merged = process_dataframe_to_plot(ivt_171_merged)
pri_171_merged = process_dataframe_to_plot(pri_171_merged)

add_group_name_column(ist_171_merged, 'ИСТ-171')
add_group_name_column(ivt_171_merged, 'ИВТ-171')
add_group_name_column(pri_171_merged, 'ПРИ-171')

groups_dataframe = pd.concat([ist_171_merged, ivt_171_merged, pri_171_merged])
groups_dataframe = groups_dataframe.reset_index(drop=True)
groups_dataframe.to_csv('data/sexy_dataframe.csv', index=False)
