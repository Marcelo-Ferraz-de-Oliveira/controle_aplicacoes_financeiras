from webapp.tradutor import nome_pregao_to_codigo

def test_nome_pregao_to_codigo ():
    names = ('ABEVB161ON 15,62', 'AMBEV S/AON', 'IRBRB330ON 3,30','ISHARE SP500CI','PETROBRASPN', 'USIMINASPNA')
    expected_codes = ['ABEVB161','ABEV3','IRBRB330','IVVB11','PETR4','USIM5']
    codes = []
    for name in names:
        codes.append(nome_pregao_to_codigo(name))
    assert expected_codes == codes