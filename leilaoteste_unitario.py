import unittest

class Arrematante:
    def __init__(self, nome, cpf, email):
        self.nome = nome
        self.cpf = cpf
        self.email = email


class Leilao:
    def __init__(self, valorMin, dataExp):
        self.status = "INATIVO"
        self.recebeLance = False
        self.dataExp = dataExp
        self.valorMin = valorMin
        self.lances = []
        self.ultimoArrematante = None

    def abrirLeilao(self):
        if self.status == "INATIVO":
            self.status = "ABERTO"
        else:
            print("Não é possível realizar essa ação.")

    def expLeilao(self, dia):
        if dia > self.dataExp:
            self.status = "EXPIRADO"
        else:
            print("Não é possível realizar essa ação.")

    def finLeilao(self):
        if self.status == "EXPIRADO" or self.status == "ABERTO":
            self.status = "FINALIZADO"
        else:
            print("Não é possível realizar essa ação.")

    def darLance(self, lance, arrematante):
        if self.status != "ABERTO":
            print("O leilão não está aberto para lances.")
            return False
        if self.ultimoArrematante == arrematante:
            print("Não é possível dar dois lances seguidos por um mesmo arrematante")
            return False
        if lance < self.valorMin:
            print("É necessário um lance maior que o valor mínimo")
            return False
        if self.lances and lance <= max(self.lances):
            print("É necessário um lance maior que o lance atual")
            return False
        self.lances.append(lance)
        self.ultimoArrematante = arrematante
        print("Lance de " + str(lance) + " aplicado!")
        return True

    def concluirLeilao(self):
        self.status = "FINALIZADO"

    def listaLances(self):
        return sorted(self.lances)

    def maiorLance(self):
        if self.lances:
            return max(self.lances)
        else:
            return None

    def menorLance(self):
        if self.lances:
            return min(self.lances)
        else:
            return None

    def enviarEmailVencedor(self):
        if self.status == "FINALIZADO" and self.ultimoArrematante:
            print(f"E-mail enviado para {self.ultimoArrematante.email} parabenizando-o pelo arremate.")

# Exemplo de uso:
arrematante1 = Arrematante("Fulano", "123.456.789-00", "fulano@example.com")
arrematante2 = Arrematante("Ciclano", "987.654.321-00", "ciclano@example.com")

leilao = Leilao(100, 30)  # Valor mínimo e dias de expiração

leilao.abrirLeilao()
leilao.darLance(150, arrematante1)
leilao.darLance(151, arrematante1)
leilao.darLance(200, arrematante2)
leilao.concluirLeilao()

print("Lista de Lances:", leilao.listaLances())
print("Maior Lance:", leilao.maiorLance())
print("Menor Lance:", leilao.menorLance())

leilao.enviarEmailVencedor()

class TestArrematante(unittest.TestCase):
    def test_init(self):
        arrematante = Arrematante("Fulano", "123.456.789-00", "fulano@example.com")
        self.assertEqual(arrematante.nome, "Fulano")
        self.assertEqual(arrematante.cpf, "123.456.789-00")
        self.assertEqual(arrematante.email, "fulano@example.com")

class TestLeilao(unittest.TestCase):
    def setUp(self):
        self.leilao = Leilao(100, 30)
        self.arrematante1 = Arrematante("Fulano", "123.456.789-00", "fulano@example.com")
        self.arrematante2 = Arrematante("Ciclano", "987.654.321-00", "ciclano@example.com")

    def test_init(self):
        self.assertEqual(self.leilao.status, "INATIVO")
        self.assertEqual(self.leilao.recebeLance, False)
        self.assertEqual(self.leilao.dataExp, 30)
        self.assertEqual(self.leilao.valorMin, 100)
        self.assertEqual(self.leilao.lances, [])
        self.assertEqual(self.leilao.ultimoArrematante, None)

    def test_abrirLeilao(self):
        self.leilao.abrirLeilao()
        self.assertEqual(self.leilao.status, "ABERTO")

    def test_expLeilao(self):
        self.leilao.expLeilao(31)
        self.assertEqual(self.leilao.status, "EXPIRADO")

    def test_finLeilao(self):
        self.leilao.abrirLeilao()
        self.leilao.finLeilao()
        self.assertEqual(self.leilao.status, "FINALIZADO")

    def test_darLance_LeilaoNaoAberto(self):
        with self.assertRaises(ValueError):
            self.leilao.darLance(150, self.arrematante1)

    def test_darLance_MesmoArrematante(self):
        self.leilao.abrirLeilao()
        self.leilao.darLance(150, self.arrematante1)
        with self.assertRaises(ValueError):
            self.leilao.darLance(151, self.arrematante1)  # corrigido para "self.leilao"

    def test_darLance_ValorInferiorMinimo(self):
        self.leilao.abrirLeilao()
        with self.assertRaises(ValueError):
            self.leilao.darLance(99, self.arrematante1)

    def test_darLance_ValorMenorQueLanceAtual(self):
        self.leilao.abrirLeilao()
        self.leilao.darLance(150, self.arrematante1)
        with self.assertRaises(ValueError):
            self.leilao.darLance(149, self.arrematante2)

    def test_darLance_Sucesso(self):
        self.leilao.abrirLeilao()
        self.assertTrue(self.leilao.darLance(150, self.arrematante1))
        self.assertEqual(self.leilao.lances, [150])
        self.assertEqual(self.leilao.ultimoArrematante, self.arrematante1)

    def test_concluirLeilao(self):
        self.leilao.abrirLeilao()
        self.leilao.darLance(150, self.arrematante1)
        self.leilao.concluirLeilao()
        self.assertEqual(self.leilao.status, "FINALIZADO")

