from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import OrderedDict

PRI_URLS = OrderedDict({
        # 2 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C003718&zach=All&semestr=YEAR&group=%D0%9F%D0%A0%D0%98%D0%B1-191',
        # 3 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002847&zach=All&semestr=YEAR&group=%D0%9F%D0%A0%D0%98%D0%B1-181',
        4 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002003&zach=All&semestr=YEAR&group=%D0%9F%D0%A0%D0%98-171'
})

IVT_URLS = OrderedDict({
       # 2 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C003715&zach=All&semestr=YEAR&group=%D0%98%D0%92%D0%A2%D0%B1-191',
       # 3 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002844&zach=All&semestr=YEAR&group=%D0%98%D0%92%D0%A2%D0%B1-181',
       4 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C001999&zach=All&semestr=YEAR&group=%D0%98%D0%92%D0%A2-171'
})

IST_URLS = OrderedDict({
       # 2 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C003716&zach=All&semestr=YEAR&group=%D0%98%D0%A1%D0%A2%D0%B1-191',
       # 3 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002845&zach=All&semestr=YEAR&group=%D0%98%D0%A1%D0%A2%D0%B1-181',
       4 : 'https://volsu.ru/rating/?plan_id=%D0%90%D0%A0%D0%9C002002&zach=All&semestr=YEAR&group=%D0%98%D0%A1%D0%A2-171'
})


def parse_page(url):
       request = requests.get(url)
       soup = BeautifulSoup(request.text, features='html.parser')
       rows = soup.find_all('tr')

       table = []
       headers = []
       for header in rows[0]:
              if header == '\n':
                     pass;
              elif header.find('div'):
                     header_divs = header.find_all('div')
                     # header_divs = header_divs[0].text
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
              group_df = pd.DataFrame(group_table[1::], columns=group_table[0])
              group_dataframes.append(group_df)

       return group_dataframes


# piece of shit
def drop_no_data_rows(dataframe):
       for column in dataframe.columns:
              indexes = dataframe.index[dataframe[column] == 'Нет данных']
              if len(indexes) != 0:
                     indexes = indexes[::-1]
                     for index in indexes:
                            dataframe = dataframe.drop(index, axis=0)

       return dataframe


def cast_data_to_int(dataframe):
       return dataframe[dataframe.columns[1::]].astype('int32')


def process_dataframe_to_plot(dataframe):
       dataframe = drop_no_data_rows(dataframe)
       dataframe = cast_data_to_int(dataframe)
       dataframe = drop_zero_score_sum(dataframe)

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
              semesters = key * 2
              for i in range(1, semesters):
                     url = value.replace('YEAR', str(i))
                     urls.append(url)

              group_urls[key] = urls

gen_urls(PRI_URLS)
pri_171_urls = [pair[1] for pair in list(PRI_URLS.items())][2]
pri_171_dataframes = make_dataframes(pri_171_urls)

gen_urls(IVT_URLS)
ivt_171_urls = [pair[1] for pair in list(IVT_URLS.items())][2]
ivt_171_dataframes = make_dataframes(ivt_171_urls)

gen_urls(IST_URLS)
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