#!/usr/bin/env python3
"""
Generates corpus/sentence_analysis/ structure and prompts.txt files.

For each language, qwen generates sentences and annotates every word
with its grammatical category, morphology, and syntactic function —
all written in the target language.

Scale: 5 languages × 8 categories × 3 angles = 120 corpus files
       × 15 annotated sentences each ≈ 1,800 annotated sentences ≈ ~1.5 MB
"""

import os

CORPUS_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "corpus", "sentence_analysis"
)

# ---------------------------------------------------------------------------
# Output format (embedded in every prompt)
# ---------------------------------------------------------------------------

FORMAT = """\
Format each example as follows. Write the sentence on the first line prefixed \
with the label used in the target language (e.g. "Phrase :", "Sentence:", \
"Oración:", "Frase:", "Sentença:"), then one annotation line per word. \
Separate examples with a single blank line. Output only the examples.

Example (French):
Phrase : Le chat mange une souris.
le : déterminant défini, masculin singulier
chat : nom commun, masculin singulier, sujet du verbe «mange»
mange : verbe «manger», 3e personne du singulier, présent de l'indicatif, voix active
une : déterminant indéfini, féminin singulier
souris : nom commun, féminin singulier, complément d'objet direct du verbe «mange»\
"""

# ---------------------------------------------------------------------------
# Languages and categories
# ---------------------------------------------------------------------------

LANGUAGES = {
    "french": {
        "label": "French",
        "instruction_lang": "en français",
        "categories": {
            "declaratives_simples": {
                "description": "simple declarative sentences with subject + verb or subject + verb + attribute (SV, SVC)",
                "angles": [
                    ("present_indicatif.corpus",
                     "Generate 15 annotated French sentences in the present indicative tense. "
                     "Use simple SV and SVC structures (e.g. Le soleil brille. Marie est heureuse.). "
                     "Vary subjects: proper nouns, common nouns, pronouns. Annotate all words in French."),
                    ("passe_compose.corpus",
                     "Generate 15 annotated French sentences in the passé composé. "
                     "Include both avoir and être auxiliaries. "
                     "Annotate the auxiliary and past participle separately. All annotations in French."),
                    ("imparfait_futur.corpus",
                     "Generate 15 annotated French sentences mixing imparfait and futur simple tenses. "
                     "Include state descriptions (imparfait) and future actions (futur). "
                     "All annotations in French."),
                ],
            },
            "complement_objet_direct": {
                "description": "sentences with a direct object (COD)",
                "angles": [
                    ("verbes_transitifs.corpus",
                     "Generate 15 annotated French sentences with a direct object (complément d'objet direct). "
                     "Use varied transitive verbs (manger, voir, aimer, prendre, lire, écrire, etc.). "
                     "Clearly label the COD in the annotation. All annotations in French."),
                    ("pronoms_cod.corpus",
                     "Generate 15 annotated French sentences where the direct object is replaced by a pronoun "
                     "(le, la, les, me, te, nous, vous). "
                     "Annotate pronoun type, gender, number, and function. All annotations in French."),
                    ("determinants_varies.corpus",
                     "Generate 15 annotated French sentences with varied determinants before the COD "
                     "(défini, indéfini, partitif, démonstratif, possessif). "
                     "Annotate each determinant type precisely. All annotations in French."),
                ],
            },
            "complement_objet_indirect": {
                "description": "sentences with indirect objects and prepositional complements",
                "angles": [
                    ("coi_prepositions.corpus",
                     "Generate 15 annotated French sentences with an indirect object (complément d'objet indirect) "
                     "introduced by 'à' or 'de'. Use verbs like parler à, donner à, se souvenir de, avoir besoin de. "
                     "All annotations in French."),
                    ("complements_circonstanciels.corpus",
                     "Generate 15 annotated French sentences with circumstantial complements (lieu, temps, manière, cause). "
                     "Label each complement type (CC de lieu, CC de temps, etc.). All annotations in French."),
                    ("double_objet.corpus",
                     "Generate 15 annotated French sentences with both a COD and a COI. "
                     "Use verbs like donner, envoyer, montrer, dire, expliquer. "
                     "All annotations in French."),
                ],
            },
            "subordonnees": {
                "description": "complex sentences with subordinate or relative clauses",
                "angles": [
                    ("relatives.corpus",
                     "Generate 15 annotated French sentences containing a relative clause "
                     "(introduced by qui, que, dont, où, lequel, etc.). "
                     "Annotate the relative pronoun and its antecedent. All annotations in French."),
                    ("conjonctives.corpus",
                     "Generate 15 annotated French sentences with a subordinate clause "
                     "introduced by a conjunction (parce que, quand, si, bien que, pour que, etc.). "
                     "Label the conjunction type and the mood of the subordinate verb. All annotations in French."),
                    ("infinitives.corpus",
                     "Generate 15 annotated French sentences with an infinitive complement or infinitive clause. "
                     "Include constructions like vouloir faire, essayer de, pour + infinitive. "
                     "All annotations in French."),
                ],
            },
            "interrogatives": {
                "description": "question sentences (yes/no and wh- questions)",
                "angles": [
                    ("questions_totales.corpus",
                     "Generate 15 annotated French yes/no questions using est-ce que, inversion, or intonation. "
                     "Vary question types and tenses. Annotate inversion and question structure. All annotations in French."),
                    ("questions_partielles.corpus",
                     "Generate 15 annotated French wh- questions using qui, que, quoi, où, quand, comment, pourquoi, combien. "
                     "Annotate the interrogative word and its function. All annotations in French."),
                    ("questions_indirectes.corpus",
                     "Generate 15 annotated French sentences containing an indirect question "
                     "(e.g. Je me demande si..., Il veut savoir où...). "
                     "All annotations in French."),
                ],
            },
            "negations": {
                "description": "negative constructions",
                "angles": [
                    ("negation_simple.corpus",
                     "Generate 15 annotated French sentences using simple negation (ne...pas, ne...plus, ne...jamais). "
                     "Annotate the two-part negation structure and how it frames the verb. All annotations in French."),
                    ("negation_complexe.corpus",
                     "Generate 15 annotated French sentences using complex negation (ne...rien, ne...personne, "
                     "ne...que, ne...aucun, ni...ni). Annotate the negation type and its scope. All annotations in French."),
                    ("negation_infinitif.corpus",
                     "Generate 15 annotated French sentences with negated infinitive constructions "
                     "(ne pas faire, ne jamais partir, etc.) and negated subordinate clauses. "
                     "All annotations in French."),
                ],
            },
            "pronoms": {
                "description": "sentences focused on pronoun usage and reference",
                "angles": [
                    ("pronoms_personnels.corpus",
                     "Generate 15 annotated French sentences with varied personal pronouns as subject and object. "
                     "Include tonic pronouns (moi, toi, lui, elle, nous, vous, eux, elles). "
                     "Annotate pronoun type, person, number, gender, and function. All annotations in French."),
                    ("pronoms_relatifs_demonstratifs.corpus",
                     "Generate 15 annotated French sentences using relative pronouns (qui, que, dont, lequel) "
                     "and demonstrative pronouns (celui, celle, ceux, celles, ce). "
                     "All annotations in French."),
                    ("pronoms_indefinis_possessifs.corpus",
                     "Generate 15 annotated French sentences using indefinite pronouns (on, tout, rien, quelqu'un, chacun) "
                     "and possessive pronouns (le mien, la sienne, les nôtres). "
                     "All annotations in French."),
                ],
            },
            "imperatifs_exclamatifs": {
                "description": "imperative and exclamatory sentences",
                "angles": [
                    ("imperatifs.corpus",
                     "Generate 15 annotated French imperative sentences (2nd person singular and plural, 1st person plural). "
                     "Include both affirmative and negative imperatives. "
                     "Annotate mood and the absence of an explicit subject. All annotations in French."),
                    ("exclamatives.corpus",
                     "Generate 15 annotated French exclamatory sentences using que, comme, quel/quelle/quels/quelles. "
                     "Annotate exclamative structure and word order. All annotations in French."),
                    ("imperatifs_pronominaux.corpus",
                     "Generate 15 annotated French imperative sentences with pronominal verbs or object pronouns "
                     "(Lève-toi ! Donne-le-moi ! Ne te décourage pas !). "
                     "Annotate pronoun placement and elision. All annotations in French."),
                ],
            },
        },
    },
    "english": {
        "label": "English",
        "instruction_lang": "in English",
        "categories": {
            "simple_declaratives": {
                "description": "simple declarative sentences (SV, SVC, SVO)",
                "angles": [
                    ("simple_present.corpus",
                     "Generate 15 annotated English sentences in the simple present tense. "
                     "Use SV and SVC structures. Vary subjects (nouns, pronouns, proper names). "
                     "Annotate all words in English with grammatical category and syntactic function."),
                    ("past_tenses.corpus",
                     "Generate 15 annotated English sentences in the simple past and past perfect tenses. "
                     "Mix regular and irregular verbs. Annotate tense, aspect, and verb form. All annotations in English."),
                    ("future_perfect.corpus",
                     "Generate 15 annotated English sentences using future (will/going to) and present perfect tenses. "
                     "Annotate the auxiliary verbs and their role. All annotations in English."),
                ],
            },
            "direct_objects": {
                "description": "sentences with direct and indirect objects",
                "angles": [
                    ("transitive_verbs.corpus",
                     "Generate 15 annotated English sentences with transitive verbs and direct objects. "
                     "Use varied objects (noun phrases, pronouns, gerunds). Clearly label the direct object. "
                     "All annotations in English."),
                    ("indirect_objects.corpus",
                     "Generate 15 annotated English sentences with both direct and indirect objects. "
                     "Use ditransitive verbs (give, send, tell, show, teach, buy). "
                     "Annotate both objects. All annotations in English."),
                    ("object_pronouns.corpus",
                     "Generate 15 annotated English sentences where the object is a pronoun "
                     "(him, her, it, them, me, us). "
                     "Annotate pronoun case, number, and function. All annotations in English."),
                ],
            },
            "relative_subordinate": {
                "description": "relative clauses and subordinate constructions",
                "angles": [
                    ("relative_clauses.corpus",
                     "Generate 15 annotated English sentences with relative clauses "
                     "(who, which, that, whom, whose, where, when). "
                     "Annotate the relative pronoun, antecedent, and clause type (restrictive vs. non-restrictive). "
                     "All annotations in English."),
                    ("subordinate_conjunctions.corpus",
                     "Generate 15 annotated English sentences with subordinate clauses "
                     "(because, although, when, if, unless, since, while, as soon as). "
                     "Annotate conjunction type and clause relationship. All annotations in English."),
                    ("infinitive_gerund.corpus",
                     "Generate 15 annotated English sentences with infinitive and gerund complements "
                     "(want to do, enjoy doing, stop to do, stop doing). "
                     "Annotate the non-finite verb form and its function. All annotations in English."),
                ],
            },
            "questions": {
                "description": "yes/no and wh- questions",
                "angles": [
                    ("yes_no_questions.corpus",
                     "Generate 15 annotated English yes/no questions using auxiliary inversion "
                     "(do/does/did, is/are/was/were, have/has, can/could/will/would). "
                     "Annotate the auxiliary and subject-auxiliary inversion. All annotations in English."),
                    ("wh_questions.corpus",
                     "Generate 15 annotated English wh- questions (who, what, where, when, why, how, which, whose). "
                     "Annotate the wh-word role (subject, object, adjunct) and question structure. All annotations in English."),
                    ("tag_questions.corpus",
                     "Generate 15 annotated English sentences with tag questions (isn't it, don't they, haven't you, etc.). "
                     "Annotate the main clause and the tag structure including polarity. All annotations in English."),
                ],
            },
            "negations": {
                "description": "negative constructions",
                "angles": [
                    ("auxiliary_negation.corpus",
                     "Generate 15 annotated English sentences with auxiliary negation "
                     "(don't, doesn't, didn't, isn't, aren't, haven't, can't, won't). "
                     "Annotate the contracted and full negative forms. All annotations in English."),
                    ("negative_words.corpus",
                     "Generate 15 annotated English sentences using negative words "
                     "(nobody, nothing, nowhere, never, neither, nor). "
                     "Annotate scope of negation. All annotations in English."),
                    ("partial_negation.corpus",
                     "Generate 15 annotated English sentences with partial negation and restrictive adverbs "
                     "(only, barely, hardly, scarcely, rarely). "
                     "Annotate the focus of negation. All annotations in English."),
                ],
            },
            "pronouns": {
                "description": "pronoun types and reference",
                "angles": [
                    ("personal_possessive.corpus",
                     "Generate 15 annotated English sentences featuring personal and possessive pronouns. "
                     "Cover all persons and cases (subject, object, possessive adjective, possessive pronoun). "
                     "All annotations in English."),
                    ("demonstrative_reflexive.corpus",
                     "Generate 15 annotated English sentences with demonstrative (this, that, these, those) "
                     "and reflexive pronouns (myself, yourself, himself, themselves). "
                     "All annotations in English."),
                    ("indefinite_relative.corpus",
                     "Generate 15 annotated English sentences using indefinite pronouns "
                     "(someone, anyone, everyone, nobody, something, each, every, both, either, neither). "
                     "All annotations in English."),
                ],
            },
            "passives_causatives": {
                "description": "passive voice and causative constructions",
                "angles": [
                    ("passive_voice.corpus",
                     "Generate 15 annotated English sentences in passive voice (present, past, perfect). "
                     "Annotate the agent (by-phrase), patient, and auxiliary be. All annotations in English."),
                    ("get_passive.corpus",
                     "Generate 15 annotated English sentences with get-passive constructions "
                     "(got fired, got promoted, got hurt). "
                     "Annotate how get differs from be in passive. All annotations in English."),
                    ("causatives.corpus",
                     "Generate 15 annotated English sentences with causative verbs "
                     "(make, let, have, get + object + infinitive/past participle). "
                     "All annotations in English."),
                ],
            },
            "imperatives_exclamatives": {
                "description": "imperative and exclamatory sentences",
                "angles": [
                    ("imperatives.corpus",
                     "Generate 15 annotated English imperative sentences (affirmative and negative). "
                     "Include do-imperatives (Do sit down!) and let's constructions. "
                     "Annotate the implicit subject and mood. All annotations in English."),
                    ("exclamatives.corpus",
                     "Generate 15 annotated English exclamatory sentences using what and how "
                     "(What a day! How beautiful!). "
                     "Annotate exclamative structure and word order. All annotations in English."),
                    ("conditionals.corpus",
                     "Generate 15 annotated English conditional sentences (zero, first, second, third conditionals). "
                     "Annotate the if-clause, main clause, and the modal used. All annotations in English."),
                ],
            },
        },
    },
    "spanish": {
        "label": "Spanish",
        "instruction_lang": "en español",
        "categories": {
            "declarativas_simples": {
                "description": "oraciones declarativas simples",
                "angles": [
                    ("presente_indicativo.corpus",
                     "Genera 15 oraciones declarativas en español en el presente de indicativo. "
                     "Usa estructuras SV y SVC. Varía sujetos: sustantivos, pronombres, nombres propios. "
                     "Anota todas las palabras en español con su categoría gramatical y función sintáctica."),
                    ("pasado.corpus",
                     "Genera 15 oraciones en español en el pretérito indefinido y pretérito imperfecto. "
                     "Alterna acciones puntuales (indefinido) y estados o acciones habituales (imperfecto). "
                     "Todas las anotaciones en español."),
                    ("futuro_condicional.corpus",
                     "Genera 15 oraciones en español en el futuro simple y condicional. "
                     "Incluye predicciones, promesas y hipótesis. Todas las anotaciones en español."),
                ],
            },
            "objeto_directo_indirecto": {
                "description": "oraciones con complemento directo e indirecto",
                "angles": [
                    ("complemento_directo.corpus",
                     "Genera 15 oraciones en español con complemento directo (CD). "
                     "Usa verbos transitivos variados. Señala claramente el CD en la anotación. "
                     "Todas las anotaciones en español."),
                    ("complemento_indirecto.corpus",
                     "Genera 15 oraciones en español con complemento indirecto (CI) introducido por 'a' o 'para'. "
                     "Incluye verbos como dar, decir, enviar, mostrar, explicar. "
                     "Todas las anotaciones en español."),
                    ("clíticos.corpus",
                     "Genera 15 oraciones en español con pronombres clíticos (lo, la, los, las, le, les, me, te, nos). "
                     "Incluye casos de duplicación de clítico. Anota persona, número, género y función. "
                     "Todas las anotaciones en español."),
                ],
            },
            "subordinadas": {
                "description": "oraciones subordinadas y relativas",
                "angles": [
                    ("relativas.corpus",
                     "Genera 15 oraciones en español con una oración de relativo "
                     "(que, quien, cuyo, donde, el cual, etc.). "
                     "Anota el pronombre relativo, su antecedente y el tipo de oración. "
                     "Todas las anotaciones en español."),
                    ("subordinadas_conjunciones.corpus",
                     "Genera 15 oraciones en español con subordinadas adverbiales "
                     "(porque, aunque, cuando, si, para que, antes de que, etc.). "
                     "Anota el tipo de subordinada y el modo del verbo subordinado. "
                     "Todas las anotaciones en español."),
                    ("infinitivos_gerundios.corpus",
                     "Genera 15 oraciones en español con infinitivos y gerundios como complementos verbales "
                     "(querer hacer, seguir hablando, al llegar, etc.). "
                     "Todas las anotaciones en español."),
                ],
            },
            "interrogativas": {
                "description": "oraciones interrogativas directas e indirectas",
                "angles": [
                    ("interrogativas_totales.corpus",
                     "Genera 15 oraciones interrogativas totales en español (respuesta sí/no). "
                     "Incluye inversión sujeto-verbo y entonación ascendente. "
                     "Anota la estructura interrogativa. Todas las anotaciones en español."),
                    ("interrogativas_parciales.corpus",
                     "Genera 15 oraciones interrogativas parciales en español con qué, quién, dónde, "
                     "cuándo, cómo, por qué, cuánto, cuál. "
                     "Anota el pronombre interrogativo y su función. Todas las anotaciones en español."),
                    ("interrogativas_indirectas.corpus",
                     "Genera 15 oraciones en español con interrogativas indirectas "
                     "(No sé si..., Me pregunto cuándo..., Dime qué...). "
                     "Todas las anotaciones en español."),
                ],
            },
            "negaciones": {
                "description": "construcciones negativas",
                "angles": [
                    ("negacion_simple.corpus",
                     "Genera 15 oraciones negativas simples en español usando 'no' antepuesto al verbo. "
                     "Incluye negaciones en distintos tiempos verbales. "
                     "Todas las anotaciones en español."),
                    ("palabras_negativas.corpus",
                     "Genera 15 oraciones en español con palabras negativas "
                     "(nada, nadie, nunca, jamás, ninguno, tampoco, ni...ni). "
                     "Anota la concordancia negativa. Todas las anotaciones en español."),
                    ("negacion_con_si.corpus",
                     "Genera 15 oraciones condicionales negativas en español "
                     "(si no llegas, si nunca estudias, a no ser que...). "
                     "Todas las anotaciones en español."),
                ],
            },
            "pronombres": {
                "description": "uso de pronombres y referencia",
                "angles": [
                    ("pronombres_personales.corpus",
                     "Genera 15 oraciones en español con pronombres personales sujeto y objeto "
                     "(yo, tú, él, ella, nosotros, vosotros, ellos + formas tónicas). "
                     "Anota persona, número, género y función. Todas las anotaciones en español."),
                    ("pronombres_demostrativos_posesivos.corpus",
                     "Genera 15 oraciones en español con pronombres demostrativos (este, ese, aquel y formas) "
                     "y posesivos (mío, tuyo, suyo, nuestro, etc.). "
                     "Todas las anotaciones en español."),
                    ("pronombres_indefinidos_relativos.corpus",
                     "Genera 15 oraciones en español con pronombres indefinidos "
                     "(algo, alguien, todo, cada, cualquiera, ambos) y relativos. "
                     "Todas las anotaciones en español."),
                ],
            },
            "pasiva_perifrasis": {
                "description": "voz pasiva y perífrasis verbales",
                "angles": [
                    ("voz_pasiva.corpus",
                     "Genera 15 oraciones en español en voz pasiva (ser + participio). "
                     "Incluye distintos tiempos verbales y complemento agente. "
                     "Todas las anotaciones en español."),
                    ("pasiva_refleja.corpus",
                     "Genera 15 oraciones en español con pasiva refleja (se + verbo en 3ª persona). "
                     "Anota el valor impersonal o pasivo del se. Todas las anotaciones en español."),
                    ("perifrasis_verbales.corpus",
                     "Genera 15 oraciones en español con perífrasis verbales "
                     "(estar + gerundio, ir a + infinitivo, tener que + infinitivo, acabar de + infinitivo). "
                     "Todas las anotaciones en español."),
                ],
            },
            "imperativos_exclamativos": {
                "description": "oraciones imperativas y exclamativas",
                "angles": [
                    ("imperativos.corpus",
                     "Genera 15 oraciones imperativas en español (afirmativas y negativas, tú/usted/vosotros/nosotros). "
                     "Incluye imperativos con clíticos (dámelo, no te vayas). "
                     "Todas las anotaciones en español."),
                    ("exclamativas.corpus",
                     "Genera 15 oraciones exclamativas en español con qué, cómo, cuánto, vaya. "
                     "Anota la estructura exclamativa. Todas las anotaciones en español."),
                    ("desiderativas_dubitativas.corpus",
                     "Genera 15 oraciones desiderativas (¡Ojalá llueva! ¡Que tengas suerte!) "
                     "y dubitativas en español. Anota el modo subjuntivo y su valor. "
                     "Todas las anotaciones en español."),
                ],
            },
        },
    },
    "italian": {
        "label": "Italian",
        "instruction_lang": "in italiano",
        "categories": {
            "dichiarative_semplici": {
                "description": "frasi dichiarative semplici",
                "angles": [
                    ("presente_indicativo.corpus",
                     "Genera 15 frasi dichiarative in italiano al presente indicativo. "
                     "Usa strutture SV e SVC. Varia i soggetti: nomi, pronomi, nomi propri. "
                     "Annota tutte le parole in italiano con la categoria grammaticale e la funzione sintattica."),
                    ("passato_prossimo_imperfetto.corpus",
                     "Genera 15 frasi in italiano al passato prossimo e all'imperfetto. "
                     "Alterna azioni compiute (passato prossimo) e stati o azioni abituali (imperfetto). "
                     "Tutte le annotazioni in italiano."),
                    ("futuro_condizionale.corpus",
                     "Genera 15 frasi in italiano al futuro semplice e al condizionale presente. "
                     "Includi previsioni, promesse e ipotesi. Tutte le annotazioni in italiano."),
                ],
            },
            "complemento_oggetto": {
                "description": "frasi con complemento oggetto diretto e indiretto",
                "angles": [
                    ("oggetto_diretto.corpus",
                     "Genera 15 frasi in italiano con verbi transitivi e complemento oggetto diretto. "
                     "Usa verbi variati (mangiare, vedere, amare, prendere, leggere, scrivere). "
                     "Indica chiaramente il complemento oggetto. Tutte le annotazioni in italiano."),
                    ("oggetto_indiretto.corpus",
                     "Genera 15 frasi in italiano con complemento oggetto indiretto introdotto da 'a' o 'di'. "
                     "Usa verbi come dare, dire, inviare, mostrare, spiegare, parlare. "
                     "Tutte le annotazioni in italiano."),
                    ("pronomi_clitici.corpus",
                     "Genera 15 frasi in italiano con pronomi clitici (lo, la, li, le, gli, le, mi, ti, ci, vi). "
                     "Includi casi di pronomi combinati (glielo, me lo, te la). "
                     "Annota persona, numero, genere e funzione. Tutte le annotazioni in italiano."),
                ],
            },
            "subordinate": {
                "description": "frasi subordinate e relative",
                "angles": [
                    ("relative.corpus",
                     "Genera 15 frasi in italiano con una proposizione relativa "
                     "(che, cui, il quale, dove, chi). "
                     "Annota il pronome relativo, il suo antecedente e il tipo di relativa. "
                     "Tutte le annotazioni in italiano."),
                    ("congiunzioni_subordinanti.corpus",
                     "Genera 15 frasi in italiano con proposizioni subordinate avverbiali "
                     "(perché, sebbene, quando, se, affinché, prima che, ecc.). "
                     "Annota il tipo di subordinata e il modo del verbo. Tutte le annotazioni in italiano."),
                    ("infinitive_gerundive.corpus",
                     "Genera 15 frasi in italiano con costruzioni infinitive e gerundive "
                     "(volere fare, continuare a fare, pur essendo, dopo aver fatto). "
                     "Tutte le annotazioni in italiano."),
                ],
            },
            "interrogative": {
                "description": "frasi interrogative dirette e indirette",
                "angles": [
                    ("interrogative_totali.corpus",
                     "Genera 15 frasi interrogative totali in italiano (risposta sì/no). "
                     "Includi variazioni di intonazione e ordine delle parole. "
                     "Tutte le annotazioni in italiano."),
                    ("interrogative_parziali.corpus",
                     "Genera 15 frasi interrogative parziali in italiano con chi, che cosa, dove, "
                     "quando, come, perché, quanto, quale. "
                     "Annota il pronome interrogativo e la sua funzione. Tutte le annotazioni in italiano."),
                    ("interrogative_indirette.corpus",
                     "Genera 15 frasi in italiano con interrogative indirette "
                     "(Non so se..., Mi chiedo quando..., Dimmi cosa...). "
                     "Tutte le annotazioni in italiano."),
                ],
            },
            "negazioni": {
                "description": "costruzioni negative",
                "angles": [
                    ("negazione_semplice.corpus",
                     "Genera 15 frasi negative semplici in italiano con 'non' prima del verbo. "
                     "Includi tempi verbali diversi. Tutte le annotazioni in italiano."),
                    ("parole_negative.corpus",
                     "Genera 15 frasi in italiano con parole negative "
                     "(niente, nessuno, mai, neanche, né...né, affatto). "
                     "Annota la concordanza negativa. Tutte le annotazioni in italiano."),
                    ("negazione_congiuntivo.corpus",
                     "Genera 15 frasi in italiano con negazione e congiuntivo "
                     "(non credo che, non è possibile che, senza che, a meno che). "
                     "Tutte le annotazioni in italiano."),
                ],
            },
            "pronomi": {
                "description": "uso dei pronomi e riferimento",
                "angles": [
                    ("pronomi_personali.corpus",
                     "Genera 15 frasi in italiano con pronomi personali soggetto e complemento "
                     "(io, tu, lui/lei, noi, voi, loro + forme toniche). "
                     "Annota persona, numero, genere e funzione. Tutte le annotazioni in italiano."),
                    ("pronomi_dimostrativi_possessivi.corpus",
                     "Genera 15 frasi in italiano con pronomi dimostrativi (questo, quello, ciò) "
                     "e possessivi (il mio, il tuo, il suo, il nostro). "
                     "Tutte le annotazioni in italiano."),
                    ("pronomi_indefiniti.corpus",
                     "Genera 15 frasi in italiano con pronomi indefiniti "
                     "(qualcuno, nessuno, tutto, ognuno, chiunque, qualcosa, poco, molto). "
                     "Tutte le annotazioni in italiano."),
                ],
            },
            "passivo_riflessivo": {
                "description": "voce passiva e costruzioni riflessive",
                "angles": [
                    ("voce_passiva.corpus",
                     "Genera 15 frasi in italiano alla voce passiva (essere + participio passato). "
                     "Includi diversi tempi verbali e il complemento d'agente (da + agente). "
                     "Tutte le annotazioni in italiano."),
                    ("verbi_riflessivi.corpus",
                     "Genera 15 frasi in italiano con verbi riflessivi propri, reciproci e apparenti "
                     "(lavarsi, vedersi, sentirsi, alzarsi). "
                     "Annota il tipo di riflessivo. Tutte le annotazioni in italiano."),
                    ("si_impersonale_passivante.corpus",
                     "Genera 15 frasi in italiano con si impersonale e si passivante "
                     "(si dice che, si vedono molte stelle). "
                     "Tutte le annotazioni in italiano."),
                ],
            },
            "imperativi_esclamativi": {
                "description": "frasi imperative ed esclamative",
                "angles": [
                    ("imperativi.corpus",
                     "Genera 15 frasi imperative in italiano (affermative e negative, tu/Lei/noi/voi). "
                     "Includi imperativi con pronomi clitici (dammelo, non farlo, alzati). "
                     "Tutte le annotazioni in italiano."),
                    ("esclamative.corpus",
                     "Genera 15 frasi esclamative in italiano con che, come, quanto, accidenti. "
                     "Annota la struttura esclamativa. Tutte le annotazioni in italiano."),
                    ("congiuntivo_esortativo.corpus",
                     "Genera 15 frasi in italiano con congiuntivo esortativo e ottativo "
                     "(Che venga! Magari potessi! Che Dio ti benedica!). "
                     "Tutte le annotazioni in italiano."),
                ],
            },
        },
    },
    "portuguese": {
        "label": "Portuguese",
        "instruction_lang": "em português",
        "categories": {
            "declarativas_simples": {
                "description": "frases declarativas simples",
                "angles": [
                    ("presente_indicativo.corpus",
                     "Gera 15 frases declarativas em português no presente do indicativo. "
                     "Usa estruturas SV e SVC. Varia os sujeitos: substantivos, pronomes, nomes próprios. "
                     "Anota todas as palavras em português com a categoria gramatical e a função sintática."),
                    ("preterito_imperfeito.corpus",
                     "Gera 15 frases em português no pretérito perfeito e imperfeito do indicativo. "
                     "Alterna ações concluídas (perfeito) e estados ou ações habituais (imperfeito). "
                     "Todas as anotações em português."),
                    ("futuro_condicional.corpus",
                     "Gera 15 frases em português no futuro do presente e no condicional. "
                     "Inclui previsões, promessas e hipóteses. Todas as anotações em português."),
                ],
            },
            "objeto_direto_indireto": {
                "description": "frases com objeto direto e indireto",
                "angles": [
                    ("objeto_direto.corpus",
                     "Gera 15 frases em português com verbos transitivos e objeto direto (OD). "
                     "Usa verbos variados. Identifica claramente o OD na anotação. "
                     "Todas as anotações em português."),
                    ("objeto_indireto.corpus",
                     "Gera 15 frases em português com objeto indireto (OI) introduzido por 'a' ou 'para'. "
                     "Usa verbos como dar, dizer, enviar, mostrar, explicar, falar. "
                     "Todas as anotações em português."),
                    ("pronomes_obliquos.corpus",
                     "Gera 15 frases em português com pronomes oblíquos átonos e tônicos "
                     "(me, te, se, nos, vos, o, a, os, as, lhe, lhes, mim, ti, ele, ela). "
                     "Anota pessoa, número, género e função. Todas as anotações em português."),
                ],
            },
            "subordinadas": {
                "description": "orações subordinadas e relativas",
                "angles": [
                    ("relativas.corpus",
                     "Gera 15 frases em português com uma oração relativa "
                     "(que, quem, cujo, onde, o qual). "
                     "Anota o pronome relativo, o seu antecedente e o tipo de relativa. "
                     "Todas as anotações em português."),
                    ("conjuncoes_subordinativas.corpus",
                     "Gera 15 frases em português com orações subordinadas adverbiais "
                     "(porque, embora, quando, se, para que, antes que, etc.). "
                     "Anota o tipo de subordinada e o modo do verbo. Todas as anotações em português."),
                    ("infinitivo_gerundio.corpus",
                     "Gera 15 frases em português com construções de infinitivo e gerúndio "
                     "(querer fazer, continuar fazendo, ao chegar, depois de ter feito). "
                     "Todas as anotações em português."),
                ],
            },
            "interrogativas": {
                "description": "frases interrogativas diretas e indiretas",
                "angles": [
                    ("interrogativas_totais.corpus",
                     "Gera 15 frases interrogativas totais em português (resposta sim/não). "
                     "Inclui variações de entonação e ordem das palavras. "
                     "Todas as anotações em português."),
                    ("interrogativas_parciais.corpus",
                     "Gera 15 frases interrogativas parciais em português com quem, o que, onde, "
                     "quando, como, por que, quanto, qual. "
                     "Anota o pronome interrogativo e a sua função. Todas as anotações em português."),
                    ("interrogativas_indiretas.corpus",
                     "Gera 15 frases em português com interrogativas indiretas "
                     "(Não sei se..., Pergunto-me quando..., Diz-me o que...). "
                     "Todas as anotações em português."),
                ],
            },
            "negacoes": {
                "description": "construções negativas",
                "angles": [
                    ("negacao_simples.corpus",
                     "Gera 15 frases negativas simples em português com 'não' antes do verbo. "
                     "Inclui diferentes tempos verbais. Todas as anotações em português."),
                    ("palavras_negativas.corpus",
                     "Gera 15 frases em português com palavras negativas "
                     "(nada, ninguém, nunca, jamais, nenhum, nem...nem, tampouco). "
                     "Anota a concordância negativa. Todas as anotações em português."),
                    ("negacao_subjuntivo.corpus",
                     "Gera 15 frases em português com negação e subjuntivo "
                     "(não acredito que, não é possível que, sem que, a não ser que). "
                     "Todas as anotações em português."),
                ],
            },
            "pronomes": {
                "description": "uso de pronomes e referência",
                "angles": [
                    ("pronomes_pessoais.corpus",
                     "Gera 15 frases em português com pronomes pessoais sujeito e complemento "
                     "(eu, tu, ele/ela, nós, vós, eles/elas + formas tônicas). "
                     "Anota pessoa, número, género e função. Todas as anotações em português."),
                    ("pronomes_demonstrativos_possessivos.corpus",
                     "Gera 15 frases em português com pronomes demonstrativos (este, esse, aquele e formas) "
                     "e possessivos (meu, teu, seu, nosso, vosso). "
                     "Todas as anotações em português."),
                    ("pronomes_indefinidos.corpus",
                     "Gera 15 frases em português com pronomes indefinidos "
                     "(alguém, ninguém, tudo, cada, qualquer, ambos, algo, nada). "
                     "Todas as anotações em português."),
                ],
            },
            "passiva_reflexiva": {
                "description": "voz passiva e construções reflexivas",
                "angles": [
                    ("voz_passiva.corpus",
                     "Gera 15 frases em português na voz passiva (ser + particípio passado). "
                     "Inclui diferentes tempos verbais e o agente da passiva (por + agente). "
                     "Todas as anotações em português."),
                    ("verbos_reflexivos.corpus",
                     "Gera 15 frases em português com verbos reflexivos, recíprocos e pronominais "
                     "(lavar-se, ver-se, sentir-se, levantar-se). "
                     "Anota o tipo de reflexivo. Todas as anotações em português."),
                    ("se_apassivador_indefinido.corpus",
                     "Gera 15 frases em português com se apassivador e se indefinido "
                     "(vende-se casas, fala-se português, diz-se que). "
                     "Todas as anotações em português."),
                ],
            },
            "imperativos_exclamativos": {
                "description": "frases imperativas e exclamativas",
                "angles": [
                    ("imperativos.corpus",
                     "Gera 15 frases imperativas em português (afirmativas e negativas, tu/você/nós/vocês). "
                     "Inclui imperativos com pronomes clíticos (dá-me, não o faças, levanta-te). "
                     "Todas as anotações em português."),
                    ("exclamativas.corpus",
                     "Gera 15 frases exclamativas em português com que, como, quanto, quanta. "
                     "Anota a estrutura exclamativa. Todas as anotações em português."),
                    ("subjuntivo_optativo.corpus",
                     "Gera 15 frases em português com subjuntivo optativo e desiderativo "
                     "(Oxalá venha! Que Deus te abençoe! Tomara que...). "
                     "Todas as anotações em português."),
                ],
            },
        },
    },
}


def build_prompt(lang_key: str, info: dict, category: str, angle_prompt: str) -> str:
    return (
        f"Language: {info['label']} | Category: {category} | "
        f"Annotations must be written {info['instruction_lang']}.\n\n"
        f"{angle_prompt}\n\n"
        f"{FORMAT}"
    )


def main():
    total_dirs = 0
    total_prompts = 0

    for lang_key, info in LANGUAGES.items():
        for category, cat_info in info["categories"].items():
            dirpath = os.path.join(CORPUS_DIR, lang_key, category)
            os.makedirs(dirpath, exist_ok=True)

            lines = []
            for filename, angle_prompt in cat_info["angles"]:
                prompt = build_prompt(lang_key, info, category, angle_prompt)
                prompt_oneline = prompt.replace("\n", " | ")
                lines.append(f"{filename} {prompt_oneline}")

            prompts_path = os.path.join(dirpath, "prompts.txt")
            with open(prompts_path, "w") as f:
                f.write("\n".join(lines) + "\n")

            total_dirs += 1
            total_prompts += len(lines)
            print(f"  {lang_key}/{category}/prompts.txt ({len(lines)} prompts)")

    print(f"\nDone! Created {total_dirs} directories with {total_prompts} total prompts.")


if __name__ == "__main__":
    main()
