MoIPy
=====

Camada de abstração para integração via API com o MoIP em Python.

Dependências
------------

O MoIPy tem as seguintes dependências:

 - lxml
 - pycurl

Instalação
----------

A instalação pode ser feita via pip:

    pip install moipy

Ou então pelo repositório do Github:

    git clone git://github.com/moiplabs/moipy.git
    cd moipy
    python moipy/moip.py # executa os testes
    python setup.py build
    sudo python setup.py install

Uso
----

Basta importar a classe do MoIP e sair brincando :-)

    from moipy import MoIP

    moip = MoIP()

    moip.set_credenciais(token='seu_token',key='sua_key')
    moip.set_razao('Razao do Pagmento')
    moip.set_ambiente('sandbox') # sandbox é o default
    moip.set_valor(12345)
    moip.set_id_proprio('abc123-')
    moip.envia()
    print moip.get_resposta() # {sucesso:'Sucesso','token':'KJHSDASKD392847293AHFJKDSAH'}


Licença
------

MoIPy Copyright (C) 2010 Herberth Amaral

This library is free software; you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation; either version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along with this library; if not, write to the Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
