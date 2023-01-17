import pandas, xlsxwriter
from datetime import date


def main():
    ano_inicio = 2017
    anos = range(ano_inicio, date.today().year+1)
    wb = xlsxwriter.Workbook('compilado.xlsx')
    plan1 = wb.add_worksheet('contagem')
    plan2 = wb.add_worksheet('percentual')

    contagem = pandas.DataFrame()
    percentual = pandas.DataFrame()
    for n, ano in enumerate(anos):
        plan1.write(0, n+1, str(ano))
        plan2.write(0, n+1, str(ano))
        url = f'https://www.megasena.com/resultados/ano-{ano}'

        df = pandas.read_html(url)[0]
        df = df.loc[df['Concurso / Data'].str.contains('Concurso')]
        dados = pandas.DataFrame(columns=[str(ano)])

        for i in range(len(df)):
            sorteio = df.iloc[i]

            novo = pandas.DataFrame(
                {str(ano): [int(i) for i in sorteio[1].split('  ')]})
            dados = pandas.concat([dados, novo])

        aux1 = dados[str(ano)].value_counts().to_frame()
        aux1.sort_index(axis=0, inplace=True)
        contagem = pandas.concat([contagem, aux1], axis=1)

        aux2 = (dados[str(ano)].value_counts(normalize = True)*600).to_frame()
        aux2.sort_index(axis=0, inplace=True)
        percentual = pandas.concat([percentual, aux2], axis=1)

        plan1.write(0, n+1, str(ano))

    for i in range(1, 61):
        plan1.write(i, 0, str(i))
        plan2.write(i, 0, str(i))
    
    for i in range(len(contagem)):
        for j in range(len(contagem.iloc[i])):
            plan1.write(i+1, j+1, contagem.iloc[i, j])

    for i in range(len(percentual)):
        for j in range(len(percentual.iloc[i])):
            plan2.write(i+1, j+1, percentual.iloc[i, j])
    
    wb.close()    


if __name__ == '__main__':
    main()