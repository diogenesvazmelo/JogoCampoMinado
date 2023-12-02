import sys
sys.path.insert(0, '../src')
import unittest
from menu_principal import *

import unittest.mock

class TestMenuPrincipal(unittest.TestCase):
    def testTamanhoMapaIndexError(self):        
        menu = MenuPrincipal()
        l, c, m = menu._trata_string_tamanho_mapa('6')
        self.assertEqual('Entrada Inválida! (IndexError)', m)

    def testTamanhoMapaValueError(self):        
        menu = MenuPrincipal()
        l, c, m = menu._trata_string_tamanho_mapa('6x')
        self.assertEqual('Entrada Inválida! (ValueError)', m)

    def testTamanhoMapaInvalido(self):        
        menu = MenuPrincipal()
        l, c, m = menu._trata_string_tamanho_mapa('0x5')
        self.assertEqual('Entrada Inválida!', m)

    def testTamanhoMapaValidoLinha(self):        
        menu = MenuPrincipal()
        l, c, m = menu._trata_string_tamanho_mapa('5x4')
        self.assertEqual(5, l)

    def testTamanhoMapaValidoColuna(self):        
        menu = MenuPrincipal()
        l, c, m = menu._trata_string_tamanho_mapa('5x4')
        self.assertEqual(4, c)

    def testTamanhoMapaValidoMsg(self):        
        menu = MenuPrincipal()
        l, c, m = menu._trata_string_tamanho_mapa('5x4')
        self.assertEqual('', m)