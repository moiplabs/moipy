#*-* encoding:utf-8 *-*
from lxml import etree
import pycurl
import os

class MoIP:
    """
    Classe para montar o XML de instrucoes

    Exemplo de uso:
    
    >>> moip = MoIP()
    >>> moip.set_credenciais(token='meu_token',key='minha_key')   # doctest: +ELLIPSIS 
    <__main__.MoIP instance at 0x...>
    >>> moip.set_razao('Razao do pagamento') # doctest: +ELLIPSIS
    <__main__.MoIP instance at 0x...>
    >>> moip.set_valor('12345') # doctest: +ELLIPSIS
    <__main__.MoIP instance at 0x...>
    
    Lembrando que o valor deve ser especificado em centavos. Portanto,
    R$ 123,45 = 12345
    
    O MoIPy implementa o padrão 'Fluent Interfaces', por isso a instância do
    objeto MoIP é retornada a cada chamada de método
    """

    #url do sandbox
    url = "https://desenvolvedor.moip.com.br/sandbox/ws/alpha/EnviarInstrucao/Unica"


    def __init__(self):
        """
        Inicializa o objeto MoIP.
        >>> m = MoIP()
        >>> type(m.enviar_instrucao)
        <type 'lxml.etree._Element'>
        >>> type(m.enviar_instrucao[0])
        <type 'lxml.etree._Element'>

        """
        enviar_instrucao = etree.Element("EnviarInstrucao")
        instrucao_unica = etree.SubElement(enviar_instrucao,"InstrucaoUnica")
        self.enviar_instrucao = enviar_instrucao 
        

    def set_razao(self, razao):
        """
        Exemplo de uso:

        >>> m = MoIP()
        >>> m.set_razao('Razao do Pagamento') # doctest: +ELLIPSIS
        <__main__.MoIP instance at 0x...>

        No final, o nó 'Razão' será adicionado:

        >>> m.enviar_instrucao.xpath('//Razao')[0].text
        'Razao do Pagamento'

        """
        instrucao_unica = self.enviar_instrucao[0]
 
        _razao = etree.SubElement(instrucao_unica,"Razao")
        _razao.text = razao
        return self
     
    def set_valor(self, valor):
        valor = str(valor)

        instrucao_unica = self.enviar_instrucao[0]

        valores = etree.SubElement(instrucao_unica,"Valores")
        _valor = etree.SubElement(valores,"Valor",moeda="BRL")
        _valor.text = valor 
        return self

    def get_xml(self):
        """
        Retorna o XML gerado até agora

        >>> m = MoIP() # doctest: +ELLIPSIS 
        >>> m.get_xml()
        '<EnviarInstrucao><InstrucaoUnica/></EnviarInstrucao>'
        """
        return etree.tostring(self.enviar_instrucao)

    def set_id_proprio(self,id):
        instrucao_unica = self.enviar_instrucao[0]
        id_proprio = etree.SubElement(instrucao_unica,"IdProprio")
        id_proprio.text = id
        return self

    def set_data_vencimento(self,data):
        instrucao_unica = self.enviar_instrucao[0]
        data_vencimento = etree.SubElement(instrucao_unica,"DataVencimento")
        data_vencimento.text = data
        return self

    def set_recebedor(self,login_moip,email,apelido):
        instrucao_unica = self.enviar_instrucao[0]
        recebedor = etree.SubElement(instrucao_unica,"Recebedor")
        _login_moip = etree.SubElement(recebedor,"LoginMoip")
        _login_moip.text = login_moip
        _email = etree.SubElement(recebedor,"Email")
        _email.text = email
        _apelido = etree.SubElement(recebedor,"Apelido")
        _apelido.text = apelido

        return self
    
    def set_ambiente(self,ambiente):
        """
        Configura o ambiente (Produção ou Sandbox)
        
        >>> m = MoIP()
        >>> m.set_ambiente('sandbox') # doctest: +ELLIPSIS 
        <__main__.MoIP instance at 0x...>
        >>> m.url
        'https://desenvolvedor.moip.com.br/sandbox/ws/alpha/EnviarInstrucao/Unica'
        >>> m.set_ambiente('producao') # doctest: +ELLIPSIS 
        <__main__.MoIP instance at 0x...>
        >>> m.url
        'https://www.moip.com.br/ws/alpha/EnviarInstrucao/Unica'

        """
        if ambiente=="sandbox":
            self.url = "https://desenvolvedor.moip.com.br/sandbox/ws/alpha/EnviarInstrucao/Unica"
        elif ambiente=="producao":
            self.url = "https://www.moip.com.br/ws/alpha/EnviarInstrucao/Unica"

        return self

    def envia(self):
        r = RespostaMoIP()
        
        passwd = self.token+":"+self.key

        passwd64 = base64.b64encode(passwd)

        c.setopt(pycurl.URL,self.url)
        c.setopt(pycurl.HTTPHEADER,["Authorization: Basic "+passwd64])
        c.setopt(pycurl.USERAGENT,"Mozilla/4.0")
        c.setopt(pycurl.USERPWD,passwd)
        c.setopt(pycurl.POST,True)
        c.setopt(pycurl.POSTFIELDS,self.get_xml())
        c.setopt(pycurl.WRITEFUNCTION,r.callback)
        c.perform()
        c.close()
         
        self.retorno = r.conteudo
        return self

    def set_credenciais(self,token,key):
        self.token = token
        self.key = key
        return self

    def get_resposta(self):
        resposta = etree.XML(self.retorno)
        return {'sucesso':resposta[0][1].text,'token':resposta[0][2].text} 

class RespostaMoIP:
    def __init__(self):
        self.conteudo = ''

    def callback(self,buf):
        self.conteudo = buf        


if __name__ == '__main__':
    import doctest
    doctest.testmod(report=True,verbose=True)
