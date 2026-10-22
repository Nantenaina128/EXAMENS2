
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define NB_QUESTIONS 20
#define NB_CHOIX 3
#define NB_QUESTIONS_JEU 10

typedef struct {
    char question[300];
    char choix[NB_CHOIX][150];
    int bonneReponse;
} Question;

// Maka ilay meilleur score efa voatahiry ao anaty fichier
int lireMeilleurScore() {
    FILE *fichier = fopen("meilleur_score.txt", "r");
    int score = 0;

    if (fichier != NULL) {
        fscanf(fichier, "%d", &score);
        fclose(fichier);
    }

    return score;
}

// Mitahiry ny meilleur score vaovao raha misy
void sauvegarderMeilleurScore(int score) {
    FILE *fichier = fopen("meilleur_score.txt", "w");

    if (fichier != NULL) {
        fprintf(fichier, "%d", score);
        fclose(fichier);
    } else {
        printf("Impossible de sauvegarder le score !\n");
    }
}

// Afangaro ny ordre-n'ny questions mba tsy hitovy foana
void melangerQuestions(int indices[]) {
    int i, j, temp;

    for (i = 0; i < NB_QUESTIONS; i++) {
        indices[i] = i;
    }

    for (i = NB_QUESTIONS - 1; i > 0; i--) {
        j = rand() % (i + 1);

        temp = indices[i];
        indices[i] = indices[j];
        indices[j] = temp;
    }
}

// Asehoy ny questions diso sy ny corrections feno
void afficherCorrections(Question questions[], int indices[],
                         int reponsesJoueur[], int nombreQuestions) {
    int i, erreurs = 0;

    printf("\n=============================================\n");
    printf("              CORRECTION DES ERREURS\n");
    printf("=============================================\n");

    for (i = 0; i < nombreQuestions; i++) {
        int q = indices[i];

        if (reponsesJoueur[i] != questions[q].bonneReponse) {
            erreurs++;

            printf("\nQuestion %d : %s\n", i + 1, questions[q].question);

            printf("Votre reponse : %d - %s\n",
                   reponsesJoueur[i],
                   questions[q].choix[reponsesJoueur[i] - 1]);

            printf("La bonne reponse : %d - %s\n",
                   questions[q].bonneReponse,
                   questions[q].choix[questions[q].bonneReponse - 1]);

            printf("---------------------------------------------\n");
        }
    }

    if (erreurs == 0) {
        printf("\nBravo ! Toutes vos reponses sont correctes !\n");
    } else {
        printf("\n%d questions incorrectes. Consultez les corrections !\n",
               erreurs);
    }

    printf("=============================================\n");
}

// Kajio ny score dia asehoy ny resultat final
void afficherResultats(Question questions[], int indices[],
                       int reponsesJoueur[], int nombreQuestions) {
    int i, score = 0, mauvaises = 0;

    for (i = 0; i < nombreQuestions; i++) {
        if (reponsesJoueur[i] == questions[indices[i]].bonneReponse) {
            score++;
        } else {
            mauvaises++;
        }
    }

    printf("\n=============================================\n");
    printf("                RESULTAT FINAL\n");
    printf("=============================================\n");
    printf("Score : %d / %d\n", score, nombreQuestions);
    printf("Bonnes reponses : %d\n", score);
    printf("Mauvaises reponses : %d\n", mauvaises);
    printf("=============================================\n");

    // Rehefa vita ny quiz dia aseho ny questions diso
    afficherCorrections(questions, indices, reponsesJoueur,
                        nombreQuestions);

    // Comparaison amin'ilay meilleur score efa tao aloha
    {
        int meilleurScore = lireMeilleurScore();

        if (score > meilleurScore) {
            printf("\nNOUVEAU MEILLEUR SCORE !\n");
            printf("Ancien meilleur score : %d / %d\n",
                   meilleurScore, nombreQuestions);
            printf("Nouveau meilleur score : %d / %d\n",
                   score, nombreQuestions);

            sauvegarderMeilleurScore(score);
        } else {
            printf("\nMeilleur score actuel : %d / %d\n",
                   meilleurScore, nombreQuestions);
        }
    }
}

int main() {
    Question questions[NB_QUESTIONS] = {
        {"Quelle est l'unite de la force dans le Systeme International ?",
         {"Le newton", "Le joule", "Le watt"}, 1},

        {"Quelle est l'unite de la vitesse dans le Systeme International ?",
         {"Le metre par seconde", "Le kilometre", "Le newton"}, 1},

        {"Quelle force attire les objets vers le centre de la Terre ?",
         {"La force electrique", "La force magnetique", "La force de gravite"}, 3},

        {"Quelle est la formule de la vitesse moyenne ?",
         {"v = d / t", "v = d * t", "v = t / d"}, 1},

        {"Quelle est l'unite de l'energie dans le Systeme International ?",
         {"Le joule", "Le newton", "Le watt"}, 1},

        {"Quelle grandeur physique represente la quantite de matiere d'un objet ?",
         {"La masse", "Le poids", "La vitesse"}, 1},

        {"Quelle est l'unite de la masse dans le Systeme International ?",
         {"Le gramme", "Le kilogramme", "Le newton"}, 2},

        {"Quelle est la formule du poids d'un objet ?",
         {"P = m * g", "P = m / g", "P = g / m"}, 1},

        {"Quelle est l'unite de la puissance electrique ?",
         {"Le volt", "L'ampere", "Le watt"}, 3},

        {"Quelle grandeur electrique se mesure en volts ?",
         {"La tension", "L'intensite", "La resistance"}, 1},

        {"Quelle grandeur electrique se mesure en amperes ?",
         {"La tension", "L'intensite du courant", "La resistance"}, 2},

        {"Quelle est l'unite de la resistance electrique ?",
         {"L'ohm", "Le volt", "L'ampere"}, 1},

        {"Quelle loi relie la tension, la resistance et l'intensite ?",
         {"La loi de Newton", "La loi d'Ohm", "La loi de Joule"}, 2},

        {"Quelle est la formule de la loi d'Ohm ?",
         {"U = R * I", "U = R / I", "U = I / R"}, 1},

        {"Quel appareil permet de mesurer une tension electrique ?",
         {"Un amperemetre", "Un voltmetre", "Un thermometre"}, 2},

        {"Quel appareil permet de mesurer l'intensite du courant ?",
         {"Un amperemetre", "Un voltmetre", "Un barometre"}, 1},

        {"Quelle est approximativement la vitesse de la lumiere dans le vide ?",
         {"30 000 km/s", "300 000 km/s", "3 000 km/s"}, 2},

        {"Comment appelle-t-on le changement de direction de la lumiere lorsqu'elle passe d'un milieu a un autre ?",
         {"La reflexion", "La dispersion", "La refraction"}, 3},

        {"Quel instrument permet de mesurer la temperature ?",
         {"Un thermometre", "Un voltmetre", "Un amperemetre"}, 1},

        {"Comment appelle-t-on l'energie possedee par un objet en mouvement ?",
         {"L'energie thermique", "L'energie cinetique", "L'energie chimique"}, 2}
    };

    int indices[NB_QUESTIONS];
    int reponsesJoueur[NB_QUESTIONS_JEU];
    int i, choixJoueur;

    srand((unsigned int)time(NULL));
    melangerQuestions(indices);

    printf("=============================================\n");
    printf("          QUIZ DE PHYSIQUE EN C\n");
    printf("=============================================\n");
    printf("Bienvenue dans le quiz !\n");
    printf("Allez-y, repondez bien aux questions !\n");

    for (i = 0; i < NB_QUESTIONS_JEU; i++) {
        int q = indices[i];

        printf("\n---------------------------------------------\n");
        printf("Question %d / %d\n", i + 1, NB_QUESTIONS_JEU);
        printf("%s\n\n", questions[q].question);

        printf("1 - %s\n", questions[q].choix[0]);
        printf("2 - %s\n", questions[q].choix[1]);
        printf("3 - %s\n", questions[q].choix[2]);

        do {
            printf("\nVotre reponse (1, 2 ou 3) : ");

            if (scanf("%d", &choixJoueur) != 1) {
                printf("Choix invalide ! Entrez le chiffre 1, 2 ou 3.\n");

                while (getchar() != '\n');
                choixJoueur = 0;
            } else if (choixJoueur < 1 || choixJoueur > 3) {
                printf("Choisissez uniquement 1, 2 ou 3 !\n");
            }

        } while (choixJoueur < 1 || choixJoueur > 3);

        reponsesJoueur[i] = choixJoueur;
    }

    afficherResultats(questions, indices, reponsesJoueur,
                      NB_QUESTIONS_JEU);

    printf("\nMerci d'avoir joue ! Bonne chance pour la prochaine fois !\n");

    return 0;
}
