import json
import os
import re
from typing import Any, Dict, List, Sequence, TypedDict

import streamlit as st
from dotenv import load_dotenv
from mistralai import Mistral

MAX_LOG_CHARS = 12000
DEFAULT_MODEL = "mistral-small-latest"
VALID_CRITICALITIES = {"CRITIQUE", "MAJEUR", "MINEUR", "INFO"}


class IncidentAnalysis(TypedDict):
    criticite: str
    resume_technique: str
    plan_action: List[str]


class MistralAPIError(Exception):
    """Raised when the Mistral call fails or the response is invalid."""


def load_settings() -> Dict[str, str]:
    load_dotenv()
    return {"api_key": os.environ.get("MISTRAL_API_KEY", "").strip()}


def build_system_prompt() -> str:
    return (
        "Tu es un ingénieur d'exploitation de premier niveau en data center. "
        "Analyse le log fourni et réponds uniquement en JSON valide, sans Markdown ni texte additionnel. "
        "Le JSON doit respecter exactement ce schéma: "
        '{"criticite":"CRITIQUE|MAJEUR|MINEUR|INFO","resume_technique":"2 phrases maximum","plan_action":["étape 1","étape 2","étape 3"]}. '
        "Contraintes: criticite en majuscules, resume_technique en français, plan_action avec exactement 3 étapes courtes et actionnables."
    )


def strip_code_fences(text: str) -> str:
    candidate = text.strip()
    if not candidate.startswith("```"):
        return candidate

    lines = candidate.splitlines()
    if len(lines) < 2:
        return candidate

    lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def count_sentences(text: str) -> int:
    fragments = [fragment for fragment in re.split(r"(?<=[.!?])\s+", text.strip()) if fragment]
    return len(fragments) if fragments else 0


def parse_model_output(raw_content: str) -> IncidentAnalysis:
    normalized = strip_code_fences(raw_content)

    try:
        data = json.loads(normalized)
    except json.JSONDecodeError as exc:
        raise MistralAPIError("La réponse du modèle n'est pas un JSON valide.") from exc

    if not isinstance(data, dict):
        raise MistralAPIError("La réponse du modèle doit être un objet JSON.")

    criticite = str(data.get("criticite", "")).strip().upper()
    resume_technique = str(data.get("resume_technique", "")).strip()
    plan_action = data.get("plan_action")

    if criticite not in VALID_CRITICALITIES:
        raise MistralAPIError(
            "La criticité retournée est invalide. Valeurs attendues: CRITIQUE, MAJEUR, MINEUR, INFO."
        )

    if not resume_technique:
        raise MistralAPIError("Le résumé technique est vide.")

    if count_sentences(resume_technique) > 2:
        raise MistralAPIError("Le résumé technique dépasse la limite de deux phrases.")

    if not isinstance(plan_action, list) or len(plan_action) != 3:
        raise MistralAPIError("Le plan d'action doit contenir exactement trois étapes.")

    cleaned_plan: List[str] = []
    for item in plan_action:
        if not isinstance(item, str) or not item.strip():
            raise MistralAPIError("Une étape du plan d'action est vide ou invalide.")
        cleaned_plan.append(item.strip())

    return {
        "criticite": criticite,
        "resume_technique": resume_technique,
        "plan_action": cleaned_plan,
    }


def extract_content(response: Any) -> str:
    choices = getattr(response, "choices", None)
    if choices is None and isinstance(response, dict):
        choices = response.get("choices")

    if not isinstance(choices, Sequence) or not choices:
        raise MistralAPIError("Réponse API incomplète: aucune proposition trouvée.")

    first_choice = choices[0]
    message = getattr(first_choice, "message", None)
    if message is None and isinstance(first_choice, dict):
        message = first_choice.get("message")

    if message is None:
        raise MistralAPIError("Réponse API incomplète: message absent.")

    content = getattr(message, "content", None)
    if content is None and isinstance(message, dict):
        content = message.get("content")

    if not isinstance(content, str) or not content.strip():
        raise MistralAPIError("Réponse API incomplète: contenu manquant.")

    return content


def translate_exception(exc: Exception) -> MistralAPIError:
    message = str(exc).lower()
    if any(keyword in message for keyword in ("timeout", "timed out", "read timeout")):
        return MistralAPIError(
            "Le délai de réponse de l'API Mistral a été dépassé. Réessaie dans quelques instants."
        )
    if any(keyword in message for keyword in ("connect", "connection", "network", "dns")):
        return MistralAPIError(
            "Impossible de contacter l'API Mistral. Vérifie ta connexion réseau."
        )
    if any(keyword in message for keyword in ("401", "unauthorized", "auth")):
        return MistralAPIError(
            "Authentification Mistral échouée. Vérifie la valeur de MISTRAL_API_KEY dans .env."
        )
    return MistralAPIError("L'appel à Mistral a échoué de manière inattendue.")


def call_mistral(api_key: str, incident_log: str) -> IncidentAnalysis:
    client = Mistral(api_key=api_key)
    messages = [
        {"role": "system", "content": build_system_prompt()},
        {"role": "user", "content": f"Log serveur brut:\n{incident_log}"},
    ]

    try:
        response = client.chat.complete(
            model=DEFAULT_MODEL,
            messages=messages,
            temperature=0.2,
            response_format={"type": "json_object"},
        )
    except Exception as exc:  # noqa: BLE001
        raise translate_exception(exc) from exc

    try:
        content = extract_content(response)
        return parse_model_output(content)
    except MistralAPIError:
        raise
    except Exception as exc:  # noqa: BLE001
        raise MistralAPIError("Réponse Mistral inattendue ou illisible.") from exc


def render_result(result: IncidentAnalysis) -> None:
    st.success("Analyse terminée")
    st.markdown(f"### Criticité: **{result['criticite']}**")
    st.markdown("### Résumé technique")
    st.write(result["resume_technique"])
    st.markdown("### Plan d'action")
    for index, step in enumerate(result["plan_action"], start=1):
        st.write(f"{index}. {step}")


def main() -> None:
    st.set_page_config(page_title="Diagnostic incidents DCO", page_icon="🛠️", layout="centered")
    st.title("Diagnostic d'incidents DCO")
    st.caption("Colle un log serveur brut puis lance l'analyse automatisée.")

    settings = load_settings()

    incident_log = st.text_area(
        "Log d'erreur serveur",
        height=320,
        placeholder="Colle ici un log serveur brut: alertes kernel, erreurs réseau, surchauffe, etc.",
    )

    st.caption(f"Limite maximale: {MAX_LOG_CHARS} caractères")

    if st.button("Analyser l'incident", type="primary"):
        cleaned_log = incident_log.strip()

        if not settings["api_key"]:
            st.error("Clé API manquante. Définis MISTRAL_API_KEY dans ton fichier .env.")
            st.stop()

        if not cleaned_log:
            st.error("Le log est vide. Colle un log avant de lancer l'analyse.")
            st.stop()

        if len(cleaned_log) > MAX_LOG_CHARS:
            st.error(f"Le log dépasse la limite autorisée ({MAX_LOG_CHARS} caractères).")
            st.stop()

        with st.spinner("Analyse en cours..."):
            try:
                result = call_mistral(settings["api_key"], cleaned_log)
                render_result(result)
            except MistralAPIError as exc:
                st.error(str(exc))
            except Exception:  # noqa: BLE001
                st.error("Une erreur inattendue est survenue pendant l'analyse.")


if __name__ == "__main__":
    main()
