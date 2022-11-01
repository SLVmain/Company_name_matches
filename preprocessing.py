import pandas as pd

from modules import preprocessing


def preprocess(path: str) -> None:

    df = pd.read_csv(path, usecols=['name_1', 'name_2'])

    df['name_1_alt'] = df.name_1.apply(lambda x: preprocessing(x))
    df['name_2_alt'] = df.name_2.apply(lambda x: preprocessing(x))

    df.to_csv('./Source/preprocessed.csv', index=False)


if __name__ == '__main__':
    # Путь для загрузки начальных данных из облака:
    path = 'https://getfile.dokpub.com/yandex/get/https://disk.yandex.ru/d/6YzocVnWPIP1KQ'

    # Путь для загрузки начальных данных размещённых локально в каталог проекта по указанному пути:
    # path = './Source/train.csv'

    preprocess(path)
    df = pd.read_csv('./Source/preprocessed.csv')
    print(df[['name_2', 'name_2_alt']].head())
