import spacy_streamlit
import streamlit as st
from anonymize import AllAnonym, LabelAnonym, RandomAnonym
from ingestors import Streamingestor
import json
from itertools import chain

from sensitive_identification.name_identifiers import SpacyIdentifier
from sensitive_identification.regex_identification import RegexIdentifier

st.set_page_config(page_title="Anonimización de contenidos generados por usuarios", header_title="Anonimizador bilingüe", layout="wide", menu_items={
    'Get Help': 'https://huggingface.co/PlanTL-GOB-ES',
    'Report a bug': 'https://github.com/TeMU-BSC/AnonymizationPipeline/issues',
    'About': 'Demostrador de anonimización de textos bilingüs castellano/catalán entrenado para entornos de participación ciudadana. Para acceder a otros demostradores del PlanTL [ver aqui](https://plantl.bsc.es)'

}, social_icons=[
            {
                "url": "https://github.com/TeMU-BSC/AnonymizationPipeline",
                "title": "Github",
                "classes": "fa-brands fa-github fa-xl",
                "color": "#fff",
            },
            {
                "url": "https://hub.docker.com/r/bsctemu/anonymization-pipeline",
                "title": "Docker Hub",
                "classes": "fa-brands fa-docker fa-xl",
                "color": "#fff",
            }
        ])



labels_colors = {"ID": "#fff1e6", "LOC": "#eae4e9", "EMAIL": "#bee1e6", "LICENSE_PLATE": "#fde2e4", "ORG": "#dfe7fd",
                 "PER": "#bee1e6", "MISC": "#f0efeb", "FINANCIAL": "#caffbf", "VEHICLE": "#fad2e1", "CARD": "#ffadad",
                 "ZIP": "#fdffb6", "TELEPHONE": "#cddafd"}

@st.cache(show_spinner=False, allow_output_mutation=True, suppress_st_warning=True)
def load_models():
    unstructured_identifier = SpacyIdentifier("es_anonimization_core_lg")
    regex_identifier = RegexIdentifier("data/regex_definition.csv")
    ingestor = Streamingestor("")
    labels = set(chain(unstructured_identifier.get_labels(), regex_identifier.get_labels()))
    return {"unstructured": unstructured_identifier, "regex": regex_identifier, "ingestor": ingestor,
            "anonymizers": {"Random": RandomAnonym(), "Etiqueta": LabelAnonym(), "Inteligente": AllAnonym()},
            "labels": labels}


models = load_models()
labels = models["labels"]

c30, c31, c32 = st.columns([2.5, 1, 3])


with st.expander("ℹ️ - Acerca del anonimizador", expanded=False):
    st.write(
        """
-   Este demostrador permite identificar (y anonimizar si así se desea) textos en castellano y catalán. Ha sido entrenado en textos bilingües de atención ciudadana.
	    """
    )
    st.markdown("")

ce, c1, ce, c2, c3 = st.columns([0.07, 1.5, 0.07, 5, 0.07])
st.markdown("")
with c1:
    # st.markdown("---")
    selection = st.radio(
        "Método de anonimización",
        ["Inteligente", "Etiqueta", "Random"],
        help="Consulta los métodos de anonimización disponibles en la sección de abajo.",
    )

    with st.expander("ℹ️ - ¿Cuales son los métodos de anonimización disponibles?"):
        st.write("""
                ##### Intelligent
                _intelligent_ reemplaza la información con substituciones a partir de gazetteers correspondientes a la etiqueta del tipo detectado. 

                > **Entrada**: "Hola, me llamo María Salima y vivo en Carrer de las Rosas 123. Tel: 617753689."

                > **Anonimizado**: "Hola, me llamo Shakira Lois y vivo en carrer de Nicaragua 94. Tel: 211608837."
                
                ##### Label
                _label_ reemplaza la información sensible con una etiqueta que identifica su clase. 

                > **Entrada**: "Hola, me llamo María Salima y vivo en Carrer de las Rosas 123. Tel: 617753689."

                > **Anonimizado**: "Hola, me llamo \<PER\> y vivo en \<LOC\>. Tel: \<TELEPHONE\>."

                ##### Random
                _random_ reemplaza la información sensible con una con una cadena de texto aleatoria, que preserva la ortotipografía (mayúsculas o minúscules, etc.). 

                > **Entrada**: "Hola, me llamo María Salima y vivo en Carrer de las Rosas 123. Tel: 617753689."

                > **Anonimizado**: "Hola, me llamo Dfkwa Mjzhnt y vivo en Ujflqo vc jaa Xvzqs 682. Tel: 441573591."
                """)

with c2:
    st.markdown("##### Entrada de datos")
    text_input = st.text_area("Escribe el texto que deseas anonimizar",
                              value="Hola, me llamo María Salima y vivo en la Calle de las Rosas 123. Tel: 617753689.")

    models["ingestor"].ingest_text(text_input)

    registry = models["ingestor"].registry
    models["unstructured"].identify_sensitive(registry)
    models["regex"].identify_sensitive(registry)

    doc = [{"text": registry.text,
            "ents": [{"start": span["start"], "end": span["end"], "label": span["label"]} for span in
                     registry.spans]}]

    st.button("Anonimizar")

    spacy_streamlit.visualize_ner(doc, colors=labels_colors, manual=True,
                                  show_table=False, labels=labels,
                                  expander_open=False, title="Identificación de datos")

    # uploaded_file = st.file_uploader("o sube un archivo", type=["doc", "docx", "txt"])

    # if uploaded_file is not None:
    #     file_input = uploaded_file.getvalue()
    #     text_input = file_input.decode("utf-8")

    # anonymize = st.checkbox("Anonimizar")

    anonymizers = models["anonymizers"]
    anonimyzer = anonymizers[selection]
    models["ingestor"].anonymize_registries(anonimyzer)
    registry = models["ingestor"].registry
    doc = [{"text": registry.text,
            "ents": [{"start": span["start"], "end": span["end"], "label": span["label"]} for span in
                     registry.spans]}]
    spacy_streamlit.visualize_ner(doc, colors=labels_colors, manual=True,
                                  show_table=False, labels=labels, key="second",
                                  expander_open=False)

    st.download_button(
        label="Descargar salida anonimizada (JSON)"
        , file_name="anonym.json"
        , mime="application/json"
        , data=json.dumps(doc[0])
    )
