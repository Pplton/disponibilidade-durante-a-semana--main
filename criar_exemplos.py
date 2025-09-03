#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar arquivos de exemplo
"""

import pandas as pd
import os
from datetime import datetime, timedelta

def criar_exemplo_entregadores():
    """Cria arquivo de exemplo de entregadores"""
    dados = {
        'Nome': [
            'João Silva',
            'Maria Santos', 
            'Pedro Oliveira',
            'Ana Costa',
            'Carlos Ferreira',
            'Lucia Rodrigues',
            'Roberto Alves',
            'Fernanda Lima',
            'Marcos Pereira',
            'Patricia Souza'
        ],
        'Telefone': [
            '11999999999',
            '11888888888',
            '11777777777',
            '11666666666',
            '11555555555',
            '11444444444',
            '11333333333',
            '11222222222',
            '11111111111',
            '11000000000'
        ],
        'Cidade': [
            'São Paulo', 'São Paulo', 'São Paulo', 'São Paulo', 'São Paulo',
            'São Paulo', 'São Paulo', 'São Paulo', 'São Paulo', 'São Paulo'
        ],
        'Bairro': [
            'Centro', 'Vila Madalena', 'Moema', 'Itaim Bibi', 'Pinheiros',
            'Consolação', 'Liberdade', 'Perdizes', 'Santana', 'Tatuapé'
        ],
        'CEP': [
            '01234-567', '05433-000', '04038-001', '04530-001', '05422-000',
            '01302-000', '01508-000', '01234-000', '02012-000', '03087-000'
        ]
    }
    
    df = pd.DataFrame(dados)
    
    # Criar diretório se não existir
    os.makedirs('exemplos', exist_ok=True)
    
    # Salvar arquivo
    df.to_excel('exemplos/Entregadores_Exemplo.xlsx', index=False)
    print("✅ Arquivo de exemplo de entregadores criado: exemplos/Entregadores_Exemplo.xlsx")

def criar_exemplo_pedidos():
    """Cria arquivo de exemplo de pedidos"""
    # Datas de exemplo (próximos 3 dias)
    hoje = datetime.now().date()
    datas = [hoje + timedelta(days=i) for i in range(3)]
    
    dados = []
    entregadores = [
        'joão silva', 'maria santos', 'pedro oliveira', 'ana costa', 'carlos ferreira',
        'lucia rodrigues', 'roberto alves', 'fernanda lima', 'marcos pereira', 'patricia souza'
    ]
    
    clientes = [f'Cliente {chr(65+i)}' for i in range(10)]
    enderecos = [f'Rua {chr(65+i)} {100+i}' for i in range(10)]
    valores = [25.50, 30.00, 15.75, 45.00, 20.25, 35.50, 28.00, 22.75, 40.00, 18.90]
    
    # Criar alguns agendamentos para cada data
    for i, data in enumerate(datas):
        # Agendar alguns entregadores para cada data
        for j in range(3):  # 3 entregadores por dia
            entregador_idx = (i * 3 + j) % len(entregadores)
            cliente_idx = (i * 3 + j) % len(clientes)
            
            hora = 8 + j * 2  # 8h, 10h, 12h
            data_hora = f"{data.strftime('%d/%m/%Y')} {hora:02d}:00"
            
            dados.append({
                'Data de Agendamento': data_hora,
                'Entregador': entregadores[entregador_idx],
                'Cliente': clientes[cliente_idx],
                'Endereço': enderecos[cliente_idx],
                'Valor': valores[cliente_idx]
            })
    
    df = pd.DataFrame(dados)
    
    # Salvar arquivo
    df.to_excel('exemplos/Pedidos_Exemplo.xlsx', index=False)
    print("✅ Arquivo de exemplo de pedidos criado: exemplos/Pedidos_Exemplo.xlsx")

def main():
    """Função principal"""
    print("📋 Criando arquivos de exemplo...")
    print("=" * 40)
    
    try:
        criar_exemplo_entregadores()
        criar_exemplo_pedidos()
        print("\n🎉 Todos os arquivos de exemplo foram criados com sucesso!")
        print("\n📁 Arquivos criados:")
        print("   - exemplos/Entregadores_Exemplo.xlsx")
        print("   - exemplos/Pedidos_Exemplo.xlsx")
        print("\n💡 Use estes arquivos como referência para o formato das suas planilhas.")
        
    except Exception as e:
        print(f"❌ Erro ao criar arquivos de exemplo: {e}")

if __name__ == "__main__":
    main()
