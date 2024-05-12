import telebot
from bs4 import BeautifulSoup
from selenium import webdriver


bot = telebot.TeleBot("6878898648:AAEYkYpnjweNCV4KHJwfDwb2F9V11QI_Xds")


def get_currency() -> str:
    iFin_shop_url = "https://ifin.kz/exchange/astana"
    driver = webdriver.Chrome()
    driver.get(url=iFin_shop_url)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.find_all("div", class_="tbl-row row-toggle company-row")
    list_of_buy_sell = []
    dict_buy_dollar = {}
    dict_sell_dollar = {}
    for row in rows:
        raw_name = row.find("a", class_="table-row-title")
        formatted_name = raw_name.text.replace(" ", "").replace("\n", "")
        print(formatted_name)
        price_in_div = row.select(".tbl-td.rate-value")

        dollar_buy = (
            price_in_div[0].find("span").text.replace(" ", "").replace("\n", "")
        )
        dollar_sell = (
            price_in_div[1].find("span").text.replace(" ", "").replace("\n", "")
        )
        dict_buy_dollar[formatted_name] = dollar_buy
        dict_sell_dollar[formatted_name] = dollar_sell
        list_of_buy_sell.append(
            f"Покупка доллара: {dollar_buy}, Продажа доллара: {dollar_sell}"
        )
        # print(f"Покупка доллара: {dollar_buy}, Продажа доллара: {dollar_sell}")

    for i, j in list(dict_buy_dollar.items()):
        if j == "-":
            del dict_buy_dollar[i]

    max_buy = max(dict_buy_dollar.values())
    max_buy_keys = list(
        filter(lambda key: dict_buy_dollar[key] == max_buy, dict_buy_dollar)
    )
    min_sell = min(dict_sell_dollar.values())
    min_sell_keys = list(
        filter(lambda key: dict_sell_dollar[key] == min_sell, dict_sell_dollar)
    )
    print(list_of_buy_sell)
    return f"Минимальная цена продажи доллара: {min(dict_sell_dollar.values())} - {min_sell_keys}; Максимальная цена покупки доллара: {max(dict_buy_dollar.values())} - {max_buy_keys}"


@bot.message_handler(commands=["start"])
def url(message):
    bot.send_message(message.chat.id, get_currency())


bot.infinity_polling(skip_pending=True)

@bot.message_handler(content_types=['stop']) 
def stop(message): 
    bot.stop_bot()