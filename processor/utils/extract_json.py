import json
from json_repair import repair_json

def extract_json_simple(text):
    start_index = text.find('{')
    end_index = text.rfind('}')

    if start_index == -1 or end_index == -1:
        return None  # No JSON found
    json_str = repair_json(text[start_index:end_index + 1])
    
    return json.dumps(json.loads(json_str), ensure_ascii=False, indent=2)




if __name__ == "__main__":
    print("hello")
    pseudo_json = '''
  {
  "id": 395,
  "title": "Банки",
  "years": {
    "1876": "Рік, коли в Мадейрі вже існувало відділення Банку Португалії.",
    "1878": "Рік банкрутства Жуана Жозе Родрігеса Лейтана та рік, коли Томаш Антоніу Гомеш вступив на посаду агента Банку Португалії на Мадейрі.",
    "1887": "Рік розпуску Комерційного банку Мадейри.",
    "1888": "Рік, з якого агентство Банку Португалії на Мадейрі є скарбницею державної казни для операцій з державою.",
    "1904": "Початок періоду, коли було призначено кількох агентів Банку Португалії на Мадейрі.",
    "1919": "Рік відкриття філії Національного Заморського банку на Мадейрі.",
    "1875": "Рік відкриття Комерційного банку Мадейри у Фуншалі.",
    "1877": "Рік, коли Комерційний банк Мадейри мав прибуток у розмірі 39 942 732 реалів.",
    "1879": "Рік, коли Комерційний банк Мадейри мав прибуток у розмірі 32 851 757 реалів, згаданий як не дуже процвітаючий через відтік капіталу.",  
    "1884": "Рік, коли Комерційний банк Мадейри не розподілив дивіденди.",
    "1885": "Рік, коли Комерційний банк Мадейри не розподілив дивіденди, було випущено 6 000 акцій.",
    "1886": "Рік, коли Комерційний банк Мадейри не розподілив дивіденди, і рік, коли граф Канавіал порадив створити промисловий банк на Мадейрі.",
    "1800": "Рік, коли уряд метрополії рекомендував створити кредитну спілку на Мадейрі.",
    "1824": "Рік, коли губернатор і генерал-капітан Дон Мануель де Португал е Каштру надіслав центральному уряду клопотання про створення банку у Фуншалі.",
    "1920": "23 червня 1920 року відкрився Банк Мадейри.",
    "1921": "Датою 7 січня 1921 року є декрет, який дозволив остаточне створення того ж Банку Мадейри.",
    "1922": "Усі ці установи, що здійснюють банківські операції, необхідні для комерції Фуншала, а також інші, перебувають у досить процвітаючому стані завдяки їхньому чудовому управлінню та довірі, якою вони користуються на ринку."
  },
  "people": {
    "Жуан Жозе Родрігес Лейтан": "Торговець, який очолював агентство Банку Португалії на Мадейрі у 1876 році та збанкрутував у 1878 році.",
    "Томаш Антоніу Гомеш": "Вступив на посаду агента Банку Португалії на Мадейрі 15 липня 1878 року.",  
    "Енріке де Барруш Гомеш": "Директор Банку Португалії, який перебував на Мадейрі через банкрутство Жуана Жозе Родрігеса Лейтана.",
    "Раймунду Сієве де Менезеш": "Колишній скарбник, який служив тимчасовим агентом Банку Португалії на Мадейрі.",
    "Луїш де Фрейташ Бранку": "Один з агентів Банку Португалії на Мадейрі з 1904 року.",
    "Енріке Авгушту Вієйра де Каштру": "Агент Банку Португалії на Мадейрі з 1904 року.",
    "Едуарду Мартінш да Сілвейра": "Агент Банку Португалії на Мадейрі з 1904 року.",
    "Фернанду Ферру": "Агент Банку Португалії на Мадейрі з 1904 року.",
    "Енріке де Са Ногейра": "Агент Банку Португалії на Мадейрі з 1904 року.",
    "Франсішку Камілу Мейра": "Агент Банку Португалії на Мадейрі з 1904 року.",  
    "Раул Родрігеш Коен": "Агент Банку Португалії на Мадейрі з 1904 року.",
    "Антоніу Норонья де Барруш": "Агент Банку Португалії на Мадейрі з 1904 року.",
    "Луїш Гомеш да Консейсан": "Перший представник Національного Заморського банку на Мадейрі.",
    "Жуан де Салеш Калдейра": "Член першої дирекції Комерційного банку Мадейри.",
    "Карлуш Біанкі": "Член першої дирекції Комерційного банку Мадейри.",
    "Жозе Паулу душ Сантуш": "Член першої дирекції Комерційного банку Мадейри.",
    "Вільям Хінтон": "Член першої наглядової ради Комерційного банку Мадейри.",
    "Мануел Інісіу да Кошта Ліра": "Член першої наглядової ради Комерційного банку Мадейри.",
    "Роберту Вілкінсон": "Член першої наглядової ради Комерційного банку Мадейри.",
    "Антоніу Каетану Араган": "Член першої наглядової ради Комерційного банку Мадейри.",
    "Мануел Фігейра де Шавеш": "Член першої наглядової ради Комерційного банку Мадейри.",
    "Северіану Алберту де Фрейташ Ферраш": "Перший голова загальних зборів Комерційного банку Мадейри.",
    "Граф Канавіал": "Порадив створити промисловий банк на Мадейрі у 1886 році."
  },
  "locations": {
    "Мадейра": "Місце розташування відділень кредитних установ материка та місце історичних подій, пов'язаних з банківськими установами.",
    "Фуншал": "Місто на Мадейрі, де розташовані різні установи, що працюють як банківські установи, і де відкрився Комерційний банк Мадейри."
  },
  "body": ""  
}'''
    j = extract_json_simple(pseudo_json)
    print(j)
    # print type of j
    
    print(type(j))
    # import json
    # print(json.loads(j))