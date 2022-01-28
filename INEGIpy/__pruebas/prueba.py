### scripts para hacer pruebas 

from indicador_general import IndicadorGeneral

token = '92170321-528f-f1dd-5d59-f8613e072746'

def prueba_indicador_general(token):
    print('Prueba Indicador_General.obtener_df()')
    indicador  = IndicadorGeneral(token)
    print("definiendo indicadores dentro de obtener_df()")
    print(indicador.obtener_df(['493925'],['BIE'],['PIB'],None,None).head())


if __name__ == '__main__':
    prueba_indicador_general(token)



