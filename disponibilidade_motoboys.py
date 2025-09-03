#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Análise de Disponibilidade de Motoboys
=================================================

Sistema automatizado para análise de disponibilidade de motoboys durante a semana.
Permite selecionar datas específicas e gera relatórios em Excel e PDF com os 
motoboys disponíveis (não agendados) para cada data selecionada.

Autor: Sistema de Gestão de Motoboys
Versão: 2.0
Data: 2024
"""

import pandas as pd
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import Calendar
from datetime import datetime, date
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import locale
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('disponibilidade_motoboys.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConfigManager:
    """Gerenciador de configurações do sistema"""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self) -> dict:
        """Carrega configurações do arquivo JSON"""
        default_config = {
            "arquivos": {
                "cadastro": "Entregadores.xlsx",
                "agendamento": "Pedidos.xls"
            },
            "planilha": {
                "header_agendamento": 3,
                "colunas_cadastro": ["nome", "telefone", "cidade", "bairro", "cep"],
                "coluna_entregador": "entregador",
                "coluna_data": "data_agendamento"
            },
            "relatorio": {
                "formato_data": "%d/%m/%Y",
                "nome_excel": "Motoboys_Nao_Escalados.xlsx",
                "nome_pdf": "Motoboys_Nao_Escalados.pdf"
            },
            "interface": {
                "titulo": "Sistema de Disponibilidade de Motoboys",
                "largura": 900,
                "altura": 700
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # Mesclar com configurações padrão
                return self._merge_config(default_config, config)
            except Exception as e:
                logger.warning(f"Erro ao carregar configurações: {e}. Usando configurações padrão.")
        
        return default_config
    
    def _merge_config(self, default: dict, user: dict) -> dict:
        """Mescla configurações do usuário com as padrão"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_config(result[key], value)
            else:
                result[key] = value
        return result
    
    def save_config(self):
        """Salva configurações no arquivo JSON"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Erro ao salvar configurações: {e}")
    
    def get(self, key_path: str, default=None):
        """Obtém valor de configuração usando notação de ponto"""
        keys = key_path.split('.')
        value = self.config
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        return value

class DataProcessor:
    """Processador de dados das planilhas"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        self.cadastro_df = None
        self.agendamento_df = None
        self.data_col = None
        self.entregador_col = None
    
    def carregar_dados(self, cadastro_path: str = None, agendamento_path: str = None) -> bool:
        """Carrega os dados das planilhas"""
        try:
            # Usar caminhos fornecidos ou da configuração
            if not cadastro_path:
                cadastro_path = self.config.get('arquivos.cadastro')
            if not agendamento_path:
                agendamento_path = self.config.get('arquivos.agendamento')
            
            # Verificar se arquivos existem
            if not os.path.exists(cadastro_path):
                raise FileNotFoundError(f"Arquivo de cadastro não encontrado: {cadastro_path}")
            if not os.path.exists(agendamento_path):
                raise FileNotFoundError(f"Arquivo de agendamento não encontrado: {agendamento_path}")
            
            # Ler as planilhas
            logger.info(f"Carregando arquivo de cadastro: {cadastro_path}")
            self.cadastro_df = pd.read_excel(cadastro_path)
            
            header_row = self.config.get('planilha.header_agendamento', 3)
            logger.info(f"Carregando arquivo de agendamento: {agendamento_path} (header: {header_row})")
            self.agendamento_df = pd.read_excel(agendamento_path, header=header_row)
            
            # Processar dados
            self._processar_cadastro()
            self._processar_agendamento()
            
            logger.info("Dados carregados com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao carregar dados: {e}")
            raise
    
    def _processar_cadastro(self):
        """Processa dados de cadastro"""
        # Padronizar nomes das colunas
        self.cadastro_df.columns = self.cadastro_df.columns.str.strip().str.lower()
        
        # Verificar se coluna 'nome' existe
        if 'nome' not in self.cadastro_df.columns:
            raise ValueError("Coluna 'nome' não encontrada na planilha de cadastro")
        
        # Padronizar os nomes dos entregadores
        self.cadastro_df['nome'] = self.cadastro_df['nome'].str.strip().str.lower()
        
        # Corrigir Telefone para texto
        if 'telefone' in self.cadastro_df.columns:
            self.cadastro_df['telefone'] = self.cadastro_df['telefone'].astype(str).str.replace('.0', '', regex=False)
        
        logger.info(f"Processados {len(self.cadastro_df)} registros de cadastro")
    
    def _processar_agendamento(self):
        """Processa dados de agendamento"""
        # Padronizar nomes das colunas
        self.agendamento_df.columns = self.agendamento_df.columns.str.strip().str.lower()
        
        # Identificar a coluna do entregador
        self.entregador_col = self._encontrar_coluna_entregador()
        if not self.entregador_col:
            raise ValueError("Coluna do entregador não encontrada na planilha de agendamento")
        
        self.agendamento_df['entregador'] = self.agendamento_df[self.entregador_col].str.strip().str.lower()
        
        # Identificar a coluna de data
        self.data_col = self._encontrar_coluna_data()
        if not self.data_col:
            raise ValueError("Coluna de data não encontrada na planilha de agendamento")
        
        logger.info(f"Processados {len(self.agendamento_df)} registros de agendamento")
    
    def _encontrar_coluna_entregador(self) -> Optional[str]:
        """Encontra a coluna do entregador automaticamente"""
        # Tentar encontrar por nome exato primeiro
        coluna_config = self.config.get('planilha.coluna_entregador')
        if coluna_config and coluna_config in self.agendamento_df.columns:
            return coluna_config
        
        # Buscar automaticamente
        for col in self.agendamento_df.columns:
            if isinstance(col, str):
                col_lower = col.lower()
                if any(palavra in col_lower for palavra in ['entregador', 'motoboy', 'delivery', 'nome']):
                    return col
        
        # Buscar por padrão (nome longo com espaços)
        for col in self.agendamento_df.columns:
            if isinstance(col, str) and len(col) > 10 and ' ' in col and not col.startswith('unnamed'):
                return col
        
        return None
    
    def _encontrar_coluna_data(self) -> Optional[str]:
        """Encontra a coluna de data automaticamente"""
        # Tentar encontrar por nome exato primeiro
        coluna_config = self.config.get('planilha.coluna_data')
        if coluna_config and coluna_config in self.agendamento_df.columns:
            return coluna_config
        
        # Buscar automaticamente
        for col in self.agendamento_df.columns:
            if isinstance(col, str):
                col_lower = col.lower()
                if any(palavra in col_lower for palavra in ['data', 'date', 'agendamento', 'agenda']):
                    return col
        
        # Buscar por padrão (contém / e :)
        for col in self.agendamento_df.columns:
            if isinstance(col, str) and '/' in col and ':' in col and len(col) > 15:
                return col
        
        return None
    
    def obter_motoboys_disponiveis(self, datas: List[str]) -> Dict[str, pd.DataFrame]:
        """Obtém motoboys disponíveis para as datas especificadas"""
        nao_agendados_por_data = {}
        
        for data_str in datas:
            try:
                # Converter string para date
                data_obj = datetime.strptime(data_str, '%d/%m/%Y').date()
                
                # Filtrar agendados na data
                agendados_no_dia = self.agendamento_df[
                    pd.to_datetime(self.agendamento_df[self.data_col], dayfirst=True, errors='coerce').dt.date == data_obj
                ]['entregador']
                
                # Motoboys não agendados
                motoboys_nao_agendados = self.cadastro_df[~self.cadastro_df['nome'].isin(agendados_no_dia)]
                
                if not motoboys_nao_agendados.empty:
                    # Selecionar colunas desejadas
                    colunas_desejadas = [
                        col for col in self.config.get('planilha.colunas_cadastro', [])
                        if col in self.cadastro_df.columns
                    ]
                    resultado = motoboys_nao_agendados[colunas_desejadas].copy()
                    nao_agendados_por_data[data_str] = resultado
                    
            except Exception as e:
                logger.error(f"Erro ao processar data {data_str}: {e}")
                continue
        
        return nao_agendados_por_data

class RelatorioGenerator:
    """Gerador de relatórios Excel e PDF"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
    
    def gerar_excel(self, dados_por_data: Dict[str, pd.DataFrame], output_path: str = None) -> str:
        """Gera relatório Excel"""
        if not output_path:
            output_path = self.config.get('relatorio.nome_excel', 'Motoboys_Nao_Escalados.xlsx')
        
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for data, df in dados_por_data.items():
                    if not df.empty:
                        # Nome da aba com data
                        aba_nome = data.replace('/', '_')
                        df.to_excel(writer, sheet_name=aba_nome, index=False)
            
            logger.info(f"Relatório Excel gerado: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar Excel: {e}")
            raise
    
    def gerar_pdf(self, dados_por_data: Dict[str, pd.DataFrame], output_path: str = None) -> str:
        """Gera relatório PDF"""
        if not output_path:
            output_path = self.config.get('relatorio.nome_pdf', 'Motoboys_Nao_Escalados.pdf')
        
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # Estilos
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Centralizado
            )
            
            date_style = ParagraphStyle(
                'DateStyle',
                parent=styles['Heading2'],
                fontSize=14,
                spaceAfter=20,
                textColor=colors.darkblue
            )
            
            # Título principal
            title = Paragraph("Relatório de Motoboys Disponíveis", title_style)
            story.append(title)
            story.append(Spacer(1, 20))
            
            # Para cada data
            for data_str in sorted(dados_por_data.keys()):
                df = dados_por_data[data_str]
                
                if df.empty:
                    continue
                
                # Título da data
                data_title = Paragraph(f"Data: {data_str}", date_style)
                story.append(data_title)
                
                # Preparar dados para tabela
                headers = [col.title() for col in df.columns]
                data = [headers] + df.values.tolist()
                
                # Criar tabela
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ]))
                
                story.append(table)
                story.append(Spacer(1, 30))
            
            # Gerar PDF
            doc.build(story)
            logger.info(f"Relatório PDF gerado: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Erro ao gerar PDF: {e}")
            raise

class DisponibilidadeApp:
    """Aplicação principal com interface gráfica"""
    
    def __init__(self, root):
        self.root = root
        self.config = ConfigManager()
        self.data_processor = DataProcessor(self.config)
        self.relatorio_generator = RelatorioGenerator(self.config)
        
        # Configurar janela
        self._configurar_janela()
        
        # Variáveis
        self.datas_selecionadas = []
        self.cadastro_path = None
        self.agendamento_path = None
        
        # Criar interface
        self._criar_interface()
        
        # Tentar carregar dados automaticamente
        self._tentar_carregar_dados_automatico()
    
    def _configurar_janela(self):
        """Configura a janela principal"""
        titulo = self.config.get('interface.titulo', 'Sistema de Disponibilidade de Motoboys')
        largura = self.config.get('interface.largura', 900)
        altura = self.config.get('interface.altura', 700)
        
        self.root.title(titulo)
        self.root.geometry(f"{largura}x{altura}")
        self.root.minsize(800, 600)
        
        # Configurar ícone (se existir)
        try:
            if os.path.exists('icon.ico'):
                self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def _criar_interface(self):
        """Cria a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Sistema de Disponibilidade de Motoboys", 
                          font=('Arial', 16, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame de arquivos
        arquivos_frame = ttk.LabelFrame(main_frame, text="Arquivos de Dados", padding="10")
        arquivos_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        arquivos_frame.columnconfigure(1, weight=1)
        
        # Cadastro
        ttk.Label(arquivos_frame, text="Cadastro:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.cadastro_label = ttk.Label(arquivos_frame, text="Não selecionado", foreground="red")
        self.cadastro_label.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 5))
        ttk.Button(arquivos_frame, text="Selecionar", 
                  command=self._selecionar_cadastro).grid(row=0, column=2)
        
        # Agendamento
        ttk.Label(arquivos_frame, text="Agendamento:").grid(row=1, column=0, sticky=tk.W, padx=(0, 5), pady=(5, 0))
        self.agendamento_label = ttk.Label(arquivos_frame, text="Não selecionado", foreground="red")
        self.agendamento_label.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 5), pady=(5, 0))
        ttk.Button(arquivos_frame, text="Selecionar", 
                  command=self._selecionar_agendamento).grid(row=1, column=2, pady=(5, 0))
        
        # Frame do calendário
        cal_frame = ttk.LabelFrame(main_frame, text="Calendário (Duplo clique para adicionar)", padding="10")
        cal_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Calendário
        self.cal = Calendar(cal_frame, selectmode='day', date_pattern='dd/mm/yyyy')
        self.cal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.cal.bind('<Double-Button-1>', lambda e: self._adicionar_data())
        
        # Frame das datas selecionadas
        datas_frame = ttk.LabelFrame(main_frame, text="Datas Selecionadas", padding="10")
        datas_frame.grid(row=2, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        datas_frame.columnconfigure(0, weight=1)
        
        # Lista das datas selecionadas
        self.lista_datas = tk.Listbox(datas_frame, height=10)
        self.lista_datas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(datas_frame, orient="vertical", command=self.lista_datas.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.lista_datas.configure(yscrollcommand=scrollbar.set)
        
        # Botões de gerenciamento de datas
        btn_frame = ttk.Frame(datas_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Adicionar Data", 
                  command=self._adicionar_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Remover Data", 
                  command=self._remover_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Limpar Todas", 
                  command=self._limpar_datas).pack(side=tk.LEFT)
        
        # Frame dos botões principais
        acao_frame = ttk.Frame(main_frame)
        acao_frame.grid(row=3, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(acao_frame, text="Gerar Relatórios", 
                  command=self._gerar_relatorios, 
                  style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(acao_frame, text="Configurações", 
                  command=self._abrir_configuracoes).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(acao_frame, text="Sair", 
                  command=self.root.destroy).pack(side=tk.LEFT)
        
        # Configurar grid weights
        main_frame.rowconfigure(2, weight=1)
        cal_frame.rowconfigure(0, weight=1)
        cal_frame.columnconfigure(0, weight=1)
        datas_frame.rowconfigure(0, weight=1)
    
    def _tentar_carregar_dados_automatico(self):
        """Tenta carregar dados automaticamente se os arquivos existirem"""
        cadastro_path = self.config.get('arquivos.cadastro')
        agendamento_path = self.config.get('arquivos.agendamento')
        
        if os.path.exists(cadastro_path) and os.path.exists(agendamento_path):
            try:
                self.cadastro_path = cadastro_path
                self.agendamento_path = agendamento_path
                self._atualizar_labels_arquivos()
                self.data_processor.carregar_dados(cadastro_path, agendamento_path)
                messagebox.showinfo("Sucesso", "Dados carregados automaticamente!")
            except Exception as e:
                messagebox.showwarning("Aviso", f"Erro ao carregar dados automaticamente: {e}")
    
    def _selecionar_cadastro(self):
        """Seleciona arquivo de cadastro"""
        arquivo = filedialog.askopenfilename(
            title="Selecione a planilha de CADASTRO dos motoboys",
            filetypes=[('Arquivos Excel', '*.xlsx *.xls'), ('Todos os arquivos', '*.*')]
        )
        if arquivo:
            self.cadastro_path = arquivo
            self._atualizar_labels_arquivos()
    
    def _selecionar_agendamento(self):
        """Seleciona arquivo de agendamento"""
        arquivo = filedialog.askopenfilename(
            title="Selecione a planilha de AGENDAMENTO dos motoboys",
            filetypes=[('Arquivos Excel', '*.xlsx *.xls'), ('Todos os arquivos', '*.*')]
        )
        if arquivo:
            self.agendamento_path = arquivo
            self._atualizar_labels_arquivos()
    
    def _atualizar_labels_arquivos(self):
        """Atualiza os labels dos arquivos selecionados"""
        if self.cadastro_path:
            nome = os.path.basename(self.cadastro_path)
            self.cadastro_label.config(text=nome, foreground="green")
        else:
            self.cadastro_label.config(text="Não selecionado", foreground="red")
        
        if self.agendamento_path:
            nome = os.path.basename(self.agendamento_path)
            self.agendamento_label.config(text=nome, foreground="green")
        else:
            self.agendamento_label.config(text="Não selecionado", foreground="red")
    
    def _adicionar_data(self):
        """Adiciona a data selecionada no calendário à lista"""
        data_selecionada = self.cal.get_date()
        if data_selecionada not in self.datas_selecionadas:
            self.datas_selecionadas.append(data_selecionada)
            self.datas_selecionadas.sort()
            self._atualizar_lista_datas()
            self.cal.selection_clear()
    
    def _remover_data(self):
        """Remove a data selecionada da lista"""
        selection = self.lista_datas.curselection()
        if selection:
            index = selection[0]
            self.datas_selecionadas.pop(index)
            self._atualizar_lista_datas()
    
    def _limpar_datas(self):
        """Limpa todas as datas selecionadas"""
        self.datas_selecionadas.clear()
        self._atualizar_lista_datas()
    
    def _atualizar_lista_datas(self):
        """Atualiza a lista de datas selecionadas"""
        self.lista_datas.delete(0, tk.END)
        for data in self.datas_selecionadas:
            self.lista_datas.insert(tk.END, data)
    
    def _gerar_relatorios(self):
        """Gera os relatórios Excel e PDF"""
        # Verificar se arquivos foram selecionados
        if not self.cadastro_path or not self.agendamento_path:
            messagebox.showerror("Erro", "Selecione os arquivos de cadastro e agendamento!")
            return
        
        if not self.datas_selecionadas:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma data!")
            return
        
        try:
            # Carregar dados
            self.data_processor.carregar_dados(self.cadastro_path, self.agendamento_path)
            
            # Processar dados para as datas selecionadas
            nao_agendados_por_data = self.data_processor.obter_motoboys_disponiveis(self.datas_selecionadas)
            
            if not nao_agendados_por_data:
                messagebox.showinfo("Informação", "Não há motoboys disponíveis nas datas selecionadas!")
                return
            
            # Gerar relatórios
            excel_path = self.relatorio_generator.gerar_excel(nao_agendados_por_data)
            pdf_path = self.relatorio_generator.gerar_pdf(nao_agendados_por_data)
            
            messagebox.showinfo("Sucesso", 
                              f"Relatórios gerados com sucesso!\n\n"
                              f"Excel: {os.path.basename(excel_path)}\n"
                              f"PDF: {os.path.basename(pdf_path)}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatórios: {str(e)}")
            logger.error(f"Erro ao gerar relatórios: {e}")
    
    def _abrir_configuracoes(self):
        """Abre janela de configurações"""
        # Implementar janela de configurações se necessário
        messagebox.showinfo("Configurações", "Funcionalidade de configurações em desenvolvimento.")

def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    dependencias = [
        ('pandas', 'pandas'),
        ('tkcalendar', 'tkcalendar'),
        ('reportlab', 'reportlab'),
        ('openpyxl', 'openpyxl')
    ]
    
    faltando = []
    for nome, modulo in dependencias:
        try:
            __import__(modulo)
        except ImportError:
            faltando.append(nome)
    
    if faltando:
        print("❌ Dependências não encontradas:")
        for dep in faltando:
            print(f"   - {dep}")
        print("\n📦 Instale as dependências com:")
        print("pip install " + " ".join(faltando))
        return False
    
    return True

def main():
    """Função principal"""
    print("🚚 Sistema de Disponibilidade de Motoboys v2.0")
    print("=" * 50)
    
    # Verificar dependências
    if not verificar_dependencias():
        input("\nPressione Enter para sair...")
        return
    
    # Configurar locale para português
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        except:
            pass
    
    try:
        # Criar aplicação
        root = tk.Tk()
        app = DisponibilidadeApp(root)
        
        # Centralizar janela
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
        y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
        root.geometry(f"+{x}+{y}")
        
        # Iniciar aplicação
        root.mainloop()
        
    except Exception as e:
        logger.error(f"Erro na aplicação principal: {e}")
        messagebox.showerror("Erro Fatal", f"Erro na aplicação: {str(e)}")
    finally:
        logger.info("Aplicação finalizada")

if __name__ == "__main__":
    main()
