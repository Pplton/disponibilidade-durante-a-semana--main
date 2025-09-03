#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialização do Sistema de Disponibilidade de Motoboys
================================================================

Este script facilita a inicialização do sistema, verificando dependências
e criando arquivos necessários automaticamente.
"""

import sys
import os
import subprocess
import importlib.util

def verificar_python():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 ou superior é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def verificar_dependencias():
    """Verifica e instala dependências se necessário"""
    dependencias = [
        'pandas',
        'tkcalendar', 
        'reportlab',
        'openpyxl'
    ]
    
    print("\n📦 Verificando dependências...")
    
    faltando = []
    for dep in dependencias:
        if importlib.util.find_spec(dep) is None:
            faltando.append(dep)
            print(f"❌ {dep} não encontrado")
        else:
            print(f"✅ {dep} encontrado")
    
    if faltando:
        print(f"\n🔧 Instalando dependências faltantes: {', '.join(faltando)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + faltando)
            print("✅ Dependências instaladas com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao instalar dependências: {e}")
            print("\n💡 Tente instalar manualmente:")
            print(f"   pip install {' '.join(faltando)}")
            return False
    
    return True

def criar_arquivos_necessarios():
    """Cria arquivos necessários se não existirem"""
    print("\n📁 Verificando arquivos necessários...")
    
    # Verificar se config.json existe
    if not os.path.exists('config.json'):
        print("⚠️  Arquivo config.json não encontrado")
        print("   Será criado automaticamente na primeira execução")
    
    # Verificar se exemplos existem
    if not os.path.exists('exemplos'):
        print("📋 Criando arquivos de exemplo...")
        try:
            import criar_exemplos
            criar_exemplos.main()
        except Exception as e:
            print(f"⚠️  Erro ao criar exemplos: {e}")
    
    print("✅ Verificação de arquivos concluída")

def mostrar_ajuda():
    """Mostra informações de ajuda"""
    print("\n" + "="*60)
    print("🚚 SISTEMA DE DISPONIBILIDADE DE MOTOBOYS")
    print("="*60)
    print("\n📖 COMO USAR:")
    print("1. Prepare suas planilhas:")
    print("   - Entregadores.xlsx (cadastro dos motoboys)")
    print("   - Pedidos.xls (agendamentos)")
    print("\n2. Execute o sistema:")
    print("   python disponibilidade_motoboys.py")
    print("\n3. Na interface:")
    print("   - Selecione os arquivos de dados")
    print("   - Escolha as datas no calendário")
    print("   - Clique em 'Gerar Relatórios'")
    print("\n📁 ARQUIVOS DE EXEMPLO:")
    print("   - exemplos/Entregadores_Exemplo.xlsx")
    print("   - exemplos/Pedidos_Exemplo.xlsx")
    print("\n🔧 CONFIGURAÇÃO:")
    print("   - Edite config.json para personalizar")
    print("   - Consulte README.md para mais detalhes")
    print("\n" + "="*60)

def main():
    """Função principal"""
    print("🚀 Iniciando Sistema de Disponibilidade de Motoboys...")
    
    # Verificar Python
    if not verificar_python():
        input("\nPressione Enter para sair...")
        return
    
    # Verificar dependências
    if not verificar_dependencias():
        input("\nPressione Enter para sair...")
        return
    
    # Criar arquivos necessários
    criar_arquivos_necessarios()
    
    # Mostrar ajuda
    mostrar_ajuda()
    
    # Perguntar se quer executar
    print("\n❓ Deseja executar o sistema agora? (s/n): ", end="")
    resposta = input().lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        print("\n🚀 Iniciando sistema...")
        try:
            import disponibilidade_motoboys
            disponibilidade_motoboys.main()
        except Exception as e:
            print(f"❌ Erro ao iniciar sistema: {e}")
            input("\nPressione Enter para sair...")
    else:
        print("\n👋 Sistema pronto para uso!")
        print("   Execute: python disponibilidade_motoboys.py")

if __name__ == "__main__":
    main()
