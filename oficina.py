
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

import json
import locale

Builder.load_file("menu.kv")
Builder.load_file("cadastroproduto.kv")
Builder.load_file("cadastroservico.kv")
Builder.load_file("removerproduto.kv")
Builder.load_file("removerservico.kv")
Builder.load_file("iniciaros.kv")


class RemoverProdutoPopup(Popup):
    def __init__(self, menu, **kwargs):
        super(RemoverProdutoPopup, self).__init__(**kwargs)
        self.menu = menu
        self.carregar_produtos()

    def carregar_produtos(self):
        self.ids.produtos_layout.clear_widgets()

        for produto in self.menu.produtos:
            
            produto_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)

            checkbox = CheckBox(size_hint_x=None, width=30)
            
            produto_layout.add_widget(checkbox)

            produto_layout.add_widget(Button(text=produto["nome"]))

            produto_layout.add_widget(Label(text=f'R${produto["preco"]:.2f}'))

            self.ids.produtos_layout.add_widget(produto_layout)
    
    def remover_produtos(self):
        produtos_layout = self.ids.produtos_layout

        produtos_para_remover = []

        for produto_layout in produtos_layout.children:
            checkbox = None
            for widget in produto_layout.children:
                if isinstance(widget, CheckBox):
                    checkbox = widget
                    break

            if checkbox is not None and checkbox.active:
                # Se o checkbox estiver marcado, armazene o produto para remoção
                nome_produto = None
                for widget in produto_layout.children:
                    if isinstance(widget, Button):
                        nome_produto = widget.text
                        break

                if nome_produto is not None:
                    produtos_para_remover.append(nome_produto)

        # Remover todos os produtos marcados de uma vez
        self.menu.produtos = [produto for produto in self.menu.produtos if produto["nome"] not in produtos_para_remover]

        self.carregar_produtos()
        self.menu.salvar_produtos()

class RemoverServicoPopup(Popup):
    def __init__(self, menu, **kwargs):
        super(RemoverServicoPopup, self).__init__(**kwargs)
        self.menu = menu
        self.carregar_servicos()

    def carregar_servicos(self):
        # Limpe os widgets antigos
        self.ids.servicos_layout.clear_widgets()

        for servico in self.menu.servicos:
            # Crie um layout para cada serviço
            servico_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)

            # Adicione um checkbox ao layout
            checkbox = CheckBox(size_hint_x=None, width=30)
            servico_layout.add_widget(checkbox)

            # Adicione o nome do serviço ao layout
            servico_layout.add_widget(Button(text=servico["nome"]))

            # Adicione o preço do serviço ao layout
            servico_layout.add_widget(Label(text=f'R${servico["preco"]:.2f}'))

            # Adicione o layout do serviço ao layout principal
            self.ids.servicos_layout.add_widget(servico_layout)

    def remover_servicos(self):
        # Adicione o código para remover os serviços selecionados
        servicos_layout = self.ids.servicos_layout

        servicos_para_remover = []

        for servico_layout in servicos_layout.children:
            checkbox = None
            for widget in servico_layout.children:
                if isinstance(widget, CheckBox):
                    checkbox = widget
                    break

            if checkbox is not None and checkbox.active:
                # Se o checkbox estiver marcado, armazene o serviço para remoção
                nome_servico = None
                for widget in servico_layout.children:
                    if isinstance(widget, Button):
                        nome_servico = widget.text
                        break

                if nome_servico is not None:
                    servicos_para_remover.append(nome_servico)

        # Remova todos os serviços marcados de uma vez
        self.menu.servicos = [servico for servico in self.menu.servicos if servico["nome"] not in servicos_para_remover]

        # Atualize a exibição após a remoção
        self.carregar_servicos()
        # Salve as alterações nos serviços
        self.menu.salvar_servicos()
# oficina.py

class IniciarOsPopupContent(BoxLayout):
    def limpar_itens_selecionados(self):
        self.ids.itens_selecionados_layout.clear_widgets()

class IniciarOs(BoxLayout):
    itens_selecionados = []

    def __init__(self, menu, **kwargs):
        super(IniciarOs, self).__init__(**kwargs)
        self.menu = menu
        self.carregar_produtos_servicos()

    def carregar_produtos_servicos(self):
        produtos_servicos_layout = self.ids.produtos_servicos_layout
        produtos_servicos_layout.clear_widgets()

        for produto in self.menu.produtos:
            checkbox = CheckBox(size_hint_x=None, width='30dp')
            produto_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            produto_layout.add_widget(checkbox)
            produto_layout.add_widget(Label(text=f"{produto['nome']} - R${produto['preco']:.2f}"))
            produtos_servicos_layout.add_widget(produto_layout)

        for servico in self.menu.servicos:
            checkbox = CheckBox(size_hint_x=None, width='30dp')
            servico_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            servico_layout.add_widget(checkbox)
            servico_layout.add_widget(Label(text=f"{servico['nome']} - R${servico['preco']:.2f}"))
            produtos_servicos_layout.add_widget(servico_layout)

    def on_checkbox_active(self, checkbox, value, nome_item, preco_item):
        if value:
            self.itens_selecionados.append({'nome': nome_item, 'preco': preco_item})
        else:
            self.itens_selecionados = [item for item in self.itens_selecionados if item['nome'] != nome_item]

    def fechar_os_popup(self):
        total = sum(item['preco'] for item in self.itens_selecionados)

        popup_content = IniciarOsPopupContent()

        for item in self.itens_selecionados:
            nome_label = Label(text=item['nome'])
            preco_label = Label(text=f'R${item["preco"]:.2f}')

            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            item_layout.add_widget(nome_label)
            item_layout.add_widget(preco_label)
            popup_content.ids.itens_selecionados_layout.add_widget(item_layout)

        popup_content.ids.itens_selecionados_layout.add_widget(Label(text=f'Total: R${total:.2f}', size_hint_y=None, height='30dp'))

        popup = Popup(title='Itens Selecionados', content=popup_content, size_hint=(None, None), size=(600, 400))
        popup.open()
class Menu(BoxLayout):
    
    def carregar_itens(self, arquivo_json):
        try:
            with open(arquivo_json, "r") as file:
                itens = json.load(file)
        except FileNotFoundError:
            itens = []
        return itens
    
    def carregar_produtos(self):
        try:
            with open("produtos.json", "r") as file:
                produtos = json.load(file)
        except FileNotFoundError:
            produtos = []
        return produtos

    def carregar_servicos(self):
        try:
            with open("servicos.json", "r") as file:
                servicos = json.load(file)
        except FileNotFoundError:
            servicos = []
        return servicos
    
    
    def iniciar_os_popup(self):
        popup = Popup(title='Iniciar OS', content=IniciarOs(menu=self), size_hint=(None, None), size=(600, 800))
        popup.open()
    # def iniciar_os_popup(self):
    #     popup = Popup(title='Iniciar OS', content=iniciaros(menu=self), size_hint=(None, None), size=(600, 400))
    #     popup.open()
    
    def __init__(self, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.produtos = self.carregar_produtos()
        self.servicos = self.carregar_servicos()
    
    def iniciar_os_popup(self):
        popup = Popup(title='Iniciar OS', content=IniciarOs(menu=self), size_hint=(None, None), size=(600, 800))
        popup.open()
    
    def cadastrar_servico_popup(self):
        popup = Popup(title='Cadastrar Serviço', content=cadastroservico(menu=self), size_hint=(None, None), size=(600, 400))
        popup.open()

    def remover_servico_popup(self):
        popup = RemoverServicoPopup(title="Remover Serviço",menu=self, size_hint=(None, None), size=(600, 800))
        popup.open()
    
    def carregar_servicos(self):
        try:
            with open("servicos.json", "r") as file:
                servicos = json.load(file)
        except FileNotFoundError:
            servicos = []
        return servicos

    def salvar_servicos(self):
        with open("servicos.json", "w") as file:
            json.dump(self.servicos, file)


    def cadastrar_produto_popup(self):
        popup = Popup(title='Cadastrar Produto', content=cadastroproduto(menu=self), size_hint=(None, None), size=(600, 400))
        popup.open()

    def carregar_produtos(self):
        try:
            with open("produtos.json", "r") as file:
                produtos = json.load(file)
        except FileNotFoundError:
            produtos = []
        return produtos

    def salvar_produtos(self):
        with open("produtos.json", "w") as file:
            json.dump(self.produtos, file)
    
    def remover_produto_popup(self):
        popup = RemoverProdutoPopup(title="Remover Produto" ,menu=self, size_hint=(None, None), size=(600, 800))
        popup.open()
                

    def sair(self):
        self.salvar_produtos()
        self.salvar_servicos()
        App.get_running_app().stop()

class cadastroproduto(BoxLayout):
    def __init__(self, menu, **kwargs):
        super(cadastroproduto, self).__init__(**kwargs)
        self.menu = menu

    def cadastrar_produto(self, nome, preco_text):
        try:
            preco = float(preco_text.replace('R$', '').replace('.', '').replace(',', '.'))  # Remover 'R$', '.' e substituir ',' por '.'
            produto = {"nome": nome, "preco": preco}
            self.menu.produtos.append(produto)
            print(f"Produto cadastrado: Nome: {nome}, Preço: R${preco}")
            self.menu.salvar_produtos()
            self.voltar()
        except ValueError:
            print("Erro ao cadastrar o produto. Certifique-se de que o preço é um número válido.")

    def formatar_preco(self):
        try:
            preco_text = self.ids.preco_input.text
            preco = float(preco_text.replace('R$', '').replace('.', '').replace(',', '.'))  # Remover 'R$', '.' e substituir ',' por '.'
            preco_formatado = locale.currency(preco, grouping=True, symbol=None)
            self.ids.preco_input.text = preco_formatado
        except ValueError:
            pass


    def voltar(self):
        self.parent.parent.parent.dismiss()  # Fechar o popup

class cadastroservico(BoxLayout):
    def __init__(self, menu, **kwargs):
        super(cadastroservico, self).__init__(**kwargs)
        self.menu = menu

    def cadastrar_servico(self, nome, preco_text):
        try:
            preco = float(preco_text.replace('R$', '').replace('.', '').replace(',', '.'))  # Remover 'R$', '.' e substituir ',' por '.'
            servico = {"nome": nome, "preco": preco}
            self.menu.servicos.append(servico)
            print(f"Serviço cadastrado: Nome: {nome}, Preço: R${preco}")
            self.menu.salvar_servicos()
            self.voltar()
        except ValueError:
            print("Erro ao cadastrar o serviço. Certifique-se de que o preço é um número válido.")

    def formatar_preco(self):
        try:
            preco_text = self.ids.preco_input.text
            preco = float(preco_text.replace('R$', '').replace('.', '').replace(',', '.'))  # Remover 'R$', '.' e substituir ',' por '.'
            preco_formatado = locale.currency(preco, grouping=True, symbol=None)
            self.ids.preco_input.text = preco_formatado
        except ValueError:
            pass

    def voltar(self):
        self.parent.parent.parent.dismiss()  # Fechar o popup

class MyApp(App):
    def build(self):
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        return Menu()

if __name__ == '__main__':
    MyApp().run()




