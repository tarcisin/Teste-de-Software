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
