import os
import requests
import xmltodict
import json
from tqdm import tqdm

from ics import Calendar, Event


def main():
    event = {'name': input('생성할 일정의 이름을 입력 해 주세요. : '),
             'begin': input('그 일정의 시작 일자를 음력으로 적어 주세요. 예)2023-07-21 15:26:18 : '),
             'end': int(input('종료가 되는 해를 입력해 주세요. 최대 2050년입니다. 예)2027 : '))}

    year, month, day = event['begin'].split('-')
    c = Calendar()

    for y in tqdm(range(int(year), event['end'] + 1)):
        url = 'http://apis.data.go.kr/B090041/openapi/service/LrsrCldInfoService/getSolCalInfo'
        params = {'serviceKey': os.environ['SERVICE_KEY'], 'lunYear': str(y), 'lunMonth': month, 'lunDay': day}

        response = requests.get(url, params=params)
        e = Event()

        cc = xmltodict.parse(response.content)  # return collections.OrderedDict
        data = json.loads(json.dumps(cc))

        day_info = data['response']['body']['items']['item']

        # 윤달일 경우 첫번째 값을 달력에 추가
        if isinstance(day_info, list):
            day_info = day_info[0]

        e.name, e.begin = event['name'], '{0}-{1}-{2}'.format(day_info['solYear'],
                                                              day_info['solMonth'],
                                                              day_info['solDay'])
        e.make_all_day()

        c.events.add(e)

    file_name = input('거의 완료되었습니다. 파일 이름을 적어 주세요. : ')

    with open('{0}.ics'.format(file_name), 'w') as my_file:
        my_file.writelines(c.serialize_iter())

    return


if __name__ == '__main__':
    main()
