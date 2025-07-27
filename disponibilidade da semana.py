import pandas as pd
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from datetime import datetime, date
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import locale

# Configurar locale para português
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        pass

class DisponibilidadeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disponibilidade de Motoboys")
        self.root.geometry("800x600")
        
        # Variáveis
        self.datas_selecionadas = []
        self.cadastro_df = None
        self.agendamento_df = None
        
        # Carregar dados
        self.carregar_dados()
        
        # Criar interface
        self.criar_interface()
        
    def carregar_dados(self):
        """Carrega os dados das planilhas"""
        try:
            # Caminhos dos arquivos
            cadastro_path = 'Entregadores.xlsx'
            agendamento_path = 'Pedidos.xls'
            
            # Ler as planilhas
            self.cadastro_df = pd.read_excel(cadastro_path)
            self.agendamento_df = pd.read_excel(agendamento_path, header=3)
            
            # Padronizar nomes das colunas
            self.cadastro_df.columns = self.cadastro_df.columns.str.strip().str.lower()
            self.agendamento_df.columns = self.agendamento_df.columns.str.strip().str.lower()
            
            # Padronizar os nomes dos entregadores
            self.cadastro_df['nome'] = self.cadastro_df['nome'].str.strip().str.lower()
            
            # Identificar a coluna do entregador
            entregador_col = None
            for col in self.agendamento_df.columns:
                if isinstance(col, str) and len(col) > 10 and ' ' in col and not col.startswith('unnamed'):
                    entregador_col = col
                    break
            
            if not entregador_col:
                raise Exception("Coluna do entregador não encontrada em Pedidos.xls")
            
            self.agendamento_df['entregador'] = self.agendamento_df[entregador_col].str.strip().str.lower()
            
            # Corrigir Telefone para texto
            if 'telefone' in self.cadastro_df.columns:
                self.cadastro_df['telefone'] = self.cadastro_df['telefone'].astype(str).str.replace('.0', '', regex=False)
            
            # Identificar a coluna de data
            data_col = None
            for col in self.agendamento_df.columns:
                if isinstance(col, str) and '/' in col and ':' in col and len(col) > 15:
                    data_col = col
                    break
            
            if not data_col:
                raise Exception("Coluna de data não encontrada em Pedidos.xls")
            
            self.data_col = data_col
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {str(e)}")
            self.root.destroy()
    
    def criar_interface(self):
        """Cria a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Seleção de Datas para Análise", font=('Arial', 14, 'bold'))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Frame do calendário
        cal_frame = ttk.LabelFrame(main_frame, text="Calendário (Duplo clique para adicionar)", padding="10")
        cal_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Calendário
        self.cal = Calendar(cal_frame, selectmode='day', date_pattern='dd/mm/yyyy')
        self.cal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        # Adicionar evento de duplo clique para adicionar data automaticamente
        self.cal.bind('<Double-Button-1>', lambda e: self.adicionar_data())
        
        # Frame das datas selecionadas
        datas_frame = ttk.LabelFrame(main_frame, text="Datas Selecionadas", padding="10")
        datas_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        datas_frame.columnconfigure(0, weight=1)
        
        # Lista das datas selecionadas
        self.lista_datas = tk.Listbox(datas_frame, height=10)
        self.lista_datas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Scrollbar para a lista
        scrollbar = ttk.Scrollbar(datas_frame, orient="vertical", command=self.lista_datas.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.lista_datas.configure(yscrollcommand=scrollbar.set)
        
        # Botões
        btn_frame = ttk.Frame(datas_frame)
        btn_frame.grid(row=1, column=0, columnspan=2, pady=(0, 10))
        
        ttk.Button(btn_frame, text="Adicionar Data", command=self.adicionar_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Remover Data", command=self.remover_data).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="Limpar Todas", command=self.limpar_datas).pack(side=tk.LEFT)
        
        # Frame dos botões principais
        acao_frame = ttk.Frame(main_frame)
        acao_frame.grid(row=2, column=0, columnspan=3, pady=(20, 0))
        
        ttk.Button(acao_frame, text="Gerar Relatório", command=self.gerar_relatorio, style='Accent.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(acao_frame, text="Sair", command=self.root.destroy).pack(side=tk.LEFT)
        
        # Configurar grid weights
        main_frame.rowconfigure(1, weight=1)
        cal_frame.rowconfigure(0, weight=1)
        cal_frame.columnconfigure(0, weight=1)
        datas_frame.rowconfigure(0, weight=1)
    
    def adicionar_data(self):
        """Adiciona a data selecionada no calendário à lista"""
        data_selecionada = self.cal.get_date()
        if data_selecionada not in self.datas_selecionadas:
            self.datas_selecionadas.append(data_selecionada)
            self.datas_selecionadas.sort()
            self.atualizar_lista_datas()
            # Limpar seleção do calendário para próxima seleção
            self.cal.selection_clear()
    
    def remover_data(self):
        """Remove a data selecionada da lista"""
        selection = self.lista_datas.curselection()
        if selection:
            index = selection[0]
            data_removida = self.datas_selecionadas.pop(index)
            self.atualizar_lista_datas()
    
    def limpar_datas(self):
        """Limpa todas as datas selecionadas"""
        self.datas_selecionadas.clear()
        self.atualizar_lista_datas()
    
    def atualizar_lista_datas(self):
        """Atualiza a lista de datas selecionadas"""
        self.lista_datas.delete(0, tk.END)
        for data in self.datas_selecionadas:
            self.lista_datas.insert(tk.END, data)
    
    def gerar_relatorio(self):
        """Gera o relatório Excel e PDF"""
        if not self.datas_selecionadas:
            messagebox.showwarning("Aviso", "Selecione pelo menos uma data!")
            return
        
        try:
            # Processar dados para as datas selecionadas
            nao_agendados_por_data = {}
            
            for data_str in self.datas_selecionadas:
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
                    colunas_desejadas = [col for col in ['nome', 'telefone', 'cidade', 'bairro', 'cep'] if col in self.cadastro_df.columns]
                    resultado = motoboys_nao_agendados[colunas_desejadas].copy()
                    nao_agendados_por_data[data_str] = resultado
            
            if not nao_agendados_por_data:
                messagebox.showinfo("Informação", "Não há motoboys disponíveis nas datas selecionadas!")
                return
            
            # Gerar Excel
            output_excel = os.path.join(os.getcwd(), 'Motoboys_Nao_Escalados.xlsx')
            with pd.ExcelWriter(output_excel) as writer:
                for data, df_ in nao_agendados_por_data.items():
                    aba_nome = data.replace('/', '_')
                    df_.to_excel(writer, sheet_name=aba_nome, index=False)
            
            # Gerar PDF
            output_pdf = os.path.join(os.getcwd(), 'Motoboys_Nao_Escalados.pdf')
            self.gerar_pdf(nao_agendados_por_data, output_pdf)
            
            messagebox.showinfo("Sucesso", 
                              f"Relatórios gerados com sucesso!\n\n"
                              f"Excel: {output_excel}\n"
                              f"PDF: {output_pdf}")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar relatório: {str(e)}")
    
    def gerar_pdf(self, dados_por_data, output_path):
        """Gera o relatório em PDF"""
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

def main():
    # Verificar se as bibliotecas necessárias estão instaladas
    try:
        import tkcalendar
        import reportlab
    except ImportError as e:
        print(f"Erro: Biblioteca não encontrada: {e}")
        print("Instale as bibliotecas necessárias:")
        print("pip install tkcalendar reportlab")
        return
    
    # Criar aplicação
    root = tk.Tk()
    app = DisponibilidadeApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
