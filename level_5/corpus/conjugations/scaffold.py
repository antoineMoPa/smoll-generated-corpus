#!/usr/bin/env python3
"""
Creates corpus/conjugations/ directory structure and prompts.txt files.
5 languages × 6 tenses × 10 batches of 10 verbs = 300 corpus files.
Each corpus file contains 10 full conjugation tables.
"""

import os

BASE = os.path.dirname(os.path.abspath(__file__))

BATCH_SIZE = 10

# ---------------------------------------------------------------------------
# Format template embedded in every prompt
# ---------------------------------------------------------------------------

FORMAT = (
    "Format each verb as follows (blank line between verbs, no extra text):\n"
    "Verb: <infinitive> (<english gloss>)\n"
    "Language: <language>\n"
    "Tense: <tense name>\n"
    "<pronoun/person>: <conjugated form>\n"
    "...(one line per person)\n\n"
    "Use the standard persons for the language. Output only the tables, nothing else."
)

# ---------------------------------------------------------------------------
# Languages
# ---------------------------------------------------------------------------

LANGUAGES = {
    "french": {
        "label": "French",
        "persons": "je, tu, il/elle, nous, vous, ils/elles",
        "tenses": [
            ("present",      "présent de l'indicatif"),
            ("imperfect",    "imparfait de l'indicatif"),
            ("passe_compose","passé composé"),
            ("future",       "futur simple"),
            ("conditional",  "conditionnel présent"),
            ("subjunctive",  "subjonctif présent"),
        ],
        "verbs": [
            ("être", "to be"), ("avoir", "to have"), ("aller", "to go"),
            ("faire", "to do/make"), ("dire", "to say"), ("pouvoir", "to be able to"),
            ("vouloir", "to want"), ("savoir", "to know"), ("venir", "to come"),
            ("voir", "to see"), ("prendre", "to take"), ("parler", "to speak"),
            ("donner", "to give"), ("partir", "to leave"), ("mettre", "to put"),
            ("passer", "to pass"), ("venir", "to come"), ("tenir", "to hold"),
            ("porter", "to carry"), ("regarder", "to watch"), ("trouver", "to find"),
            ("laisser", "to leave/let"), ("appeler", "to call"), ("sentir", "to feel"),
            ("croire", "to believe"), ("penser", "to think"), ("suivre", "to follow"),
            ("écrire", "to write"), ("vivre", "to live"), ("comprendre", "to understand"),
            ("entrer", "to enter"), ("sortir", "to go out"), ("rendre", "to give back"),
            ("manger", "to eat"), ("montrer", "to show"), ("chercher", "to look for"),
            ("jouer", "to play"), ("attendre", "to wait"), ("tomber", "to fall"),
            ("continuer", "to continue"), ("finir", "to finish"), ("ouvrir", "to open"),
            ("lire", "to read"), ("courir", "to run"), ("connaître", "to know (someone)"),
            ("aimer", "to love/like"), ("travailler", "to work"), ("devenir", "to become"),
            ("recevoir", "to receive"), ("répondre", "to answer"), ("décider", "to decide"),
            ("apprendre", "to learn"), ("permettre", "to allow"), ("revenir", "to come back"),
            ("arriver", "to arrive"), ("descendre", "to go down"), ("monter", "to go up"),
            ("sembler", "to seem"), ("expliquer", "to explain"), ("utiliser", "to use"),
            ("garder", "to keep"), ("imaginer", "to imagine"), ("toucher", "to touch"),
            ("produire", "to produce"), ("servir", "to serve"), ("présenter", "to present"),
            ("retourner", "to return"), ("reconnaître", "to recognize"), ("proposer", "to propose"),
            ("entendre", "to hear"), ("obtenir", "to obtain"), ("réussir", "to succeed"),
            ("payer", "to pay"), ("choisir", "to choose"), ("lever", "to lift"),
            ("dormir", "to sleep"), ("conduire", "to drive"), ("naître", "to be born"),
            ("mourir", "to die"), ("pleurer", "to cry"), ("rire", "to laugh"),
            ("couper", "to cut"), ("vendre", "to sell"), ("construire", "to build"),
            ("perdre", "to lose"), ("changer", "to change"), ("marcher", "to walk"),
            ("rester", "to stay"), ("rappeler", "to recall"), ("commencer", "to start"),
            ("réaliser", "to realize"), ("éviter", "to avoid"), ("représenter", "to represent"),
            ("chanter", "to sing"), ("cuisiner", "to cook"), ("peindre", "to paint"),
            ("boire", "to drink"), ("nager", "to swim"), ("danser", "to dance"),
        ],
    },
    "spanish": {
        "label": "Spanish",
        "persons": "yo, tú, él/ella, nosotros, vosotros, ellos/ellas",
        "tenses": [
            ("present",      "presente de indicativo"),
            ("preterite",    "pretérito indefinido"),
            ("imperfect",    "pretérito imperfecto"),
            ("future",       "futuro simple"),
            ("conditional",  "condicional simple"),
            ("subjunctive",  "subjuntivo presente"),
        ],
        "verbs": [
            ("ser", "to be (permanent)"), ("estar", "to be (temporary)"), ("haber", "to have (auxiliary)"),
            ("tener", "to have"), ("hacer", "to do/make"), ("poder", "to be able to"),
            ("decir", "to say"), ("ir", "to go"), ("ver", "to see"),
            ("dar", "to give"), ("saber", "to know"), ("querer", "to want"),
            ("llegar", "to arrive"), ("pasar", "to pass/happen"), ("deber", "to owe/must"),
            ("poner", "to put"), ("parecer", "to seem"), ("quedar", "to stay/remain"),
            ("creer", "to believe"), ("hablar", "to speak"), ("llevar", "to carry/wear"),
            ("dejar", "to leave/let"), ("seguir", "to follow"), ("encontrar", "to find"),
            ("llamar", "to call"), ("venir", "to come"), ("pensar", "to think"),
            ("salir", "to go out"), ("volver", "to return"), ("tomar", "to take"),
            ("conocer", "to know (someone)"), ("vivir", "to live"), ("sentir", "to feel"),
            ("tratar", "to treat/try"), ("mirar", "to look at"), ("contar", "to count/tell"),
            ("empezar", "to begin"), ("esperar", "to wait/hope"), ("buscar", "to look for"),
            ("existir", "to exist"), ("entrar", "to enter"), ("trabajar", "to work"),
            ("escribir", "to write"), ("perder", "to lose"), ("producir", "to produce"),
            ("ocurrir", "to occur"), ("entender", "to understand"), ("pedir", "to ask for"),
            ("recibir", "to receive"), ("recordar", "to remember"), ("terminar", "to finish"),
            ("permitir", "to allow"), ("aparecer", "to appear"), ("conseguir", "to achieve"),
            ("comenzar", "to begin"), ("servir", "to serve"), ("sacar", "to take out"),
            ("necesitar", "to need"), ("mantener", "to maintain"), ("resultar", "to result"),
            ("leer", "to read"), ("caer", "to fall"), ("cambiar", "to change"),
            ("presentar", "to present"), ("crear", "to create"), ("abrir", "to open"),
            ("considerar", "to consider"), ("oír", "to hear"), ("andar", "to walk"),
            ("jugar", "to play"), ("dormir", "to sleep"), ("morir", "to die"),
            ("pagar", "to pay"), ("ayudar", "to help"), ("ganar", "to win/earn"),
            ("usar", "to use"), ("explicar", "to explain"), ("preguntar", "to ask"),
            ("tocar", "to touch/play"), ("correr", "to run"), ("beber", "to drink"),
            ("comer", "to eat"), ("traer", "to bring"), ("estudiar", "to study"),
            ("aprender", "to learn"), ("construir", "to build"), ("nacer", "to be born"),
            ("moverse", "to move"), ("elegir", "to choose"), ("crecer", "to grow"),
            ("subir", "to go up"), ("bajar", "to go down"), ("reír", "to laugh"),
            ("cantar", "to sing"), ("bailar", "to dance"), ("cocinar", "to cook"),
            ("viajar", "to travel"), ("comprar", "to buy"), ("vender", "to sell"),
        ],
    },
    "italian": {
        "label": "Italian",
        "persons": "io, tu, lui/lei, noi, voi, loro",
        "tenses": [
            ("present",      "presente indicativo"),
            ("imperfect",    "imperfetto indicativo"),
            ("passe_compose","passato prossimo"),
            ("future",       "futuro semplice"),
            ("conditional",  "condizionale presente"),
            ("subjunctive",  "congiuntivo presente"),
        ],
        "verbs": [
            ("essere", "to be"), ("avere", "to have"), ("fare", "to do/make"),
            ("dire", "to say"), ("potere", "to be able to"), ("volere", "to want"),
            ("sapere", "to know"), ("venire", "to come"), ("vedere", "to see"),
            ("dare", "to give"), ("andare", "to go"), ("stare", "to stay/be"),
            ("parlare", "to speak"), ("trovare", "to find"), ("mettere", "to put"),
            ("passare", "to pass"), ("tenere", "to hold"), ("portare", "to carry"),
            ("guardare", "to watch"), ("lasciare", "to leave/let"), ("sentire", "to feel/hear"),
            ("credere", "to believe"), ("pensare", "to think"), ("seguire", "to follow"),
            ("scrivere", "to write"), ("vivere", "to live"), ("capire", "to understand"),
            ("entrare", "to enter"), ("uscire", "to go out"), ("rendere", "to render/give back"),
            ("mangiare", "to eat"), ("mostrare", "to show"), ("cercare", "to look for"),
            ("giocare", "to play"), ("aspettare", "to wait"), ("cadere", "to fall"),
            ("continuare", "to continue"), ("finire", "to finish"), ("aprire", "to open"),
            ("leggere", "to read"), ("correre", "to run"), ("conoscere", "to know (someone)"),
            ("amare", "to love"), ("lavorare", "to work"), ("diventare", "to become"),
            ("ricevere", "to receive"), ("rispondere", "to answer"), ("decidere", "to decide"),
            ("imparare", "to learn"), ("permettere", "to allow"), ("tornare", "to return"),
            ("arrivare", "to arrive"), ("scendere", "to go down"), ("salire", "to go up"),
            ("sembrare", "to seem"), ("spiegare", "to explain"), ("usare", "to use"),
            ("mantenere", "to maintain"), ("immaginare", "to imagine"), ("toccare", "to touch"),
            ("produrre", "to produce"), ("servire", "to serve"), ("presentare", "to present"),
            ("riconoscere", "to recognize"), ("proporre", "to propose"), ("sentire", "to hear"),
            ("ottenere", "to obtain"), ("riuscire", "to succeed"), ("pagare", "to pay"),
            ("scegliere", "to choose"), ("alzare", "to lift"), ("dormire", "to sleep"),
            ("guidare", "to drive"), ("nascere", "to be born"), ("morire", "to die"),
            ("piangere", "to cry"), ("ridere", "to laugh"), ("tagliare", "to cut"),
            ("vendere", "to sell"), ("costruire", "to build"), ("perdere", "to lose"),
            ("cambiare", "to change"), ("camminare", "to walk"), ("restare", "to stay"),
            ("cominciare", "to start"), ("realizzare", "to realize"), ("evitare", "to avoid"),
            ("cantare", "to sing"), ("cucinare", "to cook"), ("dipingere", "to paint"),
            ("bere", "to drink"), ("nuotare", "to swim"), ("ballare", "to dance"),
            ("comprare", "to buy"), ("viaggiare", "to travel"), ("studiare", "to study"),
        ],
    },
    "portuguese": {
        "label": "Portuguese",
        "persons": "eu, tu, ele/ela, nós, vós, eles/elas",
        "tenses": [
            ("present",      "presente do indicativo"),
            ("imperfect",    "pretérito imperfeito do indicativo"),
            ("preterite",    "pretérito perfeito do indicativo"),
            ("future",       "futuro do presente"),
            ("conditional",  "condicional presente"),
            ("subjunctive",  "subjuntivo presente"),
        ],
        "verbs": [
            ("ser", "to be (permanent)"), ("estar", "to be (temporary)"), ("ter", "to have"),
            ("haver", "to have (auxiliary)"), ("fazer", "to do/make"), ("poder", "to be able to"),
            ("dizer", "to say"), ("ir", "to go"), ("ver", "to see"),
            ("dar", "to give"), ("saber", "to know"), ("querer", "to want"),
            ("chegar", "to arrive"), ("passar", "to pass"), ("dever", "to owe/must"),
            ("pôr", "to put"), ("parecer", "to seem"), ("ficar", "to stay/become"),
            ("crer", "to believe"), ("falar", "to speak"), ("levar", "to carry/take"),
            ("deixar", "to leave/let"), ("seguir", "to follow"), ("encontrar", "to find"),
            ("chamar", "to call"), ("vir", "to come"), ("pensar", "to think"),
            ("sair", "to go out"), ("voltar", "to return"), ("tomar", "to take"),
            ("conhecer", "to know (someone)"), ("viver", "to live"), ("sentir", "to feel"),
            ("tratar", "to treat/try"), ("olhar", "to look at"), ("contar", "to count/tell"),
            ("começar", "to begin"), ("esperar", "to wait/hope"), ("buscar", "to look for"),
            ("existir", "to exist"), ("entrar", "to enter"), ("trabalhar", "to work"),
            ("escrever", "to write"), ("perder", "to lose"), ("produzir", "to produce"),
            ("ocorrer", "to occur"), ("entender", "to understand"), ("pedir", "to ask for"),
            ("receber", "to receive"), ("lembrar", "to remember"), ("terminar", "to finish"),
            ("permitir", "to allow"), ("aparecer", "to appear"), ("conseguir", "to achieve"),
            ("servir", "to serve"), ("tirar", "to take out"), ("precisar", "to need"),
            ("manter", "to maintain"), ("resultar", "to result"), ("ler", "to read"),
            ("cair", "to fall"), ("mudar", "to change"), ("apresentar", "to present"),
            ("criar", "to create"), ("abrir", "to open"), ("considerar", "to consider"),
            ("ouvir", "to hear"), ("andar", "to walk"), ("jogar", "to play"),
            ("dormir", "to sleep"), ("morrer", "to die"), ("pagar", "to pay"),
            ("ajudar", "to help"), ("ganhar", "to win/earn"), ("usar", "to use"),
            ("explicar", "to explain"), ("perguntar", "to ask"), ("tocar", "to touch/play"),
            ("correr", "to run"), ("beber", "to drink"), ("comer", "to eat"),
            ("trazer", "to bring"), ("estudar", "to study"), ("aprender", "to learn"),
            ("construir", "to build"), ("nascer", "to be born"), ("mover", "to move"),
            ("escolher", "to choose"), ("crescer", "to grow"), ("subir", "to go up"),
            ("descer", "to go down"), ("rir", "to laugh"), ("cantar", "to sing"),
            ("dançar", "to dance"), ("cozinhar", "to cook"), ("viajar", "to travel"),
            ("comprar", "to buy"), ("vender", "to sell"), ("nadar", "to swim"),
        ],
    },
    "english": {
        "label": "English",
        "persons": "I, you, he/she/it, we, you (plural), they",
        "tenses": [
            ("simple_present",    "simple present"),
            ("simple_past",       "simple past"),
            ("present_perfect",   "present perfect"),
            ("future_will",       "future (will)"),
            ("present_continuous","present continuous"),
            ("past_continuous",   "past continuous"),
        ],
        "verbs": [
            ("be", "to be"), ("have", "to have"), ("do", "to do"),
            ("say", "to say"), ("get", "to get"), ("make", "to make"),
            ("go", "to go"), ("know", "to know"), ("take", "to take"),
            ("see", "to see"), ("come", "to come"), ("think", "to think"),
            ("look", "to look"), ("want", "to want"), ("give", "to give"),
            ("use", "to use"), ("find", "to find"), ("tell", "to tell"),
            ("ask", "to ask"), ("seem", "to seem"), ("feel", "to feel"),
            ("try", "to try"), ("leave", "to leave"), ("call", "to call"),
            ("keep", "to keep"), ("let", "to let"), ("begin", "to begin"),
            ("show", "to show"), ("hear", "to hear"), ("play", "to play"),
            ("run", "to run"), ("move", "to move"), ("live", "to live"),
            ("believe", "to believe"), ("hold", "to hold"), ("bring", "to bring"),
            ("happen", "to happen"), ("write", "to write"), ("provide", "to provide"),
            ("sit", "to sit"), ("stand", "to stand"), ("lose", "to lose"),
            ("pay", "to pay"), ("meet", "to meet"), ("include", "to include"),
            ("continue", "to continue"), ("set", "to set"), ("learn", "to learn"),
            ("change", "to change"), ("lead", "to lead"), ("understand", "to understand"),
            ("watch", "to watch"), ("follow", "to follow"), ("stop", "to stop"),
            ("create", "to create"), ("speak", "to speak"), ("read", "to read"),
            ("spend", "to spend"), ("grow", "to grow"), ("open", "to open"),
            ("walk", "to walk"), ("win", "to win"), ("offer", "to offer"),
            ("remember", "to remember"), ("love", "to love"), ("consider", "to consider"),
            ("appear", "to appear"), ("buy", "to buy"), ("wait", "to wait"),
            ("serve", "to serve"), ("die", "to die"), ("send", "to send"),
            ("expect", "to expect"), ("build", "to build"), ("stay", "to stay"),
            ("fall", "to fall"), ("cut", "to cut"), ("reach", "to reach"),
            ("kill", "to kill"), ("remain", "to remain"), ("suggest", "to suggest"),
            ("raise", "to raise"), ("pass", "to pass"), ("sell", "to sell"),
            ("decide", "to decide"), ("return", "to return"), ("explain", "to explain"),
            ("hope", "to hope"), ("develop", "to develop"), ("carry", "to carry"),
            ("break", "to break"), ("receive", "to receive"), ("agree", "to agree"),
            ("support", "to support"), ("hit", "to hit"), ("produce", "to produce"),
            ("eat", "to eat"), ("cover", "to cover"), ("catch", "to catch"),
            ("choose", "to choose"), ("drive", "to drive"), ("throw", "to throw"),
        ],
    },
}


def batches(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


def build_prompt(lang_key: str, info: dict, tense_slug: str, tense_name: str, batch: list) -> str:
    verb_list = ", ".join(f"{v} ({g})" for v, g in batch)
    return (
        f"Generate conjugation tables for the following {len(batch)} {info['label']} verbs "
        f"in the {tense_name} tense: {verb_list}. "
        f"Persons: {info['persons']}. "
        + FORMAT
    )


def main():
    os.makedirs(BASE, exist_ok=True)
    total_dirs = 0
    total_prompts = 0

    for lang_key, info in LANGUAGES.items():
        for tense_slug, tense_name in info["tenses"]:
            dirpath = os.path.join(BASE, lang_key, tense_slug)
            os.makedirs(dirpath, exist_ok=True)

            lines = []
            for i, batch in enumerate(batches(info["verbs"], BATCH_SIZE), 1):
                filename = f"batch_{i:02d}.corpus"
                prompt = build_prompt(lang_key, info, tense_slug, tense_name, batch)
                prompt_oneline = prompt.replace("\n", " | ")
                lines.append(f"{filename} {prompt_oneline}")

            prompts_path = os.path.join(dirpath, "prompts.txt")
            with open(prompts_path, "w") as f:
                f.write("\n".join(lines) + "\n")

            total_dirs += 1
            total_prompts += len(lines)
            print(f"  {lang_key}/{tense_slug}/prompts.txt ({len(lines)} prompts)")

    print(f"\nDone! Created {total_dirs} directories with {total_prompts} total prompts.")


if __name__ == "__main__":
    main()
