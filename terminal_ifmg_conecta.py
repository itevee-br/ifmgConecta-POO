# ============================================
# SISTEMA DE CONTEUDOS GRATUITOS
# ============================================

import json
import os

# armazenamento de dados
conteudos = []
usuarios = []  # Lista de usuarios cadastrados
usuario_logado = None  # Usuario atualmente logado
ARQUIVO_JSON = "conteudos.json"
ARQUIVO_USUARIOS = "usuarios.json"


# ============================================
# FUNCOES DE PERSISTENCIA (JSON)
# ============================================

def salvar_dados():
    """Salva todos os conteudos em um arquivo JSON"""
    dados = []
    for item in conteudos:
        if isinstance(item, Evento):
            dados.append({
                "tipo": "evento",
                "titulo": item.titulo,
                "descricao": item.descricao,
                "data": item.data,
                "local": item.local
            })
        elif isinstance(item, Curso):
            dados.append({
                "tipo": "curso",
                "titulo": item.titulo,
                "descricao": item.descricao,
                "link": item.link
            })
    
    try:
        with open(ARQUIVO_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"[ERRO] Falha ao salvar dados: {e}")
        return False


def carregar_dados():
    """Carrega os dados do arquivo JSON"""
    global conteudos
    
    if not os.path.exists(ARQUIVO_JSON):
        return False
    
    try:
        with open(ARQUIVO_JSON, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        conteudos = []
        for item in dados:
            if item["tipo"] == "evento":
                evento = Evento(
                    item["titulo"],
                    item["descricao"],
                    item["data"],
                    item["local"]
                )
                conteudos.append(evento)
            elif item["tipo"] == "curso":
                curso = Curso(
                    item["titulo"],
                    item["descricao"],
                    item["link"]
                )
                conteudos.append(curso)
        
        return True
    except:
        conteudos = []
        return False


def salvar_usuarios():
    """Salva a lista de usuarios em JSON"""
    dados = []
    for user in usuarios:
        # Verificar se e admin
        is_admin = isinstance(user, Adm)
        dados.append({
            "nome": user.nome,
            "senha": user._senha,
            "favoritos": [item.titulo for item in user._favoritos],
            "is_admin": is_admin  # Salvar se e admin
        })
    
    try:
        with open(ARQUIVO_USUARIOS, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False


def carregar_usuarios():
    """Carrega a lista de usuarios do JSON"""
    global usuarios
    
    if not os.path.exists(ARQUIVO_USUARIOS):
        return False
    
    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        usuarios = []
        for item in dados:
            # Criar usuario com base no tipo
            if item.get("is_admin", False):
                user = Adm(item["nome"], item["senha"])
            else:
                user = Usuario(item["nome"], item["senha"])
            
            # Recuperar favoritos pelo titulo
            for titulo in item["favoritos"]:
                for conteudo in conteudos:
                    if conteudo.titulo == titulo:
                        user._favoritos.append(conteudo)
            usuarios.append(user)
        
        return True
    except:
        usuarios = []
        return False


def carregar_dados_automatico():
    """Tenta carregar dados automaticamente ao iniciar"""
    dados_ok = carregar_dados()
    usuarios_ok = carregar_usuarios()
    
    if not dados_ok:
        print("[INFO] Nenhum arquivo de conteudos encontrado. Criando dados de exemplo...")
        criar_dados_exemplo()
    
    if not usuarios_ok:
        print("[INFO] Nenhum arquivo de usuarios encontrado.")
    
    return dados_ok


def criar_dados_exemplo():
    """Cria dados de exemplo"""
    adm_temp = Adm("admin", "1234")
    adm_temp.criar_evento("Workshop de Python", "Aprenda Python do zero", "15/07/2026", "Online")
    adm_temp.criar_evento("Feira de Livros", "Troca de livros gratuita", "20/07/2026", "Praca Central")
    adm_temp.criar_curso("Design Gratis", "Introducao ao design grafico", "https://cursogratis.com/design")
    adm_temp.criar_curso("Financas Pessoais", "Aprenda a organizar suas financas", "https://cursogratis.com/financas")
    
    # Salvar dados de exemplo
    salvar_dados()


# ============================================
# FUNCOES DE LISTAGEM (qualquer usuario pode usar)
# ============================================

def listar_conteudos():
    """Lista todos os conteudos"""
    if not conteudos:
        print("[INFO] Nenhum conteudo cadastrado.")
        return
    
    print("\n" + "="*50)
    print("TODOS OS CONTEUDOS")
    print("="*50)
    for i, item in enumerate(conteudos, 1):
        print(f"\n[CONTEUDO {i}]")
        item.exibir()
        print("-"*30)


def listar_eventos():
    """Lista apenas eventos"""
    eventos = [item for item in conteudos if isinstance(item, Evento)]
    if not eventos:
        print("[INFO] Nenhum evento cadastrado.")
        return
    
    print("\n" + "="*50)
    print("EVENTOS")
    print("="*50)
    for i, item in enumerate(eventos, 1):
        print(f"\n[EVENTO {i}]")
        item.exibir()
        print("-"*30)


def listar_cursos():
    """Lista apenas cursos"""
    cursos = [item for item in conteudos if isinstance(item, Curso)]
    if not cursos:
        print("[INFO] Nenhum curso cadastrado.")
        return
    
    print("\n" + "="*50)
    print("CURSOS")
    print("="*50)
    for i, item in enumerate(cursos, 1):
        print(f"\n[CURSO {i}]")
        item.exibir()
        print("-"*30)


def buscar_por_titulo(titulo):
    """Busca conteudo por titulo"""
    resultados = []
    for item in conteudos:
        if titulo.lower() in item.titulo.lower():
            resultados.append(item)
    
    if resultados:
        print(f"\n[OK] Encontrados {len(resultados)} resultado(s):")
        for item in resultados:
            item.exibir()
            print()
        return resultados
    else:
        print(f"[AVISO] Nenhum conteudo encontrado com '{titulo}'")
        return []


# ============================================
# CLASSES
# ============================================

class Usuario:
    def __init__(self, nome, senha):
        self._nome = nome
        self._senha = senha
        self._favoritos = []
    
    @property
    def nome(self):
        return self._nome
    
    def adicionar_favorito(self, item):
        if item not in self._favoritos:
            self._favoritos.append(item)
            salvar_usuarios()  # Salvar mudancas
            print(f"[OK] '{item.titulo}' adicionado aos favoritos.")
        else:
            print(f"[AVISO] '{item.titulo}' ja esta nos favoritos.")
    
    def remover_favorito(self, item):
        if item in self._favoritos:
            self._favoritos.remove(item)
            salvar_usuarios()  # Salvar mudancas
            print(f"[OK] '{item.titulo}' removido dos favoritos.")
        else:
            print(f"[AVISO] '{item.titulo}' nao esta nos favoritos.")
    
    def listar_favoritos(self):
        if not self._favoritos:
            print("[INFO] Nenhum favorito.")
            return
        
        print("\n" + "="*50)
        print(f"FAVORITOS DE {self._nome}")
        print("="*50)
        for i, item in enumerate(self._favoritos, 1):
            print(f"\n[FAVORITO {i}]")
            item.exibir()
            print("-"*30)


class Adm(Usuario):
    def __init__(self, nome, senha):
        super().__init__(nome, senha)
    
    # ===== CREATE (apenas admin) =====
    def criar_evento(self, titulo, descricao, data, local):
        evento = Evento(titulo, descricao, data, local)
        conteudos.append(evento)
        salvar_dados()
        print(f"[OK] Evento '{titulo}' criado com sucesso!")
        return evento
    
    def criar_curso(self, titulo, descricao, link):
        curso = Curso(titulo, descricao, link)
        conteudos.append(curso)
        salvar_dados()
        print(f"[OK] Curso '{titulo}' criado com sucesso!")
        return curso
    
    # ===== UPDATE (apenas admin) =====
    def atualizar_evento_por_titulo(self, titulo, novo_titulo=None, nova_descricao=None, 
                                     nova_data=None, novo_local=None):
        for item in conteudos:
            if isinstance(item, Evento) and item.titulo.lower() == titulo.lower():
                if novo_titulo:
                    item.titulo = novo_titulo
                if nova_descricao:
                    item.descricao = nova_descricao
                if nova_data:
                    item.data = nova_data
                if novo_local:
                    item.local = novo_local
                salvar_dados()
                print(f"[OK] Evento '{titulo}' atualizado com sucesso!")
                return True
        print(f"[ERRO] Evento '{titulo}' nao encontrado.")
        return False
    
    def atualizar_curso_por_titulo(self, titulo, novo_titulo=None, nova_descricao=None, 
                                    novo_link=None):
        for item in conteudos:
            if isinstance(item, Curso) and item.titulo.lower() == titulo.lower():
                if novo_titulo:
                    item.titulo = novo_titulo
                if nova_descricao:
                    item.descricao = nova_descricao
                if novo_link:
                    item.link = novo_link
                salvar_dados()
                print(f"[OK] Curso '{titulo}' atualizado com sucesso!")
                return True
        print(f"[ERRO] Curso '{titulo}' nao encontrado.")
        return False
    
    # ===== DELETE (apenas admin) =====
    def deletar_por_titulo(self, titulo):
        for i, item in enumerate(conteudos):
            if item.titulo.lower() == titulo.lower():
                tipo = "Evento" if isinstance(item, Evento) else "Curso"
                conteudos.pop(i)
                salvar_dados()
                print(f"[OK] {tipo} '{titulo}' deletado com sucesso!")
                return True
        print(f"[ERRO] Conteudo '{titulo}' nao encontrado.")
        return False


class Conteudo:
    def __init__(self, titulo, descricao):
        self.titulo = titulo
        self.descricao = descricao
    
    def exibir(self):
        print(f"Titulo: {self.titulo}")
        print(f"Descricao: {self.descricao}")


class Evento(Conteudo):
    def __init__(self, titulo, descricao, data, local):
        super().__init__(titulo, descricao)
        self.data = data
        self.local = local
    
    def exibir(self):
        super().exibir()
        print(f"Data: {self.data}")
        print(f"Local: {self.local}")


class Curso(Conteudo):
    def __init__(self, titulo, descricao, link):
        super().__init__(titulo, descricao)
        self.link = link

    def exibir(self):
        super().exibir()
        print(f"Link: {self.link}")


# ============================================
# SISTEMA DE LOGIN
# ============================================

def fazer_login():
    """Tela de login"""
    global usuario_logado
    
    print("\n" + "="*50)
    print("SISTEMA DE CONTEUDOS GRATUITOS")
    print("="*50)
    print("Debug - Login adm: admin / senha: 1234")
    print("-"*50)
    print("1 - Login")
    print("2 - Criar Conta")
    print("0 - Sair")
    print("-"*50)
    
    opcao = input("Escolha uma opcao: ")
    
    if opcao == "1":
        return tela_login()
    elif opcao == "2":
        return tela_criar_conta()
    elif opcao == "0":
        return False
    else:
        print("[ERRO] Opcao invalida!")
        return fazer_login()


def tela_login():
    """Tela para fazer login"""
    global usuario_logado
    
    print("\n" + "="*50)
    print("LOGIN")
    print("="*50)
    nome = input("Nome: ")
    senha = input("Senha: ")
    
    for user in usuarios:
        if user.nome == nome and user._senha == senha:
            usuario_logado = user
            print(f"\n[OK] Bem-vindo(a), {nome}!")
            return True
    
    print("\n[ERRO] Nome ou senha incorretos!")
    return fazer_login()


def tela_criar_conta():
    """Tela para criar nova conta"""
    global usuario_logado
    
    print("\n" + "="*50)
    print("CRIAR CONTA")
    print("="*50)
    nome = input("Nome: ")
    
    # Verificar se nome ja existe
    for user in usuarios:
        if user.nome == nome:
            print("[ERRO] Nome de usuario ja existe!")
            return tela_criar_conta()
    
    senha = input("Senha: ")
    senha_confirm = input("Confirmar senha: ")
    
    if senha != senha_confirm:
        print("[ERRO] As senhas nao coincidem!")
        return tela_criar_conta()
    
    # Criar usuario comum (nao administrador)
    novo_usuario = Usuario(nome, senha)
    usuarios.append(novo_usuario)
    salvar_usuarios()
    
    usuario_logado = novo_usuario
    print(f"\n[OK] Conta criada com sucesso! Bem-vindo(a), {nome}!")
    return True


# ============================================
# MENU PRINCIPAL
# ============================================

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def aguardar_enter():
    input("\nPressione Enter para continuar...")


def menu_principal():
    print("\n" + "="*50)
    print(f"SISTEMA DE CONTEUDOS GRATUITOS - Logado como: {usuario_logado.nome}")
    print("="*50)
    print("1 - Listar Todos os Conteudos")
    print("2 - Listar Eventos")
    print("3 - Listar Cursos")
    print("4 - Buscar por Titulo")
    print("5 - Favoritar Conteudo")
    print("6 - Remover Favorito")
    print("7 - Listar Favoritos")
    
    # Opcoes de administrador (so aparece se for admin)
    if isinstance(usuario_logado, Adm):
        print("-"*50)
        print("[OPCOES DE ADMIN]")
        print("8 - Criar Evento")
        print("9 - Criar Curso")
        print("10 - Atualizar Evento")
        print("11 - Atualizar Curso")
        print("12 - Deletar Conteudo")
        print("13 - Salvar Dados (manual)")
        print("14 - Carregar Dados (manual)")
    
    print("-"*50)
    print("0 - Sair / Logout")
    print("-"*50)
    return input("Escolha uma opcao: ")


def menu_favoritar():
    """Favoritar conteudo (qualquer usuario pode)"""
    global usuario_logado
    
    print("\n" + "="*50)
    print("FAVORITAR CONTEUDO")
    print("="*50)
    titulo = input("Titulo do conteudo: ")
    
    for item in conteudos:
        if item.titulo.lower() == titulo.lower():
            usuario_logado.adicionar_favorito(item)
            return
    
    print(f"[ERRO] Conteudo '{titulo}' nao encontrado.")


def menu_remover_favorito():
    """Remover favorito (qualquer usuario pode)"""
    global usuario_logado
    
    print("\n" + "="*50)
    print("REMOVER FAVORITO")
    print("="*50)
    titulo = input("Titulo do conteudo: ")
    
    for item in usuario_logado._favoritos:
        if item.titulo.lower() == titulo.lower():
            usuario_logado.remover_favorito(item)
            return
    
    print(f"[ERRO] '{titulo}' nao esta nos favoritos.")


def menu_listar_favoritos():
    """Listar favoritos (qualquer usuario pode)"""
    global usuario_logado
    usuario_logado.listar_favoritos()


def main():
    global usuario_logado, conteudos, usuarios
    
    # Carregar dados
    carregar_dados_automatico()
    carregar_usuarios()
    
    # Se nao tem admin, criar um padrao
    admin_existe = False
    for user in usuarios:
        if isinstance(user, Adm):
            admin_existe = True
            break
    
    if not admin_existe:
        # Criar admin padrao
        admin = Adm("admin", "1234")
        usuarios.append(admin)
        salvar_usuarios()
        print("[INFO] Administrador padrao criado: admin / 1234")
    
    # Se nao tem conteudos, criar exemplos
    if not conteudos:
        criar_dados_exemplo()
    
    # Tela de login
    if not fazer_login():
        print("\n[INFO] Saindo do sistema...")
        return
    
    # Loop principal
    while True:
        opcao = menu_principal()
        
        # ===== OPCAO 0 - SAIR (qualquer usuario) =====
        if opcao == "0":
            print("\n[INFO] Salvando dados antes de sair...")
            salvar_dados()
            salvar_usuarios()
            print("[INFO] Saindo do sistema...")
            break
        
        # ===== OPCOES COMUNS (todos usuarios) =====
        elif opcao == "1":
            listar_conteudos()
        
        elif opcao == "2":
            listar_eventos()
        
        elif opcao == "3":
            listar_cursos()
        
        elif opcao == "4":
            print("\n" + "="*50)
            print("BUSCAR POR TITULO")
            print("="*50)
            titulo = input("Digite o titulo (ou parte): ")
            buscar_por_titulo(titulo)
        
        elif opcao == "5":
            menu_favoritar()
        
        elif opcao == "6":
            menu_remover_favorito()
        
        elif opcao == "7":
            menu_listar_favoritos()
        
        # ===== OPCOES DE ADMINISTRADOR =====
        elif isinstance(usuario_logado, Adm):
            if opcao == "8":
                menu_criar_evento(usuario_logado)
            elif opcao == "9":
                menu_criar_curso(usuario_logado)
            elif opcao == "10":
                menu_atualizar_evento(usuario_logado)
            elif opcao == "11":
                menu_atualizar_curso(usuario_logado)
            elif opcao == "12":
                menu_deletar(usuario_logado)
            elif opcao == "13":
                salvar_dados()
            elif opcao == "14":
                carregar_dados()
            else:
                print("[ERRO] Opcao invalida!")
        
        else:
            print("[ERRO] Opcao invalida! (Apenas administradores podem acessar esta funcao)")
        
        aguardar_enter()


# ============================================
# MENUS DO ADMIN
# ============================================

def menu_criar_evento(adm):
    print("\n" + "="*50)
    print("CRIAR NOVO EVENTO")
    print("="*50)
    titulo = input("Titulo: ")
    descricao = input("Descricao: ")
    data = input("Data (DD/MM/AAAA): ")
    local = input("Local: ")
    adm.criar_evento(titulo, descricao, data, local)


def menu_criar_curso(adm):
    print("\n" + "="*50)
    print("CRIAR NOVO CURSO")
    print("="*50)
    titulo = input("Titulo: ")
    descricao = input("Descricao: ")
    link = input("Link: ")
    adm.criar_curso(titulo, descricao, link)


def menu_atualizar_evento(adm):
    print("\n" + "="*50)
    print("ATUALIZAR EVENTO")
    print("="*50)
    titulo = input("Titulo do evento a atualizar: ")
    print("\nDeixe em branco para nao alterar.")
    novo_titulo = input("Novo titulo: ") or None
    nova_descricao = input("Nova descricao: ") or None
    nova_data = input("Nova data: ") or None
    novo_local = input("Novo local: ") or None
    adm.atualizar_evento_por_titulo(titulo, novo_titulo, nova_descricao, nova_data, novo_local)


def menu_atualizar_curso(adm):
    print("\n" + "="*50)
    print("ATUALIZAR CURSO")
    print("="*50)
    titulo = input("Titulo do curso a atualizar: ")
    print("\nDeixe em branco para nao alterar.")
    novo_titulo = input("Novo titulo: ") or None
    nova_descricao = input("Nova descricao: ") or None
    novo_link = input("Novo link: ") or None
    adm.atualizar_curso_por_titulo(titulo, novo_titulo, nova_descricao, novo_link)


def menu_deletar(adm):
    print("\n" + "="*50)
    print("DELETAR CONTEUDO")
    print("="*50)
    titulo = input("Titulo do conteudo a deletar: ")
    confirm = input(f"Tem certeza que deseja deletar '{titulo}'? (s/n): ")
    if confirm.lower() == 's':
        adm.deletar_por_titulo(titulo)
    else:
        print("[INFO] Operacao cancelada.")


# ============================================
# EXECUCAO
# ============================================

if __name__ == "__main__":
    main()