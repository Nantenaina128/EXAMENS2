import re
import math
import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ============================================================
# TEO AMIN'NY LOKO SY NY STYLE (couleurs)
# ============================================================

# Eto no apetraka ny loko rehetra, mba mora ovaina
# rehefa te hanova ny endrika ny interface ianao a.
COULEUR_FOND = "#eef2f7"
COULEUR_ACCENT = "#2563eb"
COULEUR_ACCENT_SURVOL = "#1d4ed8"
COULEUR_COURBE = "#2563eb"
COULEUR_TEXTE = "#1f2937"

# Valeur par défaut ataon'ny champ rehefa miseho, ka tsy
# mila manoratra zavatra rehetra ianao vao hijery ny courbe.
VALEURS_PAR_DEFAUT = {
    "a": "1",
    "b": "0",
    "c": "0",
    "n": "2"
}

# Ny paramètres ilain'ny type de fonction tsirairay.
# (anarana ny paramètre, soratra aseho eo amin'ny interface)
PARAMETRES = {
    "Linéaire": [
        ("a", "Coefficient a")
    ],
    "Affine": [
        ("a", "Coefficient a"),
        ("b", "Constante b")
    ],
    "Polynôme": [
        ("a", "Coefficient a"),
        ("b", "Coefficient b"),
        ("c", "Constante c")
    ],
    "Puissance": [
        ("a", "Coefficient a"),
        ("n", "Exposant n")
    ],
    "Exponentielle": [
        ("a", "Coefficient a"),
        ("b", "Coefficient b"),
        ("c", "Constante c")
    ],
    "Logarithmique": [
        ("a", "Coefficient a"),
        ("b", "Constante b")
    ]
}

# Ireo fonction mathématiques azon'ny calculatrice ampiasaina.
# Tsy misy afa-tsy ireto, mba tsy hisy code hafa mandeha ao a.
FONCTIONS_AUTORISEES = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "pi": math.pi,
    "e": math.e
}

# Fenêtre-n'ny calculatrice (None raha mbola tsy misokatra),
# ampiasaina mba tsy hisokatra imbetsaka ilay izy.
fenetre_calculatrice = None


# ============================================================
# FIKAJIANA NY VALEUR-N'NY FONCTION
# ============================================================

# Eto no anaovana ny calcul an'ilay fonction arakaraka
# ny type de fonction sy ny valeur nampidirin'ny utilisateur.
def calculer_fonction(x, type_fonction, valeurs):

    # Atao mangina ny avertissement numpy (division par zéro,
    # overflow...) satria hojerena ambany ny valeur tsy mety a.
    with np.errstate(all="ignore"):

        if type_fonction == "Linéaire":
            y = valeurs["a"] * x

        elif type_fonction == "Affine":
            y = valeurs["a"] * x + valeurs["b"]

        elif type_fonction == "Polynôme":
            y = (
                valeurs["a"] * x**2
                + valeurs["b"] * x
                + valeurs["c"]
            )

        elif type_fonction == "Puissance":
            y = valeurs["a"] * x**valeurs["n"]

        elif type_fonction == "Exponentielle":
            y = (
                valeurs["a"] * np.exp(valeurs["b"] * x)
                + valeurs["c"]
            )

        elif type_fonction == "Logarithmique":
            y = valeurs["a"] * np.log(x) + valeurs["b"]

        else:
            raise ValueError(
                f"Type de fonction inconnu : {type_fonction}"
            )

    # Ny inf (infini) dia atao nan mba tsy hanimba ny graphique.
    return np.where(np.isfinite(y), y, np.nan)


# ============================================================
# FANAMBOARANA NY EXPRESSION MATHEMATIQUE
# ============================================================

# Mamadika ny nombre ho soratra madio: 2.0 dia "2", 0.5 dia "0.5".
def formater_nombre(valeur):
    return f"{valeur:g}"


# Manampy signe + na - alohan'ny terme, ka tsy hisy "+ -3" ratsy tarehy a.
def terme_signe(valeur, suffixe=""):

    if valeur < 0:
        return f" - {formater_nombre(-valeur)}{suffixe}"

    return f" + {formater_nombre(valeur)}{suffixe}"


# Eto no anamboarana ny formule mba ho mora vakina
# ary aseho eo amin'ny graphique.
def obtenir_expression(type_fonction, valeurs):

    a = formater_nombre(valeurs.get("a", 0))

    if type_fonction == "Linéaire":
        return f"f(x) = {a}x"

    elif type_fonction == "Affine":
        return f"f(x) = {a}x" + terme_signe(valeurs["b"])

    elif type_fonction == "Polynôme":
        return (
            f"f(x) = {a}x²"
            + terme_signe(valeurs["b"], "x")
            + terme_signe(valeurs["c"])
        )

    elif type_fonction == "Puissance":
        return f"f(x) = {a}x^{formater_nombre(valeurs['n'])}"

    elif type_fonction == "Exponentielle":
        return (
            f"f(x) = {a}e^({formater_nombre(valeurs['b'])}x)"
            + terme_signe(valeurs["c"])
        )

    elif type_fonction == "Logarithmique":
        return f"f(x) = {a}ln(x)" + terme_signe(valeurs["b"])


# ============================================================
# INFORMATIONS MOMBA NY FONCTION
# ============================================================

# Ity fonction ity no mitazona ny information momba ny
# forme générale sy domaine-n'ilay fonction voafidy.
def obtenir_informations(type_fonction):

    informations = {

        "Linéaire": {
            "forme": "f(x) = ax",
            "domaine": "ℝ",
            "description": "Fonction linéaire"
        },

        "Affine": {
            "forme": "f(x) = ax + b",
            "domaine": "ℝ",
            "description": "Fonction affine"
        },

        "Polynôme": {
            "forme": "f(x) = ax² + bx + c",
            "domaine": "ℝ",
            "description": "Polynôme du second degré"
        },

        "Puissance": {
            "forme": "f(x) = axⁿ",
            "domaine": "Selon la valeur de n",
            "description": "Fonction puissance"
        },

        "Exponentielle": {
            "forme": "f(x) = ae^(bx) + c",
            "domaine": "ℝ",
            "description": "Fonction exponentielle"
        },

        "Logarithmique": {
            "forme": "f(x) = a ln(x) + b",
            "domaine": "]0 ; +∞[",
            "description": "Fonction logarithmique"
        }
    }

    return informations[type_fonction]


# ============================================================
# FAMARAN'NY VALEUR NAMPIDIRINA
# ============================================================

# Maka ny valeur rehetra ao amin'ny champ ary mamadika azy ho nombre.
# Raha tsy nombre dia mipoaka ValueError, ka ilay messagebox no miseho.
def lire_valeurs():

    valeurs = {}

    for nom, champ in champs.items():

        # Azo soratana amin'ny virgule koa (2,5), ovaina ho point a.
        texte = champ.get().strip().replace(",", ".")

        valeurs[nom] = float(texte)

    return valeurs


# ============================================================
# AFFICHAGE-N'NY GRAPHIQUE
# ============================================================

# Eto no maka ny valeur rehetra nampidirina, manao calcul
# ary avy eo mampiseho ny courbe ao amin'ny interface.
def afficher_graphique():

    try:
        type_fonction = type_fonction_var.get()
        valeurs = lire_valeurs()

        # Mamorona valeur ho an'ny axe x.
        x = np.linspace(-10, 10, 1000)

        # Tsy afaka manao ln(x) amin'ny x <= 0.
        # Ka manomboka amin'ny 0.01 isika.
        if type_fonction == "Logarithmique":
            x = np.linspace(0.01, 10, 1000)

        elif type_fonction == "Puissance":

            n = valeurs["n"]

            # Raha exposant tsy entier dia mety tsy hisy valeur réelle
            # rehefa x négatif (na n négatif aza), ka x > 0 ihany no raisina.
            if not float(n).is_integer():
                x = np.linspace(0.01, 10, 1000)

            # Raha exposant entier négatif dia tsy azo ampiasaina x = 0.
            # Asiana nan eo afovoany mba tsy hampitohy ny sampana roa
            # amin'ny tsipika mitsangana ratsy tarehy.
            elif n < 0:
                x = np.concatenate([
                    np.linspace(-10, -0.01, 500),
                    [np.nan],
                    np.linspace(0.01, 10, 500)
                ])

        # Calcul-na f(x).
        y = calculer_fonction(
            x,
            type_fonction,
            valeurs
        )

        expression = obtenir_expression(
            type_fonction,
            valeurs
        )

        # Esorina aloha ny graphique taloha.
        ax.clear()

        # Atao ny dessin an'ilay courbe.
        ax.plot(
            x,
            y,
            color=COULEUR_COURBE,
            linewidth=2.2,
            label=expression
        )

        # Axe horizontal sy axe vertical.
        ax.axhline(
            0,
            color="#6b7280",
            linewidth=1
        )

        ax.axvline(
            0,
            color="#6b7280",
            linewidth=1
        )

        # Raha exposant négatif dia mitsambikina be ny courbe
        # akaikin'ny 0, ka voafetra ny axe y mba hiseho tsara a.
        if type_fonction == "Puissance" and valeurs["n"] < 0:
            limite = max(10, 10 * abs(valeurs["a"]))
            ax.set_ylim(-limite, limite)

        # Titre-n'ny graphique.
        ax.set_title(
            expression,
            fontsize=13,
            fontweight="bold",
            color=COULEUR_TEXTE
        )

        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")

        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(loc="best")

        # Atao refresh ilay graphique ao amin'ny fenêtre.
        canvas.draw()

        # Ovana koa ny information eo amin'ny gauche.
        informations = obtenir_informations(
            type_fonction
        )

        texte_information.set(
            f"Forme générale : {informations['forme']}\n"
            f"Domaine : {informations['domaine']}\n"
            f"Fonction tracée : {expression}"
        )

    except ValueError:

        messagebox.showerror(
            "Erreur",
            "Ampidiro nombre ihany azafady."
        )

    except Exception as erreur:

        messagebox.showerror(
            "Erreur",
            str(erreur)
        )


# ============================================================
# REHEFA MANOVA TYPE DE FONCTION
# ============================================================

# Rehefa misafidy fonction hafa ao amin'ny liste dia
# ovaina automatique koa ny paramètres tokony hiseho.
def changer_fonction(event=None):

    # Fafana aloha ny ancien paramètres.
    for widget in cadre_parametres.winfo_children():
        widget.destroy()

    champs.clear()

    # Fafana koa ny information taloha, fa tsy mifanaraka
    # amin'ny fonction vaovao intsony izy ireny a.
    texte_information.set("")

    type_fonction = type_fonction_var.get()

    informations = obtenir_informations(
        type_fonction
    )

    # Aseho ny anaran'ilay fonction.
    ttk.Label(
        cadre_parametres,
        text=informations["description"],
        font=("Arial", 12, "bold")
    ).pack(pady=(10, 5))

    # Aseho eto aloha ny forme générale,
    # vao avy eo ny champ-na paramètres.
    ttk.Label(
        cadre_parametres,
        text=informations["forme"],
        font=("Arial", 13)
    ).pack(pady=5)

    # Aseho koa ny domaine de définition.
    ttk.Label(
        cadre_parametres,
        text=f"Domaine : {informations['domaine']}"
    ).pack(pady=(0, 10))

    # Paramètres arakaraka ny type de fonction.
    # Ny dictionnaire PARAMETRES no mamaritra izay ilaina,
    # ka tsy mila elif maro intsony isika a.
    for nom, texte in PARAMETRES[type_fonction]:
        creer_champ(nom, texte)


# ============================================================
# CREATION-N'NY CHAMP DE SAISIE
# ============================================================

# Fonction iray ampiasaina mba tsy hiverimberina ny code
# rehefa mamorona champ vaovao.
def creer_champ(nom, texte):

    ligne = ttk.Frame(
        cadre_parametres
    )

    ligne.pack(
        pady=5,
        padx=10
    )

    ttk.Label(
        ligne,
        text=texte,
        width=18
    ).pack(side="left")

    entree = ttk.Entry(
        ligne,
        width=15
    )

    # Asiana valeur par défaut mba tsy foana ny champ.
    entree.insert(
        0,
        VALEURS_PAR_DEFAUT.get(nom, "1")
    )

    # Manindry Entrée dia mandeha avy hatrany ny graphique.
    entree.bind(
        "<Return>",
        lambda event: afficher_graphique()
    )

    entree.pack(
        side="left"
    )

    champs[nom] = entree


# ============================================================
# CALCULATRICE SCIENTIFIQUE
# ============================================================

# Manokatra fenêtre vaovao misy calculatrice scientifique.
def ouvrir_calculatrice():

    global fenetre_calculatrice

    # Raha efa misokatra ilay calculatrice dia asongadina fotsiny,
    # fa tsy mamorona iray hafa intsony.
    if (
        fenetre_calculatrice is not None
        and fenetre_calculatrice.winfo_exists()
    ):
        fenetre_calculatrice.lift()
        fenetre_calculatrice.focus_force()
        return

    calculatrice = tk.Toplevel(
        fenetre
    )

    fenetre_calculatrice = calculatrice

    calculatrice.title(
        "Calculatrice scientifique"
    )

    calculatrice.geometry(
        "400x560"
    )

    calculatrice.resizable(
        False,
        False
    )

    calculatrice.configure(
        background=COULEUR_FOND
    )

    expression = tk.StringVar()

    entree = ttk.Entry(
        calculatrice,
        textvariable=expression,
        font=("Arial", 18),
        justify="right"
    )

    entree.pack(
        padx=10,
        pady=15,
        fill="x",
        ipady=8
    )

    # Mivantana ao amin'ny entrée avy hatrany, ary
    # Entrée = "=" mba mora ny fampiasana clavier a.
    entree.focus_set()

    calculatrice.bind(
        "<Return>",
        lambda event: calculer_expression(
            "=",
            expression
        )
    )

    cadre = ttk.Frame(
        calculatrice
    )

    cadre.pack(
        padx=10,
        pady=10,
        fill="both",
        expand=True
    )

    # Ny boutons rehetra: (soratra, valeur ampidirina, andalana,
    # tsanganana, isan'ny tsanganana raisiny, style).
    # Ny "=" dia mitaingina andalana roa mba ho miavaka a.
    boutons = [

        ("sin", "sin(", 0, 0, 1, "Op.TButton"),
        ("cos", "cos(", 0, 1, 1, "Op.TButton"),
        ("tan", "tan(", 0, 2, 1, "Op.TButton"),
        ("ln", "log(", 0, 3, 1, "Op.TButton"),

        ("√", "sqrt(", 1, 0, 1, "Op.TButton"),
        ("π", "pi", 1, 1, 1, "Op.TButton"),
        ("e", "e", 1, 2, 1, "Op.TButton"),
        ("C", "C", 1, 3, 1, "Clear.TButton"),

        ("(", "(", 2, 0, 1, "Op.TButton"),
        (")", ")", 2, 1, 1, "Op.TButton"),
        ("/", "/", 2, 2, 1, "Op.TButton"),
        ("*", "*", 2, 3, 1, "Op.TButton"),

        ("7", "7", 3, 0, 1, "Chiffre.TButton"),
        ("8", "8", 3, 1, 1, "Chiffre.TButton"),
        ("9", "9", 3, 2, 1, "Chiffre.TButton"),
        ("-", "-", 3, 3, 1, "Op.TButton"),

        ("4", "4", 4, 0, 1, "Chiffre.TButton"),
        ("5", "5", 4, 1, 1, "Chiffre.TButton"),
        ("6", "6", 4, 2, 1, "Chiffre.TButton"),
        ("+", "+", 4, 3, 1, "Op.TButton"),

        ("1", "1", 5, 0, 1, "Chiffre.TButton"),
        ("2", "2", 5, 1, 1, "Chiffre.TButton"),
        ("3", "3", 5, 2, 1, "Chiffre.TButton"),

        ("0", "0", 6, 0, 2, "Chiffre.TButton"),
        (".", ".", 6, 2, 1, "Chiffre.TButton"),

        ("=", "=", 5, 3, 1, "Egal.TButton")
    ]

    # Ny "=" no manana rowspan=2 (andalana 5 sy 6).
    for texte, valeur, ligne, colonne, span, style in boutons:

        ttk.Button(
            cadre,
            text=texte,
            style=style,
            command=lambda v=valeur:
            calculer_expression(
                v,
                expression
            )
        ).grid(
            row=ligne,
            column=colonne,
            columnspan=span,
            rowspan=2 if valeur == "=" else 1,
            sticky="nsew",
            padx=3,
            pady=3,
            ipady=6
        )

    # Mba hitovy ny habeny ny tsanganana sy andalana rehetra.
    for i in range(4):
        cadre.columnconfigure(i, weight=1, uniform="col")

    for i in range(7):
        cadre.rowconfigure(i, weight=1, uniform="lig")


# ============================================================
# CALCUL-N'NY EXPRESSION AO AMIN'NY CALCULATRICE
# ============================================================

# Eto no anaovana ny opération rehefa manindry bouton
# ao amin'ny calculatrice ny utilisateur.
def calculer_expression(valeur, expression):

    if valeur == "C":

        expression.set("")

    elif valeur == "=":

        try:

            texte = expression.get().strip()

            # Tsy misy azo kajiana raha foana ny champ a.
            if not texte:
                return

            # Fanamarinana aloha: tsy azo ny litera/mot tsy ao
            # amin'ny lisitra, ary tsy azo ny caractère hafahafa
            # (toy ny "_") mba tsy hisy code ratsy mivoaka.
            mots = re.findall(r"[A-Za-z_]+", texte)

            if any(mot not in FONCTIONS_AUTORISEES for mot in mots):
                raise ValueError("Mot non autorisé")

            if not re.fullmatch(r"[0-9A-Za-z+\-*/().,\s]+", texte):
                raise ValueError("Caractère non autorisé")

            # eval() eto dia voafetra amin'ireo fonction
            # mathématiques izay tena ilaintsika ihany.
            resultat = eval(
                texte,
                {
                    "__builtins__": {},
                    **FONCTIONS_AUTORISEES
                }
            )

            # Raha tsy nombre réel ny valiny (complexe, infini...)
            # dia atao Erreur.
            if not isinstance(resultat, (int, float)):
                raise ValueError("Résultat invalide")

            if isinstance(resultat, float):

                if not math.isfinite(resultat):
                    raise ValueError("Résultat invalide")

                # .12g mba tsy hiseho 0.30000000000000004 ary
                # 4.0 dia "4" fotsiny.
                expression.set(f"{resultat:.12g}")

            else:
                expression.set(str(resultat))

        except Exception:

            expression.set(
                "Erreur"
            )

    else:

        # Ampiana ao amin'ny expression ilay bouton
        # notsindrian'ny utilisateur.
        actuel = expression.get()

        # Raha "Erreur" no eo dia fafana aloha, fa tsy
        # hiteraka "Erreur5" izany a.
        if actuel == "Erreur":
            actuel = ""

        expression.set(
            actuel + valeur
        )


# ============================================================
# INTERFACE PRINCIPALE
# ============================================================

fenetre = tk.Tk()

fenetre.title(
    "Étude d'une fonction"
)

fenetre.geometry(
    "1200x750"
)

fenetre.minsize(
    950,
    650
)

fenetre.configure(
    background=COULEUR_FOND
)


# ------------------------------------------------------------
# STYLE ttk (endrika ny widget rehetra)
# ------------------------------------------------------------

# Ny thème "clam" no mamela ny loko hovana tsara,
# fa ny thème par défaut dia mavesatra ovaina kokoa e.
style = ttk.Style(fenetre)
style.theme_use("clam")

style.configure(
    "TFrame",
    background=COULEUR_FOND
)

style.configure(
    "TLabel",
    background=COULEUR_FOND,
    foreground=COULEUR_TEXTE,
    font=("Arial", 10)
)

style.configure(
    "TLabelframe",
    background=COULEUR_FOND
)

style.configure(
    "TLabelframe.Label",
    background=COULEUR_FOND,
    foreground=COULEUR_ACCENT,
    font=("Arial", 10, "bold")
)

# Bouton principal (Afficher le graphique...).
style.configure(
    "Accent.TButton",
    background=COULEUR_ACCENT,
    foreground="white",
    font=("Arial", 11, "bold"),
    borderwidth=0,
    padding=6
)

style.map(
    "Accent.TButton",
    background=[("active", COULEUR_ACCENT_SURVOL)]
)

# Boutons an'ny calculatrice: chiffre, opérateur, égal, clear.
style.configure(
    "Chiffre.TButton",
    background="white",
    font=("Arial", 12),
    borderwidth=1
)

style.map(
    "Chiffre.TButton",
    background=[("active", "#e5e7eb")]
)

style.configure(
    "Op.TButton",
    background="#dbeafe",
    font=("Arial", 12),
    borderwidth=1
)

style.map(
    "Op.TButton",
    background=[("active", "#bfdbfe")]
)

style.configure(
    "Egal.TButton",
    background=COULEUR_ACCENT,
    foreground="white",
    font=("Arial", 14, "bold"),
    borderwidth=1
)

style.map(
    "Egal.TButton",
    background=[("active", COULEUR_ACCENT_SURVOL)]
)

style.configure(
    "Clear.TButton",
    background="#fecaca",
    font=("Arial", 12, "bold"),
    borderwidth=1
)

style.map(
    "Clear.TButton",
    background=[("active", "#fca5a5")]
)


# Type de fonction aseho par défaut.
type_fonction_var = tk.StringVar(
    value="Affine"
)

# Ity dictionnaire ity no hitahirizana ny champ rehetra.
champs = {}


# ============================================================
# PARTIE GAUCHE : PARAMETRES
# ============================================================

cadre_gauche = ttk.Frame(
    fenetre
)

cadre_gauche.pack(
    side="left",
    fill="y",
    padx=20,
    pady=20
)


ttk.Label(
    cadre_gauche,
    text="Étude d'une fonction",
    font=("Arial", 20, "bold"),
    foreground=COULEUR_ACCENT
).pack(
    pady=15
)


ttk.Label(
    cadre_gauche,
    text="Choisir le type de fonction :"
).pack(
    pady=5
)


# Liste déroulante ampiasaina hisafidianana ny
# type de fonction tiana hianarana.
liste_fonctions = ttk.Combobox(
    cadre_gauche,
    textvariable=type_fonction_var,

    values=[
        "Linéaire",
        "Affine",
        "Polynôme",
        "Puissance",
        "Exponentielle",
        "Logarithmique"
    ],

    state="readonly",
    width=25
)

liste_fonctions.pack(
    pady=5
)

liste_fonctions.bind(
    "<<ComboboxSelected>>",
    changer_fonction
)


# Eto no miseho ireo paramètres miankina amin'ny
# fonction voafidy.
cadre_parametres = ttk.LabelFrame(
    cadre_gauche,
    text="Paramètres de la fonction"
)

cadre_parametres.pack(
    pady=20,
    fill="x"
)


# Bouton hanombohana ny calcul sy affichage graphique.
ttk.Button(
    cadre_gauche,
    text="Afficher le graphique",
    style="Accent.TButton",
    command=afficher_graphique
).pack(
    pady=15,
    ipady=5,
    fill="x"
)


# Bouton hanokafana ny calculatrice.
ttk.Button(
    cadre_gauche,
    text="Calculatrice scientifique",
    command=ouvrir_calculatrice
).pack(
    pady=5,
    ipady=5,
    fill="x"
)


# ============================================================
# INFORMATIONS MOMBA NY FONCTION
# ============================================================

cadre_info = ttk.LabelFrame(
    cadre_gauche,
    text="Informations"
)

cadre_info.pack(
    pady=15,
    fill="x"
)


texte_information = tk.StringVar()


ttk.Label(
    cadre_info,
    textvariable=texte_information,
    justify="left",
    wraplength=260
).pack(
    padx=10,
    pady=10
)


# ============================================================
# PARTIE DROITE : GRAPHIQUE
# ============================================================

cadre_graphique = ttk.Frame(
    fenetre
)

cadre_graphique.pack(
    side="right",
    fill="both",
    expand=True,
    padx=10,
    pady=20
)


# Création de la figure Matplotlib.
# Ampiasaina ny Figure mivantana (fa tsy pyplot) satria
# tsy mila fenêtre matplotlib faharoa isika ao anaty Tkinter a.
figure = Figure(
    figsize=(7, 5),
    dpi=100,
    facecolor=COULEUR_FOND,
    layout="tight"
)

ax = figure.add_subplot(111)

ax.set_title(
    "Graphique"
)

ax.set_xlabel(
    "x"
)

ax.set_ylabel(
    "f(x)"
)

ax.grid(True, linestyle="--", alpha=0.4)


# Ampidirina ao anatin'ny interface Tkinter
# ilay graphique Matplotlib.
canvas = FigureCanvasTkAgg(
    figure,
    master=cadre_graphique
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


# ============================================================
# INITIALISATION
# ============================================================

# Rehefa manomboka ny programme dia aseho avy hatrany
# ireo paramètres an'ny fonction affine.
changer_fonction()


# Manomboka eto ny boucle principale an'i Tkinter.
fenetre.mainloop()