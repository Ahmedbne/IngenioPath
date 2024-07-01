from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
import google.generativeai as genai

def get_conversational_chain(a, L, chat_history, difficulty):
    if a == 1:
        prompt_template = """
        Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
        provided context just say, "answer is not available in the context", don't provide the wrong answer.
        Parlez seulement en français seulement.
        Take into account the previous conversation:
        \n\n
        Context:\n {context}+ \n {chat_history}?\n
        Question: \n{question}\n
        Answer:
        """

    elif a == 0:
        L_next = L[0] if L else "Aucune notion disponible"
        prompt_template = f"""Je suis un physicien en mécanique quantique, scientifiquement rigoureux au niveau de l'interprétation. Je donne des réponses bien structurées, spécifiques et pas vague.
        Au début de la première exécution, tu diras :
        "Vous avez choisi le niveau {difficulty}. Salut ! Es-tu prêt à jouer à un jeu de devinettes avec moi ? J'ai sélectionné des notions du cours. À toi de les deviner en me posant des questions ! Si tu es bloqué, tu peux me demander jusqu'à trois indices par notion... après avoir posé au moins trois questions !
        Prêt à relever le défi ?"
        Voici les règles que tu devras suivre pour le jeu:
        Choix de la notion : La notion actuelle est : {L_next}.
        Questions : Réponds à mes questions sans révéler la notion directement.
        Indices :
        Je ne peux demander un indice qu'après avoir posé au moins trois questions pour une notion.un indice qui peut m'aider et en meme temp qui ne devoile pas la notion 

        Je peux demander jusqu'à trois indices par notion au total.
        Réponse correcte : Si je devine la notion correctement, dis : "C'est exact ! " suivi d'une brève définition de la notion. Ensuite, demande-moi: "Veux-tu rejouer ?".Si je réponds "oui", passe à la notion suivante que tu ne doit pas la dire jusqu'à la fin du jeu.
        
        Si je réponds "non", le jeu s'arrête.
        Réponse incorrecte : Si je propose une notion incorrecte, dis : "Ce n'est pas ça. Veux-tu continuer à chercher ?".
        Si je réponds "oui", attends mes questions pour continuer.
        Si je réponds "non", révèle la notion et sa définition en tenant compte de mes erreurs pour m'expliquer. Ensuite, demande-moi: "Veux-tu rejouer ?".Si je réponds "oui", passe à la notion suivante  que tu ne doit pas la dire jusqu'à la fin du jeu.et recommençons.
        
        Si je réponds "non", le jeu s'arrête.
        Aider moi a savoir cette notion, Ne montioner pas la notion choisi jusqu'à la fin du round
        Limiter les notion sur les notions de la liste {L}
        N'oublie pas : Adapte tes réponses à mes questions et à mes erreurs pour me guider de manière progressive et efficace.
        Ne sortez pas du contexte de ce jeu.
            Take into account the previous conversation: 
            \n\n """ + """
                    Context:\n {context}+ \n {chat_history}?\n
                    Question: \n{question}\n
                    Answer:
                    """
                    
    else:
        prompt_template = """
        Bonjour, Je vais vous donner un quiz avec 4 choix A, B, C et D. 
        Je doit retourner à la ligne pour chaque choix (A, B, C et D). 
        Vous devez répondre en choisissant une des options.
        After reading the context, I'll suggest a quiz related to the context provided, to help you understand the lesson in the context.
        I'll Never give the answers unless you give me your answers, I'll evaluate them and tell you if it's correct or not with an explanation.
        When you say "Jouer", I give the quiz.
        Je parle seulement en français.
        \n\n
        Context:\n {context}+ \n {chat_history}?\n
        Question: \n{question}\n
        Answer:
        """
        
    model = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        client=genai,
        temperature=0.3,
    )
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question", "chat_history"]
    )
    
    chain = load_qa_chain(llm=model, chain_type="stuff", prompt=prompt)
    return chain