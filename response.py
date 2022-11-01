import pandas as pd

import Levenshtein
import jellyfish

from modules import preprocessing


def main():
    comp_name = input('Введите название компании:\n')

    # some company names for test
    # comp_name = 'Bridgestone （Huizhou）Synthetic Rubber Co., Ltd.'
    # comp_name = 'Rishichem Distributors Pvt., Ltd.'

    comp_name_alt = preprocessing(comp_name)

    df = pd.read_csv('./Source/preprocessed.csv', usecols=['name_2', 'name_2_alt'])

    # Levenshtein
    df.insert(2, 'l', df.name_2_alt.apply(lambda x: Levenshtein.ratio(x, comp_name_alt)))

    # Jaro Similarity
    df.insert(3, 'js', df.name_2_alt.apply(lambda x: jellyfish.jaro_similarity(x, comp_name_alt)))

    # Jaro-Winkler Similarity
    df.insert(4, 'jws', df.name_2_alt.apply(lambda x: jellyfish.jaro_winkler_similarity(x, comp_name_alt)))

    df.insert(5, 'mean', df[['l', 'js', 'jws']].mean(axis=1))

    res = df[['name_2', 'mean']].drop_duplicates(['name_2']).sort_values('mean', ignore_index=True,
                                                                         ascending=False).head(3)

    print(f'Топ три наиболее похожих названий компаний:')

    res['mean'] = res['mean'].apply(lambda x: round(x, 2))

    print(res.rename(columns={'name_2': 'Наименование', 'mean': 'Мера близости'}))


if __name__ == '__main__':
    main()
