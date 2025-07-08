import streamlit as st
import pandas as pd
from io import BytesIO

# --- Função de Inicialização do Session State ---
def initialize_session_state():
    """
    Inicializa o st.session_state com valores padrão para limpar o formulário.
    """
    if "initialized" not in st.session_state:
        # Informações Pessoais/Empresariais
        st.session_state.nome_input = ""
        st.session_state.fantasia_input = ""
        st.session_state.insc_estadual_input = ""
        st.session_state.insc_municipal_input = ""
        st.session_state.email_input = ""
        st.session_state.telefone_input = ""
        st.session_state.celular_input = ""
        st.session_state.tipo_doc_radio = "CPF"
        st.session_state.cpf_input = ""
        st.session_state.cnpj_input = ""

        # Endereço do Cliente (Principal)
        st.session_state.cliente_cep_input = ""
        st.session_state.cliente_logradouro_input = ""
        st.session_state.cliente_numero_input = ""
        st.session_state.cliente_complemento_input = ""
        st.session_state.cliente_bairro_input = ""
        st.session_state.cliente_cidade_input = ""
        st.session_state.cliente_estado_input = ""

        # Controles para mostrar/ocultar seções
        st.session_state.show_endereco_entrega = False # Novo
        st.session_state.show_referencias = False # Novo

        # Endereço de Entrega
        st.session_state.entrega_cep_input = ""
        st.session_state.entrega_rua_input = ""
        st.session_state.entrega_numero_input = ""
        st.session_state.entrega_complemento_input = ""
        st.session_state.entrega_bairro_input = ""
        st.session_state.entrega_cidade_input = ""
        st.session_state.entrega_estado_input = ""

        # Documentos para Entrega
        st.session_state.doc_contrato_social = False
        st.session_state.doc_comprovante_endereco = False

        # Referências
        st.session_state.ref1_nome = ""
        st.session_state.ref1_contato = ""
        st.session_state.ref2_nome = ""
        st.session_state.ref2_contato = ""
        st.session_state.ref3_nome = ""
        st.session_state.ref3_contato = ""

        # Observações
        st.session_state.observacao_area = ""

        st.session_state.initialized = True

# --- Função para Limpar os Campos ---
def clear_form():
    """
    Reseta todos os valores no st.session_state para limpar os campos do formulário.
    """
    for key in st.session_state.keys():
        # Exclui as chaves de controle de visibilidade da limpeza para que elas permaneçam False
        if key in ["show_endereco_entrega", "show_referencias", "initialized"]:
            continue
        if (key.endswith('_input') or key.endswith('_area') or
            key.endswith('_nome') or key.endswith('_contato')):
            if key == "tipo_doc_radio":
                st.session_state[key] = "CPF"
            else:
                st.session_state[key] = ""
        elif key.startswith('doc_'):
            st.session_state[key] = False
    
    # Resetar os controles de visibilidade explicitamente para False ao limpar
    st.session_state.show_endereco_entrega = False
    st.session_state.show_referencias = False
    
    st.rerun()

# --- Aplicação Streamlit Principal ---
def app():
    # Inicializa o estado da sessão na primeira execução
    initialize_session_state()

    st.set_page_config(page_title="Ficha de Cadastro de Cliente", layout="centered")

    # --- Logo da Empresa ---
    try:
        st.image("Logo Veteagro.png", width=200) # Ajuste a largura conforme necessário
    except FileNotFoundError:
        st.warning("A logo 'Logo Veteagro.png' não foi encontrada. Certifique-se de que está no mesmo diretório do script.")
    except Exception as e:
        st.warning(f"Erro ao carregar a logo: {e}")

    st.title("📝 Ficha de Cadastro de Cliente")
    st.write("Preencha os dados do cliente para gerar e baixar a ficha em Excel. Use o botão 'Limpar Cadastro' para reiniciar o formulário.")

    # --- Seção: Informações Principais do Cliente ---
    st.header("Informações Pessoais/Empresariais")
    nome = st.text_input("Nome / Razão Social*", value=st.session_state.nome_input, help="Nome completo do cliente ou razão social da empresa.", key="nome_input")
    fantasia = st.text_input("Nome Fantasia (Opcional)", value=st.session_state.fantasia_input, help="Nome fantasia da empresa, se aplicável.", key="fantasia_input")
    insc_estadual = st.text_input("Inscrição Estadual (Opcional)", value=st.session_state.insc_estadual_input, max_chars=14, help="Número de inscrição estadual da empresa (somente números).", key="insc_estadual_input")
    insc_municipal = st.text_input("Inscrição Municipal (Opcional)", value=st.session_state.insc_municipal_input, max_chars=14, help="Número de inscrição municipal da empresa (somente números).", key="insc_municipal_input")
    email = st.text_input("Email (Opcional)", value=st.session_state.email_input, help="Email de contato do cliente.", key="email_input")
    telefone = st.text_input("Telefone*", value=st.session_state.telefone_input, max_chars=15, help="Número de telefone do cliente (somente números).", key="telefone_input")
    celular = st.text_input("Celular (Opcional)", value=st.session_state.celular_input, max_chars=15, help="Número de celular do cliente (somente números).", key="celular_input")

    tipo_documento = st.radio("Tipo de Documento*", ["CPF", "CNPJ"], horizontal=True, key="tipo_doc_radio")
    documento = ""
    if tipo_documento == "CPF":
        documento = st.text_input("CPF*", value=st.session_state.cpf_input, max_chars=14, help="Digite o CPF do cliente (somente números).", key="cpf_input")
    else:
        documento = st.text_input("CNPJ*", value=st.session_state.cnpj_input, max_chars=18, help="Digite o CNPJ da empresa (somente números).", key="cnpj_input")

    # --- Endereço do Cliente ---
    st.markdown("---")
    st.header("Endereço do Cliente (Sede/Principal)")
    st.write("Preencha os dados do endereço principal do cliente. Os campos marcados com * são obrigatórios.")

    cliente_cep = st.text_input("CEP*", value=st.session_state.cliente_cep_input, max_chars=9, help="Digite o CEP do cliente (somente números).", key="cliente_cep_input")
    cliente_logradouro = st.text_input("Logradouro*", value=st.session_state.cliente_logradouro_input, help="Nome do logradouro.", key="cliente_logradouro_input")
    cliente_numero = st.text_input("Número*", value=st.session_state.cliente_numero_input, help="Número do imóvel.", key="cliente_numero_input")
    cliente_complemento = st.text_input("Complemento", value=st.session_state.cliente_complemento_input, help="Ex: Apartamento, Bloco, Sala.", key="cliente_complemento_input")
    cliente_bairro = st.text_input("Bairro*", value=st.session_state.cliente_bairro_input, help="Nome do bairro.", key="cliente_bairro_input")
    cliente_cidade = st.text_input("Cidade*", value=st.session_state.cliente_cidade_input, help="Nome da cidade.", key="cliente_cidade_input")
    cliente_estado = st.text_input("Estado*", value=st.session_state.cliente_estado_input, help="Ex: CE, SP, MG", key="cliente_estado_input").upper()

    # --- Opção para Endereço de Entrega ---
    st.markdown("---")
    # O valor do checkbox agora controla o estado da sessão diretamente
    st.session_state.show_endereco_entrega = st.checkbox("Cadastrar Endereço de Entrega (se diferente do principal)", value=st.session_state.show_endereco_entrega, key="show_endereco_entrega_checkbox")

    if st.session_state.show_endereco_entrega:
        st.header("Endereço de Entrega")
        st.write("Preencha o endereço de entrega.")

        entrega_cep = st.text_input("CEP Entrega*", value=st.session_state.entrega_cep_input, max_chars=9, help="Código de Endereçamento Postal (somente números).", key="entrega_cep_input")
        entrega_rua = st.text_input("Rua/Avenida Entrega*", value=st.session_state.entrega_rua_input, help="Nome da rua ou avenida.", key="entrega_rua_input")
        entrega_numero = st.text_input("Número Entrega*", value=st.session_state.entrega_numero_input, help="Número do imóvel.", key="entrega_numero_input")
        entrega_complemento = st.text_input("Complemento Entrega", value=st.session_state.entrega_complemento_input, help="Ex: Apartamento, Bloco, Sala.", key="entrega_complemento_input")
        entrega_bairro = st.text_input("Bairro Entrega*", value=st.session_state.entrega_bairro_input, help="Nome do bairro.", key="entrega_bairro_input")
        entrega_cidade = st.text_input("Cidade Entrega*", value=st.session_state.entrega_cidade_input, help="Nome da cidade.", key="entrega_cidade_input")
        entrega_estado = st.text_input("Estado Entrega*", value=st.session_state.entrega_estado_input, help="Ex: CE, SP, MG", key="entrega_estado_input").upper()
    else:
        # Se a seção não for exibida, garantimos que as variáveis tenham valores vazios
        entrega_cep, entrega_rua, entrega_numero, entrega_complemento, entrega_bairro, entrega_cidade, entrega_estado = ("", "", "", "", "", "", "")


    # --- Seção: Documentos para Entrega ---
    st.header("Documentos para Entrega")
    st.write("Marque os documentos que foram entregues junto com a ficha de cadastro.")
    doc_contrato_social = st.checkbox("Contrato Social", value=st.session_state.doc_contrato_social, key="doc_contrato_social")
    doc_comprovante_endereco = st.checkbox("Comprovante de Endereço (conta de água ou energia)", value=st.session_state.doc_comprovante_endereco, key="doc_comprovante_endereco")


    # --- Opção para Referências ---
    st.markdown("---")
    # O valor do checkbox agora controla o estado da sessão diretamente
    st.session_state.show_referencias = st.checkbox("Cadastrar Referências", value=st.session_state.show_referencias, key="show_referencias_checkbox")

    if st.session_state.show_referencias:
        st.header("Referências")
        st.write("Forneça até 3 referências (pessoas ou empresas que possam atestar sobre o cliente).")
        referencia1_nome = st.text_input("Nome Referência 1", value=st.session_state.ref1_nome, key="ref1_nome")
        referencia1_contato = st.text_input("Contato Referência 1 (Telefone/Email)", value=st.session_state.ref1_contato, key="ref1_contato")
        referencia2_nome = st.text_input("Nome Referência 2", value=st.session_state.ref2_nome, key="ref2_nome")
        referencia2_contato = st.text_input("Contato Referência 2 (Telefone/Email)", value=st.session_state.ref2_contato, key="ref2_contato")
        referencia3_nome = st.text_input("Nome Referência 3", value=st.session_state.ref3_nome, key="ref3_nome")
        referencia3_contato = st.text_input("Contato Referência 3 (Telefone/Email)", value=st.session_state.ref3_contato, key="ref3_contato")
    else:
        # Se a seção não for exibida, garantimos que as variáveis tenham valores vazios
        referencia1_nome, referencia1_contato = ("", "")
        referencia2_nome, referencia2_contato = ("", "")
        referencia3_nome, referencia3_contato = ("", "")


    # --- Seção: Campo de Observação ---
    st.header("Observações")
    observacao = st.text_area("Observações Adicionais", value=st.session_state.observacao_area, height=150, help="Qualquer informação extra relevante sobre o cliente.", key="observacao_area")

    # --- Botões de Ação ---
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Gerar e Baixar Ficha em Excel", type="primary", use_container_width=True):
            # --- Validação dos Campos Obrigatórios ---
            if not (nome and documento and telefone and cliente_cep and cliente_logradouro and
                    cliente_numero and cliente_bairro and cliente_cidade and cliente_estado):
                st.error("🚨 Por favor, preencha todos os campos obrigatórios (marcados com *).")
            # Validação para endereço de entrega SE a opção for marcada
            elif st.session_state.show_endereco_entrega and not (entrega_cep and entrega_rua and
                                                                 entrega_numero and entrega_bairro and
                                                                 entrega_cidade and entrega_estado):
                st.error("🚨 Por favor, preencha todos os campos obrigatórios do Endereço de Entrega.")
            else:
                # --- Coleta e Organização dos Dados ---
                dados_cliente = {
                    "Nome/Razão Social": nome,
                    "Nome Fantasia": fantasia if fantasia else "Não informado",
                    "Inscrição Estadual": insc_estadual if insc_estadual else "Não informado",
                    "Inscrição Municipal": insc_municipal if insc_municipal else "Não informado",
                    "Email": email if email else "Não informado",
                    "Telefone": telefone,
                    "Celular": celular if celular else "Não informado",
                    "Tipo Documento": tipo_documento,
                    "Documento": documento,
                    "Endereço do Cliente (Principal)": {
                        "CEP": cliente_cep,
                        "Logradouro": cliente_logradouro,
                        "Número": cliente_numero,
                        "Complemento": cliente_complemento if cliente_complemento else "Não informado",
                        "Bairro": cliente_bairro,
                        "Cidade": cliente_cidade,
                        "Estado": cliente_estado
                    },
                    "Endereço de Entrega (Opcional)": {}, # Inicializa vazio
                    "Documentos Entregues": {
                        "Contrato Social": "Sim" if doc_contrato_social else "Não",
                        "Comprovante de Endereço": "Sim" if doc_comprovante_endereco else "Não"
                    },
                    "Referências": [], # Inicializa vazio
                    "Observações": observacao if observacao else "Nenhuma observação."
                }

                # Preenche Endereço de Entrega se for cadastrado
                if st.session_state.show_endereco_entrega:
                    dados_cliente["Endereço de Entrega (Opcional)"] = {
                        "CEP": entrega_cep,
                        "Rua/Avenida": entrega_rua,
                        "Número": entrega_numero,
                        "Complemento": entrega_complemento if entrega_complemento else "Não informado",
                        "Bairro": entrega_bairro,
                        "Cidade": entrega_cidade,
                        "Estado": entrega_estado
                    }
                else: # Se não for para cadastrar, preenche com "Não informado"
                     dados_cliente["Endereço de Entrega (Opcional)"] = {
                        "CEP": "Não informado", "Rua/Avenida": "Não informado", "Número": "Não informado",
                        "Complemento": "Não informado", "Bairro": "Não informado", "Cidade": "Não informado",
                        "Estado": "Não informado"
                    }

                # Preenche Referências se for cadastrado
                if st.session_state.show_referencias:
                    if referencia1_nome:
                        dados_cliente["Referências"].append({"Nome": referencia1_nome, "Contato": referencia1_contato})
                    if referencia2_nome:
                        dados_cliente["Referências"].append({"Nome": referencia2_nome, "Contato": referencia2_contato})
                    if referencia3_nome:
                        dados_cliente["Referências"].append({"Nome": referencia3_nome, "Contato": referencia3_contato})
                else: # Se não for para cadastrar, preenche com "Não informado"
                    dados_cliente["Referências"].append({"Nome": "Não informado", "Contato": "Não informado"})


                # --- Geração e Download do Arquivo Excel ---
                st.success("✅ Ficha preenchida com sucesso! Agora você pode baixar o arquivo Excel.")
                st.write("---")
                st.subheader("📥 Baixar Ficha em Excel")

                # Preparar os dados para o DataFrame do Pandas
                data_for_excel = [
                    {"Campo": "Nome/Razão Social", "Valor": dados_cliente['Nome/Razão Social']},
                    {"Campo": "Nome Fantasia", "Valor": dados_cliente['Nome Fantasia']},
                    {"Campo": "Inscrição Estadual", "Valor": dados_cliente['Inscrição Estadual']},
                    {"Campo": "Inscrição Municipal", "Valor": dados_cliente['Inscrição Municipal']},
                    {"Campo": "Email", "Valor": dados_cliente['Email']},
                    {"Campo": "Telefone", "Valor": dados_cliente['Telefone']},
                    {"Campo": "Celular", "Valor": dados_cliente['Celular']},
                    {"Campo": "Tipo Documento", "Valor": dados_cliente['Tipo Documento']},
                    {"Campo": "Documento", "Valor": dados_cliente['Documento']},
                    # Campos do Endereço do Cliente (Principal)
                    {"Campo": "Endereço Principal - CEP", "Valor": dados_cliente['Endereço do Cliente (Principal)']['CEP']},
                    {"Campo": "Endereço Principal - Logradouro", "Valor": dados_cliente['Endereço do Cliente (Principal)']['Logradouro']},
                    {"Campo": "Endereço Principal - Número", "Valor": dados_cliente['Endereço do Cliente (Principal)']['Número']},
                    {"Campo": "Endereço Principal - Complemento", "Valor": dados_cliente['Endereço do Cliente (Principal)']['Complemento']},
                    {"Campo": "Endereço Principal - Bairro", "Valor": dados_cliente['Endereço do Cliente (Principal)']['Bairro']},
                    {"Campo": "Endereço Principal - Cidade", "Valor": dados_cliente['Endereço do Cliente (Principal)']['Cidade']},
                    {"Campo": "Endereço Principal - Estado", "Valor": dados_cliente['Endereço do Cliente (Principal)']['Estado']},
                    # Campos do Endereço de Entrega
                    {"Campo": "Endereço Entrega - CEP", "Valor": dados_cliente['Endereço de Entrega (Opcional)']['CEP']},
                    {"Campo": "Endereço Entrega - Rua/Avenida", "Valor": dados_cliente['Endereço de Entrega (Opcional)']['Rua/Avenida']},
                    {"Campo": "Endereço Entrega - Número", "Valor": dados_cliente['Endereço de Entrega (Opcional)']['Número']},
                    {"Campo": "Endereço Entrega - Complemento", "Valor": dados_cliente['Endereço de Entrega (Opcional)']['Complemento']},
                    {"Campo": "Endereço Entrega - Bairro", "Valor": dados_cliente['Endereço de Entrega (Opcional)']['Bairro']},
                    {"Campo": "Endereço Entrega - Cidade", "Valor": dados_cliente['Endereço de Entrega (Opcional)']['Cidade']},
                    {"Campo": "Endereço Entrega - Estado", "Valor": dados_cliente['Endereço de Entrega (Opcional)']['Estado']},

                    {"Campo": "Documento: Contrato Social Entregue?", "Valor": dados_cliente['Documentos Entregues']['Contrato Social']},
                    {"Campo": "Documento: Comprovante de Endereço Entregue?", "Valor": dados_cliente['Documentos Entregues']['Comprovante de Endereço']}
                ]

                # Adiciona referências ao data_for_excel
                for i, ref in enumerate(dados_cliente["Referências"]):
                    data_for_excel.append({"Campo": f"Referência {i+1} Nome", "Valor": ref['Nome']})
                    data_for_excel.append({"Campo": f"Referência {i+1} Contato", "Valor": ref['Contato']})
                
                # Se nenhuma referência foi informada, garantir que apareça "Não informado"
                if not dados_cliente["Referências"] and not st.session_state.show_referencias:
                     data_for_excel.append({"Campo": "Referências", "Valor": "Não informado"})


                data_for_excel.append({"Campo": "Observações", "Valor": dados_cliente['Observações']})

                df = pd.DataFrame(data_for_excel)

                output = BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Cadastro Cliente')
                processed_data = output.getvalue()

                st.download_button(
                    label="Clique para Baixar Ficha em Excel",
                    data=processed_data,
                    file_name=f"cadastro_cliente_{dados_cliente['Nome/Razão Social'].replace(' ', '_').lower()}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    help="Baixa um arquivo Excel (.xlsx) com os dados preenchidos."
                )

    with col2:
        # Botão para limpar o formulário
        if st.button("Limpar Cadastro", type="secondary", use_container_width=True, on_click=clear_form):
            pass

# --- Execução da Aplicação ---
if __name__ == "__main__":
    app()