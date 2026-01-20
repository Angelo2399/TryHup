from fastapi import APIRouter, status

router = APIRouter(
    prefix="/meta",
    tags=["meta"],
)


@router.get(
    "/creator-categories",
    status_code=status.HTTP_200_OK,
)
def get_creator_categories():
    return {
        "categories": [
            {
                "key": "standard_creator",
                "label": "Creator standard",
                "description": (
                    "Intrattenimento, lifestyle, gaming, fitness non medico, "
                    "vlog e divulgazione leggera. Contenuti per adulti e "
                    "promozione OnlyFans non sono ammessi."
                ),
                "risk_level": "low",
                "verification_required": False,
                "badge": None,
            },
            {
                "key": "science_educational",
                "label": "Scienza divulgativa",
                "description": (
                    "Divulgazione culturale e scientifica non applicativa: "
                    "storia, scienze umane, fisica, biologia non clinica, "
                    "chimica teorica, matematica, astronomia."
                ),
                "risk_level": "medium",
                "verification_required": False,
                "badge": None,
            },
            {
                "key": "professional_sensitive",
                "label": "Professioni sensibili",
                "description": (
                    "Contenuti ad alto impatto sulla vita delle persone: "
                    "medicina, psicologia, economia e finanza, "
                    "temi giuridici, ingegneria, chimica applicata, "
                    "nutrizione clinica e sicurezza."
                ),
                "risk_level": "high",
                "verification_required": True,
                "badge": "verified_professional",
            },
            {
                "key": "social_opinion",
                "label": "Impatto sociale / Opinione",
                "description": (
                    "Opinioni e analisi su politica, società, geopolitica, "
                    "attualità e media. Non include consulenza professionale."
                ),
                "risk_level": "medium",
                "verification_required": False,
                "badge": None,
            },
            {
                "key": "political_in_office",
                "label": "Personalità politica in carica",
                "description": (
                    "Persone che ricoprono incarichi politici istituzionali "
                    "(locali, nazionali o europei). Trasparenza obbligatoria."
                ),
                "risk_level": "high",
                "verification_required": True,
                "badge": "political_in_office",
            },
            {
                "key": "public_figure",
                "label": "Personaggio pubblico",
                "description": (
                    "Celebrità o figure pubbliche con notorietà esterna alla "
                    "piattaforma. Il badge è facoltativo e non comporta privilegi."
                ),
                "risk_level": "medium",
                "verification_required": False,
                "badge": "public_figure",
            },
        ],
        "content_policies": {
            "anti_copy_paste": (
                "Il copia-incolla integrale di contenuti dal web non è consentito. "
                "Sono ammessi solo contenuti originali, rielaborazioni personali "
                "o citazioni brevi accompagnate da commento."
            )
        },
    }
