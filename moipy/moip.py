#! /usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import pycurl

from lxml import etree


class Moip():

    def __init__(self, razao, xml_node = "EnviarInstrucao"):
        
        if xml_node:
            self.xml_node = etree.Element(xml_node)
            
            self._monta_xml(self.xml_node, unique = True, InstrucaoUnica = dict(Razao=razao))
            
            
    def _monta_xml(self, parent, unique=False, **kwargs):
        """Metodo interno que monta o XML utilizando os parametros passados
        por outros metodos."""
        
        if isinstance(parent, etree._Element):
            node_parent = parent
        else:
            node_parent = etree.Element(parent)
        
        for k,v in kwargs.items():
            if unique and node_parent.find(k) is not None:
                node = node_parent.find(k) 
            else:
                node = etree.SubElement(node_parent, k)
               
            if isinstance(v, dict):
                self._monta_xml(node, **v)
            else:
                node.text = v
                
        return node_parent


    def set_credenciais(self, token, key):
        
        self.token = token
        self.key = key
        
        return self
    

    def set_ambiente(self,ambiente):

        if ambiente=="sandbox":
            self.url = "https://desenvolvedor.moip.com.br/sandbox/ws/alpha/EnviarInstrucao/Unica"
        elif ambiente=="producao":
            self.url = "https://www.moip.com.br/ws/alpha/EnviarInstrucao/Unica"
        else:
            raise ValueError("Ambiente inválido")
        
     
    def set_valor(self, valor):
        
        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(Valores=dict(Valor=valor)))
        
        return self


    def set_id_proprio(self, id):
        
        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(IdProprio=id))
        
        return self


    def set_data_vencimento(self,data):
        
        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(DataVencimento=data))
        
        return self


    def set_recebedor(self,login_moip,email,apelido):
        
        self._monta_xml(self.xml_node, unique=True, InstrucaoUnica=dict(Recebedor=dict(LoginMoip=login_moip, Email=email, Apelido=apelido)))

        return self
    

    def envia(self):
        resposta = RespostaMoIP()
        
        passwd = self.token + ":" + self.key

        passwd64 = base64.b64encode(passwd)
        
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL,self.url)
        curl.setopt(pycurl.HTTPHEADER,["Authorization: Basic " + passwd64])
        curl.setopt(pycurl.USERAGENT,"Mozilla/4.0")
        curl.setopt(pycurl.USERPWD,passwd)
        curl.setopt(pycurl.POST,True)
        curl.setopt(pycurl.POSTFIELDS,self._get_xml())
        curl.setopt(pycurl.WRITEFUNCTION,resposta.callback)
        curl.perform()
        curl.close()
         
        self.retorno = resposta.conteudo

        return self


    def _get_xml(self):
        """Metodo interno que retorna o objeto etree em formato string"""
        
        return etree.tostring(self.xml_node)
    

    def get_resposta(self):
        
        resposta = etree.XML(self.retorno)
        return {'sucesso':resposta[0][1].text,'token':resposta[0][2].text} 


class RespostaMoIP:
    def __init__(self):
        self.conteudo = ''


    def callback(self,buf):
        self.conteudo = buf        